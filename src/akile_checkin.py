import time

from src.solver.cf_solver import LocalSolverCF
from src.config.config import config
from src.request import tg


def main():
    local_solver_cf = LocalSolverCF('https://akile.io/login', incognito_mode=True)
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

    if local_solver_cf.page.url.__contains__("login"):
        try:
            local_solver_cf.page.actions.click("@name=email").input(email)
            local_solver_cf.page.actions.click("@name=password").input(password)
            login_button = local_solver_cf.page.ele("tag=button@@text()=登录")
            login_button.click()
            print("登录成功")
        except:
            print(local_solver_cf.page.html)
            print("登录失败，登录页面查找元素失败")
            tg.send_message("Akile: 签到失败", message_thread_id=topic_id)
            return
        time.sleep(5)
    else:
        print("已是登录状态")
    local_solver_cf.page.get("https://console.akile.io/")
    time.sleep(5)
    button = local_solver_cf.page.ele("tag=button@@text()=今日已签到")
    if not button:
        try:
            button = local_solver_cf.page.ele("每日签到")
            button.click()
            print("签到成功")
            time.sleep(5)
        except:
            print("Akile: 签到失败")
            tg.send_message("Akile: 签到失败", message_thread_id=topic_id)
            print(local_solver_cf.page.html)
            return
    else:
        print("今日已签到，查询签到结果")
    try:
        total = local_solver_cf.page.eles(".text-3xl font-bold mb-1")[0].text
        print("签到结果：" + total)
        tg.send_message("Akile: " + total, message_thread_id=topic_id)
        print("发送tg消息成功")
    except:
        print(local_solver_cf.page.html)
        print("Akile: 签到成功，查询签到结果失败")
        tg.send_message("Akile: 签到成功，查询签到结果失败", message_thread_id=topic_id)
        return


if __name__ == '__main__':
    main()
