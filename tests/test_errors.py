import httpx
import pytest
import respx

from relevan import AsyncClient, Client
from relevan._errors import RelevanAPIError, RelevanAuthError, RelevanRateLimitError

BASE_URL = "https://api.dev.relevan.dev"
ORGS_URL = f"{BASE_URL}/v1/organizations"
SEARCH_URL = f"{BASE_URL}/v1/org-1/indexes/products/search"


@respx.mock
def test_401_without_a_message_raises_auth_error() -> None:
    respx.get(ORGS_URL).mock(return_value=httpx.Response(401, json={"error": "Unauthorized"}))
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    with pytest.raises(RelevanAuthError, match=r"GET /v1/organizations failed \(401\)"):
        client.organizations.list()


@respx.mock
def test_401_with_a_non_json_body_raises_auth_error() -> None:
    respx.get(ORGS_URL).mock(return_value=httpx.Response(401, text="Unauthorized"))
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    with pytest.raises(RelevanAuthError):
        client.organizations.list()


@respx.mock
async def test_async_401_without_a_message_raises_auth_error() -> None:
    respx.get(ORGS_URL).mock(return_value=httpx.Response(401, json={}))
    client = AsyncClient(api_key="relevan_test", base_url=BASE_URL)

    with pytest.raises(RelevanAuthError):
        await client.organizations.list()


@respx.mock
def test_429_with_only_a_message_raises_rate_limit_error_with_retry_after() -> None:
    respx.post(SEARCH_URL).mock(
        return_value=httpx.Response(
            429, json={"message": "Too many requests"}, headers={"Retry-After": "7"}
        )
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL, max_retries=0)

    with pytest.raises(RelevanRateLimitError, match="Too many requests") as excinfo:
        client.search.search("org-1", "products", query="tetra")
    assert excinfo.value.retry_after_seconds == 7


@respx.mock
def test_undocumented_status_with_a_non_json_body_raises_api_error() -> None:
    respx.post(SEARCH_URL).mock(return_value=httpx.Response(502, text="<html>Bad Gateway</html>"))
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    with pytest.raises(RelevanAPIError) as excinfo:
        client.search.search("org-1", "products", query="tetra")
    assert excinfo.value.status_code == 502
    assert str(excinfo.value) == "POST /v1/org-1/indexes/products/search failed (502)"
