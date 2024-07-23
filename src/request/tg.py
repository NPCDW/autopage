import string

import requests

from src.config.config import config


def send_message(text: string):
    bot_token = config['telegram']['bot_token']
    chat_id = config['telegram']['chat_id']

    requests.post("https://api.telegram.org/bot" + bot_token + "/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })


if __name__ == '__main__':
    send_message("测试消息")
