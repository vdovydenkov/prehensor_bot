# bot/__main__.py
import logging
from bot.bootstrap import bot_init, logger_init
from bot.setup_logging import add_file_handlers
from bot.config.configurator import Cfg


def main():
    logger_init()
    logger = logging.getLogger('prehensor')
    logger.info('Загружаем конфигурацию.')
    try:
        cfg = Cfg()
        logger.info('Конфигурация бота успешно загружена.')
    except Exception:
        logger.error('Ошибка при загрузке конфигурации!', exc_info=True)
    if cfg.debug_mode:
        logger.info('Включен отладочный режим!')
    # Включаем файловые логи - отладочный и лог ошибок
    add_file_handlers(logger, cfg.log_dir)
    logger.info(f'Включили файловое логирование в папку: {cfg.log_dir}')

    logger.info('Запускаем бота.')
    bot_init(cfg)

    logger.info('Завершаемся.')

if __name__ == '__main__':
    main()
