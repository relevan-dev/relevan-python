import json
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx
from hermes_relevan import RelevanMemoryProvider, register
from hermes_relevan.client import INTEGRATION

BASE_URL = "https://api.dev.relevan.dev"
SEARCH_URL = f"{BASE_URL}/v1/org-1/indexes/hermes-notes/search"
FEEDBACK_URL = f"{BASE_URL}/v1-beta/org-1/indexes/hermes-notes/feedback"
ACCEPTED = httpx.Response(202, json={"message": "Feedback accepted"})


def _hit(doc_id: str, title: str, body: str) -> dict[str, Any]:
    return {
        "id": doc_id,
        "score": 3.0,
        "document": {"title": title, "body": body, "tags": ["homelab"]},
        "explanation": "",
        "matchedFields": ["body"],
        "matchedTerms": [],
    }


def _search_body(query_id: str) -> dict[str, Any]:
    return {
        "results": [
            _hit(
                "obsidian:proxmox-1",
                "Proxmox backup plan",
                "Nightly vzdump of every VM to the Synology NAS at 02:00 with zstd.",
            ),
            _hit(
                "obsidian:wireguard-2",
                "Wireguard VPN",
                "WireGuard runs on the OPNsense router, port 51820 UDP.",
            ),
        ],
        "searchContext": {
            "queryUsed": "backups",
            "totalHits": 2,
            "matchedTerms": [],
            "topContributingFields": ["body"],
            "titleField": "title",
            "scoringSummary": "",
            "suggestions": "",
            "searchableFields": ["title", "body"],
            "sessionId": "hermes-session",
            "queryId": query_id,
        },
        "took": 4,
    }


@pytest.fixture
def provider(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> RelevanMemoryProvider:
    monkeypatch.setenv("RELEVAN_API_KEY", "relevan_test_key")
    (tmp_path / "relevan.json").write_text(
        json.dumps({"index": "hermes-notes", "org_id": "org-1", "base_url": BASE_URL}),
        encoding="utf-8",
    )
    instance = RelevanMemoryProvider()
    assert instance.is_available()
    instance.initialize("hermes-session", hermes_home=str(tmp_path), platform="cli")
    return instance


def _feedback_bodies(route: respx.Route) -> list[dict[str, Any]]:
    return [json.loads(call.request.content) for call in route.calls]


def test_register_hands_hermes_a_new_instance() -> None:
    registered: list[Any] = []

    class Ctx:
        def register_memory_provider(self, provider: Any) -> None:
            registered.append(provider)

    register(Ctx())
    register(Ctx())
    assert isinstance(registered[0], RelevanMemoryProvider)
    assert registered[0] is not registered[1]


@respx.mock
def test_prefetch_recalls_and_sync_turn_sends_llm_judgment(
    provider: RelevanMemoryProvider,
) -> None:
    search = respx.post(SEARCH_URL).mock(return_value=httpx.Response(200, json=_search_body("q-1")))
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)

    block = provider.prefetch("how are my VMs backed up?", session_id="hermes-session")

    assert 'query_id="q-1"' in block
    assert "[obsidian:proxmox-1] Proxmox backup plan — body: Nightly vzdump" in block
    status = provider.recall_status()
    assert status is not None
    assert status.count == 2
    assert json.loads(search.calls.last.request.content)["sessionId"] == "hermes-session"

    provider.sync_turn(
        "how are my VMs backed up?",
        "Every night at 02:00 vzdump copies them to the Synology [obsidian:proxmox-1].",
        session_id="hermes-session",
    )
    provider.shutdown()

    assert _feedback_bodies(feedback) == [
        {
            "actionName": "llm_judgment",
            "source": "production",
            "queryId": "q-1",
            "objectId": "obsidian:proxmox-1",
            "position": 0,
            "sessionId": "hermes-session",
            "grade": 2,
            "description": "Hermes reply cited the result id.",
        }
    ]
    for call in [*search.calls, *feedback.calls]:
        assert call.request.headers["X-Relevan-Integration"] == INTEGRATION


@respx.mock
def test_sync_turn_sends_nothing_when_the_reply_ignores_the_recall(
    provider: RelevanMemoryProvider,
) -> None:
    respx.post(SEARCH_URL).mock(return_value=httpx.Response(200, json=_search_body("q-2")))
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)

    provider.prefetch("tell me a joke", session_id="hermes-session")
    provider.sync_turn(
        "tell me a joke", "Why did the scarecrow win an award?", session_id="hermes-session"
    )
    provider.shutdown()

    assert feedback.calls.call_count == 0


