import os
import PyPDF2
import dashscope

# 配置
API_KEY = "sk-579299350a8048ea9bf905b55fad4b23"
MODEL_NAME = "qwen-max-2025-01-25"
INPUT_DIR = "case21-30"
OUTPUT_DIR = "summary21-30"

def load_pdf(file_path):
    """读取PDF文件内容"""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = '\n'.join([page.extract_text() for page in reader.pages])
        return text.strip()

def call_model(text, filename):
    """调用阿里云模型分析案例"""
    dashscope.api_key = API_KEY
    
    prompt = f"""请从以下案例中提取关键信息，按以下结构总结：

【标题】<保持原文标题不变>

- 项目背景
- 主要措施（3-5点）
- 取得成效（2-3项具体成果）
- 经验教训（3-5点）

要求：字数不超过600字

案例[{filename}]：
{text[:8000]}"""

    response = dashscope.Generation.call(
        model=MODEL_NAME,
        prompt=prompt,
        temperature=0.3,
        top_p=0.8
    )
    return response.output.text

def save_result(content, filename):
    """保存结果到文件"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_filename = f"{os.path.splitext(filename)[0]}_summary.md"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"#{os.path.splitext(filename)[0]}案例摘要\n\n")
        f.write(content)
    
    print(f"✅ 生成: {output_filename}")

def batch_process():
    """批量处理PDF文件"""
    os.makedirs(INPUT_DIR, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    
    print(f"发现 {len(pdf_files)} 个PDF文件")
    
    for filename in pdf_files:
        print(f"处理: {filename}")
        
        file_path = os.path.join(INPUT_DIR, filename)
        text = load_pdf(file_path)
        result = call_model(text, filename)
        save_result(result, filename)
    
    print(f"完成！输出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    batch_process()