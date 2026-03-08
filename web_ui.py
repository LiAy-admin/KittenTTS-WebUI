import gradio as gr
import numpy as np
import soundfile as sf
import json
import os
import time
from kittentts.onnx_model import KittenTTS_1_Onnx

# 检测推理设备
def get_inference_device():
    """检测当前使用的推理设备"""
    try:
        import onnxruntime as ort
        available_providers = ort.get_available_providers()
        
        # 优先使用 GPU 提供者
        gpu_providers = ['CUDAExecutionProvider', 'DmlExecutionProvider', 'CoreMLExecutionProvider']
        for provider in gpu_providers:
            if provider in available_providers:
                return f"GPU ({provider})"
        
        # 如果没有 GPU，使用 CPU
        if 'CPUExecutionProvider' in available_providers:
            return "CPU"
        
        return "Unknown"
    except Exception as e:
        return f"Error: {str(e)}"

# 检测 GPU 支持状态
def check_gpu_support():
    """检测是否支持 GPU 推理"""
    try:
        import onnxruntime as ort
        available_providers = ort.get_available_providers()
        gpu_providers = ['CUDAExecutionProvider', 'DmlExecutionProvider', 'CoreMLExecutionProvider']
        
        for provider in gpu_providers:
            if provider in available_providers:
                return True, f"支持 GPU ({provider})"
        
        return False, "当前只支持 CPU 推理"
    except Exception as e:
        return False, f"检测失败: {str(e)}"

# 获取设备信息
device_info = get_inference_device()
gpu_supported, gpu_status = check_gpu_support()

