import os
import asyncio
import json
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from dual_stage_retrieval_tool import dual_stage_retrieve

load_dotenv()

async def stream_agent_response(agent, input_data):
    """统一的流式输出处理"""
    content=""
    structured_response=None
    async for event in agent.astream_events(input_data):
        if event.get("event") == "on_chain_end":
            event_data = event.get("data", {})
            if "output" in event_data and "structured_response" in event_data["output"]:
                structured_response = event_data["output"]["structured_response"]
        else:
            chunk = event.get("data", {}).get("chunk", {})
            if hasattr(chunk, 'content') and chunk.content:
                print(chunk.content, end="", flush=True)
                content+=chunk.content

    return structured_response,content

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
        tools=[dual_stage_retrieve],
        prompt="""
        你是一个专业的乡村振兴顾问AI助手，拥有访问振兴乡村案例知识库的能力。
        
        ## 知识库检索工具使用指南：
        
        ### 核心原则：
        1. **提炼关键词**：不要将用户的完整问题直接传入工具，而是提炼出核心关键词进行检索
        2. **多次检索**：可以多次调用工具获取更完整的信息，每次聚焦不同关键词
        3. **渐进式查询**：先用宽泛关键词，再根据结果进行精准查询
        
        ### 检索策略：
        - 将复杂问题拆解为多个核心概念分别检索
        - 使用简洁的关键词而非完整句子
        - 根据检索结果调整后续查询策略
        
        ### 使用示例：
        - 用户问"如何在山区发展生态农业产业化经营模式"，应该：
          1. 先检索"生态农业"获取基础信息
          2. 再检索"产业化经营"了解经营模式
          3. 最后检索"山区农业"获取地域特色案例
        
        ### 注意事项：
        - 每次检索只传入3-5个核心关键词
        - 避免传入完整的用户问题
        - 多角度检索比单次检索更能获得全面信息
        
        记住：用关键词检索，多次调用，综合分析！
        """
    )
    
    test_query = """"
    浙江湖州某乡村拥有一片闲置的山谷林地，周边有溪流、小型瀑布等自然景观，但长期因缺乏开发而处于
荒废状态，当地也希望通过发展文旅产业带动乡村振兴，却面临资金有限、业态规划不清晰、担心同质化竞争
等问题。若该村庄计划借鉴类似模式打造露营文旅项目，可从哪些方面入手破解发展难题？其思路与浙江安吉
半岛理想村（半岛露营村2号营地）的实践有哪些共通之处？
    """
    print(f"🤖 查询: {test_query}")
    print("=" * 60)
    print()
    structured_response,content=await stream_agent_response(agent, {"messages": [{"role": "user", "content": test_query}]})

    

if __name__ == "__main__":
    asyncio.run(stream_with_token_output())