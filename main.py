 
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Импортируем функции из ваших скриптов
import subs        # Скрипт для загрузки субтитров (&#8203;:contentReference[oaicite:0]{index=0})
import processVTT  # Скрипт для обработки VTT файлов (&#8203;:contentReference[oaicite:1]{index=1})

def process_video():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Ошибка", "Введите ссылку на видео.")
        return

    # Каталог для сохранения субтитров
    output_dir = "subtitles"
    os.makedirs(output_dir, exist_ok=True)

    # Загрузка субтитров по ссылке
    try:
        downloaded_files = subs.download_all_subtitles(url, output_dir=output_dir)
    except Exception as e:
        messagebox.showerror("Ошибка при загрузке", f"Произошла ошибка: {e}")
        return

    if not downloaded_files:
        messagebox.showinfo("Информация", "Субтитры не были загружены.")
        return

    # Очистка списка обработанных файлов
    listbox.delete(0, tk.END)

    # Обработка каждого VTT файла и сохранение результата
    for file in downloaded_files:
        if file.lower().endswith('.vtt'):
            try:
                processed_text = processVTT.merge_vtt_file(file)
                txt_filename = os.path.splitext(file)[0] + ".txt"
                with open(txt_filename, 'w', encoding='utf-8') as f:
                    f.write(processed_text)
                listbox.insert(tk.END, txt_filename)
            except Exception as e:
                messagebox.showerror("Ошибка обработки", f"Ошибка при обработке файла {file}: {e}")
    messagebox.showinfo("Готово", "Субтитры загружены и обработаны.")

def open_subtitle():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Ошибка", "Выберите файл субтитров для открытия.")
        return
    file_to_open = listbox.get(selected[0])
    if os.path.exists(file_to_open):
        try:
            with open(file_to_open, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
            return

        # Открытие нового окна для просмотра содержимого
        view_window = tk.Toplevel(root)
        view_window.title(file_to_open)
        text_area = scrolledtext.ScrolledText(view_window, width=80, height=30)
        text_area.pack(expand=True, fill='both')
        text_area.insert(tk.END, content)
    else:
        messagebox.showerror("Ошибка", "Файл не найден.")

# Создание главного окна
root = tk.Tk()
root.title("Subtitle Downloader and Processor")

# Фрейм для ввода ссылки и кнопки загрузки
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Ссылка на видео:").grid(row=0, column=0, sticky='w')
url_entry = tk.Entry(frame, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)
download_button = tk.Button(frame, text="Загрузить и обработать", command=process_video)
download_button.grid(row=0, column=2, padx=5)

# Список для отображения обработанных файлов
listbox = tk.Listbox(root, width=80)
listbox.pack(padx=10, pady=10)

# Кнопка для открытия выбранного файла
open_button = tk.Button(root, text="Открыть выбранные субтитры", command=open_subtitle)
open_button.pack(pady=5)

root.mainloop()
