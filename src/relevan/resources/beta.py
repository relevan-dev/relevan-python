from __future__ import annotations

from typing import Any, Literal, TypedDict

from .._beta import warn_beta
from .._generated.api.feedback import post_v_1_beta_org_id_indexes_index_name_feedback
from .._generated.client import AuthenticatedClient
from .._generated.models.feedback_request import FeedbackRequest
from .._generated.models.feedback_request_action_name import FeedbackRequestActionName
from .._generated.models.feedback_request_source import FeedbackRequestSource
from .._generated.models.message_response import MessageResponse
from .._generated.types import UNSET, Unset
from .._unwrap import unwrap

__all__ = [
    "AsyncBeta",
    "Beta",
    "FeedbackRequestActionName",
    "FeedbackRequestSource",
    "JudgedResult",
]

FeedbackAction = (
    FeedbackRequestActionName | Literal["click", "conversion", "llm_judgment", "search_judgment"]
)
FeedbackSource = FeedbackRequestSource | Literal["production", "eval"]
Grade = Literal[0, 1, 2]


class _JudgedResultRequired(TypedDict):
    object_id: str
    grade: Grade


class JudgedResult(_JudgedResultRequired, total=False):
    """One result's grade inside a `search_judgment`."""

    position: int


def _feedback_request(
    action_name: FeedbackAction,
    source: FeedbackSource | Unset,
    query_id: str | Unset,
    object_id: str | Unset,
    position: int | Unset,
    label: str | Unset,
    session_id: str | Unset,
    customer_id: str | Unset,
    grade: Grade | Unset,
    results: list[JudgedResult] | Unset,
    description: str | Unset,
) -> FeedbackRequest:
    body: dict[str, Any] = {
        "actionName": action_name,
        "source": source,
        "queryId": query_id,
        "objectId": object_id,
        "position": position,
        "label": label,
        "sessionId": session_id,
        "customerId": customer_id,
        "grade": grade,
        "description": description,
    }
    if not isinstance(results, Unset):
        body["results"] = [
            {"objectId": r["object_id"], "grade": r["grade"], "position": r.get("position", UNSET)}
            for r in results
        ]
    return FeedbackRequest.from_dict(
        {key: value for key, value in body.items() if not isinstance(value, Unset)}
    )


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
        action_name: FeedbackAction,
        source: FeedbackSource | Unset = UNSET,
        query_id: str | Unset = UNSET,
        object_id: str | Unset = UNSET,
        position: int | Unset = UNSET,
        label: str | Unset = UNSET,
        session_id: str | Unset = UNSET,
        customer_id: str | Unset = UNSET,
        grade: Grade | Unset = UNSET,
        results: list[JudgedResult] | Unset = UNSET,
        description: str | Unset = UNSET,
    ) -> MessageResponse:
        """Report what happened after a search — not optional.

        An agent that searches but never reports what happened teaches
        Relevan nothing. Send this after every result you act on: a click, an
        agent's own relevance judgment of one result (`llm_judgment`) or of
        the whole search (`search_judgment`), or a closing event such as a
        purchase or a hire (`conversion`).

        At least one of `query_id`, `session_id`, or `customer_id` is
        required. `object_id` is required when `action_name` is `"click"` or
        `"llm_judgment"`. The API accepts one `search_judgment` per
        `query_id`; a second one gets a 409.

        Args:
            org_id: The organization's id or slug.
            index_name: The index's URL-safe name.
            action_name: `"click"`, `"llm_judgment"`, `"search_judgment"`, or `"conversion"`.
            source: `"production"` (the API default) for real traffic, or `"eval"`
                for a test suite or benchmark run.
            query_id: The `search_context.query_id` from the search this feedback concerns.
            object_id: The id of the result this feedback is about.
            position: The result's rank position in the response, when known.
            label: A short name for a conversion event, e.g. `"hire"` or `"purchase"`.
            session_id: The `session_id` used on the search this feedback concerns.
            customer_id: The `customer_id` used on the search this feedback concerns.
            grade: How useful the result was: 0 not useful, 1 a little useful,
                2 very useful. With `search_judgment`, it grades the whole search.
            results: Per-result grades for a `search_judgment`, at most 100.
            description: Free text, at most 2000 characters: what the user
                wanted, and why the results did or did not match.

        Example:
            >>> client.beta.send_feedback(
            ...     org_id, "products",
            ...     action_name="click",
            ...     query_id=results.search_context.query_id,
            ...     object_id=results.results[0].id,
            ...     position=0,
            ... )
        """
        warn_beta("beta.send_feedback")
        body = _feedback_request(
            action_name,
            source,
            query_id,
            object_id,
            position,
            label,
            session_id,
            customer_id,
            grade,
            results,
            description,
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
        action_name: FeedbackAction,
        source: FeedbackSource | Unset = UNSET,
        query_id: str | Unset = UNSET,
        object_id: str | Unset = UNSET,
        position: int | Unset = UNSET,
        label: str | Unset = UNSET,
        session_id: str | Unset = UNSET,
        customer_id: str | Unset = UNSET,
        grade: Grade | Unset = UNSET,
        results: list[JudgedResult] | Unset = UNSET,
        description: str | Unset = UNSET,
    ) -> MessageResponse:
        """Async version of `Beta.send_feedback`."""
        warn_beta("beta.send_feedback")
        body = _feedback_request(
            action_name,
            source,
            query_id,
            object_id,
            position,
            label,
            session_id,
            customer_id,
            grade,
            results,
            description,
        )
        response = await post_v_1_beta_org_id_indexes_index_name_feedback.asyncio_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=MessageResponse, endpoint="beta.send_feedback")
