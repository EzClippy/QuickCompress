import os
import json
import threading
import tkinter.font as tkFont
from tkinter import Label, Button, Entry, filedialog, messagebox, Radiobutton, StringVar, Frame, ttk
from utils.image_processing import process_images_in_directory, resize_and_convert
from constants.constants import MAX_PIXELS_OPTIONS_DICT, SUPPORTED_IMAGE_FORMATS_IMPORT, SUPPORTED_IMAGE_FORMATS_EXPORT
from gui.progress_window import ProgressWindow
from config.config import LANGUAGE_FILE

def load_texts(language_file):
    with open(language_file, 'r', encoding='utf-8') as file:
        return json.load(file)

texts = load_texts(LANGUAGE_FILE)

class ImageConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title(texts["app_title"])

        master.maxsize(550, 320)
        master.resizable(False, False)

        self.frame = Frame(master)
        self.frame.pack(expand=True)

        textFont = tkFont.Font(size=11)
        labelFont = tkFont.Font(size=12)
        inputFont = tkFont.Font(size=14)
        buttonFont = tkFont.Font(size=12)

        self.input_type = StringVar()
        self.input_type.set("directory")

        self.radio_dir = Radiobutton(self.frame, text=texts["input_directory"], variable=self.input_type, value="directory", command=self.toggle_input, font=labelFont, height=2, width=20, indicatoron=0)
        self.radio_dir.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.radio_file = Radiobutton(self.frame, text=texts["input_file"], variable=self.input_type, value="file", command=self.toggle_input, font=labelFont, height=2, width=20, indicatoron=0)
        self.radio_file.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        self.entry_input = Entry(self.frame, font=inputFont)
        self.entry_input.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.button_browse_input = Button(self.frame, text=texts["browse_button"], command=self.browse_input, font=buttonFont)
        self.button_browse_input.grid(row=2, column=2, padx=5, pady=5)

        self.label_output = Label(self.frame, text=texts["output_directory_label"], font=labelFont)
        self.label_output.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.entry_output = Entry(self.frame, font=inputFont)
        self.entry_output.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.button_browse_output = Button(self.frame, text=texts["browse_button"], command=self.browse_output, font=buttonFont)
        self.button_browse_output.grid(row=4, column=2, padx=5, pady=5)

        self.label_size = Label(self.frame, text=texts["select_size"], font=labelFont)
        self.label_size.grid(row=5, column=0, sticky="w", padx=5, pady=5)

        self.MAX_PIXELS_OPTIONS_LABEL = list(MAX_PIXELS_OPTIONS_DICT.keys())
        self.MAX_PIXELS_OPTIONS = list(MAX_PIXELS_OPTIONS_DICT.values())

        self.size_var = StringVar()
        self.size_var.set(self.MAX_PIXELS_OPTIONS_LABEL[0])

        self.dropdown_size = ttk.Combobox(self.frame, textvariable=self.size_var, values=self.MAX_PIXELS_OPTIONS_LABEL, font=labelFont, state='readonly')
        self.dropdown_size.grid(row=5, column=1, padx=5, pady=5)
        self.dropdown_size.bind("<<ComboboxSelected>>", self.on_size_selection_change)

        self.label_format = Label(self.frame, text=texts["select_format"], font=labelFont)
        self.label_format.grid(row=6, column=0, sticky="w", padx=5, pady=5)

        self.format_var = StringVar()
        self.format_var.set(SUPPORTED_IMAGE_FORMATS_EXPORT[0])
        self.dropdown_format = ttk.Combobox(self.frame, textvariable=self.format_var, values=SUPPORTED_IMAGE_FORMATS_EXPORT, font=labelFont, state='readonly')
        self.dropdown_format.grid(row=6, column=1, padx=5, pady=5)

        self.button_compress = Button(self.frame, text=texts["compress_button"], command=self.convert, font=buttonFont)
        self.button_compress.grid(row=7, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        self.cancelled = False

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def toggle_input(self):
        self.entry_input.delete(0, 'end')

    def browse_input(self):
        if self.input_type.get() == "directory":
            path = filedialog.askdirectory()
        else:
            filetypes = [("Image files", ";*".join(SUPPORTED_IMAGE_FORMATS_IMPORT))]
            path = filedialog.askopenfilename(filetypes=filetypes)
        
        self.entry_input.delete(0, 'end')
        self.entry_input.insert(0, path)

    def browse_output(self):
        path = filedialog.askdirectory()
        self.entry_output.delete(0, 'end')
        self.entry_output.insert(0, path)

    def convert(self):
        input_path = self.entry_input.get()
        output_path = self.entry_output.get()
        selected_size_label = self.size_var.get()
        selected_size = MAX_PIXELS_OPTIONS_DICT[selected_size_label]
        selected_format = self.format_var.get()

        if not os.path.exists(input_path):
            messagebox.showerror(texts["error_title"], texts["error_invalid_input"])
            return

        if not output_path or not os.path.exists(output_path):
            messagebox.showerror(texts["error_title"], texts["error_invalid_output"])
            return

        self.cancelled = False
        progress_window = self.show_progress_window()

        self.master.attributes('-disabled', True)

        thread = threading.Thread(target=self.run_conversion, args=(input_path, output_path, progress_window, selected_size, selected_format))
        thread.start()

    def run_conversion(self, input_path, output_path, progress_window, selected_size, selected_format):
        success = False
        if self.input_type.get() == "directory":
            if os.path.isdir(input_path):
                success = process_images_in_directory(input_path, output_path, progress_window, self, selected_size, selected_format)
            else:
                messagebox.showerror(texts["error_title"], texts["error_invalid_input"])
        elif self.input_type.get() == "file":
            if os.path.isfile(input_path):
                success = resize_and_convert(input_path, os.path.join(output_path, os.path.basename(input_path)), selected_size, selected_format)
            else:
                messagebox.showerror(texts["error_title"], texts["error_invalid_input"])

        progress_window.destroy()

        self.master.attributes('-disabled', False)

        if not self.cancelled:
            if success:
                messagebox.showinfo(texts["success_title"], texts["success_compression"])
            else:
                messagebox.showerror(texts["error_title"], texts["error_compression"])

    def show_progress_window(self):
        progress_window = ProgressWindow(self.master, on_cancel=self.cancel_conversion)
        progress_window.title(texts["processing_title"])
        progress_window.geometry("400x100")
        progress_window.resizable(False, False)
        self.center_window(progress_window, 400, 100)

        return progress_window

    def cancel_conversion(self):
        self.cancelled = True
        messagebox.showinfo(texts["cancel_title"], texts["cancel_message"])
        self.master.attributes('-disabled', False)

    def on_size_selection_change(self, event):
        selected_label = self.size_var.get()
        print(f"Selected label: {selected_label}, Corresponding value: {MAX_PIXELS_OPTIONS_DICT[selected_label]}")

    def on_close(self):
        self.master.destroy()