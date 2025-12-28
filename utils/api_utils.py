"""Small helper utilities for API testing.

Provides simple get/post wrappers (using requests) and a JSON comparison helper
that returns (equal: bool, diffs: list[str]).
"""
from typing import Any, Dict, List, Optional, Tuple
import json
import requests


def get_request(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 10) -> Tuple[int, Any]:
    """Perform a GET request and return (status_code, parsed_json_or_text).
    """
    if requests is None:
        raise RuntimeError("requests package is required for get_request")

    resp = requests.get(url, params=params, headers=headers, timeout=timeout)
    try:
        return resp.status_code, resp.json()
    except ValueError:
        return resp.status_code, resp.text


def post_request(url: str, data: Optional[Dict[str, Any]] = None, json_body: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 10) -> Tuple[int, Any]:
    """Perform a POST request and return (status_code, parsed_json_or_text).

    `json_body` will be sent as JSON; otherwise `data` will be form-encoded.
    """    
    
    if json_body is not None:
        resp = requests.post(url, json=json_body, headers=headers, timeout=timeout)
    else:
        resp = requests.post(url, data=data, headers=headers, timeout=timeout)

    try:
        return resp.status_code, resp.json()
    except ValueError:
        return resp.status_code, resp.text


def _format_path(path: str, key: Any) -> str:
    if path:
        return f"{path}.{key}"
    return str(key)


def compare_json(a: Any, b: Any, path: str = "") -> Tuple[bool, List[str]]:
    """Recursively compare two JSON-like objects.

    Returns (equal, diffs) where diffs is a list of human-readable differences.
    The comparison treats lists by index and dicts by keys.
    """
    diffs: List[str] = []

    if type(a) != type(b):
        diffs.append(f"Type mismatch at '{path}': {type(a).__name__} != {type(b).__name__}")
        return False, diffs

    if isinstance(a, dict):
        a_keys = set(a.keys())
        b_keys = set(b.keys())
        for key in sorted(a_keys - b_keys):
            diffs.append(f"Missing key in actual at '{_format_path(path, key)}'")
        for key in sorted(b_keys - a_keys):
            diffs.append(f"Unexpected key in actual at '{_format_path(path, key)}'")
        for key in sorted(a_keys & b_keys):
            eq, sub = compare_json(a[key], b[key], _format_path(path, key))
            diffs.extend(sub)
        return (len(diffs) == 0), diffs

    if isinstance(a, list):
        if len(a) != len(b):
            diffs.append(f"List length mismatch at '{path}': {len(a)} != {len(b)}")
        for i, (ai, bi) in enumerate(zip(a, b)):
            eq, sub = compare_json(ai, bi, _format_path(path, i))
            diffs.extend(sub)
        return (len(diffs) == 0), diffs

    # primitive
    if a != b:
        diffs.append(f"Value mismatch at '{path}': {a!r} != {b!r}")
        return False, diffs

    return True, diffs


def compare_json_files(file_a: str, file_b: str) -> Tuple[bool, List[str]]:
    """Load two JSON files and compare them using compare_json.

    Returns (equal, diffs).
    """
    with open(file_a, "r", encoding="utf-8") as fa:
        a = json.load(fa)
    with open(file_b, "r", encoding="utf-8") as fb:
        b = json.load(fb)
    return compare_json(a, b)
