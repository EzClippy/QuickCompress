import json
from tkinter import Label, ttk, Toplevel
from config.config import LANGUAGE_FILE
from config.config import ICON_PATH

def load_texts(language_file):
    with open(language_file, 'r', encoding='utf-8') as file:
        return json.load(file)

texts = load_texts(LANGUAGE_FILE)

class ProgressWindow(Toplevel):
    def __init__(self, master=None, on_cancel=None, **kwargs):
        super().__init__(master, **kwargs)
        self.iconbitmap(ICON_PATH)
        self.label = Label(self, text=texts["processing_message"])
        self.label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self, mode="determinate")
        self.progress_bar.pack(expand=True, fill="both", padx=20, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.on_cancel = on_cancel

    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.update_idletasks()

    def on_cancel(self):
        if self.on_cancel:
            self.on_cancel()
        self.destroy()