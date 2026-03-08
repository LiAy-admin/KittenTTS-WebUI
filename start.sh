#!/bin/bash

# KittenTTS 快速启动脚本

echo "🚀 启动 KittenTTS Web UI..."
echo ""

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: ./deploy.sh"
    exit 1
fi

# 检查模型
if [ ! -d "models/nano" ]; then
    echo "❌ 模型不存在，请先运行: ./deploy.sh"
    exit 1
fi

# 启动 Web UI
source .venv/bin/activate
python web_ui.py
