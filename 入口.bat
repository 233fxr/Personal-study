@echo off
chcp 65001 >nul
REM ─── 408 课程笔记本 Windows 启动脚本 ───
REM 自动定位到脚本所在目录
cd /d "%~dp0"

echo ========================================
echo   408 考研复习笔记本
echo ========================================
echo.
echo [1/2] 生成索引 & 清单...
python 生成索引.py
if %ERRORLEVEL% NEQ 0 (
    echo [警告] 索引生成出错，继续启动服务...
)

echo.
echo [2/2] 启动服务 & 打开浏览器...
start http://localhost:8765

echo.
echo 服务启动中... 按 Ctrl+C 停止。
echo.
python server.py
pause
