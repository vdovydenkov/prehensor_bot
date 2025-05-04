# bot/services/reporter.py
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

DEBUG_LOG = 'prehensor_bot_debug.log'
ERRORS_LOG = 'prehensor_bot_errors.log'

def set_console_logger(name: str = 'prehensor') -> logging.Logger:
    """
    Настройка консольного логгирования на уровне INFO.
    Вызывается до загрузки .env и логирования в файл.
    """
    logger = logging.getLogger(name)
    if any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        return logger

    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    fmt = logging.Formatter(
        '%(asctime)s %(message)s',
        datefmt='%H:%M:%S'
    )
    console.setFormatter(fmt)
    logger.addHandler(console)
    return logger

def add_file_handlers(logger: logging.Logger, log_dir: str) -> None:
    """
    После успешной загрузки .env — добавляем файловые хендлеры:
    prehensor_bot_debug.log - для отладочных сообщений;
    prehensor_bot_error.log - для ошибок.
    """
    # не добавляем, если уже есть RotatingFileHandler с таким файлом
    for h in logger.handlers:
        if isinstance(h, RotatingFileHandler) \
           and (h.baseFilename.endswith(DEBUG_LOG) \
           or h.baseFilename.endswith(ERRORS_LOG)):
            return
    # создаём папку, если надо
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)

    fmt = logging.Formatter(
        '%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Сначала отладочный лог
    file_path = path / DEBUG_LOG
    file_rot = RotatingFileHandler(
        filename=str(file_path),
        maxBytes=1_000_000,
        backupCount=2
    )
    file_rot.setLevel(logging.DEBUG)
    file_rot.setFormatter(fmt)
    logger.addHandler(file_rot)
    # Теперь лог с ошибками
    file_path = path / ERRORS_LOG
    file_rot = RotatingFileHandler(
        filename=str(file_path),
        maxBytes=1_000_000,
        backupCount=2
    )
    file_rot.setLevel(logging.ERROR)
    file_rot.setFormatter(fmt)
    logger.addHandler(file_rot)
