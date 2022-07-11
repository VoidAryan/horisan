import html
import socket
import random
import sys
from time import time
import json
from datetime import datetime
from platform import python_version
from typing import List
from uuid import uuid4
from pyrogram import __version__ as pyrover
from pyrogram import filters, errors

import requests
from telegram import InlineQueryResultArticle, ParseMode, InlineQueryResultPhoto, InputTextMessageContent, Update, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram import __version__
from telegram.error import BadRequest
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          Filters, MessageHandler)
from telegram.utils.helpers import mention_html
import horisan.modules.sql.global_bans_sql as gban

import horisan.modules.sql.users_sql as sql
from horisan import (
    OWNER_ID,
    DRAGONS,
    DEMONS,
    DEV_USERS,
    EVENT_LOGS,
    TIGERS,
    WOLVES,
    pgram,
    sw, LOGGER
)
from horisan.modules.helper_funcs.misc import article
from horisan.modules.helper_funcs.decorators import Horinline
from horisan.modules.sudoers import bot_sys_stats as bss


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        text = text.replace(prefix, "", 1)
    return text

@Horinline()
def inlinequery(update: Update, _) -> None:
    """
    Main InlineQueryHandler callback.
    """
    query = update.inline_query.query
    user = update.effective_user

    results: List = []
    inline_help_dicts = [
        {
            "title": "O W N E R",
            "description": "He's Creator Of Me !",
            "message_text": "Link to my owner sama! 👑",
            "thumb_urL": "https://telegra.ph/file/40d4f0659dd7468ae376a.jpg",
            "keyboard": ".void",
        },
         {
            "title": "Anime Channel",
            "description": "Anime Providing Channel For Watching Anime",
            "message_text": "Click the button below to Watch Anime in our channel.",
            "thumb_urL": "https://telegra.ph/file/6638fd2dd521bf1ee6e2b.jpg",
            "keyboard": ".anime",
        },
        {
            "title": "Kyouko • Hori",
            "description": "Kyouko Hori Inline...",
            "message_text": "Click the button below to get the Kyouko Inline.",
            "thumb_urL": "https://telegra.ph/file/0eb9add961031411f5312.jpg",
            "keyboard": ".hori",
        },
        {
            "title": "【V๏ɪ፝֟𝔡】◈Network◈",
            "description": "Kyouko Works Under 【V๏ɪ፝֟𝔡】◈Network◈",
            "message_text": "Click the button to check out 【V๏ɪ፝֟𝔡】◈Network◈",
            "thumb_urL": "https://telegra.ph/file/2d49d53bace654813fa37.jpg",
            "keyboard": ".network",
        },
        {
            "title": "Account info on Hori",
            "description": "Look up a Telegram account in Kuouko database",
            "message_text": "Click the button below to look up a person in Kyouko database using their Telegram ID",
            "thumb_urL": "https://telegra.ph/file/5adc1fd5632f64f379a51.jpg",
            "keyboard": ".info",
        },
        {
            "title": "Help",
            "description": "Help Inline Commands",
            "message_text": "Click the button below to get Help Of Inline Commands.",
            "thumb_urL": "https://telegra.ph/file/5adc1fd5632f64f379a51.jpg",
            "keyboard": ".guide",
        },
        {
            "title": "Anilist",
            "description": "Search anime and manga on AniList.co",
            "message_text": "Click the button below to search anime and manga on AniList.co",
            "thumb_urL": "https://telegra.ph/file/68bb30a3aee0a98cb501a.jpg",
            "keyboard": ".anilist",
        },
    ]

    inline_funcs = {
        ".info": inlineinfo,
        ".void": void,
        ".hori": hori,  
        ".anime": anime,
        ".network": network,
        ".anilist": media_query,
        #".gban" : Gban,
        ".guide": guide,
    }

    if (f := query.split(" ", 1)[0]) in inline_funcs:
        inline_funcs[f](remove_prefix(query, f).strip(), update, user)
    else:
        for ihelp in inline_help_dicts:
            results.append(
                article(
                    title=ihelp["title"],
                    description=ihelp["description"],
                    message_text=ihelp["message_text"],
                    thumb_url=ihelp["thumb_urL"],
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Click Here",
                                    switch_inline_query_current_chat=ihelp[
                                        "keyboard"
                                    ],
                                )
                            ]
                        ]
                    ),
                )
            )

        update.inline_query.answer(results, cache_time=5)


