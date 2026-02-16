# hn-mcp

[![PyPI](https://img.shields.io/pypi/v/hn-mcp)](https://pypi.org/project/hn-mcp/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![codecov](https://codecov.io/gh/tomwojcik/news-ycombinator-mcp/graph/badge.svg)](https://codecov.io/gh/tomwojcik/news-ycombinator-mcp)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

HN threads have 500+ comments nested 10 levels deep. Your AI agent needs to read them without blowing its context window.

**hn-mcp** is an MCP server that gives AI agents full access to Hacker News — complete comment trees, search, and user profiles — with depth control so they can explore progressively instead of fetching everything at once.

### Features

- **Full comment trees** — no depth limits, no truncation
- **Depth control** — fetch just top-level comments or the entire tree
- **Smart pruning** — `reply_count` at cut-off points so agents decide what to expand
- **Search** — full-text search across stories and comments with filters
- **No API keys** — uses the public Algolia HN API
- **100% test coverage** — tested with VCR cassettes, no network calls needed

### Typical agent workflow

```
1. get_thread(42123456, depth=1)       → story + 85 top-level comments with reply_counts
2. Agent picks Comment A (47 replies)
3. get_comment_tree(comment_a_id)      → full 47-reply subtree
4. Agent summarizes branch, picks next
```

Or for smaller threads, just `get_thread(id, depth=-1)` to get the entire tree at once.

## Getting started

**Standard config** works in most tools:

```json
{
  "mcpServers": {
    "hn": {
      "command": "uvx",
      "args": ["hn-mcp"]
    }
  }
}
```

<details>
<summary>Claude Code</summary>

```bash
claude mcp add hn -- uvx hn-mcp
```

Add `--scope user` to make it available in all projects.

</details>

<details>
<summary>Claude Desktop</summary>

Follow the MCP install [guide](https://modelcontextprotocol.io/quickstart/user), use the standard config above.

</details>

<details>
<summary>Cursor</summary>

Add to your Cursor MCP config (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "hn": {
      "command": "uvx",
      "args": ["hn-mcp"]
    }
  }
}
```

</details>

<details>
<summary>Windsurf</summary>

Follow the Windsurf MCP [documentation](https://docs.windsurf.com/windsurf/mcp), use the standard config above.

</details>

<details>
<summary>VS Code / Copilot</summary>

Add to your VS Code MCP config (`.vscode/mcp.json`):

```json
{
  "mcpServers": {
    "hn": {
      "command": "uvx",
      "args": ["hn-mcp"]
    }
  }
}
```

</details>

<details>
<summary>From source</summary>

If you want to run from a local clone instead:

```bash
claude mcp add hn -- uv run --directory /absolute/path/to/news-ycombinator-mcp hn-mcp
```

</details>

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (provides `uvx`)

## Tools

| Tool | Description | Key Inputs | Returns |
|---|---|---|---|
| `get_thread` | Fetch a story and its comment tree | `story_id`, `depth` (0=story only, 1=top-level, N=N levels, -1=full tree) | Story metadata + pruned comment tree |
| `get_comment_tree` | Dive into a specific comment's reply subtree | `comment_id`, `depth` (default: -1, full subtree) | Comment + nested replies |
| `get_stories` | Browse HN by category | `category` (top, new, ask_hn, show_hn), `count` | List of story summaries |
| `search_stories` | Full-text search for stories | `query`, `sort_by` (relevance/date), `count`, `page` | Paginated story results |
| `search_comments` | Full-text search for comments | `query`, `sort_by`, `story_id`, `author`, `count`, `page` | Paginated comment results |
| `get_user` | Fetch a user profile | `username` | Username, karma, about, created date |

### Depth parameter

The `depth` parameter on `get_thread` and `get_comment_tree` controls how much of the tree you get:

```
depth=0   (no comments — story metadata only)
depth=1   Comment A (reply_count=3)       ← just the comment + count
depth=2   Comment A                        ← comment + direct replies
            ├── Reply A1 (reply_count=2)
            ├── Reply A2 (reply_count=0)
            └── Reply A3 (reply_count=1)
depth=-1  Full tree, no pruning
```

## Development

```bash
git clone https://github.com/tomwojcik/news-ycombinator-mcp
cd news-ycombinator-mcp
make venv
make install
```

### Run tests

```bash
make test
```

Tests use [vcrpy](https://github.com/kevin1024/vcrpy) cassettes — no network calls needed. Coverage is reported automatically.

### Re-record cassettes

If the Algolia API response format changes:

```bash
# In tests/conftest.py, temporarily change record_mode to "new_episodes"
uv run pytest
# Then change it back to "none"
```

### Project structure

```
src/hn_mcp/
├── app.py               # FastMCP instance + tree pruning helpers
├── client.py            # HNClient — async Algolia API client
├── server.py            # Entrypoint
├── types.py             # TypedDict definitions for all responses
└── tools/
    ├── get_thread.py
    ├── get_comment_tree.py
    ├── get_stories.py
    ├── search_stories.py
    ├── search_comments.py
    └── get_user.py
```

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Contributions welcome. Please open an issue first to discuss what you'd like to change.

When submitting a PR:

1. Add tests for new functionality
2. Record VCR cassettes for any new API calls
3. Ensure `uv run pytest` passes with 100% coverage
