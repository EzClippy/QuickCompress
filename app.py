import os
from tkinter import Tk
from gui.image_converter_gui import ImageConverterGUI
from config.config import ICON_PATH

def main():
    root = Tk()
    root.iconbitmap(ICON_PATH)
    app = ImageConverterGUI(root)
    app.center_window(root, 600, 450)
    root.mainloop()

if __name__ == "__main__":
    main()