"""The Relevan client this provider uses, marked with the integration header."""

from __future__ import annotations

from relevan import Client

PLUGIN_VERSION = "0.1.0"
INTEGRATION = f"hermes/{PLUGIN_VERSION}"
DEFAULT_BASE_URL = "https://api.relevan.dev"


def make_client(api_key: str, base_url: str = DEFAULT_BASE_URL, timeout: float = 10.0) -> Client:
    """Build a Relevan client whose requests send `X-Relevan-Integration: hermes/<version>`."""
    return Client(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
        max_retries=1,
        integration=INTEGRATION,
    )
