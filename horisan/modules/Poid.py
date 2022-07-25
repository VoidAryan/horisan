from telethon import events, Button, custom, version
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import os,re
import requests
import time
from datetime import datetime
from PIL import Image
from io import BytesIO
from horisan import telethn as bot
from horisan.events import register


edit_time = 5
""" =======================CONSTANTS====================== """
file1 = "😈"
file2 = "https://telegra.ph/file/2d8c929d3ae263df9edc3.jpg"
file3 = "https://telegra.ph/file/17c38d512eebc1a67d4ef.jpg"
file4 = "https://telegra.ph/file/671138f203cbb7223a61d.jpg"
file5 = "https://telegra.ph/file/671138f203cbb7223a61d.jpg"
""" =======================CONSTANTS====================== """

@register(pattern="/poid")
async def myinfo(event):
    chat = await event.get_chat()
    current_time = datetime.utcnow()
    betsy = event.sender.first_name
    button = [[custom.Button.inline("【USER INFO】",data="information")]]
    on = await bot.send_file(event.chat_id, file=file2,caption= f"۞ Konichiwa {betsy}, I'm Kyouko Hori\n۞ I'm Created By [V O I D](t.me/voidaryan)\n\n۞ Click The Button Below To Get Your Info", buttons=button)

    await asyncio.sleep(edit_time)
    ok = await bot.edit_message(event.chat_id, on, file=file3, buttons=button) 

    await asyncio.sleep(edit_time)
    ok2 = await bot.edit_message(event.chat_id, ok, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok3 = await bot.edit_message(event.chat_id, ok2, file=file1, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok4 = await bot.edit_message(event.chat_id, ok3, file=file2, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok5 = await bot.edit_message(event.chat_id, ok4, file=file1, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok6 = await bot.edit_message(event.chat_id, ok5, file=file3, buttons=button)
    
    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"information")))
async def callback_query_handler(event):
  try:
    PRO = await bot.get_entity(event.sender_id)
    MIKU = "Your Info Under Kyouko\n\n"
    MIKU += f"───────────────────\n"
    MIKU += f"۞ FIRST NAME : {PRO.first_name} \n"
    MIKU += f"۞ LAST NAME : {PRO.last_name}\n"
    MIKU += f"۞ YOU BOT : {PRO.bot} \n"
    MIKU += f"۞ RESTRICTED : {PRO.restricted} \n"
    MIKU += f"۞ USER ID : {event.sender_id}\n"
    MIKU += f"۞ USERNAME : {PRO.username}\n"
    MIKU += f"───────────────────\n"
    await event.answer(MIKU, alert=True)
  except Exception as e:
    return

__help__ = """
/myinfo: shows your info in inline button
"""

__mod_name__ = "poid"
__command_list__ = [
    "myinfo"
]
