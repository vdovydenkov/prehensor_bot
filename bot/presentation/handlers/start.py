# bot/presentation/handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.config.configurator import Cfg
from bot.config.defaults import DEFAULT_RAW_CONFIG
from bot.presentation.common.handler_decorators import handle_user_errors

import logging
logger = logging.getLogger('prehensor')

@handle_user_errors
async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    local_id = 'start_command'

    chat_id = update.effective_chat.id
    if chat_id is None:
        logger.warning(f'[{local_id}] chat_id is None.')
        return

    service = context.bot_data.get('service')
    if service is None:
        logger.error(f'[{local_id}] User service is None!')
        return

    user = await service.get_or_create_user(
        update.effective_user
    )

    user_msg = update.message.text

    # Идентификатор для логгера - добавляем имя пользователя
    local_id = f'start_command:{user.name}'

    logger.info(f'[{local_id}] user_msg={user_msg}')

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
        if cfg.owner_id == user.tg_id:
            await service.set_as_owner(user)
            text += '\nВладелец опознан!'

    # сброс пользовательских данных
    context.user_data.clear()
    context.user_data['user_cfg'] = cfg.user

    await send_to_chat(
        chat_id,
        context.bot,
        f"{user.name}, {text}"
    )
