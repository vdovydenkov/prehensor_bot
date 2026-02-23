# bot/handlers/message.py

import logging
logger = logging.getLogger('prehensor')

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.validators import is_http_url
from bot.core.fetcher import fetch_url
from bot.core.messenger import send_to_chat, send_media_info
from bot.config.configurator import Cfg
from bot.config.defaults import DEFAULT_RAW_CONFIG

async def message_processor(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
    chat_id = update.effective_chat.id
    if chat_id is None:
        logger.warning('message_processor: chat_id is None.')
        return

    username = update.effective_user.first_name or 'Anonym'
    user_msg = update.message.text

    # Идентификатор для логгера
    local_id = f'message_processor:{username}'

    logger.info(f'[{local_id}] user_msg={user_msg}')

    cfg = context.bot_data.get('cfg')
    if (cfg is None) or (not isinstance(cfg, Cfg)):
        logger.warning(
            f'[{local_id}] Не считался конфиг и тексты сообщений из cfg.msg.command_or_link'
            'Пытаемся считать из DEFAULT_RAW_CONFIG.'
        )
        msg = DEFAULT_RAW_CONFIG.get('msg')
        if msg is None:
            logger.error(
                    f'[{local_id}] Не считались сообщения из DEFAULT_RAW_CONFIG.'
                )
            command_or_link = 'Нужно прислать или команду, или ссылку на медиа.'
            check_link = 'Проверяю что по ссылке.'
        else:
            command_or_link = msg.get('command_or_link', 'Нужно прислать или команду, или ссылку на медиа.')
            check_link = msg.get('check_link', 'Проверяю что по ссылке.')
    else:
        command_or_link = cfg.msg.command_or_link
        check_link = cfg.msg.check_link

    logger.debug(f'[{local_id}] Проверяем http-валидатором.')
    if not is_http_url(user_msg):
        return await send_to_chat(
            chat_id,
            context.bot,
            command_or_link
        )

    await send_to_chat(
        chat_id,
        context.bot,
        check_link
    )
    logger.info(f'[{local_id}] Передаем ссылку в fetcher для получения информации.')
    media_info = await fetch_url(
        user_msg, 
        update,
        context,
        download=False
    )

    if media_info is None:
        logger.warning(f'[{local_id}] media_info не получен от fetch_url.')
        return await send_to_chat(
            chat_id,
            context.bot,
            'Информация о медиа не найдена.'
        )

    logger.debug(
        f'[{local_id}] Получили media_info от fetch_url, сохраняем в контекст и отправляем в messenger/send_media_info'
    )
    context.user_data['media_info'] = media_info
    context.user_data['url'] = user_msg
    await send_media_info(
        chat_id,
        context.bot,
        media_info,
        details=False
    )
