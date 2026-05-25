import os
import tkinter as tk

selected_item = ""
was = False
search_list = []
searching_bool = False
searc_name = None
search_name = None

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
        back_btn = tk.Button(scroll_frame, text="Назад", command=back, bg="#d1cfd1").pack(side=tk.RIGHT)
    direct = tk.Label(scroll_frame, text=os.getcwd()).pack()
    for item in lis:
        if os.path.isfile(item):
            btn = tk.Button(scroll_frame, text=f"📄 Файл {item}", command=lambda i=item: f_analyze(i), bg="#9c9c9c")
            btn.pack(fill=tk.BOTH, padx=10, pady=2)
        else:
            btn = tk.Button(scroll_frame, text=f"📁 Папка {item}", command=lambda i=item: d_analyze(i), bg="#f2f05e")
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
    b_1 = tk.Button(new_window, text="Открыть файл", command=open_file, bg="#679bab")
    b_1.pack()
    b_2 = tk.Button(new_window, text="Удалить файл", command=remove_file, bg="#ff8859")
    b_2.pack()
    b_3 = tk.Button(new_window, text="Переименовать файл", command=rename_file, bg="#60c46a")
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
    b_1 = tk.Button(new_window, text="Открыть папку", command=open_dir, bg="#679bab")
    b_1.pack()
    b_2 = tk.Button(new_window, text="Удалить папку", command=remove_file, bg="#ff8859")
    b_2.pack()
    b_3 = tk.Button(new_window, text="Переименовать папку", command=rename_file, bg="#60c46a")
    b_3.pack()
    new_window.mainloop()

def open_dir():
    global selected_item
    if type(selected_item) == tuple:
        selected_item = selected_item[1]
    os.chdir(selected_item)
    type_analyze(os.listdir())

def open_file():
    global selected_item
    os.startfile(selected_item)


def rename_file():
    global entry_widget, rename_window
    rename_window = tk.Toplevel()
    rename_window.geometry("300x100")
    tk.Label(rename_window, text=f"Новое имя для: {selected_item}").pack(pady=5)
    entry_widget = tk.Entry(rename_window, width=30)
    entry_widget.insert(0, selected_item)
    entry_widget.pack(pady=5)
    btn_rename = tk.Button(rename_window, text="Подтвердить", command=confirm_rename)
    btn_rename.pack(pady=5)

def confirm_rename():
    global entry_widget, rename_window, selected_item
    new_name = entry_widget.get()
    if not new_name or new_name == selected_item:
        rename_window.destroy()
        return
    try:
        os.rename(selected_item, new_name)
        rename_window.destroy()
        type_analyze(os.listdir())
    except Exception as e:
        tk.Label(rename_window, text="Ошибка", fg="red").pack()

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
    try:
        if "." in name:
            with open(name, "w") as f:
                f.write("")
        else:
            os.mkdir(name)
        type_analyze(os.listdir())
    except:
        err = tk.Label(scroll_frame, text="Ошибка", fg="red").pack()


def searching():
    global searc_name
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    tk.Label(scroll_frame, text="Введите имя для поиска:").pack(pady=5)
    searc_name = tk.Entry(scroll_frame)
    searc_name.pack(pady=5)
    get_btn = tk.Button(scroll_frame, text="Найти", command=get_search, bg="#FFFFFF")
    get_btn.pack(pady=5)

def get_search():
    global search_list, searching_bool, searc_name, search_name
    search_query = searc_name.get()
    search_list = []
    searching_bool = True
    directory_path = os.getcwd()
    for root, dirs, files in os.walk(directory_path):
        for directory in dirs:
            if search_query in directory:
                search_list.append((root, directory))
        for file in files:
            if search_query in file:
                search_list.append((root, file))
    searching_2()

def searching_2():
    global search_list
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    if not search_list:
        tk.Label(scroll_frame, text="Ничего не найдено").pack()
    for item in search_list:
        full_path = os.path.join(item[0], item[1])
        if os.path.isfile(full_path):
            btn = tk.Button(scroll_frame, text=f"📄 Файл {item[1]}", command=lambda i=item: f_analyze(i), bg="#9c9c9c")
            btn.pack(fill=tk.BOTH, padx=10, pady=2)
        else:
            btn = tk.Button(scroll_frame, text=f"📁 Папка {item[1]}", command=lambda i=item: d_analyze(i), bg="#f2f05e")
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
tk.Button(top_frame, text="Создать", command=create_new_item, bg="#62de59").pack(side=tk.LEFT)
canvas = tk.Canvas(window)
scroll_frame = tk.Frame(canvas)

scroll_frame.bind("<Configure>", lambda x: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

window.bind_all("<MouseWheel>", on_mouse_wheel)
search_button = tk.Button(top_frame, text="Перейти к поиску", command=searching, bg="#6572a1").pack()
direction = os.getcwd()
os.chdir(direction[2])
direction = os.getcwd()
lis = os.listdir()
type_analyze(lis)
window.mainloop()