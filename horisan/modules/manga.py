from telethon import Button, events

from horisan import telethn as bot

from horisan.utils.API import kissmangaapi as kiss
from horisan.utils import formating_results as format

manga_video = "https://telegra.ph/file/113fffe85ff0294b41b9d.mp4"
text = "Something went wrong....."

class Manga:
    @bot.on(events.NewMessage(pattern=r"^/read"))
    async def event_handler_manga(event):
        try:
            text = event.raw_text.split()
            text.pop(0)
            anime_name = " ".join(text)
            split_data = anime_name.split(":")
            chap = kiss.get_manga_chapter(split_data[0], split_data[1])
            if chap == "Invalid Mangaid or chapter number":
                await event.reply(
                    "Something went wrong....."
                )
                return
            format.manga_chapter_html(f"{split_data[0]}{split_data[1]}", chap)
            await bot.send_message(
                event.chat_id,
                "Open this in google chrome",
                file=f"{split_data[0]}{split_data[1]}.html",
            )

        except Exception as e:
            return
            print(e)


__mod_name__ = "【ᴍᴀɴɢᴀ】"
__help__ = """
• `/manga <name of Manga>` *:* Shows Manga Info You Searched
• `/read <name of Manga>` *:* Downloads Any Manga By Search
                               
The files provided are in multiple qualities to download just open file in chrome
"""
