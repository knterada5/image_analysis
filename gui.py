import tkinter as tk
import tkinter.ttk as ttk
import tkinterdnd2 as dnd2
import test_tab
from PIL import Image, ImageTk

import os

import tkinter.filedialog as filedialog
import glob
import re
import color_histgram

def main():
    root = dnd2.Tk()
    root.geoetry('400x200')
    root.title('Image analysis')
    root.mainloop()

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        self.create_tabs()
        return
    
    def create_tabs(self):
        pass

class HistogramTab(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

    def create_widgets(self):
        pass

    def get_data(self, in_frame, _out_frame):
        pass

    def analyze(self):
        pass

class DropFolderFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

    def create(self):
        pass

    def get_path(self, event):
        pass

    def select_button_click(self):
        pass

    def return_data(self):
        pass

class MyStringVar(tk.StringVar):
    def __init__(self):
        super().__init__()

    def set(self, path):
        super().set()

    def set_params(self, frame=None, file_list=None):
        self.frame = frame
        self.file_list = file_list

    def up_frame(self):
        pass

    def set_list(self, path_list):
        pass

if __name__ == '__main__':
    main()