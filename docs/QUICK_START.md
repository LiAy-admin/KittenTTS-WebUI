# KittenTTS 快速参考卡

## 🚀 一键部署

### Bash 版本（推荐）
```bash
# 首次部署
./deploy.sh

# 快速启动
./start.sh

# 查看状态
./deploy.sh status
```

### Python 版本（跨平台）
```bash
# 首次部署
python deploy.py

# 快速启动
python start.py

# 查看状态
python deploy.py status
```

## 📱 Web UI 使用

1. **启动**: `./start.sh`
2. **访问**: `http://localhost:7860`
3. **输入文本**: 输入要转换的文本
4. **选择模型**: nano/micro/mini/nano-int8
5. **选择音色**: Bella/Jasper/Luna/Bruno/Rosie/Hugo/Kiki/Leo
6. **调整语速**: 0.5 - 2.0
7. **生成**: 点击"生成音频"按钮

## 🎤 模型选择

| 模型 | 参数 | 大小 | 特点 | 适用场景 |
|------|------|------|------|---------|
| nano | 15M | 56MB | ⚡ 最快 | 实时应用 |
| nano-int8 | 15M | 25MB | 📦 最小 | 嵌入式设备 |
| micro | 40M | 41MB | ⚖️ 平衡 | 日常使用 |
| mini | 80M | 80MB | 🎯 最高质量 | 专业应用 |

## 📝 常用命令

### 部署相关
```bash
./deploy.sh deploy    # 完整部署
./deploy.sh models    # 下载模型
./deploy.sh status    # 查看状态
./deploy.sh help      # 查看帮助
```

### 应用相关
```bash
python test_local_model.py    # 测试模型
python example.py             # 运行示例
python compare_models.py      # 模型对比
```

### 工具相关
```bash
python verify_all_models.py       # 验证模型
python check_model_paths.py       # 检查路径
python check_cuda.py              # 检查 CUDA
```

## 📚 文档导航

| 文档 | 用途 |
|------|------|
| README.md | 项目说明 |
| DEPLOYMENT.md | 部署指南 |
| USAGE.md | 使用示例 |
| MODEL_STATUS.md | 模型信息 |
| PROJECT_FILES.md | 文件清单 |
| QUICK_START.md | 快速参考（本文档） |

## 🔧 基础代码

### 生成语音
```python
from kittentts.onnx_model import KittenTTS_1_Onnx
import json
import soundfile as sf

# 加载模型
config = json.load(open('models/nano/config.json'))
model = KittenTTS_1_Onnx(
    model_path='models/nano/kitten_tts_nano_v0_8.onnx',
    voices_path='models/nano/voices.npz',
    **config
)

# 生成音频
audio = model.generate("Hello, world!", voice="Bella", speed=1.0)

# 保存
sf.write('output.wav', audio, 24000)
```

## 🐛 故障排除

### 问题：虚拟环境不存在
```bash
# 解决：运行部署脚本
./deploy.sh
```

### 问题：模型下载失败
```bash
# 解决：单独下载模型
./deploy.sh models
```

### 问题：Web UI 无法启动
```bash
# 解决：检查端口占用
lsof -i :7860
```

### 问题：模型加载失败
```bash
# 解决：验证模型
python verify_all_models.py
```

## ✅ 部署检查清单

- [ ] Python 3.11.1 已安装
- [ ] UV 已安装（或自动安装）
- [ ] 网络连接正常
- [ ] 至少 500MB 磁盘空间
- [ ] 运行 `./deploy.sh`
- [ ] 验证 `./deploy.sh status`

## 📊 性能参考

### 推理速度（相对）
- nano: ⚡⚡⚡⚡⚡
- nano-int8: ⚡⚡⚡⚡⚡
- micro: ⚡⚡⚡⚡
- mini: ⚡⚡⚡

### 音质（相对）
- nano: ⭐⭐⭐
- nano-int8: ⭐⭐⭐
- micro: ⭐⭐⭐⭐
- mini: ⭐⭐⭐⭐⭐

### 资源占用（相对）
- nano: 🟡 中等
- nano-int8: 🟢 低
- micro: 🟡 中等
- mini: 🔴 高

## 🎯 快速场景

### 场景 1: 快速测试
```bash
./start.sh
# 在浏览器中打开 http://localhost:7860
# 输入文本，点击生成
```

### 场景 2: 批量生成
```python
# 参考 USAGE.md 中的批量生成示例
```

### 场景 3: 高质量输出
```bash
# 使用 mini 模型
# 启动 Web UI，选择 mini 模型
```

### 场景 4: 资源受限
```bash
# 使用 nano-int8 模型
# 启动 Web UI，选择 nano-int8 模型
```

## 📞 获取帮助

1. **查看文档**: `cat README.md`
2. **查看状态**: `./deploy.sh status`
3. **查看帮助**: `./deploy.sh help`
4. **运行测试**: `./deploy.sh test`

## 🎉 开始使用

```bash
# 第一步：部署（仅需一次）
./deploy.sh

# 第二步：启动
./start.sh

# 第三步：使用
# 在浏览器中打开 http://localhost:7860
```

---

**提示**: 将此文件保存到书签或桌面，随时快速参考！

**文档更新**: 2026-03-08
**版本**: v1.0.0
