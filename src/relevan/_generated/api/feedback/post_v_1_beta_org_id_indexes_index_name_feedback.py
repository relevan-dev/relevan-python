from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.feedback_request import FeedbackRequest
from ...models.message_response import MessageResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    index_name: str,
    *,
    body: FeedbackRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1-beta/{org_id}/indexes/{index_name}/feedback".format(
            org_id=quote(str(org_id), safe=""),
            index_name=quote(str(index_name), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | MessageResponse | None:
    if response.status_code == 202:
        response_202 = MessageResponse.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | MessageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    index_name: str,
    *,
    client: AuthenticatedClient | Client,
    body: FeedbackRequest | Unset = UNSET,
) -> Response[ErrorResponse | MessageResponse]:
    """Report feedback about a search result

     Report a click, an LLM relevance judgment, or a conversion event, attributed to the same sessionId
    and customerId a prior search used. Beta: this endpoint's contract may still change. See
    docs/search-feedback-logging-design.md.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (FeedbackRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MessageResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    index_name: str,
    *,
    client: AuthenticatedClient | Client,
    body: FeedbackRequest | Unset = UNSET,
) -> ErrorResponse | MessageResponse | None:
    """Report feedback about a search result

     Report a click, an LLM relevance judgment, or a conversion event, attributed to the same sessionId
    and customerId a prior search used. Beta: this endpoint's contract may still change. See
    docs/search-feedback-logging-design.md.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (FeedbackRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MessageResponse
    """

    return sync_detailed(
        org_id=org_id,
        index_name=index_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    index_name: str,
    *,
    client: AuthenticatedClient | Client,
    body: FeedbackRequest | Unset = UNSET,
) -> Response[ErrorResponse | MessageResponse]:
    """Report feedback about a search result

     Report a click, an LLM relevance judgment, or a conversion event, attributed to the same sessionId
    and customerId a prior search used. Beta: this endpoint's contract may still change. See
    docs/search-feedback-logging-design.md.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (FeedbackRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MessageResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    index_name: str,
    *,
    client: AuthenticatedClient | Client,
    body: FeedbackRequest | Unset = UNSET,
) -> ErrorResponse | MessageResponse | None:
    """Report feedback about a search result

     Report a click, an LLM relevance judgment, or a conversion event, attributed to the same sessionId
    and customerId a prior search used. Beta: this endpoint's contract may still change. See
    docs/search-feedback-logging-design.md.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (FeedbackRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MessageResponse
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            index_name=index_name,
            client=client,
            body=body,
        )
    ).parsed
