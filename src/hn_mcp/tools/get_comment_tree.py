from __future__ import annotations

import httpx

import hn_mcp.app as app
from hn_mcp.types import Comment, ErrorResult


@app.mcp.tool()
async def get_comment_tree(comment_id: int, depth: int = -1) -> Comment | ErrorResult:
    """Fetch a specific comment and its reply subtree.

    Use this to dive into a branch after scanning top-level comments
    with get_thread(depth=1).

    Args:
        comment_id: The HN comment ID.
        depth: How many levels of replies to include below this comment.
            0 = this comment only (with reply_count).
            N = N levels of replies.
            -1 = full subtree (default).
    """
    try:
        data = await app.client.get_item(comment_id)
    except httpx.HTTPStatusError as exc:  # pragma: no cover
        return ErrorResult(
            error=f"Failed to fetch comment {comment_id}: HTTP {exc.response.status_code}"
        )
    except httpx.TimeoutException:  # pragma: no cover
        return ErrorResult(error=f"Request timed out fetching comment {comment_id}")

    result = app._prune_comment(data, depth)
    if result is None:  # pragma: no cover — Algolia omits deleted items
        return ErrorResult(error="Comment not found or deleted")
    return result
