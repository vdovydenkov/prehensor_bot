import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.media_downloader import get_media_from_url
from bot.core.messenger import send_to_chat
from bot.config import UserSettings

def process_hook(data, context: ContextTypes.DEFAULT_TYPE, update: Update, event_loop: asyncio.AbstractEventLoop):
    # Берём настройки из контекста
    settings = context.bot_data['settings']

    async def send_progress(data):
        # Значение предыдущего прогресса загрузки
        last_progress_value = context.user_data.get('last_progress_value', 0)
        # Берём текущий статус
        status = data.get('status')
        downloaded = data.get('downloaded_bytes', 0)
        total = data.get('total_bytes', None)
        if status == 'downloading':
            # Есть ли информация об общем размере загружаемого медиа-файла
            if total:
                percent = f'{downloaded / total * 100:.0f}%'
                progress_message = f'{percent} {settings.msg_progress_percent}'
            else: # Если нет, показываем количество загруженных байт
                # Преобразуем информацию о загрузке в удобочитаемый вид
                download_info = format_bytes(downloaded)
                progress_message = f'{settings.msg_download_progress} {download_info}'
            # Выдаём сообщение о загрузке после преодоления заданного шага (количества мегабайт)
            if downloaded > last_progress_value + settings.system.progress_step:
                context.user_data['last_progress_value'] = downloaded
                await send_to_chat(update, context, progress_message)
        elif status == 'finished':
            # Переводим информацию о загрузке в удобочитаемый формат
            download_info = format_bytes(downloaded)
            progress_message = f'{download_info} {settings.msg_download_completed} {settings.msg_send_file}'
            await send_to_chat(update, context, progress_message)
        elif status == 'error':
            error = data.get('error')
            await send_to_chat(update, context, f'{settings.error} {error}')

    if event_loop:
        asyncio.run_coroutine_threadsafe(send_progress(data), event_loop)
    else:
        print("Ошибка: Не получен event loop")

async def fetch_url(url, update, context, download=False):
    settings = context.bot_data['settings']
    user_settings = context.user_data.get('user_settings', UserSettings())
    loop = asyncio.get_event_loop()

    ydl_options = {}
    if download:
        # id пользователя для имени временного файла
        user_id = update.effective_user.id
        # Заменяем шаблон на реальное значение
        outtmpl = settings.outtmpl.replace('~user_id~', str(user_id))
        # Заполняем настройками параметры загрузки и постобработки.
        ydl_options = {
            'format': settings.format_result,
            'postprocessors': [{
                'key': settings.postprocessors_key,
                'preferredcodec': user_settings.codec_value,
                'preferredquality': user_settings.quality,
            }],
            'outtmpl': outtmpl,
            'progress_hooks': [lambda data: process_hook(data, context, update, loop)],
        }

        # Информируем пользователя
        await send_to_chat(update, context, settings.msg_start_downloading)
    
    try:
        info = await asyncio.to_thread(get_media_from_url, url, ydl_options, download)
    except Exception as e:
        await send_to_chat(update, context, f"{settings.error} {e}")
        return None

    if not info:
        await send_to_chat(update, context, settings.err_no_download_info)
    return info
