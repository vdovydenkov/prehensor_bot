import os, asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.format import format_bytes
from bot.utils.convertors import media_data_to_string

async def send_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    settings = context.bot_data['settings']
    if settings.system.debug_mode:
        print("SEND:", text)
    if update.effective_chat:
        await update.effective_chat.send_message(text=text)

async def show_media_info(update, context, details=False):
    settings = context.bot_data['settings']
    info = context.user_data.get('media_info')
    if not info:
        return await send_to_chat(update, context, settings.msg_no_media_info)
    text = media_data_to_string(info, details)
    await send_to_chat(update, context, text)

async def send_media(update, context):
    settings = context.bot_data['settings']
    user_settings = context.user_data['user_settings']
    media_info = context.user_data.get('media_info')
    if not media_info:
        return
    result_path = media_info.get('result_path')
    if result_path is None:
        return await send_to_chat(update, context, settings.err_path_is_empty)
    
    # Извлекаем базовую часть пути, без расширения
    base = os.path.splitext(result_path)[0]
    # К этому пути добавляем расширение выбранного кодека
    new_result_path = f"{base}.{user_settings.codec_value.lstrip('.')}"

    if not os.path.exists(new_result_path):
        return await send_to_chat(update, context, settings.err_file_not_found)
        
    try:  # Отправляем загруженный файл в чат
        with open(new_result_path, 'rb') as file:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    except Exception as exc_error:        
        await send_to_chat(update, context, f'{settings.error} {exc_error}')
    finally:  # Удаляем файл
        try: os.remove(new_result_path)
        except OSError as error:
            print(f"Ошибка при удалении файла: {error}")
