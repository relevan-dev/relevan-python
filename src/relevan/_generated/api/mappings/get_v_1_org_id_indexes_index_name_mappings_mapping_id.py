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
    mapping_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/{org_id}/indexes/{index_name}/mappings/{mapping_id}".format(
            org_id=quote(str(org_id), safe=""),
            index_name=quote(str(index_name), safe=""),
            mapping_id=quote(str(mapping_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | MappingRevision | None:
    if response.status_code == 200:
        response_200 = MappingRevision.from_dict(response.json())

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
) -> Response[ErrorResponse | MappingRevision]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    index_name: str,
    mapping_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | MappingRevision]:
    """Get index mapping

     Retrieve the mapping given the mapping ID.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        mapping_id (str): Mapping revision identifier Example:
            550e8400-e29b-41d4-a716-446655440000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MappingRevision]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
        mapping_id=mapping_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    index_name: str,
    mapping_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | MappingRevision | None:
    """Get index mapping

     Retrieve the mapping given the mapping ID.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        mapping_id (str): Mapping revision identifier Example:
            550e8400-e29b-41d4-a716-446655440000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MappingRevision
    """

    return sync_detailed(
        org_id=org_id,
        index_name=index_name,
        mapping_id=mapping_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    index_name: str,
    mapping_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | MappingRevision]:
    """Get index mapping

     Retrieve the mapping given the mapping ID.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        mapping_id (str): Mapping revision identifier Example:
            550e8400-e29b-41d4-a716-446655440000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | MappingRevision]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        index_name=index_name,
        mapping_id=mapping_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    index_name: str,
    mapping_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | MappingRevision | None:
    """Get index mapping

     Retrieve the mapping given the mapping ID.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        mapping_id (str): Mapping revision identifier Example:
            550e8400-e29b-41d4-a716-446655440000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | MappingRevision
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            index_name=index_name,
            mapping_id=mapping_id,
            client=client,
        )
    ).parsed
