# KittenTTS 使用示例

## 🚀 快速启动

### 方法 1: 使用快速启动脚本
```bash
# Bash 版本
./start.sh

# Python 版本
python start.py
```

### 方法 2: 使用部署脚本
```bash
# Bash 版本
./deploy.sh webui

# Python 版本
python deploy.py webui
```

### 方法 3: 直接运行
```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动 Web UI
python web_ui.py
```

## 📱 Web UI 使用

1. **启动服务**
   ```bash
   ./start.sh
   ```

2. **访问界面**
   - 打开浏览器访问: `http://localhost:7860`
   - 或在局域网内访问: `http://你的IP:7860`

3. **生成语音**
   - 输入文本: "Hello, welcome to KittenTTS!"
   - 选择模型: nano (最快) / micro (平衡) / mini (最高质量)
   - 选择音色: Bella / Jasper / Luna / Bruno / Rosie / Hugo / Kiki / Leo
   - 调整语速: 0.5 (慢) - 2.0 (快)
   - 点击"生成音频"按钮

4. **下载音频**
   - 生成完成后，点击音频播放器右侧的下载按钮
   - 音频保存为 WAV 格式，采样率 24000Hz

## 💻 命令行使用

### 基础示例

```python
from kittentts.onnx_model import KittenTTS_1_Onnx
import json
import soundfile as sf

# 加载模型
config_path = "models/nano/config.json"
model_path = "models/nano/kitten_tts_nano_v0_8.onnx"
voices_path = "models/nano/voices.npz"

with open(config_path, 'r') as f:
    config = json.load(f)

model = KittenTTS_1_Onnx(
    model_path=model_path,
    voices_path=voices_path,
    speed_priors=config.get("speed_priors", {}),
    voice_aliases=config.get("voice_aliases", {})
)

# 生成音频
text = "Hello, this is a test of the KittenTTS model."
voice = "Bella"
speed = 1.0

audio = model.generate(text, voice=voice, speed=speed)

# 保存音频
sf.write('output.wav', audio, 24000)
print("✓ 音频已保存到 output.wav")
```

### 批量生成示例

```python
from kittentts.onnx_model import KittenTTS_1_Onnx
import json
import soundfile as sf

# 加载模型（同上）

# 批量生成
texts = [
    "This is the first sentence.",
    "This is the second sentence.",
    "This is the third sentence."
]

for i, text in enumerate(texts):
    audio = model.generate(text, voice="Bella", speed=1.0)
    sf.write(f'output_{i+1}.wav', audio, 24000)
    print(f"✓ 已生成: output_{i+1}.wav")
```

### 不同音色示例

```python
# 可用音色
voices = ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']

text = "Hello, welcome to KittenTTS!"

for voice in voices:
    audio = model.generate(text, voice=voice, speed=1.0)
    sf.write(f'{voice}.wav', audio, 24000)
    print(f"✓ 已生成: {voice}.wav")
```

### 不同模型对比

```python
from kittentts.onnx_model import KittenTTS_1_Onnx
import json
import time

models = {
    'nano': 'models/nano',
    'nano-int8': 'models/nano-int8',
    'micro': 'models/micro',
    'mini': 'models/mini'
}

text = "This is a comparison test of different models."

for model_name, model_dir in models.items():
    # 加载模型
    config_path = f"{model_dir}/config.json"
    model_path = f"{model_dir}/kitten_tts_nano_v0_8.onnx" if model_name == 'nano-int8' else f"{model_dir}/kitten_tts_{model_name}_v0_8.onnx"
    voices_path = f"{model_dir}/voices.npz"

    with open(config_path, 'r') as f:
        config = json.load(f)

    model = KittenTTS_1_Onnx(
        model_path=model_path,
        voices_path=voices_path,
        speed_priors=config.get("speed_priors", {}),
        voice_aliases=config.get("voice_aliases", {})
    )

    # 生成并计时
    start_time = time.time()
    audio = model.generate(text, voice="Bella", speed=1.0)
    elapsed = time.time() - start_time

    print(f"{model_name}: {elapsed:.2f}秒")
```

## 🎯 使用场景

### 1. 实时语音合成
```python
# 使用 nano 模型获得最快速度
model = load_model('models/nano')
audio = model.generate(text, voice="Bella", speed=1.0)
```

### 2. 高质量语音
```python
# 使用 mini 模型获得最佳音质
model = load_model('models/mini')
audio = model.generate(text, voice="Bella", speed=1.0)
```

### 3. 资源受限环境
```python
# 使用 nano-int8 模型最小化资源使用
model = load_model('models/nano-int8')
audio = model.generate(text, voice="Bella", speed=1.0)
```

### 4. 播客/有声读物
```python
# 使用 mini 模型 + 慢速语速
model = load_model('models/mini')
audio = model.generate(text, voice="Jasper", speed=0.9)
```

## 📊 性能参考

| 模型 | 推理速度 | 音质 | 内存使用 | 适用场景 |
|------|---------|------|---------|---------|
| nano | ⚡⚡⚡ | ⭐⭐⭐ | 低 | 实时应用 |
| nano-int8 | ⚡⚡⚡ | ⭐⭐⭐ | 极低 | 嵌入式设备 |
| micro | ⚡⚡ | ⭐⭐⭐⭐ | 中等 | 日常使用 |
| mini | ⚡ | ⭐⭐⭐⭐⭐ | 高 | 专业应用 |

## 🔧 高级配置

### 调整语速
```python
# 0.5 = 慢速, 1.0 = 正常, 2.0 = 快速
audio = model.generate(text, voice="Bella", speed=0.8)
```

### 文本预处理
```python
# 自动清理文本
audio = model.generate(text, voice="Bella", clean_text=True)
```

### 批量生成（优化）
```python
# 预加载模型，避免重复加载
# 生成多个音频时保持模型在内存中
for text in texts:
    audio = model.generate(text, voice="Bella", speed=1.0)
    # 保存音频
```

## 🐛 常见问题

### Q: 如何选择合适的模型？
A:
- 需要**最快速度**: nano
- 需要**最小体积**: nano-int8
- 需要**平衡性能**: micro
- 需要**最高音质**: mini

### Q: 音色可以混合使用吗？
A: 不可以，每次生成只能使用一个音色。如需混合音色，需要分段生成。

### Q: 支持多语言吗？
A: 主要支持英语，对其他语言的支持有限。

### Q: 可以调整音高吗？
A: 当前版本不支持直接调整音高，可以通过选择不同音色来实现。

## 📞 获取帮助

- 查看 README.md 了解部署方法
- 运行 `./deploy.sh help` 查看部署脚本帮助
- 查看 MODEL_STATUS.md 了解模型状态

---

**祝你使用愉快！** 🎉
