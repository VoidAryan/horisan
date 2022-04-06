import os
import re
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from horisan.events import register
from horisan import telethn as tbot


PHOTO = "https://telegra.ph/file/cdac21f2ea046a1c6a593.jpg"


@register(pattern=("/quicksetup"))
async def awake(event):
    TEXT = """
    [Here is the setup guide for Kyouko Hori]

#1 How to use bot in group?
 • Add bot in your GC
 • Make it admin with proper rights!
 • Give VC rights if you want music player to work

And woo hoo! Bot is ready to work!



#2 What this bot can do and how to check available commands?

 • Type /help in group or in its pm! Both works.
 • Click on the help module you want to check out.
"""
    BUTTON = [
        [
            Button.url("【Support】", "https://t.me/kyoukohori_robot"),
            Button.url("【Owner Sama】", "https://t.me/voidxtoxic"),
        ]
    ]
    await tbot.send_file(event.chat_id, PHOTO, caption=TEXT, buttons=BUTTON)

__help__ = """
 ──「Quick Setup」──                         
 
❂ /quicksetup: An small setup guide to show how bot funtions etc."""
   
__mod_name__ = "【ꜱᴇᴛᴜᴘ】"
