import threading
import queue
from typing import Callable, List
from .downloader import VideoDownloader


class DownloadTask:
    def __init__(self, url: str, title: str = ""):
        self.url = url
        self.title = title
        self.status = "pending"  # pending, downloading, completed, failed, cancelled
        self.progress = 0.0
        self.speed = ""
        self.eta = ""
        self.error = ""


class QueueManager:
    def __init__(self, output_dir: str, quality: str, max_workers: int = 3):
        self.output_dir = output_dir
        self.quality = quality
        self.max_workers = max_workers
        self.task_queue = queue.Queue()
        self.tasks: List[DownloadTask] = []
        self.active_downloads = {}
        self.running = False
        self.workers = []
        self.update_callback: Callable = None

    def set_update_callback(self, callback: Callable):
        """Set callback for task updates"""
        self.update_callback = callback

    def add_task(self, url: str, title: str = ""):
        """Add a download task to the queue"""
        task = DownloadTask(url, title)
        self.tasks.append(task)
        self.task_queue.put(task)
        if self.update_callback:
            self.update_callback()
        return task

    def add_tasks(self, urls: List[str]):
        """Add multiple download tasks"""
        for url in urls:
            self.add_task(url.strip())

    def start(self):
        """Start processing the download queue"""
        if self.running:
            return

        self.running = True
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)

    def stop(self):
        """Stop all downloads"""
        self.running = False

        # Cancel active downloads
        for downloader in self.active_downloads.values():
            downloader.cancel()

        # Clear queue
        while not self.task_queue.empty():
            try:
                task = self.task_queue.get_nowait()
                if task.status == "pending":
                    task.status = "cancelled"
            except queue.Empty:
                break

        if self.update_callback:
            self.update_callback()

    def _worker(self):
        """Worker thread for processing downloads"""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
            except queue.Empty:
                continue

            if not self.running:
                break

            task.status = "downloading"
            if self.update_callback:
                self.update_callback()

            def progress_callback(d):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    downloaded = d.get('downloaded_bytes', 0)

                    if total > 0:
                        task.progress = (downloaded / total) * 100

                    task.speed = d.get('_speed_str', '')
                    task.eta = d.get('_eta_str', '')

                    if self.update_callback:
                        self.update_callback()

                elif d['status'] == 'finished':
                    task.progress = 100
                    if self.update_callback:
                        self.update_callback()

            downloader = VideoDownloader(self.output_dir, self.quality, progress_callback)
            self.active_downloads[task.url] = downloader

            result = downloader.download(task.url)

            if result['success']:
                task.status = "completed"
                task.progress = 100
                if not task.title:
                    task.title = result['title']
            else:
                task.status = "failed"
                task.error = result['error']

            del self.active_downloads[task.url]

            if self.update_callback:
                self.update_callback()

            self.task_queue.task_done()

    def get_stats(self):
        """Get download statistics"""
        pending = sum(1 for t in self.tasks if t.status == "pending")
        downloading = sum(1 for t in self.tasks if t.status == "downloading")
        completed = sum(1 for t in self.tasks if t.status == "completed")
        failed = sum(1 for t in self.tasks if t.status == "failed")

        return {
            'total': len(self.tasks),
            'pending': pending,
            'downloading': downloading,
            'completed': completed,
            'failed': failed
        }