@respx.mock
def test_feedback_tool_sends_grade_and_suppresses_the_implicit_event(
    provider: RelevanMemoryProvider,
) -> None:
    respx.post(SEARCH_URL).mock(return_value=httpx.Response(200, json=_search_body("q-3")))
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)

    provider.prefetch("vpn port?", session_id="hermes-session")
    result = json.loads(
        provider.handle_tool_call(
            "relevan_feedback",
            {
                "query_id": "q-3",
                "object_id": "obsidian:wireguard-2",
                "action": "unhelpful",
                "reason": "The user moved the VPN to Tailscale.",
            },
        )
    )
    provider.sync_turn("vpn port?", "It was [obsidian:wireguard-2].", session_id="hermes-session")
    provider.shutdown()

    assert result["ok"] is True
    bodies = _feedback_bodies(feedback)
    assert len(bodies) == 1
    assert bodies[0]["grade"] == 0
    assert bodies[0]["description"] == "The user moved the VPN to Tailscale."


@respx.mock
def test_search_tool_results_also_get_implicit_feedback(provider: RelevanMemoryProvider) -> None:
    respx.post(SEARCH_URL).mock(return_value=httpx.Response(200, json=_search_body("q-4")))
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)

    provider.on_turn_start(1, "vpn?")
    result = json.loads(provider.handle_tool_call("relevan_search", {"query": "wireguard"}))
    provider.sync_turn("vpn?", "Wireguard VPN listens on 51820.", session_id="hermes-session")
    provider.shutdown()

    assert result["query_id"] == "q-4"
    assert [r["id"] for r in result["results"]] == ["obsidian:proxmox-1", "obsidian:wireguard-2"]
    assert [(b["queryId"], b["objectId"]) for b in _feedback_bodies(feedback)] == [
        ("q-4", "obsidian:wireguard-2")
    ]


@respx.mock
def test_a_failed_search_recalls_nothing(provider: RelevanMemoryProvider) -> None:
    respx.post(SEARCH_URL).mock(return_value=httpx.Response(500, json={"message": "boom"}))

    assert provider.prefetch("anything", session_id="hermes-session") == ""
    assert provider.recall_status() is None


def test_subagents_send_no_implicit_feedback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("RELEVAN_API_KEY", "relevan_test_key")
    instance = RelevanMemoryProvider()
    instance.initialize("s", hermes_home=str(tmp_path), agent_context="subagent")
    with respx.mock(assert_all_called=False) as mock:
        feedback = mock.post(url__regex=r".*/feedback").mock(return_value=httpx.Response(202))
        instance.sync_turn("q", "a", session_id="s")
    assert feedback.calls.call_count == 0


@respx.mock
def test_recall_shows_numbers_booleans_and_lists_by_name(provider: RelevanMemoryProvider) -> None:
    body = _search_body("q-5")
    body["results"] = [
        {
            **_hit("product:cl-500", "Rain shell jacket", "Three-layer waterproof shell."),
            "document": {
                "title": "Rain shell jacket",
                "description": "Three-layer waterproof shell with pit zips.",
                "price": 249.0,
                "in_stock": True,
                "tags": ["waterproof", "jacket"],
            },
        }
    ]
    respx.post(SEARCH_URL).mock(return_value=httpx.Response(200, json=body))

    block = provider.prefetch("rain jacket", session_id="hermes-session")

    assert (
        "[product:cl-500] Rain shell jacket — description: Three-layer waterproof shell with "
        "pit zips.; price: 249.0; in_stock: yes; tags: waterproof, jacket"
    ) in block


@respx.mock
def test_a_recall_slower_than_the_budget_is_dropped(
    provider: RelevanMemoryProvider, monkeypatch: pytest.MonkeyPatch
) -> None:
    respx.post(SEARCH_URL).mock(return_value=httpx.Response(200, json=_search_body("q-6")))
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)
    clock = iter([100.0, 107.0])
    monkeypatch.setattr("hermes_relevan.provider.time.monotonic", lambda: next(clock))

    assert provider.prefetch("backups", session_id="hermes-session") == ""
    assert provider.recall_status() is None
    provider.sync_turn("backups", "[obsidian:proxmox-1] runs nightly.", session_id="hermes-session")
    provider.shutdown()

    assert feedback.calls.call_count == 0


