from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.limit_error_response import LimitErrorResponse
from ...models.search_request import SearchRequest
from ...models.search_result import SearchResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    index_name: str,
    *,
    body: SearchRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/{org_id}/indexes/{index_name}/search".format(
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
) -> ErrorResponse | LimitErrorResponse | SearchResult | None:
    if response.status_code == 200:
        response_200 = SearchResult.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = LimitErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | LimitErrorResponse | SearchResult]:
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
    body: SearchRequest | Unset = UNSET,
) -> Response[ErrorResponse | LimitErrorResponse | SearchResult]:
    """Search an index

     Execute a search query against an index. Returns the same rich, LLM-oriented result shape for every
    caller — direct API consumer or agent.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (SearchRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LimitErrorResponse | SearchResult]
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
    body: SearchRequest | Unset = UNSET,
) -> ErrorResponse | LimitErrorResponse | SearchResult | None:
    """Search an index

     Execute a search query against an index. Returns the same rich, LLM-oriented result shape for every
    caller — direct API consumer or agent.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (SearchRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LimitErrorResponse | SearchResult
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
    body: SearchRequest | Unset = UNSET,
) -> Response[ErrorResponse | LimitErrorResponse | SearchResult]:
    """Search an index

     Execute a search query against an index. Returns the same rich, LLM-oriented result shape for every
    caller — direct API consumer or agent.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (SearchRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | LimitErrorResponse | SearchResult]
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
    body: SearchRequest | Unset = UNSET,
) -> ErrorResponse | LimitErrorResponse | SearchResult | None:
    """Search an index

     Execute a search query against an index. Returns the same rich, LLM-oriented result shape for every
    caller — direct API consumer or agent.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (SearchRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | LimitErrorResponse | SearchResult
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            index_name=index_name,
            client=client,
            body=body,
        )
    ).parsed
