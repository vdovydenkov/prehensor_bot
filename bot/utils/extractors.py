# bot/utils/extractors.py
from typing import Dict

def get_path(
        media_info: Dict
    ) -> str | None:
    '''
    Принимает параметром словарь с информацией о медиафайле,
    ищет requested_downloads / filepath
    возвращает путь к файлу или None.
    '''
    downloads = media_info.get('requested_downloads')
    if isinstance(downloads, list) and downloads:
        first = downloads[0]
        if isinstance(first, dict):
            return first.get('filepath')
    return None
