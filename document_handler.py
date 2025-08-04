import os
import json
import requests
import dashscope
import docx
import PyPDF2
import warnings
import time
from pathlib import Path
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

class DocumentHandler:
    def __init__(self):
        # API配置 - 整合config逻辑
        self.api_key = "sk-b5b5e8b8b6b84b8b8b5b5e8b8b6b84b8b"
        self.model = "qwen-max-2025-01-25"
        
        # Dify配置
        self.dify_api_key = "dataset-Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8"
        self.dify_base_url = "https://api.dify.ai/v1"
        
        # 两个知识库ID
        self.summary_dataset_id = "summary_dataset_id_here"  # 摘要知识库
        self.original_dataset_id = "original_dataset_id_here"  # 原始文档知识库
        
        # 文本分割参数 - 整合config逻辑
        self.chunk_size = 3000
        self.overlap_size = 500
        
        # 支持的文件类型 - 整合config逻辑
        self.supported_extensions = ['.docx', '.pdf', '.md', '.txt']
        
        # 输入和输出目录 - 整合config逻辑
        self.input_dir = "input_files"
        self.summary_output_dir = "summary_results"
        self.cleaned_output_dir = "cleaned_results"
        self.cleaned_summaries_dir = "cleaned_summaries"
        
        # 并发控制
        self.max_workers = 10
        self.retry_delay = 30
        self.max_retries = 3
        
        # 确保目录存在 - 整合config逻辑
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保所有必要的目录存在"""
        directories = [
            self.input_dir,
            self.summary_output_dir,
            self.cleaned_output_dir,
            self.cleaned_summaries_dir
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def process_documents(self, input_dir=None):
        """处理文档的主流程"""
        if input_dir is None:
            input_dir = self.input_dir
            
        print("开始文档处理流程...")
        
        # 1. 摘要提取
        print("\n=== 步骤1: 摘要提取 ===")
        self.extract_summaries(input_dir, self.summary_output_dir)
        
        # 2. 数据清洗 - 原始文档
        print("\n=== 步骤2: 清洗原始文档 ===")
        self.clean_documents(input_dir, self.cleaned_output_dir)
        
        # 3. 数据清洗 - 摘要文档
        print("\n=== 步骤3: 清洗摘要文档 ===")
        self.clean_documents(self.summary_output_dir, self.cleaned_summaries_dir)
        
        # 4. 上传到知识库
        print("\n=== 步骤4: 上传到知识库 ===")
        # 上传清洗后的摘要到摘要知识库
        print("上传摘要到摘要知识库...")
        self.upload_to_dify(self.cleaned_summaries_dir, self.summary_dataset_id)
        
        # 上传清洗后的原始文档到原始文档知识库
        print("上传原始文档到原始文档知识库...")
        self.upload_to_dify(self.cleaned_output_dir, self.original_dataset_id)
        
        # 5. 清理中间文件
        print("\n=== 步骤5: 清理中间文件 ===")
        self.clean_intermediate_files()
        
        print("\n文档处理流程完成！")
    
    def _read_file(self, file_path: str) -> str:
        """读取文件并转换为文本 - 整合document_processor逻辑"""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # 检查文件类型是否支持
        if extension not in self.supported_extensions:
            raise ValueError(f"不支持的文件格式: {extension}")
        
        # 根据文件扩展名选择对应的读取方法
        readers = {
            '.docx': self._read_docx,
            '.pdf': self._read_pdf,
            '.md': self._read_text,
            '.txt': self._read_text
        }
        
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
        """调用阿里云模型生成摘要，带重试机制"""
        dashscope.api_key = self.api_key
        
        prompt = f"""请从以下案例中提取关键信息，按以下结构总结：

【标题】<保持原文标题不变>

- 项目背景
- 主要措施（3-5点）
- 取得成效（2-3项具体成果）
- 经验教训（3-5点）

要求：字数不超过600字

案例[{filename}]：
{text}"""

        for attempt in range(self.max_retries):
            response = dashscope.Generation.call(
                model=self.model,
                prompt=prompt,
                temperature=0.3,
                top_p=0.8
            )
            
            if response and response.output and response.output.text:
                return response.output.text
            
            print(f"摘要生成失败 (尝试 {attempt + 1}/{self.max_retries}): {filename}")
            if attempt < self.max_retries - 1:
                print(f"等待 {self.retry_delay} 秒后重试...")
                time.sleep(self.retry_delay)
        
        return f"摘要生成失败，已重试 {self.max_retries} 次"

    def _clean_text(self, text: str) -> str:
        """清洗文本并提取关键词，带重试机制"""
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
        
        for attempt in range(self.max_retries):
            response = dashscope.Generation.call(
                model=self.model,
                prompt=prompt,
                temperature=0.3,
                top_p=0.8
            )
            
            if response and response.output and response.output.text:
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
            
            print(f"文本清洗失败 (尝试 {attempt + 1}/{self.max_retries})")
            if attempt < self.max_retries - 1:
                print(f"等待 {self.retry_delay} 秒后重试...")
                time.sleep(self.retry_delay)
        
        return f"{text}\n###API调用失败，已重试 {self.max_retries} 次"

    def _process_chunks_parallel(self, chunks):
        """并发处理文本片段，限制并发数为10"""
        results = [None] * len(chunks)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._process_chunk, i, chunk): i 
                      for i, chunk in enumerate(chunks)}
            
            for future in as_completed(futures):
                chunk_index = futures[future]
                results[chunk_index] = future.result()
                
                # 添加短暂延迟，避免API速率限制
                time.sleep(0.5)
        
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