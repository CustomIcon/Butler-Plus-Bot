from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


prvt_message = '''
**Butler+ v0.0.1 Up and Running**
`Group Scans are on`
'''

grp_message = '''
**Butler+ v0.0.1 Up and Running**
Coming Soon!!!
'''


async def start(client, message):
    if message.chat.type != "private":
        await message.reply_text(grp_message)
        return
    else:
        buttons = [[InlineKeyboardButton("Managed by this Person", url="https://t.me/pokurt"),
                    InlineKeyboardButton('Help', callback_data='help_back')]]
        await message.reply_text(prvt_message, reply_markup=InlineKeyboardMarkup(buttons))
