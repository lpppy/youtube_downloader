"""
自动化测试 YouTube 下载器核心功能（无需用户输入）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.downloader import VideoDownloader
from core.config import QUALITY_OPTIONS


def test_video_info():
    """测试获取视频信息"""
    print("=" * 60)
    print("测试 1: 获取视频信息")
    print("=" * 60)

    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

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


def test_playlist_info():
    """测试获取播放列表信息"""
    print("\n" + "=" * 60)
    print("测试 2: 获取播放列表信息")
    print("=" * 60)

    # 使用一个小型公开播放列表
    test_url = "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"

    downloader = VideoDownloader(
        output_dir="./test_downloads",
        quality=QUALITY_OPTIONS['720p']
    )

    print(f"\n正在获取播放列表信息: {test_url}")
    info = downloader.get_video_info(test_url)

    if 'error' in info:
        print(f"❌ 错误: {info['error']}")
        return False

    print(f"\n✓ 播放列表标题: {info.get('title', 'Unknown')}")
    print(f"✓ 是否为播放列表: {info.get('is_playlist', False)}")
    if info.get('is_playlist'):
        print(f"✓ 视频数量: {info.get('count', 0)}")

    return True


def test_quality_options():
    """测试清晰度选项"""
    print("\n" + "=" * 60)
    print("测试 3: 清晰度选项")
    print("=" * 60)

    print("\n可用的清晰度选项:")
    for name, format_str in QUALITY_OPTIONS.items():
        print(f"  ✓ {name}: {format_str}")

    return True


def main():
    print("\n" + "=" * 60)
    print("YouTube 下载器 - 自动化测试")
    print("=" * 60)

    os.makedirs("./test_downloads", exist_ok=True)

    results = []

    try:
        results.append(("获取视频信息", test_video_info()))
        results.append(("获取播放列表信息", test_playlist_info()))
        results.append(("清晰度选项", test_quality_options()))

    except KeyboardInterrupt:
        print("\n\n测试被用户中断。")
    except Exception as e:
        print(f"\n\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")

    print(f"\n总计: {passed}/{total} 测试通过")
    print("=" * 60)

    if passed == total:
        print("\n🎉 所有测试通过！核心功能正常工作。")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败。")

    print("\n注意: 此测试仅验证信息获取功能，未进行实际下载。")
    print("要测试完整下载功能，请运行 GUI 应用: python main.py")


if __name__ == "__main__":
    main()
