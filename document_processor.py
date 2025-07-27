import os
import docx
import PyPDF2
from pathlib import Path
import markdown
from typing import List, Tuple

class DocumentProcessor:
    """文档处理器，负责将各种格式的文档转换为文本"""
    
    def __init__(self):
        self.supported_extensions = ['.docx', '.pdf', '.md', '.txt']
    
    def read_file(self, file_path: str) -> str:
        """根据文件类型读取文件内容并转换为字符串"""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.docx':
            return self._read_docx(file_path)
        elif extension == '.pdf':
            return self._read_pdf(file_path)
        elif extension == '.md':
            return self._read_markdown(file_path)
        elif extension == '.txt':
            return self._read_txt(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {extension}")
    
    def _read_docx(self, file_path: Path) -> str:
        """读取Word文档"""
        try:
            doc = docx.Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            raise Exception(f"读取Word文档失败: {e}")
    
    def _read_pdf(self, file_path: Path) -> str:
        """读取PDF文档"""
        try:
            text = []
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        except Exception as e:
            raise Exception(f"读取PDF文档失败: {e}")
    
    def _read_markdown(self, file_path: Path) -> str:
        """读取Markdown文档"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"读取Markdown文档失败: {e}")
    
    def _read_txt(self, file_path: Path) -> str:
        """读取文本文档"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"读取文本文档失败: {e}")
    
    def get_files_in_directory(self, directory: str) -> List[str]:
        """获取目录中所有支持的文件"""
        files = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            return files
        
        for file_path in directory_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                files.append(str(file_path))
        
        return files