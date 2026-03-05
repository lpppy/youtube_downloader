"""
测试 YouTube 下载器核心功能
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.downloader import VideoDownloader
from core.config import QUALITY_OPTIONS


def test_video_info():
    """测试获取视频信息"""
    print("=" * 60)
    print("测试 1: 获取视频信息")
    print("=" * 60)

    # 使用一个公开的测试视频
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - 第一个 YouTube 视频

    downloader = VideoDownloader(
        output_dir="./test_downloads",
        quality=QUALITY_OPTIONS['720p']
    )

    print(f"\n正在获取视频信息: {test_url}")
    info = downloader.get_video_info(test_url)

    if 'error' in info:
        print(f"❌ 错误: {info['error']}")
        return False

    print(f"\n✓ 视频标题: {info.get('title', 'Unknown')}")
    print(f"✓ 是否为播放列表: {info.get('is_playlist', False)}")
    if not info.get('is_playlist'):
        duration = info.get('duration', 0)
        print(f"✓ 视频时长: {duration} 秒 ({duration // 60}:{duration % 60:02d})")

    return True


def test_download():
    """测试下载功能"""
    print("\n" + "=" * 60)
    print("测试 2: 下载视频")
    print("=" * 60)

    # 使用一个很短的测试视频
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

    def progress_callback(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)

            if total > 0:
                percent = (downloaded / total) * 100
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                print(f"\r下载进度: {percent:.1f}% | 速度: {speed} | 剩余: {eta}", end='', flush=True)

        elif d['status'] == 'finished':
            print("\n✓ 下载完成，正在处理...")

    downloader = VideoDownloader(
        output_dir="./test_downloads",
        quality=QUALITY_OPTIONS['480p'],  # 使用较低清晰度以加快测试
        progress_callback=progress_callback
    )

    print(f"\n开始下载: {test_url}")
    print("(使用 480p 清晰度进行测试)\n")

    result = downloader.download(test_url)

    if result['success']:
        print(f"\n✓ 下载成功!")
        print(f"✓ 视频标题: {result['title']}")
        print(f"✓ 保存位置: ./test_downloads/")
        return True
    else:
        print(f"\n❌ 下载失败: {result['error']}")
        return False


def test_queue_manager():
    """测试队列管理器"""
    print("\n" + "=" * 60)
    print("测试 3: 队列管理器")
    print("=" * 60)

    from core.queue_manager import QueueManager
    import time

    # 创建队列管理器
    queue_manager = QueueManager(
        output_dir="./test_downloads",
        quality=QUALITY_OPTIONS['480p'],
        max_workers=2
    )

    # 添加测试任务（使用相同的短视频）
    test_urls = [
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",
    ]

    print(f"\n添加 {len(test_urls)} 个下载任务...")
    queue_manager.add_tasks(test_urls)

    # 设置更新回调
    def update_callback():
        stats = queue_manager.get_stats()
        print(f"\r状态 - 总计:{stats['total']} | 等待:{stats['pending']} | "
              f"下载中:{stats['downloading']} | 完成:{stats['completed']} | "
              f"失败:{stats['failed']}", end='', flush=True)

    queue_manager.set_update_callback(update_callback)

    # 启动下载
    print("启动队列管理器...\n")
    queue_manager.start()

    # 等待完成
    while True:
        stats = queue_manager.get_stats()
        if stats['downloading'] == 0 and stats['pending'] == 0:
            break
        time.sleep(1)

    print("\n\n✓ 队列管理器测试完成!")

    final_stats = queue_manager.get_stats()
    print(f"\n最终统计:")
    print(f"  - 总任务数: {final_stats['total']}")
    print(f"  - 成功: {final_stats['completed']}")
    print(f"  - 失败: {final_stats['failed']}")

    return final_stats['completed'] > 0


def main():
    print("\n" + "=" * 60)
    print("YouTube 下载器 - 功能测试")
    print("=" * 60)

    # 创建测试目录
    os.makedirs("./test_downloads", exist_ok=True)

    results = []

    # 运行测试
    try:
        results.append(("获取视频信息", test_video_info()))

        # 询问是否继续下载测试
        print("\n" + "-" * 60)
        response = input("\n是否继续进行下载测试？这将下载一个短视频 (y/n): ").strip().lower()

        if response == 'y':
            results.append(("下载视频", test_download()))
            results.append(("队列管理器", test_queue_manager()))
        else:
            print("\n跳过下载测试。")

    except KeyboardInterrupt:
        print("\n\n测试被用户中断。")
    except Exception as e:
        print(f"\n\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

    # 显示测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")

    print("\n" + "=" * 60)

    # 清理提示
    print("\n提示: 测试文件保存在 ./test_downloads/ 目录中")
    print("可以手动删除该目录以清理测试文件。")


if __name__ == "__main__":
    main()
