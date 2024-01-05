from telebot import TeleBot
from telebot.types import Message

from ...data import set_notification_settings, show_user_database

def message_handler_alert(message: Message, bot: TeleBot):
    user = show_user_database(message.chat.id)
    
    isnotification = not user['user']['premium']['notification']
    set_notification_settings(message.chat.id, isnotification)

    if isnotification:
        bot.send_message(message.chat.id, "Has activado las notificaciones 🔔")
    else:
        bot.send_message(message.chat.id, "Has desactivado las notificaciones 🔕")