from playwright.sync_api import Page, expect
from pages.basePg import BasePg

class HomePg(BasePg):
    def __init__(self, page: Page):
        self.page = page
        self.icon_profile = "div.search-block button.dropbtn"

    def is_it_home(self):
        try:
            expect(self.page.locator(self.icon_profile)).to_be_visible(timeout=60_000) 
        except Exception as e:
            raise Exception("Home page didn't load as expected.")
        
        

