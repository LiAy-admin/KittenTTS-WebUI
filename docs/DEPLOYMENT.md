# KittenTTS 一键部署脚本 - 部署总结

## 📦 创建的部署脚本

### 1. 主要部署脚本

#### `deploy.sh` (Bash 脚本)
- **路径**: `/workspace/deploy.sh`
- **权限**: 可执行 (chmod +x)
- **适用**: Linux/WSL 系统
- **大小**: 6.5 KB
- **功能**: 完整的自动化部署流程

#### `deploy.py` (Python 脚本)
- **路径**: `/workspace/deploy.py`
- **权限**: 可执行 (chmod +x)
- **适用**: 跨平台 (Linux/macOS/Windows)
- **大小**: 8.8 KB
- **功能**: 完整的自动化部署流程

### 2. 快速启动脚本

#### `start.sh` (Bash 脚本)
- **路径**: `/workspace/start.sh`
- **权限**: 可执行 (chmod +x)
- **适用**: Linux/WSL 系统
- **大小**: 400 字节
- **功能**: 快速启动 Web UI

#### `start.py` (Python 脚本)
- **路径**: `/workspace/start.py`
- **权限**: 可执行 (chmod +x)
- **适用**: 跨平台
- **大小**: 608 字节
- **功能**: 快速启动 Web UI

## 🎯 脚本功能

### 自动化部署流程

部署脚本会自动执行以下步骤：

1. ✅ **环境检查**
   - 检查 UV 是否安装（未安装则自动安装）
   - 检查 Python 版本（要求 3.11.1）

2. ✅ **虚拟环境创建**
   - 使用 UV 创建 Python 3.11.1 虚拟环境
   - 自动检测已存在的虚拟环境

3. ✅ **依赖安装**
   - 自动安装 `requirements.txt` 中的所有依赖
   - 支持 UV 的高效包管理

4. ✅ **模型下载**
   - 从 ModelScope 下载 nano 和 nano-int8 模型
   - 从 Hugging Face 下载 micro 和 mini 模型
   - 自动创建符号链接

5. ✅ **模型验证**
   - 验证所有模型文件完整性
   - 测试模型加载功能

6. ✅ **服务启动**
   - 启动 Web UI 界面
   - 自动查找可用端口

## 📝 使用方法

### 首次部署（完整安装）

**Bash 版本:**
```bash
./deploy.sh
```

**Python 版本:**
```bash
python deploy.py
```

### 日常使用（快速启动）

**Bash 版本:**
```bash
./start.sh
```

**Python 版本:**
```bash
python start.py
```

### 其他命令

**Bash 版本:**
```bash
./deploy.sh status    # 查看状态
./deploy.sh test      # 运行测试
./deploy.sh models    # 下载模型
./deploy.sh webui     # 启动 Web UI
./deploy.sh help      # 查看帮助
```

**Python 版本:**
```bash
python deploy.py status    # 查看状态
python deploy.py test      # 运行测试
python deploy.py models    # 下载模型
python deploy.py webui     # 启动 Web UI
python deploy.py help      # 查看帮助
```

## 📚 配套文档

### 1. README.md
- **路径**: `/workspace/README.md`
- **内容**: 完整的部署和使用指南
- **包含**: 快速开始、使用方法、故障排除等

### 2. USAGE.md
- **路径**: `/workspace/USAGE.md`
- **内容**: 详细的使用示例和代码
- **包含**: 基础示例、批量生成、性能参考等

### 3. MODEL_STATUS.md
- **路径**: `/workspace/MODEL_STATUS.md`
- **内容**: 模型下载状态报告
- **包含**: 模型信息、验证结果、使用建议等

### 4. DEPLOYMENT.md (本文档)
- **路径**: `/workspace/DEPLOYMENT.md`
- **内容**: 部署脚本总结和说明

## 🎨 特色功能

### 1. 彩色输出
- 使用 ANSI 颜色代码提供清晰的视觉反馈
- 成功（绿色）、信息（蓝色）、警告（黄色）、错误（红色）

### 2. 错误处理
- 完善的错误检查和异常处理
- 友好的错误提示信息

### 3. 进度显示
- 实时显示部署进度
- 清晰的步骤提示

### 4. 智能检测
- 自动检测已安装的组件
- 避免重复操作

### 5. 跨平台支持
- Bash 脚本支持 Linux/WSL
- Python 脚本支持所有平台

## 🔍 脚本验证

### 已验证功能

```bash
# 状态检查
python deploy.py status

# 结果:
# [SUCCESS] 虚拟环境: 存在
# [SUCCESS] 模型 nano: 存在
# [SUCCESS] 模型 nano-int8: 存在
# [SUCCESS] 模型 micro: 存在
# [SUCCESS] 模型 mini: 存在
# [SUCCESS] 依赖: 已安装
```

```bash
# 模型验证
python verify_all_models.py

# 结果:
# ✓ nano: 加载成功, 8 个音色
# ✓ nano-int8: 加载成功, 8 个音色
# ✓ micro: 加载成功, 8 个音色
# ✓ mini: 加载成功, 8 个音色
```

## 📊 部署时间参考

| 步骤 | 预计时间 | 说明 |
|------|---------|------|
| 检查环境 | ~10秒 | 检查 UV 和 Python |
| 创建虚拟环境 | ~30秒 | UV 创建 .venv |
| 安装依赖 | ~2-3分钟 | 安装所有 Python 包 |
| 下载模型 | ~5-10分钟 | 下载 4 个模型（约 200MB） |
| 验证模型 | ~30秒 | 加载所有模型验证 |
| **总计** | **~8-15分钟** | 首次完整部署 |

## 💡 使用建议

### 新用户
1. 使用 `./deploy.sh` 或 `python deploy.py` 进行完整部署
2. 部署完成后使用 `./start.sh` 或 `python start.py` 日常启动
3. 查看 `USAGE.md` 了解详细使用方法

### 开发者
1. 参考脚本代码进行定制化
2. 使用 `deploy.sh models` 单独下载模型
3. 使用 `deploy.sh test` 验证功能

### 运维人员
1. 使用 `deploy.sh status` 监控系统状态
2. 定期运行模型验证确保正常运行
3. 根据需求选择合适的模型

## 🚀 快速开始三步走

### 第一步：部署
```bash
./deploy.sh
```

### 第二步：验证
```bash
./deploy.sh status
```

### 第三步：启动
```bash
./start.sh
```

然后访问: `http://localhost:7860`

## 📞 技术支持

遇到问题？
1. 查看 `README.md` 的故障排除章节
2. 运行 `./deploy.sh status` 检查状态
3. 查看 `MODEL_STATUS.md` 了解模型状态

## 🎉 总结

**KittenTTS 一键部署脚本提供了：**

- ✅ 完全自动化的部署流程
- ✅ 跨平台支持（Bash + Python）
- ✅ 智能环境检测
- ✅ 自动模型下载
- ✅ 友好的用户界面
- ✅ 完善的错误处理
- ✅ 详细的文档说明

**现在你只需要一条命令就能完成整个项目的部署！**

---

**立即开始**: `./deploy.sh` 或 `python deploy.py`

祝你使用愉快！🎊
