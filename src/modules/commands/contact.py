from telebot import TeleBot
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def message_handler_contact(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, "Soy un estudiante de informática 💻, entusiasta a la programación 👨‍💻. Si gustas contactarme, ¡no dudes en hacerlo! 📩",
                     reply_markup= InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="DM 📩", url='https://t.me/fcoagz')
    ))