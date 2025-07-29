import os
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from config import Config
from document_processor import DocumentProcessor
from text_splitter import TextSplitter
from llm_client import LLMClient

@dataclass
class ChunkTask:
    """文本片段处理任务"""
    file_path: str
    chunk_index: int
    chunk_text: str
    is_first_chunk: bool

@dataclass
class ProcessResult:
    """文件处理结果"""
    file_path: str
    success: bool
    output_path: str = None
    error: str = None

class DataCleaner:
    """数据清洗器 - 核心处理类"""
    
    def __init__(self, max_workers: int = 10):
        # 初始化组件
        self.doc_processor = DocumentProcessor()
        self.text_splitter = TextSplitter(Config.CHUNK_SIZE, Config.OVERLAP_SIZE)
        self.llm_client = LLMClient()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.max_workers = max_workers
        
        # 确保目录存在
        Config.ensure_directories()
    
    def process_files(self, input_dir: str) -> List[ProcessResult]:
        """批量处理文件"""
        # 获取待处理文件
        files = self._get_files(input_dir)
        if not files:
            print("未找到支持的文件")
            return []
        
        print(f"找到 {len(files)} 个文件")
        
        # 逐个处理文件
        results = []
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] 处理: {Path(file_path).name}")
            result = self._process_single_file(file_path)
            results.append(result)
            
            if result.success:
                print(f"  ✓ 完成: {Path(result.output_path).name}")
            else:
                print(f"  ✗ 失败: {result.error}")
        
        return results
    
    def _get_files(self, input_dir: str) -> List[str]:
        """获取支持的文件列表"""
        files = []
        input_path = Path(input_dir)
        
        if not input_path.exists():
            return files
        
        for file_path in input_path.iterdir():
            if file_path.suffix.lower() in Config.SUPPORTED_EXTENSIONS:
                files.append(str(file_path))
        
        return files
    
    def _process_single_file(self, file_path: str) -> ProcessResult:
        """处理单个文件"""
        try:
            # 读取文件
            text = self.doc_processor.read_file(file_path)
            
            # 分割文本
            chunks = self.text_splitter.split_text(text)
            print(f"  分割成 {len(chunks)} 段")
            
            # 显示并发处理信息
            concurrent_chunks = min(len(chunks), self.max_workers)
            print(f"  同时处理 {concurrent_chunks} 段")
            
            # 并发处理所有片段
            processed_chunks = self._process_chunks_parallel(file_path, chunks)
            
            # 合并结果
            final_content = '\n'.join(processed_chunks)
            
            # 保存结果
            output_path = self._save_result(file_path, final_content)
            
            return ProcessResult(file_path, True, output_path)
            
        except Exception as e:
            return ProcessResult(file_path, False, error=str(e))
    
    def _process_chunks_parallel(self, file_path: str, chunks: List[str]) -> List[str]:
        """并发处理文本片段"""
        # 创建任务
        tasks = []
        for i, chunk in enumerate(chunks):
            task = ChunkTask(file_path, i, chunk, i == 0)
            tasks.append(task)
        
        # 提交任务到线程池
        futures = {self.executor.submit(self._process_chunk, task): task.chunk_index 
                  for task in tasks}
        
        # 收集结果
        results = [None] * len(chunks)
        for future in as_completed(futures):
            chunk_index = futures[future]
            try:
                formatted_chunk = future.result()
                results[chunk_index] = formatted_chunk
            except Exception as e:
                # 处理失败时使用原文本
                original_chunk = chunks[chunk_index]
                if chunk_index == 0:
                    results[chunk_index] = f"{original_chunk}\n###处理失败"
                else:
                    results[chunk_index] = f"&&&&\n{original_chunk}\n###处理失败"
        
        return results
    
    def _process_chunk(self, task: ChunkTask) -> str:
        """处理单个文本片段"""
        # 调用LLM清洗文本
        cleaned_result = self.llm_client.clean_text(task.chunk_text)
        
        # 格式化输出
        if task.is_first_chunk:
            return cleaned_result
        else:
            return f"&&&&\n{cleaned_result}"
    
    def _save_result(self, input_file: str, content: str) -> str:
        """保存清洗结果"""
        input_path = Path(input_file)
        output_filename = f"{input_path.stem}_cleaned.md"
        output_path = Path(Config.OUTPUT_DIR) / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_path)
    
    def shutdown(self):
        """关闭资源"""
        self.executor.shutdown(wait=True)

def main():
    """主函数 - 程序入口"""
    print("数据清洗工具启动")
    
    # 创建清洗器
    cleaner = DataCleaner(max_workers=10)
    
    try:
        # 处理文件
        results = cleaner.process_files(Config.INPUT_DIR)
        
        # 输出结果统计
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        
        print(f"\n处理完成: {success_count}/{total_count} 成功")
        
        # 显示成功的文件
        for result in results:
            if result.success:
                input_name = Path(result.file_path).name
                output_name = Path(result.output_path).name
                print(f"  {input_name} -> {output_name}")
        
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"\n程序错误: {e}")
    finally:
        cleaner.shutdown()

if __name__ == "__main__":
    main()