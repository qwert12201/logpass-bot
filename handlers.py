from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from db import db_session
import inline
from models import Logpass

PAGE_SIZE = 20

def start(update: Update, context: CallbackContext):
    context.user_data['offset'] = 0
    username = update.message.chat.username
    update.message.reply_text(
        f'Привет, {username}!',
        reply_markup=inline.logpass_kb())

def handle(update: Update, context: CallbackContext):
    context.user_data['offset'] = 0
    offset = context.user_data['offset']
    items = db_session.query(Logpass).slice(offset, offset + PAGE_SIZE)
    result = "".join(item.logpass for item in items)

    keyboard = [[InlineKeyboardButton("→", callback_data="page")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data['offset'] = offset + PAGE_SIZE

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=result,
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext):
    last_text = "Логпассы закончились"
    query = update.callback_query
    query.answer()
    if query.data == "page":
        offset = context.user_data.get('offset', 0)
        text = next_page(offset)
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("→", callback_data="page")]]
        )
        context.user_data['offset'] = offset + PAGE_SIZE
    query.edit_message_text(text=text, reply_markup=reply_markup)
    if offset == 240:
        query.edit_message_reply_markup(reply_markup=None)
        update.callback_query.message.reply_text(last_text)

def next_page(offset):
    items = db_session.query(Logpass).slice(offset, offset + PAGE_SIZE)
    return "".join(item.logpass for item in items)


if __name__ == "__main__":
    print(handle())
