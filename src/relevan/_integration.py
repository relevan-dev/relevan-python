from __future__ import annotations

from importlib.metadata import version

INTEGRATION_HEADER = "X-Relevan-Integration"


def resolve_integration(integration: str | None) -> str:
    """Resolve the `X-Relevan-Integration` value that every request sends.

    The API records it on search and feedback events, so Relevan can tell
    which integration sent the traffic. It is a label, not a credential.

    Args:
        integration: `<name>/<version>`, for example `"hermes/0.1.0"`, or
            `None` for this client's own name and version.

    Returns:
        The value to send: the argument, else `python/<this package's version>`.
    """
    return integration if integration is not None else f"python/{version('relevan')}"
