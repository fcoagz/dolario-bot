import json

from telebot import TeleBot
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from ...data import show_user_database
from ...utils.dollar import getdate

def _edit_symbol(symbol: str):
    if symbol == '▲':
        return '🔺'
    elif symbol == '▼':
        return '🔻'
    else:
        return '🟰'

def _get_values_dollar_text(user_id: int):
    user = show_user_database(user_id)
    user_file_path  = user['user']['premium']['configuration']['path']

    with open(user_file_path, 'r') as f:
        data = json.load(f)
    return list(data)

def message_handler_dollar(message: Message, bot: TeleBot):
    user = show_user_database(message.chat.id)

    if not user['user']['premium']['configuration']['show_dollar']:
            bot.send_message(message.chat.id, "No tiene configurado el dólar, 🙏 por favor ingresa aquí ⚙️ para que vayas a configuración.",
                             reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='⚙️ Configuración', callback_data='configuration')))
    else:
        try:
            if user['user']['premium']['configuration']['show_dollar'] == "text":
                message_text = f"Los siguientes precios del dolar del día <b>{getdate()['date']}. {getdate()['time']}</b> son los siguientes:\n\n"
                monitors = _get_values_dollar_text(message.chat.id)
                    
                for x in range(len(monitors)):
                    message_text += f"|<b>{monitors[x]['title']}</b>|\n"
                    message_text += f"Precio: {monitors[x]['price']}\n"
                    message_text += f"Porcentaje: {_edit_symbol(monitors[x]['symbol'])}{monitors[x]['percent']}\n"
                    message_text += f"Última actualización: {monitors[x]['last_update']}\n\n"
                bot.send_message(message.chat.id, message_text, reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton(text='💱 Conversión', callback_data='conversion')))
        except:
            bot.send_message(message.chat.id, "En un rato te avisaremos para que tus ajustes queden guardados en la base de datos. Debido a muchas peticiones, estás en cola ⏳")

def func_callback_inline_type_convertion(message: Message, bot: TeleBot):
    message_convertion = {
        'text': """
Presiona el tipo de conversión que deseas hacer: si es en <b>USD</b> o en <b>Bolívares</b> 💰. Al seleccionar una de ellas, deberás introducir el monto de la moneda que elegiste 📝. Luego, te estaré mostrando la lista 📋 de los monitores con los precios de la otra moneda 💱.
""",
        'reply_markup': InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text='USD', callback_data='convertion-usd'),
        InlineKeyboardButton(text='BS', callback_data='convertion-bs')
        )
    }

    bot.send_message(message.chat.id, **message_convertion)

def step_input_value(currency: str, message: Message, bot: TeleBot):
    msg = bot.edit_message_text(chat_id=message.chat.id, text="Ahora, por favor ingresa el monto 💰 que te gustaría consultar en los monitores con los precios de la otra moneda 💱.\n\n <code>El valor puede ser entera o decimal</code>\n\nEnvia /exit para salir.",
                                message_id=message.message_id)
    bot.register_next_step_handler(msg, lambda m: show_values_dollar(currency, m, bot))

def show_values_dollar(currency: str, message: Message, bot: TeleBot):
    value = message.text.replace(',', '.')

    if message.text.startswith('/'):
        if message.text == '/exit':
            bot.send_message(message.chat.id, "No se realizará ninguna conversión. Lista de comandos. /help")
        return

    try:
        monitors = _get_values_dollar_text(message.chat.id)
                
        message_text = f"La siguiente conversión de los precios, según los monitores, es la siguiente:\n\n"
        for x in range(len(monitors)):
            convertion = f"Bs. {round(float(value) * float(monitors[x]['price']), 2)}" if currency == 'usd' else f"$ {round(float(value) / float(monitors[x]['price']), 2)}"
            message_text += f"|<b>{monitors[x]['title']}</b>|\n"
            message_text += f"Precio: {monitors[x]['price']}\n"
            message_text += f"<b>Conversión</b>: {f'$ {value}' if currency == 'usd' else f'Bs. {value}'} ➡️ {convertion}\n\n"
        bot.send_message(message.chat.id, message_text, reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='💱 Conversión', callback_data='conversion')))
    except:
        msg = bot.send_message(message.chat.id, "Por favor ingresa el monto 💰 que te gustaría consultar en los monitores con los precios de la otra moneda 💱. \n\n<code>El valor puede ser entera o decimal</code>")
        bot.register_next_step_handler(msg, lambda m: show_values_dollar(currency, m, bot))   