import os
from typing import Dict, Any, Optional
from langchain_core.tools import tool
from alibabacloud_bailian20231229 import models as bailian_20231229_models
from alibabacloud_bailian20231229.client import Client as bailian20231229Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from dotenv import load_dotenv
load_dotenv()


# 阿里云百炼配置常量
WORKSPACE_ID = os.environ.get('WORKSPACE_ID', '')
dataset1 = os.environ.get('BAILIAN_DATASET_ID_2', '')

def create_bailian_client() -> bailian20231229Client:
    """创建阿里云百炼客户端"""
    config = open_api_models.Config(
        access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
        access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    )
    config.endpoint = 'bailian.cn-beijing.aliyuncs.com'
    return bailian20231229Client(config)

def retrieve_from_bailian(client: bailian20231229Client, workspace_id: str, index_id: str, query: str) -> Optional[Dict[str, Any]]:
    """从阿里云百炼知识库中检索信息"""
    headers = {}
    retrieve_request = bailian_20231229_models.RetrieveRequest(
        index_id=index_id,
        query=query
    )
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
def bailian_knowledge_retrieve(query: str, workspace_id: str = None, index_id: str = None, top_k: int = 5) -> str:
    """
    从阿里云百炼知识库中检索相关信息。
    
    这个工具连接阿里云百炼服务，在指定的知识库中搜索与查询相关的内容。
    适用于需要从企业知识库、文档库或专业资料中获取准确信息的场景。
    
    Args:
        query (str): 要检索的查询文本，例如 "生态农业发展现状"
        workspace_id (str, optional): 阿里云百炼业务空间ID，默认使用环境变量WORKSPACE_ID
        index_id (str, optional): 知识库ID，默认使用环境变量INDEX_ID  
        top_k (int, optional): 返回的最大结果数量，默认为5
        
    Returns:
        str: 格式化的检索结果
        
    Example:
        >>> result = bailian_knowledge_retrieve("可持续农业技术")
        >>> print(result)
        📊 百炼知识库检索结果:
        - 查询: 可持续农业技术
        - 知识库ID: xxx
        - 检索到: 3 条相关内容
        
        📚 检索内容:
        1. [相关内容1]
        2. [相关内容2]
        3. [相关内容3]
    """
    
    # 使用传入参数或环境变量
    ws_id = workspace_id or WORKSPACE_ID
    idx_id = dataset1
    
    if not ws_id or not idx_id:
        return "❌ 错误：缺少必要的配置参数。请设置 WORKSPACE_ID 和 INDEX_ID 环境变量，或在调用时传入参数。"
    
    # 创建客户端并检索
    client = create_bailian_client()
    result = retrieve_from_bailian(client, ws_id, idx_id, query)
    
    if not result:
        return f"❌ 检索失败：无法从知识库中获取相关信息"
    
    # 解析检索结果 - 直接从result中获取nodes
    nodes = result.get('nodes', [])
    
    if not nodes:
        return f"📊 百炼知识库检索结果:\n- 查询: {query}\n- 知识库ID: {idx_id}\n- 检索结果: 未找到相关内容"
    
    # 格式化输出结果
    result_lines = [
        f"📊 百炼知识库检索结果:",
        f"- 查询: {query}",
        f"- 知识库ID: {idx_id}",
        f"- 检索到: {len(nodes)} 条相关内容",
        "",
        "📚 检索内容:"
    ]
    
    for i, node in enumerate(nodes[:top_k], 1):
        # 根据API文档，节点对象的属性可能是直接属性而不是字典
        score = getattr(node, 'score', 0) if hasattr(node, 'score') else node.get('Score', 0)
        text = getattr(node, 'text', '') if hasattr(node, 'text') else node.get('Text', '')
        metadata = getattr(node, 'metadata', {}) if hasattr(node, 'metadata') else node.get('Metadata', {})
        
        result_lines.extend([
            f"\n{'-'*40}",
            f"结果 {i} (相关度: {score:.3f}):",
            f"{'-'*40}",
            text.strip()
        ])
        
        # 如果有元数据，也显示出来
        if metadata:
            result_lines.append(f"\n📋 元数据: {metadata}")
    
    return '\n'.join(result_lines)

if __name__ == "__main__":
    # 测试百炼知识库检索功能
    test_query = "生态农业案例"
    print(f"测试查询: {test_query}")
    print(f"{'='*80}")
    result = bailian_knowledge_retrieve.invoke({"query": test_query})
    print(result)