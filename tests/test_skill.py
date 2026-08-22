import httpx
import pytest
import respx

from relevan import Client
from relevan._errors import RelevanAuthError

BASE_URL = "https://api.dev.relevan.dev"


@respx.mock
def test_get_skill_doc_returns_markdown_text() -> None:
    respx.get(f"{BASE_URL}/v1/org-1/indexes/products/skill").mock(
        return_value=httpx.Response(200, text="# products\n\nSearchable fields: name, price.")
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    doc = client.skill.get("org-1", "products")

    assert doc.startswith("# products")


@respx.mock
def test_get_skill_doc_raises_auth_error_on_401() -> None:
    respx.get(f"{BASE_URL}/v1/org-1/indexes/products/skill").mock(
        return_value=httpx.Response(401, json={"message": "Unauthorized"})
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    with pytest.raises(RelevanAuthError):
        client.skill.get("org-1", "products")
