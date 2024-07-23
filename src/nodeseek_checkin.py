import time

from src.solver.cf_solver import LocalSolverCF
from src.config.config import config
from src.request import tg


def main():
    session = config['nodeseek']['session']

    cookies = ['session=' + session + '; domain=www.nodeseek.com']
    local_solver_cf = LocalSolverCF('https://www.nodeseek.com/board', cookies)
    local_solver_cf.solver()
    try:
        button = local_solver_cf.page.ele("试试手气")
        button.click()
    except:
        print("没有找到签到按钮，可能已经签过到了")
    time.sleep(2)
    try:
        checkin_result = local_solver_cf.page.ele(".head-info").text
        tg.send_message("NodeSeek: " + checkin_result)
    except:
        tg.send_message("NodeSeek: 签到失败")
    # print(local_solver_cf.page.html)
    if config["application"]["close_after_exec"]:
        local_solver_cf.close()


if __name__ == '__main__':
    main()
