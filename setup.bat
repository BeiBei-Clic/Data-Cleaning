@echo off
echo 安装项目依赖...
pip install -r requirements.txt
echo.
echo 创建输入目录...
mkdir input_files 2>nul
echo.
echo 设置完成！
echo.
echo 使用说明：
echo 1. 在 .env 文件中设置 OPENROUTER_API_KEY
echo 2. 将要处理的文件放入 input_files 目录
echo 3. 运行 python main.py
echo.
pause