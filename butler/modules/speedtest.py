import speedtest
import re
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from butler import SUDO, butler


def convert(speed):
    return round(int(speed) / 1048576, 2)


async def speedtestxyz(client, message):
    buttons = [[InlineKeyboardButton("Image",
                                    callback_data="speedtest_image"),
                InlineKeyboardButton("Text",
                                    callback_data="speedtest_text")]]
    await message.reply_text(
        "Select SpeedTest Mode",
        reply_markup=InlineKeyboardMarkup(buttons))


def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


def speedtest_callback(_, __, query):
    if re.match("speedtest", query.data):
        return True


speedtest_create = filters.create(speedtest_callback)


@butler.on_callback_query(speedtest_create)
async def speedtestxyz_callback(client, query):
    if query.from_user.id in SUDO:
        await query.message.edit_text('Runing a speedtest....')
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = 'SpeedTest Results:'

        if query.data == 'speedtest_image':
            speedtest_image = speed.results.share()
            replym = f"**[SpeedTest Results:]({speedtest_image})**"
            await query.message.edit_text(replym, parse_mode="markdown")

        elif query.data == 'speedtest_text':
            result = speed.results.dict()
            replymsg += f"\n - **ISP:** `{result['client']['isp']}`"
            replymsg += f"\n - **Download:** `{speed_convert(result['download'])}`"
            replymsg += f"\n - **Upload:** `{speed_convert(result['upload'])}`"
            replymsg += f"\n - **Ping:** `{result['ping']}`"
            await query.message.edit_text(replymsg, parse_mode="markdown")
    else:
        await client.answer_callback_query(query.id, "No, you are not allowed to do this", show_alert=False)
