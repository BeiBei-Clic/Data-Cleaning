import os
import time
import requests
import zipfile
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class MinerUParser:
    def __init__(self):
        self.token = os.getenv('MINERU_API_TOKEN', '官网申请的api token')
        self.base_url = "https://mineru.net/api/v4"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
    
    def parse_file_to_md(self, file_path: str, output_dir: str = "./output") -> str:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"文件不存在: {file_path}")
            return ""
        
        print(f"开始处理文件: {file_path.name}")
        
        # 申请上传URL
        upload_data = {
            "enable_formula": True,
            "language": "ch",
            "enable_table": True,
            "files": [{"name": file_path.name, "is_ocr": True, "data_id": file_path.name}]
        }
        
        response = requests.post(f"{self.base_url}/file-urls/batch", headers=self.headers, json=upload_data)
        if response.status_code != 200:
            print(f"申请上传URL失败: {response.status_code}")
            return ""
        
        result = response.json()
        if result["code"] != 0:
            print(f"申请上传URL失败: {result.get('msg', '未知错误')}")
            return ""
        
        batch_id = result["data"]["batch_id"]
        upload_url = result["data"]["file_urls"][0]
        print(f"获取上传URL成功，batch_id: {batch_id}")
        
        # 上传文件
        with open(file_path, 'rb') as f:
            upload_response = requests.put(upload_url, data=f)
            if upload_response.status_code != 200:
                print(f"文件上传失败: {upload_response.status_code}")
                return ""
        
        print("文件上传成功")
        
        # 等待解析完成
        for _ in range(30):  # 最多等待5分钟
            time.sleep(10)
            
            result_response = requests.get(f"{self.base_url}/extract-results/batch/{batch_id}", headers=self.headers)
            if result_response.status_code != 200:
                continue
                
            result_data = result_response.json()
            if result_data["code"] != 0:
                continue
                
            extract_results = result_data["data"]["extract_result"]
            if not extract_results:
                continue
                
            file_result = extract_results[0]
            if file_result["state"] == "done" and "full_zip_url" in file_result:
                zip_url = file_result["full_zip_url"]
                print(f"解析完成，下载结果: {zip_url}")
                return self._download_and_extract_zip(zip_url, file_path.stem, output_dir)
            else:
                print(f"解析中，状态: {file_result.get('state', 'unknown')}")
        
        print("解析超时")
        return ""
    
    def _download_and_extract_zip(self, zip_url: str, file_stem: str, output_dir: str) -> str:
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 下载zip文件时不使用代理
        proxies = {'http': None, 'https': None}
        zip_response = requests.get(zip_url, proxies=proxies, timeout=30)
        if zip_response.status_code != 200:
            print(f"下载zip文件失败: {zip_response.status_code}")
            return ""
        
        temp_zip_path = output_path / f"{file_stem}_temp.zip"
        with open(temp_zip_path, 'wb') as f:
            f.write(zip_response.content)
        
        # 解压并查找markdown文件
        extract_dir = output_path / f"{file_stem}_extracted"
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        md_files = list(extract_dir.rglob("*.md"))
        if md_files:
            target_md = output_path / f"{file_stem}.md"
            with open(md_files[0], 'r', encoding='utf-8') as src, open(target_md, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            
            print(f"Markdown文件已保存到: {target_md}")
            
            # 清理临时文件
            temp_zip_path.unlink()
            shutil.rmtree(extract_dir)
            
            return str(target_md)
        else:
            print("在解压文件中未找到markdown文件")
            return ""
    
    def batch_parse_files(self, input_dir: str, output_dir: str = "./output"):
        input_path = Path(input_dir)
        if not input_path.exists():
            print(f"输入目录不存在: {input_dir}")
            return
        
        supported_extensions = {'.pdf', '.docx', '.doc', '.ppt', '.pptx'}
        files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in supported_extensions]
        
        if not files:
            print("未找到支持的文件")
            return
        
        print(f"找到 {len(files)} 个文件待处理")
        
        success_count = 0
        for file_path in files:
            result = self.parse_file_to_md(str(file_path), output_dir)
            if result:
                success_count += 1
            print("-" * 50)
        
        print(f"批量处理完成，成功: {success_count}/{len(files)}")

def main():
    parser = MinerUParser()
    parser.batch_parse_files("./input_files", "./output")

if __name__ == "__main__":
    main()