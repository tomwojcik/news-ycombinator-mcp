from __future__ import annotations

from typing import Literal

import httpx

import hn_mcp.app as app
from hn_mcp.types import ErrorResult, StoryItem

MAX_COUNT = 100


@app.mcp.tool()
async def get_stories(
    category: Literal["top", "new", "ask_hn", "show_hn"],
    count: int = 20,
) -> list[StoryItem] | ErrorResult:
    """Browse HN stories by category. Returns metadata only (no comments).

    Args:
        category: One of: top, new, ask_hn, show_hn.
        count: Number of stories to return (default 20, max 100).
    """
    count = min(count, MAX_COUNT)
    params_map = {
        "top": (app.client.search, {"tags": "front_page"}),
        "new": (app.client.search_by_date, {"tags": "story"}),
        "ask_hn": (app.client.search, {"tags": "ask_hn"}),
        "show_hn": (app.client.search, {"tags": "show_hn"}),
    }

    if category not in params_map:
        return ErrorResult(
            error=f"Invalid category '{category}'. Must be one of: top, new, ask_hn, show_hn"
        )

    method, tags = params_map[category]

    try:
        data = await method({**tags, "hitsPerPage": count})
    except httpx.HTTPStatusError as exc:  # pragma: no cover
        return ErrorResult(
            error=f"Failed to fetch {category} stories: HTTP {exc.response.status_code}"
        )
    except httpx.TimeoutException:  # pragma: no cover
        return ErrorResult(error=f"Request timed out fetching {category} stories")

    return [
        StoryItem(
            id=app._parse_id(hit.get("story_id") or hit.get("objectID")),
            title=hit.get("title"),
            url=hit.get("url"),
            author=hit.get("author"),
            points=hit.get("points"),
            num_comments=hit.get("num_comments"),
        )
        for hit in data.get("hits", [])
    ]
