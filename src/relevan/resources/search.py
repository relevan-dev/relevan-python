from __future__ import annotations

from .._generated.api.search import post_v_1_org_id_indexes_index_name_search
from .._generated.client import AuthenticatedClient
from .._generated.models.search_filter_type_0 import SearchFilterType0
from .._generated.models.search_filter_type_1 import SearchFilterType1
from .._generated.models.search_request import SearchRequest
from .._generated.models.search_request_boost import SearchRequestBoost
from .._generated.models.search_result import SearchResult
from .._generated.types import UNSET, Unset
from .._rate_limit import RateLimit, parse_rate_limit
from .._unwrap import unwrap

__all__ = ["AsyncSearch", "Search", "SearchFilterType0", "SearchFilterType1", "SearchResult"]

SearchFilter = SearchFilterType0 | SearchFilterType1


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
            filters: Exact-match filters, ANDed together.
            boost: Per-term weight multipliers, e.g. `{"getting": 2}`.
            offset: Result offset for pagination (max 500).
            size: Number of results to return (max 100).
            session_id: The previous response's `session_id`, to continue a session.
            customer_id: A stable, caller-supplied end-user identifier.

        Raises:
            RelevanRateLimitError: The org's search rate limit was exceeded
                and the client's automatic retries were exhausted.

        Example:
            >>> results = client.search.search(org_id, "products", query="wireless headphones")
            >>> results.results[0].explanation
        """
        body = SearchRequest(
            query=query,
            filters=filters,
            boost=SearchRequestBoost.from_dict(boost) if not isinstance(boost, Unset) else UNSET,
            from_=offset,
            size=size,
            session_id=session_id,
            customer_id=customer_id,
        )
        response = post_v_1_org_id_indexes_index_name_search.sync_detailed(
            org_id, index_name, client=self._client, body=body
        )
        self.last_rate_limit = parse_rate_limit(response.headers)
        return unwrap(response, success_type=SearchResult, endpoint="search.search")


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
    ) -> SearchResult:
        """Async version of `Search.search`."""
        body = SearchRequest(
            query=query,
            filters=filters,
            boost=SearchRequestBoost.from_dict(boost) if not isinstance(boost, Unset) else UNSET,
            from_=offset,
            size=size,
            session_id=session_id,
            customer_id=customer_id,
        )
        response = await post_v_1_org_id_indexes_index_name_search.asyncio_detailed(
            org_id, index_name, client=self._client, body=body
        )
        self.last_rate_limit = parse_rate_limit(response.headers)
        return unwrap(response, success_type=SearchResult, endpoint="search.search")
