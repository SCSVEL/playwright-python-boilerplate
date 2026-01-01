from os import environ
import pytest
import requests
from utils.reporter import Reporter


@pytest.fixture(scope="session", autouse=True)
def bfr_api_for_auth():
    # ToDo: Implement auth logic for API tests only            
    yield requests

@pytest.fixture(scope="function", autouse=True)
def reporter():    
    curr_test_name = environ.get("PYTEST_CURRENT_TEST", "TEST REPORT")
    curr_test_name = curr_test_name.split("::")[1].split(" ")[0].strip()
    reporter = Reporter(curr_test_name, None)
    yield reporter
    reporter.save()
