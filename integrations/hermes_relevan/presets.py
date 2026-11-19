"""Ready-made index presets: a mapping plus loaders that turn local data into documents.

`personal-notes` takes an Obsidian vault or a Paperless-ngx export.
`product-catalog` takes a JSON, JSON Lines or CSV file of products.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MAX_BODY_CHARS = 20_000
BULK_BATCH = 500

Document = tuple[str, dict[str, Any]]


@dataclass(frozen=True)
class Preset:
    name: str
    description: str
    mapping: dict[str, Any]


PERSONAL_NOTES = Preset(
    name="personal-notes",
    description="Notes and documents from an Obsidian vault or a Paperless-ngx export.",
    mapping={
        "title": {"use": ["searchable", "autocompletable", "highlightable"], "kind": "text"},
        "body": {"use": ["searchable", "highlightable"], "kind": "text"},
        "tags": {"use": ["filterable"], "kind": "array"},
        "source": {"use": ["filterable"], "kind": "id"},
        "path": {"use": ["filterable"], "kind": "id"},
        "correspondent": {"use": ["searchable", "filterable"], "kind": "text", "language": "none"},
        "document_type": {"use": ["filterable"], "kind": "id"},
        "created": {"use": ["filterable", "sortable"], "kind": "date"},
        "modified": {"use": ["filterable", "sortable"], "kind": "date"},
    },
)

PRODUCT_CATALOG = Preset(
    name="product-catalog",
    description="A product catalog: title, description, brand, category, price and stock.",
    mapping={
        "title": {"use": ["searchable", "autocompletable", "highlightable"], "kind": "text"},
        "description": {"use": ["searchable", "highlightable"], "kind": "text"},
        "brand": {"use": ["searchable", "filterable"], "kind": "text", "language": "none"},
        "category": {"use": ["searchable", "filterable"], "kind": "text"},
        "tags": {"use": ["filterable"], "kind": "array"},
        "sku": {"use": ["searchable", "filterable"], "kind": "id", "language": "none"},
        "price": {"use": ["filterable", "sortable"], "kind": "number"},
        "in_stock": {"use": ["filterable"], "kind": "boolean"},
        "url": {"use": ["filterable"], "kind": "id"},
    },
)

PRESETS = {preset.name: preset for preset in (PERSONAL_NOTES, PRODUCT_CATALOG)}

_ID_UNSAFE = re.compile(r"[^A-Za-z0-9_.:-]+")


def document_id(prefix: str, key: str) -> str:
    """A Relevan-safe document id: readable, unique, at most 512 characters."""
    slug = _ID_UNSAFE.sub("-", key).strip("-")[:80]
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}:{slug}-{digest}" if slug else f"{prefix}:{digest}"


def _iso(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def _date(value: Any) -> str | None:
    if not value:
        return None
    text = str(value).strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).isoformat()
    except ValueError:
        return None


def _split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Read the YAML front matter of a note: scalars, inline lists and dash lists."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta: dict[str, Any] = {}
    key = None
    for line in text[3:end].splitlines():
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and key:
            current = meta.get(key)
            items = current if isinstance(current, list) else []
            items.append(line.lstrip()[2:].strip().strip("\"'"))
            meta[key] = items
            continue
        name, sep, value = line.partition(":")
        if not sep:
            continue
        key = name.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key] = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        else:
            meta[key] = value.strip("\"'")
    return meta, text[end + 4 :].lstrip("\n")


_INLINE_TAG = re.compile(r"(?<![\w#&])#([A-Za-z][\w/-]*)")


def load_obsidian_vault(vault: Path) -> Iterator[Document]:
    """One document per Markdown note. Skips the .obsidian and .trash folders."""
    for note in sorted(vault.rglob("*.md")):
        relative = note.relative_to(vault)
        if relative.parts[0] in {".obsidian", ".trash"}:
            continue
        meta, body = _split_front_matter(note.read_text(encoding="utf-8", errors="replace"))
        raw_tags = meta.get("tags") or []
        tags = [raw_tags] if isinstance(raw_tags, str) else list(raw_tags)
        tags += _INLINE_TAG.findall(body)
        stat = note.stat()
        content: dict[str, Any] = {
            "title": str(meta.get("title") or note.stem),
            "body": body[:MAX_BODY_CHARS],
            "tags": sorted({t.lstrip("#") for t in tags if t}),
            "source": "obsidian",
            "path": relative.as_posix(),
            "modified": _iso(stat.st_mtime),
        }
        created = _date(meta.get("created") or meta.get("date"))
        if created:
            content["created"] = created
        yield document_id("obsidian", relative.as_posix()), content


def _paperless_records(export: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for manifest in sorted(export.rglob("*manifest.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        records.extend(data if isinstance(data, list) else [data])
    if not records:
        raise FileNotFoundError(f"No manifest.json in {export}. Run document_exporter first.")
    return records


def load_paperless_export(export: Path) -> Iterator[Document]:
    """One document per Paperless-ngx document, from a `document_exporter` folder.

    Uses the OCR text that Paperless stores as `content`, and resolves the
    correspondent, document type and tags to their names.
    """
    records = _paperless_records(export)
    names: dict[tuple[str, Any], str] = {}
    for record in records:
        model = record.get("model", "")
        if model in {"documents.correspondent", "documents.tag", "documents.documenttype"}:
            names[(model, record.get("pk"))] = str(record.get("fields", {}).get("name", ""))
    for record in records:
        if record.get("model") != "documents.document":
            continue
        fields = record.get("fields", {})
        pk = record.get("pk")
        content: dict[str, Any] = {
            "title": str(fields.get("title") or f"Document {pk}"),
            "body": str(fields.get("content") or "")[:MAX_BODY_CHARS],
            "tags": sorted(
                n for t in fields.get("tags") or [] if (n := names.get(("documents.tag", t)))
            ),
            "source": "paperless",
        }
        if correspondent := names.get(("documents.correspondent", fields.get("correspondent"))):
            content["correspondent"] = correspondent
        if document_type := names.get(("documents.documenttype", fields.get("document_type"))):
            content["document_type"] = document_type
        if created := _date(fields.get("created")):
            content["created"] = created
        if modified := _date(fields.get("modified") or fields.get("added")):
            content["modified"] = modified
        if exported := record.get("__exported_file_name__"):
            content["path"] = str(exported)
        yield document_id("paperless", str(pk)), content


def _product(row: dict[str, Any]) -> dict[str, Any]:
    content: dict[str, Any] = {}
    for field in ("title", "description", "brand", "category", "sku", "url"):
        if row.get(field) not in (None, ""):
            content[field] = str(row[field])
    if row.get("price") not in (None, ""):
        content["price"] = float(row["price"])
    if row.get("in_stock") not in (None, ""):
        value = row["in_stock"]
        content["in_stock"] = (
            value
            if isinstance(value, bool)
            else str(value).lower()
            in {
                "1",
                "true",
                "yes",
                "y",
            }
        )
    tags = row.get("tags")
    if isinstance(tags, str):
        tags = [t.strip() for t in re.split(r"[,;|]", tags) if t.strip()]
    if tags:
        content["tags"] = list(tags)
    return content


def load_product_file(path: Path) -> Iterator[Document]:
    """Products from a JSON array, JSON Lines or CSV file. Each row needs `id` or `sku`.

    Columns outside the preset mapping are dropped, because Relevan rejects a
    field the mapping does not declare.
    """
    rows: list[dict[str, Any]]
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))
    elif path.suffix.lower() in {".jsonl", ".ndjson"}:
        lines = path.read_text(encoding="utf-8").splitlines()
        rows = [json.loads(line) for line in lines if line.strip()]
    else:
        rows = json.loads(path.read_text(encoding="utf-8"))
    for row in rows:
        key = str(row.get("id") or row.get("sku") or "")
        if not key:
            raise ValueError(f"A product row has no id or sku: {row}")
        yield document_id("product", key), _product(row)


def ingest(
    client: Any,
    org_id: str,
    index: str,
    preset: Preset,
    documents: list[Document],
    ready_timeout: float = 120.0,
) -> int:
    """Create the index if needed, deploy the preset mapping, and bulk-ingest the documents."""
    from relevan import RelevanAPIError

    try:
        client.indexes.get(org_id, index)
    except RelevanAPIError as exc:
        if exc.status_code != 404:
            raise
        client.indexes.create(org_id, name=index, description=f"Hermes {preset.name} preset")
    deadline = time.monotonic() + ready_timeout
    while (status := str(client.indexes.get(org_id, index).status.value)) != "ready":
        if status == "failed" or time.monotonic() > deadline:
            raise RuntimeError(f"Index {index} is {status}, not ready")
        time.sleep(2)
    client.mappings.create(org_id, index, fields=preset.mapping)
    for start in range(0, len(documents), BULK_BATCH):
        client.documents.bulk_ingest(org_id, index, documents=documents[start : start + BULK_BATCH])
    return len(documents)
