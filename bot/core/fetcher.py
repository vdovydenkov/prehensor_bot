# bot/core/fetcher
import logging
logger = logging.getLogger('prehensor')

import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.config import UserSettings
from bot.core.messenger import send_to_chat
from bot.services.media_downloader import get_media_from_url
from bot.utils.format import format_bytes

def process_hook(data, context: ContextTypes.DEFAULT_TYPE, update: Update, event_loop: asyncio.AbstractEventLoop):
    username = update.effective_user.first_name or 'Anonym'
    logger.debug(f'[{username}] process_hook получил данные:\n{data}')
    settings = context.bot_data['settings']

    async def send_progress(data):
        status = data.get('status')
        downloaded = data.get('downloaded_bytes', 0)
        total = data.get('total_bytes')
        if status == 'downloading':
            if total:
                percent = f'{downloaded / total * 100:.0f}%'
                progress = f'{percent} {settings.msg_progress_percent}'
            else:
                download_info = format_bytes(downloaded)
                progress = f'{settings.msg_download_progress} {download_info}'
            # Если прогресс преодолел заданный шаг — отправляем сообщение
            last_progress_value = context.user_data.get('last_progress_value', 0)
            step = settings.user.progress_step
            if downloaded > last_progress_value + step:
                logger.debug(f'[{username}] Прогресс преодолел шаг {step} байт, строка готова: {progress}')
                context.user_data['last_progress_value'] = downloaded
                await send_to_chat(update, context, progress)
        elif status == 'finished':
            download_info = format_bytes(downloaded)
            progress = f'{download_info} {settings.msg_download_completed} {settings.msg_send_file}'
            logger.debug(f'[{username}] Статус=finished')
            await send_to_chat(update, context, progress)
        elif status == 'error':
            error = data.get('error')
            logger.debug(f'[{username}] В статусе данных в process_hook передана ошибка: {error}')
    if event_loop and not event_loop.is_closed():
        logger.debug(f'[{username}] Отправляем данные для формирования строки прогресса.')
        asyncio.run_coroutine_threadsafe(send_progress(data), event_loop)
    else:
        logger.debug(f'[{username}] Не задан или закрыт event_loop.')

async def fetch_url(url, update, context, download=False):
    settings = context.bot_data['settings']
    user_settings = context.user_data.get('user_settings', UserSettings())
    username = update.effective_user.first_name or 'Anonym'
    logger.debug(f'[{username}] пришли в fetch_url.')
    # Получаем event loop до вызова asyncio.to_thread
    event_loop = asyncio.get_running_loop()
    ydl_options = {}
    if download:
        user_id = update.effective_user.id
        outtmpl = settings.system.outtmpl.replace('~user_id~', str(user_id))
        ydl_options = {
            'format': settings.format_result,
            'postprocessors': [{
                'key': settings.postprocessors_key,
                'preferredcodec': user_settings.codec_value,
                'preferredquality': user_settings.quality,
            }],
            'outtmpl': outtmpl,
            'cachedir': settings.system.cache_dir,
            'progress_hooks': [lambda data: process_hook(data, context, update, event_loop)],
        }
        logger.info(f'[{username}] Сформировали параметры для загрузки:\n{ydl_options}')
        await send_to_chat(update, context, settings.msg_start_downloading)
    # Добавляем своего логгера
    ydl_options.setdefault('logger', logger)
    try:
        logger.info(f'[{username}] Стартуем запрос к ydl. Ссылка: {url}')
        # get_media_from_url вызывается в потоке, loop передан заранее
        info = await asyncio.to_thread(get_media_from_url, url, ydl_options, download)
    except Exception as e:
        logger.error(f'[{username}] ошибка при вызове get_media_from_url: ', exc_info=True)
        await send_to_chat(update, context, f"{settings.error} {e}")
        return None
    if not info:
        logger.error(f'[{username}] данные после запроса ydl пустые.')
        await send_to_chat(update, context, settings.err_no_download_info)
    return info
