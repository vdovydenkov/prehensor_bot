# bot/utils/validators.py

import re

def is_http_url(string: str) -> bool:
    '''
    Функция проверяет, является ли строка HTTP/HTTPS ссылкой.
    '''

    # Проверяем что передали
    if not isinstance(string, str):
        return False

    regex = re.compile(
        r'^(?:http)s?://' # схема http или https
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # доменное имя
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # или IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # или IPv6
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, string) is not None and 'localhost' not in string and ':' not in string.split('/')[2]
