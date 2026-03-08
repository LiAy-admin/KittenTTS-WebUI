#!/usr/bin/env python3
"""从 Hugging Face 下载缺失的 KittenTTS 模型"""

import os
import sys

# 使用国内镜像加速下载
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from huggingface_hub import snapshot_download

print("=" * 80)
print("从 Hugging Face 下载缺失的 KittenTTS 模型")
print("使用国内镜像: https://hf-mirror.com")
print("=" * 80)

# 模型配置
MODELS_TO_DOWNLOAD = {
    'micro': {
        'repo_id': 'KittenML/kitten-tts-micro-0.8',
        'local_dir': 'models/micro',
        'description': '40M 参数, 41MB - 速度与质量平衡'
    },
    'mini': {
        'repo_id': 'KittenML/kitten-tts-mini-0.8',
        'local_dir': 'models/mini',
        'description': '80M 参数, 80MB - 最高质量'
    }
}

def download_model(model_name, repo_id, local_dir, description):
    """从 Hugging Face 下载模型"""
    print(f"\n📦 开始下载 {model_name.upper()} 模型")
    print(f"   仓库: {repo_id}")
    print(f"   本地路径: {local_dir}")
    print(f"   描述: {description}")
    
    try:
        model_dir = snapshot_download(
            repo_id=repo_id,
            cache_dir='models',
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print(f"✓ 模型下载成功!")
        print(f"📂 模型路径: {model_dir}")
        
        # 列出下载的文件
        files = os.listdir(local_dir)
        print(f"\n📄 下载的文件:")
        for f in files:
            if not f.startswith('.'):
                file_path = os.path.join(local_dir, f)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    size_mb = size / 1024 / 1024
                    print(f"  - {f}: {size_mb:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success_count = 0
    total_count = len(MODELS_TO_DOWNLOAD)
    
    for model_name, config in MODELS_TO_DOWNLOAD.items():
        if download_model(model_name, config['repo_id'], config['local_dir'], config['description']):
            success_count += 1
    
    print("\n" + "=" * 80)
    print("下载完成!")
    print("=" * 80)
    print(f"✓ 成功: {success_count}/{total_count}")
    print(f"❌ 失败: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n🎉 所有模型下载完成!")
        print("\n💡 现在可以使用以下命令测试:")
        print("  - python compare_models.py")
        print("  - python web_ui.py (支持所有模型)")
    else:
        print("\n⚠️  部分模型下载失败，请检查网络连接后重试")

if __name__ == "__main__":
    main()
