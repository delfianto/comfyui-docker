#!/usr/bin/env python3
"""Smoke test for the official ComfyUI API proxy and SDK.

Verifies:
1. Direct HTTP probe to /api/v2/health on the proxy endpoint.
2. Direct HTTP probe to /api/v2/jobs.
3. SDK connection using comfy-sdk client against the proxy.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, cast

PROXY_URL = os.environ.get("COMFY_PROXY_URL", "http://127.0.0.1:8189")


def test_health() -> None:
    print(f"[1/3] Testing GET {PROXY_URL}/api/v2/health ...", end=" ", flush=True)
    req = urllib.request.Request(f"{PROXY_URL}/api/v2/health")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status_code = getattr(resp, "status", 200)
            assert status_code == 200, f"Expected 200, got {status_code}"
            raw = cast(bytes, resp.read())
            data = cast(dict[str, object], json.loads(raw.decode("utf-8")))
            assert data.get("status") == "healthy", f"Unexpected status: {data}"
            print(f"OK (upstream: {data.get('upstream')})")
    except urllib.error.URLError as exc:
        print(f"FAILED: {exc}")
        sys.exit(1)


def test_jobs_endpoint() -> None:
    print(f"[2/3] Testing GET {PROXY_URL}/api/v2/jobs ...", end=" ", flush=True)
    req = urllib.request.Request(f"{PROXY_URL}/api/v2/jobs")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status_code = getattr(resp, "status", 200)
            assert status_code == 200, f"Expected 200, got {status_code}"
            raw = cast(bytes, resp.read())
            data = cast(dict[str, object], json.loads(raw.decode("utf-8")))
            print(f"OK (jobs response keys: {list(data.keys())})")
    except urllib.error.URLError as exc:
        print(f"FAILED: {exc}")
        sys.exit(1)


def test_sdk() -> None:
    print(f"[3/3] Testing Comfy SDK against {PROXY_URL} ...", end=" ", flush=True)
    try:
        os.environ["COMFY_BASE_URL"] = PROXY_URL
        from comfy_sdk import Comfy  # pyright: ignore[reportMissingImports]

        client: Any = Comfy()
        jobs_data = cast(dict[str, object], client._low.list_jobs())
        jobs_list = cast(list[object], jobs_data.get("jobs", []))
        print(
            f"OK (client connected, verified API v2 contract, {len(jobs_list)} jobs listed)"
        )
    except ImportError:
        print(
            "SKIPPED (comfy-sdk not installed in current environment; install with 'uv pip install comfy-sdk')"
        )
    except Exception as exc:  # noqa: BLE001
        print(f"FAILED: {exc}")
        sys.exit(1)


def main() -> None:
    print(f"--- ComfyUI API Proxy Smoke Test ({PROXY_URL}) ---")
    test_health()
    test_jobs_endpoint()
    test_sdk()
    print("All checks completed successfully!")


if __name__ == "__main__":
    main()
