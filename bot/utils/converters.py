# bot/utils/converters.py

from bot.utils.format import format_duration

def media_data_to_string(media_info: dict, details: bool = False) -> str:
    '''
    Функция принимает словарь с данными о медиа-файле и возвращает связный текст.
    details = False - коротко,
    details = True - подробно.
    '''

    if media_info is None:
        return None

    title = media_info.get('title', 'Без заголовка')
    description = media_info.get('description', '')
    uploader = media_info.get('uploader', None)

    # Если автор указан, он добавляется к заголовку
    result = title + f' * {uploader}\n' if uploader else '\n'
    result += '-' * 30
    result += f'\n{description}\n'

    if details:
        duration = media_info.get('duration', None)
        formatted_duration = format_duration(duration) if duration else 'Не указана'
        result += f'Длительность: {formatted_duration}\n'

        view_count = media_info.get('view_count', None) # Просмотры
        like_count = media_info.get('like_count', None) # лайков
        dislike_count = media_info.get('dislike_count', None) # дизлайков
        repost_count = media_info.get('repost_count', None) # репостов

        view_statistic = []
        
        if view_count is not None:
            view_statistic.append(f'Просмотров: {view_count}')
        if like_count is not None:
            view_statistic.append(f'Лайков: {like_count}')
        if dislike_count is not None:
            view_statistic.append(f'Дизлайков: {dislike_count}')
        if repost_count is not None:
            view_statistic.append(f'Репостов: {repost_count}')
        
        result += ', '.join(view_statistic) + ".\n"

    return result
