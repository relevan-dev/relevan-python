from __future__ import annotations

from typing import Any

from .._generated.api.mappings import (
    get_v_1_org_id_indexes_index_name_mappings,
    get_v_1_org_id_indexes_index_name_mappings_mapping_id,
    post_v_1_org_id_indexes_index_name_mappings,
)
from .._generated.client import AuthenticatedClient
from .._generated.models.mapping_revision import MappingRevision
from .._generated.models.update_mapping import UpdateMapping
from .._generated.models.update_mapping_fields import UpdateMappingFields
from .._generated.models.update_mapping_language import UpdateMappingLanguage
from .._generated.types import UNSET, Unset
from .._unwrap import unwrap, unwrap_list

__all__ = ["AsyncMappings", "MappingRevision", "Mappings"]


class Mappings:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def list(self, org_id: str, index_name: str) -> list[MappingRevision]:
        """List every mapping revision ever created for an index, newest first."""
        response = get_v_1_org_id_indexes_index_name_mappings.sync_detailed(
            org_id, index_name, client=self._client
        )
        return unwrap_list(response, item_type=MappingRevision, endpoint="mappings.list")

    def get(self, org_id: str, index_name: str, mapping_id: str) -> MappingRevision:
        """Get one mapping revision by id."""
        response = get_v_1_org_id_indexes_index_name_mappings_mapping_id.sync_detailed(
            org_id, index_name, mapping_id, client=self._client
        )
        return unwrap(response, success_type=MappingRevision, endpoint="mappings.get")

    def create(
        self,
        org_id: str,
        index_name: str,
        *,
        fields: dict[str, Any],
        language: UpdateMappingLanguage | Unset = UNSET,
    ) -> MappingRevision:
        """Deploy a new mapping revision, defining the index's fields and how each is used.

        Args:
            org_id: The organization's id or slug.
            index_name: The index's URL-safe name.
            fields: Field mappings by field name, e.g. `{"name": {"use": ["searchable"]},
                "price": {"use": ["filterable"], "kind": "number"}}`.
            language: The language for text fields that don't name their own. Defaults to english.
        """
        body = UpdateMapping(fields=UpdateMappingFields.from_dict(fields), language=language)
        response = post_v_1_org_id_indexes_index_name_mappings.sync_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=MappingRevision, endpoint="mappings.create")


class AsyncMappings:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    async def list(self, org_id: str, index_name: str) -> list[MappingRevision]:
        """Async version of `Mappings.list`."""
        response = await get_v_1_org_id_indexes_index_name_mappings.asyncio_detailed(
            org_id, index_name, client=self._client
        )
        return unwrap_list(response, item_type=MappingRevision, endpoint="mappings.list")

    async def get(self, org_id: str, index_name: str, mapping_id: str) -> MappingRevision:
        """Async version of `Mappings.get`."""
        response = await get_v_1_org_id_indexes_index_name_mappings_mapping_id.asyncio_detailed(
            org_id, index_name, mapping_id, client=self._client
        )
        return unwrap(response, success_type=MappingRevision, endpoint="mappings.get")

    async def create(
        self,
        org_id: str,
        index_name: str,
        *,
        fields: dict[str, Any],
        language: UpdateMappingLanguage | Unset = UNSET,
    ) -> MappingRevision:
        """Async version of `Mappings.create`."""
        body = UpdateMapping(fields=UpdateMappingFields.from_dict(fields), language=language)
        response = await post_v_1_org_id_indexes_index_name_mappings.asyncio_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=MappingRevision, endpoint="mappings.create")
