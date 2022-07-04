import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from horisan.events import register
from horisan import telethn as tbot


PHOTO = "https://telegra.ph/file/65c078b44d2e0dec549e2.mp4"


@register(pattern=("/alive"))
async def awake(event):
    TEXT = f"**Hey [{event.sender.first_name}](tg://user?id={event.sender.id}) ! Im `Kyouko San`. An anime based robot always ready to make your gc efficient!** \n\n"
    TEXT += "◈ Working Under [【V๏ɪ፝֟𝔡】Network](t.me/voidxnetwork) ◈"
    BUTTON = [
        [
            Button.url("【Support】", "https://t.me/kyoukoXSupport"),
            Button.url("【Updates】", "https://t.me/hori_x_updates"),
        ],
    ]
    await tbot.send_file(event.chat_id, PHOTO, caption=TEXT, buttons=BUTTON)
