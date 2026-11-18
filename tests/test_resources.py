import json

import httpx
import pytest
import respx

from relevan import Client, RelevanBetaWarning

BASE_URL = "https://api.dev.relevan.dev"

INDEX = {
    "id": "idx-1",
    "organizationId": "org-1",
    "indexName": "products",
    "displayName": "Products",
    "description": None,
    "status": "ready",
    "readyAt": "2026-10-06T20:00:00.146Z",
    "failedAt": None,
    "createdAt": "2026-10-06T19:59:40.217Z",
    "updatedAt": "2026-10-06T20:00:00.145Z",
}


@respx.mock
def test_get_index_returns_the_index_detail() -> None:
    respx.get(f"{BASE_URL}/v1/org-1/indexes/products").mock(
        return_value=httpx.Response(
            200,
            json={
                **INDEX,
                "documentsAccepted": 10,
                "documentsIndexed": 9,
                "documentsAcceptedChangedAt": None,
                "readyToSearch": True,
            },
        )
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    index = client.indexes.get("org-1", "products")

    assert index.documents_indexed == 9
    assert index.ready_to_search is True


@respx.mock
def test_create_index_returns_the_created_index() -> None:
    respx.post(f"{BASE_URL}/v1/org-1/indexes").mock(
        return_value=httpx.Response(
            201,
            json={
                **INDEX,
                "status": "creating",
                "readyAt": None,
                "consoleUrl": "https://console.relevan.dev/indexes/products",
                "skillUrl": f"{BASE_URL}/v1/org-1/indexes/products/skill",
            },
        )
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    index = client.indexes.create("org-1", name="products")

    assert index.skill_url.endswith("/skill")


@respx.mock
def test_usage_returns_the_storage_usage() -> None:
    respx.get(f"{BASE_URL}/v1/org-1/usage").mock(
        return_value=httpx.Response(
            200,
            json={
                "tier": "starter",
                "storage": {"usedBytes": 100, "limitBytes": None, "remainingBytes": None},
            },
        )
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    usage = client.usage.get("org-1")

    assert usage.storage.used_bytes == 100


@respx.mock
def test_filter_values_sends_the_fields_and_returns_the_counts() -> None:
    route = respx.post(f"{BASE_URL}/v1/org-1/indexes/products/filter-values").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 3,
                "fields": {
                    "brand": {
                        "values": [{"value": "Acme", "count": 3}],
                        "otherCount": 0,
                        "total": 3,
                        "missing": 0,
                        "distinct": 1,
                        "complete": True,
                    }
                },
                "ranges": {},
            },
        )
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    result = client.search.filter_values("org-1", "products", fields=["brand"])

    assert json.loads(route.calls.last.request.content) == {"fields": ["brand"]}
    assert result.count == 3


@respx.mock
def test_send_feedback_serializes_a_search_judgment() -> None:
    route = respx.post(f"{BASE_URL}/v1-beta/org-1/indexes/products/feedback").mock(
        return_value=httpx.Response(202, json={"message": "ok"})
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    with pytest.warns(RelevanBetaWarning):
        client.beta.send_feedback(
            "org-1",
            "products",
            action_name="search_judgment",
            source="eval",
            query_id="query-1",
            grade=1,
            results=[
                {"object_id": "sku-1", "grade": 2, "position": 0},
                {"object_id": "sku-2", "grade": 0},
            ],
            description="The user wanted boots.",
        )

    assert json.loads(route.calls.last.request.content) == {
        "actionName": "search_judgment",
        "source": "eval",
        "queryId": "query-1",
        "grade": 1,
        "results": [
            {"objectId": "sku-1", "grade": 2, "position": 0},
            {"objectId": "sku-2", "grade": 0},
        ],
        "description": "The user wanted boots.",
    }
