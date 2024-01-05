import os, time
from datetime import datetime
from threading import Thread

from pytz import timezone

from .data.database import path_accounts, show_user_database
from .data.accounts.files import (
    create_file_text_in_database,
    add_path_file_in_database,
    set_status_message
)
from .utils.dollar import getdate, get_value_dollar, ExchangeMonitor
from .utils.message_direct import send_message

path_text = f"{path_accounts}/files/text"
caracas = timezone("America/Caracas")

def handler_new_changes():
    users = [int(user_id.replace('u', '').replace('.json', '')) 
             for user_id in os.listdir(path_accounts)[1:]]
    
    date = datetime.now(caracas)
    days = getdate()['date'].split(',')[0]

    for x in range(len(users)):
        user = show_user_database(users[x])

        user_id    = user['id']
        first_name = user['user']['first_name']
        ispremium  = user['user']['premium']['ispremium']
        path       = user['user']['premium']['configuration']['path']
        show_dolar = user['user']['premium']['configuration']['show_dollar']
        hours      = user['user']['premium']['configuration']['updated_hours']
        total_monitors = user['user']['premium']['configuration']['monitors']
        notification = user['user']['premium']['notification']

        if ispremium and show_dolar:
            get_monitors = get_value_dollar('dollar_premium', provider=ExchangeMonitor)
            monitors = [get_monitors[monitor] for monitor in get_monitors if monitor in total_monitors]
        
            if show_dolar == "text":
                create_file_text_in_database(user_id, monitors)
                if not path:
                    user_file_path = os.path.join(path_text, f"u{user_id}.json")
                    add_path_file_in_database(user_file_path, user_id)

                    send_message(user_id, "Acabo de actualizar tu base de datos, ve ingresa a 💲 para que veas los monitores que elegiste a mostrar.", reply_markup={
                        'inline_keyboard': [[{'text':'💰 Dolar', 'callback_data':'dollar'}]]
                    })

                if notification and len(hours) > 0 and not days in ['sábado', 'domingo']:
                    current_date = date.strftime("%H:%M:%S")
                    
                    for x in range(len(hours)):
                        if hours[x]['time'][:2] == current_date[:2]:
                            if hours[x]['time'] <= current_date and not hours[x]['message']:
                                set_status_message(user_id, x, message=True)
                                welcome = f"Buenos dias {first_name} ☀️" if int(hours[x]['time'][:2]) < 12 else f"Buenas tardes {first_name} 🌆"
                                
                                send_message(user_id, f"{welcome}, te notifico que el dólar acaba de ser actualizado 💵. Presiona el botón para que veas el nuevo cambio.", reply_markup={
                                    'inline_keyboard': [[{'text':'💰 Dolar', 'callback_data':'dollar'}]]
                                })
                        else:
                            set_status_message(user_id, x, message=False)

def run():
    while True:
        handler_new_changes()
        time.sleep(120)

def updating():
    t = Thread(target=run)
    t.start()