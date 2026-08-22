from __future__ import annotations

import httpx

from ._auth import mask_api_key, resolve_api_key
from ._generated.client import AuthenticatedClient
from ._rate_limit import DEFAULT_MAX_RETRIES, RetryingTransport
from .resources.beta import Beta
from .resources.documents import Documents
from .resources.indexes import Indexes
from .resources.mappings import Mappings
from .resources.organizations import Organizations
from .resources.search import Search
from .resources.skill import Skill

DEFAULT_BASE_URL = "https://api.relevan.dev"
DEFAULT_TIMEOUT = 30.0


class Client:
    """Synchronous client for the Relevan API.

    Args:
        api_key: An org-scoped API key. Defaults to the `RELEVAN_API_KEY`
            environment variable when not given.
        base_url: The API's base URL. Defaults to production; pass
            `"https://api.dev.relevan.dev"` to use the dev environment.
        timeout: Per-request timeout, in seconds.
        max_retries: How many times to retry a `429` response, honoring the
            server's `Retry-After` header, before raising `RelevanRateLimitError`.

    Example:
        >>> client = Client()
        >>> org = client.organizations.list()[0]
        >>> client.search.search(org.id, "products", query="wireless headphones")
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
        generated.set_httpx_client(
            httpx.Client(
                base_url=base_url,
                headers={"x-api-key": self._api_key},
                timeout=timeout,
                transport=RetryingTransport(httpx.HTTPTransport(), max_retries=max_retries),
            )
        )
        self._generated = generated

        self.organizations = Organizations(generated)
        self.indexes = Indexes(generated)
        self.documents = Documents(generated)
        self.mappings = Mappings(generated)
        self.search = Search(generated)
        self.skill = Skill(generated)
        self.beta = Beta(generated)

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._generated.get_httpx_client().close()

    def __enter__(self) -> Client:
        self._generated.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"Client(base_url={self._base_url!r}, api_key={mask_api_key(self._api_key)!r})"
