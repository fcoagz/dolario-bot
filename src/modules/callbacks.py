from telebot import TeleBot
from telebot.types import CallbackQuery

from .commands import (
    message_handler_dollar,
    message_handler_configuration,
    message_handler_help
)
from .commands.dollar import func_callback_inline_type_convertion, step_input_value
from .commands.configuration import (
    func_callback_inline_dollar,
    func_callback_inline_updateHours,
    func_callback_inline_notification
)

functions = {
    'dollar': message_handler_dollar,
    'configuration': message_handler_configuration,
    'help': message_handler_help,
    'conversion': func_callback_inline_type_convertion,
}

def func_callback_inline(call: CallbackQuery, bot: TeleBot):
    process = functions.get(call.data, None)

    if not process and len(call.data.split('config-')) > 1:
        data_split = call.data.split('config-')

        if data_split[1] == 'dollar':
            func_callback_inline_dollar(call.message, bot)
        elif data_split[1] == 'updateHours':
            func_callback_inline_updateHours(call.message, bot)
        elif data_split[1] == 'notification':
            func_callback_inline_notification(call, bot)
    elif not process and len(call.data.split('convertion-')) > 1:
        data_split = call.data.split('convertion-')
        step_input_value(data_split[1], call.message, bot)
    else:
        message_handler = process
        message_handler(call.message, bot)
