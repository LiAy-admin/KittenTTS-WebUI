# KittenTTS-WebUI

基于 KittenTTS 的语音合成 Web 界面，支持 4 种模型、8 种音色。

##  一键安装

```bash
# 克隆项目
git clone https://github.com/LiAy-admin/KittenTTS-WebUI.git
cd KittenTTS-WebUI

# 一键安装
./install.sh

# 启动
./start.sh
```

或者远程一键安装：
```bash
curl -fsSL https://raw.githubusercontent.com/LiAy-admin/KittenTTS-WebUI/main/install.sh | bash
```

然后访问：**http://localhost:7860**

## 📦 模型信息

| 模型 | 参数量 | 大小 | 特点 |
|------|--------|------|------|
| nano | 15M | 55MB | ⚡ 最快 |
| nano-int8 | 15M | 24MB | 📦 最小 |
| micro | 40M | 40MB | ⚖️ 平衡 |
| mini | 80M | 75MB | 🎯 高质量 |

## 🎤 支持音色

Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo

## 🛠️ 手动安装

```bash
# 创建虚拟环境
uv venv --python 3.11.1
source .venv/bin/activate

# 安装依赖
uv pip install -r requirements.txt

# 下载模型（可选，项目已包含模型）
python download_modelscope.py
python download_missing_models.py

# 启动
python web_ui.py
```

## 📁 项目结构

```
KittenTTS-WebUI/
├── install.sh          # 一键安装脚本
├── start.sh            # 启动脚本
├── web_ui.py           # Web UI
├── requirements.txt    # 依赖
├── models/             # 模型文件
│   ├── nano/
│   ├── nano-int8/
│   ├── micro/
│   └── mini/
├── kittentts/          # 核心代码
└── docs/               # 文档
```

## 🔧 环境要求

- Python 3.11+
- UV 包管理器（自动安装）
- 300MB+ 磁盘空间

## � 已知问题与修复

### Gradio 兼容性问题

项目已自动处理 Gradio 库的兼容性问题：

1. **使用稳定版本**：requirements.txt 中使用 Gradio 3.50.2（稳定版本）
2. **自动修复脚本**：`fix_gradio_client.py` 会自动修复 gradio-client 库的已知 bug
3. **集成到安装流程**：install.sh 和 deploy.sh 会在安装依赖后自动运行修复脚本

如果遇到 `TypeError: argument of type 'bool' is not iterable` 错误，可以手动运行：
```bash
python fix_gradio_client.py
```

## �📄 许可证

本项目遵循原 KittenTTS 项目的许可证。
