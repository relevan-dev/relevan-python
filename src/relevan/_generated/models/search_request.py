from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_filter_type_0 import SearchFilterType0
    from ..models.search_filter_type_1 import SearchFilterType1
    from ..models.search_range_filter import SearchRangeFilter
    from ..models.search_request_boost import SearchRequestBoost


T = TypeVar("T", bound="SearchRequest")


@_attrs_define
class SearchRequest:
    """
    Attributes:
        query (str): The search query text Example: neon tetra.
        filters (list[SearchFilterType0 | SearchFilterType1 | SearchRangeFilter] | Unset): Filters, ANDed together.
            Exact-match, in, or range (date/number fields).
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
        boost (SearchRequestBoost | Unset): Per-term weight multipliers. Adds an extra match clause for each term across
            searchable fields; it does not change how the base query matches. Each term must occur in the query. The search
            ignores a term that does not, and names it in searchContext.warnings. Example: {'getting': 2}.
        from_ (int | Unset): Result offset for pagination (max 500)
        size (int | Unset): Number of results to return (max 100) Example: 10.
        session_id (str | Unset): Groups requests from the same conversation. Send back the sessionId from the previous
            response to continue a session; omit it to start a new one. Example: 8f14e45f-ceea-467e-a1a4-8f6c1c1a1a1a.
        customer_id (str | Unset): Caller-supplied end-user identifier, stable across sessions. Hashed before storage;
            never logged or returned in plain text. Example: user_48291.
    """

    query: str
    filters: list[SearchFilterType0 | SearchFilterType1 | SearchRangeFilter] | Unset = UNSET
    partition: str | Unset = UNSET
    routing: str | Unset = UNSET
    boost: SearchRequestBoost | Unset = UNSET
    from_: int | Unset = UNSET
    size: int | Unset = UNSET
    session_id: str | Unset = UNSET
    customer_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.search_filter_type_0 import SearchFilterType0
        from ..models.search_filter_type_1 import SearchFilterType1

        query = self.query

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

        boost: dict[str, Any] | Unset = UNSET
        if not isinstance(self.boost, Unset):
            boost = self.boost.to_dict()

        from_ = self.from_

        size = self.size

        session_id = self.session_id

        customer_id = self.customer_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if filters is not UNSET:
            field_dict["filters"] = filters
        if partition is not UNSET:
            field_dict["partition"] = partition
        if routing is not UNSET:
            field_dict["routing"] = routing
        if boost is not UNSET:
            field_dict["boost"] = boost
        if from_ is not UNSET:
            field_dict["from"] = from_
        if size is not UNSET:
            field_dict["size"] = size
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id
        if customer_id is not UNSET:
            field_dict["customerId"] = customer_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_filter_type_0 import SearchFilterType0
        from ..models.search_filter_type_1 import SearchFilterType1
        from ..models.search_range_filter import SearchRangeFilter
        from ..models.search_request_boost import SearchRequestBoost

        d = dict(src_dict)
        query = d.pop("query")

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

        _boost = d.pop("boost", UNSET)
        boost: SearchRequestBoost | Unset
        if isinstance(_boost, Unset):
            boost = UNSET
        else:
            boost = SearchRequestBoost.from_dict(_boost)

        from_ = d.pop("from", UNSET)

        size = d.pop("size", UNSET)

        session_id = d.pop("sessionId", UNSET)

        customer_id = d.pop("customerId", UNSET)

        search_request = cls(
            query=query,
            filters=filters,
            partition=partition,
            routing=routing,
            boost=boost,
            from_=from_,
            size=size,
            session_id=session_id,
            customer_id=customer_id,
        )

        search_request.additional_properties = d
        return search_request

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
