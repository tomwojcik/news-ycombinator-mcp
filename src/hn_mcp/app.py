"""FastMCP instance, API client, and shared helpers."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP

from hn_mcp.client import HNClient
from hn_mcp.types import Comment

client = HNClient()


@asynccontextmanager
async def _lifespan(_server: FastMCP) -> AsyncIterator[None]:  # pragma: no cover
    try:
        yield
    finally:
        await client.aclose()


mcp = FastMCP(
    "hn",
    lifespan=_lifespan,
    instructions=(
        "Hacker News MCP server. Use get_thread with depth=1 to scan top-level "
        "comments, then get_comment_tree to dive into interesting branches."
    ),
)


def _prune_comment(node: dict, depth: int) -> Comment | None:
    """Return a pruned comment dict. *depth* is how many levels of replies to include below this node."""
    if node.get("author") is None:
        return None

    children = node.get("children", [])
    comment: Comment = {
        "id": node.get("id"),
        "author": node["author"],
        "text": node.get("text") or "",
        "reply_count": _count_descendants(children),
    }

    if depth != 0 and children:
        next_depth = depth if depth < 0 else depth - 1
        replies: list[Comment] = []
        for child in children:
            pruned = _prune_comment(child, next_depth)
            if pruned is not None:
                replies.append(pruned)
        comment["replies"] = replies

    return comment


def _count_descendants(children: list[dict]) -> int:
    """Count all non-deleted descendant comments."""
    total = 0
    stack = list(children)
    while stack:
        child = stack.pop()
        if child.get("author") is not None:
            total += 1
            stack.extend(child.get("children", []))
    return total


def _parse_id(value: int | str | None) -> int | None:
    """Normalize an Algolia ID (string or int) to int."""
    return int(value) if value is not None else None
