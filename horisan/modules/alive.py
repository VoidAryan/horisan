import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from horisan.events import register
from horisan import telethn as tbot


PHOTO = "https://telegra.ph/file/c458924bf40c213062dd2.mp4"


@register(pattern=("/alive"))
async def awake(event):
    TEXT = f"**Hey There Weebs!![{event.sender.first_name}](tg://user?id={event.sender.id})** \n\n"
    TEXT += f"**I Am Hori San!**\n\n"
    TEXT += f"**Meet My izumi kun hehe - [VOID](https://t.me/voidxtoxic)**** \n\n"
    TEXT += "**◈ I will love to be in your groupchat ◈"
    BUTTON = [
        [
            Button.url("【Support】", "https://t.me/HoriXSupport"),
            Button.url("【Updates】", "https://t.me/kyouko_updates"),
        ]
    ]
    await tbot.send_file(event.chat_id, PHOTO, caption=TEXT, buttons=BUTTON)
