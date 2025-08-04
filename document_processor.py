import docx
import PyPDF2
from pathlib import Path
import warnings

class DocumentProcessor:
    """文档处理器 - 将各种格式文档转换为文本"""
    
    def __init__(self):
        # 支持的文件格式
        self.supported_extensions = ['.docx', '.pdf', '.md', '.txt']
    
    def read_file(self, file_path: str) -> str:
        """读取文件并转换为文本"""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # 根据文件扩展名选择对应的读取方法
        readers = {
            '.docx': self._read_docx,
            '.pdf': self._read_pdf,
            '.md': self._read_text,
            '.txt': self._read_text
        }
        
        if extension not in readers:
            raise ValueError(f"不支持的文件格式: {extension}")
        
        return readers[extension](file_path)
    
    def _read_docx(self, file_path: Path) -> str:
        """读取Word文档"""
        doc = docx.Document(file_path)
        # 提取所有段落文本
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(paragraphs)
    
    def _read_pdf(self, file_path: Path) -> str:
        """读取PDF文档"""
        # 抑制PDF解析警告
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                # 提取所有页面文本
                pages = [page.extract_text() for page in pdf_reader.pages]
                return '\n'.join(pages)
    
    def _read_text(self, file_path: Path) -> str:
        """读取文本文件（包括txt和md）"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()