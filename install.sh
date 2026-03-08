#!/bin/bash

# KittenTTS-WebUI 一键安装脚本
# 使用方法: curl -fsSL https://raw.githubusercontent.com/LiAy-admin/KittenTTS-WebUI/main/install.sh | bash

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 打印函数
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# 检测命令是否存在
command_exists() { command -v "$1" &> /dev/null; }

echo "=================================================="
echo "  KittenTTS-WebUI 一键安装脚本"
echo "=================================================="
echo ""

# 1. 检查 Python
info "检查 Python 环境..."
if ! command_exists python3; then
    error "未找到 Python3，请先安装 Python 3.11+"
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
success "Python 版本: $PYTHON_VERSION"

# 2. 检查/安装 UV
info "检查 UV 包管理器..."
if ! command_exists uv; then
    info "正在安装 UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    success "UV 安装完成"
else
    success "UV 已安装"
fi

# 3. 创建虚拟环境
info "创建虚拟环境..."
if [ ! -d ".venv" ]; then
    uv venv --python 3.11.1
    success "虚拟环境创建完成"
else
    success "虚拟环境已存在"
fi

# 4. 安装依赖
info "安装项目依赖..."
source .venv/bin/activate
uv pip install -r requirements.txt
success "依赖安装完成"

# 5. 检查/下载模型
info "检查模型文件..."
MODELS_COUNT=$(find models -name "*.onnx" 2>/dev/null | wc -l)
if [ "$MODELS_COUNT" -lt 4 ]; then
    info "下载模型文件..."
    python download_modelscope.py
    python download_missing_models.py
    success "模型下载完成"
else
    success "模型文件已存在 ($MODELS_COUNT 个)"
fi

# 6. 验证安装
info "验证安装..."
python verify_all_models.py
success "安装验证通过"

echo ""
echo "=================================================="
echo "  ${GREEN}安装完成！${NC}"
echo "=================================================="
echo ""
echo "启动方式:"
echo "  ./start.sh          # 启动 Web UI"
echo "  python web_ui.py    # 或直接运行 Python"
echo ""
echo "访问地址: http://localhost:7860"
echo ""
