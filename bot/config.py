# bot/config.py
import logging
logger = logging.getLogger('prehensor')

import os
from pathlib import Path
from dotenv import load_dotenv

# Константные значения по умолчанию
CODEC_TITLE_DEFAULT = 'MPEG Audio Layer III (mp3)'
CODEC_VALUE_DEFAULT = 'mp3'
QUALITY_DEFAULT = '128'

FORMAT_RESULT_DEFAULT = 'bestaudio/best'
POSTPROCESSORS_KEY_DEFAULT = 'FFmpegExtractAudio'
TEMP_DIR = 'temp'

def init_env() -> bool:
    """
    1) Если файл /etc/prehensor_bot/.env существует — грузим его.
    2) Иначе — грузим .env из текущей рабочей директории (локально).
    Результат возвращаем.
    """
    # путь на сервере
    etc_env = Path('/etc/prehensor_bot/.env')
    if etc_env.is_file():
        result = load_dotenv(dotenv_path=etc_env)
        logger.info(f'Загружаем окружение из {etc_env}')
    else:
        # Ищем .env локально
        result = load_dotenv()  
        logger.info('Загружаем окружение из .env в текущей директории.')
    return result

# Системные настройки
class SystemSettings:
    def __init__(self):
        # Токен нужно сохранить в файл .env в формате:
        # TG_TOKEN=<токен_бота>
        # LOG_DIR=<путь_к_логам>

        # Загружаем переменные окружения из .env-файла
        if not init_env():
            raise FileNotFoundError('.env not found.')
        self.tg_token = os.environ.get('TG_TOKEN')
        # Если возникла проблема при десериализации токена
        if not self.tg_token:
            raise ValueError("TG_TOKEN is missing in .env file")
        # Формируем путь к логам, если не считался из переменной окружения
        default_logs = Path(__file__).parent.parent / 'logs'
        log_dir = os.environ.get('LOG_DIR', str(default_logs))
        if not Path(log_dir).is_dir:
            log_dir = default_logs
        self.log_dir = log_dir
        # Формируем путь к временному файлу: в папке temp уровнем выше,
        # Вместо ~user_id~ нужно поставить id пользователя чат-бота
        tmp = Path(__file__).parent.parent / TEMP_DIR
        self.outtmpl = str(
            tmp /
            f'media_~user_id~_%(id)s.%(ext)s'
        )
        self.cache_dir = str(
            tmp / 'chache')

        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            logger.debug(f'Создали каталог для кэша: {self.cache_dir}')
        except Exception:
            logger.error(f'Ошибка при создании каталога для кэша: {self.cache_dir}', exc_info=True)

# Пользовательские настройки
class UserSettings:
    def __init__(self):
        # Инициируем значения по умолчанию
        self.set_default()
    
    # Устанавливаем все значения по умолчанию
    def set_default(self):
        self.codec_title = CODEC_TITLE_DEFAULT
        self.codec_value = CODEC_VALUE_DEFAULT
        self.quality = QUALITY_DEFAULT
        # Шаг обновления информации о грогрессе загрузки через каждые 2 мегабайта
        self.progress_step = 2*1024*1024
    
# Все настройки
class Settings:
    def __init__(self):
        # Инициализируем системные настройки
        self.system = SystemSettings()
        
        # Инициализируем настройки по умолчанию
        self.set_default()
    
    # Устанавливаем настройки по умолчанию
    def set_default(self) -> None:
        self.format_result = FORMAT_RESULT_DEFAULT
        self.postprocessors_key = POSTPROCESSORS_KEY_DEFAULT

        # Текстовые сообщения
        self.msg_command_or_link = 'Нужно прислать или команду, или ссылку на медиа.'
        self.msg_check_link = 'Проверяю что по ссылке.'
        self.msg_no_media_info = 'Нет информации о медиа.'
        self.msg_start_downloading = 'Загружаю!'
        self.msg_progress_percent = 'загружено.'
        self.msg_download_progress = 'Загружено '
        self.msg_download_completed = 'загружено.'
        self.msg_send_file = 'Отправляю файл в чат.'
        self.msg_no_link = 'Нет ссылки на медиа.'
        
        # Тексты ошибок
        self.error = 'Ошибка:'
        self.err_file_not_found = f'{self.error} файл для отправки не существует.'
        self.err_path_is_empty = f'{self.error} пустой путь к загруженному файлу.'
        self.err_no_download_info = f'{self.error} нет информации о загруженном файле.'
        self.err_download_failed = 'Не удалось загрузить медиа-файл.'
        self.err_sending_failed = 'Не получилось отправить файл в чат.'

        self.msg_start_text = 'привет! Я бот-выцеплятор. Мне можно дать ссылку, по которой я скачаю медиа-файл.'
        self.msg_help_text = f'''
Бот для загрузки медиафайлов по вашим ссылкам.

        * Команды бота *
/start      Стартовать бот или сбросить все настройки.
/help       Этот текст.
<ссылка>    Получить краткую информацию о медиа по ссылке. При этом ссылка сохраняется в контексте бота.
/info       Подробная информация о медиа. Если ссылку не указать, то она будет взята из контекста бота.
/download   Загрузка медиа. Если ссылку не указать, то она будет взята из контекста бота.

----------------------------------------------------------------

Для загрузки медиа используется библиотека yt_dlp.
Поддерживаются: YouTube, VK, Odnoklassniki, Instagram, TikTok, Twitter, Rutube, SoundCloud, Dailymotion, Twitch, Mail.ru, Yandex Music и ещё сотни разных аудио-видеосервисов.
Полный список по ссылке: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
'''