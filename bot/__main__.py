# bot/__main__.py

from bot.core.log_reporter import (
    set_logger,
    add_console_handler,
    add_file_handlers
)

logger = set_logger('prehensor')
add_console_handler(logger)
logger.info('Консольный логгер инициализирован.')

from telegram.ext import ApplicationBuilder
from telegram.error import (
    Conflict,
    NetworkError,
    InvalidToken,
    TelegramError,
)

from bot.config.configurator import Cfg
from bot.handlers import register_handlers

def main():
    logger.info('Загружаем конфигурацию.')
    try:
        cfg = Cfg()
    except Exception:
        logger.debug('Ошибка при загрузке конфигурации!', exc_info=True)
    logger.info('Конфигурация бота успешно загружена.')
    # Включаем файловые логи - отладочный и лог ошибок
    add_file_handlers(logger, cfg.log_dir)
    logger.info(f'Включили файловое логирование в папку: {cfg.log_dir}')

    app = ApplicationBuilder().token(cfg.tg_token).build()
    app.bot_data['cfg'] = cfg

    logger.info('Регистрируем хендлеры телеграм-бота.')
    register_handlers(app)

    logger.info('Запускаем бота.')
    try:
        app.run_polling()
    except Conflict:
        logger.error(cfg.err.bot_conflict)
    except NetworkError:
        logger.error(cfg.err.network_error)
    except InvalidToken:
        logger.error(cfg.err.invalid_token)
    except TelegramError as err:
        logger.error(cfg.err.other_telegram_error, exc_info=True)

    logger.info('Завершаемся.')

if __name__ == '__main__':
    main()
