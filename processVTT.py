#!/usr/bin/env python3
import sys
import os
import difflib
import webvtt

def timestamp_to_seconds(ts):
    """Преобразует временную метку 'HH:MM:SS.mmm' в число секунд (float)."""
    h, m, s = ts.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def merge_segments(segments):
    """
    Последовательно объединяет сегменты, используя difflib для обнаружения совпадающих блоков.
    Если в конце уже объединённого текста (в токенах) и начале нового сегмента находится общий блок,
    то дублирующая часть не добавляется.
    """
    # Начинаем со слов первого сегмента
    merged_tokens = segments[0].text.strip().split()
    for seg in segments[1:]:
        new_tokens = seg.text.strip().split()
        if not new_tokens:
            continue

        # Используем SequenceMatcher для нахождения совпадения между концом merged_tokens и началом new_tokens
        matcher = difflib.SequenceMatcher(None, merged_tokens, new_tokens)
        overlap = 0
        for i, j, n in matcher.get_matching_blocks():
            # Ищем совпадение, которое начинается в new_tokens с нулевого индекса
            # и совпадает с окончанием merged_tokens
            if j == 0 and i + n == len(merged_tokens):
                overlap = n
        # Добавляем в результат только те слова из нового сегмента, которые не повторяются
        merged_tokens.extend(new_tokens[overlap:])
    return " ".join(merged_tokens)

def merge_vtt_file(input_filename):
    """
    Читает VTT-файл, сортирует сегменты по времени начала,
    и объединяет их последовательно с вырезанием повторов.
    """
    segments = list(webvtt.read(input_filename))
    # Сортируем сегменты по времени начала
    segments.sort(key=lambda seg: timestamp_to_seconds(seg.start))

    if not segments:
        return ""

    merged_text = merge_segments(segments)
    return merged_text

def main():
    if len(sys.argv) < 2:
        print("Использование: python merge_vtt.py <input.vtt> [output.txt]")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(input_filename)[0] + ".txt"

    merged_text = merge_vtt_file(input_filename)

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(merged_text)

    print(f"Сохранён файл: {output_filename}")

if __name__ == "__main__":
    main()
