# bot/__main__.py

from bot.core.log_reporter import (
    set_logger,
    add_console_handler,
    add_file_handlers
)

logger = set_logger('prehensor')
add_console_handler(logger)
logger.info('Консольный логгер инициализирован.')

from bot.core.initializer import bot_init
from bot.core.error_handler import error_catcher
from bot.config.configurator import Cfg

def main():
    logger.info('Загружаем конфигурацию.')
    try:
        cfg = Cfg()
        logger.info('Конфигурация бота успешно загружена.', cfg)
    except Exception:
        logger.info('Ошибка при загрузке конфигурации!', exc_info=True)
    # Включаем файловые логи - отладочный и лог ошибок
    add_file_handlers(logger, cfg.log_dir)
    logger.info(f'Включили файловое логирование в папку: {cfg.log_dir}')

    bot_init(cfg)

    logger.info('Завершаемся.')

if __name__ == '__main__':
    main()