def inlineinfo(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    bot = context.bot
    query = update.inline_query.query
    LOGGER.info(query)
    user_id = update.effective_user.id

    try:
        search = query.split(" ", 1)[1]
    except IndexError:
        search = user_id

    try:
        user = bot.get_chat(int(search))
    except (BadRequest, ValueError):
        user = bot.get_chat(user_id)

    chat = update.effective_chat
    sql.update_user(user.id, user.username)

    text = (
        f"<b>Information:</b>\n"
        f"• ID: <code>{user.id}</code>\n"
        f"• First Name: {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n• Last Name: {html.escape(user.last_name)}"

    if user.username:
        text += f"\n• Username: @{html.escape(user.username)}"

    text += f"\n• Permanent user link: {mention_html(user.id, 'link')}"

    nation_level_present = False

    if user.id == OWNER_ID:
        text += f"\n\nThis person is VOID'S wife aka : Owner 👑"
        nation_level_present = True
    elif user.id in DEV_USERS:
        text += f"\n\nThis Person is Vice-president 💫"
        nation_level_present = True
    elif user.id in DRAGONS:
        text += f"\n\nThe Only Advisors Are Here ! 🔱"
        nation_level_present = True
    elif user.id in DEMONS:
        text += f"\n\nMy helpers here for GanFight 💢"
        nation_level_present = True
    elif user.id in TIGERS:
        text += f"\n\nThe Nation level of this person is Tiger Level Disaster"
        nation_level_present = True
    elif user.id in WOLVES:
        text += f"\n\nThe Nation level of this person is Wolf Level Disaster"
        nation_level_present = True

    if nation_level_present:
        text += ' [<a href="https://t.me/{}?start=nations">?</a>]'.format(bot.username)

    try:
        spamwtc = sw.get_ban(int(user.id))
        if spamwtc:
            text += "<b>\n\n• SpamWatched:\n</b> Yes"
            text += f"\n• Reason: <pre>{spamwtc.reason}</pre>"
            text += "\n• Appeal at @Kyoukoxsupport"
        else:
            text += "<b>\n\n• SpamWatched:</b> No"
    except:
        pass  # don't crash if api is down somehow...

    num_chats = sql.get_user_num_chats(user.id)
    text += f"\n• <b>Chat count</b>: <code>{num_chats}</code>"




    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Report Error",
                    url=f"https://t.me/Kyoukoxsupport",
                ),
                InlineKeyboardButton(
                    text="Search again",
                    switch_inline_query_current_chat=".info ",
                ),

            ],
        ]
        )

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            thumb_url="https://telegra.ph/file/1f8bf7dd687617a7e9d8c.jpg",
            title=f"User info of {html.escape(user.first_name)}",
            input_message_content=InputTextMessageContent(text, parse_mode=ParseMode.HTML,
                                                          disable_web_page_preview=True),
            reply_markup=kb
        ),
    ]

    update.inline_query.answer(results, cache_time=5)


def void(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user_id = update.effective_user.id
    user = context.bot.get_chat(user_id)
    sql.update_user(user.id, user.username)
    about_text = f"""
    • [V O I D](https://t.me/Void_Toxic) \n\n• My Izumi Kun aka the reason why im able to serve you all. 👑
    """
    results: list = []
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="V O I D",
                    url=f"https://t.me/void_toxic",
                ),

            ],
            ])

    results.append(
        InlineQueryResultPhoto(
            id=str(uuid4()),
            title="VOID",
            description="Creator Of Hori",
            thumb_url="https://telegra.ph/file/58c5ce909c2add2928f97.jpg",
            photo_url="https://telegra.ph/file/40d4f0659dd7468ae376a.jpg",
            caption=about_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb,
        )
    )
    update.inline_query.answer(results)
    
