import requests
import json
import os
from typing import Optional, Dict, Any, Union


class DifyFileUploader:
    """处理文件上传操作的类"""

    def __init__(self, file_dir: str = "load_file"):
        """
        初始化文件上传器

        :param file_dir: 存放上传文件的目录
        """
        self.file_dir = file_dir
        if not os.path.exists(self.file_dir):
            os.makedirs(self.file_dir)

    def get_file_path(self, filename: str) -> str:
        """
        获取文件的完整路径

        :param filename: 文件名
        :return: 完整文件路径
        """
        return os.path.join(self.file_dir, filename)

    def list_uploadable_files(self, extensions: list = ['.pdf', '.docx', '.txt', '.md']) -> list:
        """
        列出可上传的文件

        :param extensions: 允许的文件扩展名列表
        :return: 可上传的文件名列表
        """
        if not os.path.exists(self.file_dir):
            return []

        return [f for f in os.listdir(self.file_dir)
                if any(f.lower().endswith(ext) for ext in extensions)]


class DifyKnowledgeBaseOperator:
    """处理Dify知识库API操作的类"""

    def __init__(self, api_key: str, base_url: str = "http://localhost:8081/v1"):
        """
        初始化Dify知识库操作器

        :param api_key: Dify API密钥
        :param base_url: Dify API基础URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

    def create_document_by_file(
            self,
            dataset_id: str,
            file_path: str,
            process_rule: Optional[Dict[str, Any]] = None,
            original_document_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        通过文件在知识库中创建新文档

        :param dataset_id: 知识库ID
        :param file_path: 要上传的文件完整路径
        :param process_rule: 处理规则配置，包含段落分割设置
        :param original_document_id: 源文档ID(用于更新文档)
        :return: API响应结果
        """
        url = f"{self.base_url}/datasets/{dataset_id}/document/create-by-file"

        # 准备data参数
        data_payload = {}

        # 处理规则设置
        if process_rule:
            # 直接使用传入的process_rule，它应该已经是正确的格式
            data_payload = process_rule
        elif not original_document_id:
            # 默认处理规则 - 父子分段模式，按照你的要求配置
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

        if original_document_id:
            data_payload["original_document_id"] = original_document_id

        # 添加调试信息
        print("发送的参数:", json.dumps(data_payload, indent=2, ensure_ascii=False))

        # 准备multipart/form-data请求
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            data_str = json.dumps(data_payload, ensure_ascii=False)

            response = requests.post(
                url,
                headers=self.headers,
                files=files,
                data={'data': data_str}
            )

        if response.status_code != 200:
            print("错误响应:", response.text)
        response.raise_for_status()
        return response.json()


class DifyKnowledgeBaseManager:
    """管理Dify知识库操作的顶层类"""

    def __init__(self, api_key: str, base_url: str = "http://localhost:8081/v1", file_dir: str = "load_file"):
        """
        初始化知识库管理器

        :param api_key: Dify API密钥
        :param base_url: Dify API基础URL
        :param file_dir: 上传文件目录
        """
        self.file_uploader = DifyFileUploader(file_dir)
        self.kb_operator = DifyKnowledgeBaseOperator(api_key, base_url)

    def upload_file_to_knowledge_base(
            self,
            dataset_id: str,
            filename: str,
            process_rule: Optional[Dict[str, Any]] = None,
            original_document_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        上传文件到知识库

        :param dataset_id: 知识库ID
        :param filename: 文件名(在load_file目录下)
        :param process_rule: 处理规则配置,即分段设置
        :param original_document_id: 源文档ID(用于更新文档)
        :return: API响应结果
        """
        file_path = self.file_uploader.get_file_path(filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")

        return self.kb_operator.create_document_by_file(
            dataset_id=dataset_id,
            file_path=file_path,
            process_rule=process_rule,
            original_document_id=original_document_id
        )

    def batch_upload_files(
                self,
                dataset_id: str,
                extensions: list = ['.pdf', '.docx', '.txt', '.md'],
                process_rule: Optional[Dict[str, Any]] = None
        ) -> Dict[str, Dict[str, Any]]:
            """
            批量上传文件到知识库

            :param dataset_id: 知识库ID
            :param extensions: 允许的文件扩展名列表
            :param process_rule: 处理规则配置
            :return: 上传结果字典
            """
            # 初始化一个空字典，用于存储所有文件的上传结果
            results = {}
            
            # 遍历符合条件的可上传文件列表
            # self.file_uploader.list_uploadable_files(extensions)会返回指定目录下
            # 所有扩展名在extensions列表中的文件名称
            for filename in self.file_uploader.list_uploadable_files(extensions):
                # 调用上传单个文件的方法，将当前文件上传到指定知识库
                # 传入知识库ID、文件名和处理规则
                result = self.upload_file_to_knowledge_base(
                    dataset_id=dataset_id,
                    filename=filename,
                    process_rule=process_rule
                )
                
                # 将当前文件的上传结果存入结果字典
                # 键为文件名，值为包含状态和详细结果的字典
                results[filename] = {
                    "status": "success",  # 标记上传状态为成功
                    "result": result      # 存储API返回的详细结果
                }
            
            # 循环结束后，返回包含所有文件上传结果的字典
            return results


# 使用示例
if __name__ == "__main__":
    # 配置信息 - 使用你提供的具体值
    API_KEY = "dataset-nn9K2CMUXa9rSKLlNpMwmHU7"
    BASE_URL = "http://localhost/v1"
    DATASET_ID = "5a36aa21-0aa7-433e-bdab-72aa9931b543"
    FILE_DIR = "load_file"  # 存放上传文件的目录

    # 初始化管理器
    manager = DifyKnowledgeBaseManager(
        api_key=API_KEY,
        base_url=BASE_URL,
        file_dir=FILE_DIR
    )

    # 自定义处理规则示例
    custom_process_rule = {
        "indexing_technique": "high_quality",
        "doc_form": "hierarchical_model",
        "process_rule": {
            "mode": "hierarchical",
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails", "enabled": False}
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

    batch_results = manager.batch_upload_files(
        dataset_id=DATASET_ID,
        extensions=['.pdf', '.md'],
        process_rule=custom_process_rule
    )
    print("批量上传结果:", json.dumps(batch_results, indent=2, ensure_ascii=False))
