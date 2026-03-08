#!/usr/bin/env python3
"""
修复 gradio-client 库的 TypeError bug

这个脚本会自动修复 gradio-client 库中的两个已知问题：
1. get_type 函数中 schema 参数类型检查
2. additionalProperties 参数为布尔值的处理

使用方法：
- 在安装依赖后自动运行
- 或手动运行: python fix_gradio_client.py
"""

import os
import sys
from pathlib import Path


def find_gradio_client_utils():
    """查找 gradio_client/utils.py 文件"""
    venv_path = Path(".venv")
    
    if not venv_path.exists():
        print("❌ 虚拟环境不存在")
        return None
    
    possible_paths = [
        venv_path / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages" / "gradio_client" / "utils.py",
        venv_path / "lib64" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages" / "gradio_client" / "utils.py",
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None


def fix_get_type_function(content):
    """修复 get_type 函数"""
    old_code = """def get_type(schema: dict):
    if "const" in schema:
        return "const\""""
    
    new_code = """def get_type(schema: dict):
    if not isinstance(schema, dict):
        return "any"
    if "const" in schema:
        return "const\""""
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        print("  ✓ 修复 get_type 函数的类型检查")
        return True
    return False


def fix_additional_properties(content):
    """修复 additionalProperties 处理"""
    old_code = """        if "additionalProperties" in schema:
            des += [
                f"str, {_json_schema_to_python_type(schema['additionalProperties'], defs)}"
            ]"""
    
    new_code = """        if "additionalProperties" in schema:
            additional_props = schema['additionalProperties']
            if isinstance(additional_props, bool):
                des.append("str, any")
            else:
                des.append(f"str, {_json_schema_to_python_type(additional_props, defs)}")"""
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        print("  ✓ 修复 additionalProperties 的布尔值处理")
        return True
    return False


def main():
    print("=" * 60)
    print("修复 gradio-client 库的 TypeError bug")
    print("=" * 60)
    print()
    
    utils_path = find_gradio_client_utils()
    
    if not utils_path:
        print("❌ 未找到 gradio_client/utils.py 文件")
        print("   请确保已安装 gradio-client 库")
        sys.exit(1)
    
    print(f"找到文件: {utils_path}")
    print()
    
    with open(utils_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("应用修复...")
    fixed1 = fix_get_type_function(content)
    fixed2 = fix_additional_properties(content)
    
    if fixed1 or fixed2:
        with open(utils_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print()
        print("✅ 修复完成！")
        print()
        print("修复内容:")
        if fixed1:
            print("  1. 添加了 schema 参数的类型检查")
        if fixed2:
            print("  2. 添加了 additionalProperties 布尔值的处理")
        print()
    else:
        print()
        print("ℹ️  无需修复，文件已经是最新的")
        print()
    
    print("=" * 60)


if __name__ == "__main__":
    main()