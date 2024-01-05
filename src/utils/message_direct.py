import os

import requests
from dotenv import load_dotenv

from ..data import show_user_database

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

def send(endpoint: str, params: dict):
    url = f'https://api.telegram.org/bot{bot_token}/{endpoint}'
    response = requests.post(url, json=params)

    return response

def send_message(chat_id: int, text: str, reply_markup: dict = None):
    params = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
    response = send('sendMessage', params)

    if response.status_code == requests.codes.ok:
        user = show_user_database(chat_id)
        print(f"Mensaje enviado a {user['user']['first_name']}, ID: {chat_id}.")