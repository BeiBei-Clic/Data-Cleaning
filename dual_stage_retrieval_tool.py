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
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
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
    list_index_documents_request = bailian_20231229_models.ListIndexDocumentsRequest(
        index_id=index_id,
        document_name=document_name
    )
    runtime = util_models.RuntimeOptions()
    return client.list_index_documents_with_options(workspace_id, list_index_documents_request, headers, runtime)

def extract_document_ids_from_summary_results(nodes: List) -> List[str]:
    """
    从摘要检索结果中提取文档ID（摘要文件名）
    
    参数:
        nodes: 检索结果节点列表
        
    返回:
        List[str]: 提取到的文档ID列表
    """
    document_ids = []
    
    for node in nodes:
        # 尝试从元数据中获取文档ID
        metadata = getattr(node, 'metadata', {}) if hasattr(node, 'metadata') else {}
        
        # 检查元数据中是否有doc_id字段
        if isinstance(metadata, dict):
            doc_id = metadata.get('doc_id')
            if doc_id:
                # 从完整的doc_id中提取实际的文档ID
                # 格式通常是: file_xxxxx_数字，我们需要提取中间的xxxxx部分
                if 'file_' in doc_id:
                    # 提取file_后面到最后一个下划线之前的部分
                    parts = doc_id.split('_')
                    if len(parts) >= 3:
                        # 重新组合为原始文档ID格式
                        extracted_id = '_'.join(parts[1:-1])  # 去掉file_前缀和最后的数字后缀
                        if extracted_id and extracted_id not in document_ids:
                            document_ids.append(extracted_id)
                else:
                    # 如果不是file_格式，直接使用
                    if doc_id not in document_ids:
                        document_ids.append(doc_id)
        
    return document_ids

def retrieve_full_document_by_id(client, workspace_id, index_id, document_id: str) -> Optional[str]:
    """
    通过文档ID从原文知识库中检索完整文档内容
    
    参数:
        client: 百炼客户端
        workspace_id: 工作空间ID
        index_id: 原文知识库ID
        document_id: 文档ID
        
    返回:
        Optional[str]: 完整文档内容，如果未找到则返回None
    """
    try:
        # 方法1：使用文档ID作为查询词进行检索
        result = retrieve_index(client, workspace_id, index_id, document_id)
        
        if result and hasattr(result, 'body') and hasattr(result.body, 'data'):
            nodes = result.body.data.nodes if hasattr(result.body.data, 'nodes') else []
            if nodes:
                # 合并所有检索到的内容
                full_content = []
                for node in nodes:
                    text = getattr(node, 'text', '') if hasattr(node, 'text') else ''
                    if text.strip():
                        full_content.append(text.strip())
                
                if full_content:
                    return '\n\n'.join(full_content)
        
        # 方法2：尝试通过文档列表API查找特定文档
        doc_list_result = list_index_documents(client, workspace_id, index_id, f"{document_id}.md")
        if doc_list_result and hasattr(doc_list_result, 'body'):
            # 如果找到了文档，再次尝试检索
            result = retrieve_index(client, workspace_id, index_id, f"文档ID:{document_id}")
            if result and hasattr(result, 'body'):
                nodes = result.body.data.nodes if hasattr(result.body.data, 'nodes') else []
                if nodes:
                    full_content = []
                    for node in nodes:
                        text = getattr(node, 'text', '') if hasattr(node, 'text') else ''
                        if text.strip():
                            full_content.append(text.strip())
                    
                    if full_content:
                        return '\n\n'.join(full_content)
        
        return None
        
    except Exception as e:
        print(f"检索完整文档时发生错误: {str(e)}")
        return None

