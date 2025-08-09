from telegram import BotCommand
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

import settings
import handlers

def main():
    bot = Updater(settings.API_TOKEN)
    dp = bot.dispatcher
    bot.bot.set_my_commands([
        BotCommand("/start", "Запускает бота"), 
    ])
    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(MessageHandler(Filters.regex('^(Логпассы)$'), handlers.handle))
    dp.add_handler(CallbackQueryHandler(handlers.button))
    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
