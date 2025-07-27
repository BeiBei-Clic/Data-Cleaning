import requests
import json
from typing import Dict, Any, Tuple
from config import Config

class LLMClient:
    """大模型客户端，用于调用OpenRouter API进行文本清洗"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        self.model = model or Config.DEFAULT_MODEL
        
        if not self.api_key:
            raise ValueError("请设置OPENROUTER_API_KEY环境变量")
    
    def clean_text(self, text: str) -> Tuple[str, str]:
        """
        使用大模型清洗文本并提取关键字
        
        Args:
            text: 需要清洗的文本
            
        Returns:
            (清洗后的文本, 关键字)
        """
        prompt = self._create_cleaning_prompt(text)
        
        try:
            response = self._call_api(prompt)
            return self._parse_response(response)
        except Exception as e:
            print(f"调用大模型API失败: {e}")
            return text, ""
    
    def _create_cleaning_prompt(self, text: str) -> str:
        """创建清洗文本的提示词"""
        return f"""请对以下文本进行数据清洗，要求：

1. 删除无用字符、格式错误
2. 优化排版
3. 除乱码字符和排版问题，原封不动保存原文
4. 提取3-5个关键词

请按以下格式返回结果：

**清洗后文本：**
[清洗后的文本内容]

**关键词：**
[关键词1, 关键词2, 关键词3, ...]

原文本：
{text}
"""
    
    def _call_api(self, prompt: str) -> Dict[Any, Any]:
        """调用OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",  # 可选
            "X-Title": "Data Cleaning Tool"  # 可选
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.3
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API调用失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    def _parse_response(self, response: Dict[Any, Any]) -> Tuple[str, str]:
        """解析API响应"""
        try:
            content = response['choices'][0]['message']['content']
            
            # 解析清洗后的文本和关键词
            if "**清洗后文本：**" in content and "**关键词：**" in content:
                parts = content.split("**关键词：**")
                cleaned_text = parts[0].replace("**清洗后文本：**", "").strip()
                keywords = parts[1].strip()
            else:
                # 如果格式不符合预期，返回原始内容
                cleaned_text = content
                keywords = ""
            
            return cleaned_text, keywords
            
        except (KeyError, IndexError) as e:
            raise Exception(f"解析API响应失败: {e}")