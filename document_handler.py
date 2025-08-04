import os
import json
import requests
import PyPDF2
import docx
import dashscope
import warnings
from pathlib import Path
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import Config

class DocumentHandler:
    """文档处理类，整合摘要提取、数据清洗和知识库上传功能"""
    
    def __init__(self, max_workers: int = 10):
        # 统一使用阿里云模型配置
        self.api_key = "sk-579299350a8048ea9bf905b55fad4b23"
        self.model = "qwen-max-2025-01-25"
        
        # 文本分割配置
        self.chunk_size = Config.CHUNK_SIZE
        self.overlap_size = Config.OVERLAP_SIZE
        
        # 支持的文件格式
        self.supported_extensions = ['.docx', '.pdf', '.md', '.txt']
        
        self.max_workers = max_workers
        
        # 知识库上传配置
        self.dify_api_key = "dataset-nn9K2CMUXa9rSKLlNpMwmHU7"
        self.dify_base_url = "http://localhost/v1"
        
        # 两个不同的知识库ID
        self.summary_dataset_id = "5a36aa21-0aa7-433e-bdab-72aa9931b543"  # 摘要知识库
        self.document_dataset_id = "8e162a14-c930-40a9-8395-39502b58a45b"  # 原始文档知识库，需要替换为实际ID
        
        Config.ensure_directories()
    
    def extract_summary(self, input_dir: str, output_dir: str = "summary_results"):
        """摘要提取方法"""
        os.makedirs(output_dir, exist_ok=True)
        
        files = [f for f in os.listdir(input_dir) 
                if f.lower().endswith(('.pdf', '.docx', '.md', '.txt'))]
        
        print(f"发现 {len(files)} 个文件需要提取摘要")
        
        for filename in files:
            print(f"提取摘要: {filename}")
            
            file_path = os.path.join(input_dir, filename)
            text = self._read_file(file_path)
            summary = self._call_summary_model(text, filename)
            self._save_summary(summary, filename, output_dir)
        
        print(f"摘要提取完成！输出目录: {output_dir}")
    
    def clean_data(self, input_dir: str, output_dir: str = "cleaned_results"):
        """数据清洗方法"""
        os.makedirs(output_dir, exist_ok=True)
        
        files = [str(f) for f in Path(input_dir).iterdir() 
                if f.suffix.lower() in self.supported_extensions]
        
        print(f"找到 {len(files)} 个文件需要清洗")
        
        for i, file_path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] 清洗: {Path(file_path).name}")
            self._clean_single_file(file_path, output_dir)
    
    def upload_summaries_to_knowledge_base(self, summary_dir: str):
        """上传摘要到摘要知识库"""
        max_case_id = self._get_max_case_id(self.summary_dataset_id)
        print(f"摘要知识库当前最大case_id: {max_case_id}")
        
        files = [f for f in os.listdir(summary_dir) 
                if f.lower().endswith(('.md', '.txt'))]
        
        current_case_id = max_case_id + 1
        
        for filename in files:
            self._upload_single_file(summary_dir, filename, current_case_id, self.summary_dataset_id)
            current_case_id += 1
    
    def upload_documents_to_knowledge_base(self, cleaned_dir: str):
        """上传清洗后的原始文档到文档知识库"""
        max_case_id = self._get_max_case_id(self.document_dataset_id)
        print(f"文档知识库当前最大case_id: {max_case_id}")
        
        files = [f for f in os.listdir(cleaned_dir) 
                if f.lower().endswith(('.pdf', '.docx', '.txt', '.md'))]
        
        current_case_id = max_case_id + 1
        
        for filename in files:
            self._upload_single_file(cleaned_dir, filename, current_case_id, self.document_dataset_id)
            current_case_id += 1

    def clean_intermediate_files(self):
        """清空所有中间文件夹"""
        intermediate_dirs = [
            "summary_results",
            "cleaned_results", 
            "cleaned_summaries"
        ]
        
        for dir_name in intermediate_dirs:
            if os.path.exists(dir_name):
                for file in os.listdir(dir_name):
                    file_path = os.path.join(dir_name, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"删除文件: {file_path}")
        
        print("中间文件清理完成")

    def process_documents(self, input_dir: str, 
                         summary_dir: str = "summary_results",
                         cleaned_dir: str = "cleaned_results"):
        """总的文档处理方法，依次执行摘要提取、数据清洗和知识库上传"""
        print("开始文档处理流程...")
        
        # 1. 摘要提取
        print("\n=== 步骤1: 摘要提取 ===")
        self.extract_summary(input_dir, summary_dir)
        
        # 2. 数据清洗（对原始文档）
        print("\n=== 步骤2: 数据清洗原始文档 ===")
        self.clean_data(input_dir, cleaned_dir)
        
        # 3. 数据清洗（对摘要）
        print("\n=== 步骤3: 数据清洗摘要 ===")
        cleaned_summary_dir = "cleaned_summaries"
        self.clean_data(summary_dir, cleaned_summary_dir)
        
        # 4. 上传清洗后的摘要到摘要知识库
        print("\n=== 步骤4: 上传摘要到摘要知识库 ===")
        self.upload_summaries_to_knowledge_base(cleaned_summary_dir)
        
        # 5. 上传清洗后的原始文档到文档知识库
        print("\n=== 步骤5: 上传原始文档到文档知识库 ===")
        self.upload_documents_to_knowledge_base(cleaned_dir)
        
        # 6. 清理中间文件
        print("\n=== 步骤6: 清理中间文件 ===")
        self.clean_intermediate_files()
        
        print("\n文档处理流程完成！")
    
    def _read_file(self, file_path: str) -> str:
        """读取文件并转换为文本 - 整合document_processor逻辑"""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # 根据文件扩展名选择对应的读取方法
        readers = {
            '.docx': self._read_docx,
            '.pdf': self._read_pdf,
            '.md': self._read_text,
            '.txt': self._read_text
        }
        
        if extension not in readers:
            raise ValueError(f"不支持的文件格式: {extension}")
        
        return readers[extension](file_path)
    
    def _read_docx(self, file_path: Path) -> str:
        """读取Word文档"""
        doc = docx.Document(file_path)
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(paragraphs)
    
    def _read_pdf(self, file_path: Path) -> str:
        """读取PDF文档"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pages = [page.extract_text() for page in pdf_reader.pages]
                return '\n'.join(pages)
    
    def _read_text(self, file_path: Path) -> str:
        """读取文本文件（包括txt和md）"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _split_text(self, text: str) -> List[str]:
        """将文本按指定长度分割，保持重复冗余 - 整合text_splitter逻辑"""
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # 计算当前片段的结束位置
            end = start + self.chunk_size
            
            # 如果不是最后一个片段，尝试在合适的位置断开
            if end < len(text):
                # 寻找最近的句号、换行符或空格来断开
                break_chars = ['\n\n', '。', '\n', ' ']
                best_break = end
                
                for char in break_chars:
                    # 在overlap范围内寻找断开点
                    search_start = max(start + self.chunk_size - self.overlap_size, start)
                    char_pos = text.rfind(char, search_start, end)
                    if char_pos != -1:
                        best_break = char_pos + len(char)
                        break
                
                end = best_break
            
            # 提取当前片段
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # 如果已经到达文本末尾，退出循环
            if end >= len(text):
                break
            
            # 计算下一个片段的开始位置（保持重复冗余）
            start = max(end - self.overlap_size, start + 1)
        
        return chunks
    
    def _call_summary_model(self, text, filename):
        """调用阿里云模型生成摘要"""
        dashscope.api_key = self.api_key
        
        prompt = f"""请从以下案例中提取关键信息，按以下结构总结：

【标题】<保持原文标题不变>

- 项目背景
- 主要措施（3-5点）
- 取得成效（2-3项具体成果）
- 经验教训（3-5点）

要求：字数不超过600字

案例[{filename}]：
{text[:8000]}"""

        response = dashscope.Generation.call(
            model=self.model,
            prompt=prompt,
            temperature=0.3,
            top_p=0.8
        )
        return response.output.text
    
    def _clean_text(self, text: str) -> str:
        """清洗文本并提取关键词"""
        dashscope.api_key = self.api_key
        
        prompt = f"""请对以下文本进行清洗和关键词提取：

清洗要求：
1. 保持原语言，删除页眉页脚、HTML标签、多余空白
2. 修正段落分割，清理乱码
3. 保留重要信息、数据、地名等

关键词提取要求：
- 提取8-12个相关关键词
- 重点关注：经营模式、产业类型、技术应用、政策措施

输出格式：
清洗后文本：
[清洗后的文本内容]
关键词：
[关键词1, 关键词2, 关键词3, ...]

原文本：
{text}
"""
        
        response = dashscope.Generation.call(
            model=self.model,
            prompt=prompt,
            temperature=0.3,
            top_p=0.8
        )
        
        content = response.output.text
        
        # 解析响应
        if "清洗后文本：" in content and "关键词：" in content:
            parts = content.split("关键词：")
            cleaned_text = parts[0].replace("清洗后文本：", "").strip()
            keywords = parts[1].strip()
            
            if "原文本：" in keywords:
                keywords = keywords.split("原文本：")[0].strip()
            
            # 格式化关键词
            keyword_list = [kw.strip() for kw in keywords.replace('###', '').split(',') if kw.strip()]
            formatted_keywords = ' '.join([f"###{kw}" for kw in keyword_list])
            return f"{cleaned_text}\n{formatted_keywords}"
        
        return f"{content}\n###处理失败"
    
    def _save_summary(self, content, filename, output_dir):
        """保存摘要结果"""
        output_filename = f"{os.path.splitext(filename)[0]}_summary.md"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"#{os.path.splitext(filename)[0]}案例摘要\n\n")
            f.write(content)
        
        print(f"✅ 生成摘要: {output_filename}")
    
    def _clean_single_file(self, file_path, output_dir):
        """清洗单个文件"""
        # 读取和分割文本
        text = self._read_file(file_path)
        chunks = self._split_text(text)
        print(f"  分割成 {len(chunks)} 段")
        
        # 并发处理片段
        processed_chunks = self._process_chunks_parallel(chunks)
        
        # 保存结果
        final_content = '\n'.join(processed_chunks)
        output_path = self._save_cleaned_result(file_path, final_content, output_dir)
        print(f"  ✓ 完成: {Path(output_path).name}")
    
    def _process_chunks_parallel(self, chunks):
        """并发处理文本片段"""
        results = [None] * len(chunks)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._process_chunk, i, chunk): i 
                      for i, chunk in enumerate(chunks)}
            
            for future in as_completed(futures):
                chunk_index = futures[future]
                results[chunk_index] = future.result()
        
        return results
    
    def _process_chunk(self, index, chunk_text):
        """处理单个文本片段"""
        cleaned_result = self._clean_text(chunk_text)
        
        if index == 0:
            return cleaned_result
        else:
            return f"&&&&\n{cleaned_result}"
    
    def _save_cleaned_result(self, input_file, content, output_dir):
        """保存清洗结果"""
        input_path = Path(input_file)
        output_filename = f"{input_path.stem}_cleaned.md"
        output_path = Path(output_dir) / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_path)
    
    def _get_max_case_id(self, dataset_id):
        """获取指定知识库中当前最大的case_id"""
        url = f"{self.dify_base_url}/datasets/{dataset_id}/documents"
        headers = {'Authorization': f'Bearer {self.dify_api_key}'}
        
        response = requests.get(url, headers=headers)
        documents = response.json().get('data', [])
        max_case_id = 0
        
        for doc in documents:
            doc_metadata = doc.get('doc_metadata', [])
            if doc_metadata:
                for meta in doc_metadata:
                    if meta.get('name') == 'case_id':
                        case_id = meta.get('value')
                        if case_id and str(case_id).isdigit():
                            max_case_id = max(max_case_id, int(case_id))
        
        return max_case_id
    
    def _upload_single_file(self, input_dir, filename, case_id, dataset_id):
        """上传单个文件到指定知识库"""
        file_path = os.path.join(input_dir, filename)
        url = f"{self.dify_base_url}/datasets/{dataset_id}/document/create-by-file"
        headers = {'Authorization': f'Bearer {self.dify_api_key}'}
        
        data_payload = {
            "indexing_technique": "high_quality",
            "doc_form": "hierarchical_model",
            "process_rule": {
                "mode": "hierarchical",
                "rules": {
                    "pre_processing_rules": [
                        {"id": "remove_extra_spaces", "enabled": True},
                        {"id": "remove_urls_emails", "enabled": True}
                    ],
                    "parent_mode": "paragraph",
                    "segmentation": {
                        "separator": "&&&&",
                        "max_tokens": 4000
                    },
                    "subchunk_segmentation": {
                        "separator": "###",
                        "max_tokens": 96
                    }
                }
            }
        }
        
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f)}
            data_str = json.dumps(data_payload, ensure_ascii=False)
            response = requests.post(url, headers=headers, files=files, data={'data': data_str})
        
        if response.status_code == 200:
            result = response.json()
            document_id = result['document']['id']
            
            if self._update_document_metadata(document_id, case_id, dataset_id):
                print(f"上传成功: {filename}, case_id: {case_id}")
            else:
                print(f"上传成功但元数据设置失败: {filename}")
            
            return result
        else:
            print(f"上传失败: {filename}")
            return None
    
    def _update_document_metadata(self, document_id, case_id, dataset_id):
        """更新指定知识库中文档的元数据"""
        metadata_url = f"{self.dify_base_url}/datasets/{dataset_id}/metadata"
        headers = {'Authorization': f'Bearer {self.dify_api_key}'}
        metadata_response = requests.get(metadata_url, headers=headers)
        
        metadata_fields = metadata_response.json().get('doc_metadata', [])
        case_id_field_id = None
        for field in metadata_fields:
            if field.get('name') == 'case_id':
                case_id_field_id = field['id']
                break
        
        if not case_id_field_id:
            print("未找到case_id元数据字段")
            return False
        
        url = f"{self.dify_base_url}/datasets/{dataset_id}/documents/metadata"
        headers = {
            'Authorization': f'Bearer {self.dify_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "operation_data": [
                {
                    "document_id": document_id,
                    "metadata_list": [
                        {
                            "id": case_id_field_id,
                            "value": str(case_id),
                            "name": "case_id"
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.status_code == 200

if __name__ == "__main__":
    # 使用示例
    handler = DocumentHandler()
    
    # 处理input_files目录中的所有文档
    handler.process_documents("input_files")