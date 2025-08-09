from telegram import ReplyKeyboardMarkup

from models import Logpass
from db import db_session

def logpass_kb() -> ReplyKeyboardMarkup:
    btns = [
        ['Логпассы'],
    ]
    return ReplyKeyboardMarkup(btns, resize_keyboard=True)

def message_kb() -> ReplyKeyboardMarkup:
    btns = [
        ['->'],
    ]
    return ReplyKeyboardMarkup(btns, resize_keyboard=True)

def load_logpass(name: str):
    with open(name, "r", encoding="utf-8") as f:
        a = f.readlines()
        print("Чтение файла завершено")
        for logpass in a:
            db_session.add(Logpass(logpass=logpass))
    db_session.commit()


if __name__ == "__main__":
    load_logpass("logpass.txt")
    print("Сохранено в датабазу")
