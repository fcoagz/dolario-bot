from datetime import time

from telebot import TeleBot
from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)

from ...data import (
    show_user_database,
    set_dollar_settings,
    set_hours_settings,
    set_notification_settings
    )
from ...utils.dollar import get_value_dollar, ExchangeMonitor

configuration_dollar = {}
type_dollar = {
    '📄 Texto': "text"
    # '🖼️ Imagen': "image"
}

tmonitors = ['bancamiga', 'banco_de_venezuela', 'banesco', 'banplus', 'bbva_provincial', 
             'bcv', 'binance', 'amazon_gift_card', 'enparalelovzla',
             'mercantil','paypal','dolartoday']

def message_handler_configuration(message: Message, bot: TeleBot):
    configuracion = {
        'text': """
La finalidad de esta versión es permitirte configurar el bot a tu gusto. Puedes seleccionar qué monitores de dólar mostrar, decidir cómo quieres que se muestre la información y establecer la hora en la que deseas que se actualice. A continuación, te ofrecemos las siguientes opciones de configuración:
""",
        'reply_markup': InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("💵 Dollar", callback_data="config-dollar"),
            InlineKeyboardButton("⏰ Hora en actualizar", callback_data="config-updateHours"),
            InlineKeyboardButton("🔔 Notificar", callback_data="config-notification")
        )
    }
    bot.send_message(message.chat.id, **configuracion)

def func_callback_inline_dollar(message: Message, bot: TeleBot):
    msg = bot.send_message(message.chat.id, "📈 Indícame cómo quieres que se muestre el dólar:", reply_markup=ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton('📄 Texto')))
    bot.register_next_step_handler(msg, lambda m: step_get_total_monitors(m, bot))

def step_get_total_monitors(message: Message, bot: TeleBot):
    if message.text in ['📄 Texto']:
        configuration_dollar[message.chat.id] = {}
        configuration_dollar[message.chat.id]['show_dollar'] = type_dollar.get(message.text)

        total_monitors = """
¡Aquí tienes una lista de los monitores disponibles! 😊🔍

1- <b>Bancamiga</b> | <code>bancamiga</code>
2- <b>Banco de Venezuela</b> | <code>banco_de_venezuela</code>
3- <b>Banesco</b> | <code>banesco</code>
4- <b>Banplus</b> | <code>banplus</code>
5- <b>BBVA Provincial</b> | <code>bbva_provincial</code>
6- <b>BCV</b> | <code>bcv</code>
7- <b>Binance</b> | <code>binance</code>
8- <b>Amazon Gift Card</b> | <code>amazon_gift_card</code>
9- <b>EnParaleloVzla</b> | <code>enparalelovzla</code>
10- <b>Mercantil</b> | <code>mercantil</code>
11- <b>PayPal</b> | <code>paypal</code>
12- <b>DolarToday</b> | <code>dolartoday</code>
"""
        introduction_monitor = """
📋 Envíame una lista de los monitores que quieres que te muestren. Utiliza este formato:

<code>6,9,2</code> -> Ingresa el número correspondiente al monitor (separado por comas)

Tienes permitido seleccionar de 3️⃣ hasta 5️⃣ monitores. Próximamente iremos incrementando.
    """
       
        bot.send_message(message.chat.id, total_monitors, reply_markup=ReplyKeyboardRemove())
        msg = bot.send_message(message.chat.id, introduction_monitor)
        bot.register_next_step_handler(msg, lambda m: step_save_user_data(m, bot))
    else:
        msg = bot.send_message(message.chat.id, "Por favor, asegúrate de haber elegido entre <code>📄 Texto</code> y <code>🖼️ Imagen</code>")
        bot.register_next_step_handler(msg, lambda m: step_get_total_monitors(m, bot))

