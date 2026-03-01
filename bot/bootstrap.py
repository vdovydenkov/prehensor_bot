# bot\bootstrap.py

import logging
logger = logging.getLogger('prehensor')

from telegram.ext import ApplicationBuilder
from telegram.request import HTTPXRequest

from bot.presentation.common.error_handler import error_handler
from bot.infra.config.configurator import Cfg
from bot.infra.repositories.user_repository import UserRepository
from bot.infra.repositories.sqlite_user_repository import SqliteUserRepository
from bot.application.user_service import UserService
from bot.presentation.handlers import register_handlers

def bot_init(config: Cfg = None) -> None:
    '''
    Логика инициализации бота:
      Регистрация командных хендлеров,
      Регистрация хендлера ошибок.
    '''
    # Таймауты бота
    timeout_settings = HTTPXRequest(
        read_timeout=300.0,
        write_timeout=300.0,
        connect_timeout=30.0,
        pool_timeout=30.0,
    )

    builder = (
        ApplicationBuilder()
        .token(config.tg_token)
        .request(timeout_settings)
    )

    # В отладочном режиме используем стандартный Telegram API
    if not config.debug_mode:
        # На VPS установлен локальный Telegram API, подключаемся к нему
        builder = builder.base_url("http://127.0.0.1:8081/bot")

    app = builder.build()

    app.bot_data['cfg'] = config

    register_handlers(app)

    app.add_error_handler(error_handler)

    repo = SqliteUserRepository()
    service = UserService(repo)
    app.bot_data['service'] = service

    logger.info('Запускаем бота.')
    app.run_polling()
