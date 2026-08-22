from __future__ import annotations

from .._beta import warn_beta
from .._generated.api.feedback import post_v_1_beta_org_id_indexes_index_name_feedback
from .._generated.client import AuthenticatedClient
from .._generated.models.feedback_request import FeedbackRequest
from .._generated.models.feedback_request_action_name import FeedbackRequestActionName
from .._generated.models.message_response import MessageResponse
from .._generated.types import UNSET, Unset
from .._unwrap import unwrap

__all__ = ["AsyncBeta", "Beta", "FeedbackRequestActionName"]


class Beta:
    """Endpoints under the API's `/v1-beta` path.

    **Beta.** These endpoints' contracts may change without warning. Every
    call here emits a `relevan.RelevanBetaWarning`.
    """

    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def send_feedback(
        self,
        org_id: str,
        index_name: str,
        *,
        action_name: FeedbackRequestActionName,
        query_id: str | Unset = UNSET,
        object_id: str | Unset = UNSET,
        position: int | Unset = UNSET,
        label: str | Unset = UNSET,
        session_id: str | Unset = UNSET,
        customer_id: str | Unset = UNSET,
    ) -> MessageResponse:
        """Report what happened after a search — not optional.

        An agent that searches but never reports what happened teaches
        Relevan nothing. Send this after every result you act on: a click, an
        agent's own relevance judgment (`llm_judgment`), or a closing event
        such as a purchase or a hire (`conversion`).

        At least one of `query_id`, `session_id`, or `customer_id` is
        required. `object_id` is required when `action_name` is `"click"` or
        `"llm_judgment"`.

        Args:
            org_id: The organization's id or slug.
            index_name: The index's URL-safe name.
            action_name: `"click"`, `"llm_judgment"`, or `"conversion"`.
            query_id: The `search_context.query_id` from the search this feedback concerns.
            object_id: The id of the result this feedback is about.
            position: The result's rank position in the response, when known.
            label: A short name for a conversion event, e.g. `"hire"` or `"purchase"`.
            session_id: The `session_id` used on the search this feedback concerns.
            customer_id: The `customer_id` used on the search this feedback concerns.

        Example:
            >>> client.beta.send_feedback(
            ...     org_id, "products",
            ...     action_name=FeedbackRequestActionName.CLICK,
            ...     query_id=results.search_context.query_id,
            ...     object_id=results.results[0].id,
            ...     position=0,
            ... )
        """
        warn_beta("beta.send_feedback")
        body = FeedbackRequest(
            action_name=action_name,
            query_id=query_id,
            object_id=object_id,
            position=position,
            label=label,
            session_id=session_id,
            customer_id=customer_id,
        )
        response = post_v_1_beta_org_id_indexes_index_name_feedback.sync_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=MessageResponse, endpoint="beta.send_feedback")


class AsyncBeta:
    """Async version of `Beta`."""

    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    async def send_feedback(
        self,
        org_id: str,
        index_name: str,
        *,
        action_name: FeedbackRequestActionName,
        query_id: str | Unset = UNSET,
        object_id: str | Unset = UNSET,
        position: int | Unset = UNSET,
        label: str | Unset = UNSET,
        session_id: str | Unset = UNSET,
        customer_id: str | Unset = UNSET,
    ) -> MessageResponse:
        """Async version of `Beta.send_feedback`."""
        warn_beta("beta.send_feedback")
        body = FeedbackRequest(
            action_name=action_name,
            query_id=query_id,
            object_id=object_id,
            position=position,
            label=label,
            session_id=session_id,
            customer_id=customer_id,
        )
        response = await post_v_1_beta_org_id_indexes_index_name_feedback.asyncio_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=MessageResponse, endpoint="beta.send_feedback")
