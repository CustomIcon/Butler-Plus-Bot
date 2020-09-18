from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from butler.utils import custom_filters
from butler import butler, SUDO

from butler.modules.start import start
from butler.modules.help import help_command
from butler.modules.locks import view_perm
from butler.modules.whois import whois
from butler.modules.speedtest import speedtestxyz
from butler.modules.paste import paste
from butler.modules.translate import translate
from butler.modules.reporting import report, report_setting, buttons
from butler.modules.eval import evaluate, terminal
from butler.modules.misc import echo_message, ping_bot
from butler.modules.antiflood import set_flood, flood
from butler.modules.fun import runs, slap
from butler.modules.cleaner import cleaner_setting, bluetextclean
from butler.modules.admins import (
    unpin_message,
    pin_message,
    mute_hammer,
    unmute,
    kick_user,
    ban_usr,
    unban_usr,
    promote_usr,
    demote_usr,
    invite_link
)


handlers = [
    MessageHandler(start, custom_filters.command('start')),
    MessageHandler(help_command, custom_filters.command('help')),
    MessageHandler(view_perm, custom_filters.command('locks')),
    MessageHandler(whois, custom_filters.command('info')),
    MessageHandler(pin_message, custom_filters.command('pin')),
    MessageHandler(unpin_message, custom_filters.command('unpin')),
    MessageHandler(mute_hammer, custom_filters.command('mute')),
    MessageHandler(unmute, custom_filters.command('unmute')),
    MessageHandler(kick_user, custom_filters.command('kick')),
    MessageHandler(ban_usr, custom_filters.command('ban')),
    MessageHandler(unban_usr, custom_filters.command('unban')),
    MessageHandler(promote_usr, custom_filters.command('promote')),
    MessageHandler(demote_usr, custom_filters.command('demote')),
    MessageHandler(speedtestxyz, custom_filters.command('speedtest') & filters.user(SUDO)),
    MessageHandler(evaluate, custom_filters.command('py') & filters.user(SUDO)),
    MessageHandler(terminal, custom_filters.command('exec') & filters.user(SUDO)),
    MessageHandler(invite_link, custom_filters.command('invitelink')),
    MessageHandler(paste, custom_filters.command('paste')),
    MessageHandler(translate, custom_filters.command('tr')),
    MessageHandler(echo_message, custom_filters.command('echo') & filters.user(SUDO)),
    MessageHandler(ping_bot, custom_filters.command('ping') & filters.user(SUDO)),
    MessageHandler(report_setting, custom_filters.command("reporting")),
    MessageHandler(report, filters.group & custom_filters.command('report')),
    CallbackQueryHandler(buttons, filters.regex(r"rp_")),
    MessageHandler(set_flood, custom_filters.command('setflood') & ~filters.private),
    MessageHandler(flood, custom_filters.command('flood') & ~filters.private),
    MessageHandler(runs, custom_filters.command('runs') & ~filters.private),
    MessageHandler(slap, custom_filters.command('slap') & ~filters.private),
    MessageHandler(cleaner_setting, custom_filters.command('cleanbluetext') & ~filters.private),
    MessageHandler(bluetextclean, filters.text & ~filters.private)
]

for handler in handlers:
    butler.add_handler(handler)