# bot/main.py
from bot.services.reporter import set_console_logger, add_file_handlers

logger = set_console_logger('prehensor')
logger.info('Консольный логгер инициализирован. Переменные окружения из .env не загружены.')

from telegram.ext import ApplicationBuilder
from bot.config import Settings
from bot.handlers import register_handlers

def main():
    logger.info('Загружаем конфигурацию.')
    try:
        settings = Settings()
    except Exception:
        logger.critical('Ошибка при загрузке конфигурации!', exc_info=True)
        exit(1)
    logger.info('Конфигурация бота успешно загружена.')
    # Включаем отладочное логгирование и лог ошибок в файлы
    add_file_handlers(logger, settings.system.log_dir)
    logger.info(f'Включили файловое логирование в папку: {settings.system.log_dir}')

    app = ApplicationBuilder().token(settings.system.tg_token).build()
    app.bot_data['settings'] = settings

    logger.info("Регистрируем handler'ы")
    register_handlers(app)

    logger.info('Запускаем бота.')
    app.run_polling()

if __name__ == '__main__':
    main()
    logger.info('Корректное завершение.')
