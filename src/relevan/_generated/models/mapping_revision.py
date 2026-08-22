from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.mapping import Mapping


T = TypeVar("T", bound="MappingRevision")


@_attrs_define
class MappingRevision:
    """
    Attributes:
        id (str): Unique mapping revision identifier Example: 550e8400-e29b-41d4-a716-446655440000.
        revision (int): Monotonic mapping revision number (starts at 1 within an index) Example: 1.
        relevan_mapping (Mapping): Parsed Relevan mapping JSON
        relevan_mapping_yaml (str): Canonicalized Relevan mapping YAML Example: fields:
              name:
                use: [searchable]
            .
        relevan_mapping_hash (str): sha256 hash of canonical Relevan mapping YAML Example: 3b7c4a1d....
        created_by (None | str): User id that created the revision (nullable) Example:
            550e8400-e29b-41d4-a716-446655440000.
        created_at (str): Mapping revision creation timestamp Example: 2024-01-15T10:30:00.000Z.
    """

    id: str
    revision: int
    relevan_mapping: Mapping
    relevan_mapping_yaml: str
    relevan_mapping_hash: str
    created_by: str | None
    created_at: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        revision = self.revision

        relevan_mapping = self.relevan_mapping.to_dict()

        relevan_mapping_yaml = self.relevan_mapping_yaml

        relevan_mapping_hash = self.relevan_mapping_hash

        created_by: str | None
        created_by = self.created_by

        created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "revision": revision,
                "relevanMapping": relevan_mapping,
                "relevanMappingYaml": relevan_mapping_yaml,
                "relevanMappingHash": relevan_mapping_hash,
                "createdBy": created_by,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mapping import Mapping

        d = dict(src_dict)
        id = d.pop("id")

        revision = d.pop("revision")

        relevan_mapping = Mapping.from_dict(d.pop("relevanMapping"))

        relevan_mapping_yaml = d.pop("relevanMappingYaml")

        relevan_mapping_hash = d.pop("relevanMappingHash")

        def _parse_created_by(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        created_by = _parse_created_by(d.pop("createdBy"))

        created_at = d.pop("createdAt")

        mapping_revision = cls(
            id=id,
            revision=revision,
            relevan_mapping=relevan_mapping,
            relevan_mapping_yaml=relevan_mapping_yaml,
            relevan_mapping_hash=relevan_mapping_hash,
            created_by=created_by,
            created_at=created_at,
        )

        mapping_revision.additional_properties = d
        return mapping_revision

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
