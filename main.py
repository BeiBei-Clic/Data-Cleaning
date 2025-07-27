import os
import time
from pathlib import Path
from typing import List, Dict, Tuple
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import Config
from document_processor import DocumentProcessor
from text_splitter import TextSplitter
from llm_client import LLMClient

class DataCleaningPipeline:
    """数据清洗流水线"""
    
    def __init__(self):
        self.config = Config()
        self.doc_processor = DocumentProcessor()
        self.text_splitter = TextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            overlap_size=Config.OVERLAP_SIZE
        )
        self.llm_client = LLMClient()
        
        # 确保目录存在
        Config.ensure_directories()
    
    def process_file(self, file_path: str) -> Dict:
        """处理单个文件"""
        print(f"\n开始处理文件: {file_path}")
        
        try:
            # 1. 读取文件内容
            print("1. 读取文件内容...")
            text = self.doc_processor.read_file(file_path)
            print(f"   文件长度: {len(text)} 字符")
            
            # 2. 分割文本
            print("2. 分割文本...")
            chunks = self.text_splitter.split_text(text)
            print(f"   分割为 {len(chunks)} 个片段")
            
            # 3. 并发清洗文本片段
            print("3. 开始并发清洗文本片段...")
            processed_chunks = self._process_chunks_concurrently(chunks)
            
            # 4. 连接所有片段
            print("4. 格式化输出结果...")
            final_content = '\n'.join(processed_chunks)
            
            # 5. 保存结果
            output_path = self._save_result(file_path, final_content, len(chunks))
            
            result = {
                'status': 'success',
                'input_file': file_path,
                'output_file': output_path,
                'original_length': len(text),
                'final_length': len(final_content),
                'chunks_count': len(chunks)
            }
            
            print(f"✅ 文件处理完成: {output_path}")
            return result
            
        except Exception as e:
            print(f"❌ 文件处理失败: {e}")
            return {
                'status': 'error',
                'input_file': file_path,
                'error': str(e)
            }
    
    def _process_chunks_concurrently(self, chunks: List[str], max_workers: int = 10) -> List[str]:
        """并发处理文本片段"""
        processed_chunks = [''] * len(chunks)  # 预分配列表，保持顺序
        
        # 使用线程池并发处理
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_index = {
                executor.submit(self._process_single_chunk, i, chunk): i 
                for i, chunk in enumerate(chunks)
            }
            
            # 收集结果
            completed_count = 0
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    formatted_chunk = future.result()
                    processed_chunks[index] = formatted_chunk
                    completed_count += 1
                    print(f"   完成片段 {completed_count}/{len(chunks)}")
                except Exception as e:
                    print(f"   片段 {index+1} 处理失败: {e}")
                    # 使用原文本作为备选
                    chunk = chunks[index]
                    if index == 0:
                        processed_chunks[index] = f"{chunk}\n###处理失败"
                    else:
                        processed_chunks[index] = f"&&&&\n{chunk}\n###处理失败"
        
        return processed_chunks
    
    def _process_single_chunk(self, index: int, chunk: str) -> str:
        """处理单个文本片段"""
        try:
            cleaned_text, keywords = self.llm_client.clean_text(chunk)
            
            # 处理关键词：分割并格式化为 ###关键词1 ###关键词2 格式
            if keywords:
                # 分割关键词（支持逗号、分号、中文逗号等分隔符）
                import re
                keyword_list = re.split(r'[,，;；、\s]+', keywords.strip())
                keyword_list = [kw.strip() for kw in keyword_list if kw.strip()]
                formatted_keywords = ' '.join([f'###{kw}' for kw in keyword_list])
            else:
                formatted_keywords = '###无关键词'
            
            # 格式化片段：第一个片段不加前缀&&&&，其他片段前加&&&&
            if index == 0:
                # 第一个片段格式：正文内容\n###关键词
                formatted_chunk = f"{cleaned_text}\n{formatted_keywords}"
            else:
                # 其他片段格式：&&&&\n正文内容\n###关键词
                formatted_chunk = f"&&&&\n{cleaned_text}\n{formatted_keywords}"
            
            return formatted_chunk
            
        except Exception as e:
            raise Exception(f"清洗片段失败: {e}")
    
    def _save_result(self, input_file: str, content: str, chunks_count: int) -> str:
        """保存清洗结果"""
        input_path = Path(input_file)
        output_filename = f"{input_path.stem}_cleaned.md"
        output_path = Path(Config.OUTPUT_DIR) / output_filename
        
        # 直接保存内容，不添加额外的文档信息
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_path)
    
    def process_directory(self, input_dir: str = None) -> List[Dict]:
        """处理目录中的所有文件"""
        input_dir = input_dir or Config.INPUT_DIR
        
        print(f"开始处理目录: {input_dir}")
        
        # 获取所有支持的文件
        files = self.doc_processor.get_files_in_directory(input_dir)
        
        if not files:
            print(f"在目录 {input_dir} 中没有找到支持的文件")
            return []
        
        print(f"找到 {len(files)} 个文件待处理")
        
        results = []
        for file_path in files:
            result = self.process_file(file_path)
            results.append(result)
        
        # 打印总结
        self._print_summary(results)
        
        return results
    
    def _print_summary(self, results: List[Dict]):
        """打印处理总结"""
        success_count = len([r for r in results if r['status'] == 'success'])
        error_count = len([r for r in results if r['status'] == 'error'])
        
        print(f"\n{'='*50}")
        print(f"处理完成!")
        print(f"总文件数: {len(results)}")
        print(f"成功: {success_count}")
        print(f"失败: {error_count}")
        
        if error_count > 0:
            print(f"\n失败的文件:")
            for result in results:
                if result['status'] == 'error':
                    print(f"  - {result['input_file']}: {result['error']}")
        
        print(f"\n清洗结果保存在: {Config.OUTPUT_DIR}")
        print(f"{'='*50}")

def main():
    """主函数"""
    print("数据清洗工具启动")
    print(f"支持的文件格式: {Config.SUPPORTED_EXTENSIONS}")
    print(f"输入目录: {Config.INPUT_DIR}")
    print(f"输出目录: {Config.OUTPUT_DIR}")
    
    # 创建处理流水线
    pipeline = DataCleaningPipeline()
    
    # 处理目录中的所有文件
    results = pipeline.process_directory()
    
    return results

if __name__ == "__main__":
    main()