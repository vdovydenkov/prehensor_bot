# /bot/presentation/handlers/help.py

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.config.configurator import Cfg
from bot.config.defaults import DEFAULT_RAW_CONFIG
from bot.presentation.common.handler_decorators import handle_user_errors

import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    if chat_id is None:
        logger.warning('help_command: chat_id is None.')
        return

    username = update.effective_user.first_name or 'Anonym'
    user_msg = update.message.text

    # Идентификатор для логгера
    local_id = f'help_command:{username}'

    logger.info(f'[{local_id}] user_msg={user_msg}')

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

    await send_to_chat(
        chat_id,
        context.bot,
        text
    )
