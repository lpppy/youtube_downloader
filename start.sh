#!/bin/bash

# YouTube 下载器启动脚本
# 双击此文件即可启动应用

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "首次运行，正在创建虚拟环境..."
    python3 -m venv venv

    echo "正在安装依赖..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo "安装完成！"
else
    source venv/bin/activate
fi

# 启动应用
echo "正在启动 YouTube 下载器..."
python main.py

# 保持窗口打开（如果出错）
if [ $? -ne 0 ]; then
    echo ""
    echo "应用启动失败，按任意键退出..."
    read -n 1
fi
