from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.index_status import IndexStatus

T = TypeVar("T", bound="Index")


@_attrs_define
class Index:
    """
    Attributes:
        id (str): Unique index identifier Example: 550e8400-e29b-41d4-a716-446655440000.
        organization_id (str): Organization ID that owns this index Example: org_123456789.
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within org) Example: products.
        display_name (None | str): Display name shown in the UI Example: Product Catalog.
        description (None | str): Index description Example: Product catalog index.
        status (IndexStatus): Current index lifecycle status Example: ready.
        ready_at (None | str): The first time the index status became ready. Null if it was never ready. Example:
            2024-01-15T10:31:12.000Z.
        failed_at (None | str): The first time the index status became failed. Null if it never failed.
        created_at (str): Index creation timestamp Example: 2024-01-15T10:30:00.000Z.
        updated_at (str): Last update timestamp Example: 2024-01-15T10:30:00.000Z.
    """

    id: str
    organization_id: str
    index_name: str
    display_name: str | None
    description: str | None
    status: IndexStatus
    ready_at: str | None
    failed_at: str | None
    created_at: str
    updated_at: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        organization_id = self.organization_id

        index_name = self.index_name

        display_name: str | None
        display_name = self.display_name

        description: str | None
        description = self.description

        status = self.status.value

        ready_at: str | None
        ready_at = self.ready_at

        failed_at: str | None
        failed_at = self.failed_at

        created_at = self.created_at

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "organizationId": organization_id,
                "indexName": index_name,
                "displayName": display_name,
                "description": description,
                "status": status,
                "readyAt": ready_at,
                "failedAt": failed_at,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        organization_id = d.pop("organizationId")

        index_name = d.pop("indexName")

        def _parse_display_name(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        display_name = _parse_display_name(d.pop("displayName"))

        def _parse_description(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        status = IndexStatus(d.pop("status"))

        def _parse_ready_at(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        ready_at = _parse_ready_at(d.pop("readyAt"))

        def _parse_failed_at(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        failed_at = _parse_failed_at(d.pop("failedAt"))

        created_at = d.pop("createdAt")

        updated_at = d.pop("updatedAt")

        index = cls(
            id=id,
            organization_id=organization_id,
            index_name=index_name,
            display_name=display_name,
            description=description,
            status=status,
            ready_at=ready_at,
            failed_at=failed_at,
            created_at=created_at,
            updated_at=updated_at,
        )

        index.additional_properties = d
        return index

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
