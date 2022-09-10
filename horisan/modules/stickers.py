import os
import re 
import cv2
import math
import requests
import cloudscraper 
import urllib.request as urllib
from PIL import Image
from html import escape
from pyrogram import filters
from bs4 import BeautifulSoup as bs 
from cloudscraper import CloudScraper
from horisan import pbot 
from bs4 import BeautifulSoup
from urllib.parse import quote as urlquote
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import TelegramError, Update, CallbackQuery
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram.utils.helpers import mention_html
from horisan import dispatcher
from horisan.modules.disable import DisableAbleCommandHandler

# void is so stooopid. oh im void
from horisan.modules.helper_funcs.alternate import typing_action 

combot_stickers_url = "https://combot.org/telegram/stickers?q="
 
def stickerid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", The sticker id you are replying is :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get id sticker",
            parse_mode=ParseMode.HTML,
        ) 

 
scraper = CloudScraper()
def get_cbs_data(query, page, user_id):
    # returns (text, buttons)
    text = scraper.get(f'{combot_stickers_url}{urlquote(query)}&page={page}').text
    soup = BeautifulSoup(text, 'lxml')
    div = soup.find('div', class_='page__container')
    packs = div.find_all('a', class_='sticker-pack__btn')
    titles = div.find_all('div', 'sticker-pack__title')
    has_prev_page = has_next_page = None
    highlighted_page = div.find('a', class_='pagination__link is-active')
    if highlighted_page is not None and user_id is not None:
        highlighted_page = highlighted_page.parent
        has_prev_page = highlighted_page.previous_sibling.previous_sibling is not None
        has_next_page = highlighted_page.next_sibling.next_sibling is not None
    buttons = []
    if has_prev_page:
        buttons.append(InlineKeyboardButton(text='⟨', callback_data=f'cbs_{page - 1}_{user_id}'))
    if has_next_page:
        buttons.append(InlineKeyboardButton(text='⟩', callback_data=f'cbs_{page + 1}_{user_id}'))
    buttons = InlineKeyboardMarkup([buttons]) if buttons else None
    text = f'Stickers for <code>{escape(query)}</code>:\nPage: {page}'
    if packs and titles:
        for pack, title in zip(packs, titles):
            link = pack['href']
            text += f"\n• <a href='{link}'>{escape(title.get_text())}</a>"
    elif page == 1:
        text = 'No results found, try a different term'
    else:
        text += "\n\nInterestingly, there's nothing here."
    return text, buttons
 
def cb_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    query = ' '.join(msg.text.split()[1:])
    if not query:
        msg.reply_text("Provide some term to search for a sticker pack.")
        return
    if len(query) > 50:
        msg.reply_text("Provide a search query under 50 characters")
        return
    if msg.from_user:
        user_id = msg.from_user.id
    else:
        user_id = None
    text, buttons = get_cbs_data(query, 1, user_id)
    msg.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=buttons)
 
def cbs_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    _, page, user_id = query.data.split('_', 2)
    if int(user_id) != query.from_user.id:
        query.answer('Not for you', cache_time=60 * 60)
        return
    search_query = query.message.text.split('\n', 1)[0].split(maxsplit=2)[2][:-1]
    text, buttons = get_cbs_data(search_query, int(page), query.from_user.id)
    query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=buttons)
    query.answer()
    
@typing_action
def combot_sticker(update, context):
    msg = update.effective_message
    split = msg.text.split(" ", 1)
    if len(split) == 1:
        msg.reply_text("Provide Some Name To Search For Packs.")
        return
    text = requests.get(combot_stickers_url + split[1]).text
    soup = bs(text, "lxml")
    results = soup.find_all("a", {"class": "sticker-pack__btn"})
    titles = soup.find_all("div", "sticker-pack__title")
    if not results:
        msg.reply_text("No Results Found! :(")
        return
    reply = f"Stickers for *{split[1]}*:"
    for result, title in zip(results, titles):
        link = result["href"]
        reply += f"\n• [{title.get_text()}]({link})"
    msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


