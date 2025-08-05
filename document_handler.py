import os
import time
import json
import warnings
from pathlib import Path
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import dashscope
import docx
import PyPDF2
from dotenv import load_dotenv

class DocumentHandler:
    def __init__(self):
        load_dotenv()
        
        # API配置
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        self.model = 'qwen-max-2025-01-25'
        self.dify_api_key = os.getenv('DIFY_API_KEY')
        self.dify_base_url = os.getenv('DIFY_BASE_URL', 'http://localhost/v1')
        self.summary_dataset_id = os.getenv('SUMMARY_DATASET_ID')
        self.original_dataset_id = os.getenv('ORIGINAL_DATASET_ID')
        
        # 处理参数
        self.chunk_size = 3000
        self.overlap_size = 500
        self.max_workers = 10
        self.max_retries = 3
        
        # Dify参数
        self.parent_mode = "paragraph"
        self.parent_separator = "&&&&"
        self.parent_max_tokens = 4000
        self.subchunk_separator = "###"
        self.subchunk_max_tokens = 96
        
        # 目录
        self.summary_dir = "temp_summaries"
        self.cleaned_original_dir = "temp_cleaned_originals"
        self.cleaned_summary_dir = "temp_cleaned_summaries"
        
        # 确保目录存在
        for directory in ["input_files", self.summary_dir, self.cleaned_original_dir, self.cleaned_summary_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # 内存存储
        self.summaries: Dict[str, str] = {}
        self.cleaned_originals: Dict[str, str] = {}
        self.cleaned_summaries: Dict[str, str] = {}

    def read_file(self, file_path: str) -> str:
        """读取文件内容"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext == '.docx':
            doc = docx.Document(path)
            return '\n'.join([p.text for p in doc.paragraphs])
        elif ext == '.pdf':
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with open(path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    return '\n'.join([page.extract_text() for page in reader.pages])
        else:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()

    def generate_summary(self, text: str, filename: str) -> str:
        """生成摘要"""
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
            
            if attempt < self.max_retries - 1:
                time.sleep(30)
        
        return f"摘要生成失败: {filename}"

    def clean_text_chunks(self, text: str) -> str:
        """分块清洗文本"""
        # 分割文本
        if len(text) <= self.chunk_size:
            chunks = [text]
        else:
            chunks = []
            start = 0
            
            while start < len(text):
                end = start + self.chunk_size
                
                if end < len(text):
                    for char in ['\n\n', '。', '\n', ' ']:
                        search_start = max(start + self.chunk_size - self.overlap_size, start)
                        char_pos = text.rfind(char, search_start, end)
                        if char_pos != -1:
                            end = char_pos + len(char)
                            break
                
                chunk = text[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                
                if end >= len(text):
                    break
                
                start = max(end - self.overlap_size, start + 1)
        
        # 并发清洗
        results = [None] * len(chunks)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.clean_single_chunk, i, chunk): i 
                      for i, chunk in enumerate(chunks)}
            
            for future in as_completed(futures):
                chunk_index = futures[future]
                results[chunk_index] = future.result()
                time.sleep(0.5)
        
        return '\n'.join(results)

    def clean_single_chunk(self, index: int, chunk_text: str) -> str:
        """清洗单个文本块"""
        dashscope.api_key = self.api_key
        
        prompt = f"""请对以下文本进行清洗和关键词提取：

清洗要求：
1. 保持原语言，删除页眉页脚、HTML标签、多余空白
2. 修正段落分割，清理乱码
3. 保留重要信息、数据、地名等
4. 输出纯净的正文内容，不要添加任何标题标记

关键词提取要求：
- 提取8-12个相关关键词
- 重点关注：经营模式、产业类型、技术应用、政策措施
- 关键词要简洁准确，不超过6个字

输出格式（严格按照此格式）：
清洗后文本：
[清洗后的文本内容]
关键词：
关键词1,关键词2,关键词3,关键词4,关键词5

原文本：
{chunk_text}
"""
        
        for attempt in range(self.max_retries):
            response = dashscope.Generation.call(
                model=self.model,
                prompt=prompt,
                temperature=0.3,
                top_p=0.8
            )
            
            if response and response.output and response.output.text:
                result = response.output.text
                
                # 解析结果
                cleaned_text = ""
                keywords = []
                
                if "清洗后文本：" in result and "关键词：" in result:
                    parts = result.split("关键词：")
                    cleaned_text = parts[0].replace("清洗后文本：", "").strip()
                    keyword_part = parts[1].strip()
                    
                    if "原文本：" in keyword_part:
                        keyword_part = keyword_part.split("原文本：")[0].strip()
                    
                    # 提取关键词
                    keyword_part = keyword_part.replace("###", "").replace("[", "").replace("]", "")
                    keyword_part = keyword_part.replace("、", ",").replace("；", ",").replace(";", ",")
                    
                    for kw in keyword_part.split(","):
                        kw = kw.strip()
                        if kw and len(kw) <= 10:
                            keywords.append(kw)
                    
                    if len(keywords) > 12:
                        keywords = keywords[:12]
                    elif len(keywords) < 3:
                        keywords.extend(["补充关键词"] * (3 - len(keywords)))
                else:
                    cleaned_text = result.strip()
                    keywords = ["格式解析失败"]
                
                # 清理文本
                cleaned_text = cleaned_text.replace("###", "").replace("&&&&", "")
                lines = cleaned_text.split('\n')
                cleaned_lines = []
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('**') and not line.startswith('#'):
                        cleaned_lines.append(line)
                
                cleaned_text = '\n'.join(cleaned_lines).strip()
                
                # 格式化结果
                formatted_keywords = "".join([f"{self.subchunk_separator}{kw}" for kw in keywords])
                return f"{cleaned_text}\n{formatted_keywords}"
            
            if attempt < self.max_retries - 1:
                time.sleep(30)
        
        # 失败时返回原文本
        fallback_result = chunk_text.strip()
        if self.parent_separator in fallback_result:
            return fallback_result
        else:
            return f"{self.parent_separator}\n{fallback_result}"

    def upload_to_dify(self, data_dict: Dict[str, str], dataset_id: str, data_type: str) -> bool:
        """上传到Dify知识库"""
        # 获取全局最大case_id
        max_case_id = max(
            self.get_max_case_id(self.summary_dataset_id),
            self.get_max_case_id(self.original_dataset_id)
        )
        
        upload_results = []
        sorted_files = sorted(data_dict.items())
        
        for i, (filename, content) in enumerate(sorted_files):
            case_id = max_case_id + i + 1
            temp_filename = f"{Path(filename).stem}_cleaned_{data_type}.md"
            temp_path = f"temp_{temp_filename}"
            
            # 写临时文件
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 上传文件
            success = self.upload_file(temp_path, temp_filename, case_id, dataset_id)
            upload_results.append(success)
            
            # 删除临时文件
            os.remove(temp_path)
            
            print(f"{'✅' if success else '❌'} 上传: {filename} (case_id: {case_id})")
        
        return all(upload_results)

    def get_max_case_id(self, dataset_id: str) -> int:
        """获取最大case_id"""
        url = f"{self.dify_base_url}/datasets/{dataset_id}/documents"
        headers = {'Authorization': f'Bearer {self.dify_api_key}'}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return 0
            
        documents = response.json().get('data', [])
        max_case_id = 0
        
        for doc in documents:
            for meta in doc.get('doc_metadata', []):
                if meta.get('name') == 'case_id':
                    case_id = meta.get('value')
                    if case_id and str(case_id).isdigit():
                        max_case_id = max(max_case_id, int(case_id))
        
        return max_case_id

    def upload_file(self, file_path: str, filename: str, case_id: int, dataset_id: str) -> bool:
        """上传单个文件"""
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
                    "parent_mode": self.parent_mode,
                    "segmentation": {
                        "separator": self.parent_separator,
                        "max_tokens": self.parent_max_tokens
                    },
                    "subchunk_segmentation": {
                        "separator": self.subchunk_separator,
                        "max_tokens": self.subchunk_max_tokens
                    }
                }
            }
        }
        
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f)}
            data_str = json.dumps(data_payload, ensure_ascii=False)
            response = requests.post(url, headers=headers, files=files, data={'data': data_str})
        
        if response.status_code == 200:
            document_id = response.json()['document']['id']
            return self.update_metadata(document_id, case_id, dataset_id)
        
        return False

    def update_metadata(self, document_id: str, case_id: int, dataset_id: str) -> bool:
        """更新文档元数据"""
        # 获取元数据字段ID
        metadata_url = f"{self.dify_base_url}/datasets/{dataset_id}/metadata"
        headers = {'Authorization': f'Bearer {self.dify_api_key}'}
        response = requests.get(metadata_url, headers=headers)
        
        if response.status_code != 200:
            return False
        
        case_id_field_id = None
        for field in response.json().get('doc_metadata', []):
            if field.get('name') == 'case_id':
                case_id_field_id = field['id']
                break
        
        if not case_id_field_id:
            return False
        
        # 更新元数据
        url = f"{self.dify_base_url}/datasets/{dataset_id}/documents/metadata"
        headers = {
            'Authorization': f'Bearer {self.dify_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "operation_data": [{
                "document_id": document_id,
                "metadata_list": [{
                    "id": case_id_field_id,
                    "value": str(case_id),
                    "name": "case_id"
                }]
            }]
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.status_code == 200

    def process_documents(self, input_dir: str):
        """主处理流程"""
        # 1. 处理中间文件
        for directory, storage in [
            (self.summary_dir, self.summaries),
            (self.cleaned_original_dir, self.cleaned_originals),
            (self.cleaned_summary_dir, self.cleaned_summaries)
        ]:
            if os.path.exists(directory):
                files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
                if files:
                    print(f"发现 {len(files)} 个待处理文件: {directory}")
                    for filename in files:
                        filepath = os.path.join(directory, filename)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            storage[filename] = f.read()
                        print(f"✅ 加载: {filename}")
        
        # 2. 处理新文件
        files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.pdf', '.docx', '.md', '.txt'))]
        
        if files:
            print(f"发现 {len(files)} 个新文件需要处理...")
            
            # 生成摘要
            for filename in files:
                if filename not in self.summaries:
                    filepath = os.path.join(input_dir, filename)
                    text = self.read_file(filepath)
                    summary = self.generate_summary(text, filename)
                    self.summaries[filename] = summary
                    
                    # 保存中间文件
                    summary_path = os.path.join(self.summary_dir, f"{filename}.summary")
                    with open(summary_path, 'w', encoding='utf-8') as f:
                        f.write(summary)
                    print(f"✅ 摘要: {filename}")
            
            # 清洗原始文档
            for filename in files:
                if filename not in self.cleaned_originals:
                    filepath = os.path.join(input_dir, filename)
                    text = self.read_file(filepath)
                    cleaned = self.clean_text_chunks(text)
                    self.cleaned_originals[filename] = cleaned
                    
                    # 保存中间文件
                    original_path = os.path.join(self.cleaned_original_dir, f"{filename}.cleaned_original")
                    with open(original_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned)
                    print(f"✅ 清洗原始: {filename}")
            
            # 删除摘要中间文件
            if os.path.exists(self.summary_dir):
                for filename in os.listdir(self.summary_dir):
                    os.remove(os.path.join(self.summary_dir, filename))
            
            # 清洗摘要
            for filename in files:
                if filename not in self.cleaned_summaries:
                    summary = self.summaries[filename]
                    cleaned_summary = self.clean_text_chunks(summary)
                    self.cleaned_summaries[filename] = cleaned_summary
                    
                    # 保存中间文件
                    summary_path = os.path.join(self.cleaned_summary_dir, f"{filename}.cleaned_summary")
                    with open(summary_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_summary)
                    print(f"✅ 清洗摘要: {filename}")
            
            # 删除原文中间文件
            if os.path.exists(self.cleaned_original_dir):
                for filename in os.listdir(self.cleaned_original_dir):
                    os.remove(os.path.join(self.cleaned_original_dir, filename))
        
        # 3. 上传到知识库
        if self.cleaned_summaries or self.cleaned_originals:
            print("开始上传到Dify知识库...")
            
            summary_success = True
            if self.cleaned_summaries:
                summary_success = self.upload_to_dify(self.cleaned_summaries, self.summary_dataset_id, "summary")
                if summary_success:
                    # 清理摘要中间文件
                    if os.path.exists(self.cleaned_summary_dir):
                        for filename in os.listdir(self.cleaned_summary_dir):
                            os.remove(os.path.join(self.cleaned_summary_dir, filename))
                    print("✅ 摘要上传成功，已清理中间文件")
                else:
                    print("❌ 摘要上传失败，保留中间文件")
            
            original_success = True
            if self.cleaned_originals:
                original_success = self.upload_to_dify(self.cleaned_originals, self.original_dataset_id, "original")
                if original_success:
                    # 清理所有临时目录
                    for temp_dir in [self.summary_dir, self.cleaned_original_dir, self.cleaned_summary_dir]:
                        if os.path.exists(temp_dir):
                            for filename in os.listdir(temp_dir):
                                os.remove(os.path.join(temp_dir, filename))
                    print("✅ 原文上传成功，已清理所有中间文件")
                else:
                    print("❌ 原文上传失败，保留中间文件")
            
            if summary_success and original_success:
                print("✅ 所有文档处理完成！")
            else:
                print("⚠️ 部分上传失败，可重新运行程序继续处理")
        else:
            print("✅ 所有文档处理完成！")

if __name__ == "__main__":
    handler = DocumentHandler()
    handler.process_documents("input_files")