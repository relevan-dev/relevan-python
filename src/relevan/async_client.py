from __future__ import annotations

import httpx

from ._auth import mask_api_key, resolve_api_key
from ._generated.client import AuthenticatedClient
from ._rate_limit import DEFAULT_MAX_RETRIES, RetryingAsyncTransport
from ._unwrap import raise_for_error_status_async
from .resources.beta import AsyncBeta
from .resources.documents import AsyncDocuments
from .resources.indexes import AsyncIndexes
from .resources.mappings import AsyncMappings
from .resources.organizations import AsyncOrganizations
from .resources.search import AsyncSearch
from .resources.skill import AsyncSkill
from .resources.usage import AsyncUsage

DEFAULT_BASE_URL = "https://api.relevan.dev"
DEFAULT_TIMEOUT = 30.0


class AsyncClient:
    """Async client for the Relevan API — same method surface as `Client`.

    Args:
        api_key: An org-scoped API key. Defaults to the `RELEVAN_API_KEY`
            environment variable when not given.
        base_url: The API's base URL. Defaults to production; pass
            `"https://api.dev.relevan.dev"` to use the dev environment.
        timeout: Per-request timeout, in seconds.
        max_retries: How many times to retry a `429` response, honoring the
            server's `Retry-After` header, before raising `RelevanRateLimitError`.

    Example:
        >>> async with AsyncClient() as client:
        ...     org = (await client.organizations.list())[0]
        ...     await client.search.search(org.id, "products", query="wireless headphones")
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._api_key = resolve_api_key(api_key)
        self._base_url = base_url

        generated = AuthenticatedClient(
            base_url=base_url,
            token=self._api_key,
            prefix="",
            auth_header_name="x-api-key",
            raise_on_unexpected_status=True,
        )
        generated.set_async_httpx_client(
            httpx.AsyncClient(
                base_url=base_url,
                headers={"x-api-key": self._api_key},
                timeout=timeout,
                transport=RetryingAsyncTransport(
                    httpx.AsyncHTTPTransport(), max_retries=max_retries
                ),
                event_hooks={"response": [raise_for_error_status_async]},
            )
        )
        self._generated = generated

        self.organizations = AsyncOrganizations(generated)
        self.indexes = AsyncIndexes(generated)
        self.documents = AsyncDocuments(generated)
        self.mappings = AsyncMappings(generated)
        self.search = AsyncSearch(generated)
        self.skill = AsyncSkill(generated)
        self.usage = AsyncUsage(generated)
        self.beta = AsyncBeta(generated)

    async def aclose(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._generated.get_async_httpx_client().aclose()

    async def __aenter__(self) -> AsyncClient:
        await self._generated.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    def __repr__(self) -> str:
        return f"AsyncClient(base_url={self._base_url!r}, api_key={mask_api_key(self._api_key)!r})"