@typing_action
def kang(update, context):
    msg = update.effective_message
    user = update.effective_user
    args = context.args
    packnum = 0
    packname = "a" + str(user.id) + "_by_" + context.bot.username
    packname_found = 0
    max_stickers = 120
    while packname_found == 0:
        try:
            stickerset = context.bot.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = (
                    "a"
                    + str(packnum)
                    + "_"
                    + str(user.id)
                    + "_by_"
                    + context.bot.username
                )
            else:
                packname_found = 1
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                packname_found = 1
    is_animated = False
    file_id = ""

    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            if msg.reply_to_message.sticker.is_animated:
                is_animated = True
            file_id = msg.reply_to_message.sticker.file_id

        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("ʏᴇᴀ, ɪ ᴄᴀɴ'ᴛ ᴋᴀɴɢ ᴛʜᴀᴛ.")

        kang_file = context.bot.get_file(file_id)
        if not is_animated:
            kang_file.download("kangsticker.png")
        else:
            kang_file.download("kangsticker.tgs")

        if args:
            sticker_emoji = str(args[0])
        elif msg.reply_to_message.sticker and msg.reply_to_message.sticker.emoji:
            sticker_emoji = msg.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "🤔"

        if not is_animated:
            kangsticker = "kangsticker.png"
            try:
                im = Image.open(kangsticker)
                if (im.width and im.height) < 512:
                    size1 = im.width
                    size2 = im.height
                    if im.width > im.height:
                        scale = 512 / size1
                        size1new = 512
                        size2new = size2 * scale
                    else:
                        scale = 512 / size2
                        size1new = size1 * scale
                        size2new = 512
                    size1new = math.floor(size1new)
                    size2new = math.floor(size2new)
                    sizenew = (size1new, size2new)
                    im = im.resize(sizenew)
                else:
                    maxsize = (512, 512)
                    im.thumbnail(maxsize)
                if not msg.reply_to_message.sticker:
                    im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    f"ᴋᴀɴɢᴇᴅ ✅ : [【ʏᴏᴜʀ ᴘᴀᴄᴋ】](t.me/addstickers/{packname})"
                    + f"\n\nᴇᴍᴏᴊɪ : {sticker_emoji}",
                    parse_mode=ParseMode.MARKDOWN,
                )

            except OSError as e:
                msg.reply_text("ᴛʜɪꜱ ꜰᴇᴀᴛᴜʀᴇ ɪꜱ ʀᴇᴍᴏᴠᴇᴅ ᴅᴜᴇ ᴛᴏ ᴄᴏɴᴛɪɴᴏᴜꜱ ʙᴜɢꜱ. ᴡɪʟʟ ʙᴇ ᴀᴅᴅᴇᴅ ɪꜰ ꜰɪxᴇᴅ 🎐✨")
                print(e)
                return

            except TelegramError as e:
                if e.message == "Internal Server Error: sticker set not found (500)":
                    msg.reply_text(
                        "Sticker successfully added to [pack](t.me/addstickers/%s)"
                        % packname
                        + "\n"
                        "Emoji is:" + " " + sticker_emoji,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Sticker_png_dimensions":
                    im.save(kangsticker, "PNG")
                    context.bot.add_sticker_to_set(
                        user_id=user.id,
                        name=packname,
                        png_sticker=open("kangsticker.png", "rb"),
                        emojis=sticker_emoji,
                    )
                    msg.reply_text(
                        f"ᴋᴀɴɢᴇᴅ ✅ : [【ʏᴏᴜʀ ᴘᴀᴄᴋ】](t.me/addstickers/{packname})"
                        + f"\nᴇᴍᴏᴊɪ : {sticker_emoji}",
                        parse_mode=ParseMode.MARKDOWN,
                    )
                elif e.message == "Stickers_too_much":
                    msg.reply_text("Max packsize reached. Press F to pay respect.")
                elif e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        png_sticker=open("kangsticker.png", "rb"),
                    )
                print(e)

        else:
            packname = "animated" + str(user.id) + "_by_" + context.bot.username
            packname_found = 0
            max_stickers = 50
            while packname_found == 0:
                try:
                    stickerset = context.bot.get_sticker_set(packname)
                    if len(stickerset.stickers) >= max_stickers:
                        packnum += 1
                        packname = (
                            "animated"
                            + str(packnum)
                            + "_"
                            + str(user.id)
                            + "_by_"
                            + context.bot.username
                        )
                    else:
                        packname_found = 1
                except TelegramError as e:
                    if e.message == "Stickerset_invalid":
                        packname_found = 1
            try:
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    tgs_sticker=open("kangsticker.tgs", "rb"),
                    emojis=sticker_emoji,
                )
                msg.reply_text(
                    f"ᴋᴀɴɢᴇᴅ ✅ : [【ʏᴏᴜʀ ᴘᴀᴄᴋ】](t.me/addstickers/{packname})"
                        + f"\nᴇᴍᴏᴊɪ : {sticker_emoji}",
                    parse_mode=ParseMode.MARKDOWN,
                )
            except TelegramError as e:
                if e.message == "Internal Server Error: sticker set not found (500)":
                    msg.reply_text(
                        "Sticker successfully added to [pack](t.me/addstickers/%s)"
                        % packname
                        + "\n"
                        "Emoji is:" + " " + sticker_emoji,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        tgs_sticker=open("kangsticker.tgs", "rb"),
                    )
                print(e)

    else:
        packs = "ʀᴇᴘʟʏ ᴛᴏ ɪᴍɢ/ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ꜰᴇᴀᴛᴜʀᴇ ✨\n\n"
        if packnum > 0:
            firstpackname = "a" + str(user.id) + "_by_" + context.bot.username
            for i in range(packnum + 1):
                if i == 0:
                    packs += f"[【ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ】](t.me/addstickers/{firstpackname})\n"
                else:
                    packs += f"[【ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ】{i}](t.me/addstickers/{packname})\n"
        else:
            packs += f"[【ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ】](t.me/addstickers/{packname})"
        msg.reply_text(packs, parse_mode=ParseMode.MARKDOWN)
    if os.path.isfile("kangsticker.png"):
        os.remove("kangsticker.png")
    elif os.path.isfile("kangsticker.tgs"):
        os.remove("kangsticker.tgs")


