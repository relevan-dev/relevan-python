from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bulk_ingest_request import BulkIngestRequest
from ...models.bulk_ingest_response import BulkIngestResponse
from ...models.bulk_validation_error_response import BulkValidationErrorResponse
from ...models.error_response import ErrorResponse
from ...models.storage_limit_error_response import StorageLimitErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    org_id: str,
    index_name: str,
    *,
    body: BulkIngestRequest | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/{org_id}/indexes/{index_name}/documents/_bulk".format(
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
) -> (
    BulkIngestResponse
    | BulkValidationErrorResponse
    | ErrorResponse
    | StorageLimitErrorResponse
    | None
):
    if response.status_code == 202:
        response_202 = BulkIngestResponse.from_dict(response.json())

        return response_202

    if response.status_code == 400:
        response_400 = BulkValidationErrorResponse.from_dict(response.json())

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
) -> Response[
    BulkIngestResponse | BulkValidationErrorResponse | ErrorResponse | StorageLimitErrorResponse
]:
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
    body: BulkIngestRequest | Unset = UNSET,
) -> Response[
    BulkIngestResponse | BulkValidationErrorResponse | ErrorResponse | StorageLimitErrorResponse
]:
    """Bulk ingest documents

     Ingest up to 1000 documents in a single request. If any document fails mapping validation, the
    entire request is rejected (no partial writes). Existing documents with matching IDs are upserted.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (BulkIngestRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkIngestResponse | BulkValidationErrorResponse | ErrorResponse | StorageLimitErrorResponse]
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
    body: BulkIngestRequest | Unset = UNSET,
) -> (
    BulkIngestResponse
    | BulkValidationErrorResponse
    | ErrorResponse
    | StorageLimitErrorResponse
    | None
):
    """Bulk ingest documents

     Ingest up to 1000 documents in a single request. If any document fails mapping validation, the
    entire request is rejected (no partial writes). Existing documents with matching IDs are upserted.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (BulkIngestRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkIngestResponse | BulkValidationErrorResponse | ErrorResponse | StorageLimitErrorResponse
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
    body: BulkIngestRequest | Unset = UNSET,
) -> Response[
    BulkIngestResponse | BulkValidationErrorResponse | ErrorResponse | StorageLimitErrorResponse
]:
    """Bulk ingest documents

     Ingest up to 1000 documents in a single request. If any document fails mapping validation, the
    entire request is rejected (no partial writes). Existing documents with matching IDs are upserted.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (BulkIngestRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BulkIngestResponse | BulkValidationErrorResponse | ErrorResponse | StorageLimitErrorResponse]
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
    body: BulkIngestRequest | Unset = UNSET,
) -> (
    BulkIngestResponse
    | BulkValidationErrorResponse
    | ErrorResponse
    | StorageLimitErrorResponse
    | None
):
    """Bulk ingest documents

     Ingest up to 1000 documents in a single request. If any document fails mapping validation, the
    entire request is rejected (no partial writes). Existing documents with matching IDs are upserted.

    Permission: `write`. Only a write API key can call this route. A read API key gets 403.

    Args:
        org_id (str):
        index_name (str): URL-safe index name (lowercase alphanumeric + hyphens, unique within
            org) Example: products.
        body (BulkIngestRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BulkIngestResponse | BulkValidationErrorResponse | ErrorResponse | StorageLimitErrorResponse
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            index_name=index_name,
            client=client,
            body=body,
        )
    ).parsed
