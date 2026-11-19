"""The Relevan memory provider for Hermes Agent."""

from __future__ import annotations

import json
import logging
import threading
import time
import warnings
from pathlib import Path
from typing import Any

from agent.memory_provider import MemoryProvider, RecallStatus, spawn_context_thread
from agent.secret_scope import get_secret

from .client import DEFAULT_BASE_URL, make_client
from .usage import RecalledHit, used_results

logger = logging.getLogger(__name__)

API_KEY_ENV = "RELEVAN_API_KEY"
CONFIG_FILE = "relevan.json"
DEFAULTS: dict[str, Any] = {
    "index": "",
    "org_id": "",
    "base_url": DEFAULT_BASE_URL,
    "recall_size": 5,
    "auto_feedback": True,
    "source": "production",
}
SNIPPET_CHARS = 600
SHORT_FIELD_CHARS = 80
PREFETCH_BUDGET_S = 6.0
MAX_RECALLS_PER_TURN = 8

SYSTEM_PROMPT = """# Relevan search memory
Relevan searches the user's index "{index}" before each turn. Results appear in a
<relevan-recall> block, each with an id in square brackets. When your reply uses a
result, cite its id, like [obsidian:trip-plan-1a2b3c4d5e]. Relevan learns from which
results you use. Use relevan_search for a different query, and relevan_feedback to mark
a result helpful or unhelpful when the user confirms or corrects an answer."""

SEARCH_SCHEMA = {
    "name": "relevan_search",
    "description": (
        "Search the user's Relevan index (their notes, documents or catalog). Returns results "
        "with ids and a query_id. Cite the id of each result you use."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "What to look for, in plain words."},
            "limit": {"type": "integer", "description": "Results to return, 1 to 20. Default 5."},
        },
        "required": ["query"],
    },
}

FEEDBACK_SCHEMA = {
    "name": "relevan_feedback",
    "description": (
        "Tell Relevan whether a search result was helpful. Use it when the user confirms an "
        "answer that used a result, or corrects one. This trains the ranking."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query_id": {"type": "string", "description": "The query_id of the search."},
            "object_id": {"type": "string", "description": "The id of the result."},
            "action": {
                "type": "string",
                "enum": ["helpful", "unhelpful"],
                "description": "helpful: the result answered the need. unhelpful: it did not.",
            },
            "reason": {"type": "string", "description": "Optional: why, in one sentence."},
        },
        "required": ["query_id", "object_id", "action"],
    },
}


def _field_value(value: Any) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        return ", ".join(_field_value(item) for item in value if not isinstance(item, (dict, list)))
    return " ".join(str(value).split())


def _hit_text(document: dict[str, Any], title_field: str | None) -> tuple[str, str]:
    """The title, and the other fields as `name: value`, short fields before long text."""
    title = str(document.get(title_field, "")) if title_field else ""
    fields = [
        (key, _field_value(value))
        for key, value in document.items()
        if key != title_field and value not in (None, "", []) and not isinstance(value, dict)
    ]
    fields.sort(key=lambda field: len(field[1]) > SHORT_FIELD_CHARS)
    return title, "; ".join(f"{key}: {value}" for key, value in fields if value)[:SNIPPET_CHARS]


class _Search:
    """One search's id and the results the model saw."""

    def __init__(self, query: str, query_id: str, hits: list[RecalledHit]) -> None:
        self.query = query
        self.query_id = query_id
        self.hits = hits


