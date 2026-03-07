# bot/core/fetcher.py

import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.services.media_downloader import get_media_from_url
from bot.utils.format import format_bytes

import logging
logger = logging.getLogger('prehensor')

def process_hook(
        data,
        context: ContextTypes.DEFAULT_TYPE,
        chat_id: int,
        event_loop: asyncio.AbstractEventLoop
    ):
    logger.debug('process_hook получил данные.')
    cfg = context.bot_data['cfg']

    async def send_progress(data):
        status = data.get('status')
        downloaded = data.get('downloaded_bytes', 0)
        total = data.get('total_bytes')
        if status == 'downloading':
            if total:
                percent = f'{downloaded / total * 100:.0f}%'
                progress = f'{percent} {cfg.msg.progress_percent}'
            else:
                download_info = format_bytes(downloaded)
                progress = f'{cfg.msg.download_progress} {download_info}'
            # Если прогресс преодолел заданный шаг — отправляем сообщение
            last_progress_value = context.user_data.get('last_progress_value', 0)
            step = cfg.user.progress_step
            if downloaded >= last_progress_value + step:
                logger.debug(f'Прогресс преодолел шаг {step} байт, строка готова: {progress}')
                context.user_data['last_progress_value'] = downloaded
                await send_to_chat(
                    chat_id,
                    context.bot,
                    progress
                )
        elif status == 'finished':
            download_info = format_bytes(downloaded)
            progress = f'{download_info} {cfg.msg.download_completed} {cfg.msg.send_file}'
            logger.debug('Статус=finished')
            await send_to_chat(
                chat_id,
                context.bot,
                progress
            )
        elif status == 'error':
            error = data.get('error')
            logger.debug(f'В статусе данных в process_hook передана ошибка: {error}')
    if event_loop and not event_loop.is_closed():
        asyncio.run_coroutine_threadsafe(
            send_progress(data),
            event_loop
        )
    else:
        logger.debug('Не задан или закрыт event_loop.')

def get_ydl_options(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> dict:
    '''
    Формирует ydl_options из параметров конфига.
    '''
    cfg = context.bot_data['cfg']
    user_cfg = context.user_data.get('user_cfg', cfg.user)
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or 'Anonym'
    # Берём текущии event loop, чтобы передать его в hook-функцию
    try:
        event_loop = asyncio.get_running_loop()
    except RuntimeError:
        event_loop = None
    # Заменяем шаблон временного файла на id пользователя
    outtmpl = cfg.outtmpl.replace('~user_id~', str(user_id))
    options = {
        'quiet': True,
        'no_warnings': True,
        'format': cfg.ydl.format_result,
        'postprocessors': [{
            'key': cfg.ydl.postprocessors_key,
            'preferredcodec': user_cfg.codec_value,
            'preferredquality': user_cfg.quality,
        }],
        'outtmpl': outtmpl,
        'cachedir': cfg.cache_dir,
        'progress_hooks': [
            lambda data: process_hook(data, context, chat_id, event_loop)
        ],
    }
    logger.debug(f'[{user_name}] Сформировали параметры для загрузки.')
    return options

async def fetch_url(
    url: str,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    download: bool = False
) -> dict | None:
    '''
    Запускает загрузку (если download = True, иначе - просто информацию)
    Возвращаем словарь с результатами работы.
    '''
    chat_id = update.effective_chat.id
    # Собираем конфигурацию
    cfg = context.bot_data['cfg']
    username = update.effective_user.first_name or 'Anonym'

    logger.debug(f'[{username}] Пришли в fetch_url.')

    # Получаем event loop до вызова asyncio.to_thread
    # event_loop = asyncio.get_running_loop()
    ydl_options = {}
    if download:
        context.user_data['last_progress_value'] = 0
        ydl_options = get_ydl_options(update, context)
        await send_to_chat(
            chat_id,
            context.bot,
            cfg.msg.start_downloading
        )
    # Добавляем своего логгера
    # ydl_options.setdefault('logger', logger)
    try:
        logger.info(f'[{username}] Стартуем запрос к ydl. Ссылка: {url}')
        # get_media_from_url вызывается в потоке, loop передан заранее
        info = await asyncio.to_thread(get_media_from_url, url, ydl_options, download)
    except ValueError:
        logger.error(f'[{username}] запрошен плейлист, вместо отдельного файла.')
        await send_to_chat(
            chat_id,
            context.bot,
            f"{cfg.err.prefix} Это ссылка на плейлист, я пока их загружать не умею."
        )
        return None
    except Exception as e:
        msg = str(e)
        logger.error(f'[{username}] ошибка при вызове get_media_from_url: ', exc_info=True)
        await send_to_chat(
            chat_id,
            context.bot,
            f"{cfg.err.prefix} {msg}"
        )
        return None
    if not info:
        logger.error(f'[{username}] данные после запроса ydl пустые.')
        await send_to_chat(
            chat_id,
            context.bot,
            cfg.err.no_download_info
        )
    return info
