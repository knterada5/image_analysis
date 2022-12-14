import tkinter as tk
import tkinter.ttk as ttk
import tkinterdnd2 as dnd2
from PIL import Image, ImageTk
import base
from histo import DrawGraph
import re
import os
import glob
import tkinter.filedialog as filedialog
import histo
import tkinter.font as font
import time
import threading

def main():
    app = Application()
    app.main()

class Application():
    '''Application class.'''

    def main(self):
        '''Create window and set widgets.'''
        root = dnd2.Tk()
        root.geometry('500x500')
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

class DrawGraphTab(base.BaseObserver):
    '''Draw graph tab class. Subscribe analysis process, recieve message and progress.'''
    def __init__(self, master):
        super().__init__()
        self.frame = ttk.Frame(master)
        master.add(self.frame, text='グラフ')
        self.create_widgets()

    def update_message(self, message):
        '''Catch message from DrawGraph class.'''
        # self.message = message
        print('update messgae')
        self.var.set_message(message)

    def update_process(self, process):
        '''Catch process of DrawGraph class.'''
        print('update progress')
        self.var.set_progress(process)

    def create_widgets(self):
        '''Create widgets, input area, console area, result area and run button.'''

        # Font
        f = font.Font(self.frame, family='MS gothic', size=10)
        s = ttk.Style()
        s.configure('font.TCheckbutton', font=f)
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
        pre_proc_frame = ttk.LabelFrame(select_frame, text='\033[33m前処理')
        pre_proc_frame.pack(fill='x', pady=(0,5))
        self.pre_var1 = tk.BooleanVar(value=True)
        self.remove_back = ttk.Checkbutton(pre_proc_frame, text='背景除去abcd', variable=self.pre_var1,style='font.TCheckbutton')
        self.remove_back.pack(fill='x')

        # Graph area.
        graph_frame = ttk.LabelFrame(select_frame, text='グラフ')
        graph_frame.pack(fill='x')
        # Histogram area.
        self.histo_var1 = tk.BooleanVar(value=True)
        self.histo_btn1 = ttk.Checkbutton(graph_frame, text='ヒストグラム', variable=self.histo_var1, command=lambda : self.disable_all('histo'),style='font.TCheckbutton')
        self.histo_btn1.pack(fill='x')
        histo_frame = ttk.Frame(graph_frame)
        histo_frame.pack(fill='x', pady=(0,10))
        self.histo_var2 = tk.BooleanVar(value=True)
        self.histo_btn2 = ttk.Checkbutton(histo_frame, text='BGR', variable=self.histo_var2, command=lambda:self.both_off('histo'),style='font.TCheckbutton')
        self.histo_btn2.pack(side='left',padx=10)
        self.histo_var3 = tk.BooleanVar(value=True)
        self.histo_btn3 = ttk.Checkbutton(histo_frame, text='HSV', variable=self.histo_var3, command=lambda:self.both_off('histo'),style='font.TCheckbutton')
        self.histo_btn3.pack(side='left', padx=10)
    
        # Scatter 3D area.
        self.scat_var1 = tk.BooleanVar(value=True)
        self.scat_btn1 = ttk.Checkbutton(graph_frame, text='3D散布図', variable=self.scat_var1, command=lambda : self.disable_all('scat'))
        self.scat_btn1.pack(fill='x')
        scat_frame = ttk.Frame(graph_frame)
        scat_frame.pack(fill='x')
        self.scat_var2 = tk.BooleanVar(value=True)
        self.scat_btn2 = ttk.Checkbutton(scat_frame, text='BGR', variable=self.scat_var2, command=lambda:self.both_off('scat'))
        self.scat_btn2.pack(side='left',padx=10)
        self.scat_var3 = tk.BooleanVar(value=True)
        self.scat_btn3 = ttk.Checkbutton(scat_frame, text='HSV', variable=self.scat_var3, command=lambda:self.both_off('scat'))
        self.scat_btn3.pack(side='left', padx=10)

        # Console area.
        style2 = ttk.Style()
        style2.configure('cons.TFrame', background='blue')
        console_fram = ttk.Frame(right_frame, height=50, style='cons.TFrame')
        console_fram.pack_propagate(0)
        console_fram.pack(expand=True, fill='both')
        txt_style = ttk.Style()
        txt_style.configure('txt.TLabel', font=f)
        self.var = ConsoleStringVar()
        txt = ttk.Label(console_fram,textvariable=self.var,anchor='w',style='txt.TLabel')
        txt.pack(fill='x')

        button = ttk.Button(self.frame, text='RUN', command=self.run)
        button.pack(side='left')
        
    
    def disable_all(self, graph):
        if graph == 'histo':
            var1 = self.histo_var1
            var2 = self.histo_var2
            var3 = self.histo_var3
            button2 = self.histo_btn2
            button3 = self.histo_btn3
        elif graph == 'scat':
            var1 = self.scat_var1
            var2 = self.scat_var2
            var3 = self.scat_var3
            button2 = self.scat_btn2
            button3 = self.scat_btn3
        if var1.get():
            if not var2.get() and not var3.get():
                var2.set(True)
                var3.set(True)
            button2.config(state='normal')
            button3.config(state='normal')
        else:
            button2.config(state='disabled')
            button3.config(state='disabled')

    def both_off(self, graph):
        if graph == 'histo':
            v1 = self.histo_var1
            v2 = self.histo_var2
            v3 = self.histo_var3
        elif graph == 'scat':
            v1 = self.scat_var1
            v2 = self.scat_var2
            v3 = self.scat_var3
        if not v2.get() and not v3.get():
            v1.set(False)
        elif (v2.get() or v3.get()) and not v1.get():
            v1.set(True)
    
    def run(self):
        def analyse():
            d = DrawGraph(self)
            try:
                path =d.get_image_abspath('./1.JPG')
                bgra = d.detect_white_background(path)
                bgr,hsv=d.remove_invisible(image_bgra=bgra)
                bgr_fig = d.draw_histogram(bgr,'BGR')
                d.save_histogram(bgr_fig, 'test','BGR',result_path='kuma')
                hsv_fig = d.draw_histogram(hsv,'HSV')
                d.save_histogram(hsv_fig,'test','HSV',result_path='kuma')
                fig =d.draw_scatter3d(bgr,'BGR')
                d.save_scatter3d(fig,'test','BGR',result_path='kuma')
            except Exception as e:
                self.var.set_message('  '+str(e))
                print(e)
            
        thread1 = threading.Thread(target=analyse)
        thread1.start()



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

