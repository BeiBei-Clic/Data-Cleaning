import requests
import json
from typing import Dict, Any
from config import Config

class LLMClient:
    """大模型客户端，用于调用OpenRouter API进行文本清洗"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        self.model = model or Config.DEFAULT_MODEL
        
        if not self.api_key:
            raise ValueError("请设置OPENROUTER_API_KEY环境变量")
    
    def clean_text(self, text: str) -> str:
        """
        使用大模型清洗文本并提取关键字，返回格式化的结果
        
        Args:
            text: 需要清洗的文本
            
        Returns:
            格式化的文本：原文片段\n###关键词1 ###关键词2
        """
        prompt = self._create_cleaning_prompt(text)
        
        try:
            response = self._call_api(prompt)
            cleaned_text, keywords = self._parse_response(response)
            
            # 组合成最终格式：原文片段\n###关键词1 ###关键词2
            if keywords:
                # 处理关键词格式，确保每个关键词前都有###
                keyword_list = [kw.strip() for kw in keywords.replace('###', '').split(',') if kw.strip()]
                formatted_keywords = ' '.join([f"###{kw}" for kw in keyword_list])
                return f"{cleaned_text}\n{formatted_keywords}"
            else:
                return f"{cleaned_text}\n###处理失败"
                
        except Exception as e:
            print(f"调用大模型API失败: {e}")
            # 失败时返回原文本加默认关键词
            return f"{text}\n###处理失败"
    
    def _create_cleaning_prompt(self, text: str) -> str:
        """创建清洗文本的提示词"""
        return f"""请对以下文本进行清洗和关键词提取。

清洗要求：
1. 保持原语言，不要翻译
2. 删除页眉页脚、HTML标签、多余空白
3. 修正段落分割，清理乱码
4. 保留重要信息、数据、地名等

关键词提取要求：
- 提取8-12个相关关键词
- 重点关注：经营模式、产业类型、技术应用、政策措施等
- 优先提取专业术语和地理标识

🌟 成功案例维度：
- **经营模式**：党支部+合作社、公司+农户、家庭农场、农民专业合作社、股份合作制
- **产业类型**：特色种植、生态养殖、乡村旅游、农产品加工、电商直播、文创产业
- **技术应用**：智慧农业、物联网技术、无人机植保、冷链物流、数字化管理
- **主体协作**：农户参与、企业带动、政府引导、社会资本、科研院所合作
- **市场渠道**：订单农业、农超对接、直播带货、品牌建设、产销一体化
- **效益指标**：增收致富、就业创造、产值增长、品牌价值、生态效益

⚠️ 失败案例维度：
- **失败原因**：资金链断裂、技术不足、市场定位错误、管理不善、政策理解偏差
- **风险因素**：市场波动、自然灾害、疫情影响、竞争激烈、资源短缺
- **问题表现**：产品滞销、合作破裂、环境污染、农民利益受损、可持续性差
- **整改措施**：政策调整、模式优化、技术升级、管理改进、风险防控

📄 政府文件关键词分类：

🏛️ 政策要素：
- **政策名称**：乡村振兴促进法、农业农村现代化规划、产业扶持政策、土地制度改革
- **发文单位**：农业农村部、发改委、财政部、自然资源部、省市县政府
- **时间要素**：实施期限、阶段目标、时间节点、考核周期
- **适用范围**：全国性、区域性、试点地区、特定产业、特殊群体

🎯 政策措施：
- **资金支持**：专项补贴、低息贷款、财政奖励、税收优惠、保险补贴
- **土地政策**：用地保障、流转机制、确权登记、集体建设用地、宅基地改革
- **人才政策**：人才引进、培训计划、创业扶持、技术指导、职业教育
- **基础设施**：道路建设、水利设施、信息网络、公共服务、环境整治
- **保障机制**：考核评估、监督问责、绩效管理、信息公开、社会监督

🔍 关键词提取技巧：
1. **优先提取专业术语**：如"一村一品"、"三产融合"、"美丽乡村"
2. **关注数量词和时间词**：如"2023-2025年"、"增收30%"、"带动500户"
3. **提取地理标识**：具体的省市县村名称、地理特征
4. **捕获创新要素**：新模式、新技术、新机制的关键词
5. **识别问题导向**：痛点、难点、堵点等问题关键词

结合上面的指导和你自己的思考进行提取，包括但不限于上面的内容

请直接输出清洗后的文本和关键词，格式如下：
清洗后文本：
[清洗后的文本内容]
关键词：
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
                # 如果格式不符合预期，返回原始内容
                cleaned_text = content
                keywords = ""
            
            return cleaned_text, keywords
            
        except (KeyError, IndexError) as e:
            raise Exception(f"解析API响应失败: {e}")