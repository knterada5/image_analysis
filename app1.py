import tkinter as tk
import tkinter.ttk as ttk
import tkinterdnd2 as dnd2
from PIL import Image, ImageTk
import base
from histo import DrawGraph
import re
import os

class Application(base.BaseObserver):
    '''Application class.
    
    Subscribe analysis process, recieve message and progress.
    '''
    def update_message(self, message):
        '''Catch message from DrawGraph class.'''
        self.message = message

    def update_process(self, process):
        '''Catch process of DrawGraph class.'''
        pass

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

class DrawGraphTab(ttk.Frame):
    '''Draw graph tab class'''
    def __init__(self, master):
        super().__init__(master)
        master.add(self, text='グラフ')
        self.create_widgets()

    def create_widgets(self):
        '''Create widgets, input area, console area, result area and run button.'''

        # Input area.
        input_frame = ttk.Frame(self, width=100)
        input_frame.pack_propagate(0)
        input_frame.pack(side='left', expand=True, fill='both')

class DropFolderFrame(ttk.Frame):
    '''Drop folder area.'''

    def __init__(self, master):
        super().__init__(master)
        self.pack_propagate(0)
        self.pack(expand=True, fill='both')
        self.create()
        return

    def create(self):
        pass

class DropPathStringVar(tk.StringVar):
    '''Get path from dropped, and set string var of tkinter.'''
    def __init__(self):
        super().__init__()
        self.p_frame = None

    def set(self, event):
        '''Set abspath converted from dropped strings.
        
        Parameters
        ----------
        event : event
            dnd2 dropped event.
        '''

        # Extract shortest string between '{' and '}'. 
        pattern = '\{.*?\}'
        dropped = re.findall(pattern, event.data)
        # Delete {} of head and tail.
        abspath = list(map(lambda x: x[1:-1], dropped))
        # Set parenet parameter, path.
        self.p_abspath = abspath

        def get_dir_name(path):
            '''Get only directory name.'''
            if os.path.isfile(path):
                return path.split('/')[-2]    # Folder name. (e.g. C:/Users/Taro/Documents/aaa.txt -> Documents)
            else:
                return path.split('/')[-1]

        # Get only directory name to set parent frame's label.
        directory = list(map(get_dir_name, dropped))
        # Set joined directories to StringVar. 
        super().set(", ".join(directory))

    def set_params(self, p_frame, p_path, p_list):
        '''Set parameters. frame and list.

        When set folder path to this class, this class makes frame raise
        and sets absolute path and file list to parent frame.
        
        Parameters
        ----------
        frame : tkinter.Frame or ttk.Frame
            Raised frame when set folder path to this class.
        path : list
            Set absolute path of folders to this list when set folder path to this class.
        list : StringVar
            Updated list when set folder path to this class.
        '''
        self.p_frame = p_frame
        self.p_list = p_list
        self.p_abspath = p_path

    def raise_frame(self):
        '''Raise frame when string is set. '''
        if self.p_frame != None:
            self.p_frame.tkraise()

a = Application()
a.main()