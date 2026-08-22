from __future__ import annotations

from .._generated.api.search import get_v_1_org_id_indexes_index_name_skill
from .._generated.client import AuthenticatedClient
from .._unwrap import unwrap

__all__ = ["AsyncSkill", "Skill"]


class Skill:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def get(self, org_id: str, index_name: str) -> str:
        """Get an agent-oriented skill doc for an index.

        Returns Markdown describing the index's live schema and how to query
        it — generated from the index's current mapping. Fetch this once per
        index before searching it as an agent, rather than guessing field
        names.

        Args:
            org_id: The organization's id or slug.
            index_name: The index's URL-safe name.

        Returns:
            The skill doc as Markdown text.
        """
        response = get_v_1_org_id_indexes_index_name_skill.sync_detailed(
            org_id, index_name, client=self._client
        )
        return unwrap(response, success_type=str, endpoint="skill.get")


class AsyncSkill:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    async def get(self, org_id: str, index_name: str) -> str:
        """Async version of `Skill.get`."""
        response = await get_v_1_org_id_indexes_index_name_skill.asyncio_detailed(
            org_id, index_name, client=self._client
        )
        return unwrap(response, success_type=str, endpoint="skill.get")
