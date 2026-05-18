from shutil import copyfile
import os
import tkinter as tk
from tkinter import ttk

was = False
selected_item = ""

def type_analyze(lis):
    global was
    global name_file
    for widget in window.winfo_children():
        widget.destroy()
    if was:
        h = tk.Label(window, text="Добро пожаловать в SПроводник",
                    font=100,
                    foreground="black",
                    background="white",
                    height=2)
        h.pack()
        # name_file = tk.Entry(window)
        # name_file.pack()
        # bttn = tk.Button(window, text="Подтвердить текст", command=get_entry)
        # bttn.pack()
    was = True
    for item in lis:
        if os.path.isfile(item):
            btn = tk.Button(window, text=f"📄 Файл {item}", command=lambda i=item: f_analyze(i))
            btn.pack(padx=10, pady=2)
        else:
            btn = tk.Button(window, text=f"📁 Папка {item}", command=lambda i=item: d_analyze(i))
            btn.pack(padx=10, pady=2)

def f_analyze(_):
    global selected_item
    selected_item = _
    new_window = tk.Toplevel()
    b_1 = tk.Button(new_window, text="Открыть файл", command=open_file)
    b_1.pack()
    b_2 = tk.Button(new_window, text="Удалить файл", command=remove_file)
    b_2.pack()
    b_3 = tk.Button(new_window, text="Переименовать файл", command=rename_file)
    b_3.pack()
    new_window.mainloop()

def d_analyze(_):
    global selected_item
    selected_item = _
    new_window = tk.Toplevel()
    b_1 = tk.Button(new_window, text="Открыть папку", command=open_dir)
    b_1.pack()
    b_2 = tk.Button(new_window, text="Удалить папку", command=remove_file)
    b_2.pack()
    b_3 = tk.Button(new_window, text="Переименовать папку", command=rename_file)
    b_3.pack()
    new_window.mainloop()

def open_dir():
    global selected_item
    os.chdir(selected_item)
    type_analyze(os.listdir())

def open_file():
    global selected_item
    os.startfile(selected_item)

def rename_file():
    inp = os.getcwd().split("\\")[-1]
    new_name = tk.Entry(window)
    new_name.pack()
    os.rename(inp, new_name)

def remove_file():
    inp = os.getcwd().split("\\")[-1]
    os.remove(inp)
    t = tk.Label(text="Вы успешно удалили файл/папку!")
    t.pack()

def get_entry():
    global name_file
    name_file = name_file.get()

window = tk.Tk()
window.geometry('500x2000')
t = tk.Label(window, text="Добро пожаловать в SПроводник",
                font=100,
                foreground="black",
                background="white",
                height=2)
t.pack()
direction = os.getcwd()
os.chdir(direction[2])
direction = os.getcwd()
lis = os.listdir()
type_analyze(lis)
window.mainloop()
# while True:
#     name_file = tk.Entry(window)
#     name_file.pack()
#     bttn = tk.Button(window, text="Подтвердить текст", command=get_entry)
#     bttn.pack()
#     window.mainloop()
#     if name_file not in os.listdir():
#         open(name_file, "w")
#     if os.path.isfile(name_file):
#         f_analyze()
#         break
#     else:
#         os.chdir(name_file)
#         d_analyze()
#         type_analyze(os.listdir())