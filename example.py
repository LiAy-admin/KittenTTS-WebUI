from kittentts.onnx_model import KittenTTS_1_Onnx
import json
import soundfile as sf

# 使用本地模型文件
config_path = "models/nano/config.json"
model_path = "models/nano/kitten_tts_nano_v0_8.onnx"
voices_path = "models/nano/voices.npz"

# 加载配置
with open(config_path, 'r') as f:
    config = json.load(f)

# Step 1: Load the model from local files
print("Loading model from local files...")
model = KittenTTS_1_Onnx(
    model_path=model_path,
    voices_path=voices_path,
    speed_priors=config.get("speed_priors", {}),
    voice_aliases=config.get("voice_aliases", {})
)
print(f"✓ Model loaded successfully!")
print(f"✓ Available voices: {', '.join(model.all_voice_names)}")

# Step 2: Generate the audio

# this is a sample from the TinyStories dataset. 
text ="""One day, a little girl named Lily found a needle in her room. She knew it was difficult to play with it because it was sharp. Lily wanted to share the needle with her mom, so she could sew a button on her shirt.
Lily went to her mom and said, "Mom, I found this needle. Can you share it with me and sew my shirt?" Her mom smiled and said, "Yes, Lily, we can share the needle and fix your shirt."
Together, they shared the needle and sewed the button on Lily's shirt. It was not difficult for them because they were sharing and helping each other. After they finished, Lily thanked her mom for sharing the needle and fixing her shirt. They both felt happy because they had shared and worked together."""

# available_voices : ['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo']
voice = 'Bruno'

print(f"\nGenerating audio...")
print(f"Text: {text[:100]}...")
print(f"Voice: {voice}")

audio = model.generate(text, voice=voice)

# Save the audio
sf.write('output.wav', audio, 24000)
print(f"✓ Audio saved to output.wav")
print(f"✓ Audio length: {len(audio) / 24000:.2f} seconds")
