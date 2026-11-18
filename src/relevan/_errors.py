from __future__ import annotations

from collections.abc import Mapping


class RelevanError(Exception):
    """Base class for every error this package raises.

    Attributes:
        headers: The headers of the error response, when the error came from one.
    """

    headers: Mapping[str, str] | None = None


class RelevanAuthError(RelevanError):
    """The API rejected the request's credentials (HTTP 401)."""


class RelevanRateLimitError(RelevanError):
    """The request was rate limited and all retries were exhausted (HTTP 429).

    Attributes:
        retry_after_seconds: How long the server asked the caller to wait,
            when the response included that detail.
    """

    def __init__(self, message: str, *, retry_after_seconds: float | None = None) -> None:
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


class RelevanAPIError(RelevanError):
    """The API returned an error response other than an auth or rate-limit error.

    Attributes:
        status_code: The HTTP status code of the response.
        detail: Additional detail from the response body, when present.
    """

    def __init__(self, message: str, *, status_code: int, detail: str | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail
