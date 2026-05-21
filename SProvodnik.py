from shutil import copyfile
import os
import tkinter as tk

selected_item = ""
new_name = ""

def type_analyze(lis):
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    direct = tk.Label(scroll_frame, text=os.getcwd()).pack()
    for item in lis:
        if os.path.isfile(item):
            btn = tk.Button(scroll_frame, text=f"📄 Файл {item}", command=lambda i=item: f_analyze(i))
            btn.pack(fill=tk.BOTH, padx=10, pady=2)
        else:
            btn = tk.Button(scroll_frame, text=f"📁 Папка {item}", command=lambda i=item: d_analyze(i))
            btn.pack(fill=tk.BOTH, padx=10, pady=2)

    scroll_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

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
    new_window.destroy()

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
direction = os.getcwd()
os.chdir(direction[2])
direction = os.getcwd()
lis = os.listdir()
type_analyze(lis)
window.mainloop()