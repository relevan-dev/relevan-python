from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.field_mapping_entity_type import FieldMappingEntityType
from ..models.field_mapping_kind import FieldMappingKind
from ..models.field_mapping_language import FieldMappingLanguage
from ..models.field_mapping_use_item import FieldMappingUseItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldMapping")


@_attrs_define
class FieldMapping:
    """
    Attributes:
        use (list[FieldMappingUseItem]): Intended query capabilities for this field
        kind (FieldMappingKind | Unset): Field data type (inferred if omitted) Example: text.
        language (FieldMappingLanguage | Unset): Overrides the mapping language for this field Example: english.
        entity_type (FieldMappingEntityType | Unset): Type of place that the field holds. A query that names a place of
            this type can match the field. The field must also be filterable, with kind text, id, or array. Example: state.
    """

    use: list[FieldMappingUseItem]
    kind: FieldMappingKind | Unset = UNSET
    language: FieldMappingLanguage | Unset = UNSET
    entity_type: FieldMappingEntityType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        use = []
        for use_item_data in self.use:
            use_item = use_item_data.value
            use.append(use_item)

        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        language: str | Unset = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.value

        entity_type: str | Unset = UNSET
        if not isinstance(self.entity_type, Unset):
            entity_type = self.entity_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "use": use,
            }
        )
        if kind is not UNSET:
            field_dict["kind"] = kind
        if language is not UNSET:
            field_dict["language"] = language
        if entity_type is not UNSET:
            field_dict["entityType"] = entity_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        use = []
        _use = d.pop("use")
        for use_item_data in _use:
            use_item = FieldMappingUseItem(use_item_data)

            use.append(use_item)

        _kind = d.pop("kind", UNSET)
        kind: FieldMappingKind | Unset
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = FieldMappingKind(_kind)

        _language = d.pop("language", UNSET)
        language: FieldMappingLanguage | Unset
        if isinstance(_language, Unset):
            language = UNSET
        else:
            language = FieldMappingLanguage(_language)

        _entity_type = d.pop("entityType", UNSET)
        entity_type: FieldMappingEntityType | Unset
        if isinstance(_entity_type, Unset):
            entity_type = UNSET
        else:
            entity_type = FieldMappingEntityType(_entity_type)

        field_mapping = cls(
            use=use,
            kind=kind,
            language=language,
            entity_type=entity_type,
        )

        field_mapping.additional_properties = d
        return field_mapping

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
