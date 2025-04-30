import os
from pathlib import Path
from dotenv import load_dotenv

# Константные значения по умолчанию
DEBUG_MODE = True
CODEC_TITLE_DEFAULT = 'MPEG Audio Layer III (mp3)'
CODEC_VALUE_DEFAULT = 'mp3'
QUALITY_DEFAULT = '128'

FORMAT_RESULT_DEFAULT = 'bestaudio/best'
POSTPROCESSORS_KEY_DEFAULT = 'FFmpegExtractAudio'

def init_env() -> bool:
    """
    1) Если файл /etc/audio_prehensor_bot/.env существует — грузим его.
    2) Иначе — грузим .env из текущей рабочей директории (локально).
    Результат возвращаем.
    """

    # путь на сервере
    etc_env = Path('/etc/audio_prehensor_bot/.env')

    if etc_env.is_file():
        result = load_dotenv(dotenv_path=etc_env)
        print(f'Загружаем окружение из {etc_env}')
    else:
        # Ищем .env локально
        result = load_dotenv()  
        print('Загружаем окружение из .env в текущей директории.')

    return result

# Системные настройки
class SystemSettings:
    def __init__(self):
        # Токен нужно сохранить в файл .env в формате:
        # TG_TOKEN=

        # Загружаем переменные окружения из .env-файла
        dotenv_loaded = init_env()
        # Если возникла проблема при чтении
        if not dotenv_loaded:
            raise FileNotFoundError('.env not found.')

        self.tg_token = os.environ.get('TG_TOKEN', None)
        # Если возникла проблема при десериализации
        if not self.tg_token:
            raise ValueError("TG_TOKEN is missing in .env file")

        self.debug_mode = DEBUG_MODE
        # Шаг обновления информации о грогрессе загрузки через каждый мегабайт
        self.progress_step = 1024*1024
        return
        # __init__

# Пользовательские настройки
class UserSettings:
    def __init__(self):
        # Инициируем значения по умолчанию
        self.set_default()
        return
        # __init__
    
    # Устанавливаем все значения по умолчанию
    def set_default(self):
        self.codec_title = CODEC_TITLE_DEFAULT
        self.codec_value = CODEC_VALUE_DEFAULT
        self.quality = QUALITY_DEFAULT
        return
        # set_default
    
    def __str__(self) -> str:
        return f"Codec Title: {self.codec_title}, Codec Value: {self.codec_value}, Quality: {self.quality}"

# Все настройки
class Settings:
    def __init__(self):
        # Инициализируем системные настройки
        self.system = SystemSettings()
        
        # Инициализируем настройки по умолчанию
        self.set_default()
        return
        # __init__
    
    # Устанавливаем настройки по умолчанию
    def set_default(self) -> None:
        self.format_result = FORMAT_RESULT_DEFAULT
        self.postprocessors_key = POSTPROCESSORS_KEY_DEFAULT
        # Формируем путь к временному файлу: в папке temp уровнем выше,
        # Вместо ~user_id~ нужно поставить id пользователя чат-бота
        self.outtmpl = outtmpl = str(
            Path(__file__).parent.parent / 'temp' /
            f'media_~user_id~_%(id)s.%(ext)s'
        )

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

        return
        # set_default

    def __str__(self) -> str:
        return f"Format Result: {self.format_result}, Postprocessors Key: {self.postprocessors_key}, audio_filename: {self.audio_filename}"

