from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchContextDecay")


@_attrs_define
class SearchContextDecay:
    """Among hits that match equally well, a newer document of a decayed profile ranks higher. Absent when the index has no
    recency decay.

        Attributes:
            field (str): The date field whose age lowers the score. Example: updated_at.
            type_field (None | str): The field that selects the decay profile of each document. Null when one profile
                applies to each document. Example: doc_type.
            profiles (list[str]): The profiles that decay. A document of another type keeps its score at each age. Example:
                ['type:note'].
    """

    field: str
    type_field: str | None
    profiles: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        type_field: str | None
        type_field = self.type_field

        profiles = self.profiles

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
                "typeField": type_field,
                "profiles": profiles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field")

        def _parse_type_field(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        type_field = _parse_type_field(d.pop("typeField"))

        profiles = cast(list[str], d.pop("profiles"))

        search_context_decay = cls(
            field=field,
            type_field=type_field,
            profiles=profiles,
        )

        search_context_decay.additional_properties = d
        return search_context_decay

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
