from pyrogram import filters
from pyrogram.types import ChatPermissions
from pyrogram.errors import (
    UsernameInvalid,
    ChatAdminRequired,
    PeerIdInvalid,
    UserIdInvalid,
    UserAdminInvalid,
    FloodWait,
)

from butler.helpers.admincheck import admin_check

__MODULE__ = "Locks"
__HELP__ = """
Module for Locks & Unlocks

──「 **Locks / Unlocks** 」──
-> `/lock` or `/unlock`
locks and unlocks permission in the group
__Supported Locks / Unlocks__:
 `messages` `media` `stickers`
 `polls` `info` `invite`
 `animations` `games`
 `inlinebots` `webprev`
 `pin` `all`

-> `/locks`
view group permissions
"""


async def view_perm(client, message):
    """view group permission."""
    if message.chat.type in ["group", "supergroup"]:
        v_perm = ""
        vmsg = ""
        vmedia = ""
        vstickers = ""
        vanimations = ""
        vgames = ""
        vinlinebots = ""
        vwebprev = ""
        vpolls = ""
        vinfo = ""
        vinvite = ""
        vpin = ""

        v_perm = await client.get_chat(message.chat.id)

        def convert_to_Bool(val: bool):
            if val:
                return "<code>True</code>"
            else:
                return "<code>False</code>"

        vmsg = convert_to_Bool(v_perm.permissions.can_send_messages)
        vmedia = convert_to_Bool(v_perm.permissions.can_send_media_messages)
        vstickers = convert_to_Bool(v_perm.permissions.can_send_stickers)
        vanimations = convert_to_Bool(v_perm.permissions.can_send_animations)
        vgames = convert_to_Bool(v_perm.permissions.can_send_games)
        vinlinebots = convert_to_Bool(v_perm.permissions.can_use_inline_bots)
        vwebprev = convert_to_Bool(v_perm.permissions.can_add_web_page_previews)
        vpolls = convert_to_Bool(v_perm.permissions.can_send_polls)
        vinfo = convert_to_Bool(v_perm.permissions.can_change_info)
        vinvite = convert_to_Bool(v_perm.permissions.can_invite_users)
        vpin = convert_to_Bool(v_perm.permissions.can_pin_messages)

        if v_perm is not None:
            try:
                permission_view_str = ""

                permission_view_str += "<b>Chat permissions:</b>\n"
                permission_view_str += f"<b>Send Messages:</b> {vmsg}\n"
                permission_view_str += f"<b>Send Media:</b> {vmedia}\n"
                permission_view_str += f"<b>Send Stickers:</b> {vstickers}\n"
                permission_view_str += f"<b>Send Animations:</b> {vanimations}\n"
                permission_view_str += f"<b>Can Play Games:</b> {vgames}\n"
                permission_view_str += f"<b>Can Use Inline Bots:</b> {vinlinebots}\n"
                permission_view_str += f"<b>Webpage Preview:</b> {vwebprev}\n"
                permission_view_str += f"<b>Send Polls:</b> {vpolls}\n"
                permission_view_str += f"<b>Change Info:</b> {vinfo}\n"
                permission_view_str += f"<b>Invite Users:</b> {vinvite}\n"
                permission_view_str += f"<b>Pin Messages:</b> {vpin}\n"
                await message.reply(permission_view_str)
            except Exception as e:
                await message.reply("`Error!`\n" f"**Log:** `{e}`")
    else:
        await message.delete()