# bot/presentation/messaging/telegram_messenger.py
from telegram import Bot, Message

from bot.config.constants import MAX_TELEGRAM_MESSAGE_LENGTTH

import logging
logger = logging.getLogger('prehensor')


async def send_text(
    bot:     Bot,
    chat_id: int,
    text:    str,
) -> Message:
    verified_text = _safety_text(raw_message=text)
        
    return await bot.send_message(
        chat_id=chat_id,
        text=verified_text
    )

async def update_text(
    bot:           Bot,
    chat_id:       int,
    msg_id:        int,
    updating_text: str,
    ) -> Message:
    verified_text = _safety_text(raw_message=updating_text)
    return await bot.edit_message_text(
        verified_text,
        chat_id=chat_id,
        message_id=msg_id,
    )

def _safety_text(raw_message: str) -> str:
    text = raw_message
    text_length = len(raw_message)

    if text_length > MAX_TELEGRAM_MESSAGE_LENGTTH:
        logger.warning(
            f'[messenger._safety_text] Text too long: '
            f'{text_length} > {MAX_TELEGRAM_MESSAGE_LENGTTH}.'
        )
        text = raw_message[:4093] + '...'

    return text

