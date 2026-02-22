# bot/services/media_downloader.py
import logging
logger = logging.getLogger('prehensor')

import os
import types
import yt_dlp

def get_media_from_url(
        url: str,
        options: dict,
        enable_downloading: bool = False
    ) -> dict | None:
    '''
    Функция загружает медиа-контент по переданной ссылке.
    
    Параметр 1: URL на медиа
    Параметр 2: словарь с настройками
    Параметр 3: определяет загружать ли медиа-файл или только информацию

    Возвращает словарь с информацией о загрузке и постобработке
        или None, если информацию извлечь не получилось.
    '''
    # Грузим параметры, готовимся к загрузке и постобработке
    with yt_dlp.YoutubeDL(options) as ydl:
        # Загружаем, сохраняя информацию в словарь
        logger.info(
            f'Загружаем '
            '{ "медиа" if enable_downloading else "информацию" } '
            'по URL: {url}'
        )
        extracted_info = ydl.extract_info(
            url,
            download=enable_downloading
        )
        if not extracted_info:
            return None

        if extracted_info.get('_type') == 'playlist':
            raise ValueError('Playlist URLs are not supported')

        if enable_downloading:
            downloads = extracted_info.get('requested_downloads')
            if downloads:
                result_path = downloads[0].get('filepath')    
                logger.info(f'Загружен файл {result_path}')

    return extracted_info
