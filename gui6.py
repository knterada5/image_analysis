import tkinter as tk
import tkinter.ttk as ttk
import tkinterdnd2 as dnd2
import test_tab
from PIL import Image, ImageTk
import cv2
import os
import copy
import tkinter.filedialog as filedialog

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill=tk.BOTH)
        self.create_tabs()
        return

    def create_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=tk.BOTH)
        HistogramTab(notebook)


class HistogramTab(tk.Frame):
    
    input_path = None
    output_path = None
    img = None
    b = None
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text='ヒストグラム')
        self.create_widgets()
    
    def create_widgets(self):
        # global img
        # def click():
        #     print(frame2.drop_path.get())
        # self.input_path = tk.StringVar()
        # self.output_path = tk.StringVar()
        # s = ttk.Style()
        # s.configure('aaa.TFrame', background='red')
        # s.configure('bbb.TFrame', background='blue')
        # frame1 = ttk.Frame(self, style='aaa.TFrame', width=50)
        # frame1.pack_propagate(0)
        # frame1.pack(expand=True, fill=tk.BOTH, side='left', padx=5, pady=5)
        # # var = tk.StringVar()
        # label = ttk.Label(frame1, text="画像を選択してください")
        # label.pack()
        # frame4 = ttk.Frame(frame1)
        # frame4.pack(fill=tk.X)
        # textbox = ttk.Entry(frame4, textvariable=self.input_path)
        # textbox.pack(fill=tk.X, expand=True, side='left')
        # button = ttk.Button(frame4,text="▼", command=click)
        # button.pack(side='left')
        
        # frame3 = ttk.Frame(frame1, style='bbb.TFrame', name="input_frame")
        # frame3.drop_target_register(dnd2.DND_FILES)
        # frame3.dnd_bind('<<Drop>>', self.dropped_path)
        # frame3.pack_propagate(0)
        # frame3.pack(expand=True, fill='both')
        # self.img = Image.open("./2.webp")
        # self.img = self.img.resize((100,100))
        # self.img = ImageTk.PhotoImage(self.img)
        # canvas = tk.Canvas(frame3,width=100, height=100)
        # canvas.create_image(51,51,image=self.img)
        # canvas.pack(expand=True)    
    
        # frame23 = ttk.Frame(self, style='bbb.TFrame',width=50)
        # frame23.pack_propagate(0)
        # frame23.pack(expand=True, fill=tk.BOTH, side='left')
        # label2 = ttk.Label(frame23, text='b')
        # label2.pack()

        # txt_frame = ttk.Frame(frame23)
        # txt_frame.pack(fill=tk.X)
        # res_textbox = ttk.Entry(txt_frame, textvariable=self.output_path)
        # res_textbox.pack(fill=tk.X, expand=True, side='left')
        # button2 = ttk.Button(txt_frame, text="▼")
        # button2.pack(side='left')

        # fframe = ttk.Frame(frame23, style='aaa.TFrame', name="output_frame")
        # fframe.drop_target_register(dnd2.DND_FILES)
        # fframe.dnd_bind('<<Drop>>', self.dropped_path)
        # fframe.pack_propagate(0)
        # fframe.pack(expand=True, fill='both')

        input_frame = ttk.Frame(self, width=50)
        input_frame.pack_propagate(0)
        input_frame.pack(side='left', expand=True, fill='both')
        frame1 = DropFolderFrame(input_frame)
        # global image1
        # image1 = Image.open("./folder.jpg")
        # image1 = image1.resize((100,100))
        # image1 = ImageTk.PhotoImage(image1)
        # frame1.folder_image.create_image(51,51,image=image1)

        output_frame = ttk.Frame(self, width=50)
        output_frame.pack_propagate(0)
        output_frame.pack(side='left', expand=True, fill='both')
        frame2 = DropFolderFrame(output_frame)
        


        
    def dropped_path(self, event):
        widget = str(event.widget).split('.!')[-1]
        name = widget.split('.')[-1]
        print(event.widget)
        print(widget)
        print(name)
        if name == "input_frame":
            self.input_path.set(event.data[1:-1])
        if name == "output_frame":
            self.output_path.set(event.data[1:-1])

class DropFolderFrame(tk.Frame):

    drop_path = None
    folder_image = None
    image = None

    def __init__(self, master):
        super().__init__(master)
        self.pack_propagate(0)
        self.pack(expand=True, fill='both')
        self.create()
        return

    def create(self):
        self.drop_path = tk.StringVar()

        label = ttk.Label(self, text="フォルダを選択してください")
        label.pack()

        entry_frame = ttk.Frame(self)
        entry_frame.pack(fill=tk.X)
        entry_text = ttk.Entry(entry_frame, textvariable=self.drop_path)
        entry_text.pack(side='left',expand=True, fill=tk.X)
        entry_button = ttk.Button(entry_frame, text="▼", command=self.select_folder)
        entry_button.pack(side='right')

        drop_style = ttk.Style()
        drop_style.configure('drop.TFrame', background='white')
        drop_frame = ttk.Frame(self, style='drop.TFrame', relief=tk.RIDGE, borderwidth=2)
        drop_frame.drop_target_register(dnd2.DND_FILES)
        drop_frame.dnd_bind('<<Drop>>', self.get_path)
        drop_frame.pack_propagate(0)
        drop_frame.pack(expand=True, fill='both')
        self.image = Image.open("./folder.jpg")
        self.image = self.image.resize((100,100))
        self.image = ImageTk.PhotoImage(self.image)
        self.folder_image = tk.Canvas(drop_frame, width=100, height=100)
        self.folder_image.create_image(51,51,image=self.image)
        self.folder_image.pack(expand=True)

    def get_path(self, event):
        self.drop_path.set(event.data[1:-1])
    
    def select_folder(self):
        self.drop_path = filedialog.askdirectory()




def main():
    root = dnd2.Tk()
    root.geometry('300x200')
    root.title('Image analysis')
    Application(root)
    root.mainloop()

if __name__ == '__main__':
    main()