import os
import sys

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from huggingface_hub import snapshot_download

print("使用国内镜像: https://hf-mirror.com")
print("开始下载 nano-int8 模型 (15M参数, 25MB)...")

try:
    int8_dir = snapshot_download(
        repo_id='KittenML/kitten-tts-nano-0.8-int8',
        cache_dir='models',
        local_dir='models/nano-int8',
        local_dir_use_symlinks=False
    )
    print(f"✓ 模型下载到: {int8_dir}")
    
    import os
    files = os.listdir('models/nano-int8')
    print(f"✓ 文件列表: {files}")
    
    for f in files:
        if not f.startswith('.'):
            size = os.path.getsize(f'models/nano-int8/{f}')
            print(f"  - {f}: {size/1024/1024:.2f} MB")
    
    print("\n✓ nano-int8 模型下载完成！")
    
except Exception as e:
    print(f"❌ 下载失败: {e}")
    sys.exit(1)
