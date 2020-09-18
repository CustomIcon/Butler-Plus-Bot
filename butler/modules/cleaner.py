from butler.modules.database import cleaner_db as sql
from butler.helpers.admincheck import admin_check
from butler import SUDO


async def bluetextclean(_, message):
    can_clean = sql.chat_should_clean(message.chat.id)
    try:
        if can_clean and message.entities.command:
            await message.delete()
    except AttributeError:
        pass


async def cleaner_setting(_, message):
    args = message.text.split(None, 1)
    can_clean = await admin_check(message)
    if can_clean and message.from_user.id in SUDO:
        if len(args) == 1:
            await message.reply_text(f"This chat's current setting is: `{sql.chat_should_clean(message.chat.id)}`",parse_mode='markdown')
        else:
            if args[1] in ("yes", "on"):
                sql.set_chat_setting(message.chat.id, True)
                await message.reply_text("Cleaning blue text is on!")
            elif args[1] in ("no", "off"):
                sql.set_chat_setting(message.chat.id, False)
                await message.reply_text("Cleaning blue text is off!")
    else:
        await message.reply_text('you are not an admin.')