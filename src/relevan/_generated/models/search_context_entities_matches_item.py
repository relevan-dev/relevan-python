from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_context_entities_matches_item_mode import SearchContextEntitiesMatchesItemMode

T = TypeVar("T", bound="SearchContextEntitiesMatchesItem")


@_attrs_define
class SearchContextEntitiesMatchesItem:
    """
    Attributes:
        span (str): The words of the query that name the place Example: Virginia.
        field (str):  Example: state.
        value (str): The value of the field, in lowercase and without accents Example: va.
        mode (SearchContextEntitiesMatchesItemMode): boost: a document with the value ranks higher. filter: only
            documents with the value match, and the place words left the text query.
    """

    span: str
    field: str
    value: str
    mode: SearchContextEntitiesMatchesItemMode
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        span = self.span

        field = self.field

        value = self.value

        mode = self.mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "span": span,
                "field": field,
                "value": value,
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        span = d.pop("span")

        field = d.pop("field")

        value = d.pop("value")

        mode = SearchContextEntitiesMatchesItemMode(d.pop("mode"))

        search_context_entities_matches_item = cls(
            span=span,
            field=field,
            value=value,
            mode=mode,
        )

        search_context_entities_matches_item.additional_properties = d
        return search_context_entities_matches_item

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
