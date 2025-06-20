import random
import time

from DrissionPage import ChromiumPage
from src.config.config import config
from src.solver.get_chromium_options import GetChromiumOptions


# from pyHM import mouse


class LocalSolverCF:
    def __init__(self, url, cf_verify_ele, cookies=None, incognito_mode=None, init_js=None):
        chromium_options = GetChromiumOptions(incognito_mode)
        page = ChromiumPage(addr_or_opts=chromium_options.co)
        if cookies is not None:
            page.set.cookies(cookies)
        # page.actions.move(474, 362)
        if init_js is not None:
            page.add_init_js(init_js)
        page.get(url)
        self.cf_verify_ele = cf_verify_ele
        self.page = page

    '''
    当前 cf 结构
    ```
    <div class="cf-turnstile-wrapper">
        <div>
            <div>
                #shadow-root (closed)
                <iframe src="url">
                    <html>
                        <body>
                            #shadow-root (closed)
                            <input type="checkbox">
                            <span class="cb-i"></span>
                            <span class="cb-1b-t">确认您是真人</span>
                        </body>
                    </html>
                </iframe>
            </div>
        </div>
    </div>
    ```
    '''
    def solver(self):
        cf_wrapper = self.page.ele(self.cf_verify_ele, timeout=3)
        if not cf_wrapper:
            print("cf-turnstile-wrapper不存在，无需验证")
            return None
        print("发现cf-turnstile-wrapper")
        count = 0
        while True:
            try:
                count += 1
                shadow_root = cf_wrapper.ele("tag=div", timeout=3).shadow_root
                cf_iframe = shadow_root.ele("tag=iframe", timeout=3)
                shadow_root2 = cf_iframe.ele('tag=body', timeout=3).shadow_root
                button = shadow_root2.ele("tag=input", timeout=3)
                if button.wait.displayed(timeout=3):
                    print("找到cf-turnstile-wrapper按钮")
                    break
            except:
                print("查找cf-turnstile-wrapper按钮")
                if not self.page.ele(self.cf_verify_ele, timeout=3):
                    print("cf-turnstile-wrapper消失，无需再次验证")
                    time.sleep(3)
                    return None
                time.sleep(1)
                if count > 5:
                    print("查找cf-turnstile-wrapper按钮大于5次，不再查找")
                    return None
        try:
            time.sleep(random.uniform(0.5, 1.5))
            button.click()

            # actions = Actions(self.page)
            # pre_pos = (actions.curr_x, actions.curr_y)
            # print("起始坐标：", pre_pos)
            # wrapper = self.page.ele('.cf-turnstile-wrapper')
            # print("按钮坐标：", button.rect.screen_location)
            # print("wrapper坐标：", wrapper.rect.screen_location)
            # actions.move_to((wrapper.rect.location[0] + 25, wrapper.rect.location[1] + 33))
            # actions.hold().wait(0.01, 0.15).release()  # 104-129  +-13

            # mouse.move(wrapper.rect.screen_location[0] + 25, wrapper.rect.screen_location[1] + 33)
            # mouse.click()
        except:
            print(f'click Error')
        time.sleep(3)
        print('button.value ', button.check())
        if button.check():
            print("cf-turnstile-wrapper消失，验证成功")
            return None
        print("cf-turnstile-wrapper仍然存在，验证失败")

    def close(self):
        self.page.quit()


def main():
    local_solver_cf = LocalSolverCF('https://whmcs.sharon.io/index.php?rp=/store/hk-lite')
    local_solver_cf.solver()
    local_solver_cf.page.wait.doc_loaded(timeout=5)
    print(local_solver_cf.page.html)
    if config["application"]["close_after_exec"]:
        local_solver_cf.close()


if __name__ == '__main__':
    main()
