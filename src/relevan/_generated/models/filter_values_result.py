from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.filter_values_result_fields import FilterValuesResultFields
    from ..models.filter_values_result_ranges import FilterValuesResultRanges


T = TypeVar("T", bound="FilterValuesResult")


@_attrs_define
class FilterValuesResult:
    """
    Attributes:
        count (int): The number of documents in the partition that match every filter. With no filters, the number of
            documents in the partition, or in the index when it has no partition. Example: 2.
        fields (FilterValuesResultFields): The value list of each text, id, boolean, or array field
        ranges (FilterValuesResultRanges): The min and max of each number or date field
    """

    count: int
    fields: FilterValuesResultFields
    ranges: FilterValuesResultRanges
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        fields = self.fields.to_dict()

        ranges = self.ranges.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "fields": fields,
                "ranges": ranges,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_values_result_fields import FilterValuesResultFields
        from ..models.filter_values_result_ranges import FilterValuesResultRanges

        d = dict(src_dict)
        count = d.pop("count")

        fields = FilterValuesResultFields.from_dict(d.pop("fields"))

        ranges = FilterValuesResultRanges.from_dict(d.pop("ranges"))

        filter_values_result = cls(
            count=count,
            fields=fields,
            ranges=ranges,
        )

        filter_values_result.additional_properties = d
        return filter_values_result

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
