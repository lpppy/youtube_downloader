import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from gui.main_window import MainWindow


def main():
    # Set appearance mode and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create and run the application
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
