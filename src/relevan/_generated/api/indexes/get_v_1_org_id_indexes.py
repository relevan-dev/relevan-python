from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_v1_org_id_indexes_response_401 import GetV1OrgIdIndexesResponse401
from ...models.index import Index
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/{org_id}/indexes".format(
            org_id=quote(str(org_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> GetV1OrgIdIndexesResponse401 | list[Index] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_indexes_list_item_data in _response_200:
            componentsschemas_indexes_list_item = Index.from_dict(
                componentsschemas_indexes_list_item_data
            )

            response_200.append(componentsschemas_indexes_list_item)

        return response_200

    if response.status_code == 401:
        response_401 = GetV1OrgIdIndexesResponse401.from_dict(response.json())

        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[GetV1OrgIdIndexesResponse401 | list[Index]]:
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
    page: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[GetV1OrgIdIndexesResponse401 | list[Index]]:
    """List all indexes

     Retrieve a list of all indexes in the organization.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        page (int | Unset): Page number for pagination Example: 1.
        limit (int | Unset): Number of results per page Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetV1OrgIdIndexesResponse401 | list[Index]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        page=page,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> GetV1OrgIdIndexesResponse401 | list[Index] | None:
    """List all indexes

     Retrieve a list of all indexes in the organization.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        page (int | Unset): Page number for pagination Example: 1.
        limit (int | Unset): Number of results per page Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetV1OrgIdIndexesResponse401 | list[Index]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        page=page,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[GetV1OrgIdIndexesResponse401 | list[Index]]:
    """List all indexes

     Retrieve a list of all indexes in the organization.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        page (int | Unset): Page number for pagination Example: 1.
        limit (int | Unset): Number of results per page Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetV1OrgIdIndexesResponse401 | list[Index]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: AuthenticatedClient | Client,
    page: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> GetV1OrgIdIndexesResponse401 | list[Index] | None:
    """List all indexes

     Retrieve a list of all indexes in the organization.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        page (int | Unset): Page number for pagination Example: 1.
        limit (int | Unset): Number of results per page Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetV1OrgIdIndexesResponse401 | list[Index]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            page=page,
            limit=limit,
        )
    ).parsed
