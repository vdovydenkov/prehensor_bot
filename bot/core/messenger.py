# bot/core/messenger.py

import os
from typing import Dict
from telegram import Bot

from bot.presentation.messaging.telegram_messenger import send_text
from bot.utils.converters import media_data_to_string, media_info_to_filename
from bot.utils.extractors import get_path

import logging
logger = logging.getLogger('prehensor')

'''
async def send_to_chat(
        chat_id: int,
        bot: Bot,
        text: str
    ):
    # Обрезаем длинную строку
    if len(text) > 4096:
        logger.warning(f'[send_to_chat:{chat_id}] Текст превышает лимит в 4096 символов. Текст обрезан.')
        text = text[:4093] + '...'

    if chat_id is None:
        logger.warning('[send_to_chat:{chat_id}] Попытка написать в несуществующий чат.')
        return

    await bot.send_message(chat_id, text)
'''

async def send_media_info(
        chat_id: int,
        bot: Bot,
        media_info: Dict,
        details=False,
    ) -> None:
    local_id = f'send_media_info:{chat_id}'
    logger.info(
        f'[{local_id}] Отправка media_info.'
    )
    if (media_info is None) or (not isinstance(media_info, Dict)):
        logger.error(f'[{local_id}] media_info не содержит данных или не словарь.')
        return await send_text(
            bot,
            chat_id,
            'Нет информации о медиа.'
        )

    text = media_data_to_string(media_info, details)
    await send_text(
        bot,
        chat_id,
        text
    )
    logger.debug(f'[{local_id}] Информация отправлена.')

async def send_media(
        chat_id: int,
        bot: Bot,
        media_info: Dict,
        error_msg: str = 'Ошибка при отправке файла в чат. Администратора уведомим.',
    ) -> None:
    local_id = f'send_media:{chat_id}'
    logger.info(
        f'[{local_id}] Отправка media файла в чат.'
    )
    if not media_info:
        logger.error(
            f'[{local_id}] media_info не содержит данных.'
        )
        return await send_text(
            bot,
            chat_id,
            error_msg
        )

    result_path = get_path(media_info)
    if result_path is None:
        logger.error(f'[{local_id}] media_info не содержит пути к медиафайлу.')
        return await send_text(
            bot,
            chat_id,
            error_msg
        )

    if not os.path.exists(result_path):
        logger.error(f'[{local_id}] Файл не найден: {result_path}')
        return await send_text(
            bot,
            chat_id,
            error_msg
        )

    # Делаем "красивое имя файла
    beauty_filename = media_info_to_filename(media_info)
    # Отправляем загруженный файл в чат
    try:
        with open(result_path, 'rb') as file:
            await bot.send_document(
                chat_id,
                document=file,
                filename=beauty_filename
            )
    except Exception as e:
        msg = str(e)
        logger.error(
            f'[{local_id}] Не удалось отправить медиафайл в чат:\n{msg}'
        )
        await send_text(
            bot,
            chat_id,
            error_msg
        )

    finally:  # Удаляем файл
        logger.debug(f'[{local_id}] Удаляем файл {result_path}')
        try:
            os.remove(result_path)
        except OSError as e:
            msg = str(e)
            logger.warning(
                f'[{local_id}] Не получилось удалить файл: {result_path}\n{msg}'
            )
