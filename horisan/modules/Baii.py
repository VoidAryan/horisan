from horisan import dispatcher
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode

from telegram.ext import (
    CallbackContext,
    CommandHandler,
)

PHOTO = "https://telegra.ph/file/242d186b33c49c0329a0f.mp4"



def baiibaii(update: Update, context: CallbackContext):

    TEXT = f"Baii-Baii  {mention} 👋"

    update.effective_message.reply_photo(
        PHOTO, caption= TEXT,
        parse_mode=ParseMode.MARKDOWN,

            reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="【V๏ɪ፝֟𝔡】Network", url="https://t.me/voidxnetwork")]
            ]
        ),
    )


baiibaii_handler = CommandHandler("baiibaii", baiibaii, run_async = True)
dispatcher.add_handler(baiibaii_handler)

__mod_name__ = "【baiibaii】"
