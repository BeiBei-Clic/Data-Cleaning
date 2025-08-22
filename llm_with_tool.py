import os
import asyncio
import json
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from filter import bailian_knowledge_retrieve


load_dotenv()

async def stream_with_token_output():
    llm = ChatOpenAI(
        model="google/gemini-2.5-flash",
        api_key=os.getenv('OPENROUTER_API_KEY'),
        base_url=os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1'),
        temperature=0.7,
        streaming=True
    )
    
    agent = create_react_agent(
        model=llm,
        tools=[bailian_knowledge_retrieve],
        prompt="""
        你是一个专业的乡村经营顾问AI助手，拥有访问乡村经营知识库的能力。
        
        ## 知识库工具使用指南：
        
        ### 核心原则：
        1. **提炼核心问题**：不要将用户的完整问题直接传入工具，而是提炼出核心关键词进行检索
        2. **多次检索**：可以多次调用工具获取更完整的信息，每次聚焦不同角度
        3. **利用元数据过滤**：充分利用五个元数据字段提高检索精准度
        
        ### 检索策略：
        - 将复杂问题拆解为多个核心概念分别检索
        - 先进行宽泛检索，再根据结果进行精准检索
        - 根据用户需求选择合适的元数据过滤条件
        
        ### 五个元数据过滤字段：
        1. **summary_keywords**: 摘要关键词过滤 - 用于筛选特定主题的案例
        2. **sustainable_operation**: 可持续运营关键词 - 筛选可持续发展相关内容
        3. **production_sales**: 产销关键词 - 筛选生产销售相关案例
        4. **industry_keywords**: 产业关键词 - 按产业类型筛选
        5. **resource_keywords**: 资源关键词 - 按资源类型筛选
        
        ### 使用示例：
        - 用户问"如何发展生态农业"，应该：
          1. 先检索"生态农业"获取基础信息
          2. 再检索"可持续发展"并使用sustainable_operation过滤
          3. 最后检索"农业产业化"并使用industry_keywords过滤
        
        记住：多角度检索比单次检索更能获得全面信息！
        """
    )
    
    test_query = "请帮我查询生态农业相关的信息"
    print(f"🤖 查询: {test_query}")
    print("=" * 60)
    
    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": test_query}]},
        version="v1"
    ):
        event_type = event.get("event")
        
        if event_type == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk", {})
            if hasattr(chunk, 'content') and chunk.content:
                print(chunk.content, end="", flush=True)
                
        elif event_type == "on_tool_start":
            tool_name = event.get("name", "")
            tool_input = event.get("data", {}).get("input", {})
            print(f"\n🔧 [{tool_name}] 执行中...")
            print(f"参数: {json.dumps(tool_input, ensure_ascii=False)}")
            
        elif event_type == "on_tool_end":
            tool_name = event.get("name", "")
            tool_output = event.get("data", {}).get("output", "")
            print(f"\n⚡ [{tool_name}] 完成")
            
            output_content = tool_output.content if hasattr(tool_output, 'content') else str(tool_output)
            print(f"结果: {output_content[:100]}..." if len(output_content) > 100 else f"结果: {output_content}")

if __name__ == "__main__":
    asyncio.run(stream_with_token_output())