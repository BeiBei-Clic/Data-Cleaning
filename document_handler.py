import os
import time
import json
import warnings
from pathlib import Path
from typing import Dict

import requests
import docx
import PyPDF2
from dotenv import load_dotenv
from openai import OpenAI

class DocumentHandler:
    def __init__(self):
        """
        ========================================
        文档处理器初始化 - 新手使用指南
        ========================================
        
        🚀 快速开始步骤：
        1. 创建 .env 文件并配置必要参数（见下方详细说明）
        2. 创建 input_files 文件夹，放入要处理的文档
        3. 运行程序：python document_handler.py
        
        📋 必需的 .env 文件配置：
        创建项目根目录下的 .env 文件，包含以下内容：
        
        # 大模型API配置（用于生成摘要和清洗文本不一定是OPENROUTER，记得在init那里改成你对应的就行）
        OPENROUTER_API_KEY=your_openrouter_api_key_here
        OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
        
        # Dify知识库配置（用于存储处理后的文档）
        DIFY_API_KEY=your_dify_api_key_here
        DIFY_BASE_URL=http://your_dify_server_url/v1
        SUMMARY_DATASET_ID=your_summary_dataset_id_here（存放摘要的知识库）
        ORIGINAL_DATASET_ID=your_original_dataset_id_here（存放原文的知识库）
        
        📁 文件夹说明：
        - input_files/          : 【必须创建】放入要处理的文档（PDF、Word、MD、TXT）
        - temp_summaries/       : 【自动创建】临时存储生成的摘要文件
        - temp_cleaned_originals/ : 【自动创建】临时存储清洗后的原文
        - temp_cleaned_summaries/ : 【自动创建】临时存储清洗后的摘要
        
        ⚠️ 重要提醒：
        如果 temp_ 开头的文件夹已存在，请先手动删除！
        这些是中间处理文件，可能包含上次未完成的数据。
        
        🔧 可调参数说明：
        下方参数可根据需求调整，无需修改代码其他部分
        """
        
        # 加载环境变量配置
        load_dotenv()
        
        # ==================== 大模型配置 ====================
        # 用于生成摘要和清洗文本的AI模型配置
        self.client = OpenAI(
            api_key=os.getenv('OPENROUTER_API_KEY'),    # 从.env文件读取API密钥
            base_url=os.getenv('OPENROUTER_BASE_URL')   # 从.env文件读取API地址
        )
        
        # 🔧 可调参数：选择使用的模型
        # 推荐模型：'google/gemini-2.5-flash' (快速便宜)
        # 其他选择：'anthropic/claude-3-haiku', 'openai/gpt-4o-mini'
        self.model = 'google/gemini-2.5-flash'
        
        # ==================== Dify知识库配置 ====================
        # Dify是用于存储和管理处理后文档的知识库系统
        self.dify_api_key = os.getenv('DIFY_API_KEY')                    # Dify API密钥
        self.dify_base_url = os.getenv('DIFY_BASE_URL', 'http://localhost/v1')  # Dify服务地址
        self.summary_dataset_id = os.getenv('SUMMARY_DATASET_ID')       # 摘要知识库ID
        self.original_dataset_id = os.getenv('ORIGINAL_DATASET_ID')     # 原文知识库ID
        
        # ==================== 文本处理参数 ====================
        # 🔧 可调参数：文本分块处理设置
        self.chunk_size = 3000      # 每个文本块的最大字符数（建议2000-5000）
        self.overlap_size = 500     # 文本块之间的重叠字符数（建议chunk_size的10-20%）
        self.max_retries = 3        # API调用失败时的最大重试次数
        
        # ==================== Dify知识库分块参数 ====================
        # 这些参数控制文档在Dify中的存储和检索方式
        # 🔧 可调参数：根据文档类型和检索需求调整
        self.parent_mode = "paragraph"          # 父级分块模式：paragraph(段落) 或 sentence(句子)
        self.parent_separator = "&&&&"          # 父级分块分隔符（不要修改，除非了解Dify机制）
        self.parent_max_tokens = 4000           # 父级分块最大token数（建议3000-6000）
        self.subchunk_separator = "###"         # 子分块分隔符（用于关键词标记）
        self.subchunk_max_tokens = 96           # 子分块最大token数（建议64-128）
        
        # ==================== 临时文件夹配置 ====================
        # 程序运行过程中的中间文件存储位置
        self.summary_dir = "temp_summaries"              # 存储生成的摘要
        self.cleaned_original_dir = "temp_cleaned_originals"  # 存储清洗后的原文
        self.cleaned_summary_dir = "temp_cleaned_summaries"   # 存储清洗后的摘要
        
        # 自动创建必要的目录
        # input_files: 用户放入原始文档的文件夹
        # temp_*: 程序处理过程中的临时文件夹
        for directory in ["input_files", self.summary_dir, self.cleaned_original_dir, self.cleaned_summary_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # ==================== 内存数据存储 ====================
        # 程序运行时在内存中临时存储处理结果
        self.summaries: Dict[str, str] = {}         # 存储生成的摘要 {文件名: 摘要内容}
        self.cleaned_originals: Dict[str, str] = {} # 存储清洗后的原文 {文件名: 清洗后内容}
        self.cleaned_summaries: Dict[str, str] = {} # 存储清洗后的摘要 {文件名: 清洗后摘要}
        
        print("✅ 文档处理器初始化完成！")
        print("📁 请将要处理的文档放入 input_files/ 文件夹")
        print("📄 支持的文件格式：PDF、Word(.docx)、Markdown(.md)、文本(.txt)")

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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            if response and response.choices and response.choices[0].message.content:
                return response.choices[0].message.content
            
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
        
        # 处理文本块
        results = []
        for i, chunk in enumerate(chunks):
            print(f"正在处理文本块 {i+1}/{len(chunks)}...")
            result = self.clean_single_chunk(i, chunk)
            results.append(result)
        
        # 用&&&&连接各个文本块
        return f"\n{self.parent_separator}\n".join(results)

    def clean_single_chunk(self, index: int, chunk_text: str) -> str:
        """清洗单个文本块"""
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
{chunk_text}
"""
        
        for attempt in range(self.max_retries):
            print(f"  尝试第 {attempt + 1} 次调用API...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            if response and response.choices and response.choices[0].message.content:
                content = response.choices[0].message.content
                
                # 解析清洗后的文本和关键词
                if "清洗后文本：" in content:
                    parts = content.split("关键词：")
                    cleaned_text = parts[0].replace("清洗后文本：", "").strip()
                    keywords = parts[1].split("原文本：")[0].strip()
                    
                    # 格式化关键词
                    keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
                    formatted_keywords = "".join([f"{self.subchunk_separator}{kw}" for kw in keyword_list])
                    
                    print(f"  ✅ 文本块 {index + 1} 处理成功")
                    # 返回格式：正文 + 换行 + 关键词
                    return f"{cleaned_text}\n{formatted_keywords}"
                
                # 如果没有标准格式，直接返回内容
                print(f"  ⚠️ 格式解析失败，使用原始返回内容")
                return f"{content}\n{self.subchunk_separator}处理失败"
            
            if attempt < self.max_retries - 1:
                print(f"  ⚠️ API调用失败，等待30秒后重试...")
                time.sleep(30)
        
        # 失败时返回原文本
        return f"{self.parent_separator}\n{chunk_text.strip()}"

    def upload_to_dify(self, data_dict: Dict[str, str], dataset_id: str, data_type: str) -> bool:
        """上传到Dify知识库"""
        max_case_id = max(
            self.get_max_case_id(self.summary_dataset_id),
            self.get_max_case_id(self.original_dataset_id)
        )
        
        upload_results = []
        sorted_files = sorted(data_dict.items())
        
        for i, (filename, content) in enumerate(sorted_files):
            case_id = max_case_id + i + 1
            temp_filename = f"{Path(filename).stem}_cleaned_{data_type}.md"
            
            # 根据数据类型保存到不同目录
            temp_dir = "temp_cleaned_originals" if data_type == "original" else "temp_cleaned_summaries"
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, temp_filename)
            
            # 写临时文件
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 上传文件
            success = self.upload_file(temp_path, temp_filename, case_id, dataset_id)
            upload_results.append(success)
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

    def upload_paired_documents(self) -> bool:
        """同时上传摘要和原文，确保case_id一致"""
        if not self.cleaned_summaries:
            print("没有清洗后的摘要需要上传")
            return True
            
        # 获取最大case_id
        max_case_id = max(
            self.get_max_case_id(self.summary_dataset_id),
            self.get_max_case_id(self.original_dataset_id)
        )
        
        upload_results = []
        sorted_summaries = sorted(self.cleaned_summaries.items())
        
        for i, (filename, summary_content) in enumerate(sorted_summaries):
            case_id = max_case_id + i + 1
            
            # 检查是否有对应的原文
            original_content = self.cleaned_originals.get(filename)
            if not original_content:
                print(f"⚠️ 文件 {filename} 没有对应的清洗后原文，跳过")
                continue
            
            print(f"正在上传文件对: {filename} (case_id: {case_id})")
            
            # 上传摘要
            summary_filename = f"{Path(filename).stem}_cleaned_summary.md"
            summary_temp_path = os.path.join("temp_cleaned_summaries", summary_filename)
            os.makedirs("temp_cleaned_summaries", exist_ok=True)
            
            with open(summary_temp_path, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            summary_success = self.upload_file(summary_temp_path, summary_filename, case_id, self.summary_dataset_id)
            os.remove(summary_temp_path)
            
            if not summary_success:
                print(f"❌ 摘要上传失败: {filename}")
                upload_results.append(False)
                continue
            
            # 上传原文
            original_filename = f"{Path(filename).stem}_cleaned_original.md"
            original_temp_path = os.path.join("temp_cleaned_originals", original_filename)
            os.makedirs("temp_cleaned_originals", exist_ok=True)
            
            with open(original_temp_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            original_success = self.upload_file(original_temp_path, original_filename, case_id, self.original_dataset_id)
            os.remove(original_temp_path)
            
            if summary_success and original_success:
                print(f"✅ 文件对上传成功: {filename} (case_id: {case_id})")
                upload_results.append(True)
            else:
                print(f"❌ 原文上传失败: {filename}")
                upload_results.append(False)
        
        return all(upload_results)

    def process_documents(self, input_dir: str):
        """主处理流程"""
        
        files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.pdf', '.docx', '.md', '.txt'))]
        
        if files:
            print(f"发现 {len(files)} 个新文件需要处理...")
            
            # 步骤1: 生成摘要
            print("=== 步骤1: 生成摘要 ===")
            for filename in files:
                filepath = os.path.join(input_dir, filename)
                text = self.read_file(filepath)
                summary = self.generate_summary(text, filename)
                self.summaries[filename] = summary
                
                summary_path = os.path.join(self.summary_dir, f"{filename}.summary")
                with open(summary_path, 'w', encoding='utf-8') as f:
                    f.write(summary)
                print(f"✅ 摘要: {filename}")
            
            # 步骤2: 清洗原始文档
            print("=== 步骤2: 清洗原始文档 ===")
            for filename in files:
                filepath = os.path.join(input_dir, filename)
                text = self.read_file(filepath)
                cleaned = self.clean_text_chunks(text)
                self.cleaned_originals[filename] = cleaned
                
                original_path = os.path.join(self.cleaned_original_dir, f"{filename}.cleaned_original")
                with open(original_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                print(f"✅ 清洗原始: {filename}")
            
            # 步骤3: 清洗摘要
            print("=== 步骤3: 清洗摘要 ===")
            for filename in files:
                summary = self.summaries[filename]
                cleaned_summary = self.clean_text_chunks(summary)
                self.cleaned_summaries[filename] = cleaned_summary
                
                summary_path = os.path.join(self.cleaned_summary_dir, f"{filename}.cleaned_summary")
                with open(summary_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_summary)
                print(f"✅ 清洗摘要: {filename}")
        
        # 步骤4: 配对上传到知识库
        if self.cleaned_summaries or self.cleaned_originals:
            print("=== 步骤4: 配对上传到Dify知识库 ===")
            
            upload_success = self.upload_paired_documents()
            
            if upload_success:
                # 清理所有中间文件
                for temp_dir in [self.summary_dir, self.cleaned_original_dir, self.cleaned_summary_dir]:
                    if os.path.exists(temp_dir):
                        for filename in os.listdir(temp_dir):
                            os.remove(os.path.join(temp_dir, filename))
                print("✅ 所有文档配对上传成功，已清理中间文件！")
            else:
                print("⚠️ 部分文档上传失败，保留中间文件以便重新处理")
        else:
            print("✅ 所有文档处理完成！")

if __name__ == "__main__":
    handler = DocumentHandler()
    handler.process_documents("input_files")