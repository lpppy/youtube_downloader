#!/bin/bash

# YouTube 下载器启动脚本
# 双击此文件即可启动应用

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "YouTube 批量下载器"
echo "=========================================="
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3"
    echo "请先安装 Python 3: https://www.python.org/downloads/"
    echo ""
    echo "按任意键退出..."
    read -n 1
    exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "首次运行，正在创建虚拟环境..."
    python3 -m venv venv

    if [ $? -ne 0 ]; then
        echo "❌ 创建虚拟环境失败"
        echo ""
        echo "按任意键退出..."
        read -n 1
        exit 1
    fi

    echo "正在安装依赖..."
    source venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt

    if [ $? -ne 0 ]; then
        echo "❌ 安装依赖失败"
        echo ""
        echo "按任意键退出..."
        read -n 1
        exit 1
    fi

    echo "✓ 安装完成！"
    echo ""
else
    source venv/bin/activate
fi

# 检查 Tkinter 是否可用
python -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Tkinter 未安装"
    echo ""
    echo "请运行以下命令安装 Tkinter:"
    echo "  brew install python-tk@3.13"
    echo ""
    echo "然后删除 venv 文件夹，重新运行此脚本"
    echo ""
    echo "按任意键退出..."
    read -n 1
    exit 1
fi

# 启动应用
echo "正在启动 YouTube 下载器..."
echo "GUI 窗口即将打开..."
echo ""
python main.py

# 保持窗口打开（如果出错）
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 应用启动失败"
    echo ""
    echo "按任意键退出..."
    read -n 1
fi
