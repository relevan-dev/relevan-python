from __future__ import annotations

from .._generated.api.indexes import (
    delete_v_1_org_id_indexes_index_name,
    get_v_1_org_id_indexes,
    get_v_1_org_id_indexes_index_name,
    post_v_1_org_id_indexes,
    put_v_1_org_id_indexes_index_name,
)
from .._generated.client import AuthenticatedClient
from .._generated.models.create_index import CreateIndex
from .._generated.models.created_index import CreatedIndex
from .._generated.models.index import Index
from .._generated.models.index_detail import IndexDetail
from .._generated.models.message_response import MessageResponse
from .._generated.models.update_index import UpdateIndex
from .._generated.types import UNSET, Unset
from .._unwrap import unwrap, unwrap_list

__all__ = ["AsyncIndexes", "CreatedIndex", "Index", "IndexDetail", "Indexes"]


class Indexes:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def list(
        self, org_id: str, *, page: int | Unset = UNSET, limit: int | Unset = UNSET
    ) -> list[Index]:
        """List the indexes in an organization.

        Args:
            org_id: The organization's id or slug.
            page: Page number, when paginating.
            limit: Page size, when paginating.

        Returns:
            The organization's indexes.
        """
        response = get_v_1_org_id_indexes.sync_detailed(
            org_id, client=self._client, page=page, limit=limit
        )
        return unwrap_list(response, item_type=Index, endpoint="indexes.list")

    def get(self, org_id: str, index_name: str) -> IndexDetail:
        """Get one index by name.

        Args:
            org_id: The organization's id or slug.
            index_name: The index's URL-safe name.

        Returns:
            The index, with its document counts and whether it is ready to search.
        """
        response = get_v_1_org_id_indexes_index_name.sync_detailed(
            org_id, index_name, client=self._client
        )
        return unwrap(response, success_type=IndexDetail, endpoint="indexes.get")

    def create(
        self,
        org_id: str,
        *,
        name: str,
        display_name: str | Unset = UNSET,
        description: str | Unset = UNSET,
    ) -> CreatedIndex:
        """Create a new index.

        Args:
            org_id: The organization's id or slug.
            name: URL-safe index name (lowercase alphanumeric + hyphens), unique within the org.
            display_name: Display name shown in the console UI.
            description: A human-readable description of the index.
        """
        body = CreateIndex(name=name, display_name=display_name, description=description)
        response = post_v_1_org_id_indexes.sync_detailed(org_id, client=self._client, body=body)
        return unwrap(response, success_type=CreatedIndex, endpoint="indexes.create")

    def update(
        self,
        org_id: str,
        index_name: str,
        *,
        display_name: str | Unset = UNSET,
        description: str | Unset = UNSET,
    ) -> Index:
        """Update an index's metadata (display name, description)."""
        body = UpdateIndex(display_name=display_name, description=description)
        response = put_v_1_org_id_indexes_index_name.sync_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=Index, endpoint="indexes.update")

    def delete(self, org_id: str, index_name: str) -> MessageResponse:
        """Archive and remove an index. Search cleanup happens asynchronously."""
        response = delete_v_1_org_id_indexes_index_name.sync_detailed(
            org_id, index_name, client=self._client
        )
        return unwrap(response, success_type=MessageResponse, endpoint="indexes.delete")


class AsyncIndexes:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    async def list(
        self, org_id: str, *, page: int | Unset = UNSET, limit: int | Unset = UNSET
    ) -> list[Index]:
        """Async version of `Indexes.list`."""
        response = await get_v_1_org_id_indexes.asyncio_detailed(
            org_id, client=self._client, page=page, limit=limit
        )
        return unwrap_list(response, item_type=Index, endpoint="indexes.list")

    async def get(self, org_id: str, index_name: str) -> IndexDetail:
        """Async version of `Indexes.get`."""
        response = await get_v_1_org_id_indexes_index_name.asyncio_detailed(
            org_id, index_name, client=self._client
        )
        return unwrap(response, success_type=IndexDetail, endpoint="indexes.get")

    async def create(
        self,
        org_id: str,
        *,
        name: str,
        display_name: str | Unset = UNSET,
        description: str | Unset = UNSET,
    ) -> CreatedIndex:
        """Async version of `Indexes.create`."""
        body = CreateIndex(name=name, display_name=display_name, description=description)
        response = await post_v_1_org_id_indexes.asyncio_detailed(
            org_id, client=self._client, body=body
        )
        return unwrap(response, success_type=CreatedIndex, endpoint="indexes.create")

    async def update(
        self,
        org_id: str,
        index_name: str,
        *,
        display_name: str | Unset = UNSET,
        description: str | Unset = UNSET,
    ) -> Index:
        """Async version of `Indexes.update`."""
        body = UpdateIndex(display_name=display_name, description=description)
        response = await put_v_1_org_id_indexes_index_name.asyncio_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=Index, endpoint="indexes.update")

    async def delete(self, org_id: str, index_name: str) -> MessageResponse:
        """Async version of `Indexes.delete`."""
        response = await delete_v_1_org_id_indexes_index_name.asyncio_detailed(
            org_id, index_name, client=self._client
        )
        return unwrap(response, success_type=MessageResponse, endpoint="indexes.delete")
