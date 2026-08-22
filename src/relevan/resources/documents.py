from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .._generated.api.documents import (
    delete_v_1_org_id_indexes_index_name_documents_document_id,
    get_v_1_org_id_indexes_index_name_documents,
    get_v_1_org_id_indexes_index_name_documents_document_id,
    post_v_1_org_id_indexes_index_name_documents,
    post_v_1_org_id_indexes_index_name_documents_bulk,
    put_v_1_org_id_indexes_index_name_documents_document_id,
)
from .._generated.client import AuthenticatedClient
from .._generated.models.bulk_ingest_item import BulkIngestItem
from .._generated.models.bulk_ingest_item_content import BulkIngestItemContent
from .._generated.models.bulk_ingest_request import BulkIngestRequest
from .._generated.models.bulk_ingest_response import BulkIngestResponse
from .._generated.models.create_document import CreateDocument
from .._generated.models.create_document_content import CreateDocumentContent
from .._generated.models.document import Document
from .._generated.models.documents_list import DocumentsList
from .._generated.models.message_response import MessageResponse
from .._generated.models.update_document import UpdateDocument
from .._generated.models.update_document_content import UpdateDocumentContent
from .._generated.types import UNSET, Unset
from .._unwrap import unwrap

__all__ = ["AsyncDocuments", "Document", "Documents"]


class Documents:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    def list(
        self,
        org_id: str,
        index_name: str,
        *,
        page: int | Unset = UNSET,
        limit: int | Unset = UNSET,
    ) -> DocumentsList:
        """List the documents in an index, paginated."""
        response = get_v_1_org_id_indexes_index_name_documents.sync_detailed(
            org_id, index_name, client=self._client, page=page, limit=limit
        )
        return unwrap(response, success_type=DocumentsList, endpoint="documents.list")

    def get(self, org_id: str, index_name: str, document_id: str) -> Document:
        """Get one document by id."""
        response = get_v_1_org_id_indexes_index_name_documents_document_id.sync_detailed(
            org_id, index_name, document_id, client=self._client
        )
        return unwrap(response, success_type=Document, endpoint="documents.get")

    def create(self, org_id: str, index_name: str, *, id: str, content: dict[str, Any]) -> Document:
        """Create a document. Every field in `content` must be declared in the index mapping.

        Args:
            org_id: The organization's id or slug.
            index_name: The index's URL-safe name.
            id: Caller-supplied document id, unique within the index.
            content: The document's field values, matching the index mapping.
        """
        body = CreateDocument(id=id, content=CreateDocumentContent.from_dict(content))
        response = post_v_1_org_id_indexes_index_name_documents.sync_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=Document, endpoint="documents.create")

    def update(
        self, org_id: str, index_name: str, document_id: str, *, content: dict[str, Any]
    ) -> Document:
        """Replace a document's content."""
        body = UpdateDocument(content=UpdateDocumentContent.from_dict(content))
        response = put_v_1_org_id_indexes_index_name_documents_document_id.sync_detailed(
            org_id, index_name, document_id, client=self._client, body=body
        )
        return unwrap(response, success_type=Document, endpoint="documents.update")

    def delete(self, org_id: str, index_name: str, document_id: str) -> MessageResponse:
        """Delete a document."""
        response = delete_v_1_org_id_indexes_index_name_documents_document_id.sync_detailed(
            org_id, index_name, document_id, client=self._client
        )
        return unwrap(response, success_type=MessageResponse, endpoint="documents.delete")

    def bulk_ingest(
        self, org_id: str, index_name: str, *, documents: Sequence[tuple[str, dict[str, Any]]]
    ) -> BulkIngestResponse:
        """Ingest up to 1000 documents in one call.

        Args:
            org_id: The organization's id or slug.
            index_name: The index's URL-safe name.
            documents: `(id, content)` pairs, up to 1000 per call.
        """
        items = [
            BulkIngestItem(id=doc_id, content=BulkIngestItemContent.from_dict(content))
            for doc_id, content in documents
        ]
        body = BulkIngestRequest(documents=items)
        response = post_v_1_org_id_indexes_index_name_documents_bulk.sync_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=BulkIngestResponse, endpoint="documents.bulk_ingest")


class AsyncDocuments:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client

    async def list(
        self,
        org_id: str,
        index_name: str,
        *,
        page: int | Unset = UNSET,
        limit: int | Unset = UNSET,
    ) -> DocumentsList:
        """Async version of `Documents.list`."""
        response = await get_v_1_org_id_indexes_index_name_documents.asyncio_detailed(
            org_id, index_name, client=self._client, page=page, limit=limit
        )
        return unwrap(response, success_type=DocumentsList, endpoint="documents.list")

    async def get(self, org_id: str, index_name: str, document_id: str) -> Document:
        """Async version of `Documents.get`."""
        response = await get_v_1_org_id_indexes_index_name_documents_document_id.asyncio_detailed(
            org_id, index_name, document_id, client=self._client
        )
        return unwrap(response, success_type=Document, endpoint="documents.get")

    async def create(
        self, org_id: str, index_name: str, *, id: str, content: dict[str, Any]
    ) -> Document:
        """Async version of `Documents.create`."""
        body = CreateDocument(id=id, content=CreateDocumentContent.from_dict(content))
        response = await post_v_1_org_id_indexes_index_name_documents.asyncio_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=Document, endpoint="documents.create")

    async def update(
        self, org_id: str, index_name: str, document_id: str, *, content: dict[str, Any]
    ) -> Document:
        """Async version of `Documents.update`."""
        body = UpdateDocument(content=UpdateDocumentContent.from_dict(content))
        response = await put_v_1_org_id_indexes_index_name_documents_document_id.asyncio_detailed(
            org_id, index_name, document_id, client=self._client, body=body
        )
        return unwrap(response, success_type=Document, endpoint="documents.update")

    async def delete(self, org_id: str, index_name: str, document_id: str) -> MessageResponse:
        """Async version of `Documents.delete`."""
        response = (
            await delete_v_1_org_id_indexes_index_name_documents_document_id.asyncio_detailed(
                org_id, index_name, document_id, client=self._client
            )
        )
        return unwrap(response, success_type=MessageResponse, endpoint="documents.delete")

    async def bulk_ingest(
        self, org_id: str, index_name: str, *, documents: Sequence[tuple[str, dict[str, Any]]]
    ) -> BulkIngestResponse:
        """Async version of `Documents.bulk_ingest`."""
        items = [
            BulkIngestItem(id=doc_id, content=BulkIngestItemContent.from_dict(content))
            for doc_id, content in documents
        ]
        body = BulkIngestRequest(documents=items)
        response = await post_v_1_org_id_indexes_index_name_documents_bulk.asyncio_detailed(
            org_id, index_name, client=self._client, body=body
        )
        return unwrap(response, success_type=BulkIngestResponse, endpoint="documents.bulk_ingest")
