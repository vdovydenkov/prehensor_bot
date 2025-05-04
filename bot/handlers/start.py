from telegram import Update
from telegram.ext import ContextTypes
from bot.core.messenger import send_to_chat

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cfg = context.bot_data['cfg']
    # сброс пользовательских данных
    context.user_data.clear()
    context.user_data['user_cfg'] = cfg.user

    username = update.effective_user.first_name
    await send_to_chat(update, context, f"{username}, {cfg.msg.start_text}")
