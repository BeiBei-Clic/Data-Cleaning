import os
from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# 阿里云百炼配置常量
WORKSPACE_ID = os.environ.get('WORKSPACE_ID', '')
SUMMARY_INDEX_ID = os.environ.get('BAILIAN_SUMMARY_DATASET_ID', '')  # 摘要知识库ID
ORIGINAL_INDEX_ID = os.environ.get('BAILIAN_ORIGINAL_DATASET_ID', '')  # 原文知识库ID

def create_bailian_client() -> bailian20231229Client:
    """创建阿里云百炼客户端"""
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID', ''),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET', '')
    )
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

def retrieve_index(client, workspace_id, index_id, query):
    """
    在指定的知识库中检索信息。
        
    参数:
        client (bailian20231229Client): 客户端（Client）。
        workspace_id (str): 业务空间ID。
        index_id (str): 知识库ID。
        query (str): 原始输入prompt。

    返回:
        阿里云百炼服务的响应。
    """
    headers = {}
    retrieve_request = bailian_20231229_models.RetrieveRequest(
        index_id=index_id,
        query=query
    )
    runtime = util_models.RuntimeOptions()
    return client.retrieve_with_options(workspace_id, retrieve_request, headers, runtime)

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
    # 创建请求对象，只有当document_name不为None时才传递该参数
    if document_name is not None:
        list_index_documents_request = bailian_20231229_models.ListIndexDocumentsRequest(
            index_id=index_id,
            document_name=document_name
        )
    else:
        list_index_documents_request = bailian_20231229_models.ListIndexDocumentsRequest(
            index_id=index_id
        )
    runtime = util_models.RuntimeOptions()
    return client.list_index_documents_with_options(workspace_id, list_index_documents_request, headers, runtime)

def extract_document_ids_from_summary_results(nodes: List) -> List[str]:
    """
    从摘要检索结果中提取文档ID（摘要文件名去掉.md后缀）
    
    参数:
        nodes: 检索结果节点列表
        
    返回:
        List[str]: 提取到的文档ID列表
    """
    document_ids = []
    
    for node in nodes:
        # 尝试从元数据中获取文档名称
        metadata = getattr(node, 'metadata', {}) if hasattr(node, 'metadata') else {}
        
        # 检查元数据中是否有document_name字段
        if isinstance(metadata, dict):
            document_name = metadata.get('document_name') or metadata.get('doc_name') or metadata.get('file_name')
            if document_name:
                # 从文档名称中提取文档ID（去掉.md后缀）
                if document_name.endswith('.md'):
                    doc_id = document_name[:-3]  # 去掉.md后缀
                    if doc_id and doc_id not in document_ids:
                        document_ids.append(doc_id)
                else:
                    # 如果不是.md格式，直接使用
                    if document_name not in document_ids:
                        document_ids.append(document_name)
        
        # 如果元数据中没有找到，尝试从其他可能的字段获取
        if not document_ids:
            # 检查是否有其他可能包含文档名的字段
            for field_name in ['title', 'filename', 'name']:
                field_value = metadata.get(field_name)
                if field_value and field_value.endswith('.md'):
                    doc_id = field_value[:-3]
                    if doc_id and doc_id not in document_ids:
                        document_ids.append(doc_id)
                    break
        
    return document_ids

def retrieve_full_document_by_id(client, workspace_id, index_id, document_id: str) -> Optional[str]:
    """
    通过文档ID从原文知识库中检索完整文档内容，使用精确匹配，按存储顺序返回
    """
    headers = {}
    
    # 构建元数据过滤器，精确匹配doc_id字段
    search_filters = [{
        "doc_id": document_id  # 精确匹配，不使用like
    }]
    
    retrieve_request = bailian_20231229_models.RetrieveRequest(
        index_id=index_id,
        query=document_id,  # 使用文档ID作为查询词
        search_filters=search_filters
    )
    
    runtime = util_models.RuntimeOptions()
    response = client.retrieve_with_options(workspace_id, retrieve_request, headers, runtime)
    
    if response.status_code == 200 and hasattr(response.body, 'data'):
        nodes = response.body.data.nodes if hasattr(response.body.data, 'nodes') else []
        if nodes:
            # 定义排序函数，从_id中提取数字索引
            def get_sort_key(node):
                # 尝试从元数据中获取_id
                metadata = getattr(node, 'metadata', {}) if hasattr(node, 'metadata') else {}
                if isinstance(metadata, dict):
                    node_id = metadata.get('_id', '')
                    if node_id:
                        # 从_id末尾提取数字部分，格式: {前缀}_{chunk_index}_{sub_index}
                        parts = node_id.split('_')
                        if len(parts) >= 2:
                            try:
                                # 取最后两个数字部分作为排序键
                                chunk_index = int(parts[-2]) if parts[-2].isdigit() else 0
                                sub_index = int(parts[-1]) if parts[-1].isdigit() else 0
                                return (chunk_index, sub_index)
                            except (ValueError, IndexError):
                                pass
                
                # 如果无法从_id提取，尝试其他字段
                if isinstance(metadata, dict):
                    page_number = metadata.get('page_number')
                    if page_number is not None:
                        try:
                            return (int(page_number), 0)
                        except (ValueError, TypeError):
                            pass
                
                # 默认返回(0, 0)
                return (0, 0)
            
            # 按照提取的索引进行排序
            nodes = sorted(nodes, key=get_sort_key)
            
            # 提取所有匹配文档的文本内容
            full_content = []
            for node in nodes:
                text = getattr(node, 'text', '') if hasattr(node, 'text') else ''
                if text.strip():
                    # 过滤掉元数据信息，只保留纯文本
                    lines = text.split('\n')
                    clean_lines = []
                    for line in lines:
                        if not (line.strip().startswith('📋 元数据:') or 
                               line.strip().startswith('元数据:') or
                               line.strip().startswith('文档ID:') or
                               line.strip().startswith('来源:')):
                            clean_lines.append(line)
                    
                    clean_text = '\n'.join(clean_lines).strip()
                    if clean_text:
                        full_content.append(clean_text)
            
            if full_content:
                return '\n\n'.join(full_content)
    
    return None
    
