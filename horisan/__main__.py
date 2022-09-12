import html
import os
import json
import importlib
import time
import re
import sys
import traceback
import horisan.modules.sql.users_sql as sql
from sys import argv
from typing import Optional
from telegram import __version__ as peler
from platform import python_version as memek
from horisan import (
    ALLOW_EXCL,
    CERT_PATH,
    DONATION_LINK,
    BOT_USERNAME as bu,
    LOGGER,
    OWNER_ID,
    PORT,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    pbot,
    updater,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from horisan.modules import ALL_MODULES
from horisan.modules.helper_funcs.chat_status import is_user_admin
from horisan.modules.helper_funcs.misc import paginate_modules
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


GROUP_START_IMG = "https://telegra.ph/file/ace3cc2757f843ff71330.jpg"

PM_START_TEXT = """
*ᴋᴏɴɪᴄʜɪᴡᴀ! {}!*
۞ ɪᴍ ᴋʏᴏᴜᴋᴏ ʜᴏʀɪ ᴀɴ ᴀɴɪᴍᴇ ʙᴀꜱᴇᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ. [👋](https://telegra.ph/file/ace3cc2757f843ff71330.jpg)
───────────────────────
× *Aʟɪᴠᴇ Sɪɴᴄᴇ:* {}
× {} *Wᴇᴇʙꜱ, Aᴄʀᴏꜱꜱ* {} *Cʜᴀᴛꜱ*
───────────────────────
۞ ɪᴍ ʜᴇʀᴇ ᴛᴏ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢᴄ ᴍᴏʀᴇ ᴇꜰꜰɪᴄɪᴇɴᴛʟʏ!
"""

buttons = [
    [
        InlineKeyboardButton(
            text="【Aᴅᴅ Kʏᴏᴜᴋᴏ Tᴏ Yᴏᴜʀ GC】",
            url="https://t.me/HoriXProbot?startgroup=new",
        ),
    ],
    [
        InlineKeyboardButton(text="【HELP】", callback_data="help_back"),
        InlineKeyboardButton(text="【About】", callback_data="hori_"),
    ],
]


HELP_STRINGS = """
ᴍʏ ᴀʙɪʟɪᴛɪᴇꜱ ᴀɴᴅ ɢᴜɪᴅᴇ 💫 :

۞ Kyouko Hori ɪꜱ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ ʜɪɢʜʟʏ ᴜᴘᴅᴀᴛᴇᴅ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ. 
۞ ʏᴏᴜ ᴄᴀɴ ꜱᴜᴘᴘᴏʀᴛ ᴏᴜʀ ᴡᴏʀᴋ ʙʏ ᴜꜱɪɴɢ /ᴅᴏɴᴀᴛɪᴏɴ 
۞ ᴄʟɪᴄᴋ ᴏɴ ʙᴜᴛᴛᴏɴꜱ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴛᴏ ꜱᴇᴇ ɢᴜɪᴅᴇ ꜰᴏʀ ᴜꜱɪɴɢ ᴛʜᴇᴍ. 
۞ ᴛʜɪꜱ ʙᴏᴛ ɪꜱ ᴅᴇᴠᴇʟᴏᴘᴇᴅ ᴜɴᴅᴇʀ【V๏ɪ፝֟𝔡】 [✨](https://telegra.ph/file/6a74e747aa1262f8a778a.jpg)"""


DONATE_STRING = """Heya, glad to hear you want to donate! ❤ \

 You can support the project by contacting @Kyoukoxsupport \
 If you can't donate us financially support us by helping in growth of hori san \
 Those who cannot provide monetary support are welcome to help us we are here to hear you."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("horisan.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="【Go Back】", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_text(
                PM_START_TEXT.format(
                    escape_markdown(first_name),
                    escape_markdown(uptime),
                    sql.num_users(),
                    sql.num_chats()),                        
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
            )
              
    else:
        update.effective_message.reply_photo(
            GROUP_START_IMG,
            caption="<code> Hey there I am with you Since</code>: <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="【Support】", url="https://t.me/kyoukoxsupport"
                        ),
                    ],
                ]
            ),
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors

def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="【Hᴇʟᴘ Mᴇɴᴜ】", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )   
            
        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass

def hori_about_callback(update, context):
    query = update.callback_query
    if query.data == "hori_":
        query.message.edit_text(
            text="ɪᴍ ᴋʏᴏᴜᴋᴏ ʜᴏʀɪ ʙᴏᴛ ʙᴀꜱᴇᴅ ᴏɴ ᴍᴀɪɴ ᴄʜᴀʀᴀᴄᴛᴇʀ ꜰʀᴏᴍ ᴀɴɪᴍᴇ ɴᴀᴍᴇᴅ ʜᴏʀɪᴍɪʏᴀ 🥀"
            "\n\n۞ ᴋʏᴏᴜᴋᴏ ʜᴀᴠᴇ ᴠᴀʀɪᴏᴜꜱ ꜰᴇᴀᴛᴜʀᴇꜱ ɪɴ ɪᴛ ꜱᴜᴄʜ ᴀꜱ ꜰʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ / ᴀɴᴛɪᴄʜᴀɴɴᴇʟ / ᴀɴᴛɪɴꜱꜰᴡ / ᴡᴀʀɴꜱ / ʙᴀɴꜱ / ɢʟᴏʙᴀʟ ʙᴀɴꜱ / ʀᴇᴍɪɴᴅᴇʀ / ꜰɪʟᴛᴇʀꜱ. ᴇᴛᴄ ᴡʜɪᴄʜ ᴍᴀᴋᴇꜱ ʏᴏᴜʀ ɢʀᴏᴜᴘᴄʜᴀᴛꜱ ᴍᴏʀᴇ ᴇꜰꜰᴇᴄᴛɪᴠᴇ ᴀɴᴅ ᴍᴀɴᴀɢᴇᴅ"
            "\n۞ ᴋʏᴏᴜᴋᴏ ᴡᴀꜱ ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ [V O I D](https://t.me/voidaryan)"
            "\n۞ ᴄᴜʀʀᴇɴᴛʟʏ ᴡᴏʀᴋɪɴɢ ᴜɴᴅᴇʀ [【V๏ɪ፝֟𝔡】✧Network✧](https://t.me/voidxnetwork)"
            "\n\n× ᴋʏᴏᴜᴋᴏ ʜᴏʀɪ ᴡᴀꜱ ʙᴜɪʟᴛ ʙʏ ᴜꜱɪɴɢ ᴇᴍɪᴋᴏʀᴏʙᴏᴛ ᴀꜱ ʙᴀꜱᴇ. ꜱᴏ ᴛʜᴀɴᴋꜱ ᴛᴏ ᴛʜᴇᴍ. ᴀɴᴅ ᴡᴇ ʟɪᴋᴇ ᴛᴏ ɢɪᴠᴇ ʀᴇꜱᴘᴇᴄᴛ ᴛᴏ ᴛʜᴇ ᴘᴇᴏᴘʟᴇ ᴡʜᴏ ᴡᴏʀᴋᴇᴅ ᴡɪᴛʜ ᴜꜱ ᴀꜱ ᴅᴇᴠꜱ ɪɴ ᴏᴜʀ ᴅᴀɪʟʏ ᴜᴘᴅᴀᴛᴇꜱ. ᴀɴᴅ ᴄʀᴇᴅɪᴛꜱ ᴛᴏ ᴛʜᴏꜱᴇ ᴡʜᴏ'ꜱ ᴍᴏᴅᴜʟᴇꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ᴜꜱᴇᴅ ɪɴ ʜᴏʀɪ. ❤️ ᴡᴇ ʀᴇꜱᴘᴇᴄᴛ ʏᴏᴜʀ ꜱᴜᴘᴘᴏʀᴛ ᴡɪᴛʜ ᴜꜱ.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="【ChatGroup】", callback_data="hori_chat"),
                    InlineKeyboardButton(text="【Channels】", callback_data="hori_channel"),
                 ],
                 [
                    InlineKeyboardButton(text="【Our Domain】", callback_data="hori_support"),
                    InlineKeyboardButton(text="【Github】", url="https://github.com/voidxtoxic"),
                 ],
                 [
                    InlineKeyboardButton(text="【V๏ɪ፝֟𝔡】✧Network✧", callback_data="hori_network"),
                 ],
                 [
                    InlineKeyboardButton(text="【Home】", callback_data="hori_back"),
                 ]
                ]
            ),
        )
    elif query.data == "hori_back":
        first_name = update.effective_user.first_name
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            PM_START_TEXT.format(
                escape_markdown(first_name),
                escape_markdown(uptime),
                sql.num_users(),
                sql.num_chats()),                        
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )

    elif query.data == "hori_chat":
        query.message.edit_text(
            text=f"*ʜᴇʟʟᴏ,*"
            "\nꜱᴏ ʏᴏᴜʀᴇ ɪɴᴛʀᴇꜱᴛᴇᴅ ɪɴ ᴊᴏɪɴɪɴɢ ᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ...ɪ ꜱᴇᴇ ɪᴍ ɢʟᴀᴅ. 🥀"
            "\n*ᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ ɪꜱ ᴀɴ ᴇɴɢʟɪꜱʜ ɢʀᴏᴜᴘ ᴡʜɪᴄʜ ᴍᴀɪɴᴛᴀɪɴꜱ ᴘᴇᴀᴄᴇ ᴀɴᴅ ʟᴏᴠᴇ ꜱᴏ ᴍᴀᴋᴇ ꜱᴜʀᴇ ʏᴏᴜ ʀᴇᴀᴅ ʀᴜʟᴇꜱ ᴛᴏ ᴀᴠᴏɪᴅ ᴡᴀʀɴꜱ ᴀɴᴅ ʙᴀɴꜱ.*"
            "\n*⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯*"
            "\n--| [ʜᴏʀɪᴍɪʏᴀ ꜰᴀᴍɪʟʏ](https://t.me/+CgTTj7-fLv03NDI1) |--"
            "\n*⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯*",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton(text="【Group】", url="https://t.me/+CgTTj7-fLv03NDI1"),
                    InlineKeyboardButton(text="【Rules】", url="https://telegra.ph/R%E1%B4%9C%CA%9F%E1%B4%87s--R%E1%B4%87%C9%A2%E1%B4%9C%CA%9F%E1%B4%80%E1%B4%9B%C9%AA%E1%B4%8F%C9%B4s-B%CA%8F-H%E1%B4%8F%CA%80%C9%AA%E1%B4%8D%C9%AA%CA%8F%E1%B4%80-F%E1%B4%80%E1%B4%8D%C9%AA%CA%9F%CA%8F-02-23"),
                 ],
                    [InlineKeyboardButton(text="【Back】", callback_data="hori_")]
                ]
            ),
        )

    elif query.data == "hori_channel":
        query.message.edit_text(
            text=f"ʜᴇʟʟᴏ,"
            "\nꜱᴏ ʏᴏᴜʀᴇ ɪɴᴛʀᴇꜱᴛᴇᴅ ɪɴ ᴊᴏɪɴɪɴɢ ᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ...ɪ ꜱᴇᴇ ɪᴍ ɢʟᴀᴅ ♡"
            "\nᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ᴀʀᴇ ᴄʀᴇᴀᴛᴇᴅ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ꜱᴛᴜꜰꜰꜱ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ᴀɴɪᴍᴇ. ʟɪᴋᴇ ᴍᴇᴍᴇꜱ / ᴀɴɪᴍᴇ ᴇᴛᴄ. ♡"
            "\n\nᴄʜᴇᴄᴋ ᴏᴜᴛ ᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ 👇",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton(text="【Anime】", url="https://t.me/anime_uploadz"),
                    InlineKeyboardButton(text="【Memes】", url="https://t.me/horimiya_summons"),
                 ],
                    [InlineKeyboardButton(text="【Back】", callback_data="hori_")]
                ]
            ),
        )
        
    elif query.data == "hori_support":
        query.message.edit_text(
            text="ʜᴏʀɪ ꜱᴜᴘᴘᴏʀᴛ | ᴜᴘᴅᴀᴛᴇꜱ ™"
            "\nᴊᴏɪɴ ᴍʏ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ᴛᴏ ʀᴇᴘᴏʀᴛ ᴀ ᴘʀᴏʙʟᴇᴍ ᴏɴ ʜᴏʀɪ. ʏᴏᴜ ᴄᴀɴ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇꜱ ᴀꜱᴡᴇʟʟ ꜱᴏ ʏᴏᴜ ɢᴇᴛ ɴᴏᴛɪꜰɪᴇᴅ ᴀʙᴏᴜᴛ ʜᴏʀɪ ᴀɴᴅ ɪᴛꜱ ꜰᴜᴛᴜʀᴇ ᴜᴘᴅᴀᴛᴇꜱ ᴀɴᴅ ᴀʟʟ 💫",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="【Support】", url="t.me/kyoukoxsupport"),
                        InlineKeyboardButton(
                            text="【Updates】", url="https://t.me/hori_x_updates"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="【Back】", callback_data="hori_"),
                    ],
                ]
            ),
        )

    elif query.data == "hori_network":
        query.message.edit_text(
            text=f"【V๏ɪ፝֟𝔡】✧Network✧\n"
            "\n◈ Void is an anime based Community with a motive to spread love and peace around telegram. Go through the channel and join the Community if it draws your attention. ◈",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="【Network】", url="https://t.me/voidxnetwork"
                        ),
                        InlineKeyboardButton(
                            text="【Bot】", url="https://t.me/voidxnetworkbot"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="【Back】", callback_data="hori_"),
                    ],
                ]
            ),
        )


def Source_about_callback(update, context):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text="๏›› This advance command for Musicplayer."
            "\n\n๏ Command for admins only."
            "\n • `/reload` - For refreshing the adminlist."
            "\n • `/pause` - To pause the playback."
            "\n • `/resume` - To resuming the playback You've paused."
            "\n • `/skip` - To skipping the player."
            "\n • `/end` - For end the playback."
            "\n • `/musicplayer <on/off>` - Toggle for turn ON or turn OFF the musicplayer."
            "\n\n๏ Command for all members."
            "\n • `/play` <query /reply audio> - Playing music via YouTube."
            "\n • `/playlist` - To playing a playlist of groups or your personal playlist",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="【Back】", callback_data="hori_")]]
            ),
        )
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(
                escape_markdown(first_name),
                escape_markdown(uptime),
                sql.num_users(),
                sql.num_chats()),                        
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_photo(
                "https://telegra.ph/file/250fa84d9d9abfc05904b.jpg",
                caption=f"Baka 💫 contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="【HELP】",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_photo(
            "https://telegra.ph/file/250fa84d9d9abfc05904b.jpg",
            caption=f"Baka 💫 contact me in PM to get the list of possible commands.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="【HELP】",
                            url="t.me/{}?start=help".format(context.bot.username),
                        )
                    ]
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="【Back】", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="【Back】",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi baka! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi baka! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="【Settings】",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 1606221784:
            update.effective_message.reply_text(
                "I'm free for everyone ❤️ If you wanna make me smile, just join"
                "[My Channel]({})".format(DONATION_LINK),
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "I've PM'ed you about donating to my creator!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "Contact me in PM first to get donation information."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                f"@{SUPPORT_CHAT}",
                "https://telegra.ph/file/98a2be2030b5ffb057815.jpg",     #@RyuIsGod
                "ɪ ᴀᴍ ᴀʟɪᴠᴇ ᴠᴏɪᴅ ꜱᴀᴍᴀ 🥀",
                parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                  [                  
                       InlineKeyboardButton(
                             text="【 SYSTEM STATS 】",
                             callback_data="stats_callback")
                     ] 
                ]
            ),  
        )
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    test_handler = CommandHandler("test", test, run_async=True)
    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True
    )

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True
    )

    about_callback_handler = CallbackQueryHandler(
        hori_about_callback, pattern=r"hori_", run_async=True
    )

    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_", run_async=True
    )

    donate_handler = CommandHandler("donate", donate, run_async=True)
    migrate_handler = MessageHandler(
        Filters.status_update.migrate, migrate_chats, run_async=True
    )

    dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(source_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4,drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
      

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
