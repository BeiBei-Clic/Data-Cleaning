from typing import List, Tuple

class TextSplitter:
    """文本分割器，按指定长度分割文本并保持重复冗余"""
    
    def __init__(self, chunk_size: int = 3000, overlap_size: int = 500):
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
    
    def split_text(self, text: str) -> List[str]:
        """
        将文本按指定长度分割，保持重复冗余
        
        Args:
            text: 要分割的文本
            
        Returns:
            分割后的文本片段列表
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # 计算当前片段的结束位置
            end = start + self.chunk_size
            
            # 如果不是最后一个片段，尝试在合适的位置断开
            if end < len(text):
                # 寻找最近的句号、换行符或空格来断开
                break_chars = ['\n\n', '。', '\n', ' ']
                best_break = end
                
                for char in break_chars:
                    # 在overlap范围内寻找断开点
                    search_start = max(start + self.chunk_size - self.overlap_size, start)
                    char_pos = text.rfind(char, search_start, end)
                    if char_pos != -1:
                        best_break = char_pos + len(char)
                        break
                
                end = best_break
            
            # 提取当前片段
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # 如果已经到达文本末尾，退出循环
            if end >= len(text):
                break
            
            # 计算下一个片段的开始位置（保持重复冗余）
            start = max(end - self.overlap_size, start + 1)
        
        return chunks
    
    def get_chunk_info(self, chunks: List[str]) -> List[dict]:
        """获取每个片段的信息"""
        info = []
        for i, chunk in enumerate(chunks):
            info.append({
                'index': i + 1,
                'length': len(chunk),
                'preview': chunk[:100] + '...' if len(chunk) > 100 else chunk
            })
        return info