import random
import time

from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
from DrissionPage.common import Actions
from config import config
from pyHM import mouse


class LocalSolverCF:
    def __init__(self, url, cookies=None):
        co = ChromiumOptions().set_local_port(config["application"]["remote_port"]).set_timeouts(3)
        if config["application"]["browser_path"].strip():
            co.set_browser_path("/usr/bin/google-chrome")
        if config["application"]["headless"]:
            co.headless().set_argument('--no-sandbox')
        if config["application"]["incognito_mode"]:
            co.set_argument("--incognito")
        page = ChromiumPage(co)
        if cookies is not None:
            page.set.cookies(cookies)
        # page.actions.move(474, 362)
        page.get(url)
        self.page = page

    def have_verify(self):
        try:
            cf_wrapper = self.page.ele('.cf-turnstile-wrapper', timeout=3)
            shadow_root = cf_wrapper.shadow_root
            return shadow_root
        except:
            print("没有cf_wrapper")
            return None

    '''
    当前 cf 结构
    ```
    <div class="cf-turnstile-wrapper">
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
    ```
    '''
    def capsolver(self):
        shadow_root = self.have_verify()
        if not shadow_root:
            return None
        while True:
            try:
                cf_iframe = shadow_root.ele("tag=iframe", timeout=3)
                if cf_iframe:
                    print("加载完成iframe")
                    break
            except:
                print("加载iframe")
                time.sleep(1)
        while True:
            try:
                shadow_root2 = cf_iframe.ele('tag=body', timeout=3).shadow_root
                button = shadow_root2.ele("tag=input", timeout=3)
                if button:
                    print("找到按钮")
                    break
            except:
                print("查找按钮")
                shadow_root = self.have_verify()
                if not shadow_root:
                    print("未找到按钮，cf-turnstile-wrapper消失，可能已经过了cf验证")
                    return None
                time.sleep(1)
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
            time.sleep(1)
        self.page.wait.load_start()
        time.sleep(3)

    def close(self):
        self.page.quit()


def main():
    local_solver_cf = LocalSolverCF('https://whmcs.sharon.io/index.php?rp=/store/hk-lite')
    local_solver_cf.capsolver()
    print(local_solver_cf.page.html)
    if config["application"]["close_after_exec"]:
        local_solver_cf.close()


if __name__ == '__main__':
    main()
