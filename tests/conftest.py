import pytest

BASE_URL = "https://api.dev.relevan.dev"


@pytest.fixture
def api_key() -> str:
    return "relevan_test_key_1234567890"
