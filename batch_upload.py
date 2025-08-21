# 批量上传文档到阿里云百炼知识库
import os
import glob
import time
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
    submit_index_add_documents_job
)
from dotenv import load_dotenv

load_dotenv()

def batch_upload_to_existing_knowledge_base(directory_path, workspace_id, index_id):
    """批量上传目录中的文档到已有知识库"""
    # 检查环境变量
    if not check_environment_variables():
        return {"error": "环境变量未正确设置"}
    
    # 创建客户端
    client = create_client()
    
    # 获取支持的文件格式
    supported_extensions = ['*.pdf', '*.docx', '*.doc', '*.md', '*.txt']
    all_files = []
    for ext in supported_extensions:
        all_files.extend(glob.glob(os.path.join(directory_path, ext)))
    
    if not all_files:
        return {"error": "未找到支持的文件格式"}
    
    print(f"找到 {len(all_files)} 个支持的文件")
    
    # 批量上传文件并收集文档ID
    document_ids = []
    for file_path in all_files:
        print(f"正在上传文件: {os.path.basename(file_path)}")
        
        # 计算文件信息
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
                document_ids.append(file_id)
                print(f"文件 {file_name} 解析完成！")
                break
            elif status in ['INIT', 'PARSING']:
                time.sleep(5)
            else:
                print(f"文件 {file_name} 解析失败，状态：{status}")
                break
    
    if not document_ids:
        return {"error": "没有文件上传成功"}
    
    # 向已有知识库添加文档
    print(f"向知识库 {index_id} 添加 {len(document_ids)} 个文档")
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
    while True:
        completed_jobs = 0
        for job_id in job_ids:
            job_status = get_index_job_status(client, workspace_id, index_id, job_id)
            status = job_status.body.data.status
            if status in ["COMPLETED", "FAILED"]:
                completed_jobs += 1
        
        if completed_jobs == len(job_ids):
            break
        
        print(f"已完成 {completed_jobs}/{len(job_ids)} 个任务")
        time.sleep(30)
    
    return {
        "success": True,
        "message": f"成功向知识库添加 {len(document_ids)} 个文档",
        "index_id": index_id,
        "document_ids": document_ids
    }

if __name__ == '__main__':
    # 配置参数
    directory_path = "./input_files"  # 文档目录路径
    workspace_id = os.environ.get('WORKSPACE_ID')  # 工作空间ID
    index_id = os.environ.get("BAILIAN_DATASET_ID")  # 知识库ID
    
    # 执行批量上传
    result = batch_upload_to_existing_knowledge_base(directory_path, workspace_id, index_id)
    
    # 输出结果
    if result.get("success"):
        print(f"\n批量上传成功！")
        print(f"知识库ID: {result['index_id']}")
        print(f"上传的文档数量: {len(result['document_ids'])}")
    else:
        print(f"\n批量上传失败: {result.get('error')}")