def step_save_user_data(message: Message, bot: TeleBot):
    try:
        selection_int = [int(index) for index in str(message.text).split(',')]
        monitors = [tmonitors[monitor-1] for monitor in selection_int]

        if len(monitors) >= 3 and len(monitors) <= 5:
            configuration_dollar[message.chat.id]['monitors'] = []
            for monitor in monitors:
                configuration_dollar[message.chat.id]['monitors'].append(monitor)
            configuration_dollar[message.chat.id]['total_monitor'] = len(configuration_dollar[message.chat.id]['monitors'])
            
            set_dollar_settings(message.chat.id, **configuration_dollar[message.chat.id])
            bot.send_message(message.chat.id, "¡Se ha guardado exitosamente! ✅🎉 En un rato te avisaremos para que tus ajustes queden guardados en la base de datos. Debido a muchas peticiones, estás en cola ⏳")
        else:
            msg = bot.send_message(message.chat.id, "Por favor, asegúrate de haber elegido entre 3 y 5 monitores.")
            bot.register_next_step_handler(msg, lambda m: step_save_user_data(m, bot))
    except IndexError:
        msg = bot.send_message(message.chat.id, "Número inválido de selecciones. Por favor, asegúrate de haber elegido entre 3 y 5 monitores.")
        bot.register_next_step_handler(msg, lambda m: step_save_user_data(m, bot))

def func_callback_inline_updateHours(message: Message, bot: TeleBot):
    configuration_dollar[message.chat.id] = {}
    configuration_dollar[message.chat.id]['updated_hours'] = []

    msg = bot.send_message(message.chat.id, """
🕒 Puedes ingresar hasta dos horas diferentes para recibir notificaciones. Elige la primera hora de la mañana ⏰☀️ y la segunda hora de la tarde ⏰🌙. Utilizando este formato en horario de 24 horas:\n\n<code>9:45\n13:15</code>.\n\nEnvia /exit para salir.
""")
    bot.register_next_step_handler(msg, lambda m: step_save_hours(m, bot))

def step_save_hours(message: Message, bot: TeleBot):
    if message.text.startswith('/'):
        if message.text == '/exit':
            bot.send_message(message.chat.id, "No se agregara nada establecido. Lista de comandos. /help")
        return

    if not len(configuration_dollar[message.chat.id]['updated_hours']) > 0:
        try:
            if int(message.text.split(':')[0]) > 12:
                msg = bot.send_message(message.chat.id, "Has ingresado la primera hora de la tarde ⏰🌙. Por favor, ingresa la siguiente:")
            else:
                msg = bot.send_message(message.chat.id, "Has ingresado la primera hora de la mañana ⏰☀️. Por favor, ingresa la siguiente:")
            
            hour, minute = message.text.split(":")
            configuration_dollar[message.chat.id]['updated_hours'].append({"time": str(time(int(hour), int(minute))), "message": False})
            bot.register_next_step_handler(msg, lambda m: step_save_hours(m, bot))
        except ValueError:
            msg = bot.send_message(message.chat.id, "Por favor, asegúrate de haber elegido la hora correspondiente. Utilice el formato HH:MM.")
            bot.register_next_step_handler(msg, lambda m: step_save_hours(m, bot))
    else:
        try:
            if int(message.text.split(':')[0]) > 12:
                bot.send_message(message.chat.id, "Has elegido la segunda hora de la tarde ⏰🌙.")
            else:
                bot.send_message(message.chat.id, "Has elegido la segunda hora de la mañana ⏰☀️.")
            
            hour, minute = message.text.split(":")
            configuration_dollar[message.chat.id]['updated_hours'].append({"time": str(time(int(hour), int(minute))), "message": False})
            set_hours_settings(message.chat.id, configuration_dollar[message.chat.id]['updated_hours'])
            
            bot.send_message(message.chat.id, "¡Se ha guardado exitosamente! ✅🎉")
        except ValueError:
            msg = bot.send_message(message.chat.id, "Por favor, asegúrate de haber elegido la hora correspondiente. Utilice el formato HH:MM.")
            bot.register_next_step_handler(msg, lambda m: step_save_hours(m, bot))

def func_callback_inline_notification(call: CallbackQuery, bot: TeleBot):
    info_user = dict(show_user_database(call.message.chat.id))
    isnotification = not info_user['user']['premium']['notification']
    set_notification_settings(call.message.chat.id, isnotification)

    if isnotification:
        bot.answer_callback_query(call.id, "Has activado las notificaciones")
    else:
        bot.answer_callback_query(call.id, "Has desactivado las notificaciones")