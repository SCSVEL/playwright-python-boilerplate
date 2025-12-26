import playwright
from playwright.sync_api import Page, Playwright

from utils.reporter import Reporter
from utils.uiUtils import UIUtils
from utils.utils import Utils


def test_check_if_logged_in(my_page: Page, app_pages):
    try:
        print("URL - " + Utils.get_env("APP_URL"))
        my_page.goto(Utils.get_env("APP_URL"))
        app_pages["login_pg"].login(user_name=Utils.get_env("MGR_ID"),
                                    password=Utils.get_env("MGR_PW"))
        app_pages["home_pg"].is_it_home()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def test_acct_pg(my_page: Page, app_pages):
    try:
        # Login
        app_pages["login_pg"].login(user_name=Utils.get_env("MGR_ID"),
                                    password=Utils.get_env("MGR_PW"))
        app_pages["home_pg"].is_it_home()

        # Goto Acct Mgmt page
        app_pages["home_pg"].go_to_account_pg()

        #Goto practitioner profile page
        app_pages["acct_pg"].do_something()
        
    except Exception as e:
        print(f"Error when testing account page: {e}")
        raise e


def test_reporting(my_page: Page, reporter: Reporter, app_pages):
    try:
        reporter.report_info("my first step")
        reporter.report_pass("my second step")
        reporter.report_warn("my third step")
        reporter.report_fail("my fourth step")        
    except Exception as e:
        print(f"Error when testing account page: {e}")
        raise e
        
