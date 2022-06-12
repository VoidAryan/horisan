import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from horisan.events import register
from horisan import telethn as tbot


PHOTO = "https://telegra.ph/file/242d186b33c49c0329a0f.mp4"


@register(pattern=("/afk"))
async def awake(event):
    TEXT = f"**Hey [{event.sender.first_name}](tg://user?id={event.sender.id}) ! Im `Kyouko San`. An anime based robot always ready to make your gc efficient!** \n\n"
    BUTTON = [
        [   Button.url("【V๏ɪ፝֟𝔡】Network","https://t.me/voidxnetwork")
        ]
    ]
    await tbot.send_file(event.chat_id, PHOTO, caption=TEXT, buttons=BUTTON)
