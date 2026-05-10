from shutil import copyfile
import os
import tkinter as tk

def type_analyze(lis):
    for _ in lis:
        if os.path.isfile(_):
            btn = tk.Button(window, text=f"Файл {_}", command=f_analyze)
            btn.pack()
        else:
            btn = tk.Button(window, text=f"Папка {_}", command=d_analyze)
            btn.pack()

def f_analyze():
    new_window = tk.Toplevel()
    b_1 = tk.Button(new_window, text="Открыть файл", command=open_file)
    b_1.pack()
    b_2 = tk.Button(new_window, text="Удалить файл", command=remove_file)
    b_2.pack()
    b_3 = tk.Button(new_window, text="Переименовать файл", command=rename_file)
    b_3.pack()
    new_window.mainloop()

def d_analyze():
    new_window = tk.Toplevel()
    b_1 = tk.Button(new_window, text="Открыть папку", command=open_dir)
    b_1.pack()
    b_2 = tk.Button(new_window, text="Удалить папку", command=remove_file)
    b_2.pack()
    b_3 = tk.Button(new_window, text="Переименовать папку", command=rename_file)
    b_3.pack()
    new_window.mainloop()

def open_dir():
    global name_file
    os.chdir(name_file)
    type_analyze(os.listdir())

def open_file():
    global name_file
    os.chdir(name_file)
    os.startfile(os.getcwd())

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
    name_file.get()
    window.config()

window = tk.Tk()
window.geometry('500x2000')
t = tk.Label(window, text="Добро пожаловать в SПроводник",
                font=100,
                foreground="black",
                background="white",
                height=2)
t.pack()
# print("Добро пожаовать в SПроводник")
# disc = input("Введите букву диска ")
direction = os.getcwd()
os.chdir(direction[2])
direction = os.getcwd()
lis = os.listdir()
type_analyze(lis)

while True:
    name_file = tk.Entry(window)
    name_file.pack()
    bttn = tk.Button(window, text="Подтвердить текст", command=get_entry)
    bttn.pack()
    window.mainloop()
    if name_file not in os.listdir():
        open(name_file, "w")
    if os.path.isfile(name_file):
        f_analyze()
        break
    else:
        os.chdir(name_file)
        d_analyze()
        type_analyze(os.listdir())