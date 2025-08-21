# 示例代码仅供参考，请勿在生产环境中直接使用
import hashlib
import os
import time

import requests
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models


def check_environment_variables():
    """检查并提示设置必要的环境变量"""
    required_vars = {
        'ALIBABA_CLOUD_ACCESS_KEY_ID': '阿里云访问密钥ID',
        'ALIBABA_CLOUD_ACCESS_KEY_SECRET': '阿里云访问密钥密码',
        'WORKSPACE_ID': '阿里云百炼业务空间ID'
    }
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"错误：请设置 {var} 环境变量 ({description})")
    
    return len(missing_vars) == 0


def calculate_md5(file_path: str) -> str:
    """
    计算文档的MD5值。

    参数:
        file_path (str): 文档本地路径。

    返回:
        str: 文档的MD5值。
    """
    md5_hash = hashlib.md5()

    # 以二进制形式读取文档
    with open(file_path, "rb") as f:
        # 按块读取文档，避免大文档占用过多内存
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()


def get_file_size(file_path: str) -> int:
    """
    获取文档大小（以字节为单位）。
    参数:
        file_path (str): 文档本地路径。
    返回:
        int: 文档大小（以字节为单位）。
    """
    return os.path.getsize(file_path)


# 初始化客户端（Client）
def create_client() -> bailian20231229Client:
    """
    创建并配置客户端（Client）。

    返回:
        bailian20231229Client: 配置好的客户端（Client）。
    """
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    # 下方接入地址以公有云的公网接入地址为例，可按需更换接入地址。
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)


# 申请文档上传租约
def apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id):
    """
    从阿里云百炼服务申请文档上传租约。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        category_id (str): 类目ID。
        file_name (str): 文档名称。
        file_md5 (str): 文档的MD5值。
        file_size (int): 文档大小（以字节为单位）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.ApplyFileUploadLeaseRequest(
        file_name=file_name,
        md_5=file_md5,
        size_in_bytes=file_size,
    )
    runtime = util_models.RuntimeOptions()
    return client.apply_file_upload_lease_with_options(category_id, workspace_id, request, headers, runtime)


# 上传文档到临时存储
def upload_file(pre_signed_url, headers, file_path):
    """
    将文档上传到阿里云百炼服务。
    参数:
        pre_signed_url (str): 上传租约中的 URL。
        headers (dict): 上传请求的头部。
        file_path (str): 文档本地路径。
    """
    with open(file_path, 'rb') as f:
        file_content = f.read()
    upload_headers = {
        "X-bailian-extra": headers["X-bailian-extra"],
        "Content-Type": headers["Content-Type"]
    }
    response = requests.put(pre_signed_url, data=file_content, headers=upload_headers)
    response.raise_for_status()


# 添加文档到类目中
def add_file(client: bailian20231229Client, lease_id: str, parser: str, category_id: str, workspace_id: str):
    """
    将文档添加到阿里云百炼服务的指定类目中。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        lease_id (str): 租约ID。
        parser (str): 用于文档的解析器。
        category_id (str): 类目ID。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    request = bailian_20231229_models.AddFileRequest(
        lease_id=lease_id,
        parser=parser,
        category_id=category_id,
    )
    runtime = util_models.RuntimeOptions()
    return client.add_file_with_options(workspace_id, request, headers, runtime)


