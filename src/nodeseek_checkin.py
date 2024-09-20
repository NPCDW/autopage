import time

from src.solver.cf_solver import LocalSolverCF
from src.config.config import config
from src.request import tg


def main():
    session = config['nodeseek']['session']
    topic_id = 0
    if 'topic_id' in config['nodeseek']:
        topic_id = config['nodeseek']['topic_id']

    cookies = ['session=' + session + '; domain=www.nodeseek.com']
    local_solver_cf = LocalSolverCF('https://www.nodeseek.com/board', cookies)
    local_solver_cf.solver()
    time.sleep(2)
    try:
        button = local_solver_cf.page.ele("试试手气")
        button.click()
    except:
        print("没有找到签到按钮，可能已经签过到了")
    time.sleep(2)
    try:
        checkin_result = local_solver_cf.page.ele(".head-info").text
        tg.send_message("NodeSeek: " + checkin_result, message_thread_id=topic_id)
        print("NodeSeek: " + checkin_result)
    except:
        tg.send_message("NodeSeek: 签到失败", message_thread_id=topic_id)
        print(local_solver_cf.page.html)
        print("NodeSeek: 签到失败")
    if config["application"]["close_after_exec"]:
        local_solver_cf.close()


if __name__ == '__main__':
    main()
