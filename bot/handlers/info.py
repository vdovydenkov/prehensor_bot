from telegram import Update
from telegram.ext import ContextTypes
from bot.core.messenger import show_media_info

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_media_info(update, context, details=True)
