import os
import types
import yt_dlp

# Принимает настройки и ссылку, возвращает словарь с результирующей информацией
def get_media_from_url(url: str, options: dict, enable_downloading: bool = False) -> dict:
    '''
    Функция загружает медиа-контент по ссылке.
    
    Параметр 1: URL на медиа
    Параметр 2: словарь с настройками
    Параметр 3: загружать ли медиа-файл

    Возвращает словарь с информацией о загрузке и постобработке.
    '''

    # Грузим параметры, готовимся к загрузке и постобработке
    with yt_dlp.YoutubeDL(options) as ydl:
        # Загружаем, сохраняя информацию в словарь
        extracted_info = ydl.extract_info(url, download=enable_downloading)
    
    # Берем путь к файлу с результатом
    result_path = ydl.prepare_filename(extracted_info)
    # Добавляем его как дополнительный ключ в словарь
    extracted_info['result_path'] = result_path

    return extracted_info
    # get_media_from_url