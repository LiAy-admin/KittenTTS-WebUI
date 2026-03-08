# KittenTTS 项目文件清单

## 📦 核心文件

### 部署脚本
- ✅ `deploy.sh` - Bash 一键部署脚本 (6.5 KB)
- ✅ `deploy.py` - Python 一键部署脚本 (8.8 KB)
- ✅ `start.sh` - Bash 快速启动脚本 (400 字节)
- ✅ `start.py` - Python 快速启动脚本 (608 字节)

### 应用脚本
- ✅ `web_ui.py` - Gradio Web UI 界面 (14 KB)
- ✅ `test_local_model.py` - 本地模型测试 (1.1 KB)
- ✅ `example.py` - 示例代码 (1.9 KB)
- ✅ `compare_models.py` - 模型对比 (2.4 KB)

### 工具脚本
- ✅ `check_cuda.py` - CUDA 检测 (2.6 KB)
- ✅ `check_model_paths.py` - 模型路径检查 (4.3 KB)
- ✅ `verify_all_models.py` - 模型验证 (1.2 KB)
- ✅ `download_modelscope.py` - ModelScope 下载 (2.4 KB)
- ✅ `download_missing_models.py` - Hugging Face 下载 (2.8 KB)
- ✅ `download_nano_int8.py` - 单独下载 INT8 模型 (893 字节)

### 配置文件
- ✅ `requirements.txt` - Python 依赖列表 (18 行)
- ✅ `setup.py` - 安装脚本 (1.6 KB)

### 文档文件
- ✅ `README.md` - 项目主文档 (5.0 KB)
- ✅ `USAGE.md` - 使用指南 (5.9 KB)
- ✅ `MODEL_STATUS.md` - 模型状态 (3.1 KB)
- ✅ `DEPLOYMENT.md` - 部署说明
- ✅ `PROJECT_FILES.md` - 文件清单
- ✅ `最佳环境配置方案.md` - 环境配置 (9.4 KB)

### 项目代码
- 📁 `kittentts/` - 核心代码包

### 模型文件
- 📁 `models/` - 模型目录 (4 个模型, 约 200MB)

### 虚拟环境
- 📁 `.venv/` - Python 虚拟环境

## 🎯 快速开始

### 部署
```bash
./deploy.sh  # 或 python deploy.py
```

### 启动
```bash
./start.sh   # 或 python start.py
```

### 状态
```bash
./deploy.sh status
```

## 📚 文档导航

1. **README.md** - 项目说明
2. **DEPLOYMENT.md** - 部署指南
3. **USAGE.md** - 使用示例
4. **MODEL_STATUS.md** - 模型信息
5. **PROJECT_FILES.md** - 文件清单

## ✅ 总结

本项目提供：
- ✅ 14 个实用脚本
- ✅ 6 份详细文档
- ✅ 4 个预训练模型
- ✅ 完整的自动化部署

**立即开始**: `./deploy.sh` 或 `python deploy.py`
