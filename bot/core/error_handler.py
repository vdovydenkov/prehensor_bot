# bot/core/error_catcher.py

import logging
logger = logging.getLogger('prehensor')

import asyncio

from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import (
    TelegramError, Conflict, InvalidToken, NetworkError
)

from bot.config.defaults import DEFAULT_RAW_CONFIG

async def error_catcher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Если конфига нет в контексте - берём по дефолту.
    cfg = context.bot_data.get('cfg', DEFAULT_RAW_CONFIG)

    err = context.error
    if isinstance(context.error, NetworkError):
        logger.error(cfg.err.network_error)
    elif isinstance(context.error, Conflict):
        logger.error(cfg.err.bot_conflict)
    elif isinstance(context.error, InvalidToken):
        logger.error(cfg.err.invalid_token)
    else:
        logger.error(cfg.err.other_telegram_error, exc_info=context.error)

    if isinstance(update, Update) and update.effective_user:
        try:
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text="Простите, произошла ошибка. Администратору отправлен отчёт."
            )
        except Exception as e:
            logger.warning("Не удалось отправить сообщение об ошибке пользователю", exc_info=e)

