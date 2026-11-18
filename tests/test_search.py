import httpx
import pytest
import respx

from relevan import AsyncClient, Client
from relevan._errors import RelevanAPIError

BASE_URL = "https://api.dev.relevan.dev"


def _search_success_body() -> dict:
    return {
        "results": [
            {
                "id": "sku-1",
                "score": 12.4,
                "document": {},
                "explanation": '"tetra" in name (12.4). Total score: 12.400.',
                "matchedFields": ["name"],
                "matchedTerms": ["tetra"],
            }
        ],
        "searchContext": {
            "queryUsed": "tetra",
            "totalHits": 1,
            "matchedTerms": ["tetra"],
            "topContributingFields": ["name"],
            "titleField": "name",
            "scoringSummary": "1 field matched",
            "suggestions": "",
            "searchableFields": ["name", "description"],
            "sessionId": "session-1",
            "queryId": "query-1",
        },
        "took": 3,
    }


@respx.mock
def test_search_returns_hits_with_explanations() -> None:
    respx.post(f"{BASE_URL}/v1/org-1/indexes/products/search").mock(
        return_value=httpx.Response(200, json=_search_success_body())
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    result = client.search.search("org-1", "products", query="tetra")

    assert result.results[0].id == "sku-1"
    assert "tetra" in result.results[0].explanation
    assert result.search_context.session_id == "session-1"


@respx.mock
def test_search_raises_relevan_api_error_on_400() -> None:
    respx.post(f"{BASE_URL}/v1/org-1/indexes/products/search").mock(
        return_value=httpx.Response(
            400, json={"message": "Index not found", "error": "no such index"}
        )
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    with pytest.raises(RelevanAPIError) as excinfo:
        client.search.search("org-1", "products", query="tetra")
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "no such index"


@respx.mock
async def test_async_search_returns_hits_with_explanations() -> None:
    respx.post(f"{BASE_URL}/v1/org-1/indexes/products/search").mock(
        return_value=httpx.Response(200, json=_search_success_body())
    )
    async with AsyncClient(api_key="relevan_test", base_url=BASE_URL) as client:
        result = await client.search.search("org-1", "products", query="tetra")

    assert result.results[0].id == "sku-1"
