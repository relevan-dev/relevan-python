from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any, TypeVar

import httpx

from ._errors import RelevanAPIError, RelevanAuthError, RelevanError, RelevanRateLimitError
from ._generated.types import Response

S = TypeVar("S")


def unwrap(response: Response[Any], *, success_type: type[S], endpoint: str) -> S:
    """Return a generated endpoint's success value, or raise a typed relevan error."""
    parsed = response.parsed
    if isinstance(parsed, success_type):
        return parsed
    raise error_for(response.status_code, response.content, response.headers, endpoint=endpoint)


def unwrap_list(response: Response[Any], *, item_type: type[S], endpoint: str) -> list[S]:
    """Like `unwrap`, for endpoints whose success value is a bare JSON array."""
    parsed = response.parsed
    if isinstance(parsed, list):
        return parsed
    raise error_for(response.status_code, response.content, response.headers, endpoint=endpoint)


def raise_for_error_status(response: httpx.Response) -> None:
    """httpx response hook: raise a typed relevan error for each 4xx or 5xx response.

    The hook runs before the generated client parses the body, so a body
    without the documented fields (for example no `message`) cannot raise a
    `KeyError` there.
    """
    if response.status_code < 400:
        return
    response.read()
    raise _error_for_response(response)


async def raise_for_error_status_async(response: httpx.Response) -> None:
    """Async counterpart to `raise_for_error_status`."""
    if response.status_code < 400:
        return
    await response.aread()
    raise _error_for_response(response)


def _error_for_response(response: httpx.Response) -> RelevanError:
    endpoint = f"{response.request.method} {response.request.url.path}"
    return error_for(response.status_code, response.content, response.headers, endpoint=endpoint)


def error_for(
    status_code: int, content: bytes, headers: Mapping[str, str], *, endpoint: str
) -> RelevanError:
    """Map an error response to a typed relevan error. Any body shape is accepted."""
    body = _json_object(content)
    message = body.get("message")
    if not isinstance(message, str) or not message:
        message = f"{endpoint} failed ({status_code})"
    if status_code == 401:
        return RelevanAuthError(message)
    if status_code == 429:
        return RelevanRateLimitError(message, retry_after_seconds=_retry_after(body, headers))
    detail = body.get("error")
    return RelevanAPIError(
        message, status_code=status_code, detail=detail if isinstance(detail, str) else None
    )


def _json_object(content: bytes) -> dict[str, Any]:
    try:
        body = json.loads(content)
    except ValueError:
        return {}
    return body if isinstance(body, dict) else {}


def _retry_after(body: Mapping[str, Any], headers: Mapping[str, str]) -> float | None:
    value = body.get("retryAfterSeconds")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    try:
        return float(headers["Retry-After"])
    except (KeyError, ValueError):
        return None