# 模型配置
MODELS = {
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

# 全局模型缓存
model_cache = {}

def load_model(model_name, use_gpu=False):
    """加载指定模型"""
    cache_key = f"{model_name}_{'gpu' if use_gpu else 'cpu'}"
    if cache_key in model_cache:
        return model_cache[cache_key]
    
    info = MODELS[model_name]
    config_path = f"{info['path']}/config.json"
    
    if model_name == 'nano-int8':
        model_path = f"{info['path']}/kitten_tts_nano_v0_8.onnx"
    else:
        model_path = f"{info['path']}/kitten_tts_{model_name}_v0_8.onnx"
    
    voices_path = f"{info['path']}/voices.npz"
    
    if not os.path.exists(model_path):
        raise ValueError(f"模型文件不存在: {model_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # 设置推理提供者
    providers = []
    if use_gpu:
        # 优先使用 GPU 提供者（CUDA 优先，因为 cuDNN 比 TensorRT 更容易安装）
        gpu_providers = ['CUDAExecutionProvider', 'TensorrtExecutionProvider', 'DmlExecutionProvider', 'CoreMLExecutionProvider']
        import onnxruntime as ort
        available_providers = ort.get_available_providers()
        print(f"可用的推理提供者: {available_providers}")
        
        for provider in gpu_providers:
            if provider in available_providers:
                providers.append(provider)
                print(f"使用 GPU 提供者: {provider}")
                break
        
        if not providers:
            print("警告: 未找到可用的 GPU 提供者，回退到 CPU 模式")
            print("提示: 当前 CUDA 版本可能与 onnxruntime-gpu 不兼容")
            print("建议: 请参考 完整GPU配置指南.md 安装 cuDNN")
            providers.append('CPUExecutionProvider')
    else:
        providers.append('CPUExecutionProvider')
        print("使用 CPU 模式")
    
    print(f"正在加载模型: {model_name} (设备: {'GPU' if use_gpu else 'CPU'})")
    model = KittenTTS_1_Onnx(
        model_path=model_path,
        voices_path=voices_path,
        speed_priors=config.get("speed_priors", {}),
        voice_aliases=config.get("voice_aliases", {}),
        providers=providers
    )
    
    model_cache[cache_key] = model
    print(f"模型加载完成: {model_name}")
    return model

def generate_audio(text, model_name, voice, speed, use_gpu):
    """生成音频"""
    try:
        # 检查 GPU 支持
        if use_gpu and not gpu_supported:
            error_msg = f"❌ GPU 模式不可用\n\n{gpu_status}\n\n如需使用 GPU 加速，请执行以下步骤：\n1. 卸载当前版本: pip uninstall onnxruntime\n2. 安装 GPU 版本: pip install onnxruntime-gpu\n3. 确保已安装 NVIDIA 驱动和 CUDA"
            print(error_msg)
            return None, 0, 0, "", error_msg
        
        print(f"\n开始生成音频:")
        print(f"  文本: {text[:50]}...")
        print(f"  模型: {model_name}")
        print(f"  音色: {voice}")
        print(f"  语速: {speed}")
        print(f"  设备: {'GPU' if use_gpu else 'CPU'}")
        
        model = load_model(model_name, use_gpu)
        
        # 获取实际使用的推理提供者
        actual_provider = model.session.get_providers()[0]
        print(f"  实际使用: {actual_provider}")
        
        # 根据实际提供者确定设备类型
        if 'CUDA' in actual_provider or 'Dml' in actual_provider or 'CoreML' in actual_provider or 'Tensorrt' in actual_provider:
            device = "GPU"
        else:
            device = "CPU"
        
        start_time = time.time()
        audio = model.generate(text, voice=voice, speed=speed)
        elapsed = time.time() - start_time
        
        audio_length = len(audio) / 24000
        rt_factor = audio_length / elapsed if elapsed > 0 else 0
        
        print(f"生成完成:")
        print(f"  耗时: {elapsed:.2f}秒")
        print(f"  音频长度: {audio_length:.2f}秒")
        print(f"  实时率: {rt_factor:.2f}x")
        print(f"  设备显示: {device}")
        
        return audio, elapsed, rt_factor, device, None
    except Exception as e:
        print(f"生成音频失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, 0, 0, "", str(e)

def create_ui():
    """创建 Gradio 界面"""
    with gr.Blocks(title="KittenTTS Web UI") as demo:
        gr.Markdown(
            f"""
            # 🐱 KittenTTS Web UI
            
            超轻量级文本转语音模型，支持多种音色和模型选择。
            
            ## 💻 推理设备
            **当前使用：{device_info}**
            
            ## 📦 可用模型
            | 模型 | 参数 | 大小 | 特点 |
            |------|------|------|------|
            | Nano | 15M | 56MB | ⚡ 最快 |
            | Nano-INT8 | 15M | 25MB | 📦 最小体积 |
            | Micro | 40M | 41MB | ⚖️ 平衡 |
            | Mini | 80M | 80MB | 🎯 最高质量 |
            """
        )
        
        with gr.Row():
            with gr.Column(scale=3):
                text_input = gr.Textbox(
                    label="输入文本",
                    placeholder="请输入要转换的文本...",
                    lines=5,
                    value="Hello, this is a test of KittenTTS Web UI."
                )
                
                model_dropdown = gr.Dropdown(
                    label="选择模型",
                    choices=list(MODELS.keys()),
                    value="nano",
                    info="选择不同的模型会影响音质和生成速度"
                )
                
                voice_dropdown = gr.Dropdown(
                    label="选择音色",
                    choices=['Bella', 'Jasper', 'Luna', 'Bruno', 'Rosie', 'Hugo', 'Kiki', 'Leo'],
                    value='Bella',
                    info="选择不同的声音风格"
                )
                
                speed_slider = gr.Slider(
                    label="语速",
                    minimum=0.5,
                    maximum=2.0,
                    step=0.1,
                    value=1.0,
                    info="调整语音速度，1.0 为正常速度"
                )
            
            with gr.Column(scale=1):
                gpu_radio = gr.Radio(
                    label="推理模式",
                    choices=["CPU", "GPU"],
                    value="CPU",
                    info=f"当前: {gpu_status}"
                )
                
                generate_btn = gr.Button("🎤 生成音频", variant="primary", size="lg")
                
                audio_output = gr.Audio(label="生成的音频", autoplay=False)
                
                with gr.Accordion("📊 性能统计", open=False):
                    time_info = gr.Textbox(label="生成耗时", interactive=False)
                    length_info = gr.Textbox(label="音频长度", interactive=False)
                    rt_factor_info = gr.Textbox(label="实时率", interactive=False)
                    device_info_output = gr.Textbox(label="推理设备", interactive=False)
                
                with gr.Accordion("ℹ️ 模型信息", open=False):
                    model_info = gr.Textbox(label="当前模型", interactive=False)
                    voice_info = gr.Textbox(label="可用音色", interactive=False)
        
        def on_generate(text, model_name, voice, speed, use_gpu):
            """生成音频回调"""
            if not text or not text.strip():
                return None, "", "", "", "", ""
            
            audio, elapsed, rt_factor, device, error = generate_audio(text, model_name, voice, speed, use_gpu)
            
            if error:
                return None, f"❌ 错误: {error}", "", "", "", ""
            
            audio_length = len(audio) / 24000
            model_desc = MODELS[model_name]['desc']
            
            return (
                (24000, audio),
                f"{elapsed:.2f} 秒",
                f"{audio_length:.2f} 秒",
                f"{rt_factor:.2f}x",
                device,
                f"{model_name.upper()} ({MODELS[model_name]['params']} 参数, {MODELS[model_name]['size']}) - {model_desc}"
            )
        
        def on_model_change(model_name):
            """模型改变时更新信息"""
            model_desc = MODELS[model_name]['desc']
            try:
                model = load_model(model_name)
                voices = ', '.join(model.all_voice_names)
                return f"{model_desc}", f"{voices}"
            except Exception as e:
                return f"{model_desc}", f"加载失败: {str(e)}"
        
        generate_btn.click(
            fn=on_generate,
            inputs=[text_input, model_dropdown, voice_dropdown, speed_slider, gpu_radio],
            outputs=[audio_output, time_info, length_info, rt_factor_info, device_info_output, model_info]
        )
        
        model_dropdown.change(
            fn=on_model_change,
            inputs=[model_dropdown],
            outputs=[model_info, voice_info]
        )
        
        gr.Examples(
            examples=[
                ["Hello, welcome to KittenTTS!", "nano", "Bella", 1.0, "CPU"],
                ["This is a test of the text-to-speech model.", "micro", "Jasper", 1.0, "CPU"],
                ["The quick brown fox jumps over the lazy dog.", "mini", "Luna", 1.2, "CPU"],
                ["你好，这是一个测试。", "nano", "Bruno", 1.0, "CPU"],
            ],
            inputs=[text_input, model_dropdown, voice_dropdown, speed_slider, gpu_radio],
        )
        
        gr.Markdown(
            """
            ---
            
            ### 💡 使用提示
            
            1. **Nano 模型**：生成速度最快，适合实时应用
            2. **Nano-INT8 模型**：体积最小，适合资源受限环境
            3. **Micro 模型**：速度和质量平衡，适合大多数场景
            4. **Mini 模型**：音质最好，适合播客和有声读物
            
            ### 🔗 相关链接
            
            - [GitHub](https://github.com/KittenML/KittenTTS)
            - [Hugging Face](https://huggingface.co/KittenML)
            - [在线 Demo](https://huggingface.co/spaces/KittenML/KittenTTS-Demo)
            """
        )
    
    return demo

def find_available_port(start_port=7860, max_attempts=10):
    """查找可用的端口"""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                s.close()
                return port
        except OSError:
            continue
    raise OSError(f"无法在 {start_port}-{start_port + max_attempts} 范围内找到可用端口")

if __name__ == "__main__":
    demo = create_ui()
    
    # 自动查找可用端口
    try:
        port = find_available_port(7860)
        print(f"✓ 使用端口: {port}")
    except OSError as e:
        print(f"✗ {e}")
        port = 7860
    
    # 获取本机 IP 地址
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"✓ 局域网访问地址: http://{local_ip}:{port}")
    print(f"✓ 本地访问地址: http://127.0.0.1:{port}")
    print(f"✓ 公网访问: 如需公网访问，请设置 share=True（需要下载 frpc）")
    print()
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        show_error=True
    )
