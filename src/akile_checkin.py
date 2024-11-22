import time

from src.solver.cf_solver import LocalSolverCF
from src.config.config import config
from src.request import tg


def main():
    local_solver_cf = LocalSolverCF('https://akile.io/login')
    local_solver_cf.solver()
    checkin(local_solver_cf)
    if config["application"]["close_after_exec"]:
        local_solver_cf.close()


def checkin(local_solver_cf):
    email = config['akile']['email']
    password = config['akile']['password']
    topic_id = 0
    if 'topic_id' in config['akile']:
        topic_id = config['akile']['topic_id']

    time.sleep(2)
    try:
        local_solver_cf.page.actions.click("#email").input(email)
        local_solver_cf.page.actions.click("#password").input(password)
        login_button = local_solver_cf.page.ele("tag=button@@text()=登录")
        login_button.click()
        print("登录成功")
    except:
        print(local_solver_cf.page.html)
        print("登录失败，登录页面查找元素失败")
        tg.send_message("Akile: 签到失败", message_thread_id=topic_id)
        return
    time.sleep(5)
    try:
        button = local_solver_cf.page.ele("tag=button@@text()=下次一定")
        button.click()
        print("下次一定2FA")
    except:
        print("")
    time.sleep(2)
    try:
        button = local_solver_cf.page.ele("tag=button@@text()=控制台")
        button.click()
        print("进入控制台")
    except:
        print(local_solver_cf.page.html)
        print("Akile: 查找控制台按钮失败")
        tg.send_message("Akile: 签到失败", message_thread_id=topic_id)
        return
    time.sleep(5)
    try:
        button = local_solver_cf.page.ele("每日签到")
        button.click()
        time.sleep(1)
        total = local_solver_cf.page.eles(".arco-statistic-value")[1].text
        tg.send_message("Akile: " + total, message_thread_id=topic_id)
        print("签到成功，发送tg消息成功")
    except:
        tg.send_message("Akile: 签到失败", message_thread_id=topic_id)
        print(local_solver_cf.page.html)
        print("Akile: 签到失败")


if __name__ == '__main__':
    main()
