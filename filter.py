import os
from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from dotenv import load_dotenv
load_dotenv()


# 阿里云百炼配置常量
WORKSPACE_ID = os.environ.get('WORKSPACE_ID', '')
dataset1 = os.environ.get('BAILIAN_DATASET_ID_1', '')

def create_bailian_client() -> bailian20231229Client:
    """创建阿里云百炼客户端"""
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

def retrieve_from_bailian(client: bailian20231229Client, workspace_id: str, index_id: str, query: str, search_filters: Optional[List[Dict]] = None) -> Optional[Dict[str, Any]]:
    """从阿里云百炼知识库中检索信息"""
    headers = {}
    retrieve_request = bailian_20231229_models.RetrieveRequest(
        index_id=index_id,
        query=query
    )
    
    if search_filters:
        retrieve_request.search_filters = search_filters
    
    runtime = util_models.RuntimeOptions()
    
    response = client.retrieve_with_options(workspace_id, retrieve_request, headers, runtime)
    
    if response.status_code == 200:
        return {
            'status_code': response.status_code,
            'request_id': response.body.request_id,
            'data': response.body.data,
            'nodes': response.body.data.nodes if hasattr(response.body.data, 'nodes') else []
        }
    return None

@tool
def bailian_knowledge_retrieve(
    query: str,
    summary_keywords: str = None,
    sustainable_operation: str = None,
    production_sales: str = None,
    industry_keywords: str = None,
    resource_keywords: str = None,
    workspace_id: str = None,
    top_k: int = 5
) -> str:
    """
    从乡村经营知识库中检索相关案例和信息。
    
    ⚠️ 重要使用说明：
    1. query参数应传入提炼后的核心关键词，不要传入完整问题
    2. 建议多次调用本工具从不同角度检索，获取更全面的信息
    3. 充分利用元数据过滤参数提高检索精准度
    
    Args:
        query (str): 核心检索关键词（非完整问题句子）
        summary_keywords (str, optional): 摘要关键词过滤 - 筛选特定主题案例
        sustainable_operation (str, optional): 可持续运营关键词 - 筛选可持续发展内容
        production_sales (str, optional): 产销关键词 - 筛选生产销售案例
        industry_keywords (str, optional): 产业关键词 - 按产业类型筛选
        resource_keywords (str, optional): 资源关键词 - 按资源类型筛选
        workspace_id (str, optional): 业务空间ID
        top_k (int, optional): 返回结果数量，默认5
        
    使用示例：
    - 检索生态农业基础信息：query="生态农业"
    - 检索可持续运营案例：query="运营模式", sustainable_operation="循环经济"
    - 检索特定产业案例：query="种植业", industry_keywords="有机农业"
    - 检索销售模式：query="销售渠道", production_sales="直销"
    
    Returns:
        str: 格式化的检索结果，包含相关案例和元数据信息
    """
    """
    从阿里云百炼知识库中检索相关信息，支持五种关键词过滤。
    
    Args:
        query (str): 要检索的查询文本
        summary_keywords (str, optional): 摘要关键词过滤
        sustainable_operation (str, optional): 可持续运营关键词过滤
        production_sales (str, optional): 产销关键词过滤
        industry_keywords (str, optional): 产业关键词过滤
        resource_keywords (str, optional): 资源关键词过滤
        workspace_id (str, optional): 业务空间ID
        index_id (str, optional): 知识库ID
        top_k (int, optional): 返回结果数量，默认5
        
    Returns:
        str: 格式化的检索结果
    """
    
    ws_id = workspace_id or WORKSPACE_ID
    idx_id = dataset1
    
    if not ws_id or not idx_id:
        return "❌ 错误：缺少必要的配置参数。请设置 WORKSPACE_ID 和 INDEX_ID 环境变量。"
    
    client = create_bailian_client()
    
    # 构建搜索过滤器
    search_filters = []
    filter_group = {}
    
    if summary_keywords:
        filter_group["摘要"] = {"like": summary_keywords}
    if sustainable_operation:
        filter_group["可持续运营"] = {"like": sustainable_operation}
    if production_sales:
        filter_group["产销"] = {"like": production_sales}
    if industry_keywords:
        filter_group["产业"] = {"like": industry_keywords}
    if resource_keywords:
        filter_group["资源"] = {"like": resource_keywords}
    
    if filter_group:
        search_filters.append(filter_group)
    
    result = retrieve_from_bailian(client, ws_id, idx_id, query, search_filters if search_filters else None)
    
    if not result:
        return f"❌ 检索失败：无法从知识库中获取相关信息"
    
    nodes = result.get('nodes', [])
    
    if not nodes:
        return f"📊 百炼知识库检索结果:\n- 查询: {query}\n- 知识库ID: {idx_id}\n- 检索结果: 未找到相关内容"
    
    # 格式化输出结果
    result_lines = [
        f"📊 百炼知识库检索结果:",
        f"- 查询: {query}",
        f"- 检索到: {len(nodes)} 条相关内容",
        "",
        "📚 检索内容:"
    ]
    
    for i, node in enumerate(nodes[:top_k], 1):
        score = getattr(node, 'score', 0) if hasattr(node, 'score') else node.get('Score', 0)
        text = getattr(node, 'text', '') if hasattr(node, 'text') else node.get('Text', '')
        
        result_lines.extend([
            f"\n{'-'*40}",
            f"结果 {i} (相关度: {score:.3f}):",
            f"{'-'*40}",
            text.strip()
        ])
    
    return '\n'.join(result_lines)

if __name__ == "__main__":
    test_query = "生态农业案例"
    print(f"测试查询: {test_query}")
    print(f"{'='*80}")
    result = bailian_knowledge_retrieve.invoke({
        "query": test_query,
        "sustainable_operation": "滚动投入",
        "production_sales": "门票"
    })
    print(result)