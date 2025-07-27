import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # OpenRouter API配置
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    # 默认使用的模型
    DEFAULT_MODEL = "google/gemini-2.5-flash"
    
    # 文本分割配置
    CHUNK_SIZE = 3000  # 每个片段的长度
    OVERLAP_SIZE = 500  # 重复冗余长度
    
    # 支持的文件类型
    SUPPORTED_EXTENSIONS = ['.docx', '.pdf', '.md', '.txt']
    
    # 输入和输出目录
    INPUT_DIR = "input_files"
    OUTPUT_DIR = "cleaned_results"
    
    # 确保目录存在
    @staticmethod
    def ensure_directories():
        os.makedirs(Config.INPUT_DIR, exist_ok=True)
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)