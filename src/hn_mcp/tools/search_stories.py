from __future__ import annotations

from typing import Literal

import httpx

import hn_mcp.app as app
from hn_mcp.types import ErrorResult, StoryItem, StorySearchResult

MAX_COUNT = 100


@app.mcp.tool()
async def search_stories(
    query: str,
    sort_by: Literal["relevance", "date"] = "relevance",
    count: int = 20,
    page: int = 0,
) -> StorySearchResult | ErrorResult:
    """Full-text search for HN stories.

    Args:
        query: Search terms.
        sort_by: "relevance" or "date".
        count: Results per page (default 20, max 100).
        page: Page number, 0-indexed.
    """
    count = min(count, MAX_COUNT)
    method = app.client.search_by_date if sort_by == "date" else app.client.search
    params = {"query": query, "tags": "story", "hitsPerPage": count, "page": page}

    try:
        data = await method(params)
    except httpx.HTTPStatusError as exc:  # pragma: no cover
        return ErrorResult(error=f"Search failed: HTTP {exc.response.status_code}")
    except httpx.TimeoutException:  # pragma: no cover
        return ErrorResult(error="Search request timed out")

    return StorySearchResult(
        total_hits=data.get("nbHits"),
        page=data.get("page"),
        total_pages=data.get("nbPages"),
        stories=[
            StoryItem(
                id=app._parse_id(hit.get("story_id") or hit.get("objectID")),
                title=hit.get("title"),
                url=hit.get("url"),
                author=hit.get("author"),
                points=hit.get("points"),
                num_comments=hit.get("num_comments"),
            )
            for hit in data.get("hits", [])
        ],
    )
