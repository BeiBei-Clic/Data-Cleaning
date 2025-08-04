import requests
from config import Config

class LLMClient:
    """LLM客户端 - 调用API进行文本清洗"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        self.model = model or Config.DEFAULT_MODEL
    
    def clean_text(self, text: str) -> str:
        """清洗文本并提取关键词"""
        prompt = f"""请对以下文本进行清洗和关键词提取：

清洗要求：
1. 保持原语言，删除页眉页脚、HTML标签、多余空白
2. 修正段落分割，清理乱码
3. 保留重要信息、数据、地名等

关键词提取要求：
- 提取8-12个相关关键词
- 重点关注：经营模式、产业类型、技术应用、政策措施

输出格式：
清洗后文本：
[清洗后的文本内容]
关键词：
[关键词1, 关键词2, 关键词3, ...]

原文本：
{text}
"""
        
        # 调用API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.3
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        content = response.json()['choices'][0]['message']['content']
        
        # 解析响应
        if "清洗后文本：" in content and "关键词：" in content:
            parts = content.split("关键词：")
            cleaned_text = parts[0].replace("清洗后文本：", "").strip()
            keywords = parts[1].strip()
            
            if "原文本：" in keywords:
                keywords = keywords.split("原文本：")[0].strip()
            
            # 格式化关键词
            keyword_list = [kw.strip() for kw in keywords.replace('###', '').split(',') if kw.strip()]
            formatted_keywords = ' '.join([f"###{kw}" for kw in keyword_list])
            return f"{cleaned_text}\n{formatted_keywords}"
        
        return f"{content}\n###处理失败"