class ConsoleStringVar(tk.StringVar):
    def __init__(self):
        super().__init__()
        self.message = ''
        self.progress = []
        self.text = ''

    # def set(self):
    #     print('stringvar set')
    #     self.text += self.message + '\n'
    #     for prog in self.progress:
    #         self.text += prog.name + '\n'
    #         total = prog.total
    #         print(prog.name, prog.total, prog.now)
    #         now = prog.now
    #         percent = int(now/total*100)
    #         p = (3 -len(str(percent)))*' '+str(percent)
    #         prog = '='*(percent//5 -1)+'>'+' '*(20-percent//5)
    #         self.text += f'{p}% |{prog}|\n'
    #     super().set(self.text)
            
    def set_message(self, message):

        self.text += message+'\n'
        super().set(self.text)

    def set_progress(self, progress):
        text =''
        for prog in progress:
            text += prog.name + '\n'
            total = prog.total
            print(prog.name, prog.total, prog.now)
            now = prog.now
            if now == 0:
                text+='  0% |'+'.'*20+'|\n'
            percent = int(now/total*100)
            p = (3 -len(str(percent)))*' '+str(percent)
            prog = '='*(percent//5 -1)+'>'+'.'*(20-percent//5)
            if percent ==100:
                text += f'{p}% |{prog}| Done.\n'
            else:
                text += f'{p}% |{prog}|\n'
        super().set(self.text + text)

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