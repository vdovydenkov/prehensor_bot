from pydantic import BaseModel
from pathlib import Path

# Модели Pydantic
class UserDefaults(BaseModel):
    codec_title:   str  # Полное название кодека
    codec_value:   str  # Короткое название
    quality:       int  # Битрейт
    progress_step: int  # Шаг обновления линейки прогресса (в байтах)

class SysSettings(BaseModel):
    log_dir:  Path
    temp_dir: Path

class YDLSettings(BaseModel):
    format_result:      str
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
    prefix:               str
    file_not_found:       str
    path_is_empty:        str
    no_download_info:     str
    download_failed:      str
    sending_failed:       str
    bot_conflict:         str
    network_error:        str
    invalid_token:        str
    other_telegram_error: str

class YAMLSettings(BaseModel):
    user_defaults: UserDefaults
    sys: SysSettings
    ydl: YDLSettings
    msg: MsgSettings
    err: ErrSettings

