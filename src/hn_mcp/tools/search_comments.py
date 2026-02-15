from __future__ import annotations

from typing import Literal

import httpx

import hn_mcp.app as app
from hn_mcp.types import CommentHit, CommentSearchResult, ErrorResult

MAX_COUNT = 100


@app.mcp.tool()
async def search_comments(
    query: str,
    sort_by: Literal["relevance", "date"] = "relevance",
    story_id: int | None = None,
    author: str | None = None,
    count: int = 20,
    page: int = 0,
) -> CommentSearchResult | ErrorResult:
    """Full-text search for HN comments.

    Args:
        query: Search terms.
        sort_by: "relevance" or "date".
        story_id: Optional — only search comments on this story.
        author: Optional — only search comments by this author.
        count: Results per page (default 20, max 100).
        page: Page number, 0-indexed.
    """
    count = min(count, MAX_COUNT)
    method = app.client.search_by_date if sort_by == "date" else app.client.search
    tags_parts = ["comment"]
    if story_id is not None:
        tags_parts.append(f"story_{story_id}")
    if author is not None:
        tags_parts.append(f"author_{author}")

    params = {
        "query": query,
        "tags": ",".join(tags_parts),
        "hitsPerPage": count,
        "page": page,
    }

    try:
        data = await method(params)
    except httpx.HTTPStatusError as exc:  # pragma: no cover
        return ErrorResult(
            error=f"Comment search failed: HTTP {exc.response.status_code}"
        )
    except httpx.TimeoutException:  # pragma: no cover
        return ErrorResult(error="Comment search request timed out")

    return CommentSearchResult(
        total_hits=data.get("nbHits"),
        page=data.get("page"),
        total_pages=data.get("nbPages"),
        comments=[
            CommentHit(
                id=app._parse_id(hit.get("objectID")),
                story_id=hit.get("story_id"),
                story_title=hit.get("story_title"),
                parent_id=hit.get("parent_id"),
                author=hit.get("author"),
                text=hit.get("comment_text"),
            )
            for hit in data.get("hits", [])
        ],
    )
