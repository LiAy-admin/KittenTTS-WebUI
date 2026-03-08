#!/bin/bash

# KittenTTS-WebUI 启动脚本

set -e

echo "=================================================="
echo "  KittenTTS-WebUI 启动中..."
echo "=================================================="

# 激活虚拟环境
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "错误: 虚拟环境不存在，请先运行 ./install.sh"
    exit 1
fi

# 启动 Web UI
echo ""
echo "访问地址: http://localhost:7860"
echo "按 Ctrl+C 停止服务"
echo ""

python web_ui.py
