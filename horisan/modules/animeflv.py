from animeflv import AnimeFLV
api = AnimeFLV()
from pyrogram import filters
from horisan import pbot as bot
import requests

@bot.on_message(filters.command("sr"))
async def anime(_, message):
  query = " ".join(message.command[1:])
  ufff = api.search('query')
  for uff in ufff: 
    name = uff["title"]
    name += uff["rating"]
    pic = uff["banner"]
    await message.reply_photo(pic, caption=name)