def makepack_internal(
    update,
    context,
    msg,
    user,
    emoji,
    packname,
    packnum,
    png_sticker=None,
    tgs_sticker=None,
):
    name = user.first_name
    name = name[:50]
    try:
        extra_version = " " + str(packnum) if packnum > 0 else ""
        if png_sticker:
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                f"{name}s kang pack" + extra_version,
                png_sticker=png_sticker,
                emojis=emoji,
            )
        if tgs_sticker:
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                f"{name}s animated kang pack" + extra_version,
                tgs_sticker=tgs_sticker,
                emojis=emoji,
            )

    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text(
                "Your pack can be found [here](t.me/addstickers/%s)" % packname,
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            msg.reply_text(
                "ᴍᴇᴇᴛ ᴍᴇ ɪɴ ᴘᴍ ꜰɪʀꜱᴛ ✨",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="【ᴄᴏᴍᴇ ɪɴ ᴘᴍ】", url=f"t.me/{context.bot.username}"
                            )
                        ]
                    ]
                ),
            )
        return

    if success:
        msg.reply_text(
            "ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʀᴇᴀᴛᴇᴅ : ✅ \n\n[【ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ】](t.me/addstickers/%s)"
            % packname,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        msg.reply_text("Failed to create sticker pack. Possibly due to blek mejik.")


def getsticker(update, context):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "Hello"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please check the file you requested below."
            "\nPlease use this feature wisely!",
            parse_mode=ParseMode.HTML,
        )
        context.bot.sendChatAction(chat_id, "upload_document")
        file_id = msg.reply_to_message.sticker.file_id
        newFile = context.bot.get_file(file_id)
        newFile.download("sticker.png")
        context.bot.sendDocument(chat_id, document=open("sticker.png", "rb"))
        context.bot.sendChatAction(chat_id, "upload_photo")
        context.bot.send_photo(chat_id, photo=open("sticker.png", "rb"))

    else:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "Hello"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get sticker image",
            parse_mode=ParseMode.HTML,
        )


