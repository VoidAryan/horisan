import html
import re
import os
import requests
import datetime
import platform
import time

from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
from platform import python_version
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import events

from telegram import (
    MAX_MESSAGE_LENGTH,
    ParseMode,
    Update,
    MessageEntity,
    __version__ as ptbver,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown, mention_html

from horisan import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    INFOPIC,
    dispatcher,
    sw,
    StartTime,
    SUPPORT_CHAT,
)
from horisan.__main__ import STATS, TOKEN, USER_INFO
from horisan.modules.sql import SESSION
import horisan.modules.sql.userinfo_sql as sql
from horisan.modules.disable import DisableAbleCommandHandler
from horisan.modules.sql.global_bans_sql import is_user_gbanned
from horisan.modules.sql.afk_redis import is_user_afk, start_afk
from horisan.modules.sql.users_sql import get_user_num_chats
from horisan.modules.helper_funcs.chat_status import sudo_plus
from horisan.modules.helper_funcs.extraction import extract_user
from horisan import telethn


def sinfo(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        message.reply_text("I can't extract a user from this.")
        return

    else:
        return

    rep = message.reply_text("<code>Intel About This User...</code>", parse_mode=ParseMode.HTML)

    text = (
        f"「<b> 【ɪɴꜰᴏ ᴏꜰ ᴛʜɪꜱ ᴜꜱᴇʀ】</b> 」\n"
        f"───────────────────\n"
        f"× ID: <code>{user.id}</code>\n"
        f"× First Name: {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n× Last Name: {html.escape(user.last_name)}"

    if user.username:
        text += f"\n× Username: @{html.escape(user.username)}"

    text += f"\n× Userlink: {mention_html(user.id, 'link')}"

    if chat.type != "private" and user_id != bot.id:
        _stext = "\n× State In This Chat: <code>{}</code>"
        

        afk_st = is_user_afk(user.id)
        if afk_st:
            text += _stext.format("AFK")
        else:
            status = status = bot.get_chat_member(chat.id, user.id).status
            if status:
                if status in {"left", "kicked"}:
                    text += _stext.format("Not here")
                elif status == "member":
                    text += _stext.format("Detected")
                elif status in {"administrator", "creator"}:
                    text += _stext.format("Admin")
    if user_id not in [bot.id, 777000, 1087968824]:
        userhp = hpmanager(user)
        text += f"\n───────────────────"
        text += f"\n<b>Health:</b> <code>{userhp['earnedhp']}/{userhp['totalhp']}</code>\n[<i>{make_bar(int(userhp['percentage']))} </i>{userhp['percentage']}%]"
        text += f"\n───────────────────"
    try:
        spamwtc = sw.get_ban(int(user.id))
        if spamwtc:
            text += "\n\n<b>This person is Spamwatched!</b>"
            text += f"\nReason: <pre>{spamwtc.reason}</pre>"
            text += "\nAppeal at @HorixSupport"
    except:
        pass  # don't crash if api is down somehow...

    disaster_level_present = False

    if user.id == OWNER_ID:
        text += "\n\n۞ VOID's Wifey ♡ With Disaster : President 👑"
        disaster_level_present = True
    elif user.id in DEV_USERS:
        text += "\n\n۞ The Disaster level of this person is 'Vice President'."
        disaster_level_present = True
    elif user.id in DRAGONS:
        text += "\n\n۞ The Disaster level of this person is 'Advisor'."
        disaster_level_present = True
    elif user.id in DEMONS:
        text += "\n\n۞ The Disaster level of this person is 'Secretary'."

    disaster_level_present = True

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}",
            )
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result["custom_title"]
                text += f"\n\nTitle:\n<b>{custom_title}</b>"
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id)
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id)
        if mod_info:
            text += "\n\n" + mod_info

    if INFOPIC:
        try:
            profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
            context.bot.sendChatAction(chat.id, "upload_photo")
            context.bot.send_photo(
                chat.id,
                photo=profile,
                caption=(text),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "【Health】", url="https://t.me/hori_x_updates/7"
                            ),
                            InlineKeyboardButton(
                                "【Disaster】", url="https://t.me/hori_x_updates/6"
                            ),
                        ],
                    ]
                ),
                parse_mode=ParseMode.HTML,
            )

        # Incase user don't have profile pic, send normal text
        except IndexError:
            message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "【Health】", url="https://t.me/hori_x_updates/7"
                            ),
                            InlineKeyboardButton(
                                "【Disaster】", url="https://t.me/hori_x_updates/6"
                            ),
                        ],
                    ]
                ),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )

    else:
        message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
        )

    rep.delete()
   
    
__help__ = """
*SINFO:*
❂ /sinfo*:* Get Your Info But In Smaller Size.
"""

INFO_HANDLER = DisableAbleCommandHandler("sinfo", sinfo, run_async=True)

dispatcher.add_handler(INFO_HANDLER)

__mod_name__ = "【sɪɴꜰᴏ】"
__command_list__ = ["info"]
__handlers__ = [
    INFO_HANDLER
    ]
    
    
    
