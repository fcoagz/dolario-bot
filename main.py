import os

from dotenv import load_dotenv
from telebot import TeleBot


from src.modules.commands import (
    message_handler_start,
    message_handler_dollar,
    message_handler_configuration,
    message_handler_contact,
    message_handler_alert,
    message_handler_help
)
from src.modules.callbacks import func_callback_inline
from src.updating import updating

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
parse_mode = os.getenv("PARSE_MODE")

bot = TeleBot(bot_token, parse_mode, disable_web_page_preview=False, disable_notification=True)

bot.register_message_handler(message_handler_start, commands=['start', 'reset'], pass_bot=True)
bot.register_message_handler(message_handler_dollar, commands=['dollar'], pass_bot=True)
bot.register_message_handler(message_handler_help, commands=['help'], pass_bot=True)
bot.register_message_handler(message_handler_contact, commands=['contact'], pass_bot=True)
bot.register_message_handler(message_handler_configuration, commands=['configuration'], pass_bot=True)
bot.register_message_handler(message_handler_alert, commands=['alert'], pass_bot=True)

bot.register_callback_query_handler(func_callback_inline, func=None, pass_bot=True)

updating()
bot.infinity_polling()