import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk


def show_error_dialog():
    messagebox.showerror('Error!!', 'Select folder.')

root = tk.Tk()
root.title("Note")
root.geometry("300x200")

notebook = ttk.Notebook(root)

tab_1 = tk.Frame(notebook, bg='white')
tab_2 = tk.Frame(notebook, bg='blue')

notebook.add(tab_1, text="tab1")
notebook.add(tab_2, text="tab2")

label = ttk.Label(tab_1, text="こんにちは", background='white')
button = tk.Button(tab_1, text='button', command=show_error_dialog)
button.pack()
notebook.pack(expand=True, fill='both', padx=10, pady=10)
label.pack()


root.mainloop()

