# bot/presentation/handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes

from bot.presentation.messaging.telegram_messenger import send_text
from bot.config.configurator import Cfg
from bot.config.defaults import DEFAULT_RAW_CONFIG
from bot.presentation.handlers.common.handler_decorators import (
    CommandContext,
    handle_user_errors,
    prepare_handler_context,
)

import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
@prepare_handler_context
async def start_command(
    update:  Update,
    context: ContextTypes.DEFAULT_TYPE,
    ctx:     CommandContext,
) -> None:
    service = ctx.user_service

    local_id = 'start_command'

    if ctx.domain_user is None:
        ctx.domain_user = await service.create_user(
            # Передаем Телеграм пользователя
            update.effective_user
        )

    # Идентификатор для логгера - добавляем имя пользователя
    local_id = f'start_command:{ctx.domain_user.name}'

    cfg = context.bot_data.get('cfg')
    if (cfg is None) or (not isinstance(cfg, Cfg)):
        logger.warning(
            f'[{local_id}] Не считался конфиг и приветственный текст из cfg.msg.start_text.'
            'Пытаемся считать из DEFAULT_RAW_CONFIG.'
        )
        try:
            text = DEFAULT_RAW_CONFIG['msg']['start_text']
        except KeyError:
            logger.error(f'[{local_id}] Не считался текст приветствия из DEFAULT_RAW_CONFIG.')
            text = 'привет!\n' \
            'Я бот-выцеплятор. Мне можно дать ссылку, по которой я скачаю медиа-файл.\n' \
            'Набери /help, чтобы узнать подробнее.'
    else:  # С конфигом всё в порядке
        text = cfg.msg.start_text
        # Если id владельца из конфигурации совпадает с id пользователя
        if cfg.owner_id == ctx.domain_user.tg_id:
            await service.set_as_owner(ctx.domain_user)
            text += '\nВладелец опознан!'

    # сброс пользовательских данных
    context.user_data.clear()
    context.user_data['user_cfg'] = cfg.user

    await send_text(
        context.bot,
        ctx.chat.id,
        f"{ctx.domain_user.name}, {text}"
    )
