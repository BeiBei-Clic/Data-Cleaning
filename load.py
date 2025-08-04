import requests
import json
import os

# 配置信息
API_KEY = "dataset-nn9K2CMUXa9rSKLlNpMwmHU7"
BASE_URL = "http://localhost/v1"
DATASET_ID = "5a36aa21-0aa7-433e-bdab-72aa9931b543"
FILE_DIR = "load_file"

def get_max_case_id():
    """获取知识库中当前最大的case_id"""
    url = f"{BASE_URL}/datasets/{DATASET_ID}/documents"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
    response = requests.get(url, headers=headers)
    documents = response.json().get('data', [])
    max_case_id = 0
    
    for doc in documents:
        doc_metadata = doc.get('doc_metadata', [])
        if doc_metadata:
            for meta in doc_metadata:
                if meta.get('name') == 'case_id':
                    case_id = meta.get('value')
                    if case_id and str(case_id).isdigit():
                        max_case_id = max(max_case_id, int(case_id))
    
    return max_case_id

def update_document_metadata(document_id, case_id):
    """更新文档的元数据"""
    # 获取case_id字段的ID
    metadata_url = f"{BASE_URL}/datasets/{DATASET_ID}/metadata"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    metadata_response = requests.get(metadata_url, headers=headers)
    
    metadata_fields = metadata_response.json().get('doc_metadata', [])
    case_id_field_id = None
    for field in metadata_fields:
        if field.get('name') == 'case_id':
            case_id_field_id = field['id']
            break
    
    if not case_id_field_id:
        print("未找到case_id元数据字段")
        return False
    
    # 更新文档元数据
    url = f"{BASE_URL}/datasets/{DATASET_ID}/documents/metadata"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "operation_data": [
            {
                "document_id": document_id,
                "metadata_list": [
                    {
                        "id": case_id_field_id,
                        "value": str(case_id),
                        "name": "case_id"
                    }
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200

def upload_file(filename, case_id):
    """上传单个文件到知识库，带case_id元数据"""
    file_path = os.path.join(FILE_DIR, filename)
    url = f"{BASE_URL}/datasets/{DATASET_ID}/document/create-by-file"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
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
        response = requests.post(url, headers=headers, files=files, data={'data': data_str})
    
    if response.status_code == 200:
        result = response.json()
        document_id = result['document']['id']
        
        # 上传成功后更新元数据
        if update_document_metadata(document_id, case_id):
            print(f"上传成功: {filename}, case_id: {case_id}")
        else:
            print(f"上传成功但元数据设置失败: {filename}")
        
        return result
    else:
        print(f"上传失败: {filename}")
        return None

def batch_upload():
    """批量上传文件"""
    max_case_id = get_max_case_id()
    print(f"当前最大case_id: {max_case_id}")
    
    files = [f for f in os.listdir(FILE_DIR) 
             if f.lower().endswith(('.pdf', '.docx', '.txt', '.md'))]
    
    current_case_id = max_case_id + 1
    
    for filename in files:
        upload_file(filename, current_case_id)
        current_case_id += 1

if __name__ == "__main__":
    batch_upload()
