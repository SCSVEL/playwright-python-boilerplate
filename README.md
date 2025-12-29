[![CI](https://github.com/SCSVEL/playwright-python-boilerplate/actions/workflows/ci.yml/badge.svg)](https://github.com/SCSVEL/playwright-python-boilerplate/actions/workflows/ci.yml)


# Python UI/API testing Boilerplate

This is a minimal Python project skeleton for UI and API testing with Playwright and pytest.

Files:
- `requirements.txt` - pinned dev/test tooling and runtime deps.
- `tests/` - pytest suites and fixtures.
- `tests/resources/` - JSON fixtures used by tests.
- `tests/utils/api_utils.py` - helper functions used to operate UI, call APIs and compare JSON.


Notes
- The repository includes both network tests that call `https://api.restful-api.dev/objects` and fixtures under `tests/resources/` for deterministic comparisons. 
  
