from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.mapping_language import MappingLanguage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mapping_fields import MappingFields


T = TypeVar("T", bound="Mapping")


@_attrs_define
class Mapping:
    """Parsed Relevan mapping JSON

    Attributes:
        fields (MappingFields): Field mappings by field name Example: {'name': {'use': ['searchable', 'filterable']},
            'price': {'use': ['filterable', 'sortable'], 'kind': 'number'}}.
        language (MappingLanguage | Unset): Language for every text field that does not name its own. Defaults to
            english. Example: english.
    """

    fields: MappingFields
    language: MappingLanguage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fields = self.fields.to_dict()

        language: str | Unset = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fields": fields,
            }
        )
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mapping_fields import MappingFields

        d = dict(src_dict)
        fields = MappingFields.from_dict(d.pop("fields"))

        _language = d.pop("language", UNSET)
        language: MappingLanguage | Unset
        if isinstance(_language, Unset):
            language = UNSET
        else:
            language = MappingLanguage(_language)

        mapping = cls(
            fields=fields,
            language=language,
        )

        mapping.additional_properties = d
        return mapping

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
