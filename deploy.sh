#!/bin/bash

# KittenTTS 一键部署脚本
# 支持环境检查、依赖安装、模型下载、服务启动

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

# 检查命令是否存在
check_command() {
    if command -v $1 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# 检查 UV 是否安装
check_uv() {
    if check_command uv; then
        print_success "UV 已安装: $(uv --version)"
        return 0
    else
        print_warning "UV 未安装，正在安装..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.cargo/env
        if check_command uv; then
            print_success "UV 安装成功"
            return 0
        else
            print_error "UV 安装失败"
            return 1
        fi
    fi
}

# 检查 Python 版本
check_python() {
    print_info "检查 Python 版本..."
    if check_command python3.11.1; then
        print_success "Python 3.11.1 已安装"
        PYTHON_CMD="python3.11.1"
    elif check_command python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_info "找到 Python $PYTHON_VERSION"
        PYTHON_CMD="python3"
    else
        print_error "未找到 Python，请先安装 Python 3.11.1"
        exit 1
    fi
}

# 创建虚拟环境
create_venv() {
    print_header "创建虚拟环境"

    if [ -d ".venv" ]; then
        print_warning "虚拟环境已存在，跳过创建"
    else
        print_info "使用 UV 创建虚拟环境 (Python 3.11.1)..."
        if check_uv; then
            uv venv --python 3.11.1
            print_success "虚拟环境创建成功"
        else
            print_error "创建虚拟环境失败"
            exit 1
        fi
    fi
}

# 安装依赖
install_dependencies() {
    print_header "安装依赖"

    if [ -f "requirements.txt" ]; then
        print_info "安装项目依赖..."
        source .venv/bin/activate
        uv pip install -r requirements.txt
        print_success "依赖安装完成"
    else
        print_error "未找到 requirements.txt 文件"
        exit 1
    fi
}

# 下载模型
download_models() {
    print_header "下载模型"

    # 检查模型是否已存在
    if [ -d "models/nano" ] && [ -d "models/nano-int8" ] && [ -d "models/micro" ] && [ -d "models/mini" ]; then
        print_warning "模型已存在，跳过下载"
        return 0
    fi

    print_info "开始下载模型..."

    # 下载 ModelScope 模型
    print_info "从 ModelScope 下载 nano 和 nano-int8 模型..."
    source .venv/bin/activate
    python download_modelscope.py

    # 下载 Hugging Face 模型
    print_info "从 Hugging Face 下载 micro 和 mini 模型..."
    python download_missing_models.py

    print_success "模型下载完成"
}

# 验证模型
verify_models() {
    print_header "验证模型"

    source .venv/bin/activate
    if python verify_all_models.py; then
        print_success "所有模型验证通过"
    else
        print_error "模型验证失败"
        exit 1
    fi
}

# 启动 Web UI
start_webui() {
    print_header "启动 Web UI"

    if [ ! -f "web_ui.py" ]; then
        print_error "未找到 web_ui.py 文件"
        exit 1
    fi

    print_info "启动 KittenTTS Web UI..."
    print_info "访问地址: http://localhost:7860"
    print_info "按 Ctrl+C 停止服务"
    echo ""

    source .venv/bin/activate
    python web_ui.py
}

# 完整部署
full_deploy() {
    print_header "KittenTTS 一键部署"
    print_info "开始完整部署流程..."
    echo ""

    check_uv
    check_python
    create_venv
    install_dependencies
    download_models
    verify_models

    print_header "部署完成！"
    print_success "KittenTTS 已成功部署"
    print_info "现在可以启动 Web UI 或使用其他脚本"
    echo ""
    print_info "可用命令:"
    echo "  ./deploy.sh webui     # 启动 Web UI"
    echo "  ./deploy.sh test      # 运行测试"
    echo "  ./deploy.sh status    # 查看状态"
}

# 显示状态
show_status() {
    print_header "KittenTTS 状态检查"

    # 检查虚拟环境
    if [ -d ".venv" ]; then
        print_success "虚拟环境: 存在"
    else
        print_error "虚拟环境: 不存在"
    fi

    # 检查模型
    MODELS=("nano" "nano-int8" "micro" "mini")
    for model in "${MODELS[@]}"; do
        if [ -d "models/$model" ]; then
            print_success "模型 $model: 存在"
        else
            print_error "模型 $model: 不存在"
        fi
    done

    # 检查依赖
    source .venv/bin/activate 2>/dev/null
    if python -c "import gradio" 2>/dev/null; then
        print_success "依赖: 已安装"
    else
        print_error "依赖: 未安装"
    fi
}

# 运行测试
run_test() {
    print_header "运行测试"

    if [ -f "test_local_model.py" ]; then
        print_info "运行本地模型测试..."
        source .venv/bin/activate
        python test_local_model.py
    else
        print_error "未找到测试脚本"
        exit 1
    fi
}

# 显示帮助
show_help() {
    echo "KittenTTS 一键部署脚本"
    echo ""
    echo "用法: ./deploy.sh [命令]"
    echo ""
    echo "命令:"
    echo "  deploy    完整部署 (默认)"
    echo "  webui     仅启动 Web UI"
    echo "  test      运行测试"
    echo "  status    查看状态"
    echo "  models    下载模型"
    echo "  help      显示帮助"
    echo ""
    echo "示例:"
    echo "  ./deploy.sh         # 完整部署"
    echo "  ./deploy.sh webui   # 启动 Web UI"
}

# 主函数
main() {
    case "${1:-deploy}" in
        deploy)
            full_deploy
            ;;
        webui)
            start_webui
            ;;
        test)
            run_test
            ;;
        status)
            show_status
            ;;
        models)
            download_models
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
