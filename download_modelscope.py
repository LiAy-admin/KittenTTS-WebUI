#!/usr/bin/env python3
"""使用 ModelScope 下载 KittenTTS 模型"""

from modelscope import snapshot_download
import os
import sys

print("=" * 60)
print("使用魔塔社区 (ModelScope) 下载 KittenTTS 模型")
print("=" * 60)

# 模型映射：Hugging Face -> ModelScope
MODEL_MAPPING = {
    'KittenML/kitten-tts-nano-0.8': 'KittenML/kitten-tts-nano-0.8',
    'KittenML/kitten-tts-nano-0.8-int8': 'KittenML/kitten-tts-nano-0.8-int8',
    'KittenML/kitten-tts-base-0.8': 'KittenML/kitten-tts-base-0.8',
}

def download_model(model_id, cache_dir='models'):
    """从 ModelScope 下载模型"""
    print(f"\n📦 开始下载模型: {model_id}")
    print(f"📁 缓存目录: {cache_dir}")
    
    try:
        model_dir = snapshot_download(
            model_id,
            cache_dir=cache_dir,
            revision='master'
        )
        print(f"✓ 模型下载成功!")
        print(f"📂 模型路径: {model_dir}")
        
        # 列出下载的文件
        files = os.listdir(model_dir)
        print(f"\n📄 下载的文件:")
        for f in files:
            if not f.startswith('.'):
                file_path = os.path.join(model_dir, f)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    size_mb = size / 1024 / 1024
                    print(f"  - {f}: {size_mb:.2f} MB")
        
        return model_dir
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

def main():
    print("\n可用的模型:")
    for i, (hf_id, ms_id) in enumerate(MODEL_MAPPING.items(), 1):
        print(f"  {i}. {ms_id}")
    
    print("\n下载所有推荐模型...")
    
    success_count = 0
    for hf_id, ms_id in MODEL_MAPPING.items():
        model_dir = download_model(ms_id)
        if model_dir:
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"下载完成! 成功: {success_count}/{len(MODEL_MAPPING)}")
    print("=" * 60)
    
    print("\n💡 使用提示:")
    print("  models/")
    print("    └── KittenML/")
    print("        ├── kitten-tts-nano-0.8/")
    print("        ├── kitten-tts-nano-0.8-int8/")
    print("        └── kitten-tts-base-0.8/")
    print("")
    print("  可以在代码中直接使用模型路径!")

if __name__ == "__main__":
    main()
