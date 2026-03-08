#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kittentts.onnx_model import KittenTTS_1_Onnx
import json
import numpy as np

print("=" * 60)
print("测试 KittenTTS 模型加载和音频生成")
print("=" * 60)

model_name = "nano"
info = {
    'path': f'models/{model_name}',
    'params': '15M',
    'size': '56MB',
    'desc': '超轻量，最快'
}

config_path = f"{info['path']}/config.json"
model_path = f"{info['path']}/kitten_tts_{model_name}_v0_8.onnx"
voices_path = f"{info['path']}/voices.npz"

print(f"\n[1] 检查文件...")
print(f"  配置文件: {config_path} - {'✓' if os.path.exists(config_path) else '✗'}")
print(f"  模型文件: {model_path} - {'✓' if os.path.exists(model_path) else '✗'}")
print(f"  音色文件: {voices_path} - {'✓' if os.path.exists(voices_path) else '✗'}")

if not os.path.exists(model_path):
    print(f"\n✗ 错误: 模型文件不存在")
    sys.exit(1)

print(f"\n[2] 加载配置...")
with open(config_path, 'r') as f:
    config = json.load(f)
print(f"  ✓ 配置加载成功")

print(f"\n[3] 加载模型 (CPU 模式)...")
try:
    model = KittenTTS_1_Onnx(
        model_path=model_path,
        voices_path=voices_path,
        speed_priors=config.get("speed_priors", {}),
        voice_aliases=config.get("voice_aliases", {}),
        providers=['CPUExecutionProvider']
    )
    print(f"  ✓ 模型加载成功")
except Exception as e:
    print(f"  ✗ 模型加载失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print(f"\n[4] 测试音频生成...")
test_text = "Hello, this is a test."
voice = "Bella"
speed = 1.0

print(f"  文本: {test_text}")
print(f"  音色: {voice}")
print(f"  语速: {speed}")

try:
    audio = model.generate(test_text, voice=voice, speed=speed)
    print(f"  ✓ 音频生成成功")
    print(f"  音频长度: {len(audio)} 采样点")
    print(f"  音频时长: {len(audio) / 24000:.2f} 秒")
    
    # 检查音频数据
    if isinstance(audio, np.ndarray):
        print(f"  音频类型: numpy.ndarray")
        print(f"  音频形状: {audio.shape}")
        print(f"  音频数据类型: {audio.dtype}")
        print(f"  音频范围: [{audio.min():.3f}, {audio.max():.3f}]")
    else:
        print(f"  音频类型: {type(audio)}")
    
    print(f"\n[5] 测试完成 ✓")
    print(f"\n模型工作正常！")
    
except Exception as e:
    print(f"  ✗ 音频生成失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)