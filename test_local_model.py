from kittentts.get_model import download_from_huggingface, KittenTTS
from kittentts.onnx_model import KittenTTS_1_Onnx
import json

# 使用本地模型文件
config_path = "models/nano/config.json"
model_path = "models/nano/kitten_tts_nano_v0_8.onnx"
voices_path = "models/nano/voices.npz"

# 加载配置
with open(config_path, 'r') as f:
    config = json.load(f)

print("配置信息:", config)

# 创建模型实例
model = KittenTTS_1_Onnx(
    model_path=model_path,
    voices_path=voices_path,
    speed_priors=config.get("speed_priors", {}),
    voice_aliases=config.get("voice_aliases", {})
)

print("✓ 模型加载成功!")
print("✓ 可用音色:", model.all_voice_names)

# 生成测试音频
text = "Hello, this is a test of the KittenTTS model."
voice = "Bella"

print(f"\n生成音频: {text}")
print(f"使用音色: {voice}")

audio = model.generate(text, voice=voice)
print(f"✓ 音频生成成功! 形状: {audio.shape}")

# 保存音频
import soundfile as sf
sf.write('test_output.wav', audio, 24000)
print("✓ 音频已保存到 test_output.wav")
