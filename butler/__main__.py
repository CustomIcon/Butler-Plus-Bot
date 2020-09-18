import asyncio
import importlib
import sys
import time
import traceback

from pyrogram import idle

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from butler import Owner, butler, get_bot
from butler.modules import ALL_MODULES

BOT_RUNTIME = 0
HELP_COMMANDS = {}

loop = asyncio.get_event_loop()


async def get_runtime():
    return BOT_RUNTIME


# async def reload_bot():
#     await butler.start()
#     for modul in ALL_MODULES:
#         imported_module = importlib.import_module("butler.modules." + modul)
#         importlib.reload(imported_module)


async def reinitial_restart():
    await get_bot()


async def reboot():
    global BOT_RUNTIME, HELP_COMMANDS
    importlib.reload(importlib.import_module("butler.modules"))
    # await setbot.send_message(Owner, "Bot is restarting...")
    await butler.restart()
    await reinitial_restart()
    # Reset global var
    BOT_RUNTIME = 0
    HELP_COMMANDS = {}
    for modul in ALL_MODULES:
        imported_module = importlib.import_module("butler.modules." + modul)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if imported_module.__MODULE__.lower() not in HELP_COMMANDS:
                HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
            else:
                raise Exception("Can't have two modules with the same name! Please change one")
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
        importlib.reload(imported_module)


# await butler.send_message(Owner, "Restart successfully!")

async def except_hook(errtype, value, tback):
    sys.__excepthook__(errtype, value, tback)
    errors = traceback.format_exception(etype=errtype, value=value, tb=tback)
    button = InlineKeyboardMarkup([[InlineKeyboardButton("🐞 Report bugs", callback_data="report_errors")]])
    text = "An error has accured!\n\n```{}```\n".format("".join(errors))
    if errtype == ModuleNotFoundError:
        text += "\nHint: Try this in your terminal `pip install -r requirements.txt`"
    await butler.send_message(Owner, text, reply_markup=button)


async def reinitial():
    await butler.start()
    await get_bot()
    await butler.stop()


async def start_bot():
    # sys.excepthook = except_hook
    print("----- Checking butler... -----")
    await reinitial()
    print("----------- Check done! ------------")
    # Butler
    await butler.start()
    for modul in ALL_MODULES:
        imported_module = importlib.import_module("butler.modules." + modul)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if imported_module.__MODULE__.lower() not in HELP_COMMANDS:
                HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
            else:
                raise Exception("Can't have two modules with the same name! Please change one")
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
    print("-----------------------")
    print("Butler modules: " + str(ALL_MODULES))
    print("-----------------------")
    print("Bot run successfully!")
    await idle()


if __name__ == '__main__':
    BOT_RUNTIME = int(time.time())
    loop.run_until_complete(start_bot())
