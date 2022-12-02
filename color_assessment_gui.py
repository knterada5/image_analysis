import tkinter
import tkinter.messagebox as messagebox
from tkinter import filedialog

import color_assessment

image_folder_path = None
result_folder_path = None

def run():
    global image_folder_path, result_folder_path
    if image_folder_path == None:
        messagebox.showerror('エラー', 'フォルダを選択してください')
    else:
        

def disp():
    def get_image_path():
        global image_folder_path
        image_folder_path = filedialog.askdirectory()
        text_image_path.insert(tkinter.END, image_folder_path)
    
    def get_result_path():
        global result_folder_path
        result_folder_path = filedialog.askdirectory()
        text_result_path.insert(tkinter.END, result_folder_path)

    root = tkinter.Tk()
    root.geometry('300x200')
    root.title('色の散布')

    main_frame = tkinter.Frame(root)
    main_frame.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=10)

    label_select_image = tkinter.Label(main_frame, text='画像を選択')
    label_select_result_folder = tkinter.Label(main_frame, text="保存先")

    text_image_path = tkinter.Entry(main_frame)
    text_result_path = tkinter.Entry(main_frame)

    button_select_image = tkinter.Button(main_frame, text='▼', command=get_image_path)
    button_select_result_folder = tkinter.Button(main_frame, text='▼', command=get_result_path)
    button_run = tkinter.Button(main_frame, text='実行', command=)