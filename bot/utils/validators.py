# bot/utils/validators.py

import re
import ipaddress
from urllib.parse import urlparse
import logging

logger = logging.getLogger('prehensor')

_ipv4_pattern = re.compile(r'^\d+\.\d+\.\d+\.\d+$')

def is_http_url(url: str) -> bool:
    parsed = urlparse(url)
    # Проверяем ссылку на протокол
    if parsed.scheme not in ("http", "https"):
        logger.warning(f'http-валидатор: False. У ссылки нет http или https, URL={url}')
        return False

    # Проверяем на localhost
    host = parsed.hostname
    if not host or host.lower() == "localhost":
        logger.warning(f'http-валидатор: False. Домен не указан, или ссылка на localhost, URL={url}')
        return False

    # Если похоже на IPv4 (только цифры и точки) — валидность проверяем только через ipaddress
    if _ipv4_pattern.match(host):
        try:
            ipaddress.IPv4Address(host)
            logger.debug(f'http-валидатор: True. Валидный ip-адрес, URL={url}')
            return True
        except ipaddress.AddressValueError:
            logger.warning(f'http-валидатор: False. Не валидный IP-адрес, URL={url}')
            return False

    # Иначе считаем это доменом
    logger.debug(f'http-валидатор: True. Валидный адрес, URL={url}')
    return True
