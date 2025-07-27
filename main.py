import os
import time
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from threading import Lock
from dataclasses import dataclass
from tqdm import tqdm
import threading

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
class ChunkResult:
    """文本片段处理结果"""
    file_path: str
    chunk_index: int
    formatted_chunk: str
    success: bool
    error: str = None

class GlobalResourcePool:
    """全局资源池，管理并发处理"""
    
    def __init__(self, max_workers: int = 10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.llm_client = LLMClient()
        self.lock = Lock()
        self.active_tasks = {}  # file_path -> set of futures
        self.progress_bars = {}  # file_path -> tqdm progress bar
        
    def submit_chunk_task(self, task: ChunkTask) -> Future:
        """提交文本片段处理任务"""
        future = self.executor.submit(self._process_chunk, task)
        
        with self.lock:
            if task.file_path not in self.active_tasks:
                self.active_tasks[task.file_path] = set()
            self.active_tasks[task.file_path].add(future)
        
        return future
    
    def _process_chunk(self, task: ChunkTask) -> ChunkResult:
        """处理单个文本片段"""
        try:
            # 调用LLM清洗文本，返回格式：原文片段\n###关键词1 ###关键词2
            cleaned_result = self.llm_client.clean_text(task.chunk_text)
            
            # 根据是否是第一个片段来决定格式
            if task.is_first_chunk:
                # 第一个片段不加&&&&前缀
                formatted_chunk = cleaned_result
            else:
                # 后续片段加&&&&前缀
                formatted_chunk = f"&&&&\n{cleaned_result}"
            
            # 更新进度条
            self._update_progress(task.file_path)
            
            return ChunkResult(
                file_path=task.file_path,
                chunk_index=task.chunk_index,
                formatted_chunk=formatted_chunk,
                success=True
            )
            
        except Exception as e:
            # 处理失败时使用原文本
            if task.is_first_chunk:
                formatted_chunk = f"{task.chunk_text}\n###处理失败"
            else:
                formatted_chunk = f"&&&&\n{task.chunk_text}\n###处理失败"
            
            # 更新进度条
            self._update_progress(task.file_path)
            
            return ChunkResult(
                file_path=task.file_path,
                chunk_index=task.chunk_index,
                formatted_chunk=formatted_chunk,
                success=False,
                error=str(e)
            )
    
    def _update_progress(self, file_path: str):
        """更新进度条"""
        with self.lock:
            if file_path in self.progress_bars:
                self.progress_bars[file_path].update(1)
    
    def create_progress_bar(self, file_path: str, total_chunks: int):
        """为文件创建进度条"""
        file_name = Path(file_path).name
        with self.lock:
            self.progress_bars[file_path] = tqdm(
                total=total_chunks,
                desc=f"🔄 {file_name}",
                unit="片段",
                ncols=100,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
            )
    
    def wait_for_file_completion(self, file_path: str, total_chunks: int) -> List[ChunkResult]:
        """等待指定文件的所有任务完成"""
        results = []
        file_name = Path(file_path).name
        
        with self.lock:
            futures = self.active_tasks.get(file_path, set()).copy()
        
        if not futures:
            return results
        
        # 等待所有任务完成
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"\n⚠️  [{file_name}] 任务执行异常: {e}")
        
        # 关闭进度条
        with self.lock:
            if file_path in self.progress_bars:
                self.progress_bars[file_path].close()
                del self.progress_bars[file_path]
            
            # 清理已完成的任务
            if file_path in self.active_tasks:
                del self.active_tasks[file_path]
        
        print(f"✅ [{file_name}] 处理完成!")
        return results
    
    def get_active_task_count(self) -> int:
        """获取当前活跃任务数量"""
        with self.lock:
            return sum(len(futures) for futures in self.active_tasks.values())
    
    def get_active_files(self) -> List[str]:
        """获取当前正在处理的文件列表"""
        with self.lock:
            return [Path(file_path).name for file_path in self.active_tasks.keys()]
    
    def shutdown(self):
        """关闭资源池"""
        # 关闭所有进度条
        with self.lock:
            for pbar in self.progress_bars.values():
                pbar.close()
            self.progress_bars.clear()
        
        self.executor.shutdown(wait=True)

