#!/usr/bin/env python3
"""检查项目中所有模型路径配置"""

import os
import json

print("=" * 80)
print("KittenTTS 模型路径检测报告")
print("=" * 80)

# 1. 检查实际下载的模型位置
print("\n📂 实际下载的模型位置：")
actual_models = []
for root, dirs, files in os.walk('/workspace/models/KittenML'):
    if 'config.json' in files:
        rel_path = os.path.relpath(root, '/workspace/models')
        actual_models.append(rel_path)
        # 读取配置
        config_path = os.path.join(root, 'config.json')
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"  ✓ {rel_path}")
            print(f"    - config.json: 存在")
            print(f"    - kitten_tts_nano_v0_8.onnx: {os.path.exists(os.path.join(root, 'kitten_tts_nano_v0_8.onnx'))}")
            print(f"    - voices.npz: {os.path.exists(os.path.join(root, 'voices.npz'))}")
        except Exception as e:
            print(f"  ❌ {rel_path}: {e}")

# 2. 检查符号链接
print("\n🔗 符号链接检查：")
expected_links = ['nano', 'nano-int8', 'micro', 'mini']
for link in expected_links:
    link_path = f'/workspace/models/{link}'
    if os.path.islink(link_path):
        target = os.readlink(link_path)
        target_abs = os.path.join('/workspace/models', target)
        exists = os.path.exists(target_abs)
        status = "✓" if exists else "❌"
        print(f"  {status} {link} -> {target} {'(有效)' if exists else '(无效)'}")
    elif os.path.isdir(link_path):
        print(f"  ✓ {link} (目录)")
    else:
        print(f"  ❌ {link} (不存在)")

# 3. 检查各脚本中的路径配置
print("\n📝 脚本路径配置检查：")

scripts = {
    'web_ui.py': {
        'paths': {
            'nano': 'models/nano',
            'nano-int8': 'models/nano-int8',
            'micro': 'models/micro',
            'mini': 'models/mini'
        }
    },
    'compare_models.py': {
        'paths': {
            'nano': 'models/nano',
            'nano-int8': 'models/nano-int8',
            'micro': 'models/micro',
            'mini': 'models/mini'
        }
    },
    'test_local_model.py': {
        'paths': {
            'nano': 'models/nano'
        }
    },
    'example.py': {
        'paths': {
            'nano': 'models/nano'
        }
    }
}

for script, config in scripts.items():
    print(f"\n  📄 {script}:")
    for model, path in config['paths'].items():
        full_path = f"/workspace/{path}"
        exists = os.path.exists(full_path)
        if exists:
            # 检查关键文件
            config_file = os.path.join(full_path, 'config.json')
            model_file = os.path.join(full_path, 'kitten_tts_nano_v0_8.onnx' if model == 'nano-int8' else f'kitten_tts_{model}_v0_8.onnx')
            voices_file = os.path.join(full_path, 'voices.npz')

            config_ok = os.path.exists(config_file)
            model_ok = os.path.exists(model_file)
            voices_ok = os.path.exists(voices_file)

            if config_ok and model_ok and voices_ok:
                print(f"    ✓ {model}: {path} (完整)")
            else:
                print(f"    ⚠️  {model}: {path} (不完整)")
                if not config_ok:
                    print(f"       ❌ config.json 缺失")
                if not model_ok:
                    print(f"       ❌ {os.path.basename(model_file)} 缺失")
                if not voices_ok:
                    print(f"       ❌ voices.npz 缺失")
        else:
            print(f"    ❌ {model}: {path} (路径不存在)")

# 4. 总结
print("\n" + "=" * 80)
print("总结")
print("=" * 80)

available_models = []
for model in ['nano', 'nano-int8']:
    path = f'/workspace/models/{model}'
    if os.path.exists(path):
        config_file = os.path.join(path, 'config.json')
        if os.path.exists(config_file):
            available_models.append(model)

print(f"\n✓ 可用模型: {', '.join(available_models)}")
print(f"❌ 缺失模型: {', '.join(['micro', 'mini'])}")

if available_models:
    print("\n💡 可以正常运行以下脚本:")
    print("  - python test_local_model.py")
    print("  - python example.py")
    print("  - python web_ui.py (仅使用 nano 和 nano-int8 模型)")
else:
    print("\n❌ 没有可用的模型，请先下载模型！")
