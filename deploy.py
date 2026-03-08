#!/usr/bin/env python3
"""
KittenTTS 一键部署脚本 (Python 版本)
支持环境检查、依赖安装、模型下载、服务启动
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# 颜色输出
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

def print_info(msg):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def print_success(msg):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")

def print_error(msg):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def print_header(title):
    print()
    print(f"{Colors.BLUE}========================================{Colors.NC}")
    print(f"{Colors.BLUE}{title}{Colors.NC}")
    print(f"{Colors.BLUE}========================================{Colors.NC}")
    print()

def run_command(cmd, check=True):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_uv():
    """检查 UV 是否安装"""
    print_info("检查 UV...")
    success, _, _ = run_command("which uv", check=False)
    if success:
        stdout, _, _ = run_command("uv --version")
        print_success(f"UV 已安装: {stdout.strip()}")
        return True
    else:
        print_warning("UV 未安装，正在安装...")
        success, stdout, stderr = run_command("curl -LsSf https://astral.sh/uv/install.sh | sh")
        if success:
            # 添加到 PATH
            os.environ['PATH'] += ":$HOME/.cargo/bin"
            print_success("UV 安装成功")
            return True
        else:
            print_error("UV 安装失败")
            return False

def check_python():
    """检查 Python 版本"""
    print_info("检查 Python 版本...")
    success, stdout, _ = run_command("python3.11.1 --version", check=False)
    if success:
        print_success(f"Python 3.11.1 已安装")
        return True
    else:
        success, stdout, _ = run_command("python3 --version", check=False)
        if success:
            print_info(f"找到 Python: {stdout.strip()}")
            return True
        else:
            print_error("未找到 Python，请先安装 Python 3.11.1")
            return False

def create_venv():
    """创建虚拟环境"""
    print_header("创建虚拟环境")

    if Path(".venv").exists():
        print_warning("虚拟环境已存在，跳过创建")
        return True

    print_info("使用 UV 创建虚拟环境 (Python 3.11.1)...")
    if check_uv():
        success, stdout, stderr = run_command("uv venv --python 3.11.1")
        if success:
            print_success("虚拟环境创建成功")
            return True
        else:
            print_error("虚拟环境创建失败")
            print_error(stderr)
            return False
    return False

def install_dependencies():
    """安装依赖"""
    print_header("安装依赖")

    if not Path("requirements.txt").exists():
        print_error("未找到 requirements.txt 文件")
        return False

    print_info("安装项目依赖...")
    success, stdout, stderr = run_command(
        "source .venv/bin/activate && uv pip install -r requirements.txt"
    )
    if success:
        print_success("依赖安装完成")
        return True
    else:
        print_error("依赖安装失败")
        print_error(stderr)
        return False

def download_models():
    """下载模型"""
    print_header("下载模型")

    # 检查模型是否已存在
    models_exist = all([
        Path("models/nano").exists(),
        Path("models/nano-int8").exists(),
        Path("models/micro").exists(),
        Path("models/mini").exists()
    ])

    if models_exist:
        print_warning("模型已存在，跳过下载")
        return True

    print_info("开始下载模型...")

    # 下载 ModelScope 模型
    print_info("从 ModelScope 下载 nano 和 nano-int8 模型...")
    success, stdout, stderr = run_command(
        "source .venv/bin/activate && python download_modelscope.py"
    )
    if not success:
        print_warning("ModelScope 模型下载失败，尝试使用现有模型")

    # 下载 Hugging Face 模型
    print_info("从 Hugging Face 下载 micro 和 mini 模型...")
    success, stdout, stderr = run_command(
        "source .venv/bin/activate && python download_missing_models.py"
    )
    if not success:
        print_warning("Hugging Face 模型下载失败")

    print_success("模型下载完成")
    return True

def verify_models():
    """验证模型"""
    print_header("验证模型")

    success, stdout, stderr = run_command(
        "source .venv/bin/activate && python verify_all_models.py"
    )
    if success:
        print_success("所有模型验证通过")
        return True
    else:
        print_warning("模型验证失败，但可能仍可使用")
        return True

def start_webui():
    """启动 Web UI"""
    print_header("启动 Web UI")

    if not Path("web_ui.py").exists():
        print_error("未找到 web_ui.py 文件")
        return False

    print_info("启动 KittenTTS Web UI...")
    print_info("访问地址: http://localhost:7860")
    print_info("按 Ctrl+C 停止服务")
    print()

    os.system("source .venv/bin/activate && python web_ui.py")
    return True

def show_status():
    """显示状态"""
    print_header("KittenTTS 状态检查")

    # 检查虚拟环境
    if Path(".venv").exists():
        print_success("虚拟环境: 存在")
    else:
        print_error("虚拟环境: 不存在")

    # 检查模型
    models = ["nano", "nano-int8", "micro", "mini"]
    for model in models:
        if Path(f"models/{model}").exists():
            print_success(f"模型 {model}: 存在")
        else:
            print_error(f"模型 {model}: 不存在")

    # 检查依赖
    try:
        import importlib.util
        spec = importlib.util.find_spec("gradio")
        if spec:
            print_success("依赖: 已安装")
        else:
            print_error("依赖: 未安装")
    except:
        print_error("依赖: 未安装")

def full_deploy():
    """完整部署"""
    print_header("KittenTTS 一键部署")
    print_info("开始完整部署流程...")
    print()

    steps = [
        ("检查 UV", check_uv),
        ("检查 Python", check_python),
        ("创建虚拟环境", create_venv),
        ("安装依赖", install_dependencies),
        ("下载模型", download_models),
        ("验证模型", verify_models),
    ]

    failed_steps = []
    for step_name, step_func in steps:
        if not step_func():
            failed_steps.append(step_name)

    print_header("部署完成！")

    if failed_steps:
        print_warning(f"以下步骤失败: {', '.join(failed_steps)}")
        print_warning("请检查错误信息并手动修复")
    else:
        print_success("KittenTTS 已成功部署")

    print_info("现在可以启动 Web UI 或使用其他脚本")
    print()
    print_info("可用命令:")
    print("  python deploy.py webui  # 启动 Web UI")
    print("  python deploy.py test   # 运行测试")
    print("  python deploy.py status # 查看状态")

def show_help():
    """显示帮助"""
    print("KittenTTS 一键部署脚本 (Python 版本)")
    print()
    print("用法: python deploy.py [命令]")
    print()
    print("命令:")
    print("  deploy    完整部署 (默认)")
    print("  webui     仅启动 Web UI")
    print("  test      运行测试")
    print("  status    查看状态")
    print("  models    下载模型")
    print("  help      显示帮助")
    print()
    print("示例:")
    print("  python deploy.py         # 完整部署")
    print("  python deploy.py webui   # 启动 Web UI")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        command = "deploy"
    else:
        command = sys.argv[1]

    commands = {
        "deploy": full_deploy,
        "webui": start_webui,
        "status": show_status,
        "models": download_models,
        "help": show_help,
        "--help": show_help,
        "-h": show_help,
    }

    if command in commands:
        commands[command]()
    elif command == "test":
        # 运行测试
        if Path("test_local_model.py").exists():
            print_info("运行本地模型测试...")
            os.system("source .venv/bin/activate && python test_local_model.py")
        else:
            print_error("未找到测试脚本")
    else:
        print_error(f"未知命令: {command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
