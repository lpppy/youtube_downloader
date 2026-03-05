@echo off
REM YouTube 下载器启动脚本 (Windows)
REM 双击此文件即可启动应用

cd /d "%~dp0"

REM 检查虚拟环境是否存在
if not exist "venv\" (
    echo 首次运行，正在创建虚拟环境...
    python -m venv venv

    echo 正在安装依赖...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo 安装完成！
) else (
    call venv\Scripts\activate.bat
)

REM 启动应用
echo 正在启动 YouTube 下载器...
python main.py

REM 如果出错，保持窗口打开
if errorlevel 1 (
    echo.
    echo 应用启动失败，按任意键退出...
    pause >nul
)
