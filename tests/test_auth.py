import pytest

from relevan._auth import mask_api_key, resolve_api_key
from relevan._errors import RelevanAuthError


def test_resolve_api_key_prefers_explicit_argument(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RELEVAN_API_KEY", "relevan_from_env")
    assert resolve_api_key("relevan_explicit") == "relevan_explicit"


def test_resolve_api_key_falls_back_to_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RELEVAN_API_KEY", "relevan_from_env")
    assert resolve_api_key(None) == "relevan_from_env"


def test_resolve_api_key_raises_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("RELEVAN_API_KEY", raising=False)
    with pytest.raises(RelevanAuthError):
        resolve_api_key(None)


def test_mask_api_key_never_exposes_the_secret() -> None:
    masked = mask_api_key("relevan_supersecretvalue")
    assert masked.startswith("relevan_")
    assert "supersecretvalue" not in masked
