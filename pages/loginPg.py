from playwright.sync_api import Page, expect
from .basePg import BasePg
from utils.reporter import Reporter
from utils.utils import Utils


class LoginPg(BasePg):
    def __init__(self, page: Page, reporter: Reporter):
        super().__init__(page)
        self.page = page
        self.reporter = reporter
        self.txt_user_name = "input#username"
        self.txt_user_pw = "input#password"
        self.btn_submit = "a#signOnButton"
        self.btn_cookie_continue = "#accept-btn"

    def login(self, user_name, password):
        self.page.goto(Utils.get_env("APP_URL"))
        self.handle_cookie_popup()
        self.page.locator(self.txt_user_name).type(user_name)
        self.page.locator(self.txt_user_pw).type(password)
        self.page.locator(self.btn_submit).click()
        self.handle_cookie_popup()
        return self

    def handle_cookie_popup(self):
        if self.page.locator(self.btn_cookie_continue).is_visible():
            self.page.locator(self.btn_cookie_continue).click()

        return self
