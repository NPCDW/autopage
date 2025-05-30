
from DrissionPage import ChromiumOptions
from src.config.config import config


class GetChromiumOptions:
    def __init__(self, incognito_mode=None):
        if incognito_mode is None:
            incognito_mode = config["application"]["incognito_mode"]
        co = ChromiumOptions().set_local_port(config["application"]["remote_port"]).set_timeouts(3)
        if "browser_path" in config["application"] and config["application"]["browser_path"].strip():
            co.set_browser_path(config["application"]["browser_path"])
        if config["application"]["headless"]:
            co.headless().set_argument('--no-sandbox')
        if incognito_mode:
            co.set_argument("--incognito")
        if "user_agent" in config["application"] and config["application"]["user_agent"].strip():
            co.set_user_agent(config["application"]["user_agent"])
        self.co = co

    def get_co(self):
        return self.co
