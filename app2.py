import tkinter as tk
import tkinter.ttk as ttk
import tkinterdnd2 as dnd2
from PIL import Image, ImageTk
import base1
from histo import DrawGraph
import re
import os
import glob
import tkinter.filedialog as filedialog
import histo

def main():
    app = Application()
    app.main()

class Application():
    '''Application class.'''

    def main(self):
        '''Create window and set widgets.'''
        root = dnd2.Tk()
        root.geometry('400x200')
        root.title('Image analysis')
        MainFrame(root)
        root.mainloop()

class MainFrame(ttk.Frame):
    '''Main frame, contains tabs.'''
    def __init__(self, master):
        super().__init__(master)
        # pack self and create tab menu.
        self.pack(expand=True, fill='both')
        self.create_tabs()
        return
        
    def create_tabs(self):
        '''Create tabs.'''
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')
        DrawGraphTab(notebook)

class DrawGraphTab(base1.BaseObserver):
    '''Draw graph tab class. Subscribe analysis process, recieve message and progress.'''
    def __init__(self, master):
        super().__init__()
        self.frame = ttk.Frame(master)
        master.add(self.frame, text='グラフ')
        self.create_widgets()

    def update_message(self, message):
        '''Catch message from DrawGraph class.'''
        self.message = message
        print('catch', self.message)

    def update_process(self, process):
        '''Catch process of DrawGraph class.'''
        pass

    def create_widgets(self):
        '''Create widgets, input area, console area, result area and run button.'''

        # Input area.
        input_frame = ttk.Frame(self.frame, width=100)
        input_frame.pack_propagate(0)
        input_frame.pack(side='left', expand=True, fill='both')
        self.drop_folder_frame = DropFolderFrame(input_frame)

        # Right area frame.
        right_frame = ttk.Frame(self.frame, width=100)
        right_frame.pack_propagate(0)
        right_frame.pack(side='left', expand=True, fill='both')

        # Select mode area.
        style = ttk.Style()
        style.configure('mode.TFrame', background='red')
        select_frame = ttk.Frame(right_frame, height=50, style='mode.TFrame')
        select_frame.pack_propagate(0)
        select_frame.pack(expand=True, fill='both')
        
        # Preproccessing area.
        pre_label = ttk.Label(select_frame, text='前処理')
        pre_label.pack()
        self.pre_var1 = tk.BooleanVar(value=True)
        self.remove_back = ttk.Checkbutton(select_frame, text='背景除去', variable=self.pre_var1)
        self.remove_back.config(state='disabled')
        self.remove_back.pack()

        # Histogram area.
        self.histo_var1 = tk.BooleanVar(value=True)
        remove_back = ttk.Checkbutton(select_frame, text='ヒストグラム', variable=self.histo_var1)
        remove_back.pack()
        histo_frame = ttk.Frame(select_frame)
        histo_frame.pack()
        self.histo_var2 = tk.BooleanVar(value=True)
        remove_back = ttk.Checkbutton(histo_frame, text='BGR', variable=self.histo_var2)
        remove_back.pack(side='left')
        self.histo_var3 = tk.BooleanVar(value=True)
        remove_back = ttk.Checkbutton(histo_frame, text='HSV', variable=self.histo_var3)
        remove_back.pack(side='left')

        # Console area.
        style2 = ttk.Style()
        style2.configure('cons.TFrame', background='blue')
        console_fram = ttk.Frame(right_frame, height=50, style='cons.TFrame')
        console_fram.pack_propagate(0)
        console_fram.pack(expand=True, fill='both')

        button = ttk.Button(self.frame, text='RUN', command=self.run)
        button.pack(side='left')
    rem = True
    def run(self):
        

