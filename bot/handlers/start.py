from telegram import Update
from telegram.ext import ContextTypes
from bot.core.messenger import send_to_chat
from bot.config import UserSettings

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # сброс пользовательских данных
    context.user_data.clear()
    context.user_data['user_settings'] = UserSettings()

    username = update.effective_user.first_name
    text = context.bot_data['settings'].msg_start_text
    await send_to_chat(update, context, f"{username}, {text}")
