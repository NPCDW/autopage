import time

from src.config.config import config
from DrissionPage import WebPage
from src.request import tg


def main():
    page = WebPage()
    page.change_mode('d')
    data = "period={}&plan_id={}&coupon_code={}".format(config['v2b_buy']['period'], config['v2b_buy']['plan_id'], config['v2b_buy']['coupon_code'])
    count = 0
    while True:
        response = page.post(config['v2b_buy']['domain'] + '/api/v1/user/order/save', data=data, headers={"Content-Type": "application/x-www-form-urlencoded", "authorization": config['v2b_buy']['authorization']})
        print(count, response.content.decode('unicode_escape'))
        if response.content.decode('unicode_escape').__contains__("当前商品已售罄"):
            time.sleep(1)
            count += 1
            continue
        else:
            tg.send_message("v2b 下单成功", message_thread_id=532)
            break


if __name__ == '__main__':
    main()
