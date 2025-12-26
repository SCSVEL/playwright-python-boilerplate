from playwright.sync_api import Page


class BasePg:
    def __init__(self, page: Page):
        self.page = page