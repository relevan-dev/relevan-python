#!/usr/bin/env python3
"""Regenerate src/relevan/_generated from the live Relevan OpenAPI spec.

Usage:
    uv run scripts/generate_client.py [--url URL] [--file PATH]

Two gaps in the API's own OpenAPI 3.1 document (not choices this script
should paper over silently) are fixed up here before handing the spec to
openapi-python-client:

1. `orgId` is a path parameter on every `/v1/{orgId}/...` and
   `/v1-beta/{orgId}/...` route, but the API declares it only on the Hono
   route *mount*, not on each individual `createRoute()` call, so it is
   missing from every operation's `parameters` list in the spec. Left
   as-is, the generator drops every route in the API.
2. A few routes (`documents/:documentId`, `mappings/:mappingId`) still
   use Express-style `:paramName` path segments instead of OpenAPI's
   `{paramName}`, which the generator treats as a literal, unmatched
   path segment.

Both are reported to stdout when found. If a future spec fix removes one,
this script's fix-up for it becomes a no-op and the printed count drops
to zero — that is the signal the corresponding workaround can be deleted.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import httpx

DEFAULT_SPEC_URL = "https://api.dev.relevan.dev/openapi"
GENERATED_PACKAGE = Path(__file__).resolve().parent.parent / "src" / "relevan" / "_generated"

COLON_PARAM = re.compile(r":([a-zA-Z_][a-zA-Z0-9_]*)")


def fetch_spec(url: str | None, file: Path | None) -> dict:
    if file is not None:
        return json.loads(file.read_text())
    response = httpx.get(url or DEFAULT_SPEC_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def normalize_colon_params(spec: dict) -> int:
    """Rewrite `:paramName` path segments to OpenAPI's `{paramName}`."""
    paths = spec["paths"]
    fixed = 0
    for old_path in list(paths):
        new_path, count = COLON_PARAM.subn(r"{\1}", old_path)
        if count:
            paths[new_path] = paths.pop(old_path)
            fixed += count
    return fixed


def inject_missing_org_id(spec: dict) -> int:
    """Add the `orgId` path parameter to operations under `{orgId}` paths
    that don't already declare it (see module docstring, gap 1)."""
    org_id_param = {
        "name": "orgId",
        "in": "path",
        "required": True,
        "description": "Organization id or slug.",
        "schema": {"type": "string"},
    }
    fixed = 0
    for path, operations in spec["paths"].items():
        if "{orgId}" not in path:
            continue
        for method, operation in operations.items():
            if method not in {"get", "put", "post", "delete", "patch", "options", "head"}:
                continue
            params = operation.setdefault("parameters", [])
            if any(p.get("name") == "orgId" and p.get("in") == "path" for p in params):
                continue
            params.insert(0, dict(org_id_param))
            fixed += 1
    return fixed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help=f"OpenAPI spec URL (default: {DEFAULT_SPEC_URL})")
    parser.add_argument("--file", type=Path, help="Local OpenAPI spec file, instead of --url")
    args = parser.parse_args()

    spec = fetch_spec(args.url, args.file)

    colon_fixes = normalize_colon_params(spec)
    org_id_fixes = inject_missing_org_id(spec)
    print(f"normalized {colon_fixes} colon-style path parameter(s)")
    print(f"injected the missing orgId path parameter into {org_id_fixes} operation(s)")

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
        json.dump(spec, tmp)
        tmp_path = Path(tmp.name)

    try:
        result = subprocess.run(
            [
                "uvx",
                "--from",
                "openapi-python-client",
                "openapi-python-client",
                "generate",
                "--path",
                str(tmp_path),
                "--output-path",
                str(GENERATED_PACKAGE),
                "--meta",
                "none",
                "--overwrite",
                "--fail-on-warning",
            ],
            check=False,
        )
    finally:
        tmp_path.unlink(missing_ok=True)

    if result.returncode != 0:
        print(
            "generation failed — see warnings above; each one means an endpoint "
            "silently did not get generated",
            file=sys.stderr,
        )
        return result.returncode

    print(f"wrote generated client to {GENERATED_PACKAGE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
