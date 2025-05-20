# bot/core/messenger.py

import logging
logger = logging.getLogger('prehensor')

import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.format import format_bytes
from bot.utils.converters import media_data_to_string

async def send_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    cfg = context.bot_data['cfg']
    if update.effective_chat:
        await update.effective_chat.send_message(text=text)
        username = update.effective_user.first_name or 'Anonym'
        logger.debug(f'[{username}] SEND: {text}')
    else:
        logger.warning('send_to_chat - Попытка написать в несуществующий чат.')

async def show_media_info(update, context, details=False):
    username = update.effective_user.first_name or 'Anonym'
    logger.debug(f'[{username}] Отправляем информацию о медиа.')
    cfg = context.bot_data['cfg']
    media_info = context.user_data.get('media_info')
    if not media_info:
        logger.info(f'[{username}] {cfg.msg.no_media_info}')
        return await send_to_chat(update, context, cfg.msg.no_media_info)
    text = media_data_to_string(media_info, details)
    await send_to_chat(update, context, text)
    title = media_info.get('title', 'Без заголовка')
    logger.info(f'[{username}] Информация о <{title}> отправлена.')

async def send_media(update, context):
    username = update.effective_user.first_name or 'Anonym'
    logger.info(f'[{username}] Отправляем файл в чат.')
    cfg = context.bot_data['cfg']
    user_cfg = context.user_data['user_cfg']
    media_info = context.user_data.get('media_info')
    if not media_info:
        logger.error(f'[{username}] {cfg.err.no_download_info}')
        return await send_to_chat(update, context, cfg.err.no_download_info)
    result_path = media_info.get('result_path')
    if result_path is None:
        logger.error(f'[{username}] {cfg.err.path_is_empty}')
        return await send_to_chat(update, context, cfg.err.path_is_empty)
    # Извлекаем базовую часть пути, без расширения
    base = os.path.splitext(result_path)[0]
    # К этому пути добавляем расширение выбранного кодека
    new_result_path = f"{base}.{user_cfg.codec_value.lstrip('.')}"

    if not os.path.exists(new_result_path):
        logger.error(f'[{username}] {cfg.err.file_not_found}')
        return await send_to_chat(update, context, cfg.err.file_not_found)

    try:  # Отправляем загруженный файл в чат
        with open(new_result_path, 'rb') as file:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    except Exception:        
        logger.error(f'[{username}] Ошибка отправки файла в чат.', exc_info=True)
        await send_to_chat(update, context, cfg.err.sending_failed)
    finally:  # Удаляем файл
        logger.info(f'[{username}] Удаляем файл {new_result_path}')
        try:
            os.remove(new_result_path)
        except OSError:
            logger.warning(f'[{username}] Не получилось удалить {new_result_path}', exc_info=True)