def hori(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user_id = update.effective_user.id
    user = context.bot.get_chat(user_id)
    sql.update_user(user.id, user.username)
    about_text = f"""
    ──── Kyouko-Hori ────\n\n👑 Advanced Group Management Bot. Developed to manage your groupchats effectively and efficiently 🔱
    """
    results: list = []
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Hori X ProBot",
                    url=f"https://t.me/HoriXProbot",
                ),

            ],
            [
                InlineKeyboardButton(
                    text="Support",
                    url=f"https://t.me/Kyoukoxsupport",
                ),
                 InlineKeyboardButton(
                    text="Updates",
                    url=f"https://t.me/hori_x_updates",
                ),

            ],
            [
                InlineKeyboardButton(
                    text="Try Inline",
                    switch_inline_query_current_chat="",
                ),

            ],
        ])

    results.append(
        InlineQueryResultPhoto(
            id=str(uuid4()),
            title="Kyouko-Hori",
            description="Get Hori Inline",
            thumb_url="https://telegra.ph/file/38072e410a01ed891b2e3.jpg",
            photo_url="https://telegra.ph/file/38072e410a01ed891b2e3.jpg",
            caption=about_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb,
        )
    )
    update.inline_query.answer(results)

MEDIA_QUERY = '''query ($search: String) {
  Page (perPage: 10) {
    media (search: $search) {
      id
      title {
        romaji
        english
        native
      }
      type
      format
      status
      description
      episodes
      bannerImage
      duration
      chapters
      volumes
      genres
      synonyms
      averageScore
      airingSchedule(notYetAired: true) {
        nodes {
          airingAt
          timeUntilAiring
          episode
        }
      }
      siteUrl
    }
  }
}'''


def media_query(query: str, update: Update, context: CallbackContext) -> None:
    """
    Handle anime inline query.
    """
    results: List = []

    try:
        results: List = []
        r = requests.post('https://graphql.anilist.co',
                          data=json.dumps({'query': MEDIA_QUERY, 'variables': {'search': query}}),
                          headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        res = r.json()
        data = res['data']['Page']['media']
        res = data
        for data in res:
            title_en = data["title"].get("english") or "N/A"
            title_ja = data["title"].get("romaji") or "N/A"
            format = data.get("format") or "N/A"
            type = data.get("type") or "N/A"
            bannerimg = data.get("bannerImage") or "https://telegra.ph/file/cc83a0b7102ad1d7b1cb3.jpg"
            try:
                des = data.get("description").replace("<br>", "").replace("</br>", "")
                description = des.replace("<i>", "").replace("</i>", "") or "N/A"
            except AttributeError:
                description = data.get("description")

            try:
                description = html.escape(description)
            except AttributeError:
                description = description or "N/A"

            if len((str(description))) > 700:
                description = description [0:700] + "....."

            avgsc = data.get("averageScore") or "N/A"
            status = data.get("status") or "N/A"
            genres = data.get("genres") or "N/A"
            genres = ", ".join(genres)
            img = f"https://img.anili.st/media/{data['id']}" or "https://telegra.ph/file/cc83a0b7102ad1d7b1cb3.jpg"
            aurl = data.get("siteUrl")


            kb = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Read More",
                            url=aurl,
                        ),
                        InlineKeyboardButton(
                            text="Search again",
                            switch_inline_query_current_chat=".anilist ",
                        ),

                    ],
                ])

            txt = f"<b>{title_en} | {title_ja}</b>\n"
            txt += f"<b>Format</b>: <code>{format}</code>\n"
            txt += f"<b>Type</b>: <code>{type}</code>\n"
            txt += f"<b>Average Score</b>: <code>{avgsc}</code>\n"
            txt += f"<b>Status</b>: <code>{status}</code>\n"
            txt += f"<b>Genres</b>: <code>{genres}</code>\n"
            txt += f"<b>Description</b>: <code>{description}</code>\n"
            txt += f"<a href='{img}'>&#xad</a>"

            results.append(
                InlineQueryResultArticle
                    (
                    id=str(uuid4()),
                    title=f"{title_en} | {title_ja} | {format}",
                    thumb_url=img,
                    description=f"{description}",
                    input_message_content=InputTextMessageContent(txt, parse_mode=ParseMode.HTML,
                                                                  disable_web_page_preview=False),
                    reply_markup=kb
                )
            )
    except Exception as e:

        kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Report error",
                        url="https://t.me/Kyoukoxsupport",
                    ),
                    InlineKeyboardButton(
                        text="Search again",
                        switch_inline_query_current_chat=".anilist ",
                    ),

                ],
            ])

        results.append(

            InlineQueryResultArticle
                (
                id=str(uuid4()),
                title=f"Media {query} not found",
                input_message_content=InputTextMessageContent(f"Media {query} not found due to {e}", parse_mode=ParseMode.MARKDOWN,
                                                              disable_web_page_preview=True),
                reply_markup=kb
            )

        )

    update.inline_query.answer(results, cache_time=5)

