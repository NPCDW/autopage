import time
import requests

from cf_solver import LocalSolverCF
from config import get_config


def main():
    config = get_config()
    session = config['nodeseek']['session']
    bot_token = config['telegram']['bot_token']
    chat_id = config['telegram']['chat_id']

    cookies = ['session=' + session + '; domain=www.nodeseek.com']
    local_solver_cf = LocalSolverCF('https://www.nodeseek.com/board', cookies)
    local_solver_cf.capsolver()
    try:
        button = local_solver_cf.page.ele("试试手气")
        button.click()
    except:
        print("没有找到签到按钮，可能已经签过到了")
    time.sleep(2)
    checkin_result = local_solver_cf.page.ele(".head-info").text
    requests.post("https://api.telegram.org/bot" + bot_token + "/sendMessage", json={
        "chat_id": chat_id,
        "text": "NodeSeek: " + checkin_result
    })
    # print(local_solver_cf.page.html)


if __name__ == '__main__':
    main()
