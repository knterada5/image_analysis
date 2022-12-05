import tkinter as tk

root = tk.Tk()
root.geometry('300x200')
# root.grid_rowconfigure(0, weight=1)
# root.grid_columnconfigure(0,weight=1)
# root.grid_columnconfigure(1,weight=1)

# left = tkinter.Frame(root,bg='red')
# left.grid(row=0,column=0,sticky=tkinter.NSEW)

# label = tkinter.Label(left,text='kon')
# label.pack()

# left2= tkinter.Frame(root, bg='green')
# left2.grid(row=0,column=0, sticky=tkinter.NSEW)

# left.tkraise()

# right = tkinter.Frame(root,bg='blue')
# right.grid(row=0,column=1,sticky=tkinter.NSEW)

left = tk.Frame(root, bg='red')
left.pack(expand=True,fill='both')
left.grid_rowconfigure(0,weight=1)
left.grid_columnconfigure(0,weight=1)
left.grid_columnconfigure(1,weight=1)

left2 = tk.Frame(left, bg='blue')
left2.grid(row=0,column=0,sticky=tk.NSEW)

root.mainloop()