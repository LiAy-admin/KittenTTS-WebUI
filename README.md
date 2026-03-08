# KittenTTS 一键部署指南

## 🚀 快速开始

KittenTTS 提供了两个一键部署脚本，支持自动化环境配置和模型下载：

- `deploy.sh` - Bash 脚本（推荐用于 Linux/WSL）
- `deploy.py` - Python 脚本（跨平台）

## 📋 使用方法

### Bash 脚本 (Linux/WSL)

```bash
# 赋予执行权限
chmod +x deploy.sh

# 完整部署（首次使用）
./deploy.sh

# 仅启动 Web UI
./deploy.sh webui

# 查看状态
./deploy.sh status

# 运行测试
./deploy.sh test

# 下载模型
./deploy.sh models

# 查看帮助
./deploy.sh help
```

### Python 脚本（跨平台）

```bash
# 完整部署（首次使用）
python deploy.py

# 仅启动 Web UI
python deploy.py webui

# 查看状态
python deploy.py status

# 运行测试
python deploy.py test

# 下载模型
python deploy.py models

# 查看帮助
python deploy.py help
```

## 🎯 部署流程

部署脚本会自动执行以下步骤：

1. **检查环境**
   - 检查 UV 是否安装（如未安装则自动安装）
   - 检查 Python 版本

2. **创建虚拟环境**
   - 使用 UV 创建 Python 3.11.1 虚拟环境

3. **安装依赖**
   - 自动安装 `requirements.txt` 中的所有依赖

4. **下载模型**
   - 从 ModelScope 下载 nano 和 nano-int8 模型
   - 从 Hugging Face 下载 micro 和 mini 模型
   - 自动创建符号链接

5. **验证模型**
   - 验证所有模型是否正确下载和配置

6. **启动服务**
   - 启动 Web UI 界面

## 📦 模型信息

| 模型 | 参数量 | 大小 | 特点 | 下载源 |
|------|--------|------|------|--------|
| nano | 15M | 56MB | ⚡ 最快 | ModelScope |
| nano-int8 | 15M | 25MB | 📦 最小体积 | ModelScope |
| micro | 40M | 41MB | ⚖️ 平衡 | Hugging Face |
| mini | 80M | 80MB | 🎯 最高质量 | Hugging Face |

## 🎤 可用音色

所有模型都支持以下 8 个音色：
- Bella (女声, 温柔)
- Jasper (男声, 深沉)
- Luna (女声, 活泼)
- Bruno (男声, 稳重)
- Rosie (女声, 甜美)
- Hugo (男声, 友好)
- Kiki (女声, 可爱)
- Leo (男声, 清晰)

## 🌐 Web UI 使用

启动 Web UI 后：

1. 打开浏览器访问: `http://localhost:7860`
2. 在输入框中输入要转换的文本
3. 选择模型（nano/nano-int8/micro/mini）
4. 选择音色
5. 调整语速（0.5 - 2.0）
6. 点击"生成音频"按钮

## 💻 命令行使用

除了 Web UI，还可以直接使用其他脚本：

```bash
# 测试本地模型
python test_local_model.py

# 运行示例代码
python example.py

# 对比所有模型
python compare_models.py
```

## 🔧 环境要求

- **操作系统**: Linux / macOS / Windows (WSL)
- **Python**: 3.11.1
- **UV**: 最新版本（脚本会自动安装）
- **磁盘空间**: 至少 300MB（用于存储模型）

## 📁 项目结构

```
workspace/
├── deploy.sh              # Bash 部署脚本
├── deploy.py              # Python 部署脚本
├── requirements.txt       # Python 依赖
├── web_ui.py              # Web UI 界面
├── test_local_model.py    # 本地模型测试
├── example.py             # 示例代码
├── compare_models.py      # 模型对比
├── download_modelscope.py # ModelScope 下载脚本
├── download_missing_models.py  # Hugging Face 下载脚本
├── verify_all_models.py   # 模型验证脚本
├── .venv/                 # 虚拟环境
└── models/                # 模型目录
    ├── nano/              # Nano 模型
    ├── nano-int8/         # Nano INT8 模型
    ├── micro/             # Micro 模型
    └── mini/              # Mini 模型
```

## 🐛 故障排除

### 问题：UV 安装失败

**解决方案：**
```bash
# 手动安装 UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

### 问题：模型下载失败

**解决方案：**
```bash
# 检查网络连接
# 单独下载模型
python deploy.py models
```

### 问题：Web UI 无法启动

**解决方案：**
```bash
# 检查端口是否被占用
lsof -i :7860

# 使用不同端口启动
python web_ui.py --port 7861
```

### 问题：模型加载失败

**解决方案：**
```bash
# 验证模型文件
python verify_all_models.py

# 检查模型路径
ls -la models/
```

## 📊 性能建议

1. **实时应用**: 使用 `nano` 模型
2. **资源受限**: 使用 `nano-int8` 模型
3. **大多数场景**: 使用 `micro` 模型
4. **高质量需求**: 使用 `mini` 模型

## 🔗 相关链接

- [GitHub 仓库](https://github.com/KittenML/KittenTTS)
- [Hugging Face](https://huggingface.co/KittenML)
- [ModelScope](https://www.modelscope.cn/KittenML)
- [在线 Demo](https://huggingface.co/spaces/KittenML/KittenTTS-Demo)

## 📝 更新日志

### v1.0.0
- ✅ 一键部署脚本
- ✅ 自动环境配置
- ✅ 自动模型下载
- ✅ Web UI 界面
- ✅ 支持 4 个模型
- ✅ 支持 8 个音色

## 📄 许可证

本项目遵循原 KittenTTS 项目的许可证。

---

**快速开始**: `./deploy.sh` 或 `python deploy.py`

祝你使用愉快！🎉
