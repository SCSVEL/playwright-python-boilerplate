import json
from pathlib import Path
import pytest

from utils.api_utils import get_request, compare_json


@pytest.mark.api
def test_get_objects():
    """Call the public API and compare the JSON response to our fixture."""
    url = "https://api.restful-api.dev/objects"
    status, payload = get_request(url)
    assert status == 200, f"Unexpected status code: {status}"

    # resources moved to repository root
    expected_file = Path(__file__).resolve().parent.parent.parent / "resources" / "objects_full.json"
    assert expected_file.exists(), f"Expected mock JSON not found: {expected_file}"

    with expected_file.open("r", encoding="utf-8") as fh:
        expected = json.load(fh)

    equal, diffs = compare_json(expected, payload)
    if not equal:
        # Provide helpful failure message so diffs show in pytest output
        msg = "JSON response does not match mock JSON:\n" + "\n".join(diffs)
        raise AssertionError(msg)
