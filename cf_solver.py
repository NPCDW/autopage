import random
import time
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions


class LocalSolverCF:
    def __init__(self, url, cookies=None):
        co = ChromiumOptions().set_local_port(9339).set_timeouts(3)
        # co.set_browser_path("/usr/bin/google-chrome")
        co.headless().set_argument('--no-sandbox')
        # co.set_argument("--incognito")
        co.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        page = ChromiumPage(co)
        if cookies is not None:
            page.set.cookies(cookies)
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
        if shadow_root is None:
            return None
        while True:
            try:
                cf_iframe = shadow_root.ele("tag=iframe", timeout=3)
                if cf_iframe is not None:
                    print("加载完成iframe")
                    break
            except:
                print("加载iframe")
                time.sleep(1)
        while True:
            try:
                shadow_root2 = cf_iframe.ele('tag=body', timeout=3).shadow_root
                button = shadow_root2.ele("tag=input", timeout=3)
                if button is not None:
                    print("找到按钮")
                    break
            except:
                print("查找按钮")
                shadow_root = self.have_verify()
                if shadow_root is None:
                    print("未找到按钮，cf-turnstile-wrapper消失，可能已经过了cf验证")
                    return None
                time.sleep(1)
        try:
            time.sleep(random.uniform(0.5, 1.5))
            button.click()
            # actions = Actions(self.page)
            # actions.move_to('.cf-turnstile-wrapper', duration=0.5).left(114).up(5).hold().wait(0.01, 0.15).release()  # 104-129  +-13
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
    local_solver_cf.close()


if __name__ == '__main__':
    main()
