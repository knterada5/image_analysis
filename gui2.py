import tkinterdnd2 as dnd2
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter as tk

root = dnd2.Tk()
var = tk.StringVar()

def main():
    disp()

def disp():
    root.title('test title')
    root.geometry('300x200')

    notebook = ttk.Notebook(root)
    tab_1 = tk.Frame(notebook)
    tab_2 = tk.Frame(notebook)

    notebook.add(tab_1, text='tab1')
    notebook.add(tab_2, text='tab2')
    notebook.grid(column=0,row=0)

    label = ttk.Label(tab_1, text='ラベルだよ')
    label.grid(column=0,row=0)

    entry = tk.Entry(tab_1, textvariable=var)
    entry.drop_target_register(dnd2.DND_FILES)
    entry.dnd_bind('<<Drop>>', drop)
    entry.grid(column=1, row=0)

    root.mainloop()

def drop(event):
    var.set(event.data)


if __name__ == '__main__':
    main()