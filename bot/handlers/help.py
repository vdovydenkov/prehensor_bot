from telegram import Update
from telegram.ext import ContextTypes
from bot.core.messenger import send_to_chat

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = context.bot_data['cfg'].msg.help_text
    await send_to_chat(update, context, text)
