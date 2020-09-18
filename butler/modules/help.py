import re
import time

from __main__ import HELP_COMMANDS # pylint: disable-msg=E0611
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.raw import functions

from butler import butler, DB_AVAILABLE, BotUsername
from butler.helpers.misc import paginate_modules


HELP_STRINGS = f"""
You can use / on your Butler to execute that commands.
Here is current modules I have

**Main** commands available:
 - /start: get your bot status
 - /help: get all modules help
"""

async def help_parser(client, chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help"))
    await client.send_message(chat_id, text, reply_markup=keyboard)


async def help_command(client, message):
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Help",
                url=f"t.me/{BotUsername}?start=help")]])
        await message.reply("Contact me in PM to get the list of possible commands.",
                            reply_markup=buttons)
    else:
        await help_parser(client, message.chat.id, HELP_STRINGS)


async def help_button_callback(_, __, query):
    if re.match(r"help_", query.data):
        return True


@butler.on_callback_query(filters.create(help_button_callback))
async def help_button(_client, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    if mod_match:
        module = mod_match.group(1)
        text = "This is help for the module **{}**:\n".format(HELP_COMMANDS[module].__MODULE__) \
            + HELP_COMMANDS[module].__HELP__

        await query.message.edit(text=text,
                                reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton(text="Back", callback_data="help_back")]]))

    elif back_match:
        await query.message.edit(text=HELP_STRINGS,
                    reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")))
