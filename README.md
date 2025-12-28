# Playwright-python / Python API Boilerplate

Just some boiler plate code to jump start with playwright python testing, extended
with API testing helpers and example pytest suites.

This repository contains a minimal Python project skeleton for API testing with Playwright and pytest.

Quick start (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# if you rely on Playwright browser tests:
python -m playwright install
pytest -q
```

Files of interest
- `requirements.txt` - pinned dev/test tooling and runtime deps.
- `tests/` - pytest suites and fixtures.
- `resources/` - JSON fixtures used by tests.
- `utils/api_utils.py` - helper functions used to call APIs and compare JSON.

CI
A GitHub Actions workflow is included at `.github/workflows/ci.yml`. It runs on push and pull requests
for Python 3.11 and 3.12, installs pinned requirements, installs Playwright browsers, and runs `pytest`.

Pinned requirements
`requirements.txt` contains exact pinned versions that were used when preparing this project.

Notes
- The repository includes both network tests that call `https://api.restful-api.dev/objects` and
  fixtures under `resources/` for deterministic comparisons. Consider mocking network calls
  in CI if you prefer not to depend on live external services.

Next steps
- Add CI secrets or service accounts if tests require private endpoints.
- Add more fixtures and mocked tests for offline CI execution.

