# YouTube 批量下载器

基于 yt-dlp 和 CustomTkinter 的现代化 YouTube 视频批量下载工具。

## 功能特性

- ✅ 批量下载多个视频（支持 URL 列表）
- ✅ 播放列表下载支持
- ✅ 多清晰度选择（1080p、720p、480p、最佳质量、仅音频）
- ✅ 实时下载进度显示
- ✅ 并发下载（最多 3 个同时下载）
- ✅ 现代化 GUI 界面
- ✅ 自定义输出目录

## 安装

1. 克隆或下载项目

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行应用：
```bash
python main.py
```

2. 在文本框中输入 YouTube URL（每行一个）

3. 选择视频清晰度

4. 选择保存目录（可选）

5. 点击"开始下载"

## 项目结构

```
youtube_downloader/
├── main.py                 # 应用入口
├── gui/
│   ├── __init__.py
│   └── main_window.py     # 主窗口界面
├── core/
│   ├── __init__.py
│   ├── downloader.py      # yt-dlp 封装
│   ├── queue_manager.py   # 下载队列管理
│   └── config.py          # 配置文件
├── utils/
│   └── __init__.py
└── requirements.txt
```

## 依赖

- yt-dlp: YouTube 视频下载引擎
- customtkinter: 现代化 GUI 框架
- Pillow: 图像处理库

## 系统要求

- Python 3.8+
- macOS / Windows / Linux

## 注意事项

- 下载速度取决于网络连接
- 某些视频可能因版权限制无法下载
- 建议使用稳定的网络连接

## 许可证

MIT License
