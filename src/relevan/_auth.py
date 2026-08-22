from __future__ import annotations

import os

API_KEY_ENV_VAR = "RELEVAN_API_KEY"
API_KEY_PREFIX = "relevan_"


def resolve_api_key(api_key: str | None) -> str:
    """Resolve the API key to use: an explicit argument, else the environment.

    Args:
        api_key: A key passed directly to `Client()` / `AsyncClient()`, or `None`
            to fall back to the `RELEVAN_API_KEY` environment variable.

    Returns:
        The resolved API key.

    Raises:
        RelevanAuthError: No key was passed and `RELEVAN_API_KEY` is not set.
    """
    from ._errors import RelevanAuthError

    key = api_key if api_key is not None else os.environ.get(API_KEY_ENV_VAR)
    if not key:
        raise RelevanAuthError(
            f"No API key found. Pass api_key=... or set the {API_KEY_ENV_VAR} environment variable."
        )
    return key


def mask_api_key(api_key: str) -> str:
    """Mask an API key for use in logs and `repr()` — never print a full key."""
    prefix_len = len(API_KEY_PREFIX)
    if len(api_key) <= prefix_len:
        return "***"
    return f"{api_key[:prefix_len]}{'*' * 8}"