class DropFolderFrame(ttk.Frame):
    '''Drop folder area.'''

    def __init__(self, master):
        super().__init__(master)
        self.pack_propagate(0)
        self.pack(expand=True, fill='both')
        self.create()
        return

    def create(self):
        '''Create widgets.'''
        self.dir_name = DropPathStringVar()    # Label data, directories name.
        self.files_name = FileNameStringVar()    # Label data, files name.

        # Top label
        top_label = ttk.Label(self, text='フォルダを選択してください')
        top_label.pack()

        # Entry frame, entry textbox and button.
        entry_frame = ttk.Frame(self)
        entry_frame.pack(fill='x')
        # Entry textbox
        entry_textbox = ttk.Entry(entry_frame, textvariable=self.dir_name)
        entry_textbox.pack(side='left', expand=True, fill='x')
        # Entry button
        entry_button = ttk.Button(entry_frame, text='▼', command=self.select_folder)
        entry_button.pack(side='right')

        # Base frame to switch.
        base_frame = ttk.Frame(self)
        base_frame.drop_target_register(dnd2.DND_FILES)
        base_frame.dnd_bind('<<Drop>>', self.drop)
        base_frame.pack_propagate(0)
        base_frame.pack(expand=True, fill='both')
        base_frame.rowconfigure(0, weight=1)    # column, row = 1x1
        base_frame.columnconfigure(0, weight=1)

        # Files list frame.
        self.list_frame = ttk.Frame(base_frame)
        self.list_frame.grid_propagate(0)
        self.list_frame.grid(row=0, column=0, sticky='NSEW')
        # Listbox, show files list.
        self.listbox = tk.Listbox(self.list_frame, selectmode='multiple', listvariable=self.files_name)
        self.listbox.pack(side='left', expand=True, fill='both')
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical', command=self.listbox.yview)
        self.listbox['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side='right', fill='y')

        # Drop folder frame.
        drop_frame = ttk.Frame(base_frame)
        drop_frame.grid_propagate(0)
        drop_frame.grid(row=0, column=0, sticky='NSEW')
        # Drop folder icon.
        self.folder_image = Image.open('./folder.jpg')
        self.folder_image = self.folder_image.resize((100,100))
        self.folder_image = ImageTk.PhotoImage(self.folder_image)
        folder_image_canvas = tk.Canvas(drop_frame, width=100, height=100)
        folder_image_canvas.create_image(51, 51, image=self.folder_image)    # args: center x,y
        folder_image_canvas.pack(expand=True)

    def select_folder(self):
        '''Entry button command. Select folder.'''
        self.dir_name.set(filedialog.askdirectory(), False)
        self.set_list()

    def drop(self, event):
        '''Get path when drop event occur.'''
        self.dir_name.set(event, True)
        self.set_list()

    def set_list(self):
        '''Raise file list frame and set files list to listbox.'''
        self.list_frame.tkraise()
        files = self.dir_name.return_files()
        self.files_name.set(files)

    def return_list(self):
        '''Return files name list and selected index.
        
        Returns
        ----------
        files_name : list
            All files list.
        index : list
            Selectrd index list
        '''
        return self.files_name.files, self.listbox.curselection()

class DropPathStringVar(tk.StringVar):
    '''Get path from dropped, and set stringvar of tkinter.'''
    def __init__(self):
        super().__init__()

    def set(self, event, drop):
        '''Transform event to abspath list.
        
        Parameters
        ----------
        event : event or str
            Droppd event or selected folder path.
        drop : bool
            Whether drop or select.
        '''
        if drop:
            path_list = NameUtil.get_path_from_drop(event)
        else:
            path_list = [event]

        dirs = []
        files = []
        for path in path_list:
            dirs.append(NameUtil.get_dir_name(path))
            files.extend(NameUtil.get_files_list(path))
        dir_name = '/'.join(dirs)
        self.files = files
        super().set(dir_name)

    def return_files(self):
        return self.files

class FileNameStringVar(tk.StringVar):
    '''Get file names from abspath, and set stringvar of tkinter.'''

    def __init__(self):
        super().__init__()
        self.files = []

    def set(self, files, dir_no=None):
        '''Get only file name, and set stringvar.
        
        Parameters
        ----------
        files : list
            List of files names.
        dir_no : int
            directories number.'''
        
        files = list(map(NameUtil.abspath, files))
        
        # If directory is single, show only file names.
        # Directory numbers are multi, show parent directory and file names.
        if dir_no == None:
            dirs = []
            for file in files:
                dirs.append(os.path.dirname(file))
            dir_no = len(set(dirs))
        
        self.files = files
        if dir_no == 1:
            names = list(map(os.path.basename, files))
        elif dir_no > 1:
            names = list(map(NameUtil.get_dir_and_name, files))
        print(names)
        super().set(names)

class NameUtil():
    @staticmethod
    def abspath(path):
        '''Get absolute path for windows, replace \ to /.'''
        return os.path.abspath(path).replace(os.sep,'/')

    @staticmethod
    def get_path_from_drop(event):
        '''Get abspath from dropped file or folder name.
        
        Parameters
        ----------
        event : event
            dnd2 dropped event.

        Returns
        ----------
        list : list
            Absolute file or folder path list.
        '''

        # Extract shortest string between '{' and '}'. 
        pattern = '\{.*?\}'
        dropped = re.findall(pattern, event.data)
        # Delete {} of head and tail.
        return list(map(lambda x: x[1:-1], dropped))

    @staticmethod
    def get_dir_name(path):
        '''Get only directory name.
        
        Parameters
        ----------
        path : str

        Returns
        ----------
        dir_name : str
            Parent directory name.
        '''

        abs_path = os.path.abspath(path).replace(os.sep,'/')
        if os.path.isfile(abs_path):
            return path.split('/')[-2]    # Folder name. (e.g. C:/Users/Taro/Documents/aaa.txt -> Documents)
        else:
            return path.split('/')[-1]

    @staticmethod
    def get_files_list(path):
        '''Get files list in path directory.
        
        Parameters
        ----------
        path : str
            folder path.
        
        Returns
        ----------
        files_list : list
            Files list in arg folder.'''

        abspath = NameUtil.abspath(path)
        if os.path.isfile(abspath):
            return [path]
        else:
            return glob.glob(abspath + '/*')

    @staticmethod
    def get_dir_and_name(path):
        '''Get directory and file name and join.'''
        abspath = NameUtil.abspath(path)
        after_dir = abspath.split('/')[-2:]
        return '/'.join(after_dir)

if __name__ == '__main__':
    main()