import os
import re
import glob
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk
import tkinter as tk



def sett(files, dir_no=None):
        '''Get only file name, and set stringvar.
        
        Parameters
        ----------
        files : list
            List of files names.
        dir_no : int
            directories number.'''
        files = list(map(NameUtil.abspath, files))
        if dir_no == None:
            dirs = []
            for file in files:
                # if os.path.isfile(file):
                    dirs.append(os.path.dirname(file))
                # else:
                    # dirs.append(file)
                    # print(file)
            dir_no = len(set(dirs))

        print(dir_no)
        
        files = files
        if dir_no == 1:
            names = list(map(os.path.basename, files))
        elif dir_no > 1:
            names = list(map(NameUtil.get_dir_and_name, files))

        # print(names)
        

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
        abspath = NameUtil.abspath(path)
        after_dir = abspath.split('/')[-2:]
        return '/'.join(after_dir)

f = glob.glob('./*')
f.extend(glob.glob('c:/Users/Kento Terada/VSwork/image_analysis/env/Scripts/*'))

sett(f)

root = tk.Tk()
root.geometry('400x200')
root.columnconfigure(0,weight=1)
root.rowconfigure(0, weight=1)
style = ttk.Style()
style.configure('list.TFrame',background='red')
frame = ttk.Frame(root, style='list.TFrame')
frame.grid(row=0,column=0, sticky='NSEW')
root.mainloop()
