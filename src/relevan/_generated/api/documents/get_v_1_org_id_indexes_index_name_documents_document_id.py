from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document import Document
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    org_id: str,
    index_name: str,
    document_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/{org_id}/indexes/{index_name}/documents/{document_id}".format(
            org_id=quote(str(org_id), safe=""),
            index_name=quote(str(index_name), safe=""),
            document_id=quote(str(document_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Document | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = Document.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Document | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    index_name: str,
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Document | ErrorResponse]:
    """Get a single document

     Retrieve a specific active document by ID from an index.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str):
        document_id (str): Unique document identifier Example: doc_42a1b8d9.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Document | ErrorResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
        document_id=document_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    index_name: str,
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Document | ErrorResponse | None:
    """Get a single document

     Retrieve a specific active document by ID from an index.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str):
        document_id (str): Unique document identifier Example: doc_42a1b8d9.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Document | ErrorResponse
    """

    return sync_detailed(
        org_id=org_id,
        index_name=index_name,
        document_id=document_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    index_name: str,
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Document | ErrorResponse]:
    """Get a single document

     Retrieve a specific active document by ID from an index.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str):
        document_id (str): Unique document identifier Example: doc_42a1b8d9.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Document | ErrorResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
        document_id=document_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    index_name: str,
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Document | ErrorResponse | None:
    """Get a single document

     Retrieve a specific active document by ID from an index.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str):
        document_id (str): Unique document identifier Example: doc_42a1b8d9.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Document | ErrorResponse
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            index_name=index_name,
            document_id=document_id,
            client=client,
        )
    ).parsed
