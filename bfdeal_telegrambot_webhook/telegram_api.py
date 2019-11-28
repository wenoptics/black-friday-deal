import os
import requests

TELE_TOKEN = os.environ['TELEBOT_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)


def send_message(text, chat_id, **kwargs):
    data = {
        'text': text,
        'chat_id': chat_id
    }
    data.update(kwargs)
    requests.post(URL + "sendMessage", data)

