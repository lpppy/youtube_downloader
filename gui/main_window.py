import customtkinter as ctk
from tkinter import filedialog
from typing import List
from core.config import QUALITY_OPTIONS, DEFAULT_OUTPUT_DIR, MAX_CONCURRENT_DOWNLOADS
from core.queue_manager import QueueManager, DownloadTask
from core.downloader import VideoDownloader


class DownloadItemFrame(ctk.CTkFrame):
    """Widget for displaying a single download task"""

    def __init__(self, master, task: DownloadTask, **kwargs):
        super().__init__(
            master,
            corner_radius=12,
            fg_color=("#ffffff", "#1e1e1e"),
            border_width=2,
            border_color=("#e0e0e0", "#3a3a3a"),
            **kwargs
        )
        self.task = task

        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        # Title label with icon
        title_text = task.title or task.url[:60] + "..."
        self.title_label = ctk.CTkLabel(
            self,
            text=f"🎬 {title_text}",
            anchor="w",
            font=("", 13, "bold")
        )
        self.title_label.grid(row=0, column=0, sticky="ew", padx=15, pady=(12, 5))

        # Progress bar with better styling
        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=20,
            corner_radius=10,
            progress_color=("#2fa572", "#106a43")
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=15, pady=8)

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="⏳ 等待中...",
            anchor="w",
            font=("", 11),
            text_color="gray"
        )
        self.status_label.grid(row=2, column=0, sticky="ew", padx=15, pady=(5, 12))

    def update_display(self):
        """Update the display based on task status"""
        # Update title if available
        if self.task.title:
            self.title_label.configure(text=f"🎬 {self.task.title}")

        # Update progress
        self.progress_bar.set(self.task.progress / 100)

        # Update status text and colors
        if self.task.status == "pending":
            status_text = "⏳ 等待中..."
            color = "gray"
            progress_color = ("#3b8ed0", "#1f6aa5")
        elif self.task.status == "downloading":
            status_text = f"⬇️ 下载中... {self.task.progress:.1f}%"
            if self.task.speed:
                status_text += f" | 速度: {self.task.speed}"
            if self.task.eta:
                status_text += f" | 剩余: {self.task.eta}"
            color = ("#1f538d", "#3a7ebf")
            progress_color = ("#2fa572", "#106a43")
        elif self.task.status == "completed":
            status_text = "✅ 完成"
            color = ("#2fa572", "#106a43")
            progress_color = ("#2fa572", "#106a43")
        elif self.task.status == "failed":
            status_text = f"❌ 失败: {self.task.error}"
            color = ("#d32f2f", "#b71c1c")
            progress_color = ("#d32f2f", "#b71c1c")
        elif self.task.status == "cancelled":
            status_text = "⏹ 已取消"
            color = ("#ff9800", "#f57c00")
            progress_color = ("#ff9800", "#f57c00")
        else:
            status_text = self.task.status
            color = "gray"
            progress_color = ("#3b8ed0", "#1f6aa5")

        self.status_label.configure(text=status_text, text_color=color)
        self.progress_bar.configure(progress_color=progress_color)


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube 批量下载器 🎬")
        self.geometry("1000x750")

        # Set minimum window size
        self.minsize(800, 600)

        # Initialize variables
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.queue_manager = None

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Create UI
        self._create_header()
        self._create_input_section()
        self._create_control_section()
        self._create_stats_section()
        self._create_download_list()

    def _create_header(self):
        """Create header section with title and description"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎬 YouTube 批量下载器",
            font=("", 28, "bold"),
            text_color=("#1f538d", "#3a7ebf")
        )
        title_label.pack(pady=(0, 5))

        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="支持单个视频、批量下载和播放列表 | 多清晰度选择 | 实时进度显示",
            font=("", 12),
            text_color="gray"
        )
        subtitle_label.pack()

    def _create_input_section(self):
        """Create URL input section"""
        input_frame = ctk.CTkFrame(self, corner_radius=15)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        # Label with icon
        label_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        label_frame.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            label_frame,
            text="📝 输入 YouTube URL",
            font=("", 16, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            label_frame,
            text="  (每行一个链接，支持视频和播放列表)",
            font=("", 11),
            text_color="gray"
        ).pack(side="left")

        # Text box with better styling
        self.url_textbox = ctk.CTkTextbox(
            input_frame,
            height=120,
            corner_radius=10,
            border_width=2,
            border_color=("#d0d0d0", "#404040"),
            font=("", 12)
        )
        self.url_textbox.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="ew")

    def _create_control_section(self):
        """Create control buttons and settings"""
        control_frame = ctk.CTkFrame(self, corner_radius=15)
        control_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Left side - Settings
        settings_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        settings_frame.pack(side="left", padx=15, pady=15, fill="x", expand=True)

        # Quality selection
        quality_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        quality_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            quality_frame,
            text="🎥 清晰度:",
            font=("", 13, "bold")
        ).pack(side="left", padx=(0, 8))

        self.quality_var = ctk.StringVar(value="1080p")
        self.quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            variable=self.quality_var,
            values=list(QUALITY_OPTIONS.keys()),
            width=140,
            height=35,
            corner_radius=8,
            font=("", 12)
        )
        self.quality_menu.pack(side="left")

        # Output directory
        dir_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        dir_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            dir_frame,
            text="📁 保存到:",
            font=("", 13, "bold")
        ).pack(side="left", padx=(0, 8))

        self.dir_label = ctk.CTkLabel(
            dir_frame,
            text=self.output_dir,
            anchor="w",
            font=("", 11),
            text_color="gray"
        )
        self.dir_label.pack(side="left", padx=(0, 8), fill="x", expand=True)

        self.dir_button = ctk.CTkButton(
            dir_frame,
            text="选择目录",
            command=self._select_directory,
            width=100,
            height=35,
            corner_radius=8,
            font=("", 12),
            fg_color=("#3b8ed0", "#1f6aa5"),
            hover_color=("#2d6da3", "#144870")
        )
        self.dir_button.pack(side="left")

        # Right side - Action buttons
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=15, pady=15)

        # Start button
        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶ 开始下载",
            command=self._start_download,
            width=140,
            height=40,
            corner_radius=10,
            font=("", 14, "bold"),
            fg_color=("#2fa572", "#106a43"),
            hover_color=("#26734f", "#0d5434")
        )
        self.start_button.pack(side="left", padx=(0, 10))

        # Stop button
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹ 停止",
            command=self._stop_download,
            width=100,
            height=40,
            corner_radius=10,
            font=("", 14, "bold"),
            fg_color=("#d32f2f", "#b71c1c"),
            hover_color=("#c62828", "#8e0000"),
            state="disabled"
        )
        self.stop_button.pack(side="left")

    def _create_stats_section(self):
        """Create statistics display"""
        stats_frame = ctk.CTkFrame(self, corner_radius=15, fg_color=("#e8f4f8", "#1a3a4a"))
        stats_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="📊 准备就绪 - 请输入 YouTube URL 开始下载",
            font=("", 13),
            text_color=("#1f538d", "#5dade2")
        )
        self.stats_label.pack(padx=20, pady=12)

    def _create_download_list(self):
        """Create scrollable download list"""
        list_frame = ctk.CTkFrame(self, corner_radius=15)
        list_frame.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)

        # Label with icon
        header_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            header_frame,
            text="📥 下载列表",
            font=("", 16, "bold")
        ).pack(side="left")

        # Scrollable frame
        self.download_list = ctk.CTkScrollableFrame(
            list_frame,
            corner_radius=10,
            fg_color=("#f0f0f0", "#2b2b2b")
        )
        self.download_list.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")
        self.download_list.grid_columnconfigure(0, weight=1)

        self.download_widgets = []

        # Empty state message
        self.empty_label = ctk.CTkLabel(
            self.download_list,
            text="暂无下载任务\n\n请在上方输入 YouTube URL 并点击"开始下载"",
            font=("", 13),
            text_color="gray"
        )
        self.empty_label.pack(pady=50)

    def _select_directory(self):
        """Open directory selection dialog"""
        directory = filedialog.askdirectory(initialdir=self.output_dir)
        if directory:
            self.output_dir = directory
            self.dir_label.configure(text=directory)

    def _start_download(self):
        """Start downloading videos"""
        # Get URLs from textbox
        urls_text = self.url_textbox.get("1.0", "end-1c").strip()
        if not urls_text:
            return

        urls = [url.strip() for url in urls_text.split("\n") if url.strip()]

        # Hide empty state message
        if hasattr(self, 'empty_label'):
            self.empty_label.pack_forget()

        # Create queue manager
        quality_format = QUALITY_OPTIONS[self.quality_var.get()]
        self.queue_manager = QueueManager(
            self.output_dir,
            quality_format,
            MAX_CONCURRENT_DOWNLOADS
        )
        self.queue_manager.set_update_callback(self._update_ui)

        # Add tasks
        self.queue_manager.add_tasks(urls)

        # Create widgets for each task
        self.download_widgets.clear()
        for widget in self.download_list.winfo_children():
            widget.destroy()

        for task in self.queue_manager.tasks:
            widget = DownloadItemFrame(self.download_list, task)
            widget.pack(fill="x", padx=8, pady=6)
            self.download_widgets.append(widget)

        # Start downloads
        self.queue_manager.start()

        # Update button states
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.url_textbox.configure(state="disabled")

    def _stop_download(self):
        """Stop all downloads"""
        if self.queue_manager:
            self.queue_manager.stop()

        # Update button states
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.url_textbox.configure(state="normal")

    def _update_ui(self):
        """Update UI with current download status"""
        # Update all download widgets
        for widget in self.download_widgets:
            widget.update_display()

        # Update stats
        if self.queue_manager:
            stats = self.queue_manager.get_stats()

            # Create emoji indicators
            if stats['downloading'] > 0:
                emoji = "⬇️"
            elif stats['completed'] == stats['total'] and stats['total'] > 0:
                emoji = "✅"
            elif stats['failed'] > 0:
                emoji = "⚠️"
            else:
                emoji = "📊"

            stats_text = (
                f"{emoji} 总计: {stats['total']} | "
                f"⏳ 等待: {stats['pending']} | "
                f"⬇️ 下载中: {stats['downloading']} | "
                f"✅ 完成: {stats['completed']} | "
                f"❌ 失败: {stats['failed']}"
            )
            self.stats_label.configure(text=stats_text)

            # Check if all downloads are complete
            if stats['downloading'] == 0 and stats['pending'] == 0:
                self.start_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                self.url_textbox.configure(state="normal")
