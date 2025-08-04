import requests
from typing import Dict, Any
from config import Config

class LLMClient:
    """LLM客户端 - 调用API进行文本清洗"""
    
    def __init__(self, api_key: str = None, model: str = None):
        # 初始化API配置
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        self.model = model or Config.DEFAULT_MODEL
        
        if not self.api_key:
            raise ValueError("请设置OPENROUTER_API_KEY环境变量")
    
    def clean_text(self, text: str) -> str:
        """
        清洗文本并提取关键词
        
        Args:
            text: 原始文本
            
        Returns:
            格式化结果: "清洗后文本\n###关键词1 ###关键词2"
        """
        try:
            # 创建提示词并调用API
            prompt = self._create_prompt(text)
            response = self._call_api(prompt)
            
            # 解析响应
            cleaned_text, keywords = self._parse_response(response)
            
            # 格式化关键词
            if keywords:
                keyword_list = [kw.strip() for kw in keywords.replace('###', '').split(',') if kw.strip()]
                formatted_keywords = ' '.join([f"###{kw}" for kw in keyword_list])
                return f"{cleaned_text}\n{formatted_keywords}"
            else:
                return f"{cleaned_text}\n###处理失败"
                
        except Exception as e:
            # 失败时返回原文本
            return f"{text}\n###处理失败"
    
    def _create_prompt(self, text: str) -> str:
        """创建简化的提示词"""
        return f"""请对以下文本进行清洗和关键词提取：

清洗要求：
1. 保持原语言，删除页眉页脚、HTML标签、多余空白
2. 修正段落分割，清理乱码
3. 保留重要信息、数据、地名等

关键词提取要求：
- 提取8-12个相关关键词
- 重点关注：经营模式、产业类型、技术应用、政策措施
- 优先提取专业术语和地理标识

输出格式：
清洗后文本：
[清洗后的文本内容]
关键词：
[关键词1, 关键词2, 关键词3, ...]

原文本：
{text}
"""
    
    def _call_api(self, prompt: str) -> Dict[Any, Any]:
        """调用OpenRouter API"""
        # 设置请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建请求数据
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.3
        }
        
        # 发送请求
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API调用失败: {response.status_code}")
        
        return response.json()
    
    def _parse_response(self, response: Dict[Any, Any]) -> tuple[str, str]:
        """解析API响应，返回(清洗后文本, 关键词)"""
        try:
            content = response['choices'][0]['message']['content']
            
            # 解析清洗后的文本和关键词
            if "清洗后文本：" in content and "关键词：" in content:
                parts = content.split("关键词：")
                cleaned_text = parts[0].replace("清洗后文本：", "").strip()
                keywords = parts[1].strip()
                
                # 清理可能的"原文本："部分
                if "原文本：" in keywords:
                    keywords = keywords.split("原文本：")[0].strip()
            else:
                # 格式不符合预期时，使用原始内容
                cleaned_text = content
                keywords = ""
            
            return cleaned_text, keywords
            
        except (KeyError, IndexError) as e:
            raise Exception(f"解析API响应失败: {e}")