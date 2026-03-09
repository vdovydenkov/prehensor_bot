# /bot/presentation/handlers/help.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.presentation.messaging.telegram_messenger import send_text
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
async def help_command(
    update:  Update,
    context: ContextTypes.DEFAULT_TYPE,
    ctx:     CommandContext
) -> None:
    ctx.user_service._check_user(
        ctx.domain_user,
    )

    # Идентификатор для логгера
    local_id = f'help_command:{ctx.domain_user.name}'

    cfg = context.bot_data.get('cfg')
    if (cfg is None) or (not isinstance(cfg, Cfg)):
        logger.warning(
            f'[{local_id}] Не считался конфиг и текст справки из cfg.msg.help_text.'
            'Пытаемся считать из DEFAULT_RAW_CONFIG.'
        )
        try:
            text = DEFAULT_RAW_CONFIG['msg']['help_text']
        except KeyError:
            logger.error(f'[{local_id}] Не считался текст справки из DEFAULT_RAW_CONFIG.')
            text = 'Нет текста справки.'
    else:
        text = cfg.msg.help_text

    await send_text(
        context.bot,
        ctx.chat.id,
        text
    )
