import time

from src.solver.cf_solver_inner import LocalSolverCF
from src.config.config import config


def main():
    base_url = config['rjgemby']['base_url']
    tg_id = config['rjgemby']['tg_id']
    cf_verify_ele = config['rjgemby']['cf_verify_ele']

    local_solver_cf = LocalSolverCF("{}/api/checkin/web?user_id={}".format(base_url, tg_id), cf_verify_ele=cf_verify_ele)
    local_solver_cf.solver()
    checkin(local_solver_cf)
    if config["application"]["close_after_exec"]:
        local_solver_cf.close()


def checkin(local_solver_cf):
    time.sleep(3)
    try:
        button = local_solver_cf.page.ele("#checkinBtn")
        button.click()
        time.sleep(10)
        checkin_result = local_solver_cf.page.ele("#result").text
        # print(local_solver_cf.page.html)
        print("rjgemby: 签到结果: " + checkin_result)
    except:
        print(local_solver_cf.page.html)
        print("rjgemby: 签到失败")


if __name__ == '__main__':
    main()
