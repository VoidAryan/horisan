from horisan import pbot
from pyrogram import filters


pbot.on_message(filters.command("sinfo"))
def info(_, message):
  user = message.from_user.id
    
  
  dta = bot.get_users(user)
  data = f"""**|-First Name** : {dta.first_name}
**|-Last Name**: {dta.last_name}
**|-Telegram Id**: {dta.id}
**|-PermaLink**: {dta.mention(message.from_user.first_name)}
"""
  message.reply_text(data)  #CC=@RyuSenpai
  
