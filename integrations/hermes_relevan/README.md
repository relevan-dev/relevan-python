# Relevan memory provider for Hermes Agent

This plugin makes a [Relevan](https://relevan.dev) search index the memory of
[Hermes Agent](https://github.com/NousResearch/hermes-agent). Before each turn,
Hermes searches your index and puts the top results in front of the model.
After the reply, the plugin checks which results the reply used and reports
them to Relevan. Relevan uses those reports to rank your index better.

It fits best when you already have a body of text to search: your notes, your
scanned documents, or a product catalog. Two presets set up an index for each
of these in one command.

## How it works

| Hermes hook | What the plugin does |
| --- | --- |
| `prefetch` | Searches the index with the user's message. Puts up to 5 results, with their ids, in a `<relevan-recall>` block. Skipped for greetings and slash commands. |
| `sync_turn` | Finds the recalled results that the reply used, and sends one `llm_judgment` feedback event for each, keyed to the search's `queryId`. |
| `relevan_search` tool | Lets the model run its own search. Its results get the same feedback check after the turn. |
| `relevan_feedback` tool | Lets the model mark a result helpful (grade 2) or unhelpful (grade 0), for example after the user confirms or corrects an answer. |

A result counts as used when the reply cites its id or names its title (grade
2), or when the reply repeats at least three of the result's distinctive words
(grade 1). A distinctive word is one that is not in the user's message and not
shared by most other results. A result marked through `relevan_feedback` gets
no second, automatic event.

Subagents and cron runs send no automatic feedback.

## Install

```bash
hermes plugins install relevan
hermes memory setup        # pick relevan, paste an API key, name the index
```

Create an API key in the [Relevan console](https://console.relevan.dev). A
read key can search and send feedback. Loading a preset needs a write key.

## Presets

```bash
# Personal notes: an Obsidian vault
hermes relevan load-preset personal-notes --obsidian ~/Documents/Vault

# Personal notes: a Paperless-ngx export (from `document_exporter`)
hermes relevan load-preset personal-notes --paperless ~/paperless-export

# Product catalog: JSON, JSON Lines or CSV
hermes relevan load-preset product-catalog --file products.csv --index hermes-catalog
```

Add `--dry-run` to see the documents without sending anything. Each command
creates the index if it does not exist, deploys the preset's mapping, and
uploads the documents in batches of 500. Run it again to update the documents.
`examples/` holds a small vault, a Paperless export and a catalog to try.

| Preset | Fields |
| --- | --- |
| `personal-notes` | `title`, `body`, `tags`, `source` (obsidian or paperless), `path`, `correspondent`, `document_type`, `created`, `modified` |
| `product-catalog` | `title`, `description`, `brand`, `category`, `tags`, `sku`, `price`, `in_stock`, `url`. Rows need an `id` or a `sku`. Other columns are dropped. |

## Configuration

`hermes memory setup` writes `$HERMES_HOME/relevan.json`. You can also edit
it:

| Key | Default | Meaning |
| --- | --- | --- |
| `index` | `hermes-notes` | The index to search |
| `org_id` | your first organization | The Relevan organization |
| `base_url` | `https://api.relevan.dev` | The API URL |
| `recall_size` | `5` | Results recalled before each turn |
| `auto_feedback` | `true` | Send feedback for results the reply used |
| `source` | `production` | Set `eval` to keep test traffic apart from real traffic |

The API key is read from `RELEVAN_API_KEY` through Hermes's secret scope.

## What leaves your machine

- Each user message that is not a greeting or a slash command is sent to the
  Relevan API as a search query, with the Hermes session id as `sessionId`.
- For each recalled result the reply used: the result id, its position, the
  search's `queryId`, a grade, and a fixed reason such as "Hermes reply cited
  the result id". The reply text itself is never sent.
- The `relevan_feedback` tool sends the reason the model gives, if any.
- `load-preset` uploads the text and metadata of your notes, documents or
  products to your Relevan index.
- Every request carries the header `X-Relevan-Integration: hermes/0.1.0`, so
  Relevan can count traffic from this plugin.

The plugin starts no background process, writes only `$HERMES_HOME/relevan.json`,
and has no self-updater. Feedback uses Relevan's beta feedback endpoint, whose
contract may change.

## Development

```bash
cd integrations/hermes_relevan
uv run --no-project --with ../.. --with pytest --with respx pytest
hermes plugins validate . --install-deps
```

The tests run against the client in this checkout (`--with ../..`), and
stub the three Hermes modules the plugin imports, so they run without Hermes
installed. The plugin needs relevan 0.2.0 or later, the first release with
the `integration=` option.

## License

Apache-2.0
