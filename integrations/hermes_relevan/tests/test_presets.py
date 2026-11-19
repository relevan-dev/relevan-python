import re
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from hermes_relevan.presets import (
    PERSONAL_NOTES,
    PRODUCT_CATALOG,
    document_id,
    ingest,
    load_obsidian_vault,
    load_paperless_export,
    load_product_file,
)

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
VALID_ID = re.compile(r"^[A-Za-z0-9_.:-]{1,512}$")


def test_document_ids_are_valid_and_unique() -> None:
    a = document_id("obsidian", "Home lab/Proxmox backup plan.md")
    b = document_id("obsidian", "Home lab/Proxmox backup plan (copy).md")
    assert VALID_ID.match(a)
    assert VALID_ID.match(b)
    assert a != b
    assert VALID_ID.match(document_id("x", "日本語のメモ.md"))


def test_obsidian_vault_reads_front_matter_and_inline_tags() -> None:
    docs = dict(load_obsidian_vault(EXAMPLES / "obsidian-vault"))
    assert len(docs) == 12
    by_title = {content["title"]: content for content in docs.values()}
    proxmox = by_title["Proxmox backup plan"]
    assert proxmox["tags"] == ["backups", "homelab", "proxmox"]
    assert proxmox["created"].startswith("2026-03-02")
    assert proxmox["path"] == "Home lab/Proxmox backup plan.md"
    assert not proxmox["body"].startswith("---")
    assert by_title["Reading list"]["tags"] == ["books"]
    assert all(VALID_ID.match(doc_id) for doc_id in docs)


def test_paperless_export_resolves_names() -> None:
    docs = dict(load_paperless_export(EXAMPLES / "paperless-export"))
    assert len(docs) == 6
    policy = docs[document_id("paperless", "11")]
    assert policy["correspondent"] == "Allianz"
    assert policy["document_type"] == "Policy"
    assert policy["tags"] == ["house", "insurance"]
    assert "HX-4471-209" in policy["body"]
    assert "correspondent" not in docs[document_id("paperless", "16")]


def test_paperless_export_without_manifest_fails(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        list(load_paperless_export(tmp_path))


def test_products_load_from_json_and_csv(tmp_path: Path) -> None:
    docs = dict(load_product_file(EXAMPLES / "products.json"))
    assert len(docs) == 24
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "sku,title,price,in_stock,tags,colour\nA-1,Tent,99.5,yes,camp;summer,green\n",
        encoding="utf-8",
    )
    ((doc_id, content),) = list(load_product_file(csv_file))
    assert content == {
        "title": "Tent",
        "sku": "A-1",
        "price": 99.5,
        "in_stock": True,
        "tags": ["camp", "summer"],
    }
    assert doc_id == document_id("product", "A-1")


@pytest.mark.parametrize(
    ("preset", "docs"),
    [
        (PERSONAL_NOTES, lambda: load_obsidian_vault(EXAMPLES / "obsidian-vault")),
        (PERSONAL_NOTES, lambda: load_paperless_export(EXAMPLES / "paperless-export")),
        (PRODUCT_CATALOG, lambda: load_product_file(EXAMPLES / "products.json")),
    ],
)
def test_every_loaded_field_is_in_the_mapping(preset: Any, docs: Any) -> None:
    fields = {name for _, content in docs() for name in content}
    assert fields <= set(preset.mapping)


class FakeClient:
    def __init__(self, exists: bool) -> None:
        self.calls: list[tuple[str, Any]] = []
        self._exists = exists
        self.indexes = SimpleNamespace(get=self._get, create=self._create)
        self.mappings = SimpleNamespace(create=self._mapping)
        self.documents = SimpleNamespace(bulk_ingest=self._bulk)

    def _get(self, org_id: str, index: str) -> Any:
        from relevan import RelevanAPIError

        if not self._exists:
            raise RelevanAPIError("not found", status_code=404)
        return SimpleNamespace(status=SimpleNamespace(value="ready"))

    def _create(self, org_id: str, *, name: str, description: str) -> None:
        self.calls.append(("create", name))
        self._exists = True

    def _mapping(self, org_id: str, index: str, *, fields: dict[str, Any]) -> None:
        self.calls.append(("mapping", sorted(fields)))

    def _bulk(self, org_id: str, index: str, *, documents: list[Any]) -> None:
        self.calls.append(("bulk", len(documents)))


def test_ingest_creates_maps_and_batches() -> None:
    client = FakeClient(exists=False)
    docs = [(f"p:{i}", {"title": str(i)}) for i in range(1200)]
    assert ingest(client, "org", "hermes-catalog", PRODUCT_CATALOG, docs) == 1200
    assert client.calls == [
        ("create", "hermes-catalog"),
        ("mapping", sorted(PRODUCT_CATALOG.mapping)),
        ("bulk", 500),
        ("bulk", 500),
        ("bulk", 200),
    ]
