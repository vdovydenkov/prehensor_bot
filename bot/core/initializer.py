# bot\core\initializer.py

import logging
logger = logging.getLogger('prehensor')

from telegram.ext import ApplicationBuilder

from bot.core.error_handler import error_catcher
from bot.config.configurator import Cfg
from bot.cmd_handlers import register_handlers


def bot_init(config: Cfg = None) -> None:
    '''
    Логика инициализации бота:
      Регистрация командных хендлеров,
      Регистрация хендлера ошибок.
    '''
    app = ApplicationBuilder().token(config.tg_token).build()
    app.bot_data['cfg'] = config

    logger.info('Регистрируем командные хендлеры бота.')
    register_handlers(app)

    app.add_error_handler(error_catcher)
    logger.info('Запускаем бота.')
    app.run_polling()
