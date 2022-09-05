"""import os
import re
from horisan.events import register
from horisan import telethn as tbot


PHOTO = "https://telegra.ph/file/242d186b33c49c0329a0f.mp4"


@register(pattern=("/afk"))
async def awake(event):
    TEXT = f"Baii Baii [{event.sender.first_name}](tg://user?id={event.sender.id}) 👋"
    await tbot.send_file(event.chat_id, PHOTO, caption=TEXT)
"""