@typing_action
def stickerid(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", The sticker id you are replying is :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get id sticker",
            parse_mode=ParseMode.HTML,
        )
 
def getsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        with BytesIO() as file:
            file.name = 'sticker.png'
            new_file = bot.get_file(file_id)
            new_file.download(out=file)
            file.seek(0)
            bot.send_document(chat_id, document=file)
    else:
        update.effective_message.reply_text(
            "Please reply to a sticker for me to upload its PNG.",
        )
      
def getvidsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker: 
        file_id = msg.reply_to_message.sticker.file_id
        new_file = bot.get_file(file_id)
        new_file.download("sticker.mp4")
        bot.send_video(chat_id, video=open("sticker.mp4", "rb"))
        os.remove("sticker.mp4")
    else:
        update.effective_message.reply_text(
         "Please reply to a video sticker to upload its MP4."
         )

        
def delsticker(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        context.bot.delete_sticker_from_set(file_id)
        msg.reply_text("Deleted!")
    else:
        update.effective_message.reply_text(
            "Please reply to sticker message to del sticker"
        )

def video(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.animation:
        file_id = msg.reply_to_message.animation.file_id
        new_file = bot.get_file(file_id)
        new_file.download("video.mp4")
        bot.send_video(chat_id, video=open("video.mp4", "rb"))
        os.remove("video.mp4")
    else:
        update.effective_message.reply_text(
            "Please reply to a gif for me to get it's video."
        )

            
        
__help__ = """
•  `/stickerid`*:* reply to a sticker to me to tell you its file ID.
•  `/getsticker`*:* reply to a sticker to me to upload its raw PNG file.
•  `/getvidsticker` *:* reply to a video sticker to me to upload it's mp4 file.
•  `/kang`or `/steal`*:* reply to a sticker/video sticker/animated sticker to add it to your pack.
•  `/delsticker`*:* Reply to your anime exist sticker to your pack to delete it.
•  `/stickers`*:* Find stickers for given term on combot sticker catalogue 
•  `/getvideo`*:* reply to a gif to get video easily !
Please Use 512/512 size Sticker to kang else it will cause internal problem.
And sometimes video sticker might not kang because of more Size than 512/512.
"""
__mod_name__ = "ꜱᴛɪᴄᴋᴇʀꜱ" 
KANG_HANDLER = DisableAbleCommandHandler(
    ["kang", "steal", "k"],
    kang,
    pass_args=True,
    run_async=True,
)
STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid, run_async=True)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker, run_async=True)
GETVIDSTICKER_HANDLER = DisableAbleCommandHandler("getvidsticker", getvidsticker, run_async=True)
DEL_HANDLER = DisableAbleCommandHandler("delsticker", delsticker, run_async=True)
STICKERS_HANDLER = DisableAbleCommandHandler("stickers", cb_sticker, run_async=True)
VIDEO_HANDLER = DisableAbleCommandHandler ("getvideo", video, run_async=True)
CBSCALLBACK_HANDLER = CallbackQueryHandler(cbs_callback, pattern='cbs_', run_async=True)

dispatcher.add_handler(KANG_HANDLER)
dispatcher.add_handler(VIDEO_HANDLER) 
dispatcher.add_handler(CBSCALLBACK_HANDLER)
dispatcher.add_handler(STICKERS_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(GETVIDSTICKER_HANDLER)
dispatcher.add_handler(DEL_HANDLER)
