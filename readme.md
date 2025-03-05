 
# Subtitle Downloader and Processor

Это десктоп приложение на Python, которое загружает субтитры по ссылке на видео и обрабатывает их. Программа использует два модуля:
- **subs.py** — для загрузки субтитров с использованием [yt_dlp](https://github.com/yt-dlp/yt-dlp) и [requests](https://pypi.org/project/requests/).
- **processVTT.py** — для обработки VTT файлов (слияние сегментов с устранением повторов) с помощью [webvtt-py](https://pypi.org/project/webvtt-py/).

Приложение имеет графический интерфейс, созданный на базе Tkinter, позволяющий вводить ссылку, загружать и обрабатывать субтитры, а затем просматривать результат.

## Особенности

- Ввод ссылки на видео через GUI.
- Загрузка ручных и автоматически сгенерированных субтитров.
- Обработка VTT файлов (объединение сегментов с устранением дублирования).
- Просмотр обработанных субтитров в окне приложения.

## Требования

- **Python 3.6+**
- Установленные библиотеки:
  - `yt_dlp`
  - `webvtt-py`
  - `requests`
- Tkinter (обычно входит в стандартную поставку Python)

### Установка зависимостей

Откройте терминал и выполните команду:

```bash
pip install yt_dlp webvtt-py requests

### Запуск проекта

Чтобы запустить проект в режиме разработки, выполните:

```bash
python main.py


После этого откроется окно приложения, где вы сможете:

- Ввести ссылку на видео.
- Нажать кнопку для загрузки и обработки субтитров.
- Выбрать обработанный файл из списка и открыть его для просмотра.

### Сборка исполняемого файла для Windows

Приложение можно собрать в один исполняемый файл (.exe) с помощью PyInstaller.

### Важно про кросс-компиляцию

PyInstaller не поддерживает прямую кросс-компиляцию. Это означает, что если вы собираете проект на Linux, то по умолчанию получите Linux-исполняемый файл. Чтобы создать Windows .exe, можно:

- Собрать проект на машине с Windows.
- Использовать Wine на Linux для сборки Windows-версии.

### Сборка на Windows
1. Установите Python для Windows.
Убедитесь, что Python добавлен в PATH.

2. Установите зависимости:

```bash
pip install yt_dlp webvtt-py requests```

3. Установите PyInstaller:

```bash
pip install pyinstaller```

4. Соберите приложение:

Перейдите в каталог с файлом `main.py` и выполните:

```bash
pyinstaller --onefile --windowed main.py```


После завершения сборки в папке dist появится файл main.exe. Этот файл можно переносить и запускать на компьютерах с Windows.

### Структура проекта
- `main.py` — основное приложение с графическим интерфейсом.
- `subs.py` — модуль для загрузки субтитров.
- `processVTT.py` — модуль для обработки VTT файлов.

