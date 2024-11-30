import time

from src.solver.cf_solver import LocalSolverCF
from src.config.config import config
from src.request import tg


def main():
    c_secure_login = config['ptchina']['c_secure_login']
    c_secure_pass = config['ptchina']['c_secure_pass']
    c_secure_ssl = config['ptchina']['c_secure_ssl']
    c_secure_tracker_ssl = config['ptchina']['c_secure_tracker_ssl']
    c_secure_uid = config['ptchina']['c_secure_uid']

    cookies = [
        'c_secure_login=' + c_secure_login + '; domain=ptchina.org',
        'c_secure_pass=' + c_secure_pass + '; domain=ptchina.org',
        'c_secure_ssl=' + c_secure_ssl + '; domain=ptchina.org',
        'c_secure_tracker_ssl=' + c_secure_tracker_ssl + '; domain=ptchina.org',
        'c_secure_uid=' + c_secure_uid + '; domain=ptchina.org',
    ]
    local_solver_cf = LocalSolverCF('https://ptchina.org/index.php', cookies)
    local_solver_cf.solver()
    checkin(local_solver_cf)
    if config["application"]["close_after_exec"]:
        local_solver_cf.close()


def checkin(local_solver_cf):
    topic_id = 0
    if 'topic_id' in config['ptchina']:
        topic_id = config['ptchina']['topic_id']

    time.sleep(3)
    try:
        button = local_solver_cf.page.ele("tag=a@@text()=[签到得魔力]")
        button.click()
        time.sleep(2)
        print("签到成功")
    except:
        print(local_solver_cf.page.html)
        print("铂金学院: 没有找到签到按钮，可能已经签过到了")
    try:
        total = local_solver_cf.page.ele("tag=a@@text()=[勋章]").prev().text
        tg.send_message("铂金学院: " + total, message_thread_id=topic_id)
        print("发送tg消息成功")
    except:
        print(local_solver_cf.page.html)
        print("铂金学院: 查询签到结果失败")
        tg.send_message("铂金学院: 查询签到结果失败", message_thread_id=topic_id)
        return


if __name__ == '__main__':
    main()
