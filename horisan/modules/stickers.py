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

# converting a gif into a sticker method
from horisan.services.convert import convert_gif 

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
__mod_name__ = "【ꜱᴛɪᴄᴋᴇʀꜱ】" 
STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid, run_async=True)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker, run_async=True)
GETVIDSTICKER_HANDLER = DisableAbleCommandHandler("getvidsticker", getvidsticker, run_async=True)
DEL_HANDLER = DisableAbleCommandHandler("delsticker", delsticker, run_async=True)
STICKERS_HANDLER = DisableAbleCommandHandler("stickers", cb_sticker, run_async=True)
VIDEO_HANDLER = DisableAbleCommandHandler ("getvideo", video, run_async=True)
CBSCALLBACK_HANDLER = CallbackQueryHandler(cbs_callback, pattern='cbs_', run_async=True)

dispatcher.add_handler(VIDEO_HANDLER) 
dispatcher.add_handler(CBSCALLBACK_HANDLER)
dispatcher.add_handler(STICKERS_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(GETVIDSTICKER_HANDLER)
dispatcher.add_handler(DEL_HANDLER)
