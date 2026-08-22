# relevan

Python client for the [Relevan](https://relevan.dev) search API.

- Typed, generated from Relevan's live OpenAPI 3.1 spec (`GET /openapi`).
- Sync and async clients with the same method surface.
- Retries on rate limits, honoring the server's `Retry-After` header.
- Beta endpoints are grouped under `client.beta` and warn on every call.

## Install

```bash
pip install relevan
```

## Quickstart

```python
from relevan import Client
from relevan._generated.models.feedback_request_action_name import FeedbackRequestActionName

client = Client()  # reads RELEVAN_API_KEY from the environment

org = client.organizations.list()[0]
skill_doc = client.skill.get(org.id, "products")  # read once before querying an index

results = client.search.search(org.id, "products", query="wireless headphones")
for hit in results.results:
    print(hit.id, hit.explanation)

# Close the loop: tell Relevan what happened to a result.
client.beta.send_feedback(
    org.id,
    "products",
    action_name=FeedbackRequestActionName.CLICK,
    query_id=results.search_context.query_id,
    object_id=results.results[0].id,
    position=0,
)
```

The async client mirrors this exactly:

```python
from relevan import AsyncClient

async with AsyncClient() as client:
    org = (await client.organizations.list())[0]
    results = await client.search.search(org.id, "products", query="wireless headphones")
```

## Authentication

`Client()` and `AsyncClient()` read the API key from the `RELEVAN_API_KEY`
environment variable by default — the same variable used elsewhere for
this API — or accept it directly: `Client(api_key="relevan_...")`. The key
is never written to disk or logged, and is masked in `repr(client)`.

## Rate limits

Relevan enforces per-organization rate limits. On a `429`, the client
retries automatically using the server's `Retry-After` value
(`max_retries=2` by default, configurable via `Client(max_retries=...)`).
A `RelevanRateLimitError` is raised only if retries are exhausted.

After each `client.search.search(...)` call, `client.search.last_rate_limit`
holds the org's current `RateLimit-*` snapshot (`.limit`, `.remaining`,
`.reset_seconds`), so callers can self-throttle proactively if they want to.

## Beta endpoints

Endpoints under the API's `/v1-beta` path are exposed under `client.beta`
and documented as beta in their docstrings. **Their contract may change
without warning** — each call emits a `RelevanBetaWarning` so this is
visible at the call site, not just in documentation.

```python
import warnings

warnings.simplefilter("once", category=None)  # or filter RelevanBetaWarning specifically
```

## Regenerating the client

`src/relevan/_generated/` is generated from the live OpenAPI spec and is
never hand-edited:

```bash
uv run scripts/generate_client.py --url https://api.dev.relevan.dev/openapi
```

See that script's docstring for the spec normalization it applies and why.

## Development

```bash
uv sync --extra dev
uv run ruff check .
uv run mypy src
uv run pytest
```

## License

Apache-2.0
