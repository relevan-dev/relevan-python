from __future__ import annotations

from .._generated.api.organizations import get_v1_organizations
from .._generated.client import AuthenticatedClient
from .._generated.models.organization import Organization
from .._unwrap import unwrap_list

__all__ = ["AsyncOrganizations", "Organization", "Organizations"]


class Organizations:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def list(self) -> list[Organization]:
        """List the organizations the caller's API key can access.

        An org-scoped API key always resolves to exactly one organization.
        Call this first to get the `orgId` (either `.id` or `.slug` works)
        used by every other method.

        Returns:
            The accessible organizations.

        Raises:
            RelevanAuthError: The API key is missing or invalid.

        Example:
            >>> org = client.organizations.list()[0]
            >>> org.id
        """
        response = get_v1_organizations.sync_detailed(client=self._client)
        return unwrap_list(response, item_type=Organization, endpoint="organizations.list")


class AsyncOrganizations:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    async def list(self) -> list[Organization]:
        """Async version of `Organizations.list`."""
        response = await get_v1_organizations.asyncio_detailed(client=self._client)
        return unwrap_list(response, item_type=Organization, endpoint="organizations.list")
