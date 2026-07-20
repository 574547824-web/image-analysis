@echo off
chcp 65001 >nul
echo ========================================
echo   图片解析助手 - 一键启动
echo ========================================
echo.

echo [1/3] 检查Python依赖...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo 依赖安装失败，请检查Python是否安装正确
    pause
    exit /b 1
)

echo [2/3] 启动后端服务...
echo.
echo 服务启动后，用浏览器打开 index.html 即可使用
echo 按 Ctrl+C 停止服务
echo.

echo [3/3] 打开网页...
start "" index.html

python server.py

pause
