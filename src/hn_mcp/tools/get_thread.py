from __future__ import annotations

import httpx

import hn_mcp.app as app
from hn_mcp.types import Comment, ErrorResult, Thread


@app.mcp.tool()
async def get_thread(story_id: int, depth: int = 1) -> Thread | ErrorResult:
    """Fetch a story and its comment tree from Hacker News.

    Args:
        story_id: The HN story ID.
        depth: How many levels of comment nesting to include.
            0 = story metadata only, no comments.
            1 = top-level comments only (each includes reply_count).
            2 = top-level + their direct replies.
            N = N levels deep.
            -1 = entire tree, no limits.
    """
    try:
        data = await app.client.get_item(story_id)
    except httpx.HTTPStatusError as exc:  # pragma: no cover
        return ErrorResult(
            error=f"Failed to fetch story {story_id}: HTTP {exc.response.status_code}"
        )
    except httpx.TimeoutException:  # pragma: no cover
        return ErrorResult(error=f"Request timed out fetching story {story_id}")

    comments: list[Comment] = []
    if depth != 0:
        comment_depth = depth if depth < 0 else depth - 1
        for child in data.get("children", []):
            pruned = app._prune_comment(child, comment_depth)
            if pruned is not None:
                comments.append(pruned)

    return Thread(
        id=data.get("id"),
        title=data.get("title"),
        url=data.get("url"),
        author=data.get("author"),
        points=data.get("points"),
        num_comments=app._count_descendants(data.get("children", [])),
        comments=comments,
    )
