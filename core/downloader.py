import yt_dlp
import os
from pathlib import Path
from typing import Callable, Optional


class DownloadCancelled(Exception):
    """Raised when a download is cancelled by the user."""
    pass


class VideoDownloader:
    def __init__(self, output_dir: str, quality: str, progress_callback: Optional[Callable] = None):
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.quality = quality
        self.progress_callback = progress_callback
        self._cancelled = False

    def _progress_hook(self, d):
        if self._cancelled:
            raise Exception("Download cancelled")

        if self.progress_callback and d['status'] in ['downloading', 'finished']:
            self.progress_callback(d)

    def download(self, url: str) -> dict:
        """Download a single video or playlist"""
        self._cancelled = False

        ydl_opts = {
            'format': self.quality,
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',  # 合并为 mp4 格式
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return {
                    'success': True,
                    'title': info.get('title', 'Unknown'),
                    'url': url
                }
        except Exception as e:
            error_msg = str(e)

            # 如果是 ffmpeg 错误，尝试使用单一格式下载
            if 'ffmpeg' in error_msg.lower():
                try:
                    ydl_opts['format'] = 'best'  # 使用单一最佳格式（不需要合并）
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        return {
                            'success': True,
                            'title': info.get('title', 'Unknown'),
                            'url': url,
                            'note': '使用单一格式下载（未安装 ffmpeg）'
                        }
                except Exception as e2:
                    error_msg = f"{error_msg}\n备选方案也失败: {str(e2)}"

            return {
                'success': False,
                'error': error_msg,
                'url': url
            }

    def get_video_info(self, url: str) -> dict:
        """Get video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # Check if it's a playlist
                if 'entries' in info:
                    return {
                        'is_playlist': True,
                        'title': info.get('title', 'Unknown Playlist'),
                        'count': len(list(info['entries'])),
                        'urls': [entry['webpage_url'] for entry in info['entries'] if entry]
                    }
                else:
                    return {
                        'is_playlist': False,
                        'title': info.get('title', 'Unknown'),
                        'duration': info.get('duration', 0),
                        'url': url
                    }
        except Exception as e:
            return {
                'error': str(e),
                'url': url
            }

    def cancel(self):
        """Cancel the current download"""
        self._cancelled = True
