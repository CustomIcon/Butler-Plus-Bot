from pyrogram import errors
from pyrogram.types import Message

async def send_message(message: Message, text, *args, **kwargs):
    try:
        return await message.reply_text(text, *args, **kwargs)
    except errors.BadRequest as err:
        if str(err) == "Reply message not found":
            return await message.reply_text(text, quote=False, *args, **kwargs)