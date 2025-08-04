import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import Config
from document_processor import DocumentProcessor
from text_splitter import TextSplitter
from llm_client import LLMClient

class DataCleaner:
    """数据清洗器"""
    
    def __init__(self, max_workers: int = 10):
        self.doc_processor = DocumentProcessor()
        self.text_splitter = TextSplitter(Config.CHUNK_SIZE, Config.OVERLAP_SIZE)
        self.llm_client = LLMClient()
        self.max_workers = max_workers
        Config.ensure_directories()
    
    def process_files(self, input_dir: str):
        """批量处理文件"""
        files = [str(f) for f in Path(input_dir).iterdir() 
                if f.suffix.lower() in Config.SUPPORTED_EXTENSIONS]
        
        print(f"找到 {len(files)} 个文件")
        
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] 处理: {Path(file_path).name}")
            self._process_single_file(file_path)
    
    def _process_single_file(self, file_path: str):
        """处理单个文件"""
        # 读取和分割文本
        text = self.doc_processor.read_file(file_path)
        chunks = self.text_splitter.split_text(text)
        print(f"  分割成 {len(chunks)} 段")
        
        # 并发处理片段
        processed_chunks = self._process_chunks_parallel(chunks)
        
        # 保存结果
        final_content = '\n'.join(processed_chunks)
        output_path = self._save_result(file_path, final_content)
        print(f"  ✓ 完成: {Path(output_path).name}")
    
    def _process_chunks_parallel(self, chunks):
        """并发处理文本片段"""
        results = [None] * len(chunks)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            futures = {executor.submit(self._process_chunk, i, chunk): i 
                      for i, chunk in enumerate(chunks)}
            
            # 收集结果
            for future in as_completed(futures):
                chunk_index = futures[future]
                results[chunk_index] = future.result()
        
        return results
    
    def _process_chunk(self, index, chunk_text):
        """处理单个文本片段"""
        cleaned_result = self.llm_client.clean_text(chunk_text)
        
        if index == 0:
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

def main():
    """主函数"""
    print("数据清洗工具启动")
    
    cleaner = DataCleaner(max_workers=10)
    cleaner.process_files(Config.INPUT_DIR)
    
    print("\n处理完成")

if __name__ == "__main__":
    main()