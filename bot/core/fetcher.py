import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.config import UserSettings
from bot.services.media_downloader import get_media_from_url
from bot.utils.format import format_bytes

def process_hook(data, context: ContextTypes.DEFAULT_TYPE, update: Update, event_loop: asyncio.AbstractEventLoop):
    # Для отладки
    print(f"process_hook получил данные: {data}")

    # Берём настройки из контекста
    settings = context.bot_data['settings']

    async def send_progress(data):
        last_progress_value = context.user_data.get('last_progress_value', 0)
        status = data.get('status')
        downloaded = data.get('downloaded_bytes', 0)
        total = data.get('total_bytes', None)

        if status == 'downloading':
            if total:
                percent = f'{downloaded / total * 100:.0f}%'
                progress_message = f'{percent} {settings.msg_progress_percent}'
            else:
                download_info = format_bytes(downloaded)
                progress_message = f'{settings.msg_download_progress} {download_info}'

            # Контроль шага прогресса
            if downloaded > last_progress_value + settings.system.progress_step:
                context.user_data['last_progress_value'] = downloaded
                await send_to_chat(update, context, progress_message)

        elif status == 'finished':
            download_info = format_bytes(downloaded)
            progress_message = f'{download_info} {settings.msg_download_completed} {settings.msg_send_file}'
            await send_to_chat(update, context, progress_message)

        elif status == 'error':
            error = data.get('error')
            await send_to_chat(update, context, f'{settings.error} {error}')

    if event_loop and not event_loop.is_closed():
        asyncio.run_coroutine_threadsafe(send_progress(data), event_loop)
    else:
        print("Ошибка: Не получен или закрыт event loop")


async def fetch_url(url, update, context, download=False):
    settings = context.bot_data['settings']
    user_settings = context.user_data.get('user_settings', UserSettings())
    
    # Ключевой момент: получаем loop до вызова asyncio.to_thread
    event_loop = asyncio.get_running_loop()

    ydl_options = {}
    if download:
        user_id = update.effective_user.id
        outtmpl = settings.outtmpl.replace('~user_id~', str(user_id))

        ydl_options = {
            'format': settings.format_result,
            'postprocessors': [{
                'key': settings.postprocessors_key,
                'preferredcodec': user_settings.codec_value,
                'preferredquality': user_settings.quality,
            }],
            'outtmpl': outtmpl,
            'progress_hooks': [lambda data: process_hook(data, context, update, event_loop)],
        }

        await send_to_chat(update, context, settings.msg_start_downloading)

    try:
        # get_media_from_url вызывается в потоке, loop передан заранее
        info = await asyncio.to_thread(get_media_from_url, url, ydl_options, download)
    except Exception as e:
        await send_to_chat(update, context, f"{settings.error} {e}")
        return None

    if not info:
        await send_to_chat(update, context, settings.err_no_download_info)
    return info


