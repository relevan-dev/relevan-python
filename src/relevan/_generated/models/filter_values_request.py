from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_filter_type_0 import SearchFilterType0
    from ..models.search_filter_type_1 import SearchFilterType1
    from ..models.search_range_filter import SearchRangeFilter


T = TypeVar("T", bound="FilterValuesRequest")


@_attrs_define
class FilterValuesRequest:
    """
    Attributes:
        fields (list[str] | Unset): The fields to list. The default is each field that is filterable and aggregatable,
            of kind text, id, boolean, array, number, or date. A number or date field returns its min and max in `ranges`,
            not a value list. Example: ['category', 'brand'].
        size (int | Unset): The most values to return for each field (default 20, max 100) Example: 20.
        filters (list[SearchFilterType0 | SearchFilterType1 | SearchRangeFilter] | Unset): Filters, with the same schema
            as the search `filters`. `count` matches every filter. The value list of a field obeys the filters on the other
            fields and ignores the filters on that field, so the list still shows the other values. Example: [{'field':
            'witness', 'value': 'Alan Pierce'}, {'field': 'fact_type', 'value': 'ruling'}].
        partition (str | Unset): The one partition to search, for an index that declares a partition field (for example
            `tenant_id`). Such an index refuses a request with no partition (400). The server applies it as an exact-match
            filter on the partition field, and a filter on that field is a 400. An index with no partition field refuses
            this value (400). Example: tenant-1187.
        routing (str | Unset): A value of the routing field, for an index that routes its documents by a field (for
            example `tenant_id`). The request then reads only the shard of that value, which is faster on an index with more
            than one shard. It adds no filter: the shard can hold documents with other values, so filter on the field, or
            use `partition`, to get only that value. With no value, the request reads each shard. When the partition and the
            routing use the same field, the `partition` value is also the routing value, so do not send `routing`. An index
            with no routing field refuses this value (400). Example: tenant-1187.
    """

    fields: list[str] | Unset = UNSET
    size: int | Unset = UNSET
    filters: list[SearchFilterType0 | SearchFilterType1 | SearchRangeFilter] | Unset = UNSET
    partition: str | Unset = UNSET
    routing: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.search_filter_type_0 import SearchFilterType0
        from ..models.search_filter_type_1 import SearchFilterType1

        fields: list[str] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields

        size = self.size

        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, SearchFilterType0) or isinstance(
                    filters_item_data, SearchFilterType1
                ):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        partition = self.partition

        routing = self.routing

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if fields is not UNSET:
            field_dict["fields"] = fields
        if size is not UNSET:
            field_dict["size"] = size
        if filters is not UNSET:
            field_dict["filters"] = filters
        if partition is not UNSET:
            field_dict["partition"] = partition
        if routing is not UNSET:
            field_dict["routing"] = routing

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_filter_type_0 import SearchFilterType0
        from ..models.search_filter_type_1 import SearchFilterType1
        from ..models.search_range_filter import SearchRangeFilter

        d = dict(src_dict)
        fields = cast(list[str], d.pop("fields", UNSET))

        size = d.pop("size", UNSET)

        _filters = d.pop("filters", UNSET)
        filters: list[SearchFilterType0 | SearchFilterType1 | SearchRangeFilter] | Unset = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:

                def _parse_filters_item(
                    data: object,
                ) -> SearchFilterType0 | SearchFilterType1 | SearchRangeFilter:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_search_filter_type_0 = SearchFilterType0.from_dict(data)

                        return componentsschemas_search_filter_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemas_search_filter_type_1 = SearchFilterType1.from_dict(data)

                        return componentsschemas_search_filter_type_1
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_search_filter_type_2 = SearchRangeFilter.from_dict(data)

                    return componentsschemas_search_filter_type_2

                filters_item = _parse_filters_item(filters_item_data)

                filters.append(filters_item)

        partition = d.pop("partition", UNSET)

        routing = d.pop("routing", UNSET)

        filter_values_request = cls(
            fields=fields,
            size=size,
            filters=filters,
            partition=partition,
            routing=routing,
        )

        return filter_values_request
