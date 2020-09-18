import shlex

from pyrogram.filters import *
from pyrogram.types import Message

from butler import BotUsername


def command(commands: str or List[str], prefixes: str or List[str] = "/", case_sensitive: bool = False):
    """
        This is a drop in replacement for the default Filters.command that is included
        in Pyrogram. The Pyrogram one does not support /command@botname type commands,
        so this custom filter enables that throughout all groups and private chats.
        This filter works exactly the same as the original command filter even with support for multiple command
        prefixes and case sensitivity.
        Command arguments are given to user as message.command
    """

    async def func(flt, _, message: Message):
        text: str = message.text or message.caption
        message.command = None

        if not text:
            return False

        regex = "^({prefix})+\\b({regex})\\b(\\b@{bot_name}\\b)?(.*)".format(
            prefix='|'.join(re.escape(x) for x in flt.prefixes),
            regex='|'.join(flt.commands),
            bot_name=BotUsername
        )

        matches = re.search(re.compile(regex), text)
        if matches:
            message.command = [matches.group(2)]
            for arg in shlex.split(matches.group(4).strip()):
                message.command.append(arg)
            return True
        else:
            return False

    commands = commands if type(commands) is list else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if type(prefixes) is list else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return create(
        func,
        "CustomCommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    )