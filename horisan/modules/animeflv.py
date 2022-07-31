from animeflv import AnimeFLV
api = AnimeFLV()
from pyrogram import filters
from horisan import pbot as bot

@bot.on_message(filters.command("sr"))
async def anime(_, message):
    query = " ".join(message.command[1:])
    uff = api.search('query')
    name = uff["title"]
    rat = uff["rating"]
    pic = uff["banner"]
    await message.reply_photo(pic, caption=name)