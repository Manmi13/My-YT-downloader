from pytubefix import YouTube
from pytubefix.cli import on_progress
import tkinter as tk
from tkinter import filedialog
import threading

root = tk.Tk()
root.title('mYTdownloader, ver. 1.0')
root.iconbitmap(r'C:\Users\user\Desktop\ico.ico')
root.geometry('580x300')
root.resizable(False, False)
root.configure(bg='#B0C4DE')

help_window = None
OutputPath = ''
last_percentage_reported = 0

itag = None
itag_to_search = None
streams_got = None

items = {'  video_2160': 'st_2160',
         '  video_1440': 'st_1440',
         '  video_1080': 'st_1080',
         '  video_720': 'st_720',
         '  video_480': 'st_480',
         '  video_360': 'st_360',
         '  video_240': 'st_240',
         '  audio': 'st_audio',
         }

streams_dict = {'st_2160': ('itag="315"', 'itag="401"'),
                'st_1440': ('itag="308"', 'itag="400"'),
                'st_1080': ('itag="137"', 'itag="248"', 'itag="299"', 'itag="303"', 'itag="399"'),
                'st_720': ('itag="136"', 'itag="247"', 'itag="298"', 'itag="398"', 'itag="302"'),
                'st_480': ('itag="135"', 'itag="244"', 'itag="397"'),
                'st_360': ('itag="18"', 'itag="134"', 'itag="396"'),
                'st_240': ('itag="133"', 'itag="242"', 'itag="395"'),
                'st_audio': ('itag="251"', 'itag="250"', 'itag="249"', 'itag="140"', 'itag="139"'),
                }


def on_select(event):
    global itag_to_search
    selected_index = listbox.curselection()
    if selected_index:
        selected_text = listbox.get(selected_index)
        itag_to_search = items[selected_text]


def search(par):
    global streams_got
    for i in par:
        if i in str(streams_got):
            return i[6:-1:]


def clear():
    entry_filename.delete(0, tk.END)
    entry_adress.delete(0, tk.END)
    entry_path.delete(0, tk.END)


def show_help_window():
    global help_window
    if help_window is not None and tk.Toplevel.winfo_exists(help_window):
        return

    help_window = tk.Toplevel(root)
    help_window.title("Справка")
    help_window.iconbitmap(r'C:\Users\user\Desktop\ico.ico')
    help_window.geometry("820x640")
    help_window.resizable(False, False)
    help_window.configure(bg='#B0C4DE')

    help_text = ("""
        contact: xplus1@proton.me \n
        1. Реализовано с помощью pytube и pytubefix на Python и использует коды itag *. Автор не несет никакой ответственности за использование данной программы. \n
        2. YouTube, очевидно, не желает, чтобы видео скачивали бесплатно, и постоянно улучшает методы защиты. Поэтому то, что работало вчера, может не работать завтра.\n
        3. Не все возможные itag доступны для каждого конкретного видео. Поэтому, если вы видите ошибку itag, попробуйте сменить поток. В основном касается потоков выше 720p.\n
        4. YouTube использует технологию потоковой передачи DASH, поэтому нужно загружать отдельно и аудио- и видеодорожки, а затем с помощью, например, FFmpeg, объединять.\n
        5. Измените расширение загруженного *.mp4 аудиофайла на *.m4a, чтобы добавить его как аудиодорожку к видео, например, в Light Alloy. \n
        6. Аудио приоритетно скачивается в .mp4 и кодеке \"opus\" с максимально доступным битрейтом 160 kbps, что сопоставимо с mp3 256 kbps. \n
        7. Файлы, содержащие и аудио и видео («прогрессивная загрузка»), доступны только для потока 360p.\n
        * - Каждое видео на YouTube доступно, как правило, в нескольких разрешениях. А каждое разрешение доступно в нескольких вариантах (потоках, отличающихся кодеком), которые имеют свой код itag. Например, для разрешения 1080p может быть доступно 5 разных потоков со своими кодами: itag="137"', 'itag="248"', 'itag="299"', 'itag="303"', 'itag="399". И всего таких кодов в одном видео может быть более 30. Программа ищет по itag первый доступный поток нужного разрешения и скачивает его.
        """
                 )

    label_help = tk.Label(help_window, text=help_text, font=(
        "Courier new", 12), bg='#E0E8F0', justify=tk.LEFT, wraplength=810)
    label_help.pack(padx=10, pady=10)


def show_context_menu(event):
    widget = event.widget
    context_menu.entryconfigure(
        "Вставить", command=lambda: widget.event_generate("<<Paste>>"))
    context_menu.entryconfigure(
        "Копировать", command=lambda: widget.event_generate("<<Copy>>"))
    context_menu.entryconfigure(
        "Вырезать", command=lambda: widget.event_generate("<<Cut>>"))
    context_menu.post(event.x_root, event.y_root)


