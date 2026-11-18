from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.filter_values_request import FilterValuesRequest
from ...models.filter_values_result import FilterValuesResult
from ...models.limit_error_response import LimitErrorResponse
from ...models.search_quota_error_response import SearchQuotaErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    index_name: str,
    *,
    body: FilterValuesRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/{org_id}/indexes/{index_name}/filter-values".format(
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
) -> ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse | None:
    if response.status_code == 200:
        response_200 = FilterValuesResult.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = SearchQuotaErrorResponse.from_dict(response.json())

        return response_402

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = LimitErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse]:
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
    body: FilterValuesRequest | Unset = UNSET,
) -> Response[ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse]:
    """List the filter values of an index

     Returns the most common values of the filterable fields of an index, with a document count for each
    value, and `count`: the number of documents that match every filter. The counts cover the partition
    (for an index with a partition field) and the `filters`. The value list of a field ignores the
    filters on that field. `complete` is false when the `size` limit left out values. A number or date
    field returns its min and max in `ranges`, for a `gte`/`lte` filter. Call it before you set a
    `filters` value in a search: a value that is not in the data returns no results. A response can come
    from a 60-second cache, and then counts as nothing. A cached response can show the index as it was
    up to 60 seconds before. Otherwise the request counts as one search against the rate limit and the
    monthly quota.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (FilterValuesRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse]
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
    body: FilterValuesRequest | Unset = UNSET,
) -> ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse | None:
    """List the filter values of an index

     Returns the most common values of the filterable fields of an index, with a document count for each
    value, and `count`: the number of documents that match every filter. The counts cover the partition
    (for an index with a partition field) and the `filters`. The value list of a field ignores the
    filters on that field. `complete` is false when the `size` limit left out values. A number or date
    field returns its min and max in `ranges`, for a `gte`/`lte` filter. Call it before you set a
    `filters` value in a search: a value that is not in the data returns no results. A response can come
    from a 60-second cache, and then counts as nothing. A cached response can show the index as it was
    up to 60 seconds before. Otherwise the request counts as one search against the rate limit and the
    monthly quota.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (FilterValuesRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse
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
    body: FilterValuesRequest | Unset = UNSET,
) -> Response[ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse]:
    """List the filter values of an index

     Returns the most common values of the filterable fields of an index, with a document count for each
    value, and `count`: the number of documents that match every filter. The counts cover the partition
    (for an index with a partition field) and the `filters`. The value list of a field ignores the
    filters on that field. `complete` is false when the `size` limit left out values. A number or date
    field returns its min and max in `ranges`, for a `gte`/`lte` filter. Call it before you set a
    `filters` value in a search: a value that is not in the data returns no results. A response can come
    from a 60-second cache, and then counts as nothing. A cached response can show the index as it was
    up to 60 seconds before. Otherwise the request counts as one search against the rate limit and the
    monthly quota.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (FilterValuesRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse]
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
    body: FilterValuesRequest | Unset = UNSET,
) -> ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse | None:
    """List the filter values of an index

     Returns the most common values of the filterable fields of an index, with a document count for each
    value, and `count`: the number of documents that match every filter. The counts cover the partition
    (for an index with a partition field) and the `filters`. The value list of a field ignores the
    filters on that field. `complete` is false when the `size` limit left out values. A number or date
    field returns its min and max in `ranges`, for a `gte`/`lte` filter. Call it before you set a
    `filters` value in a search: a value that is not in the data returns no results. A response can come
    from a 60-second cache, and then counts as nothing. A cached response can show the index as it was
    up to 60 seconds before. Otherwise the request counts as one search against the rate limit and the
    monthly quota.

    Permission: `read`. A read API key or a write API key can call this route.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (FilterValuesRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | FilterValuesResult | LimitErrorResponse | SearchQuotaErrorResponse
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            index_name=index_name,
            client=client,
            body=body,
        )
    ).parsed