def guide(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user_id = update.effective_user.id
    user = context.bot.get_chat(user_id)
    sql.update_user(user.id, user.username)
    help_text = f"""
     [Kyouko Inline Help](https://t.me/HoriXProbot)\n*Inline Help Commands:*\n*• .void:* `Get Link To Owner's ID`\n*• .network* `To Check Out VOID Network`\n*• .anilist:* `To Search Animes And Mangas`\n*• .info:* `To Check Your Information`\n• Want your own inline on @HoriXProbot? You can get it in low pricing by contacting @Void_Toxic
     """
    results: list = []
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Search Inline",
                    switch_inline_query_current_chat=".info ",
                ),

            ],
        ])

    results.append(
        InlineQueryResultPhoto(
            id=str(uuid4()),
            title="Help Commands",
            thumb_url="https://telegra.ph/file/fdbd57db7c25061c87cb2.jpg",
            photo_url="https://telegra.ph/file/fdbd57db7c25061c87cb2.jpg",
            caption=help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb,
        )
    )
    update.inline_query.answer(results)

@pgram.on_callback_query(filters.regex("pingCB"))
async def stats_callbacc(_, CallbackQuery):
    text = await bss()
    await pgram.answer_callback_query(CallbackQuery.id, text, show_alert=True)

def _netcat(host, port, update: Update, context: CallbackContext):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    content = update.inline_query.query.split(" ", 1)[1]
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()
    
def network(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user_id = update.effective_user.id
    user = context.bot.get_chat(user_id)
    sql.update_user(user.id, user.username)
    about_text = f"""
    ──── • 【V๏ɪ፝֟𝔡】Network • ────\n\nVoid is an anime based Community with a motive to spread love and peace around telegram. Go through the channel and join the Community if it draws your attention.
    """
    results: list = []
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="【V๏ɪ፝֟𝔡】Network",
                    url=f"https://t.me/VoidxNetwork",
                ),

            ],
            [
                InlineKeyboardButton(
                    text="| Head-Quarters |",
                    url=f"t.me/void_headquarters",
                ),

            ],
        ])

    results.append(
        InlineQueryResultPhoto(
            id=str(uuid4()),
            title="【V๏ɪ፝֟𝔡】Network",
            description="【V๏ɪ፝֟𝔡】Network At your Domain.",
            thumb_url="https://telegra.ph/file/f33fa9857280297eae877.jpg",
            photo_url="https://telegra.ph/file/f33fa9857280297eae877.jpg",
            caption=about_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb,
        )
    )
    update.inline_query.answer(results)
    
