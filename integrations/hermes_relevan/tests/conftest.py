"""Stand-ins for the Hermes modules the provider imports, so the tests run without Hermes."""

from __future__ import annotations

import os
import sys
import threading
import types
from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def _install_hermes_stubs() -> None:
    try:
        import agent.memory_provider

        return
    except ImportError:
        pass

    @dataclass(frozen=True)
    class RecallStatus:
        provider_label: str
        count: int
        glyph: str = "🧠"

    class MemoryProvider(ABC):  # noqa: B024
        pass

    def spawn_context_thread(
        target: Any,
        *,
        name: str,
        daemon: bool = True,
        args: tuple[Any, ...] = (),
        kwargs: Any = None,
    ) -> threading.Thread:
        return threading.Thread(target=target, args=args, kwargs=kwargs, name=name, daemon=daemon)

    def get_secret(name: str, default: str | None = None) -> str | None:
        return os.environ.get(name, default)

    agent = types.ModuleType("agent")
    memory_provider = types.ModuleType("agent.memory_provider")
    memory_provider.MemoryProvider = MemoryProvider  # type: ignore[attr-defined]
    memory_provider.RecallStatus = RecallStatus  # type: ignore[attr-defined]
    memory_provider.spawn_context_thread = spawn_context_thread  # type: ignore[attr-defined]
    secret_scope = types.ModuleType("agent.secret_scope")
    secret_scope.get_secret = get_secret  # type: ignore[attr-defined]
    constants = types.ModuleType("hermes_constants")
    constants.get_hermes_home = lambda: Path(os.environ.get("HERMES_HOME", "."))  # type: ignore[attr-defined]
    sys.modules.update(
        {
            "agent": agent,
            "agent.memory_provider": memory_provider,
            "agent.secret_scope": secret_scope,
            "hermes_constants": constants,
        }
    )


_install_hermes_stubs()
