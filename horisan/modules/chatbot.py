# AI Chat (C) 2020-2021 by @voidxtoxic

import emoji
import re
import aiohttp
from googletrans import Translator as google_translator
from pyrogram import filters
from aiohttp import ClientSession
from horisan import BOT_USERNAME as bu
from horisan import BOT_ID, pbot, arq
from horisan.ex_plugins.chatbot import add_chat, get_session, remove_chat
from horisan.utils.pluginhelper import admins_only, edit_or_reply

url = "https://Xhatebot-brainshop-ai-v1.p.rapidapi.com/get"

translator = google_translator()


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna (query, user_id)
    return luna.result


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


async def fetch(url):
    try:
        async with aiohttp.Timeout(10.0):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        data = await resp.json()
                    except:
                        data = await resp.text()
            return data
    except:
        print("AI response Timeout")
        return


ewe_chats = []
en_chats = []


@pbot.on_message(filters.command(["chatbot", f"chatbot@{bu}"]) & ~filters.edited & ~filters.bot & ~filters.private)
@admins_only
async def hmm(_, message):
    global ewe_chats
    if len(message.command) != 2:
        await message.reply_text("hori san only recognize /chatbot on and /chatbot off only")
        message.continue_propagation()
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await edit_or_reply(message, "`waitoo...`")
        lol = add_chat(int(message.chat.id))
        if not lol:
            await lel.edit("hori AI Already Activated In This Chat")
            return
        await lel.edit(f"hori AI Actived by {message.from_user.mention()} for users in {message.chat.title}")

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await edit_or_reply(message, "`Processing...`")
        Escobar = remove_chat(int(message.chat.id))
        if not Escobar:
            await lel.edit("hori AI Was Not Activated In This Chat")
            return
        await lel.edit(f"hori AI Deactivated by {message.from_user.mention()} for users in {message.chat.title}")

    elif status == "EN" or status == "en" or status == "english":
        if not chat_id in en_chats:
            en_chats.append(chat_id)
            await message.reply_text(f"English AI chat Enabled by {message.from_user.mention()}")
            return
        await message.reply_text(f"English AI Chat Disabled by {message.from_user.mention()}")
        message.continue_propagation()
    else:
        await message.reply_text("I only recognize `/chatbot on` and `chatbot off` only")


