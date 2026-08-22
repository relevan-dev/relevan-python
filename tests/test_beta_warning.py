import httpx
import pytest
import respx

from relevan import Client
from relevan._beta import RelevanBetaWarning
from relevan._generated.models.feedback_request_action_name import FeedbackRequestActionName

BASE_URL = "https://api.dev.relevan.dev"


@respx.mock
def test_send_feedback_emits_a_beta_warning() -> None:
    respx.post(f"{BASE_URL}/v1-beta/org-1/indexes/products/feedback").mock(
        return_value=httpx.Response(202, json={"message": "ok"})
    )
    client = Client(api_key="relevan_test", base_url=BASE_URL)

    with pytest.warns(RelevanBetaWarning):
        client.beta.send_feedback(
            "org-1",
            "products",
            action_name=FeedbackRequestActionName.CLICK,
            query_id="query-1",
            object_id="sku-1",
        )
