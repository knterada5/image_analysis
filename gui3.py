import tkinterdnd2 as dnd2
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter as tk

root = dnd2.Tk()
var = tk.StringVar()

def main():
    main_window()

def disp_frame(frame):
    frame.tkraise()

def main_window():
    root.title('Image analysis Top')
    root.geometry('904x1357')

    notebook = ttk.Notebook(root)
    notebook.grid(column=0, row=0)

    tab_histogram = tk.Frame(notebook)
    tab_3dmap = tk.Frame(notebook)
    tab_color_correction = tk.Frame(notebook)

    notebook.add(tab_histogram, text='ヒストグラム')
    notebook.add(tab_3dmap, text="3D 散布図")
    notebook.add(tab_color_correction, text='色調補正')
    
    show_histogram_frame(tab_histogram)

    root.mainloop()

def show_histogram_frame(frame):
    bg_image = tk.PhotoImage(file='1.png')
    background = tk.Label(frame, image=bg_image, text='aaa')

    background.pack(fill="x")

if __name__ == '__main__':
    main()