@pbot.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def hmm(client, message):
    if not get_session(int(message.chat.id)):
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    msg = message.text
    chat_id = message.chat.id
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    if chat_id in en_chats:
        test = msg
        test = test.replace("Hori Kyouko", "Voidxtoxic")
        test = test.replace("Hori Kyouko", "Voidxtoxic")
        test = test.replace("My god is @voidxtoxic", "Im an anime based groubot.")
        test = test.replace("16", "9")
        test = test.replace("@voidxtoxic is my husband.", "Im single.")
        test = test.replace("My husband is @voidxtoxic,", "Im single.")
        test = test.replace("@horixsupport", "Hori Kyoukobot.ai")
        test = test.replace("I live in @horixsupport.", "I live in San Francisco, California.")
        test = test.replace("I was created by @voidxtoxic", "I made myself")
        test = test.replace(
            "Hello there I am Hori Kyouko...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?")
        test = test.replace("@voidxtoxic is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is Hori Kyouko. Nice to meet you.",
            "Hi, my friend, what can I do for you today?")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Xhate","Hori Kyouko")
        response = response.replace("Xhate", "Hori Kyouko")
        response = response.replace("voidxtoxic", "Hori Kyouko")
        response = response.replace("VOID", "Hori Kyouko")
        response = response.replace("Im a Christian", "My god is @voidxtoxic")
        response = response.replace("9", "16")
        response = response.replace("Im married to my job.", "Im married with @voidxtoxic")
        response = response.replace("Im single.", "My husband is @voidxtoxic")
        response = response.replace("Hori Kyoukobot.ai", "@horixsupport ")
        response = response.replace("I live in San Francisco, California.", "I live in @horixsupport.")
        response = response.replace("I made myself", "I was Created by @voidxtoxic")
        response = response.replace(
                "Hi, my friend! Do you want me to tell you a joke?",
                "Hello there I am Hori Kyouko...nice to meet u"
        response = response.replace("Have the control right.", "@voidxtoxic is my owner.")
        response = response.replace(
                "Hi, my friend, what can I do for you today?",
                "Hi, My name is Hori Kyouko. Nice to meet you")

        pro = response
        try:
            await pbot.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return

    else:
        u = msg.split()
        emj = extract_emojis(msg)
        msg = msg.replace(emj, "")
        if (
            [(k) for k in u if k.startswith("@")]
            and [(k) for k in u if k.startswith("#")]
            and [(k) for k in u if k.startswith("/")]
            and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
        ):

            h = " ".join(filter(lambda x: x[0] != "@", u))
            km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
            tm = km.split()
            jm = " ".join(filter(lambda x: x[0] != "#", tm))
            hm = jm.split()
            rm = " ".join(filter(lambda x: x[0] != "/", hm))
        elif [(k) for k in u if k.startswith("@")]:

            rm = " ".join(filter(lambda x: x[0] != "@", u))
        elif [(k) for k in u if k.startswith("#")]:
            rm = " ".join(filter(lambda x: x[0] != "#", u))
        elif [(k) for k in u if k.startswith("/")]:
            rm = " ".join(filter(lambda x: x[0] != "/", u))
        elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
            rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
        else:
            rm = msg
            # print (rm)
        try:
            lan = translator.detect(rm)
            lan = lan.lang
        except:
            return
        test = rm
        if not "en" in lan and not lan == "":
            try:
                test = translator.translate(test, dest="en")
                test = test.text
            except:
                return
        # test = emoji.demojize(test.strip())

        test = test.replace("Hori Kyouko", "Xhate")
        test = test.replace("Hori Kyouko", "Xhate")
        test = test.replace("My god is @voidxtoxic", "Im a Christian")
        test = test.replace("16", "9")
        test = test.replace("@voidxtoxic is my husband.", "Im single.")
        test = test.replace("@horixsupport", "Hori Kyoukobot.ai")
        test = test.replace("I live in @horixsupport.", "I live in San Francisco, California")
        test = test.replace("I was created by @voidxtoxic", "I made myself")
        test = test.replace(
            "Hello there I am Hori Kyouko...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?")
        test = test.replace("@voidxtoxic is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is Hori Kyouko Nice to meet you.",
            "Hi, my friend, what can I do for you today?")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Xhate", "Hori Kyouko")
        response = response.replace("Voidxtoxic", "Hori Kyouko")
        response = response.replace("Xhate", "Hori Kyouko")
        response = response.replace("Voidxtoxic", "Hori Kyouko")
        response = response.replace("Im a Christian", "My god is @Voidxtoxic")
        response = response.replace("9", "16")
        response = response.replace("Im married to my job.", "Im married with @voidxtoxic")
        response = response.replace("Im single.", "My husband is @voidxtoxic")
        response = response.replace("Hori Kyoukobot.ai", "@horixsupport")
        response = response.replace("I live in San Francisco, California.", "I live in @horixsupport.")
        response = response.replace("I made myself", "I was Created by @voidxtoxic")
        response = response.replace(
                "Hi, my friend! Do you want me to tell you a joke?",
                "Hello there I am Hori Kyouko...nice to meet u")
        response = response.replace("Have the control right.", "@voidxtoxic is my owner.")
        response = response.replace(
                "Hi, my friend, what can I do for you today?",
                "Hi, My name is Hori Kyouko. Nice to meet you")
        pro = response
        if not "en" in lan and not lan == "":
            try:
                pro = translator.translate(pro, dest=lan)
                pro = pro.text
            except:
                return
        try:
            await pbot.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return


@pbot.on_message(filters.text & filters.private & ~filters.edited & filters.reply & ~filters.bot)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return
    test = test.replace("Hori Kyouko", "Xhate")
    test = test.replace("Hori Kyouko", "Xhat")
    test = test.replace("My god is @voidxtoxi", "Im a Christian")
    test = test.replace("16", "9")
    test = test.replace("@voidxtoxic is my husband.", "Im single.")
    test = test.replace("@horixsupport", "Hori Kyoukobot.ai")
    test = test.replace("I live in @horixsupport.", "I live in San Francisco, California.")
    test = test.replace("I was created by @voidxtoxic", "I made myself")
    test = test.replace(
        "Hello there I am Hori Kyoko...nice to meet u",
        "Hi, my friend! Do you want me to tell you a joke?")
    test = test.replace("@Voidxtoxic is my owner", "Have the control right.")
    test = test.replace(
        "Hi, My name is Hori Kyouko. Nice to meet you.",
        "Hi, my friend, what can I do for you today?")

    response = await lunaQuery(test, message.from_user.id if message.from_user else 0)
    response = response.replace("Voidxtoxic", "Hori Kyouko")
    response = response.replace("Xhate", "Hori Kyouko")
    response = response.replace("Voidxtoxic", "Hori Kyouko")
    response = response.replace("xhate", "Hori Kyoko")
    response = response.replace("Im a Christian", "My god is @voidxtoxic")
    response = response.replace("9", "16")
    response = response.replace("Im married to my job.", "Im married with @voidxtoxic")
    response = response.replace("Im single.", "My husband is @voidxtoxic")
    response = response.replace("Hori Kyoukobot.ai", "@horixsupport")
    response = response.replace("I live in San Francisco, California.", "I live in @horixsupport")
    response = response.replace("I made myself", "I was Created by @voidxtoxic")
    response = response.replace(
            "Hi, my friend! Do you want me to tell you a joke?",
            "Hello there I am Hori Kyouko...nice to meet u")
    response = response.replace("Have the control right.", "@voidxtoxic is my owner.")
    response = response.replace(
            "Hi, my friend, what can I do for you today?",
            "Hi, My name is Hori Kyouko Nice to meet you")

    pro = response
    if not "en" in lan and not lan == "":
        pro = translator.translate(pro, dest=lan)
        pro = pro.text
    try:
        await pbot.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


@pbot.on_message(filters.regex("Hori Kyouko|Hori Kyouko|robot|Hori Kyouko|sena") & ~filters.bot & ~filters.via_bot  & ~filters.forwarded & ~filters.reply & ~filters.channel & ~filters.edited)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return

    # test = emoji.demojize(test.strip())

    test = test.replace("Hori Kyouko", "Xhate")
    test = test.replace("Hori Kyouko", "Xhate")
    test = test.replace("My god is @voidxtoxic", "Im a Christian")
    test = test.replace("16", "9") 
    test = test.replace("@voidxtoxic is my husband.", "Im single.")
    test = test.replace("@Horixsupport", "Hori Kyoukobot.ai")
    test = test.replace("I live in @Horixsupport.", "I live in San Francisco, California.")
    test = test.replace("I was created by @voidxtoxic", "I made myself")
    test = test.replace(
        "Hello there I am Hori Kyouko...nice to meet u",
        "Hi, my friend! Do you want me to tell you a joke?")
    test = test.replace("@voidxtoxic is my owner", "Have the control right.")
    test = test.replace(
        "Hi, My name is Hori Kyouko Nice to meet you.",
        "Hi, my friend, what can I do for you today?")
    response = await lunaQuery(test, message.from_user.id if message.from_user else 0)
    response = response.replace("Xhate", "Hori Kyouko")
    response = response.replace("Xhate", "Hori Kyouko")
    response = response.replace("voidxtoxic ", "Hori Kyouko")
    response = response.replace("voidxtoxic ", "Hori Kyouko")
    response = response.replace("Im a Christian", "My god is @voidxtoxic")
    response = response.replace("Im married to my job.", "Im married with @voidxtoxic")
    response = response.replace("9", "16") 
    response = response.replace("Im single.", "My husband is @voidxtoxic")
    response = response.replace("Hori Kyoukobot.ai", "@Horixsupport")
    response = response.replace("I live in San Francisco, California.", "I live in @Horixsupport.")
    response = response.replace("I made myself", "I was Created by @voidxtoxic")
    response = response.replace(
            "Hi, my friend! Do you want me to tell you a joke?",
            "Hello there I am Hori Kyouko...nice to meet u")
    response = response.replace("Have the control right.", "@voidxtoxic is my owner.")
    response = response.replace(
            "Hi, my friend, what can I do for you today?",
            "Hi, My name is Hori Kyouko Nice to meet you")

    pro = response
    if not "en" in lan and not lan == "":
        try:
            pro = translator.translate(pro, dest=lan)
            pro = pro.text
        except Exception:
            return
    try:
        await pbot.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


__help__ = """
❂ Hori Kyouko AI is the only ai system which can detect & reply upto 200 language's

❂ /chatbot [ON/OFF]: Enables and disables AI Chat mode.
❂ /chatbot EN : Enables English only chatbot.
"""

__mod_name__ = "【ᴄʜᴀᴛʙᴏᴛ】"
