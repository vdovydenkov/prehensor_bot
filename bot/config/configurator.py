# bot/config/configurator.py

from bot.config.constants import YAML_SETTINGS

import logging
logger = logging.getLogger('prehensor')

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel
import yaml

from bot.config.defaults import DEFAULT_RAW_CONFIG
from bot.config.constants import ETC_ENV_PATH, LOCAL_ENV_PATH
from bot.config.models import YAMLSettings

# Загрузка .env для токена
def init_env() -> bool:
    """
    1) Если файл /etc/prehensor_bot/.env существует — грузим его.
    2) Иначе — грузим .env из текущей рабочей директории (локально).
    Результат возвращаем.
    """
    if ETC_ENV_PATH.is_file():
        logger.info(f'Загружаем .env из {ETC_ENV_PATH}')
        return load_dotenv(ETC_ENV_PATH.as_posix())

    if LOCAL_ENV_PATH.is_file():
        logger.info(f'Файл в /etc не найден, загружаем .env из {LOCAL_ENV_PATH}')
        return load_dotenv(LOCAL_ENV_PATH.as_posix())

    logger.critical(f'Файл .env не найден ни в {ETC_ENV_PATH}, ни в {LOCAL_ENV_PATH}')
    return False

def save_yaml_config(config: YAMLSettings, path: Path = None) -> None:
    '''
    Сохраняет переданный объект конфигурации YAMLSettings в YAML-файл.
    Если путь не указан — сохраняет рядом с текущим модулем.
    '''
    if not isinstance(config, YAMLSettings):
        logger.warning('Для сохранения конфигурации передали не YAMLSettings, сохранить не получится.')
        return
    path = path or (Path(__file__).parent / YAML_SETTINGS)

    # Преобразуем в словарь через pydantic, чтобы получить корректную структуру
    raw_dict = config.model_dump()

    try:
        # Создаём родительские каталоги, если их нет
        path.parent.mkdir(parents=True, exist_ok=True)

        # Записываем в файл с юникод-поддержкой и читаемым форматированием
        with path.open("w", encoding="utf-8") as f:
            yaml.dump(raw_dict, f, allow_unicode=True, sort_keys=False)

        logger.info(f"Дефолтные настройки успешно сохранены в файл: {path}")
    except Exception:
        logger.error(f"Не удалось сохранить дефолтные настройки в файл: {path}", exc_info=True)

def load_yaml_config(path: Path = None) -> YAMLSettings:
    '''
    Загрузка настроек из YAML или дефолтов
    '''
    path = path or (Path(__file__).parent / YAML_SETTINGS)
    if path.is_file():
        logger.info(f'Файл конфигурации {path} найден.')
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
    else:
        logger.info(f"{path} не нашли, используем встроенные дефолтные настройки.")
        raw = DEFAULT_RAW_CONFIG
        save_yaml_config(YAMLSettings.model_validate(raw), path)
    return YAMLSettings.model_validate(raw)

# Основной класс настроек
class Cfg:
    def __init__(self):
        if not init_env():
            logger.critical('Нет .env, нет токена. Выгружаюсь!')
            exit(1)
        self.tg_token = os.environ.get("TG_TOKEN")
        if not self.tg_token:
            logger.critical('.env считался, но токен отсутствует. Выгружаюсь!')
            exit(1)
        # Загружаем YAML-конфиг
        cfg = load_yaml_config()
        self.user = cfg.user_defaults
        self.sys = cfg.sys
        self.ydl = cfg.ydl
        self.msg = cfg.msg
        self.err = cfg.err

        # Готовим каталоги
        self.log_dir = self._ensure_dir(self.sys.log_dir)
        self.temp_dir = self._ensure_dir(self.sys.temp_dir)
        tmp = Path(__file__).parent.parent.parent / self.sys.temp_dir
        self.cache_dir = self._ensure_dir(tmp / 'cache')
        # ~user_id~ позже заменим на id пользователя
        self.outtmpl = str(tmp / "media_~user_id~_%(id)s.%(ext)s")

    @staticmethod
    def _ensure_dir(path: Path) -> str:
        if not path.is_dir():
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Создан каталог: {path}")
            except Exception:
                logger.warning(f"Не создан каталог: {path}")
        return str(path.resolve())
