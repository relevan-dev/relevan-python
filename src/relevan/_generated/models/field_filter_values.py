from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.field_filter_values_values_item import FieldFilterValuesValuesItem


T = TypeVar("T", bound="FieldFilterValues")


@_attrs_define
class FieldFilterValues:
    """
    Attributes:
        values (list[FieldFilterValuesValuesItem]): The values, highest count first. Equal counts sort by value. Each
            value works as a `filters` value in a search.
        other_count (int): The sum of the counts of the values that the size limit left out Example: 14.
        total (int): The number of documents in scope: the partition, and the filters on the other fields
        missing (int): The number of documents in scope with no value in this field
        distinct (int): The number of distinct values of the field in scope. Exact for a small count, an estimate for a
            large one.
        complete (bool): True when `values` holds every value of the field
    """

    values: list[FieldFilterValuesValuesItem]
    other_count: int
    total: int
    missing: int
    distinct: int
    complete: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        values = []
        for values_item_data in self.values:
            values_item = values_item_data.to_dict()
            values.append(values_item)

        other_count = self.other_count

        total = self.total

        missing = self.missing

        distinct = self.distinct

        complete = self.complete

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "values": values,
                "otherCount": other_count,
                "total": total,
                "missing": missing,
                "distinct": distinct,
                "complete": complete,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.field_filter_values_values_item import FieldFilterValuesValuesItem

        d = dict(src_dict)
        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = FieldFilterValuesValuesItem.from_dict(values_item_data)

            values.append(values_item)

        other_count = d.pop("otherCount")

        total = d.pop("total")

        missing = d.pop("missing")

        distinct = d.pop("distinct")

        complete = d.pop("complete")

        field_filter_values = cls(
            values=values,
            other_count=other_count,
            total=total,
            missing=missing,
            distinct=distinct,
            complete=complete,
        )

        field_filter_values.additional_properties = d
        return field_filter_values

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
