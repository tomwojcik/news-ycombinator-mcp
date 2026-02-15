# hn-mcp

MCP server for browsing **full** Hacker News comment trees. No artificial depth limits, no truncation.

Built for AI agents that need to read and summarize entire HN discussions. Uses the [Algolia HN API](https://hn.algolia.com/api) under the hood.

## Why

This server fetches the complete tree from Algolia and lets you control depth client-side — from "just top-level with reply counts" to "give me everything".

### Typical agent workflow

```
1. get_thread(42123456, depth=1)       → story + 85 top-level comments with reply_counts
2. Agent picks Comment A (47 replies)
3. get_comment_tree(comment_a_id)      → full 47-reply subtree
4. Agent summarizes branch, picks next
```

Or for smaller threads, just `get_thread(id, depth=-1)` to get the entire tree at once.

## Install in Claude Code

```bash
claude mcp add hn -- uvx hn-mcp
```

That's it. Add `--scope user` to make it available in all projects.

### From source

If you want to run from a local clone instead:

```bash
claude mcp add hn -- uv run --directory /absolute/path/to/news-ycombinator-mcp hn-mcp
```

Or manually add to your project's `.claude/settings.json`:

```json
{
  "mcpServers": {
    "hn": {
      "type": "stdio",
      "command": "uvx",
      "args": ["hn-mcp"]
    }
  }
}
```

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
