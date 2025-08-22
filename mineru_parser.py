import os
import time
import requests
import zipfile
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
        """解析文件并保存为markdown格式"""
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"文件不存在: {file_path}")
            return ""
        
        file_name = file_path.name
        print(f"开始处理文件: {file_name}")
        
        # 步骤1：申请上传URL
        upload_data = {
            "enable_formula": True,
            "language": "ch",
            "enable_table": True,
            "files": [
                {"name": file_name, "is_ocr": True, "data_id": file_name}
            ]
        }
        
        response = requests.post(
            f"{self.base_url}/file-urls/batch",
            headers=self.headers,
            json=upload_data
        )
        
        if response.status_code != 200:
            print(f"申请上传URL失败: {response.status_code}")
            return ""
        
        result = response.json()
        if result["code"] != 0:
            print(f"申请上传URL失败: {result.get('msg', '未知错误')}")
            return ""
        
        batch_id = result["data"]["batch_id"]
        upload_urls = result["data"]["file_urls"]
        print(f"获取上传URL成功，batch_id: {batch_id}")
        
        # 步骤2：上传文件
        upload_url = upload_urls[0]
        with open(file_path, 'rb') as f:
            upload_response = requests.put(upload_url, data=f)
            if upload_response.status_code != 200:
                print(f"文件上传失败: {upload_response.status_code}")
                return ""
        
        print("文件上传成功")
        
        # 步骤3：等待解析完成并获取结果
        max_wait_time = 300
        wait_time = 0
        
        while wait_time < max_wait_time:
            time.sleep(10)
            wait_time += 10
            
            result_response = requests.get(
                f"{self.base_url}/extract-results/batch/{batch_id}",
                headers=self.headers
            )
            
            if result_response.status_code == 200:
                result_data = result_response.json()
                
                if result_data["code"] == 0:
                    data = result_data["data"]
                    extract_results = data["extract_result"]
                    
                    if extract_results and len(extract_results) > 0:
                        file_result = extract_results[0]
                        
                        if file_result["state"] == "done" and "full_zip_url" in file_result:
                            zip_url = file_result["full_zip_url"]
                            print(f"解析完成，下载结果: {zip_url}")
                            
                            # 下载并解压zip文件
                            return self._download_and_extract_zip(zip_url, file_path.stem, output_dir)
                        else:
                            print(f"解析中，状态: {file_result.get('state', 'unknown')}")
            else:
                print(f"查询结果失败: {result_response.status_code}")
        
        print("解析超时")
        return ""
    
    def _download_and_extract_zip(self, zip_url: str, file_stem: str, output_dir: str) -> str:
        """下载并解压zip文件，提取markdown内容"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 下载zip文件
        zip_response = requests.get(zip_url)
        if zip_response.status_code != 200:
            print(f"下载zip文件失败: {zip_response.status_code}")
            return ""
        
        # 保存临时zip文件
        temp_zip_path = output_path / f"{file_stem}_temp.zip"
        with open(temp_zip_path, 'wb') as f:
            f.write(zip_response.content)
        
        # 解压zip文件
        extract_dir = output_path / f"{file_stem}_extracted"
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # 查找markdown文件
        md_files = list(extract_dir.rglob("*.md"))
        if md_files:
            # 复制第一个找到的markdown文件到输出目录
            source_md = md_files[0]
            target_md = output_path / f"{file_stem}.md"
            
            with open(source_md, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(target_md, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            print(f"Markdown文件已保存到: {target_md}")
            
            # 清理临时文件
            temp_zip_path.unlink()
            import shutil
            shutil.rmtree(extract_dir)
            
            return str(target_md)
        else:
            print("在解压文件中未找到markdown文件")
            return ""
    
    def batch_parse_files(self, input_dir: str, output_dir: str = "./output"):
        """批量解析目录下的文件"""
        input_path = Path(input_dir)
        if not input_path.exists():
            print(f"输入目录不存在: {input_dir}")
            return
        
        # 支持的文件类型
        supported_extensions = {'.pdf', '.docx', '.doc', '.ppt', '.pptx'}
        
        files = [f for f in input_path.iterdir() 
                if f.is_file() and f.suffix.lower() in supported_extensions]
        
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
    
    # 批量处理input_files目录下的文件
    parser.batch_parse_files("./input_files", "./output")

if __name__ == "__main__":
    main()