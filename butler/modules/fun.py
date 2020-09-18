from butler import BotID, BotName
from pyrogram.types import ChatPermissions
import html
import random
from butler.modules import fun_strings
from butler.helpers.admincheck import admin_check
import time


async def runs(_, message):
    await message.reply_text(random.choice(fun_strings.RUN_STRINGS))


async def slap(client, message):
    reply_text = message.reply_to_message.reply_text if message.reply_to_message else message.reply_text
    curr_user = html.escape(message.from_user.first_name)
    try:
        user_id = message.reply_to_message.from_user.id
    except AttributeError:
        user_id = message.from_user.id
    if user_id == BotID:
        temp = random.choice(fun_strings.SLAP_BUTLER_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                cantmute = await admin_check(message)
                if cantmute:
                    await reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                await client.restrict_chat_member(message.chat.id,
                    message.from_user.id,
                    ChatPermissions(can_send_messages=False),
                    until_date=mutetime
                )
            await reply_text(temp[0])
        else:
            await reply_text(temp)
        return

    if user_id:
        slapped_user = await client.get_users(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)
    else:
        user1 = BotName
        user2 = curr_user
    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)
    reply = temp.format(
        user1=user1,
        user2=user2,
        item=item,
        hits=hit,
        throws=throw
    )
    await reply_text(reply, parse_mode='html')