from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import CallbackContext

from db import db_session
import inline
from models import Logpass

PAGE_SIZE = 110

def start(update: Update, context: CallbackContext):
    username = update.message.chat.username
    update.message.reply_text(
        f'Привет, {username}!',
        reply_markup=inline.logpass_kb())

def handle(update: Update, context: CallbackContext):
    context.user_data['offset'] = 0
    offset = context.user_data['offset']
    text = next_page(offset)
    keyboard = [[InlineKeyboardButton("→", callback_data="page")]]
    update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    offset = context.user_data.get('offset', 0)
    total_items = db_session.query(Logpass).count()
    if query.data == "page":
        text = next_page(offset)
        new_offset = offset + PAGE_SIZE
        keyboard = []
        if new_offset < total_items:
            keyboard.append([InlineKeyboardButton("→", callback_data="page")])
        if new_offset > 0:
            keyboard.append([InlineKeyboardButton("←", callback_data="page-down")])
        context.user_data['offset'] = new_offset
    elif query.data == "page-down":
        new_offset = max(0, offset - PAGE_SIZE)
        text = previous_page(new_offset)
        keyboard = []
        if new_offset + PAGE_SIZE < total_items:
            keyboard.append([InlineKeyboardButton("→", callback_data="page")])
        if new_offset > 0:
            keyboard.append([InlineKeyboardButton("←", callback_data="page-down")])
        context.user_data['offset'] = new_offset
    query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

def next_page(offset):
    items = db_session.query(Logpass).slice(offset, offset + PAGE_SIZE)
    return "".join(item.logpass for item in items)

def previous_page(offset):
    items = db_session.query(Logpass).slice(offset, offset - PAGE_SIZE)
    return "".join(item.logpass for item in items)


if __name__ == "__main__":
    total_items = db_session.query(Logpass).count()
    print(total_items)