@tool
def dual_stage_retrieve(query: str, workspace_id: str = None, summary_index_id: str = None, 
                       original_index_id: str = None, top_k: int = 3) -> str:
    """
    双阶段检索工具：先从摘要知识库检索，再从原文知识库获取完整案例。
    
    这个工具实现两阶段检索策略：
    1. 第一阶段：在摘要知识库中检索匹配的摘要段落
    2. 第二阶段：提取摘要文件名（即原文档ID），从原文知识库中检索完整案例内容
    
    适用于需要先通过摘要快速定位相关案例，再获取完整详细内容的场景。
    
    Args:
        query (str): 要检索的查询文本，例如 "生态农业技术应用"
        workspace_id (str, optional): 阿里云百炼业务空间ID，默认使用环境变量WORKSPACE_ID
        summary_index_id (str, optional): 摘要知识库ID，默认使用环境变量BAILIAN_SUMMARY_DATASET_ID
        original_index_id (str, optional): 原文知识库ID，默认使用环境变量BAILIAN_ORIGINAL_DATASET_ID
        top_k (int, optional): 返回的最大结果数量，默认为3
        
    Returns:
        str: 格式化的检索结果，包含摘要匹配信息和完整案例内容
        
    Example:
        >>> result = dual_stage_retrieve("可持续农业发展模式")
        >>> print(result)
        🔍 双阶段检索结果:
        - 查询: 可持续农业发展模式
        - 摘要知识库: xxx
        - 原文知识库: xxx
        
        📋 第一阶段 - 摘要检索结果:
        找到 2 个相关摘要
        
        📚 第二阶段 - 完整案例内容:
        [完整案例1]
        [完整案例2]
    """
    
    # 使用传入参数或环境变量
    ws_id = workspace_id or WORKSPACE_ID
    summary_idx_id = summary_index_id or SUMMARY_INDEX_ID
    original_idx_id = original_index_id or ORIGINAL_INDEX_ID
    
    if not ws_id or not summary_idx_id or not original_idx_id:
        return "❌ 错误：缺少必要的配置参数。请设置 WORKSPACE_ID、BAILIAN_SUMMARY_DATASET_ID 和 BAILIAN_ORIGINAL_DATASET_ID 环境变量，或在调用时传入参数。"
    
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
            metadata = getattr(node, 'metadata', {}) if hasattr(node, 'metadata') else {}
            
            result_lines.extend([
                f"\n{'-'*40}",
                f"摘要 {i} (相关度: {score:.3f}):",
                f"{'-'*40}",
                text.strip()[:200] + "..." if len(text.strip()) > 200 else text.strip()
            ])
            
            if metadata:
                result_lines.append(f"📋 元数据: {metadata}")
        
        # 第二阶段：从原文知识库检索完整内容
        result_lines.extend([
            "",
            f"📚 第二阶段 - 完整案例内容:"
        ])
        
        if not document_ids:
            # 如果无法提取文档ID，尝试使用摘要内容作为查询词在原文库中检索
            print(f"⚠️ 无法从摘要中提取文档ID，尝试使用摘要内容在原文库中检索...")
            original_result = retrieve_index(client, ws_id, original_idx_id, query)
            
            if original_result and hasattr(original_result, 'body'):
                original_nodes = original_result.body.data.nodes if hasattr(original_result.body.data, 'nodes') else []
                
                if original_nodes:
                    for i, node in enumerate(original_nodes[:top_k], 1):
                        text = getattr(node, 'text', '') if hasattr(node, 'text') else ''
                        score = getattr(node, 'score', 0) if hasattr(node, 'score') else 0
                        
                        result_lines.extend([
                            f"\n{'='*50}",
                            f"完整案例 {i} (相关度: {score:.3f}):",
                            f"{'='*50}",
                            text.strip()
                        ])
                else:
                    result_lines.append("❌ 未能在原文知识库中找到对应的完整案例")
            else:
                result_lines.append("❌ 原文知识库检索失败")
        else:
            # 使用提取的文档ID检索完整内容
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
    test_query = "生态农业可持续发展"
    print(f"测试查询: {test_query}")
    print(f"{'='*80}")
    result = dual_stage_retrieve.invoke({"query": test_query})
    print(result)