import tkinter as tk


def create_tab1(self,tab1):
    text1 = tk.StringVar()
    text1.set('tab1: Hello')
    label = tk.Label(tab1, textvariable=text1)
    label.pack()
    btn = tk.Button(tab1)
    btn["text"] = "Test"
    btn["command"] = lambda:btn_func(text1)
    btn["width"] = 12
    btn.pack()
    return

def btn_func(text):
    text.set("Good morning")
    print("push")
    return