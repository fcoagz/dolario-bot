from telebot import TeleBot
from telebot.types import Message

premium = """
Aquí te ofrezco todos los comandos 📜 que puedes utilizar del bot 🤖 y cuál es su función:

/dollar: Muestra el valor actual del dólar 💵 de los monitores que preferiste que se mostraran. 
/configuration: Puedes personalizar el bot a tu gusto, seleccionar los monitores a mostrar en /dollar, establecer la hora en que desea que te avise, desactivar los anuncios y notificaciones y viceversa 🔧. 
/alert: Un comando directo que te permite activar las notificaciones 🔔 para recibir actualizaciones sobre el valor del dólar y viceversa. 
/help: Proporciona ayuda con los comandos 🆘. 
/contact: Permite ponerse en contacto con el desarrollador 📞.

Para utilizar Dolario+ deberás de configurarlo yendo al comando /configuration o su botón correspondiente, los monitores a mostrar y la hora que te gustaría que te notifique (es opcional). Esperas unos minutos para que el bot actualice en la base de datos. ¿Por qué se tarda? El bot se monitorea y verifica si ese usuario no sea un bot, al fin al cabo te estará avisando entre 3 a 5 minutos. Poco a poco estaremos agilizando el procedimiento 🚀.
"""

def message_handler_help(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, premium)