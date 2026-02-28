# bot/handlers/start.py

import logging
logger = logging.getLogger('prehensor')

from telegram import Update
from telegram.ext import ContextTypes

from bot.core.messenger import send_to_chat
from bot.infra.config.configurator import Cfg
from bot.infra.config.defaults import DEFAULT_RAW_CONFIG
from bot.domain.models.user import User

async def start_command(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
    local_id = f'start_command'

    chat_id = update.effective_chat.id
    if chat_id is None:
        logger.warning(f'[{local_id}] chat_id is None.')
        return

    service = context.bot_data.get('service')
    if service is None:
        logger.warning(f'[{local_id}] User service is None.')
        return

    user = await service.get_or_create_user(
        update.effective_user
    )

    username = update.effective_user.first_name or 'Anonym'
    user_msg = update.message.text

    # Идентификатор для логгера - добавляем имя пользователя
    local_id = f'start_command:{username}'

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
    else:
        text = cfg.msg.start_text

    # {cfg.msg.start_text}
    # сброс пользовательских данных
    context.user_data.clear()
    context.user_data['user_cfg'] = cfg.user

    await send_to_chat(
        chat_id,
        context.bot,
        f"{username}, {text}"
    )
