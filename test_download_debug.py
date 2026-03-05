"""
带详细日志的下载测试
"""
import sys
import os
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.downloader import VideoDownloader
from core.config import QUALITY_OPTIONS

# 设置日志
log_filename = f"download_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_download_with_logging():
    """测试下载并记录详细日志"""
    logger.info("=" * 60)
    logger.info("开始下载测试")
    logger.info("=" * 60)

    # 测试视频 URL
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

    logger.info(f"测试 URL: {test_url}")
    logger.info(f"清晰度: 480p")
    logger.info(f"保存目录: ./test_downloads")

    def progress_callback(d):
        try:
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)

                if total > 0:
                    percent = (downloaded / total) * 100
                    speed = d.get('_speed_str', 'N/A')
                    eta = d.get('_eta_str', 'N/A')
                    logger.debug(f"进度: {percent:.1f}% | 速度: {speed} | 剩余: {eta}")
                    print(f"\r进度: {percent:.1f}% | 速度: {speed} | 剩余: {eta}", end='', flush=True)

            elif d['status'] == 'finished':
                logger.info("下载完成，正在处理...")
                print("\n✓ 下载完成，正在处理...")

        except Exception as e:
            logger.error(f"进度回调错误: {e}", exc_info=True)

    try:
        downloader = VideoDownloader(
            output_dir="./test_downloads",
            quality=QUALITY_OPTIONS['480p'],
            progress_callback=progress_callback
        )

        logger.info("开始下载...")
        result = downloader.download(test_url)

        if result['success']:
            logger.info("=" * 60)
            logger.info("✓ 下载成功!")
            logger.info(f"视频标题: {result['title']}")
            logger.info(f"保存位置: ./test_downloads/")
            logger.info("=" * 60)
            print(f"\n✓ 下载成功!")
            print(f"视频标题: {result['title']}")
            return True
        else:
            logger.error("=" * 60)
            logger.error("✗ 下载失败")
            logger.error(f"错误信息: {result['error']}")
            logger.error("=" * 60)
            print(f"\n✗ 下载失败")
            print(f"错误信息: {result['error']}")
            return False

    except Exception as e:
        logger.error("=" * 60)
        logger.error("✗ 发生异常")
        logger.error(f"异常信息: {e}", exc_info=True)
        logger.error("=" * 60)
        print(f"\n✗ 发生异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print(f"\n日志文件: {log_filename}\n")
    success = test_download_with_logging()
    print(f"\n详细日志已保存到: {log_filename}")

    if not success:
        print("\n请查看日志文件了解详细错误信息")
