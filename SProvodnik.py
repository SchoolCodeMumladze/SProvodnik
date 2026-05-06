from shutil import copyfile
import os
import tkinter as tk

def type_analyze(lis):
    for _ in lis:
        if os.path.isfile(_):
            # name = tk.Label(window, text="Файл")
            # name.pack()
            print("Файл")
            print(_)
            # btn = tk.Button(window, f_analyze)
            # btn.pack()
            # f_analyze()
            # break
        else:
            # name = tk.Label(window, text="Папка")
            # name.pack()
            print("Папка")
            print(_)
            # btn = tk.Button(window, d_analyze)
            # d_analyze()

def f_analyze():
    # new_window = tk.Toplevel()
    # b_1 = tk.Button(new_window, text="Открыть файл", command=open_file)
    # b_1.pack()
    # b_2 = tk.Button(new_window, text="Удалить файл", command=remove_file)
    # b_2.pack()
    inp = input("Введите О, если хотите открыть файл и введите У, если хотите удалить файл ")
    if inp == "О":
        open_file()
    else:
        remove_file()

def d_analyze():
    # new_window = tk.Toplevel()
    # b_1 = tk.Button(new_window, text="Открыть папку", command=open_dir)
    # b_1.pack()
    # b_2 = tk.Button(new_window, text="Удалить папку", command=remove_file)
    # b_2.pack()
    inp = input("Введите О, если хотите открыть папку и введите У, если хотите удалить папку ")
    if inp == "О":
        open_dir()
    else:
        remove_file()

def open_dir():
    os.chdir(os.getcwd())

def open_file():
    os.chdir(os.getcwd())
    os.startfile(os.getcwd())

def remove_file():
    """Функция не работает"""
    os.remove(os.getcwd())
    print("Вы успешно удалили папку / файл")

# window = tk.Tk()
# window.geometry('500x2000')
# t = tk.Label(window, text="Добро пожаловать в SПроводник",
#                 font=100,
#                 foreground="black",
#                 background="white",
#                 height=2)
# t.pack()
print("Добро пожаовать в SПроводник")
disc = input("Введите букву диска ")
direction = os.getcwd()
os.chdir(direction[2])
direction = os.getcwd()
# while True:
lis = os.listdir()
type_analyze(lis)

while True:
    name_file = input("Введите название файла/папки, с которым хотите работать ")
    if os.path.isfile(name_file):
        f_analyze()
        break
    else:
        os.chdir(name_file)
        d_analyze()
        type_analyze(os.listdir())

# window.mainloop()