# bot/services/reporter.py
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

def set_console_logger(name: str = 'prehensor') -> logging.Logger:
    """
    Настройка консольного логгирования на уровне DEBUG.
    Вызывается до загрузки .env и логирования в файл.
    """
    logger = logging.getLogger(name)
    if any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        return logger

    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        '%(asctime)s %(message)s',
        datefmt='%H:%M:%S'
    )
    console.setFormatter(fmt)
    logger.addHandler(console)
    return logger

def add_file_handler(logger: logging.Logger, log_dir: str) -> None:
    """
    После успешной загрузки .env — добавляем файловый хендлер.
    """
    # не добавляем, если уже есть RotatingFileHandler с таким файлом
    for h in logger.handlers:
        if isinstance(h, RotatingFileHandler) and h.baseFilename.endswith('app.log'):
            return
    # создаём папку, если надо
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)

    file_path = path / 'prehensor.log'
    file_rot = RotatingFileHandler(
        filename=str(file_path),
        maxBytes=1_000_000,
        backupCount=5
    )
    file_rot.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        '%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_rot.setFormatter(fmt)
    logger.addHandler(file_rot)

