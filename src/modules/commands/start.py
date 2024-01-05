import os
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone

from telebot import TeleBot
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from ...data import (
    check_user_existence,
    create_user_in_database,
    show_user_database
)
from ...classes import User

load_dotenv()
name_bot = os.getenv('NAME')
caracas = timezone("America/Caracas")

def message_handler_start(message: Message, bot: TeleBot):
    if not check_user_existence(message.chat.id):
        date = datetime.now(caracas)
        date_str = date.strftime("%d/%m/%Y")

        data = {
            'id': message.chat.id,
            'created': date_str,
            'user': {
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
                'username': message.from_user.username,
                'premium': {
                    'ispremium': True,
                    'notification': True,
                    'advertisements': True,
                    'configuration': {
                        'show_dollar': None,
                        'path': None,
                        'total_monitors': 0,
                        'monitors': [],
                        'updated_hours': []
                    }
                }
            }
        }
        create_user_in_database(User(**data))

    user = show_user_database(message.chat.id)
    full_name = user['user']['first_name']

    if user['user']['last_name']:
        full_name += f" {user['user']['last_name']}"
    
    premium = {
        'text': f"""
¡Hola {full_name}! 🤗 Con {name_bot}+ puedes obtener el valor actual del dólar en Venezuela en tiempo real. 💵⏰

Aquí están algunos comandos que puedes usar:

<b>/dollar</b>: Muestra el valor actual del dólar. 💰
<b>/configuration</b>: Personaliza la configuración del bot. ⚙️
<b>/alert</b>: Activa las notificaciones para recibir actualizaciones sobre el valor del dólar. 🚨
<b>/help</b>: Proporciona ayuda con los comandos. 🆘
<b>/contact</b>: Permite ponerse en contacto con el desarrollador. 📞
    """,
        'reply_markup': InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text='💰 Dolar', callback_data='dollar'),
            InlineKeyboardButton(text='🆘 Help', callback_data='help'),
            InlineKeyboardButton(text='⚙️ Configuración', callback_data='configuration'))
    }

    bot.send_message(message.chat.id, **premium)
