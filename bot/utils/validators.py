import re
import ipaddress
from urllib.parse import urlparse
import logging
logger = logging.getLogger('prehensor')

regex = re.compile(
    r'^(?:http)s?://'  # http:// или https://
    r'[^/\s]+',        # хост до первого слэша или пробела
    re.IGNORECASE
)

def is_http_url(url: str) -> bool:
    '''
    Функция проверяет, является ли строка HTTP/HTTPS корректной ссылкой.
    '''

    # Проверяем что передали строку
    if not isinstance(url, str):
        logger.debug(f'В http-валидатор передали не строку. {url}, типа {type(url)}')
        return False

    if not regex.match(url):
        logger.debug(f'В http-валидаторе ссылка не прошла проверку regex:\nURL: {url}\nRegex: {regex}')
        return False
    # Пытаемся преобразовать строку в http-адрес
    try:
        parsed = urlparse(url)
        host = parsed.hostname
        if host is None:
            logger.debug(f'В http-валидатор передали ссылку без хоста: {url}')
            return False
        if host.lower() == "localhost":
            logger.debug(f'В http-валидатор передали ссылку на localhost: {url}')
            return False
        try:
            ip = ipaddress.ip_address(host)
            if ip.version == 4:
                return True  # корректный IPv4
            elif ip.version == 6:
                return True  # корректный IPv6
        except ValueError:
            return True  # не IP, значит домен — тоже подходит
    except Exception:
        logger.debug(f'В http-валидатор передали не ссылку: {url}')
        return False
