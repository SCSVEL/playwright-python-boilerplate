from playwright.sync_api import Page, expect
from pages.basePg import BasePg
from utils.reporter import Reporter


class AcctPg(BasePg):
    def __init__(self, page: Page, reporter: Reporter):
        super().__init__(page)
        self.page = page
        self.reporter = reporter


    def do_somthing(self):        
        return self

    