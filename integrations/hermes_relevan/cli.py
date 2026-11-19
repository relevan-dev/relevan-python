"""`hermes relevan ...` commands: load a preset into the configured index, show status."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from agent.secret_scope import get_secret
from hermes_constants import get_hermes_home

from .client import DEFAULT_BASE_URL, make_client
from .presets import (
    PRESETS,
    ingest,
    load_obsidian_vault,
    load_paperless_export,
    load_product_file,
)
from .provider import API_KEY_ENV, CONFIG_FILE, _read_config


def _config() -> dict[str, Any]:
    return _read_config(Path(get_hermes_home()) / CONFIG_FILE)


def _client_and_org(config: dict[str, Any]) -> tuple[Any, str]:
    key = get_secret(API_KEY_ENV)
    if not key:
        raise SystemExit(f"{API_KEY_ENV} is not set. Run: hermes memory setup")
    client = make_client(key, base_url=str(config.get("base_url") or DEFAULT_BASE_URL))
    org_id = str(config.get("org_id") or "") or client.organizations.list()[0].id
    return client, org_id


def _load(args: argparse.Namespace) -> None:
    config = _config()
    index = args.index or config.get("index")
    if not index:
        raise SystemExit("No index. Pass --index or run: hermes memory setup")
    if args.preset == "personal-notes":
        if bool(args.obsidian) == bool(args.paperless):
            raise SystemExit("personal-notes needs one of --obsidian or --paperless")
        if args.obsidian:
            documents = list(load_obsidian_vault(Path(args.obsidian).expanduser()))
        else:
            documents = list(load_paperless_export(Path(args.paperless).expanduser()))
    else:
        if not args.file:
            raise SystemExit("product-catalog needs --file (JSON, JSON Lines or CSV)")
        documents = list(load_product_file(Path(args.file).expanduser()))
    if args.dry_run:
        print(json.dumps(documents[:3], indent=2, ensure_ascii=False))
        print(f"{len(documents)} documents ready for {index} (dry run, nothing sent)")
        return
    client, org_id = _client_and_org(config)
    count = ingest(client, org_id, index, PRESETS[args.preset], documents)
    print(f"Loaded {count} documents into {index} with the {args.preset} preset")


def _status(args: argparse.Namespace) -> None:
    config = _config()
    client, org_id = _client_and_org(config)
    index = config.get("index")
    detail = client.indexes.get(org_id, index).to_dict() if index else None
    print(json.dumps({"org_id": org_id, "index": index, "detail": detail}, indent=2))


def relevan_command(args: argparse.Namespace) -> None:
    handler = getattr(args, "relevan_handler", None)
    if handler is None:
        print("Usage: hermes relevan <load-preset|status>")
        return
    handler(args)


def register_cli(subparser: argparse.ArgumentParser) -> None:
    subs = subparser.add_subparsers(dest="relevan_command")
    load = subs.add_parser("load-preset", help="Create the index and load local data into it")
    load.add_argument("preset", choices=sorted(PRESETS))
    load.add_argument("--obsidian", help="Path to an Obsidian vault (personal-notes)")
    load.add_argument("--paperless", help="Path to a Paperless-ngx export (personal-notes)")
    load.add_argument("--file", help="Products as JSON, JSON Lines or CSV (product-catalog)")
    load.add_argument("--index", help="Index name. Defaults to the configured index")
    load.add_argument("--dry-run", action="store_true", help="Show documents, send nothing")
    load.set_defaults(relevan_handler=_load)
    status = subs.add_parser("status", help="Show the configured org and index")
    status.set_defaults(relevan_handler=_status)
    subparser.set_defaults(func=relevan_command)
