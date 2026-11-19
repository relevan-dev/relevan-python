"""Relevan memory provider for Hermes Agent: search recall with feedback that trains ranking."""

from __future__ import annotations

from typing import Any

from .provider import RelevanMemoryProvider

__all__ = ["RelevanMemoryProvider", "register"]


def register(ctx: Any) -> None:
    """Hermes entry point: hand Hermes a new provider instance."""
    ctx.register_memory_provider(RelevanMemoryProvider())
