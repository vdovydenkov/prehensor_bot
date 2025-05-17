# /bot/handlers/help.py
import logging
logger = logging.getLogger('prehensor')

from telegram import Update
from telegram.ext import ContextTypes
from bot.core.messenger import send_to_chat

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    username = update.effective_user.first_name or 'Anonym'
    logger.info(f'[{username}] /help, text={user_msg}')

    text = context.bot_data['cfg'].msg.help_text
    if not text:
        logger.debug(f'[{username}] Нет текста в bot_data["cfg"].msg.help_text')
        logger.warning(f'[{username}] Нет текста справки.')
    await send_to_chat(update, context, text)
