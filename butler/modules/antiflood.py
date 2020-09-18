from pyrogram.errors import BadRequest
from pyrogram import filters
from pyrogram.types import ChatPermissions
from butler.modules.database import antiflood_db as sql
from butler.helpers.admincheck import admin_check
from butler.helpers.parser import mention_markdown
from butler import SUDO, butler

FLOOD_GROUP = 3


@butler.on_message(filters.all & filters.group, group=FLOOD_GROUP)
async def check_flood(client, message):
    user = message.from_user
    chat = message.chat
    if not user:  # ignore channels
        return

    can_flood = await admin_check(message)
    # ignore admins and whitelists
    if user.id in SUDO or can_flood:
        sql.update_flood(chat.id, None)
        return

    should_ban = sql.update_flood(chat.id, user.id)
    if not should_ban:
        return

    try:
        await client.restrict_chat_member(chat.id, user.id, ChatPermissions(can_send_messages=False))
        await client.send_message(chat.id,f"**mutes {mention_markdown(user.id, user.first_name)} permanently!**\nStop flooding the group!",
            parse_mode='markdown')
    except BadRequest:
        await message.reply_text("I can't kick people here, give me permissions first! I'll disable antiflood for now.")
        sql.set_flood(chat.id, 0)


async def set_flood(client, message):
    print('works')
    args = message.text.split(None, 1)
    chat = message.chat

    update_chat_title = chat.title
    message_chat_title = message.chat.title

    can_set_flood = await admin_check(message)
    if can_set_flood:
        if update_chat_title == message_chat_title:
            chat_name = ""
        else:
            chat_name = f" in **{update_chat_title}**"

        if len(args) >= 1:
            val = args[1].lower()
            if val in ('off', 'no', '0'):
                sql.set_flood(chat.id, 0)
                await message.reply_text(
                    "Antiflood has been disabled{}.".format(chat_name),
                    parse_mode='markdown')

            elif val.isdigit():
                amount = int(val)
                if amount <= 0:
                    sql.set_flood(chat.id, 0)
                    await message.reply_text(
                        "Antiflood has been disabled{}.".format(chat_name),
                        parse_mode='markdown')

                elif amount < 3:
                    await message.reply_text(
                        "Antiflood has to be either 0 (disabled), or a number bigger than 3!")
                else:
                    sql.set_flood(chat.id, amount)
                    await message.reply_text(
                        "Antiflood has been updated and set to {}{}".format(
                            amount, chat_name), parse_mode='html')

                return
            else:
                await message.reply_text("Unrecognised argument - please use a number, 'off', or 'no'.")
    else:
        await message.reply_text('`permission denied`')


async def flood(client, message):
    chat = message.chat
    update_chat_title = chat.title
    message_chat_title = message.chat.title

    if update_chat_title == message_chat_title:
        chat_name = ""
    else:
        chat_name = f"in **{update_chat_title}**"

    limit = sql.get_flood_limit(chat.id)

    if limit == 0:
        await message.reply_text(f"Enforcing flood control {chat_name}!")
    else:
        await message.reply_text(f"I'm currently kicking users if they send flood more than {limit}.")


__HELP__ = """
──「 **Set-Flood** 」──
-> `/flood`
Get the current flood control setting

──「 **Admin-Only** 」──
-> `/setflood` `<int/'no'/'off'>`
enables or disables flood control
"""

__MODULE__ = "AntiFlood"
