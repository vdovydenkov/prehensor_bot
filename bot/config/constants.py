# bot\config\constants.py

from pathlib import Path

# Пути к .env
ETC_ENV_PATH = Path('/etc/prehensor_bot/.env')
LOCAL_ENV_PATH = Path(__file__).resolve().parent.parent.parent / '.env'

# Константы логгера
DEBUG_LOG       = 'prehensor_bot_debug.log'
ERRORS_LOG      = 'prehensor_bot_errors.log'
LOG_MSG_FMT     = '%(asctime)s %(message)s'
LOG_DATEFMT     = '%H:%M:%S'
LOG_MAXSIZE     = 1_000_000
LOG_BACKUPCOUNT = 2

# Имена файлов
YAML_SETTINGS = 'settings.yaml'
