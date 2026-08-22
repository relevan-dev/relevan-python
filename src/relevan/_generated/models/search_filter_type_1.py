from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchFilterType1")


@_attrs_define
class SearchFilterType1:
    """
    Attributes:
        field (str):  Example: category.
        values (list[bool | float | str]):  Example: ['aquarium', 'terrarium'].
    """

    field: str
    values: list[bool | float | str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        values = []
        for values_item_data in self.values:
            values_item: bool | float | str
            values_item = values_item_data
            values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:

            def _parse_values_item(data: object) -> bool | float | str:
                return cast(bool | float | str, data)

            values_item = _parse_values_item(values_item_data)

            values.append(values_item)

        search_filter_type_1 = cls(
            field=field,
            values=values,
        )

        search_filter_type_1.additional_properties = d
        return search_filter_type_1

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
