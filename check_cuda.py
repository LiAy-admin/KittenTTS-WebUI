"""
检查 CUDA 和 GPU 支持状态
"""
import subprocess
import sys

print("=" * 60)
print("CUDA 和 GPU 支持检查")
print("=" * 60)

# 检查 CUDA 版本
print("\n[1] 检查 CUDA 版本...")
try:
    result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
    print(f"✓ CUDA 版本: {result.stdout.strip()}")
except FileNotFoundError:
    print("✗ nvcc 未找到，可能未安装 CUDA Toolkit")
except Exception as e:
    print(f"✗ 检查 CUDA 版本失败: {e}")

# 检查 NVIDIA 驱动
print("\n[2] 检查 NVIDIA 驱动...")
try:
    result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    for line in lines:
        if 'CUDA Version' in line:
            print(f"✓ {line.strip()}")
            break
except FileNotFoundError:
    print("✗ nvidia-smi 未找到")
except Exception as e:
    print(f"✗ 检查 NVIDIA 驱动失败: {e}")

# 检查 onnxruntime
print("\n[3] 检查 onnxruntime...")
try:
    import onnxruntime as ort
    print(f"✓ ONNX Runtime 版本: {ort.__version__}")
    print(f"✓ 可用的提供者: {ort.get_available_providers()}")
except ImportError:
    print("✗ onnxruntime 未安装")
except Exception as e:
    print(f"✗ 检查 onnxruntime 失败: {e}")

# 检查 GPU 信息
print("\n[4] 检查 GPU 信息...")
try:
    result = subprocess.run(['nvidia-smi', '--query-gpu=name,compute_cap,driver_version', '--format=csv,noheader'], capture_output=True, text=True)
    print(f"✓ GPU 名称: {result.stdout.strip()}")
except Exception as e:
    print(f"✗ 检查 GPU 信息失败: {e}")

# 兼容性检查
print("\n[5] 兼容性检查...")
print("\nONNX Runtime GPU 要求:")
print("  - CUDA 12.x")
print("  - cuDNN 9.x")
print("\n当前系统:")
try:
    result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'CUDA Version' in line:
            cuda_version = line.split('CUDA Version:')[1].strip()
            print(f"  - CUDA {cuda_version}")
            break
except:
    pass

# 建议
print("\n" + "=" * 60)
print("建议:")
print("=" * 60)

if '12.' in cuda_version:
    print("✓ CUDA 版本兼容，可以使用 GPU 推理")
else:
    print("✗ CUDA 版本不兼容")
    print("\n解决方案:")
    print("1. 降级 CUDA 到 12.4 版本")
    print("   下载地址: https://developer.nvidia.com/cuda-12-4-0-download-archive")
    print("2. 参考 CUDA降级指南.md 获取详细步骤")
    print("3. 或者等待 onnxruntime-gpu 更新支持 CUDA 13.x")

print("\n" + "=" * 60)
