import json
from pathlib import Path

from utils.api_utils import compare_json


# resources moved to repository root
RES = Path(__file__).resolve().parent.parent / "resources"


def test_compare_missing_field_reports_missing_key():
    expected = json.load((RES / "object_1.json").open("r", encoding="utf-8"))
    actual = json.load((RES / "object_missing_fields.json").open("r", encoding="utf-8"))

    equal, diffs = compare_json(expected, actual)
    assert not equal
    assert any("Missing key" in d or "Missing key in actual" in d or "Missing key" in d for d in diffs)


def test_compare_extra_field_reports_unexpected_key():
    expected = json.load((RES / "object_1.json").open("r", encoding="utf-8"))
    actual = json.load((RES / "object_extra_field.json").open("r", encoding="utf-8"))

    equal, diffs = compare_json(expected, actual)
    assert not equal
    assert any("Unexpected key" in d for d in diffs)


def test_malformed_json_raises_decode_error():
    path = RES / "object_malformed.json"
    try:
        with path.open("r", encoding="utf-8") as fh:
            json.load(fh)
    except json.JSONDecodeError:
        # expected
        return
    raise AssertionError("Expected JSONDecodeError when reading malformed fixture")