@tool
def dual_stage_retrieve(query: str, top_k: int = 3) -> str:
    """
    乡村振兴案例双阶段检索工具：先从摘要库检索，再获取完整案例。
    
    这个工具专门用于检索乡村振兴相关案例信息：
    1. 第一阶段：在摘要知识库中检索匹配的案例摘要
    2. 第二阶段：获取完整的案例详细内容
    
    适用于查询乡村振兴、农业发展、产业化经营等相关案例。
    
    Args:
        query (str): 检索关键词，建议使用3-5个核心关键词，如"生态农业 产业化"
        top_k (int, optional): 返回的最大结果数量，默认为3
        
    Returns:
        str: 格式化的检索结果，包含相关案例的完整内容
        
    Example:
        >>> result = dual_stage_retrieve("生态农业 可持续性")
        >>> result = dual_stage_retrieve("乡村旅游 产业融合")
        >>> result = dual_stage_retrieve("合作社 经营模式")
    """
    
    # 直接使用环境变量，不再作为参数
    ws_id = WORKSPACE_ID
    summary_idx_id = SUMMARY_INDEX_ID
    original_idx_id = ORIGINAL_INDEX_ID
    
    if not ws_id or not summary_idx_id or not original_idx_id:
        return "❌ 错误：知识库配置缺失。请检查环境变量配置。"
    
    # 创建客户端
    client = create_bailian_client()
    
    try:
        # 第一阶段：从摘要知识库检索
        print(f"🔍 第一阶段：在摘要知识库中检索 '{query}'...")
        summary_result = retrieve_index(client, ws_id, summary_idx_id, query)
        
        if not summary_result or not hasattr(summary_result, 'body'):
            return f"❌ 第一阶段检索失败：无法从摘要知识库中获取相关信息"
        
        # 解析摘要检索结果
        summary_nodes = summary_result.body.data.nodes if hasattr(summary_result.body.data, 'nodes') else []
        
        if not summary_nodes:
            return f"🔍 双阶段检索结果:\n- 查询: {query}\n- 摘要知识库: {summary_idx_id}\n- 检索结果: 未找到相关摘要"
        
        # 提取文档ID
        document_ids = extract_document_ids_from_summary_results(summary_nodes[:top_k])
        
        # 格式化输出结果
        result_lines = [
            f"🔍 双阶段检索结果:",
            f"- 查询: {query}",
            f"- 摘要知识库: {summary_idx_id}",
            f"- 原文知识库: {original_idx_id}",
            "",
            f"📋 第一阶段 - 摘要检索结果:",
            f"找到 {len(summary_nodes)} 个相关摘要"
        ]
        
        # 显示摘要内容
        for i, node in enumerate(summary_nodes[:top_k], 1):
            score = getattr(node, 'score', 0) if hasattr(node, 'score') else 0
            text = getattr(node, 'text', '') if hasattr(node, 'text') else ''
            
            result_lines.extend([
                f"\n{'-'*40}",
                f"摘要 {i} (相关度: {score:.3f}):",
                f"{'-'*40}",
                text.strip()[:200] + "..." if len(text.strip()) > 200 else text.strip()
            ])

        print('\n'.join(result_lines))
        result_lines=[]

        # 使用提取的文档ID检索完整内容
        print()
        print(f"📚 第二阶段：使用文档ID {document_ids} 检索完整案例...")
        
        full_cases_found = 0
        for i, doc_id in enumerate(document_ids[:top_k], 1):
            print(f"  正在检索文档ID: {doc_id}")
            full_content = retrieve_full_document_by_id(client, ws_id, original_idx_id, doc_id)
            
            if full_content:
                result_lines.extend([
                    f"\n{'='*50}",
                    f"完整案例 {i} (文档ID: {doc_id}):",
                    f"{'='*50}",
                    full_content
                ])
                full_cases_found += 1
            else:
                result_lines.extend([
                    f"\n⚠️ 文档ID {doc_id} 对应的完整案例未找到"
                ])
        
        if full_cases_found == 0:
            result_lines.append("\n❌ 未能检索到任何完整案例内容")
        else:
            result_lines.insert(-full_cases_found*4-1, f"\n✅ 成功检索到 {full_cases_found} 个完整案例")
        
        return '\n'.join(result_lines)
        
    except Exception as e:
        return f"❌ 双阶段检索过程中发生错误: {str(e)}"

if __name__ == "__main__":
    # 测试双阶段检索功能
    test_query = "生态农业可持续性模式"
    print(f"测试查询: {test_query}")
    print(f"{'='*80}")
    result = dual_stage_retrieve.invoke({"query": test_query})
    print(result)