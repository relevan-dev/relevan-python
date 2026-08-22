from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.mapping_revision import MappingRevision
from ...types import Response


def _get_kwargs(
    org_id: str,
    index_name: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/{org_id}/indexes/{index_name}/mappings".format(
            org_id=quote(str(org_id), safe=""),
            index_name=quote(str(index_name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[MappingRevision] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_mappings_list_item_data in _response_200:
            componentsschemas_mappings_list_item = MappingRevision.from_dict(
                componentsschemas_mappings_list_item_data
            )

            response_200.append(componentsschemas_mappings_list_item)

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
) -> Response[ErrorResponse | list[MappingRevision]]:
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
) -> Response[ErrorResponse | list[MappingRevision]]:
    """List index mappings

     Retrieve a list of all mappings for an index.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[MappingRevision]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
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
) -> ErrorResponse | list[MappingRevision] | None:
    """List index mappings

     Retrieve a list of all mappings for an index.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[MappingRevision]
    """

    return sync_detailed(
        org_id=org_id,
        index_name=index_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    index_name: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | list[MappingRevision]]:
    """List index mappings

     Retrieve a list of all mappings for an index.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[MappingRevision]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    index_name: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | list[MappingRevision] | None:
    """List index mappings

     Retrieve a list of all mappings for an index.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[MappingRevision]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            index_name=index_name,
            client=client,
        )
    ).parsed
