from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_index import CreateIndex
from ...models.created_index import CreatedIndex
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    *,
    body: CreateIndex | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/{org_id}/indexes".format(
            org_id=quote(str(org_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreatedIndex | ErrorResponse | None:
    if response.status_code == 201:
        response_201 = CreatedIndex.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CreatedIndex | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateIndex | Unset = UNSET,
) -> Response[CreatedIndex | ErrorResponse]:
    """Create a new index

     Create a new search index in the organization. Right after you create the index, give the user the
    `consoleUrl` link from the response, in your next message. Do this before you deploy a mapping or
    upload documents. Do not wait and give the link only in a final summary. Tell the user to open the
    link to monitor the progress. Fetch `skillUrl` next, before you draft a mapping.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        body (CreateIndex | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreatedIndex | ErrorResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateIndex | Unset = UNSET,
) -> CreatedIndex | ErrorResponse | None:
    """Create a new index

     Create a new search index in the organization. Right after you create the index, give the user the
    `consoleUrl` link from the response, in your next message. Do this before you deploy a mapping or
    upload documents. Do not wait and give the link only in a final summary. Tell the user to open the
    link to monitor the progress. Fetch `skillUrl` next, before you draft a mapping.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        body (CreateIndex | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreatedIndex | ErrorResponse
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateIndex | Unset = UNSET,
) -> Response[CreatedIndex | ErrorResponse]:
    """Create a new index

     Create a new search index in the organization. Right after you create the index, give the user the
    `consoleUrl` link from the response, in your next message. Do this before you deploy a mapping or
    upload documents. Do not wait and give the link only in a final summary. Tell the user to open the
    link to monitor the progress. Fetch `skillUrl` next, before you draft a mapping.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        body (CreateIndex | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreatedIndex | ErrorResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateIndex | Unset = UNSET,
) -> CreatedIndex | ErrorResponse | None:
    """Create a new index

     Create a new search index in the organization. Right after you create the index, give the user the
    `consoleUrl` link from the response, in your next message. Do this before you deploy a mapping or
    upload documents. Do not wait and give the link only in a final summary. Tell the user to open the
    link to monitor the progress. Fetch `skillUrl` next, before you draft a mapping.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        body (CreateIndex | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreatedIndex | ErrorResponse
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            body=body,
        )
    ).parsed