def _input(entry):
    return entry.get()


def _sd(entry):
    global OutputPath
    OutputPath = filedialog.askdirectory()
    if OutputPath:
        entry.config(state='normal')
        entry.delete(0, tk.END)
        entry.insert(0, OutputPath)
    return OutputPath


def _print(par):
    text_info.config(state=tk.NORMAL)
    text_info.insert(tk.END, par + '\n')
    text_info.config(state=tk.DISABLED)
    text_info.see(tk.END)


def progress_function(stream, chunk, bytes_remaining):
    global last_percentage_reported
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100

    if int(percentage_of_completion) // 5 > last_percentage_reported // 5:
        last_percentage_reported = int(percentage_of_completion)
        _print(f'{last_percentage_reported} % loaded')


def start_download():
    global itag, streams_got

    url = _input(entry_adress)
    title = _input(entry_filename)
    OutputPath = entry_path.get()

    if not url or not title or not itag_to_search:
        _print("Ошибка: не все параметры введены.")
        return

    _print('Ожидание соединения...')

    try:
        _print('Поиск потока...')

        yt = YouTube(url, on_progress_callback=progress_function)
        streams_got = yt.streams
        itag = search(streams_dict[itag_to_search])

        if not itag:
            _print(
                'Указанный поток не доступен для данного видео, попробуйте выбрать другой')
            return

        yt.streams.get_by_itag(itag).download(
            output_path=OutputPath, filename=f'{title}.mp4')

        _print('Загрузка успешно завершена...')

    except Exception as e:
        _print(f"Проверьте правильность URL. {str(e)}")


def start_download_thread():
    threading.Thread(target=start_download).start()


context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Вставить")
context_menu.add_command(label="Копировать")
context_menu.add_command(label="Вырезать")


label_adress = tk.Label(root, text='1. Введите URL адрес видео:',
                        font=("Arial", 11, 'bold'), bg='#B0C4DE')
label_adress.place(x=20, y=5)

entry_adress = tk.Entry(root, width=60, font=("Arial", 12, 'italic'))
entry_adress.bind("<Button-3>", show_context_menu)
entry_adress.place(x=20, y=30)

button_download = tk.Button(root, text='Скачать', font=(
    "Arial", 12), bg='#00FA9A', command=start_download_thread, width=7, height=2)
button_download.place(x=485, y=130)

button_help = tk.Button(root, text='?', font=(
    "Arial", 11), bg='#B0C4DE', command=show_help_window, width=7, height=1)
button_help.place(x=485, y=215)

button_clear = tk.Button(root, text='Очистить', font=(
    "Arial", 11), bg='#B0C4DE', command=clear, width=7, height=1)
button_clear.place(x=485, y=245)

label_ch_folder = tk.Label(
    root, text='2. Выберите папку для скачивания:', font=("Arial", 11, 'bold'), bg='#B0C4DE')
label_ch_folder.place(x=20, y=55)

entry_path = tk.Entry(root, width=31, font=("Arial", 12, 'italic'))
entry_path.insert(0, r"C:\Users\user\Desktop")
entry_path.bind("<Button-3>", show_context_menu)
entry_path.place(x=20, y=80)

button_ch_folder = tk.Button(root, text=' Обзор ', font=(
    "Arial", 11), bg='#B0C4DE', command=lambda: _sd(entry_path), width=7, height=1)
button_ch_folder.place(x=315, y=75)

label_filename = tk.Label(root, text='3. Сохранить как:',
                          font=("Arial", 11, 'bold'), bg='#B0C4DE')
label_filename.place(x=400, y=55)

label2_filename = tk.Label(root, text='.MP4',
                           font=("Arial", 11, 'bold'), bg='#B0C4DE')
label2_filename.place(x=525, y=80)


entry_filename = tk.Entry(root, width=13, font=("Arial", 12, 'italic'))
entry_filename.bind("<Button-3>", show_context_menu)
entry_filename.place(x=400, y=80)

label_info = tk.Label(root, text='Статус:',
                      font=("Arial", 11, 'bold'), bg='#B0C4DE')
label_info.place(x=165, y=105)

text_info = tk.Text(root, wrap='word', height=9, width=38, state=tk.DISABLED)
text_info.place(x=165, y=130)

label_listbox = tk.Label(root, text='4. Выбрать поток:',
                         font=("Arial", 11, 'bold'), bg='#B0C4DE')
label_listbox.place(x=20, y=105)

listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=16,
                     height=8, font=("Arial", 11))
listbox.place(x=20, y=130)

listbox.bind('<<ListboxSelect>>', on_select)

for item in items.keys():
    listbox.insert(tk.END, item)

root.mainloop()
