# YouTube 批量下载器

<div align="center">

基于 yt-dlp 和 CustomTkinter 的现代化 YouTube 视频批量下载工具。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)

</div>

---

## ✨ 功能特性

- 📥 **批量下载** - 支持多个 URL 同时下载
- 📋 **播放列表支持** - 一键下载整个播放列表
- 🎬 **多清晰度** - 1080p / 720p / 480p / 最佳质量 / 仅音频
- 📊 **实时进度** - 可视化下载进度显示
- ⚡ **并发下载** - 最多 3 个任务同时进行
- 🎨 **现代界面** - 基于 CustomTkinter 的美观 GUI
- 📁 **自定义目录** - 自由选择保存位置

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/lpppy/youtube_downloader.git
cd youtube_downloader
```

### 2. 安装依赖

<details>
<summary><b>🖥️ Windows</b></summary>

```bash
# 方式一：使用 pip
pip install -r requirements.txt

# 方式二：如果 pip 不可用
python -m pip install -r requirements.txt
```

> 💡 提示：如果提示找不到 `pip`，请确保已安装 Python 并添加到环境变量

</details>

<details>
<summary><b>🍎 macOS / 🐧 Linux</b></summary>

```bash
# 方式一：使用 pip3
pip3 install -r requirements.txt

# 方式二：使用 Homebrew (macOS)
brew install python
pip3 install -r requirements.txt

# 方式三：使用系统 Python
python3 -m pip install -r requirements.txt
```

</details>

---

### 3. 运行应用

<details>
<summary><b>🖥️ Windows</b></summary>

#### 方式一：双击启动（推荐）

直接双击 `启动应用.bat` 文件即可运行

#### 方式二：命令行启动

```bash
# 在文件夹空白处按住 Shift + 右键，选择"在此处打开 PowerShell 窗口"
python main.py

# 或者
start 启动应用.bat
```

</details>

<details>
<summary><b>🍎 macOS / 🐧 Linux</b></summary>

#### 方式一：使用启动脚本（推荐）

```bash
# macOS
./启动应用.command

# Linux
./start.sh
```

#### 方式二：命令行启动

```bash
python3 main.py
```

> 💡 如果提示权限不足，先执行：`chmod +x start.sh` 或 `chmod +x 启动应用.command`

</details>

---

### 4. 使用步骤

1. 在文本框中输入 YouTube URL（每行一个）
2. 选择视频清晰度
3. 选择保存目录（可选）
4. 点击「开始下载」

---

## 📂 项目结构

```
youtube_downloader/
├── main.py                 # 应用入口
├── gui/
│   ├── __init__.py
│   └── main_window.py      # 主窗口界面
├── core/
│   ├── __init__.py
│   ├── downloader.py       # yt-dlp 封装
│   ├── queue_manager.py    # 下载队列管理
│   └── config.py           # 配置文件
├── utils/
│   └── __init__.py
├── start.sh                # Linux 启动脚本
├── 启动应用.bat            # Windows 启动脚本
├── 启动应用.command        # macOS 启动脚本
└── requirements.txt        # 依赖列表
```

---

## 📦 依赖

| 依赖包 | 说明 |
|--------|------|
| yt-dlp | YouTube 视频下载引擎 |
| customtkinter | 现代化 GUI 框架 |
| Pillow | 图像处理库 |

---

## 🖼️ 界面预览

![主界面](screenshots/应用截图.png)

---

## 💡 使用提示

- 下载速度取决于网络连接质量
- 某些视频可能因版权限制无法下载
- 建议使用稳定的网络连接
- 播放列表下载可能需要较长时间

---

## 📝 License

MIT License

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star**

</div>
