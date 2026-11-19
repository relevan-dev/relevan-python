import httpx
import pytest
import respx

from relevan import AsyncClient, Client, __version__

BASE_URL = "https://api.dev.relevan.dev"
ORGS_URL = f"{BASE_URL}/v1/organizations"


@respx.mock
def test_client_sends_its_own_name_and_version_by_default() -> None:
    route = respx.get(ORGS_URL).mock(return_value=httpx.Response(200, json=[]))
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    client.organizations.list()

    assert route.calls.last.request.headers["X-Relevan-Integration"] == f"python/{__version__}"


@respx.mock
def test_client_sends_the_integration_that_the_caller_passes() -> None:
    route = respx.get(ORGS_URL).mock(return_value=httpx.Response(200, json=[]))
    client = Client(api_key="relevan_test", base_url=BASE_URL, integration="hermes/0.1.0")

    client.organizations.list()

    assert route.calls.last.request.headers["X-Relevan-Integration"] == "hermes/0.1.0"


@respx.mock
@pytest.mark.asyncio
async def test_async_client_sends_the_integration_header() -> None:
    route = respx.get(ORGS_URL).mock(return_value=httpx.Response(200, json=[]))
    default = AsyncClient(api_key="relevan_test", base_url=BASE_URL)
    custom = AsyncClient(api_key="relevan_test", base_url=BASE_URL, integration="hermes/0.1.0")

    await default.organizations.list()
    await custom.organizations.list()

    sent = [call.request.headers["X-Relevan-Integration"] for call in route.calls]
    assert sent == [f"python/{__version__}", "hermes/0.1.0"]
