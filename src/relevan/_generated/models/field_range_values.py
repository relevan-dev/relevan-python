from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FieldRangeValues")


@_attrs_define
class FieldRangeValues:
    """
    Attributes:
        min_ (float | None | str): The lowest value: a number, or an ISO 8601 time for a date field. Use it as a `gte`
            value in a range filter. Null when no document has a value. Example: 4.99.
        max_ (float | None | str): The highest value, in the same form as `min`. Use it as an `lte` value. Example:
            1299.
        total (int): The number of documents in scope: the partition, and the filters on the other fields
        missing (int): The number of documents in scope with no value in this field
    """

    min_: float | str | None
    max_: float | str | None
    total: int
    missing: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        min_: float | str | None
        min_ = self.min_

        max_: float | str | None
        max_ = self.max_

        total = self.total

        missing = self.missing

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "min": min_,
                "max": max_,
                "total": total,
                "missing": missing,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_min_(data: object) -> float | str | None:
            if data is None:
                return data
            return cast(float | None | str, data)

        min_ = _parse_min_(d.pop("min"))

        def _parse_max_(data: object) -> float | str | None:
            if data is None:
                return data
            return cast(float | None | str, data)

        max_ = _parse_max_(d.pop("max"))

        total = d.pop("total")

        missing = d.pop("missing")

        field_range_values = cls(
            min_=min_,
            max_=max_,
            total=total,
            missing=missing,
        )

        field_range_values.additional_properties = d
        return field_range_values

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
