#!/usr/bin/env python3
"""
KittenTTS 快速启动脚本
"""

import os
import sys
from pathlib import Path

def main():
    print("🚀 启动 KittenTTS Web UI...")
    print()

    # 检查虚拟环境
    if not Path(".venv").exists():
        print("❌ 虚拟环境不存在，请先运行: python deploy.py")
        sys.exit(1)

    # 检查模型
    if not Path("models/nano").exists():
        print("❌ 模型不存在，请先运行: python deploy.py")
        sys.exit(1)

    # 启动 Web UI
    os.system("source .venv/bin/activate && python web_ui.py")

if __name__ == "__main__":
    main()
