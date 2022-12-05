import tkinterdnd2 as dnd2
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter as tk
import mtab1
import test_tab

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        return

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=1, fill='both')

        tab1 = tk.Frame(notebook)
        tab2 = tk.Frame(notebook)
        tab3 = tk.Frame(notebook)

        notebook.add(tab1, text='ヒストグラム')
        notebook.add(tab2, text='3D 散布図')
        notebook.add(tab3, text='色調補正')
        
        test = test_tab.Tab2(notebook)

        mtab1.create_tab1(self, tab1)

def main():
    root = tk.Tk()
    root.geometry('300x200')
    root.title('Image analysis Home')
    app = Application(master=root)
    app.mainloop()
    pass

if __name__ == '__main__':
    main()