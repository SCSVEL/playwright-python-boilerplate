import argparse
import os
from os import environ

import dotenv
import pytest
from playwright.sync_api import Page

from utils.reporter import Reporter


def load_env_data():
    arg_parser = argparse.ArgumentParser(description="just execute the tests")
    arg_parser.add_argument('--whichenv', default="TST", help="which env?")
    args = arg_parser.parse_args([])
    if os.path.exists("../.env"):
        dotenv.load_dotenv("../.env")
    else:
        dotenv.load_dotenv("../envconfig/" + args.whichenv + ".env")


@pytest.fixture(scope="session", autouse=True)
def bfr_run(request):
    # Load the env vars
    load_env_data()



