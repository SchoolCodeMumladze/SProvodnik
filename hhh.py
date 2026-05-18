import os
import tkinter as tk
from tkinter import messagebox

# Глобальные переменные для управления состоянием
was = False
current_path = os.getcwd()
selected_item = ""


def on_mouse_wheel(event):
    # Прокрутка холста колесиком мыши
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def update_scroll_region():
    # Обновление зоны прокрутки после добавления элементов
    scroll_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def type_analyze(lis):
    global was

    # Очищаем внутренний фрейм с кнопками, а не все окно
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    if was:
        h = tk.Label(scroll_frame, text="Добро пожаловать в SПроводник",
                     font=("Arial", 14), foreground="black", background="white", height=2)
        h.pack(pady=5)

    was = True

    # Выводим текущий путь для удобства
    path_lbl = tk.Label(scroll_frame, text=f"Текущий путь: {os.getcwd()}", fg="blue")
    path_lbl.pack(pady=2)

    # Создаем кнопки для файлов и папок
    for item in lis:
        # Лямбда-функция передает конкретное имя элемента в обработчик
        if os.path.isfile(item):
            btn = tk.Button(scroll_frame, text=f"📄 Файл {item}",
                            command=lambda i=item: f_analyze(i))
            btn.pack(fill=tk.X, padx=10, pady=2)
        else:
            btn = tk.Button(scroll_frame, text=f"📁 Папка {item}",
                            command=lambda i=item: d_analyze(i))
            btn.pack(fill=tk.X, padx=10, pady=2)

    # Обновляем прокрутку под новое количество кнопок
    update_scroll_region()


def f_analyze(item_name):
    global selected_item
    selected_item = item_name
    new_window = tk.Toplevel(window)
    new_window.title(f"Файл: {item_name}")
    new_window.geometry("250x150")

    tk.Button(new_window, text="Открыть файл", command=open_file).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(new_window, text="Удалить файл", command=remove_file).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(new_window, text="Переименовать файл", command=rename_window).pack(fill=tk.X, padx=20, pady=5)


def d_analyze(item_name):
    global selected_item
    selected_item = item_name
    new_window = tk.Toplevel(window)
    new_window.title(f"Папка: {item_name}")
    new_window.geometry("250x150")

    tk.Button(new_window, text="Открыть папку", command=open_dir).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(new_window, text="Удалить папку", command=remove_dir).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(new_window, text="Переименовать папку", command=rename_window).pack(fill=tk.X, padx=20, pady=5)


def open_dir():
    global selected_item
    try:
        os.chdir(selected_item)
        type_analyze(os.listdir())
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть папку: {e}")


def open_file():
    global selected_item
    try:
        os.startfile(selected_item)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")


def rename_window():
    # Окно для ввода нового имени
    ren_win = tk.Toplevel(window)
    ren_win.title("Переименование")
    tk.Label(ren_win, text="Введите новое имя:").pack(pady=5)
    entry = tk.Entry(ren_win)
    entry.pack(pady=5)

    def confirm():
        global selected_item
        new_name = entry.get()
        if new_name:
            try:
                os.rename(selected_item, new_name)
                ren_win.destroy()
                type_analyze(os.listdir())
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    tk.Button(ren_win, text="ОК", command=confirm).pack(pady=5)


def remove_file():
    global selected_item
    try:
        os.remove(selected_item)
        messagebox.showinfo("Успех", "Вы успешно удалили файл!")
        type_analyze(os.listdir())
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def remove_dir():
    global selected_item
    try:
        os.rmdir(selected_item)
        messagebox.showinfo("Успех", "Вы успешно удалили папку!")
        type_analyze(os.listdir())
    except Exception as e:
        messagebox.showerror("Ошибка", "Папка должна быть пустой для удаления через rmdir")


def create_new_item():
    name = name_entry.get()
    if not name:
        return
    if name in os.listdir():
        messagebox.showwarning("Внимание", "Такой элемент уже существует")
        return

    if "." in name:  # Если есть расширение — создаем файл
        with open(name, "w") as f:
            f.write("")
    else:  # Иначе создаем папку
        os.mkdir(name)
    type_analyze(os.listdir())


# Инициализация главного окна
window = tk.Tk()
window.title("SПроводник")
window.geometry('500x600')

# Ввод для создания новых файлов/папок
top_frame = tk.Frame(window)
top_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(top_frame, text="Имя нового файла/папки:").pack(side=tk.LEFT)
name_entry = tk.Entry(top_frame)
name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
tk.Button(top_frame, text="Создать", command=create_new_item).pack(side=tk.LEFT)

# Создание структуры для прокрутки (Canvas + Scrollbar)
container = tk.Frame(window)
container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

canvas = tk.Canvas(container)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Привязка колесика мыши к холсту и всем его элементам
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Переход в корневую директорию диска (исправление вашей логики)
try:
    current_drive = os.getcwd()[:3]  # Например, "C:\\"
    os.chdir(current_drive)
except:
    pass

# Первый запуск анализа директории
type_analyze(os.listdir())

window.mainloop()