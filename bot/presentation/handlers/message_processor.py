# bot/handlers/message.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.validators import is_http_url
from bot.core.fetcher import fetch_url
from bot.presentation.messaging.telegram_messenger import send_text
from bot.core.messenger import send_media_info
from bot.config.configurator import Cfg
from bot.config.defaults import DEFAULT_RAW_CONFIG
from bot.presentation.handlers.common.handler_decorators import (
    CommandContext,
    handle_user_errors,
    prepare_handler_context,
)

import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
@prepare_handler_context
async def message_processor(
    update:  Update,
    context: ContextTypes.DEFAULT_TYPE,
    ctx:     CommandContext,
) -> None:
    ctx.user_service._check_user(
        ctx.domain_user,
    )

    local_id = f'message_processor:{ctx.domain_user.name}'

    logger.info(f'[{local_id}] message={ctx.message.text}')

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
    if not is_http_url(ctx.message.text):
        return await send_text(
            context.bot,
            ctx.chat.id,
            command_or_link
        )

    await send_text(
        context.bot,
        ctx.chat.id,
        check_link
    )

    logger.info(f'[{local_id}] Передаем ссылку в fetcher для получения информации.')

    media_info = await fetch_url(
        ctx.message.text,
        update,
        context,
        download=False
    )

    if media_info is None:
        logger.warning(f'[{local_id}] media_info не получен от fetch_url.')
        return await send_text(
            context.bot,
            ctx.chat.id,
            'Информация о медиа не найдена.'
        )

    logger.debug(
        f'[{local_id}] Получили media_info от fetch_url, сохраняем в контекст и отправляем в messenger/send_media_info'
    )

    context.user_data['media_info'] = media_info
    context.user_data['url'] = ctx.message.text

    await send_media_info(
        ctx.chat.id,
        context.bot,
        media_info,
        details=False
    )