def anime(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user_id = update.effective_user.id
    user = context.bot.get_chat(user_id)
    sql.update_user(user.id, user.username)
    about_text = f"""
    ‣ Anime Uploadz \n\n• Uploading All The Latest Animes \n• Best Quality, Low Size Encoded \n• One Tap Channel Access
    """
    results: list = []
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Anime Uploadz",
                    url=f"https://t.me/Anime_Uploadz",
                ),

            ],
            [
                InlineKeyboardButton(
                    text="Index",
                    url=f"https://t.me/indexuploadz",
                ),

            ],
        ])

    results.append(
        InlineQueryResultPhoto(
            id=str(uuid4()),
            title="Anime",
            description="Get Anime Uploadz Link",
            thumb_url="https://telegra.ph/file/e1ab80fc0c68556062115.jpg",
            photo_url="https://telegra.ph/file/e1ab80fc0c68556062115.jpg",
            caption=about_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb,
        )
    )
    update.inline_query.answer(results)


def gban (query: str, update: Update, context: CallbackContext) -> None:
    bot = context.bot
    v = update.inline_query.query
    user = update.effective_user
    chat = update.effective_chat
    voidgay = v.split(" ", 1)[1]
    reason = v.split(" ", 2)[2]
    useri = bot.get_chat(voidgay)
    user_id = useri["id"]
    username =  useri["username"]
    first_name = useri["first_name"]
    results: list = []
    answers = results
    if gban.is_user_gbanned(user_id):
       if not reason:
            msg = (
                "This user is already gbanned; I'd change the reason, but you haven't given me one...",
            )
            answers.append(InlineQueryResultArticle(
                            id=str(uuid4())
                            title=f"{msg}",
                            input_message_content=InputTextMessageContent(msg, disable_web_page_preview=True),
                            
            return

        old_reason = gban.update_gban_reason(
            user_id, username or first_name, reason)
        if old_reason:
            msg = (
                "This dummy is already gbanned, for the following reason:\n"
                "<code>{}</code>\n"
                "I've gone and updated it with your new reason! waito..".format(
                    html.escape(old_reason),
                ),
                parse_mode=ParseMode.HTML,
            )
            answers.append(InlineQueryResultArticle(
                            id=str(uuid4())
                            title=f"Old Gban reason is available",
                            input_message_content=InputTextMessageContent(msg, disable_web_page_preview=True),
                            

        else:
            msg= (
                "This jerk is already gbanned, but had no reason set; I've gone and updated it!",
            )
            answers.append(InlineQueryResultArticle(
                            id=str(uuid4())
                            title=f"Update old reason ",
                            input_message_content=InputTextMessageContent(msg, disable_web_page_preview=True),
                            
        return
          
        
    if chat.type != "private":
        chat_origin = "<b>{} ({})</b>\n".format(html.escape(chat.title), chat.id)
    else:
        chat_origin = "<b>{}</b>\n".format(chat.id)

    log_message = (
        f"#GBANNED @Voidxgay\n"
        
        f"<b>× Originated from:</b> <code>{chat_origin}</code>\n"
        f"<b>× Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>× Banned Jerk:</b> {mention_html(useri.id, useri.first_name)}\n"
        f"<b>× Banned Jerk ID:</b> <code>{useri.id}</code>\n"
        
        f"<b>Event Stamp:</b> <code>{current_time}</code>"
    )

    if reason:
            log_message += f"\n<b>Reason:</b> <code>{reason}</code>"

    if EVENT_LOGS:
        try:
            log = bot.send_message(EVENT_LOGS, log_message, parse_mode=ParseMode.HTML)
        except:
            pass
   gban.gban_user(user_id, username or first_name, reason)
   msg = ("User {} has been gbanned sucessfully".format(first_name))
   answers.append(InlineQueryResultArticle(
                            id=str(uuid4())
                            title=f"{}".format(first_name),
                            input_message_content=InputTextMessageContent(msg, disable_web_page_preview=True),
    
   update.inline_query.answer(results)
