import html
from typing import Optional, List
import re
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import BadRequest, Unauthorized
from pyrogram import filters

from butler.modules.database import reporting_db as sql
from butler.helpers.parser import mention_markdown
from butler import SUDO

REPORT_GROUP = 5
REPORT_IMMUNE_USERS = SUDO


async def report_setting(_, message):
    args = message.text.split(None, 1)
    if message.chat.type == 'private':
        await message.delete()
    else:
        if len(args) == 1:
            await message.reply_text(f"This chat's current setting is: `{sql.chat_should_report(message.chat.id)}`",parse_mode='markdown')
        else:
            if args[1] in ("yes", "on"):
                sql.set_chat_setting(message.chat.id, True)
                await message.reply_text(
                    "Reporting is on! Admins who have turned on reports will be notified when /report "
                    "or @admin are called.")

            elif args[1] in ("no", "off"):
                sql.set_chat_setting(message.chat.id, False)
                await message.reply_text(
                    "Reporting turn off! Admins will not be notified on /report or @admin.")


async def report(client, message):
    can_report = sql.chat_should_report(message.chat.id)
    if can_report:
        chat = await client.get_chat(message.chat.id)
        if message.reply_to_message.from_user:
            reported_user = message.reply_to_message.from_user
        else:
            await message.reply_text('I can not report "Nothing"')
            return
        chat_name = chat.title or chat.username
        if reported_user.id in REPORT_IMMUNE_USERS:
            await message.reply_text("Sudoers can not be reported")
            return
        if chat.type == 'supergroup':
            msg = "**{}:**" \
                "\n**Reported user:** {} (```{}```)" \
                "\n**Reported by:** {} (```{}```)".format(html.escape(chat.title),
                                                                    mention_markdown(reported_user.id, reported_user.first_name), reported_user.id,
                                                                    mention_markdown(message.from_user.id, message.from_user.first_name), message.from_user.id)
            link = f"\n**Link:** [click here]({message.reply_to_message.link})"
            keyboard = [[InlineKeyboardButton(u"➡ Message", url=message.reply_to_message.link)],
                        [InlineKeyboardButton(u"⚠ Kick", callback_data="rp_{}=ki={}={}".format(
                                                                chat.id, reported_user.id, reported_user.first_name)),
                        InlineKeyboardButton(u"⛔️ Ban", callback_data="rp_{}=ba={}={}".format(
                                                                chat.id, reported_user.id, reported_user.first_name))
                        ]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            msg = "{} is calling for admins in \"{}\"!".format(
                mention_markdown(message.from_user.id, message.from_user.first_name), html.escape(chat_name))
        alladmins = client.iter_chat_members(message.chat.id, filter="administrators")
        async for admin in alladmins:
            if admin.user.is_bot:  # can't message bots
                continue
            try:
                await client.send_message(
                admin.user.id,
                    msg + link,
                    parse_mode='markdown',
                    reply_markup=reply_markup)
            except Unauthorized:
                pass

        await message.reply_to_message.reply_text(
            "{} reported the message to the admins.".format(
                mention_markdown(
                    message.from_user.id,
                    message.from_user.first_name)),
            parse_mode='markdown')
    else:
        await message.delete()


async def buttons(client, query):
    splitter = query.data.replace("rp_", "").split("=")
    if splitter[1] == "ki":
        try:
            await client.kick_chat_member(splitter[0], splitter[2])
            await client.unban_chat_member(splitter[0], splitter[2])
            await query.answer("✅ Succesfully kicked")
        except Exception as err:
            await query.answer("❎ Failed to kick")
            await client.send_message(text="Error: {}".format(err),
                            chat_id=query.message.chat_id,
                            parse_mode='markdown')
    elif splitter[1] == "ba":
        try:
            await client.ban_chat_member(splitter[0], splitter[2])
            await query.answer("✅  Succesfully Banned")
            return
        except Exception as err:
            await client.send_message(text="Error: {}".format(err),
                            chat_id=query.message.chat_id,
                            parse_mode='markdown')
            await query.answer("❎ Failed to ban")


__MODULE__ = "Reporting"

__HELP__ = """
 - /report or @admin <reason>: reply to a message to report it to admins.
NOTE: neither of these will get triggered if used by admins

*Admin only:*
 - /reports <on/off>: change report setting, or view current status.
   - If in chat, toggles that chat's status.
"""