def test_non_primary_agents_get_no_feedback_tool(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("RELEVAN_API_KEY", "relevan_test_key")
    instance = RelevanMemoryProvider()
    instance.initialize("s", hermes_home=str(tmp_path), agent_context="cron")

    assert [schema["name"] for schema in instance.get_tool_schemas()] == ["relevan_search"]
    with respx.mock(assert_all_called=False) as mock:
        feedback = mock.post(url__regex=r".*/feedback").mock(return_value=ACCEPTED)
        result = json.loads(
            instance.handle_tool_call(
                "relevan_feedback", {"query_id": "q", "object_id": "o", "action": "helpful"}
            )
        )
    assert "error" in result
    assert feedback.calls.call_count == 0


@respx.mock
def test_a_late_sync_judges_only_its_own_turn(provider: RelevanMemoryProvider) -> None:
    respx.post(SEARCH_URL).mock(
        side_effect=[
            httpx.Response(200, json=_search_body("turn-1")),
            httpx.Response(200, json=_search_body("turn-2")),
        ]
    )
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)

    provider.on_turn_start(1, "how are my VMs backed up?")
    provider.prefetch("how are my VMs backed up?", session_id="hermes-session")
    provider.on_turn_start(2, "which port does the VPN use?")
    provider.prefetch("which port does the VPN use?", session_id="hermes-session")
    provider.sync_turn(
        "how are my VMs backed up?", "See [obsidian:proxmox-1].", session_id="hermes-session"
    )
    provider.sync_turn(
        "which port does the VPN use?", "See [obsidian:wireguard-2].", session_id="hermes-session"
    )
    provider.shutdown()

    assert sorted((b["queryId"], b["objectId"]) for b in _feedback_bodies(feedback)) == [
        ("turn-1", "obsidian:proxmox-1"),
        ("turn-2", "obsidian:wireguard-2"),
    ]


@respx.mock
def test_an_unsynced_turn_cannot_take_a_later_turns_searches(
    provider: RelevanMemoryProvider,
) -> None:
    respx.post(SEARCH_URL).mock(
        side_effect=[
            httpx.Response(200, json=_search_body("turn-1")),
            httpx.Response(200, json=_search_body("turn-2")),
        ]
    )
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)

    provider.on_turn_start(1, "list my VM backups")
    provider.prefetch("list my VM backups", session_id="hermes-session")
    provider.on_turn_start(2, "list my VM backups, and show the schedule")
    provider.prefetch("list my VM backups, and show the schedule", session_id="hermes-session")
    provider.sync_turn(
        "list my VM backups, and show the schedule",
        "See [obsidian:proxmox-1].",
        session_id="hermes-session",
    )
    provider.sync_turn("yes", "See [obsidian:wireguard-2].", session_id="hermes-session")
    provider.shutdown()

    assert [(b["queryId"], b["objectId"]) for b in _feedback_bodies(feedback)] == [
        ("turn-2", "obsidian:proxmox-1")
    ]


@respx.mock
def test_a_sync_with_images_matches_its_turn(provider: RelevanMemoryProvider) -> None:
    respx.post(SEARCH_URL).mock(return_value=httpx.Response(200, json=_search_body("turn-1")))
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)

    provider.on_turn_start(1, "which VM is this?")
    provider.prefetch("which VM is this?", session_id="hermes-session")
    provider.sync_turn(
        "[1 image] which VM is this?", "That is [obsidian:proxmox-1].", session_id="hermes-session"
    )
    provider.shutdown()

    assert [(b["queryId"], b["objectId"]) for b in _feedback_bodies(feedback)] == [
        ("turn-1", "obsidian:proxmox-1")
    ]


@respx.mock
def test_a_text_message_that_starts_like_an_image_count_matches_its_turn(
    provider: RelevanMemoryProvider,
) -> None:
    respx.post(SEARCH_URL).mock(return_value=httpx.Response(200, json=_search_body("turn-1")))
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)

    provider.on_turn_start(1, "[1 image] check this")
    provider.prefetch("[1 image] check this", session_id="hermes-session")
    provider.sync_turn(
        "[1 image] check this", "See [obsidian:proxmox-1].", session_id="hermes-session"
    )
    provider.shutdown()

    assert [(b["queryId"], b["objectId"]) for b in _feedback_bodies(feedback)] == [
        ("turn-1", "obsidian:proxmox-1")
    ]


@respx.mock
def test_a_resent_message_judges_only_the_new_turns_searches(
    provider: RelevanMemoryProvider,
) -> None:
    respx.post(SEARCH_URL).mock(
        side_effect=[
            httpx.Response(200, json=_search_body("turn-1")),
            httpx.Response(200, json=_search_body("turn-2")),
        ]
    )
    feedback = respx.post(FEEDBACK_URL).mock(return_value=ACCEPTED)

    provider.on_turn_start(1, "list my VM backups")
    provider.prefetch("list my VM backups", session_id="hermes-session")
    provider.on_turn_start(2, "list my VM backups")
    provider.prefetch("list my VM backups", session_id="hermes-session")
    provider.sync_turn(
        "list my VM backups", "See [obsidian:proxmox-1].", session_id="hermes-session"
    )
    provider.shutdown()

    assert [(b["queryId"], b["objectId"]) for b in _feedback_bodies(feedback)] == [
        ("turn-2", "obsidian:proxmox-1")
    ]
