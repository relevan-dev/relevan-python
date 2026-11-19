# Changelog

All notable changes to this project are documented in this file.

## 0.2.0 - 2026-11-19

- Each request sends `X-Relevan-Integration: python/<version>`, so Relevan can
  count the search and feedback traffic of this client. Pass
  `Client(integration="<name>/<version>")` or the same argument to
  `AsyncClient` to send the name of the library built on it instead.
- Every 4xx or 5xx response raises a typed error (`RelevanAuthError`,
  `RelevanRateLimitError`, or `RelevanAPIError`), also when the body has no
  `message`, is not JSON, or has a status the spec does not document. Before,
  such a body raised `KeyError('message')`, a JSON decode error, or
  `UnexpectedStatus`. Without a `message`, the error message is
  `"<METHOD> <path> failed (<status>)"`.
- `integrations/hermes_relevan` is a memory provider for Hermes Agent. It
  searches a Relevan index before each turn, and sends an `llm_judgment`
  event for each recalled result the reply used. It has `personal-notes`
  (Obsidian, Paperless-ngx) and `product-catalog` presets. It is a Hermes
  plugin with its own `pyproject.toml`, not part of the `relevan` package,
  and it needs relevan 0.2.0 or later.

## 0.1.0 - 2026-11-18

First release on PyPI.

- Sync and async clients for organizations, indexes, documents, mappings,
  search, skill docs, and usage, generated from the API's OpenAPI 3.1 spec.
- `client.search.filter_values` lists the values of an index's filterable
  fields. Search accepts `gte`/`lte` range filters, `partition`, and `routing`.
- `client.indexes.get` returns document counts and `ready_to_search`.
  `client.indexes.create` returns the console and skill URLs of the new index.
- Beta feedback under `client.beta.send_feedback`: `click`, `conversion`,
  `llm_judgment`, and `search_judgment`, with `grade`, per-result
  `results`, `description`, and `source`. `action_name` accepts a plain
  string.
- Automatic retry on `429` responses, honoring `Retry-After`.
