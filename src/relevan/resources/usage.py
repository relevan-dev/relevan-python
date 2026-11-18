from __future__ import annotations

from .._generated.api.usage import get_v_1_org_id_usage
from .._generated.client import AuthenticatedClient
from .._generated.models.usage import Usage
from .._unwrap import unwrap

__all__ = ["AsyncUsage", "Usage", "UsageResource"]


class UsageResource:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def get(self, org_id: str) -> Usage:
        """Get where the organization stands against each cap of its plan.

        Call this before a large upload: a write that adds more than
        `.storage.remaining_bytes` is refused with a 402.

        Args:
            org_id: The organization's id or slug.

        Example:
            >>> client.usage.get(org_id).storage.remaining_bytes
        """
        response = get_v_1_org_id_usage.sync_detailed(org_id, client=self._client)
        return unwrap(response, success_type=Usage, endpoint="usage.get")


class AsyncUsage:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    async def get(self, org_id: str) -> Usage:
        """Async version of `UsageResource.get`."""
        response = await get_v_1_org_id_usage.asyncio_detailed(org_id, client=self._client)
        return unwrap(response, success_type=Usage, endpoint="usage.get")
