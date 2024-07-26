import time

from src.solver.cf_solver import LocalSolverCF
from src.config.config import config
from src.request import tg


def main():
    bot_token = config['vps_monitor']['bot_token']
    chat_id = config['vps_monitor']['chat_id']
    check_intervals = config['vps_monitor']['check_intervals']
    loop_number = 0
    yxvm_tokyo_vol_basic_stocks_remaining = ""
    yxvm_tokyo_vol_standard_stocks_remaining = ""
    yxvm_tokyo_vol_advanced_stocks_remaining = ""
    yxvm_tokyo_vol_luxury_stocks_remaining = ""

    while True:
        local_solver_cf = LocalSolverCF('https://yxvm.com/index.php?rp=/store/tokyo-volume-beta')
        local_solver_cf.solver()
        # print(local_solver_cf.page.html)
        try:
            product1_stocks_remaining = local_solver_cf.page.ele("#product1-name").parent(2).ele(".qty").text
            # print(product1_stocks_remaining, yxvm_tokyo_vol_basic_stocks_remaining)
            if loop_number == 0:
                yxvm_tokyo_vol_basic_stocks_remaining = product1_stocks_remaining
            if product1_stocks_remaining != yxvm_tokyo_vol_basic_stocks_remaining:
                tg.send_message("库存变动通知\n"
                                "商品: YxVM Tokyo Volume Basic\n"
                                "库存: " + product1_stocks_remaining + "\n"
                                "价格: $3.00 USD Monthly\n"
                                "aff: [go](https://yxvm.com/index.php?aff=373&rp=/store/tokyo-volume-beta/basic)",
                                bot_token, chat_id, parse_mode="Markdown")
                yxvm_tokyo_vol_basic_stocks_remaining = product1_stocks_remaining

            product2_stocks_remaining = local_solver_cf.page.ele("#product2-name").parent(2).ele(".qty").text
            # print(product2_stocks_remaining, yxvm_tokyo_vol_standard_stocks_remaining)
            if loop_number == 0:
                yxvm_tokyo_vol_standard_stocks_remaining = product2_stocks_remaining
            if product2_stocks_remaining != yxvm_tokyo_vol_standard_stocks_remaining:
                tg.send_message("库存变动通知\n"
                                "商品: YxVM Tokyo Volume Standard\n"
                                "库存: " + product2_stocks_remaining + "\n"
                                "价格: $5.00 USD Monthly\n"
                                "aff: [go](https://yxvm.com/index.php?aff=373&rp=/store/tokyo-volume-beta/standard)",
                                bot_token, chat_id, parse_mode="Markdown")
                yxvm_tokyo_vol_standard_stocks_remaining = product2_stocks_remaining

            loop_number += 1
        except:
            print("库存变动监控失败")
        time.sleep(check_intervals)
        # if config["application"]["close_after_exec"]:
        #     local_solver_cf.close()


if __name__ == '__main__':
    main()
