# bot/utils/reporter.py

import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

from bot.config.constants import (
    DEBUG_LOG,
    ERRORS_LOG,
    LOG_MSG_FMT,
    LOG_DATEFMT,
    LOG_MAXSIZE,
    LOG_BACKUPCOUNT,
)

def _make_formatter() -> logging.Formatter:
    '''Возвращаем общий формат для хендлеров.'''
    return logging.Formatter(
        LOG_MSG_FMT,
        datefmt=LOG_DATEFMT
    )

def set_logger(name: str = 'prehensor') -> logging.Logger:
    """
    Настройка основного логгера.
    Вызывается в начале каждого модуля.
    """
    logger = logging.getLogger(name)
    if logger.level != logging.DEBUG:
        logger.setLevel(logging.DEBUG)
    return logger



def add_console_handler(logger: logging.Logger) -> None:
    '''
    Добавляем консольный хендлер.
    Повторный вызов игнорируется.
    '''
    # Проверяем повторный вызов
    if any(h.name == "console" for h in logger.handlers):
        return
    console = logging.StreamHandler()
    console.name = "console"
    # Консольный хендлер в уровень INFO
    console.setLevel(logging.INFO)
    console.setFormatter(_make_formatter())
    logger.addHandler(console)

def add_file_handlers(logger: logging.Logger, log_dir: str) -> None:
    """
    После успешной загрузки .env — добавляем файловые хендлеры:
    prehensor_bot_debug.log - для отладочных сообщений;
    prehensor_bot_error.log - для ошибок.
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    fmt = _make_formatter()

    # Перебираем настройки для хендлеров
    for level, fname, hname in (
        (logging.DEBUG, DEBUG_LOG, "debug_file"),
        (logging.ERROR, ERRORS_LOG, "error_file"),
    ):
        # Проверяем, вдруг уже есть
        if any(h.name == hname for h in logger.handlers):
            continue
        # Нету. Настраиваем
        handler = RotatingFileHandler(
            filename=log_path / fname,
            maxBytes=LOG_MAXSIZE,
            backupCount=LOG_BACKUPCOUNT
        )
        handler.name = hname
        handler.setLevel(level)
        handler.setFormatter(fmt)
        # Вуаля
        logger.addHandler(handler)
