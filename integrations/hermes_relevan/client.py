"""The Relevan client this provider uses, marked with the integration header."""

from __future__ import annotations

from relevan import Client

PLUGIN_VERSION = "0.1.0"
INTEGRATION_HEADER = "X-Relevan-Integration"
INTEGRATION = f"hermes/{PLUGIN_VERSION}"
DEFAULT_BASE_URL = "https://api.relevan.dev"


def make_client(api_key: str, base_url: str = DEFAULT_BASE_URL, timeout: float = 10.0) -> Client:
    """Build a Relevan client that sends `X-Relevan-Integration: hermes/<version>`.

    relevan 0.1.0 takes no extra headers, so the header goes on the client's
    underlying httpx client. Every request the client makes then carries it.
    """
    client = Client(api_key=api_key, base_url=base_url, timeout=timeout, max_retries=1)
    client._generated.get_httpx_client().headers[INTEGRATION_HEADER] = INTEGRATION
    return client
