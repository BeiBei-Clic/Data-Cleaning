# 数据清洗工具

这是一个自动化的文档数据清洗工具，支持处理 Word、PDF、Markdown 等格式的文件。

## 功能特性

- 📄 支持多种文件格式：Word (.docx)、PDF (.pdf)、Markdown (.md)、文本 (.txt)
- ✂️ 智能文本分割：按长度3000分割，重复冗余长度500
- 🤖 AI驱动清洗：使用OpenRouter API调用大模型进行文本清洗
- 🏷️ 关键词提取：为每个文档自动提取关键词
- 📝 Markdown输出：清洗结果保存为格式化的Markdown文件

## 安装和设置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

或者运行批处理文件：
```bash
setup.bat
```

### 2. 配置API密钥
在 `.env` 文件中设置你的 OpenRouter API 密钥：

### 3. 准备文件
将需要清洗的文件放入 `input_files` 目录中。

## 使用方法

### 基本使用
```bash
python main.py
```

### 程序化使用
```python
from main import DataCleaningPipeline

# 创建处理流水线
pipeline = DataCleaningPipeline()

# 处理单个文件
result = pipeline.process_file("path/to/your/file.docx")

# 处理整个目录
results = pipeline.process_directory("input_files")
```

## 配置选项

在 `config.py` 中可以调整以下参数：

- `CHUNK_SIZE`: 文本片段大小（默认3000字符）
- `OVERLAP_SIZE`: 重复冗余长度（默认500字符）
- `DEFAULT_MODEL`: 使用的AI模型（默认claude-3.5-sonnet）
- `INPUT_DIR`: 输入文件目录
- `OUTPUT_DIR`: 输出文件目录

## 输出格式

清洗后的文件将保存为Markdown格式，包含：
- 文件信息和处理时间
- 提取的关键词
- 清洗后的内容

## 支持的文件格式

- `.docx` - Microsoft Word文档
- `.pdf` - PDF文档
- `.md` - Markdown文档
- `.txt` - 纯文本文档

## 注意事项

1. 确保有稳定的网络连接以访问OpenRouter API
2. 大文件处理可能需要较长时间
3. API调用有频率限制，程序会自动添加延迟
4. 建议先用小文件测试配置是否正确

## 错误处理

程序包含完善的错误处理机制：
- 文件读取失败时会跳过该文件
- API调用失败时会使用原始文本
- 处理完成后会显示详细的成功/失败统计

## 目录结构
数据清洗/
├── main.py              # 主程序
├── config.py            # 配置文件
├── document_processor.py # 文档处理模块
├── text_splitter.py     # 文本分割模块
├── llm_client.py        # 大模型客户端
├── requirements.txt     # 依赖列表
├── setup.bat           # 安装脚本
├── .env                # 环境变量
├── input_files/        # 输入文件目录
├── cleaned_results/    # 清洗结果目录
└── README.md           # 说明文档
## 许可证

MIT License