# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json
import os


def get_user_list(config, key):
    with open("{}/horisan/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 1740964  # integer value, dont use ""
    API_HASH = "9a5e481e09b79b5a71ca3686ca5eee32"
    TOKEN = "5143473546:AAEXoAfOXExYSAo6mXc3hdUomRVcGTNd1J4"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 5043575895  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "Manjirou_Sama"
    SUPPORT_CHAT = "HoriXSupport"  # Your own group for support, do not add the @
    JOIN_LOGGER = (
        -1001633814912
    )  # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = (
        -1001633814912
    )  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    ERROR_LOGS = (
        -1001633814912
    )
    ARQ_API_KEY  = "ZRUXOL-UKJQCM-YEEBKE-RXLZEB-ARQ"
    ARQ_API_URL  = "ZRUXOL-UKJQCM-YEEBKE-RXLZEB-ARQ"
    DATABASE_URL = "postgres://wjcsfqzd:YQEJY-66M1lKyXC4rZ1dMb45neHsYs96@batyr.db.elephantsql.com/wjcsfqzd"
    BOT_ID = 5143473546
    BOT_USERNAME = "kyoukohori_robot"
    DEMONS = get_user_list("elevated_users.json", "demons")
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    ALLOW_EXCL = "TRUE"
    ALLOW_CHATS = "TRUE"
    CASH_API_KEY = "-xyz"
    DEL_CMDS = "True"
    DONATION_LINK = "https://t.me/HoriXSupport"
    MONGO_DB_URI = "mongodb+srv://ub:ub123@horivc.cemtd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    ENV = "ANYTHING"
    NO_LOAD = "rss"
    STRICT_GBAN = "True"
    STRING_SESSION = "1AZWarzYBuzEz3d57bNnrzgdVTMjupyvtlO6lHm7L6jqrRlxHeoBL_HKB25EWE-hos5aFVjE3QpbKm1nkcVXG5xdtP61F6HW5d9Qzu9qtQq2VKl_pzjNH7Ln2SXvwW5Z_ZD7BdiIQGa5bD15l3aIX8zZateDHLL1gAHpy_5h7p5O7hjeYkWIC7luhpZz-X5iQ-ztEp2-K7sZu5Tc-oo8bHC-UFRc_mrnCTLp3SmovgTyXiXYocbNdCR-ymIghOkW01sYocd64ND4rBaCP79VagugOfsOrvnj-ifDDp5j02hRFoi5oVhq2QMZ7Bix7oBdJrxaB8bAei3gobBFKgVWSwIvt0PEwHwg="
    DRAGONS = get_user_list("elevated_users.json", "dragons")
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "wolves")
    TIME_API_KEY = "-xyz"
    WALL_API = "6950f559377140a4e1594c564cdca6a3"
    REM_BG_API_KEY = None 
    
    
    # RECOMMENDED
    DB_URL = os.environ.get("DATABASE_URL")  # needed for any database modules
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    WORKERS = (
        8  # Number of subthreads to use. Set as number of threads your processor uses
    )
    BAN_STICKER = ""  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = (
        "awoo"  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "awoo"  # Get your API key from https://timezonedb.com/api
    WALL_API = (
        "awoo"  # For wallpapers, get one from https://wall.alphacoders.com/api.php
    )
    AI_API_KEY = "awoo"  # For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
