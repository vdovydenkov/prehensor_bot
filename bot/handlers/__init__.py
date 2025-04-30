from telegram.ext import CommandHandler, MessageHandler, filters

from .start import start_command
from .help import help_command
from .info import info_command
from .download import download_command
from .message import message_processor

def register_handlers(app):
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("download", download_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_processor))
