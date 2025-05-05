# bot/config.py
import logging
logger = logging.getLogger('prehensor')

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel
import yaml

from bot.defaults import DEFAULT_RAW_CONFIG

YAML_SETTINGS = 'settings.yaml'

# Загрузка .env для токена
def init_env() -> bool:
    """
    1) Если файл /etc/prehensor_bot/.env существует — грузим его.
    2) Иначе — грузим .env из текущей рабочей директории (локально).
    Результат возвращаем.
    """
    # путь на сервере
    etc_env = Path('/etc/prehensor_bot/.env')
    # путь на уровень выше скрипта
    local_env = Path(__file__).resolve().parent.parent / '.env'

    if etc_env.is_file():
        logger.info(f'Загружаем .env из {etc_env}')
        return load_dotenv(etc_env.as_posix())

    if local_env.is_file():
        logger.info(f'Файл в /etc не найден, загружаем .env из {local_env}')
        return load_dotenv(local_env.as_posix())

    logger.critical(f'Файл .env не найден ни в {etc_env}, ни в {local_env}')
    return False

# Модели Pydantic
class UserDefaults(BaseModel):
    codec_title: str
    codec_value: str
    quality: int
    progress_step: int  # в байтах

class SysSettings(BaseModel):
    log_dir: Path
    temp_dir: Path

class YDLSettings(BaseModel):
    format_result: str
    postprocessors_key: str

class MsgSettings(BaseModel):
    command_or_link: str
    check_link: str
    no_media_info: str
    start_downloading: str
    progress_percent: str
    download_progress: str
    download_completed: str
    send_file: str
    no_link: str
    start_text: str
    help_text: str

class ErrSettings(BaseModel):
    prefix: str
    file_not_found: str
    path_is_empty: str
    no_download_info: str
    download_failed: str
    sending_failed: str

class YAMLSettings(BaseModel):
    user_defaults: UserDefaults
    sys: SysSettings
    ydl: YDLSettings
    msg: MsgSettings
    err: ErrSettings

# Загрузка настроек из YAML или дефолтов
def load_yaml_config(path: Path = None) -> YAMLSettings:
    path = path or (Path(__file__).parent.parent / YAML_SETTINGS)
    try:
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        logger.info(f"Настройки загружены из {path}")
    except Exception:
        logger.warning(f"{path} не загружен, используем встроенные дефолтные настройки.")
        logger.debug(f'Настройки из {path} не загрузились.', exc_info=True)
        raw = DEFAULT_RAW_CONFIG
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
        tmp = Path(__file__).parent.parent / self.sys.temp_dir
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
