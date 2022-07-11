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
import horisan.modules.sql.users_sql as sql
from horisan import (
    OWNER_ID,
    DRAGONS,
    DEMONS,
    DEV_USERS,
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
            "title": "System Stats",
            "description": "System Stats of kyouko hori",
            "message_text": "Click the button below to get System Stats.",
            "thumb_urL": "https://telegra.ph/file/5adc1fd5632f64f379a51.jpg",
            "keyboard": ".stats",
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
        ".stats": stats,
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
        
def stats(query: str, update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    user_id = update.effective_user.id
    user = context.bot.get_chat(user_id)
    sql.update_user(user.id, user.username)
    about_text = f"""
    • [Kyouko • Stats](https://t.me/HoriXProbot) \n\n• Click The Button Below To Check Out System Stats Of Kyouko
    """
    results: list = []
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="S Y S T E M • S T A T S",
                    Callback_data="stats_callback",
                ),

            ],
            ])

    results.append(
        InlineQueryResultPhoto(
            id=str(uuid4()),
            title="System Stats",
            description="System Stats Of Kyouko Hori",
            thumb_url="https://telegra.ph/file/6fc4c7a913dfcd415e7fd.jpg",
            photo_url="https://telegra.ph/file/6fc4c7a913dfcd415e7fd.jpg",
            caption=about_text,
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
