from kittentts.onnx_model import KittenTTS_1_Onnx
import json
import os
import time

models_info = {
    'nano': {
        'path': 'models/nano',
        'params': '15M',
        'size': '56MB',
        'desc': '超轻量，最快'
    },
    'nano-int8': {
        'path': 'models/nano-int8',
        'params': '15M',
        'size': '25MB',
        'desc': '最小体积，INT8量化'
    },
    'micro': {
        'path': 'models/micro',
        'params': '40M',
        'size': '41MB',
        'desc': '速度与质量平衡'
    },
    'mini': {
        'path': 'models/mini',
        'params': '80M',
        'size': '80MB',
        'desc': '最高质量'
    }
}

test_text = "Hello, this is a test of the KittenTTS model with different sizes."
voice = "Bella"

print("=" * 60)
print("KittenTTS 模型对比测试")
print("=" * 60)

for model_name, info in models_info.items():
    print(f"\n📦 测试 {model_name.upper()} 模型 ({info['params']} 参数, {info['size']})")
    print(f"   描述: {info['desc']}")
    
    config_path = f"{info['path']}/config.json"
    
    if model_name == 'nano-int8':
        model_path = f"{info['path']}/kitten_tts_nano_v0_8.onnx"
    else:
        model_path = f"{info['path']}/kitten_tts_{model_name}_v0_8.onnx"
    
    voices_path = f"{info['path']}/voices.npz"
    
    if not os.path.exists(model_path):
        print(f"   ❌ 模型文件不存在: {model_path}")
        continue
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    model = KittenTTS_1_Onnx(
        model_path=model_path,
        voices_path=voices_path,
        speed_priors=config.get("speed_priors", {}),
        voice_aliases=config.get("voice_aliases", {})
    )
    
    print(f"   ✓ 模型加载成功")
    print(f"   可用音色: {', '.join(model.all_voice_names)}")
    
    start_time = time.time()
    audio = model.generate(test_text, voice=voice)
    elapsed = time.time() - start_time
    
    print(f"   ✓ 音频生成成功")
    print(f"   音频长度: {len(audio) / 24000:.2f} 秒")
    print(f"   生成耗时: {elapsed:.2f} 秒")
    print(f"   实时率: {len(audio) / 24000 / elapsed:.2f}x")
    
    import soundfile as sf
    output_file = f"test_{model_name}_{voice}.wav"
    sf.write(output_file, audio, 24000)
    print(f"   ✓ 已保存到: {output_file}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
