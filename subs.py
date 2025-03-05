#!/usr/bin/env python3
import yt_dlp
import requests
import os

def download_all_subtitles(url, output_dir="subtitles"):
    # Опции для yt_dlp: получаем данные о субтитрах, не скачивая само видео
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    os.makedirs(output_dir, exist_ok=True)
    downloaded_files = []

    # Заголовки для запроса субтитров (имитируем браузер)
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/113.0.0.0 Safari/537.36'),
        'Referer': url
    }

    # Функция для скачивания по URL субтитров
    def download_sub(sub_url, filename):
        response = requests.get(sub_url, headers=headers)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Скачан файл: {filename}")
            return True
        else:
            print(f"Ошибка загрузки субтитров для файла {filename}: HTTP {response.status_code}")
            return False

    # Скачивание ручных субтитров
    if 'subtitles' in info and info['subtitles']:
        for lang, subs in info['subtitles'].items():
            for idx, sub in enumerate(subs):
                sub_url = sub.get('url')
                if sub_url:
                    ext = sub.get('ext', 'vtt')
                    filename = os.path.join(output_dir, f"manual_{lang}_{idx}.{ext}")
                    if download_sub(sub_url, filename):
                        downloaded_files.append(filename)
    else:
        print("Ручные субтитры отсутствуют.")

    # Скачивание автоматически сгенерированных субтитров
    if 'automatic_captions' in info and info['automatic_captions']:
        for lang, subs in info['automatic_captions'].items():
            for idx, sub in enumerate(subs):
                sub_url = sub.get('url')
                if sub_url:
                    ext = sub.get('ext', 'vtt')
                    filename = os.path.join(output_dir, f"automatic_{lang}_{idx}.{ext}")
                    if download_sub(sub_url, filename):
                        downloaded_files.append(filename)
    else:
        print("Автоматические субтитры отсутствуют.")

    return downloaded_files

if __name__ == "__main__":
    video_url = input("Введите ссылку на видео VK: ")
    files = download_all_subtitles(video_url)
    if files:
        print("\nСубтитры сохранены в следующих файлах:")
        for f in files:
            print(" -", f)
    else:
        print("Субтитры не были загружены.")
