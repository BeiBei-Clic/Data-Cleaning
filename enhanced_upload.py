import os
import glob
import time
import requests
from pathlib import Path
from origin import (
    check_environment_variables,
    create_client,
    calculate_md5,
    get_file_size,
    apply_lease,
    upload_file,
    add_file,
    describe_file,
    get_index_job_status,
    submit_index_add_documents_job,
)
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class EnhancedUploader:
    def __init__(self):
        # 大模型配置
        self.client = OpenAI(
            api_key=os.getenv('OPENROUTER_API_KEY'),
            base_url=os.getenv('OPENROUTER_BASE_URL')
        )
        self.model = 'google/gemini-2.5-flash'
        
        # minerU API配置
        self.mineru_token = os.getenv('MINERU_API_TOKEN', "官网申请的api token")
        self.mineru_base_url = "https://mineru.net/api/v4"
        
        # 文本处理参数
        self.chunk_size = 20000
        self.overlap_size = 1000
        self.max_retries = 3
    
    def read_file(self, file_path: str) -> str:
        """使用minerU API读取并解析文档内容，返回markdown格式"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        # 对于纯文本文件，直接读取
        if ext in ['.txt', '.md']:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        
        # 对于PDF、DOCX等文档，使用minerU API解析
        if ext in ['.pdf', '.docx', '.doc', '.ppt', '.pptx']:
            return self._parse_with_mineru(file_path)
        
        # 其他格式尝试直接读取
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_with_mineru(self, file_path: str) -> str:
        """使用minerU API解析文档"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.mineru_token}"
        }
        
        # 1. 申请上传URL
        file_name = os.path.basename(file_path)
        upload_data = {
            "enable_formula": True,
            "language": "ch",
            "enable_table": True,
            "files": [
                {"name": file_name, "is_ocr": True, "data_id": file_name}
            ]
        }
        
        response = requests.post(
            f"{self.mineru_base_url}/file-urls/batch",
            headers=headers,
            json=upload_data
        )
        
        if response.status_code != 200:
            print(f"申请上传URL失败: {response.status_code}")
            return ""
        
        result = response.json()
        if result["code"] != 0:
            print(f"申请上传URL失败: {result.get('msg', '未知错误')}")
            return ""
        
        batch_id = result["data"]["batch_id"]
        upload_url = result["data"]["file_urls"][0]
        
        # 2. 上传文件
        with open(file_path, 'rb') as f:
            upload_response = requests.put(upload_url, data=f)
            if upload_response.status_code != 200:
                print(f"文件上传失败: {upload_response.status_code}")
                return ""
        
        print(f"文件 {file_name} 上传成功，开始解析...")
        
        # 3. 等待解析完成并获取结果
        max_wait_time = 300  # 最大等待5分钟
        wait_time = 0
        
        while wait_time < max_wait_time:
            time.sleep(10)
            wait_time += 10
            
            # 查询解析结果
            result_response = requests.get(
                f"{self.mineru_base_url}/extract-results/batch/{batch_id}",
                headers=headers
            )
            
            if result_response.status_code == 200:
                result_data = result_response.json()
                if result_data["code"] == 0:
                    data = result_data["data"]
                    if data and len(data) > 0:
                        # 获取第一个文件的解析结果
                        file_result = data[0]
                        if "md_content" in file_result:
                            print(f"文件 {file_name} 解析完成")
                            return file_result["md_content"]
                        elif "status" in file_result and file_result["status"] == "failed":
                            print(f"文件 {file_name} 解析失败")
                            return ""
            
            print(f"等待解析完成... ({wait_time}s)")
        
        print(f"文件 {file_name} 解析超时")
        return ""
    
    def generate_summary(self, text: str, filename: str) -> str:
        """生成摘要（采用分块清洗相同的分块逻辑）"""
        CHUNK_SIZE = self.chunk_size
        OVERLAP_SIZE = self.overlap_size

        prompt_template = """请从以下文本中提取关键信息作为部分摘要：

当前文档: {filename}
分块: {chunk_num}/{total_chunks}

要求：
1. 提取本部分的核心内容
2. 保持客观事实
3. 用简洁的短语列出要点

文本内容：
{chunk_text}"""

        final_prompt = """请将以下部分摘要合并为完整摘要，按结构整理：

【标题】<保持原文标题不变>

- 项目背景（整合各部分背景）
- 主要措施（合并所有措施，去重后保留3-5点）
- 取得成效（合并量化成果）
- 经验教训（整合关键经验）

要求：最终摘要不超过600字

部分摘要：
{partial_summaries}"""

        # 分块逻辑
        def split_into_chunks(text: str) -> list:
            if len(text) <= CHUNK_SIZE:
                return [text]

            chunks = []
            start = 0
            while start < len(text):
                end = start + CHUNK_SIZE
                if end < len(text):
                    for separator in ['\n\n', '。', '\n', ' ']:
                        search_start = max(start + CHUNK_SIZE - OVERLAP_SIZE, start)
                        split_pos = text.rfind(separator, search_start, end)
                        if split_pos != -1:
                            end = split_pos + len(separator)
                            break
                chunks.append(text[start:end].strip())
                start = max(end - OVERLAP_SIZE, start + 1)
            return chunks

        # 处理单个分块
        def process_chunk(chunk: str, chunk_num: int, total_chunks: int) -> str:
            prompt = prompt_template.format(
                filename=filename,
                chunk_num=chunk_num + 1,
                total_chunks=total_chunks,
                chunk_text=chunk
            )

            for attempt in range(self.max_retries):
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=300
                )
                if response and response.choices:
                    return response.choices[0].message.content
                if attempt < self.max_retries - 1:
                    time.sleep(30)
            return f"[分块{chunk_num + 1}摘要生成失败]"

        # 主流程
        chunks = split_into_chunks(text)
        if len(chunks) == 1:
            # 小文件直接处理
            prompt = f"""请从以下案例中提取关键信息，按以下结构总结：

【标题】<保持原文标题不变>

- 项目背景
- 主要措施（3-5点）
- 取得成效（2-3项具体成果）
- 经验教训（3-5点）

要求：字数不超过600字

案例[{filename}]：
{text}"""
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content

        # 大文件分块处理
        print(f"📑 大文件分块处理: {filename} (共{len(chunks)}块)")

        partial_summaries = []
        for i, chunk in enumerate(chunks):
            print(f"  正在处理分块 {i + 1}/{len(chunks)}...")
            chunk_summary = process_chunk(chunk, i, len(chunks))
            partial_summaries.append(f"=== 分块 {i + 1} ===\n{chunk_summary}")

        # 合并摘要
        print("🔄 合并部分摘要...")
        combined_text = "\n\n".join(partial_summaries)
        final_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": final_prompt.format(partial_summaries=combined_text)}],
            temperature=0.3,
            max_tokens=600
        )
        return final_response.choices[0].message.content
    
    def upload_file_to_knowledge_base(self, file_path: str, workspace_id: str, index_id: str) -> str:
        """上传文件到知识库并返回文档ID"""
        client = create_client()
        
        file_name = os.path.basename(file_path)
        file_md5 = calculate_md5(file_path)
        file_size = get_file_size(file_path)
        
        # 申请上传租约
        lease_response = apply_lease(client, 'default', file_name, file_md5, file_size, workspace_id)
        lease_id = lease_response.body.data.file_upload_lease_id
        upload_url = lease_response.body.data.param.url
        upload_headers = lease_response.body.data.param.headers
        
        # 上传文件
        upload_file(upload_url, upload_headers, file_path)
        
        # 添加文件到服务器
        add_response = add_file(client, lease_id, 'DASHSCOPE_DOCMIND', 'default', workspace_id)
        file_id = add_response.body.data.file_id
        
        # 等待文件解析完成
        while True:
            describe_response = describe_file(client, workspace_id, file_id)
            status = describe_response.body.data.status
            print(f"文件 {file_name} 状态：{status}")
            
            if status == 'PARSE_SUCCESS':
                print(f"文件 {file_name} 解析完成！")
                break
            elif status in ['INIT', 'PARSING']:
                time.sleep(5)
            else:
                print(f"文件 {file_name} 解析失败，状态：{status}")
                return None
        
        # 向知识库添加文档
        add_response = submit_index_add_documents_job(client, workspace_id, index_id, file_id, 'DATA_CENTER_FILE')
        if add_response.status_code == 200:
            job_id = add_response.body.data.id
            print(f"文档 {file_id} 添加任务已提交，任务ID: {job_id}")
            
            # 等待任务完成
            while True:
                job_status = get_index_job_status(client, workspace_id, index_id, job_id)
                status = job_status.body.data.status
                if status == "COMPLETED":
                    print(f"文档 {file_id} 添加完成")
                    return file_id
                elif status == "FAILED":
                    print(f"文档 {file_id} 添加失败")
                    return None
                time.sleep(10)
        
        return None
    
    def upload_summary_to_knowledge_base(self, summary: str, doc_id: str, workspace_id: str, index_id: str) -> bool:
        """将摘要上传到摘要知识库"""
        # 创建临时摘要文件
        temp_summary_path = f"{doc_id}.md"
        with open(temp_summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        # 上传摘要文件
        summary_doc_id = self.upload_file_to_knowledge_base(temp_summary_path, workspace_id, index_id)
        
        # 删除临时文件
        os.remove(temp_summary_path)
        
        return summary_doc_id is not None
    
    def batch_upload_with_summary(self, directory_path: str, workspace_id: str, original_index_id: str, summary_index_id: str):
        """批量上传文档并生成摘要"""
        if not check_environment_variables():
            return {"error": "环境变量未正确设置"}
        
        # 获取支持的文件格式
        supported_extensions = ['*.pdf', '*.docx', '*.doc', '*.md', '*.txt']
        all_files = []
        for ext in supported_extensions:
            all_files.extend(glob.glob(os.path.join(directory_path, ext)))
        
        if not all_files:
            return {"error": "未找到支持的文件格式"}
        
        print(f"找到 {len(all_files)} 个支持的文件")
        
        results = []
        
        for file_path in all_files:
            file_name = os.path.basename(file_path)
            print(f"\n正在处理文件: {file_name}")
            
            # 1. 读取文件内容
            print("📖 读取文件内容...")
            text = self.read_file(file_path)
            
            # 2. 生成摘要
            print("📝 生成摘要...")
            summary = self.generate_summary(text, file_name)
            
            # 3. 上传原文到知识库1
            print("📤 上传原文到原文知识库...")
            doc_id = self.upload_file_to_knowledge_base(file_path, workspace_id, original_index_id)
            
            if doc_id:
                # 4. 上传摘要到知识库2
                print(f"📤 上传摘要到摘要知识库（文档ID: {doc_id}）...")
                summary_success = self.upload_summary_to_knowledge_base(summary, doc_id, workspace_id, summary_index_id)
                
                if summary_success:
                    print(f"✅ 文件 {file_name} 处理完成")
                    results.append({
                        "file": file_name,
                        "status": "success",
                        "doc_id": doc_id
                    })
                else:
                    print(f"❌ 文件 {file_name} 摘要上传失败")
                    results.append({
                        "file": file_name,
                        "status": "summary_upload_failed",
                        "doc_id": doc_id
                    })
            else:
                print(f"❌ 文件 {file_name} 原文上传失败")
                results.append({
                    "file": file_name,
                    "status": "original_upload_failed"
                })
        
        success_count = len([r for r in results if r["status"] == "success"])
        return {
            "success": True,
            "message": f"处理完成，成功: {success_count}/{len(all_files)}",
            "results": results
        }

if __name__ == '__main__':
    # 配置参数
    directory_path = "./input_files"  # 文档目录路径
    workspace_id = os.environ.get('WORKSPACE_ID')  # 工作空间ID
    original_index_id = os.environ.get("BAILIAN_ORIGINAL_DATASET_ID")  # 原文知识库ID
    summary_index_id = os.environ.get("BAILIAN_SUMMARY_DATASET_ID")  # 摘要知识库ID
    
    # 创建上传器并执行批量上传
    uploader = EnhancedUploader()
    result = uploader.batch_upload_with_summary(directory_path, workspace_id, original_index_id, summary_index_id)
    
    # 输出结果
    if result.get("success"):
        print(f"\n{result['message']}")
        for r in result['results']:
            status_icon = "✅" if r['status'] == 'success' else "❌"
            print(f"{status_icon} {r['file']}: {r['status']}")
    else:
        print(f"\n批量上传失败: {result.get('error')}")