# 查询文档的解析状态
def describe_file(client, workspace_id, file_id):
    """
    获取文档的基本信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        file_id (str): 文档ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    runtime = util_models.RuntimeOptions()
    return client.describe_file_with_options(workspace_id, file_id, headers, runtime)


# 初始化知识库（索引）
def create_index(client, workspace_id, file_ids, name, structure_type, source_type, sink_type):
    """
    在阿里云百炼服务中创建知识库（初始化）。
    支持单个文件ID或多个文件ID列表。
    """
    headers = {}
    
    # 确保file_ids是列表格式
    if isinstance(file_ids, str):
        document_ids = [file_ids]
    else:
        document_ids = file_ids
    
    request = bailian_20231229_models.CreateIndexRequest(
        structure_type=structure_type,
        name=name,
        source_type=source_type,
        sink_type=sink_type,
        document_ids=document_ids
    )
    runtime = util_models.RuntimeOptions()
    return client.create_index_with_options(workspace_id, request, headers, runtime)


# 提交索引任务
def submit_index(client, workspace_id, index_id):
    """
    向阿里云百炼服务提交索引任务。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    submit_index_job_request = bailian_20231229_models.SubmitIndexJobRequest(
        index_id=index_id
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_job_with_options(workspace_id, submit_index_job_request, headers, runtime)


# 等待索引任务完成
def get_index_job_status(client, workspace_id, job_id, index_id):
    """
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)


def create_knowledge_base(
        file_path: str,
        workspace_id: str,
        name: str
):
    """
    使用阿里云百炼服务创建知识库。
    参数:
        file_path (str): 文档本地路径。
        workspace_id (str): 业务空间ID。
        name (str): 知识库名称。
    返回:
        str or None: 如果成功，返回知识库ID；否则返回None。
    """
    # 设置默认值
    category_id = 'default'
    parser = 'DASHSCOPE_DOCMIND'
    source_type = 'DATA_CENTER_FILE'
    structure_type = 'unstructured'
    sink_type = 'DEFAULT'
    try:
        # 步骤1：初始化客户端（Client）
        print("步骤1：初始化Client")
        client = create_client()
        # 步骤2：准备文档信息
        print("步骤2：准备文档信息")
        file_name = os.path.basename(file_path)
        file_md5 = calculate_md5(file_path)
        file_size = get_file_size(file_path)
        # 步骤3：申请上传租约
        print("步骤3：向阿里云百炼申请上传租约")
        lease_response = apply_lease(client, category_id, file_name, file_md5, file_size, workspace_id)
        lease_id = lease_response.body.data.file_upload_lease_id
        upload_url = lease_response.body.data.param.url
        upload_headers = lease_response.body.data.param.headers
        # 步骤4：上传文档
        print("步骤4：上传文档到阿里云百炼")
        upload_file(upload_url, upload_headers, file_path)
        # 步骤5：将文档添加到服务器
        print("步骤5：将文档添加到阿里云百炼服务器")
        add_response = add_file(client, lease_id, parser, category_id, workspace_id)
        file_id = add_response.body.data.file_id
        # 步骤6：检查文档状态
        print("步骤6：检查阿里云百炼中的文档状态")
        while True:
            describe_response = describe_file(client, workspace_id, file_id)
            status = describe_response.body.data.status
            print(f"当前文档状态：{status}")
            if status == 'INIT':
                print("文档待解析，请稍候...")
            elif status == 'PARSING':
                print("文档解析中，请稍候...")
            elif status == 'PARSE_SUCCESS':
                print("文档解析完成！")
                break
            else:
                print(f"未知的文档状态：{status}，请联系技术支持。")
                return None
            time.sleep(5)
        # 步骤7：初始化知识库
        print("步骤7：在阿里云百炼中初始化知识库")
        index_response = create_index(client, workspace_id, file_id, name, structure_type, source_type, sink_type)
        index_id = index_response.body.data.id
        # 步骤8：提交索引任务
        print("步骤8：向阿里云百炼提交索引任务")
        submit_response = submit_index(client, workspace_id, index_id)
        job_id = submit_response.body.data.id
        # 步骤9：获取索引任务状态
        print("步骤9：获取阿里云百炼索引任务状态")
        while True:
            get_index_job_status_response = get_index_job_status(client, workspace_id, job_id, index_id)
            status = get_index_job_status_response.body.data.status
            print(f"当前索引任务状态：{status}")
            if status == 'COMPLETED':
                break
            time.sleep(5)
        print("阿里云百炼知识库创建成功！")
        return index_id
    except Exception as e:
        print(f"发生错误：{e}")
        return None


def main():
    if not check_environment_variables():
        print("环境变量校验未通过。")
        return
    file_path = input("请输入您需要上传文档的实际本地路径（以Linux为例：/xxx/xxx/阿里云百炼系列手机产品介绍.docx）：")
    kb_name = input("请为您的知识库输入一个名称：")
    workspace_id = os.environ.get('WORKSPACE_ID')
    create_knowledge_base(file_path, workspace_id, kb_name)

def submit_index_add_documents_job(client, workspace_id, index_id, file_id, source_type):
    """
    向一个非结构化知识库追加导入已解析的文档。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文档ID。
        source_type(str): 数据类型。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    submit_index_add_documents_job_request = bailian_20231229_models.SubmitIndexAddDocumentsJobRequest(
        index_id=index_id,
        document_ids=[file_id],
        source_type=source_type
    )
    runtime = util_models.RuntimeOptions()
    return client.submit_index_add_documents_job_with_options(workspace_id, submit_index_add_documents_job_request, headers, runtime)

def list_index_documents(client, workspace_id, index_id, document_name=None):
    """
    获取指定知识库中一个或多个文档的详细信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        document_name (str, optional): 文档名称，用于过滤。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    list_index_documents_request = bailian_20231229_models.ListIndexDocumentsRequest(
        index_id=index_id,
        document_name=document_name
    )
    runtime = util_models.RuntimeOptions()
    return client.list_index_documents_with_options(workspace_id, list_index_documents_request, headers, runtime)

def get_index_job_status(client, workspace_id, index_id, job_id):
    """
    查询索引任务状态。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        job_id (str): 任务ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    get_index_job_status_request = bailian_20231229_models.GetIndexJobStatusRequest(
        index_id=index_id,
        job_id=job_id
    )
    runtime = util_models.RuntimeOptions()
    return client.get_index_job_status_with_options(workspace_id, get_index_job_status_request, headers, runtime)

def delete_index_document(client, workspace_id, index_id, file_id):
    """
    从指定的非结构化知识库中永久删除一个或多个文档。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        file_id (str): 文档ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    delete_index_document_request = bailian_20231229_models.DeleteIndexDocumentRequest(
        index_id=index_id,
        document_ids=[file_id]
    )
    runtime = util_models.RuntimeOptions()
    return client.delete_index_document_with_options(workspace_id, delete_index_document_request, headers, runtime)
def list_indices(client, workspace_id):
    """
    获取指定业务空间下一个或多个知识库的详细信息。

    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    list_indices_request = bailian_20231229_models.ListIndicesRequest()
    runtime = util_models.RuntimeOptions()
    return client.list_indices_with_options(workspace_id, list_indices_request, headers, runtime)

if __name__ == '__main__':
    main()