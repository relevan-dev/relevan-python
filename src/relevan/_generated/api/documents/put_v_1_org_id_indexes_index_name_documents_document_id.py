from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document import Document
from ...models.error_response import ErrorResponse
from ...models.storage_limit_error_response import StorageLimitErrorResponse
from ...models.update_document import UpdateDocument
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    index_name: str,
    document_id: str,
    *,
    body: UpdateDocument | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/v1/{org_id}/indexes/{index_name}/documents/{document_id}".format(
            org_id=quote(str(org_id), safe=""),
            index_name=quote(str(index_name), safe=""),
            document_id=quote(str(document_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Document | ErrorResponse | StorageLimitErrorResponse | None:
    if response.status_code == 200:
        response_200 = Document.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = StorageLimitErrorResponse.from_dict(response.json())

        return response_402

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Document | ErrorResponse | StorageLimitErrorResponse]:
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
    body: UpdateDocument | Unset = UNSET,
) -> Response[Document | ErrorResponse | StorageLimitErrorResponse]:
    """Update a document

     Replaces document content. All provided fields must be declared in the index mapping.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        index_name (str):
        document_id (str): Unique document identifier Example: doc_42a1b8d9.
        body (UpdateDocument | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Document | ErrorResponse | StorageLimitErrorResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
        document_id=document_id,
        body=body,
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
    body: UpdateDocument | Unset = UNSET,
) -> Document | ErrorResponse | StorageLimitErrorResponse | None:
    """Update a document

     Replaces document content. All provided fields must be declared in the index mapping.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        index_name (str):
        document_id (str): Unique document identifier Example: doc_42a1b8d9.
        body (UpdateDocument | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Document | ErrorResponse | StorageLimitErrorResponse
    """

    return sync_detailed(
        org_id=org_id,
        index_name=index_name,
        document_id=document_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    index_name: str,
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateDocument | Unset = UNSET,
) -> Response[Document | ErrorResponse | StorageLimitErrorResponse]:
    """Update a document

     Replaces document content. All provided fields must be declared in the index mapping.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        index_name (str):
        document_id (str): Unique document identifier Example: doc_42a1b8d9.
        body (UpdateDocument | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Document | ErrorResponse | StorageLimitErrorResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
        document_id=document_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    index_name: str,
    document_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateDocument | Unset = UNSET,
) -> Document | ErrorResponse | StorageLimitErrorResponse | None:
    """Update a document

     Replaces document content. All provided fields must be declared in the index mapping.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        index_name (str):
        document_id (str): Unique document identifier Example: doc_42a1b8d9.
        body (UpdateDocument | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Document | ErrorResponse | StorageLimitErrorResponse
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            index_name=index_name,
            document_id=document_id,
            client=client,
            body=body,
        )
    ).parsed
