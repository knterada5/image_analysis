import os
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import tkinterdnd2
from tkinterdnd2 import *
from tkinter import *



def disp():
    root = tkinterdnd2.Tk()
    root.title("Image analysis Top")
    root.geometry('300x200')

    notebook = ttk.Notebook(root)

    tab_1 = tk.Frame(notebook)

    notebook.add(tab_1, text="Color histgram")
    var = tk.StringVar()
    def drop(event):
        var.set(event.data)
        print('drop')
    data_path_type = ('ファイル', 'フォルダ')
    combobox = ttk.Combobox(tab_1, values=data_path_type, state='readonly')
    combobox.current(0)
    label_image_path = ttk.Label(tab_1, text="ラベルだよ")

    entry = Entry(root, textvariable=var)
    entry.drop_target_register(DND_FILES)
    entry.dnd_bind('<<Drop>>', drop)
    entry.grid(column=2, row=1)
    
    notebook.grid(column=0, row=0)
    combobox.grid(column=0, row=0)
    label_image_path.grid(column=1, row=0)
    
    

    root.mainloop()

    





if __name__ == '__main__':
    disp()