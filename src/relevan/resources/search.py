from __future__ import annotations

from .._generated.api.search import (
    post_v_1_org_id_indexes_index_name_filter_values,
    post_v_1_org_id_indexes_index_name_search,
)
from .._generated.client import AuthenticatedClient
from .._generated.models.filter_values_request import FilterValuesRequest
from .._generated.models.filter_values_result import FilterValuesResult
from .._generated.models.search_filter_type_0 import SearchFilterType0
from .._generated.models.search_filter_type_1 import SearchFilterType1
from .._generated.models.search_range_filter import SearchRangeFilter
from .._generated.models.search_request import SearchRequest
from .._generated.models.search_request_boost import SearchRequestBoost
from .._generated.models.search_result import SearchResult
from .._generated.types import UNSET, Unset
from .._rate_limit import RateLimit, parse_rate_limit
from .._unwrap import unwrap

__all__ = [
    "AsyncSearch",
    "FilterValuesResult",
    "Search",
    "SearchFilterType0",
    "SearchFilterType1",
    "SearchRangeFilter",
    "SearchResult",
]

SearchFilter = SearchFilterType0 | SearchFilterType1 | SearchRangeFilter


def _search_request(
    query: str,
    filters: list[SearchFilter] | Unset,
    boost: dict[str, float] | Unset,
    offset: int | Unset,
    size: int | Unset,
    session_id: str | Unset,
    customer_id: str | Unset,
    partition: str | Unset,
    routing: str | Unset,
) -> SearchRequest:
    return SearchRequest(
        query=query,
        filters=filters,
        boost=SearchRequestBoost.from_dict(boost) if not isinstance(boost, Unset) else UNSET,
        from_=offset,
        size=size,
        session_id=session_id,
        customer_id=customer_id,
        partition=partition,
        routing=routing,
    )


class Search:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client
        self.last_rate_limit: RateLimit | None = None

    def search(
        self,
        org_id: str,
        index_name: str,
        *,
        query: str,
        filters: list[SearchFilter] | Unset = UNSET,
        boost: dict[str, float] | Unset = UNSET,
        offset: int | Unset = UNSET,
        size: int | Unset = UNSET,
        session_id: str | Unset = UNSET,
        customer_id: str | Unset = UNSET,
        partition: str | Unset = UNSET,
        routing: str | Unset = UNSET,
    ) -> SearchResult:
        """Search an index and get back the same rich, LLM-oriented result shape
        used by every caller — a direct API consumer or an agent.

        Each hit carries a human-readable `.explanation` of why it matched.
        `.search_context.query_id` identifies this request — pass it to
        `client.beta.send_feedback(...)` after acting on a result; that
        feedback is what improves future search quality. `.search_context
        .session_id` groups requests from the same conversation — send it
        back on the next call to continue the session.

        After this call, `self.last_rate_limit` holds the org's current
        `RateLimit-*` snapshot (limit / remaining / reset_seconds), if the
        server sent one.

        Args:
            org_id: The organization's id or slug.
            index_name: The index's URL-safe name.
            query: The search query text.
            filters: Exact-match or `gte`/`lte` range filters, ANDed together.
            boost: Per-term weight multipliers, e.g. `{"getting": 2}`.
            offset: Result offset for pagination (max 500).
            size: Number of results to return (max 100).
            session_id: The previous response's `session_id`, to continue a session.
            customer_id: A stable, caller-supplied end-user identifier.
            partition: The one partition to search, for an index that declares
                a partition field.
            routing: A value of the routing field, for an index that routes its
                documents by a field.

        Raises:
            RelevanRateLimitError: The org's search rate limit was exceeded
                and the client's automatic retries were exhausted.

        Example:
            >>> results = client.search.search(org_id, "products", query="wireless headphones")
            >>> results.results[0].explanation
        """
        body = _search_request(
            query, filters, boost, offset, size, session_id, customer_id, partition, routing
        )
        response = post_v_1_org_id_indexes_index_name_search.sync_detailed(
            org_id, index_name, client=self._client, body=body
        )
        self.last_rate_limit = parse_rate_limit(response.headers)
        return unwrap(response, success_type=SearchResult, endpoint="search.search")

    def filter_values(
        self,
        org_id: str,
        index_name: str,
        *,
        fields: list[str] | Unset = UNSET,
        size: int | Unset = UNSET,
        filters: list[SearchFilter] | Unset = UNSET,
        partition: str | Unset = UNSET,
        routing: str | Unset = UNSET,
    ) -> FilterValuesResult:
        """List the most common values of an index's filterable fields.

        Call this before you set a `filters` value in a search: a value that
        is not in the data returns no results. Number and date fields return
        their min and max in `.ranges`, for a `gte`/`lte` filter. A response
        that is not served from the API's 60-second cache counts as one search
        against the rate limit and the monthly quota.

        Args:
            org_id: The organization's id or slug.
            index_name: The index's URL-safe name.
            fields: The fields to list. Defaults to every filterable field.
            size: The most values to return for each field (default 20, max 100).
            filters: Filters, with the same schema as `search`.
            partition: The one partition to count, for a partitioned index.
            routing: A value of the routing field, for a routed index.

        Example:
            >>> values = client.search.filter_values(org_id, "products", fields=["brand"])
        """
        body = FilterValuesRequest(
            fields=fields, size=size, filters=filters, partition=partition, routing=routing
        )
        response = post_v_1_org_id_indexes_index_name_filter_values.sync_detailed(
            org_id, index_name, client=self._client, body=body
        )
        self.last_rate_limit = parse_rate_limit(response.headers)
        return unwrap(response, success_type=FilterValuesResult, endpoint="search.filter_values")


class AsyncSearch:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client
        self.last_rate_limit: RateLimit | None = None

    async def search(
        self,
        org_id: str,
        index_name: str,
        *,
        query: str,
        filters: list[SearchFilter] | Unset = UNSET,
        boost: dict[str, float] | Unset = UNSET,
        offset: int | Unset = UNSET,
        size: int | Unset = UNSET,
        session_id: str | Unset = UNSET,
        customer_id: str | Unset = UNSET,
        partition: str | Unset = UNSET,
        routing: str | Unset = UNSET,
    ) -> SearchResult:
        """Async version of `Search.search`."""
        body = _search_request(
            query, filters, boost, offset, size, session_id, customer_id, partition, routing
        )
        response = await post_v_1_org_id_indexes_index_name_search.asyncio_detailed(
            org_id, index_name, client=self._client, body=body
        )
        self.last_rate_limit = parse_rate_limit(response.headers)
        return unwrap(response, success_type=SearchResult, endpoint="search.search")

    async def filter_values(
        self,
        org_id: str,
        index_name: str,
        *,
        fields: list[str] | Unset = UNSET,
        size: int | Unset = UNSET,
        filters: list[SearchFilter] | Unset = UNSET,
        partition: str | Unset = UNSET,
        routing: str | Unset = UNSET,
    ) -> FilterValuesResult:
        """Async version of `Search.filter_values`."""
        body = FilterValuesRequest(
            fields=fields, size=size, filters=filters, partition=partition, routing=routing
        )
        response = await post_v_1_org_id_indexes_index_name_filter_values.asyncio_detailed(
            org_id, index_name, client=self._client, body=body
        )
        self.last_rate_limit = parse_rate_limit(response.headers)
        return unwrap(response, success_type=FilterValuesResult, endpoint="search.filter_values")
