#!/usr/bin/env python3
from kittentts.onnx_model import KittenTTS_1_Onnx
import json
import os

models = {
    'nano': 'models/nano',
    'nano-int8': 'models/nano-int8',
    'micro': 'models/micro',
    'mini': 'models/mini'
}

print('测试所有模型加载...')
for name, path in models.items():
    try:
        config_path = f'{path}/config.json'
        if name == 'nano-int8':
            model_path = f'{path}/kitten_tts_nano_v0_8.onnx'
        else:
            model_path = f'{path}/kitten_tts_{name}_v0_8.onnx'
        voices_path = f'{path}/voices.npz'

        if not os.path.exists(model_path):
            print(f'❌ {name}: 模型文件不存在')
            continue

        with open(config_path, 'r') as f:
            config = json.load(f)

        model = KittenTTS_1_Onnx(
            model_path=model_path,
            voices_path=voices_path,
            speed_priors=config.get('speed_priors', {}),
            voice_aliases=config.get('voice_aliases', {})
        )

        print(f'✓ {name}: 加载成功, {len(model.all_voice_names)} 个音色')
    except Exception as e:
        print(f'❌ {name}: {str(e)}')
