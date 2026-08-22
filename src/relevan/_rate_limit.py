from __future__ import annotations

import asyncio
import time
from collections.abc import Mapping
from dataclasses import dataclass

import httpx

DEFAULT_MAX_RETRIES = 2
_DEFAULT_RETRY_AFTER_SECONDS = 1.0


@dataclass(frozen=True, slots=True)
class RateLimit:
    """A snapshot of the `RateLimit-*` response headers on a search response.

    Attributes:
        limit: Requests permitted in the current window at the org's tier.
        remaining: Requests left in the current window.
        reset_seconds: Seconds until the window rolls over.
    """

    limit: int
    remaining: int
    reset_seconds: int


def parse_rate_limit(headers: Mapping[str, str]) -> RateLimit | None:
    """Parse `RateLimit-Limit` / `-Remaining` / `-Reset` off a response, if present."""
    limit = headers.get("RateLimit-Limit")
    remaining = headers.get("RateLimit-Remaining")
    reset = headers.get("RateLimit-Reset")
    if limit is None or remaining is None or reset is None:
        return None
    try:
        return RateLimit(limit=int(limit), remaining=int(remaining), reset_seconds=int(reset))
    except ValueError:
        return None


def _retry_after_seconds(response: httpx.Response) -> float:
    header = response.headers.get("Retry-After")
    if header is None:
        return _DEFAULT_RETRY_AFTER_SECONDS
    try:
        return max(float(header), 0.0)
    except ValueError:
        return _DEFAULT_RETRY_AFTER_SECONDS


class RetryingTransport(httpx.BaseTransport):
    """Retries a 429 response using the server's `Retry-After` header.

    Wraps another transport rather than replacing it, so callers keep whatever
    connection pooling / proxying the wrapped transport already provides.
    """

    def __init__(
        self, wrapped: httpx.BaseTransport, *, max_retries: int = DEFAULT_MAX_RETRIES
    ) -> None:
        self._wrapped = wrapped
        self._max_retries = max_retries

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            response = self._wrapped.handle_request(request)
            if response.status_code != 429 or attempt >= self._max_retries:
                return response
            wait_seconds = _retry_after_seconds(response)
            response.close()
            time.sleep(wait_seconds)
            attempt += 1

    def close(self) -> None:
        self._wrapped.close()


class RetryingAsyncTransport(httpx.AsyncBaseTransport):
    """Async counterpart to `RetryingTransport`."""

    def __init__(
        self, wrapped: httpx.AsyncBaseTransport, *, max_retries: int = DEFAULT_MAX_RETRIES
    ) -> None:
        self._wrapped = wrapped
        self._max_retries = max_retries

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            response = await self._wrapped.handle_async_request(request)
            if response.status_code != 429 or attempt >= self._max_retries:
                return response
            wait_seconds = _retry_after_seconds(response)
            await response.aclose()
            await asyncio.sleep(wait_seconds)
            attempt += 1

    async def aclose(self) -> None:
        await self._wrapped.aclose()
