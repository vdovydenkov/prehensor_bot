# bot/presentation/common/error_handler.py

from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import (
    Conflict,
    InvalidToken,
    NetworkError,
)
from bot.config.defaults import DEFAULT_RAW_CONFIG

import logging
logger = logging.getLogger('prehensor')

async def error_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
    msg_for_user = 'Простите, произошла ошибка. Администратору отправлен отчёт.'
    # Если конфига нет в контексте - берём по дефолту.
    cfg = context.bot_data.get(
        'cfg',
        DEFAULT_RAW_CONFIG
    )

    err = context.error
    if isinstance(err, NetworkError):
        logger.error(cfg.err.network_error)
    elif isinstance(err, Conflict):
        logger.error(cfg.err.bot_conflict)
    elif isinstance(err, InvalidToken):
        logger.error(cfg.err.invalid_token)

    # Ошибки доступа

    else:  # Ошибку нигде не отловили
        logger.error(
            "Telegram error while processing update: %s",
            update,
            exc_info=context.error
        )

    if update.effective_chat:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=msg_for_user,
            )
        except Exception:
            logger.exception(
                'Не удалось отправить сообщение об ошибке пользователю'
            )

