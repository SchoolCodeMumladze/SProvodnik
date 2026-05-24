from shutil import copyfile
import os
import tkinter as tk

selected_item = ""
was = False
search_list = []
searching_bool = False

def back():
    global was
    dir = os.getcwd().split("\\")
    dir = dir[:-1]
    if len(dir) == 1:
        new_dir = dir[0] + "\\"
        was = False
    else:
        new_dir = "\\".join(dir)
    os.chdir(new_dir)
    type_analyze(os.listdir())

def type_analyze(lis):
    global was
    global searching_bool
    searching_bool = False
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    if was:
        back_btn = tk.Button(scroll_frame, text="Назад", command=back).pack(side=tk.RIGHT)
    direct = tk.Label(scroll_frame, text=os.getcwd()).pack()
    for item in lis:
        if os.path.isfile(item):
            btn = tk.Button(scroll_frame, text=f"📄 Файл {item}", command=lambda i=item: f_analyze(i))
            btn.pack(fill=tk.BOTH, padx=10, pady=2)
        else:
            btn = tk.Button(scroll_frame, text=f"📁 Папка {item}", command=lambda i=item: d_analyze(i))
            btn.pack(fill=tk.BOTH, padx=10, pady=2)
    was = True
    scroll_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def f_analyze(_):
    global selected_item
    global searching_bool
    if searching_bool:
        os.chdir(_[0])
        selected_item = _[1]
    else:
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
    global searching_bool
    if searching_bool:
        os.chdir(_[0])
        selected_item = _
    else:
        selected_item = _
    new_window = tk.Toplevel()
    b_1 = tk.Button(new_window, text="Открыть папку", command=open_dir)
    b_1.pack()
    b_2 = tk.Button(new_window, text="Удалить папку", command=remove_file)
    b_2.pack()
    b_3 = tk.Button(new_window, text="Переименовать папку", command=rename_file)
    b_3.pack()
    new_window.mainloop()
    new_window.destroy()

def open_dir():
    global selected_item
    os.chdir(selected_item)
    type_analyze(os.listdir())

def open_file():
    global selected_item
    os.startfile(selected_item)

def rename_file():
    global new_name
    inp = os.getcwd().split("\\")[-1]
    new_name = tk.Entry(window)
    new_name.pack()
    btn_rename = tk.Button(scroll_frame, text="Подтвердить ввод", command=get_entry).pack()
    os.rename(inp, new_name)

def get_entry():
    global new_name
    new_name = new_name.get()

def remove_file():
    inp = os.getcwd().split("\\")[-1]
    os.remove(inp)
    t = tk.Label(text="Вы успешно удалили файл/папку!")
    t.pack()

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-event.delta / 120), "units")


def create_new_item():
    name = name_entry.get()
    if "." in name:
        with open(name, "w") as f:
            f.write("")
    else:
        os.mkdir(name)
    type_analyze(os.listdir())

def searching():
    global search_list
    global searching_bool
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    search_name = tk.Entry(scroll_frame).pack()
    new_name = search_name
    get_btn = tk.Button(scroll_frame, text="Подтвердить ввод", command=lambda: new_name.get()).pack()
    searching_bool = True
    directory_path = os.getcwd()
    for root, dirs, files in os.walk(directory_path):
        dir = None
        el = None
        dir = os.path.abspath(root)
        for directory in dirs:
            if new_name in directory:
                el = directory
        for file in files:
            if new_name in file:
                el = file
        if not el:
            continue
    searching_2()

def searching_2():
    global search_list
    for item in search_list:
        if os.path.isfile(item[1]):
            btn = tk.Button(scroll_frame, text=f"📄 Файл {item[1]}", command=lambda i=item: f_analyze(i))
            btn.pack(fill=tk.BOTH, padx=10, pady=2)
        else:
            btn = tk.Button(scroll_frame, text=f"📁 Папка {item[1]}", command=lambda i=item: d_analyze(i))
            btn.pack(fill=tk.BOTH, padx=10, pady=2)
    scroll_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

window = tk.Tk()
window.geometry('1000x600')
top_frame = tk.Frame(window)
top_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(top_frame, text="Имя нового файла/папки:").pack(side=tk.LEFT)
name_entry = tk.Entry(top_frame)
name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
tk.Button(top_frame, text="Создать", command=create_new_item).pack(side=tk.LEFT)
canvas = tk.Canvas(window)
scroll_frame = tk.Frame(canvas)

scroll_frame.bind("<Configure>", lambda x: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

window.bind_all("<MouseWheel>", on_mouse_wheel)
search_button = tk.Button(top_frame, text="Перейти к поиску", command=searching).pack()
direction = os.getcwd()
os.chdir(direction[2])
direction = os.getcwd()
lis = os.listdir()
type_analyze(lis)
window.mainloop()