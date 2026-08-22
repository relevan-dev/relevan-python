from __future__ import annotations

from typing import Any, TypeVar

from ._errors import RelevanAPIError, RelevanAuthError, RelevanRateLimitError
from ._generated.models.limit_error_response import LimitErrorResponse
from ._generated.types import Response, Unset

S = TypeVar("S")


def unwrap(response: Response[Any], *, success_type: type[S], endpoint: str) -> S:
    """Return a generated endpoint's success value, or raise a typed relevan error."""
    parsed = response.parsed
    if isinstance(parsed, success_type):
        return parsed
    raise _error_for(response, parsed, endpoint=endpoint)


def unwrap_list(response: Response[Any], *, item_type: type[S], endpoint: str) -> list[S]:
    """Like `unwrap`, for endpoints whose success value is a bare JSON array."""
    parsed = response.parsed
    if isinstance(parsed, list):
        return parsed
    raise _error_for(response, parsed, endpoint=endpoint)


def _error_for(response: Response[Any], parsed: object, *, endpoint: str) -> Exception:
    message = getattr(parsed, "message", None) or f"{endpoint} failed ({response.status_code})"
    if response.status_code == 401:
        return RelevanAuthError(message)
    if isinstance(parsed, LimitErrorResponse):
        return RelevanRateLimitError(message, retry_after_seconds=parsed.retry_after_seconds)
    detail = getattr(parsed, "error", None)
    detail = detail if detail is not None and not isinstance(detail, Unset) else None
    return RelevanAPIError(message, status_code=response.status_code, detail=detail)
