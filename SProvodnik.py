from shutil import copyfile
import os
import tkinter as tk

selected_item = ""

def type_analyze(lis):
    global was
    global name_file
    for widget in scroll_frame.winfo_children():
        widget.destroy()
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

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-event.delta / 120), "units")

window = tk.Tk()
window.geometry('1000x600')
canvas = tk.Canvas(window)
scroll_frame = tk.Frame(canvas)

scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

window.bind_all("<MouseWheel>", on_mouse_wheel)
direction = os.getcwd()
os.chdir(direction[2])
direction = os.getcwd()
lis = os.listdir()
type_analyze(lis)
window.mainloop()