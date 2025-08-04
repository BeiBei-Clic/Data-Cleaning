import requests
import json
import os

# 配置信息
API_KEY = "dataset-nn9K2CMUXa9rSKLlNpMwmHU7"
BASE_URL = "http://localhost/v1"
DATASET_ID = "5a36aa21-0aa7-433e-bdab-72aa9931b543"
FILE_DIR = "load_file"

def upload_file(filename):
    """上传单个文件到知识库"""
    file_path = os.path.join(FILE_DIR, filename)
    
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return None
    
    url = f"{BASE_URL}/datasets/{DATASET_ID}/document/create-by-file"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
    # 默认处理规则
    data_payload = {
        "indexing_technique": "high_quality",
        "doc_form": "hierarchical_model",
        "process_rule": {
            "mode": "hierarchical",
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails", "enabled": True}
                ],
                "parent_mode": "paragraph",
                "segmentation": {
                    "separator": "&&&&",
                    "max_tokens": 4000
                },
                "subchunk_segmentation": {
                    "separator": "###",
                    "max_tokens": 96
                }
            }
        }
    }
    
    with open(file_path, 'rb') as f:
        files = {'file': (filename, f)}
        data_str = json.dumps(data_payload, ensure_ascii=False)
        
        response = requests.post(
            url,
            headers=headers,
            files=files,
            data={'data': data_str}
        )
    
    if response.status_code == 200:
        print(f"上传成功: {filename}")
        return response.json()
    else:
        print(f"上传失败: {filename}, 错误: {response.text}")
        return None

def batch_upload():
    """批量上传文件"""
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
    
    # 获取所有支持的文件
    files = [f for f in os.listdir(FILE_DIR) 
             if f.lower().endswith(('.pdf', '.docx', '.txt', '.md'))]
    
    results = {}
    for filename in files:
        result = upload_file(filename)
        results[filename] = result
    
    return results

if __name__ == "__main__":
    results = batch_upload()
    print("上传结果:", json.dumps(results, indent=2, ensure_ascii=False))
