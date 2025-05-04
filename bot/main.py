# bot/main.py
from bot.services.reporter import set_console_logger, add_file_handlers

logger = set_console_logger('prehensor')
logger.info('Консольный логгер инициализирован.')

from telegram.ext import ApplicationBuilder
from bot.config import Cfg
from bot.handlers import register_handlers

def main():
    logger.info('Загружаем конфигурацию.')
    try:
        cfg = Cfg()
    except Exception:
        logger.debug('Ошибка при загрузке конфигурации!', exc_info=True)
    logger.info('Конфигурация бота успешно загружена.')
    # Включаем отладочное логгирование и лог ошибок в файлы
    add_file_handlers(logger, cfg.log_dir)
    logger.info(f'Включили файловое логирование в папку: {cfg.log_dir}')

    app = ApplicationBuilder().token(cfg.tg_token).build()
    app.bot_data['cfg'] = cfg

    logger.info("Регистрируем handler'ы")
    register_handlers(app)

    logger.info('Запускаем бота.')
    app.run_polling()

if __name__ == '__main__':
    main()
    logger.info('Корректное завершение.')