class RelevanMemoryProvider(MemoryProvider):
    """Search a Relevan index before each turn, and report which results the reply used."""

    def __init__(self) -> None:
        self._config = dict(DEFAULTS)
        self._client: Any = None
        self._org_id = ""
        self._session_id = ""
        self._agent_context = "primary"
        self._lock = threading.Lock()
        self._turn_searches: dict[str, list[_Search]] = {}
        self._judged: set[tuple[str, str]] = set()
        self._last_count: int | None = None
        self._threads: list[threading.Thread] = []

    @property
    def name(self) -> str:
        return "relevan"

    def is_available(self) -> bool:
        return bool(get_secret(API_KEY_ENV))

    def unavailable_reason(self) -> str:
        return f"Set {API_KEY_ENV} and an index name with: hermes memory setup"

    def get_config_schema(self) -> list[dict[str, Any]]:
        return [
            {
                "key": "api_key",
                "description": "Relevan API key (a write key if you load a preset)",
                "secret": True,
                "required": True,
                "env_var": API_KEY_ENV,
                "url": "https://console.relevan.dev",
            },
            {
                "key": "index",
                "description": "Index to search, for example hermes-notes",
                "required": True,
                "default": "hermes-notes",
            },
        ]

    def save_config(self, values: dict[str, Any], hermes_home: str) -> None:
        path = Path(hermes_home) / CONFIG_FILE
        current = _read_config(path)
        current.update({k: v for k, v in values.items() if k in DEFAULTS})
        path.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")

    def initialize(self, session_id: str, **kwargs: Any) -> None:
        hermes_home = Path(kwargs.get("hermes_home") or ".")
        self._config = {**DEFAULTS, **_read_config(hermes_home / CONFIG_FILE)}
        self._session_id = session_id
        self._org_id = str(self._config["org_id"] or "")
        self._agent_context = kwargs.get("agent_context", "primary")
        self._client = make_client(
            get_secret(API_KEY_ENV) or "",
            base_url=str(self._config["base_url"]),
            timeout=PREFETCH_BUDGET_S - 1,
        )

    def on_session_switch(self, new_session_id: str, **kwargs: Any) -> None:
        self._session_id = new_session_id

    def system_prompt_block(self) -> str:
        if not self._config["index"]:
            return ""
        return SYSTEM_PROMPT.format(index=self._config["index"])

    def _org(self) -> str:
        if not self._org_id:
            self._org_id = self._client.organizations.list()[0].id
        return self._org_id

    def _search(self, query: str, size: int, session_id: str) -> _Search:
        result = self._client.search.search(
            self._org(),
            self._config["index"],
            query=query,
            size=size,
            session_id=session_id or self._session_id or None,
        )
        context = result.search_context
        title_field = context.title_field if isinstance(context.title_field, str) else None
        hits = []
        for position, hit in enumerate(result.results):
            title, text = _hit_text(hit.document.to_dict(), title_field)
            hits.append(RecalledHit(hit.id, position, title, text))
        return _Search(query, context.query_id, hits)

    def _record(self, search: _Search, session_id: str) -> None:
        """Keep a search whose results the model saw, for this turn's feedback check."""
        with self._lock:
            searches = self._turn_searches.setdefault(session_id or self._session_id, [])
            searches.append(search)
            del searches[:-MAX_RECALLS_PER_TURN]

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        self._last_count = None
        if not self._client or not self._config["index"] or not query.strip():
            return ""
        started = time.monotonic()
        try:
            search = self._search(query, int(self._config["recall_size"]), session_id)
        except Exception as exc:
            logger.warning("Relevan recall failed: %s", exc)
            return ""
        if time.monotonic() - started > PREFETCH_BUDGET_S:
            logger.warning(
                "Relevan recall took over %.0f s; Hermes has moved on", PREFETCH_BUDGET_S
            )
            return ""
        self._record(search, session_id)
        self._last_count = len(search.hits)
        if not search.hits:
            return ""
        lines = [f'<relevan-recall index="{self._config["index"]}" query_id="{search.query_id}">']
        for hit in search.hits:
            lines.append(
                " — ".join(part for part in (f"[{hit.object_id}] {hit.title}", hit.text) if part)
            )
        lines.append("</relevan-recall>")
        return "\n".join(lines)

    def recall_status(self) -> RecallStatus | None:
        if not self._last_count:
            return None
        return RecallStatus(provider_label="Relevan", count=self._last_count)

    def sync_turn(
        self,
        user_content: str,
        assistant_content: str,
        *,
        session_id: str = "",
        messages: list[dict[str, Any]] | None = None,
    ) -> None:
        with self._lock:
            searches = self._turn_searches.pop(session_id or self._session_id, [])
        if not searches or not self._config["auto_feedback"]:
            return
        if self._agent_context != "primary":
            return
        thread = spawn_context_thread(
            self._send_implicit_feedback,
            name="relevan-feedback",
            args=(searches, user_content, assistant_content, session_id or self._session_id),
        )
        self._threads = [t for t in self._threads if t.is_alive()] + [thread]
        thread.start()

    def _send_implicit_feedback(
        self, searches: list[_Search], user_content: str, reply: str, session_id: str
    ) -> None:
        for search in searches:
            for usage in used_results(search.hits, user_content, reply):
                key = (search.query_id, usage.hit.object_id)
                with self._lock:
                    if key in self._judged:
                        continue
                    self._judged.add(key)
                try:
                    self._feedback(
                        query_id=search.query_id,
                        object_id=usage.hit.object_id,
                        position=usage.hit.position,
                        grade=usage.grade,
                        session_id=session_id,
                        description=f"Hermes reply {usage.reason}.",
                    )
                except Exception as exc:
                    logger.warning("Relevan feedback failed: %s", exc)
                    continue
                logger.info(
                    "Relevan llm_judgment sent: query %s, result %s, grade %d (%s)",
                    search.query_id,
                    usage.hit.object_id,
                    usage.grade,
                    usage.reason,
                )

    def _feedback(self, **fields: Any) -> None:
        fields = {k: v for k, v in fields.items() if v not in (None, "")}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._client.beta.send_feedback(
                self._org(),
                self._config["index"],
                action_name="llm_judgment",
                source=self._config["source"],
                **fields,
            )

    def get_tool_schemas(self) -> list[dict[str, Any]]:
        if self._agent_context != "primary":
            return [SEARCH_SCHEMA]
        return [SEARCH_SCHEMA, FEEDBACK_SCHEMA]

    def handle_tool_call(self, tool_name: str, args: dict[str, Any], **kwargs: Any) -> str:
        try:
            if tool_name == "relevan_search":
                return self._tool_search(args)
            if tool_name == "relevan_feedback":
                return self._tool_feedback(args)
        except Exception as exc:
            return json.dumps({"error": str(exc)})
        return json.dumps({"error": f"Unknown tool {tool_name}"})

    def _tool_search(self, args: dict[str, Any]) -> str:
        query = str(args.get("query") or "").strip()
        if not query:
            return json.dumps({"error": "query is required"})
        size = max(1, min(20, int(args.get("limit") or 5)))
        search = self._search(query, size, self._session_id)
        self._record(search, self._session_id)
        return json.dumps(
            {
                "query_id": search.query_id,
                "results": [
                    {"id": h.object_id, "position": h.position, "title": h.title, "text": h.text}
                    for h in search.hits
                ],
            },
            ensure_ascii=False,
        )

    def _tool_feedback(self, args: dict[str, Any]) -> str:
        if self._agent_context != "primary":
            return json.dumps({"error": "Feedback is only sent from the primary agent"})
        query_id = str(args.get("query_id") or "")
        object_id = str(args.get("object_id") or "")
        action = args.get("action")
        if not query_id or not object_id or action not in {"helpful", "unhelpful"}:
            return json.dumps({"error": "query_id, object_id and action are required"})
        with self._lock:
            self._judged.add((query_id, object_id))
        self._feedback(
            query_id=query_id,
            object_id=object_id,
            grade=2 if action == "helpful" else 0,
            session_id=self._session_id,
            description=str(args.get("reason") or "").strip()[:2000] or None,
        )
        return json.dumps({"ok": True, "query_id": query_id, "object_id": object_id})

    def shutdown(self) -> None:
        for thread in self._threads:
            thread.join(timeout=5.0)
        if self._client is not None:
            self._client.close()


def _read_config(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}
