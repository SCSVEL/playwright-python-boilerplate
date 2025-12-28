import argparse
import os
from os import environ

import dotenv
import pytest
from playwright.sync_api import Page
from playwright.sync_api import Playwright

from pages.homePg import HomePg
from pages.loginPg import LoginPg
from pages.acctPg import AcctPg
from utils.reporter import Reporter


def load_env_data():
    arg_parser = argparse.ArgumentParser(description="just execute the tests")
    arg_parser.add_argument('--whichenv', default="TST", help="which env?")
    args = arg_parser.parse_args([])
    if os.path.exists("../.env"):
        dotenv.load_dotenv("../.env")
    else:
        dotenv.load_dotenv("../envconfig/" + args.whichenv + ".env")

@pytest.mark.ui
@pytest.fixture(scope="session", autouse=True)
def bfr_session(playwright: Playwright):
    # Load the env vars
    load_env_data()

    if playwright.node.get_closest_marker("api") is None:
        pytest.skip("skipping bfr_session fixture as not a UI test")

    # Get the browser
    if environ.get("USE_EXISTING_BROWSER") in (None, 'Yes', 'YES', True):
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = browser.contexts[0].pages[0]

        if len(browser.contexts[0].pages) > 1:
            if browser.contexts[0].pages[0].url.startswith("devtools"):
                page = browser.contexts[0].pages[1]
    else:
        browser = playwright.chromium.launch(headless=False, slow_mo=60_000, args=[])  # "--start-maximized"
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

    yield page

    if environ.get("USE_EXISTING_BROWSER") in ('No', 'NO', False):
        page.close()
        context.close()
        browser.close()


@pytest.fixture(scope="function", autouse=True)
def my_page(bfr_session: Page):
    yield bfr_session


@pytest.fixture(scope="function", autouse=True)
def reporter(my_page: Page):
    curr_test_name = environ.get("PYTEST_CURRENT_TEST", "TEST REPORT")
    curr_test_name = curr_test_name.split("::")[1].split(" ")[0].strip()
    reporter = Reporter(curr_test_name, my_page)
    yield reporter
    reporter.save()


@pytest.fixture
def app_pages(my_page: Page, reporter: Reporter):
    my_pages = {
        "home_pg": HomePg(my_page, reporter),
        "login_pg": LoginPg(my_page, reporter),
        "acct_pg": AcctPg(my_page, reporter)
    }
    return my_pages

