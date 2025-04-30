from telegram.ext import ApplicationBuilder
from bot.config import Settings
from bot.handlers import register_handlers

def main():
    print('Inside main()')
    settings = Settings()
    if settings.system.debug_mode:
        print('Конфигурация загружена.')

    app = ApplicationBuilder().token(settings.system.tg_token).build()
    app.bot_data['settings'] = settings

    # регистрация всех handler’ов
    register_handlers(app)

    if settings.system.debug_mode:
        print('Загружаем бот.')
    app.run_polling()

print('Prehensor: START')
if __name__ == '__main__':
    main()
    print('Prehensor: FINAL')
