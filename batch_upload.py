# 批量上传文档到阿里云百炼知识库
import os
import glob
from origin import (
    check_environment_variables,
    create_client,
    calculate_md5,
    get_file_size,
    apply_lease,
    upload_file,
    add_file,
    describe_file,
    create_index,
    submit_index,
    get_index_job_status,
    submit_index_add_documents_job
)
import time
from pathlib import Path
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
import requests

from dotenv import load_dotenv
load_dotenv()

def get_supported_files(input_dir):
    """获取目录中支持的文件格式"""
    supported_extensions = ['*.pdf', '*.docx', '*.doc', '*.md', '*.txt']
    all_files = []
    
    for ext in supported_extensions:
        files = glob.glob(os.path.join(input_dir, ext))
        all_files.extend(files)
    
    return all_files

def upload_single_file(client, file_path, workspace_id, category_id='default', parser='DASHSCOPE_DOCMIND'):
    """上传单个文件并返回结果字典"""
    print(f"开始上传文件: {os.path.basename(file_path)}")
    
    file_name = os.path.basename(file_path)
    file_md5 = calculate_md5(file_path)
    file_size = get_file_size(file_path)
    
    lease_response = apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id)
    lease_id = lease_response.body.data.file_upload_lease_id
    upload_url = lease_response.body.data.param.url
    upload_headers = lease_response.body.data.param.headers
    
    upload_file(upload_url, upload_headers, file_path)
    
    add_response = add_file(client, lease_id, parser, category_id, workspace_id)
    file_id = add_response.body.data.file_id
    
    while True:
        describe_response = describe_file(client, workspace_id, file_id)
        status = describe_response.body.data.status
        print(f"文件 {file_name} 状态：{status}")
        if status == 'PARSE_SUCCESS':
            print(f"文件 {file_name} 解析完成！")
            return {"success": True, "file_id": file_id}
        elif status in ['INIT', 'PARSING']:
            time.sleep(5)
        else:
            print(f"文件 {file_name} 解析失败，状态：{status}")
            return {"success": False, "error": f"解析失败，状态：{status}"}

def batch_upload_to_existing_knowledge_base(directory_path, workspace_id, index_id, category_id="default"):
    """批量上传目录中的文档到已有知识库"""
    if not check_environment_variables():
        return {"error": "环境变量未正确设置"}
    
    client = create_client()
    supported_files = get_supported_files(directory_path)
    
    if not supported_files:
        return {"error": "未找到支持的文件格式"}
    
    print(f"找到 {len(supported_files)} 个支持的文件")
    
    # 上传所有文件并收集文档ID
    document_ids = []
    upload_results = []
    
    for file_path in supported_files:
        print(f"正在上传文件: {file_path}")
        result = upload_single_file(client, file_path, workspace_id, category_id)
        
        if result["success"]:
            document_ids.append(result["file_id"])
            upload_results.append(result)
            print(f"文件上传成功: {result['file_id']}")
        else:
            print(f"文件上传失败: {result['error']}")
            upload_results.append(result)
    
    if not document_ids:
        return {"error": "没有文件上传成功"}
    
    # 向已有知识库添加文档
    print(f"向知识库 {index_id} 添加 {len(document_ids)} 个文档")
    
    # 为每个文档调用追加函数
    job_ids = []
    for file_id in document_ids:
        add_response = submit_index_add_documents_job(client, workspace_id, index_id, file_id, 'DATA_CENTER_FILE')
        if add_response.status_code == 200:
            job_id = add_response.body.data.id
            job_ids.append(job_id)
            print(f"文档 {file_id} 添加任务已提交，任务ID: {job_id}")
    
    if not job_ids:
        return {"error": "没有文档添加任务提交成功"}
    
    # 等待所有任务完成
    print("等待文档添加任务完成...")
    completed_jobs = 0
    while completed_jobs < len(job_ids):
        completed_jobs = 0
        for job_id in job_ids:
            job_status = get_index_job_status(client, workspace_id, index_id, job_id)
            status = job_status.body.data.status
            if status in ["COMPLETED", "FAILED"]:
                completed_jobs += 1
        
        if completed_jobs < len(job_ids):
            print(f"已完成 {completed_jobs}/{len(job_ids)} 个任务")
            time.sleep(30)
    
    return {
        "success": True,
        "message": f"成功向知识库添加 {len(document_ids)} 个文档",
        "index_id": index_id,
        "job_ids": job_ids,
        "document_ids": document_ids,
        "upload_results": upload_results
    }

if __name__ == '__main__':
    # 使用示例
    directory_path = "./input_files"  # 替换为您的文档目录路径
    workspace_id = os.environ.get('WORKSPACE_ID')  # 从环境变量获取
    index_id = os.environ.get("BAILIAN_DATASET_ID")  # 替换为您已有的知识库ID
    
    result = batch_upload_to_existing_knowledge_base(
        directory_path=directory_path,
        workspace_id=workspace_id,
        index_id=index_id
    )
    
    if result.get("success"):
        print(f"批量上传成功！")
        print(f"知识库ID: {result['index_id']}")
        print(f"任务IDs: {result['job_ids']}")
        print(f"上传的文档数量: {len(result['document_ids'])}")
    else:
        print(f"批量上传失败: {result.get('error')}")