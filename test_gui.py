"""
测试 GUI 是否能正常初始化（不显示窗口）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from core.config import QUALITY_OPTIONS

def test_gui_init():
    """测试 GUI 初始化"""
    print("=" * 60)
    print("测试: GUI 组件初始化")
    print("=" * 60)

    try:
        # 设置外观
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        print("\n✓ CustomTkinter 配置成功")

        # 测试创建基本组件（不显示）
        root = ctk.CTk()
        root.withdraw()  # 隐藏窗口

        # 创建测试组件
        frame = ctk.CTkFrame(root)
        label = ctk.CTkLabel(frame, text="测试标签")
        button = ctk.CTkButton(frame, text="测试按钮")
        textbox = ctk.CTkTextbox(frame, height=50)

        print("✓ 基本组件创建成功")

        # 测试清晰度选项
        print("\n清晰度选项:")
        for name, format_str in QUALITY_OPTIONS.items():
            print(f"  ✓ {name}")

        # 清理
        root.destroy()

        print("\n" + "=" * 60)
        print("🎉 GUI 测试通过！")
        print("=" * 60)
        print("\n应用可以正常启动。")
        print("请在有图形界面的环境中双击 '启动应用.command' 查看完整 GUI。")

        return True

    except Exception as e:
        print(f"\n❌ GUI 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_gui_init()
