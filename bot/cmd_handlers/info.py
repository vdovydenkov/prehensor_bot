# bot/handlers/info.py

import logging
logger = logging.getLogger('prehensor')

from telegram import Update
from telegram.ext import ContextTypes
from bot.core.messenger import show_media_info

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.first_name or 'Anonym'
    user_msg = update.message.text

    logger.info(f'[{username}] /help, text={user_msg}')

    logger.debug(f'[{username}] Переходим в core/messenger/show_media_info')
    await show_media_info(update, context, details=True)
