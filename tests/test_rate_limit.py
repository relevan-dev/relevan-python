import httpx
import respx

from relevan import Client
from relevan._errors import RelevanRateLimitError

BASE_URL = "https://api.dev.relevan.dev"


def _limit_error_body(remaining: int = 0) -> dict:
    return {
        "message": "Too many requests",
        "code": "rate_limit_exceeded",
        "limit": 60,
        "remaining": remaining,
        "resetAt": "2026-01-01T00:01:00.000Z",
        "retryAfterSeconds": 0,
    }


def _search_success_body() -> dict:
    return {
        "results": [],
        "searchContext": {
            "queryUsed": "tetra",
            "totalHits": 0,
            "matchedTerms": [],
            "topContributingFields": [],
            "scoringSummary": "",
            "suggestions": "",
            "searchableFields": [],
            "sessionId": "session-1",
            "queryId": "query-1",
        },
        "took": 1,
    }


@respx.mock
def test_search_retries_a_429_and_returns_the_eventual_success() -> None:
    route = respx.post(f"{BASE_URL}/v1/org-1/indexes/products/search")
    route.side_effect = [
        httpx.Response(429, json=_limit_error_body(), headers={"Retry-After": "0"}),
        httpx.Response(200, json=_search_success_body()),
    ]

    client = Client(api_key="relevan_test", base_url=BASE_URL)
    result = client.search.search("org-1", "products", query="tetra")

    assert result.search_context.query_id == "query-1"
    assert route.call_count == 2


@respx.mock
def test_search_raises_after_exhausting_retries() -> None:
    respx.post(f"{BASE_URL}/v1/org-1/indexes/products/search").mock(
        return_value=httpx.Response(429, json=_limit_error_body(), headers={"Retry-After": "0"})
    )

    client = Client(api_key="relevan_test", base_url=BASE_URL, max_retries=1)

    try:
        client.search.search("org-1", "products", query="tetra")
        raise AssertionError("expected RelevanRateLimitError")
    except RelevanRateLimitError as error:
        assert error.retry_after_seconds == 0


@respx.mock
def test_search_exposes_rate_limit_headers_on_success() -> None:
    respx.post(f"{BASE_URL}/v1/org-1/indexes/products/search").mock(
        return_value=httpx.Response(
            200,
            json=_search_success_body(),
            headers={"RateLimit-Limit": "60", "RateLimit-Remaining": "59", "RateLimit-Reset": "30"},
        )
    )

    client = Client(api_key="relevan_test", base_url=BASE_URL)
    client.search.search("org-1", "products", query="tetra")

    assert client.search.last_rate_limit is not None
    assert client.search.last_rate_limit.remaining == 59