class DataCleaningPipeline:
    """数据清洗流水线"""
    
    def __init__(self, resource_pool: GlobalResourcePool):
        self.config = Config()
        self.doc_processor = DocumentProcessor()
        self.text_splitter = TextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            overlap_size=Config.OVERLAP_SIZE
        )
        self.resource_pool = resource_pool
        
        # 确保目录存在
        Config.ensure_directories()
    
    def process_file(self, file_path: str) -> Dict:
        """处理单个文件"""
        file_name = Path(file_path).name
        print(f"\n{'='*60}")
        print(f"📁 开始处理文件: {file_name}")
        print(f"{'='*60}")
        
        try:
            # 1. 读取文件内容
            print(f"📖 读取文件内容...")
            text = self.doc_processor.read_file(file_path)
            print(f"✅ 文件读取完成，长度: {len(text):,} 字符")
            
            # 2. 分割文本
            print(f"✂️  分割文本...")
            chunks = self.text_splitter.split_text(text)
            print(f"✅ 文本分割完成，共 {len(chunks)} 个片段")
            
            # 3. 创建进度条
            self.resource_pool.create_progress_bar(file_path, len(chunks))
            
            # 4. 提交所有片段到全局资源池
            print(f"🚀 提交片段到处理队列...")
            self._submit_chunks_to_pool(file_path, chunks)
            
            # 5. 等待所有片段处理完成
            results = self.resource_pool.wait_for_file_completion(file_path, len(chunks))
            
            # 6. 按顺序整理结果
            print(f"📋 整理处理结果...")
            processed_chunks = self._organize_results(results, len(chunks))
            
            # 7. 连接所有片段 - 使用换行连接
            final_content = '\n'.join(processed_chunks)
            
            # 8. 保存结果
            print(f"💾 保存处理结果...")
            output_path = self._save_result(file_path, final_content, len(chunks))
            
            result = {
                'status': 'success',
                'input_file': file_path,
                'output_file': output_path,
                'original_length': len(text),
                'final_length': len(final_content),
                'chunks_count': len(chunks)
            }
            
            print(f"🎉 文件处理完成: {Path(output_path).name}")
            print(f"{'='*60}")
            return result
            
        except Exception as e:
            print(f"❌ 文件处理失败: {e}")
            print(f"{'='*60}")
            return {
                'status': 'error',
                'input_file': file_path,
                'error': str(e)
            }
    
    def _submit_chunks_to_pool(self, file_path: str, chunks: List[str]):
        """将所有文本片段提交到全局资源池"""
        for i, chunk in enumerate(chunks):
            task = ChunkTask(
                file_path=file_path,
                chunk_index=i,
                chunk_text=chunk,
                is_first_chunk=(i == 0)
            )
            self.resource_pool.submit_chunk_task(task)
        
        active_count = self.resource_pool.get_active_task_count()
        print(f"✅ 已提交 {len(chunks)} 个片段，当前队列: {active_count} 个任务")
    
    def _organize_results(self, results: List[ChunkResult], total_chunks: int) -> List[str]:
        """按顺序整理处理结果"""
        # 按chunk_index排序
        results.sort(key=lambda x: x.chunk_index)
        
        # 检查是否所有片段都处理完成
        if len(results) != total_chunks:
            raise Exception(f"片段处理不完整: 期望{total_chunks}个，实际{len(results)}个")
        
        # 统计成功和失败的片段
        success_count = sum(1 for r in results if r.success)
        failure_count = total_chunks - success_count
        
        print(f"📈 处理统计: ✅成功 {success_count} 个，❌失败 {failure_count} 个")
        
        if failure_count > 0:
            print("⚠️  失败的片段:")
            for result in results:
                if not result.success:
                    print(f"   ❌ 片段 {result.chunk_index + 1}: {result.error}")
        
        return [result.formatted_chunk for result in results]
    
    def _save_result(self, input_file: str, content: str, chunks_count: int) -> str:
        """保存清洗结果"""
        input_path = Path(input_file)
        output_filename = f"{input_path.stem}_cleaned.md"
        output_path = Path(Config.OUTPUT_DIR) / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 结果已保存到: {output_path}")
        return str(output_path)

def main():
    """主函数"""
    print("🚀 数据清洗工具启动")
    print(f"📂 输入目录: {Config.INPUT_DIR}")
    print(f"📁 输出目录: {Config.OUTPUT_DIR}")
    print(f"🔧 全局资源池大小: 10 个并发任务")
    print(f"📋 支持的文件格式: {', '.join(Config.SUPPORTED_EXTENSIONS)}")
    
    # 创建全局资源池
    resource_pool = GlobalResourcePool(max_workers=10)
    
    try:
        # 获取所有待处理文件
        files_to_process = []
        input_dir = Path(Config.INPUT_DIR)
        for file_path in input_dir.iterdir():
            if file_path.suffix.lower() in Config.SUPPORTED_EXTENSIONS:
                files_to_process.append(str(file_path))
        
        if not files_to_process:
            print("❌ 未找到支持的文件格式")
            return
        
        print(f"📊 找到 {len(files_to_process)} 个文件待处理:")
        for i, file_path in enumerate(files_to_process, 1):
            file_size = Path(file_path).stat().st_size
            print(f"   {i}. {Path(file_path).name} ({file_size:,} 字节)")
        
        # 创建数据清洗流水线
        pipeline = DataCleaningPipeline(resource_pool)
        
        # 处理所有文件
        results = []
        for i, file_path in enumerate(files_to_process, 1):
            print(f"\n🔄 处理进度: {i}/{len(files_to_process)}")
            result = pipeline.process_file(file_path)
            results.append(result)
        
        # 输出总结
        print(f"\n{'='*60}")
        print("📊 处理总结")
        print(f"{'='*60}")
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        total_files = len(results)
        
        print(f"📁 总文件数: {total_files}")
        print(f"✅ 成功处理: {success_count}")
        print(f"❌ 处理失败: {total_files - success_count}")
        
        if success_count > 0:
            print(f"\n📋 成功处理的文件:")
            for result in results:
                if result['status'] == 'success':
                    print(f"   ✅ {Path(result['input_file']).name} -> {Path(result['output_file']).name}")
                    print(f"      📊 {result['original_length']:,} -> {result['final_length']:,} 字符")
                    print(f"      🧩 {result['chunks_count']} 个片段")
        
        if total_files - success_count > 0:
            print(f"\n❌ 处理失败的文件:")
            for result in results:
                if result['status'] == 'error':
                    print(f"   ❌ {Path(result['input_file']).name}: {result['error']}")
        
        print(f"\n🎉 数据清洗完成!")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  用户中断操作")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
    finally:
        # 关闭资源池
        resource_pool.shutdown()
        print("🔚 资源池已关闭")

if __name__ == "__main__":
    main()