from __future__ import annotations

import httpx

import hn_mcp.app as app
from hn_mcp.types import ErrorResult, UserProfile


@app.mcp.tool()
async def get_user(username: str) -> UserProfile | ErrorResult:
    """Fetch a Hacker News user profile.

    Args:
        username: The HN username.
    """
    try:
        data = await app.client.get_user(username)
    except httpx.HTTPStatusError as exc:  # pragma: no cover
        return ErrorResult(
            error=f"Failed to fetch user '{username}': HTTP {exc.response.status_code}"
        )
    except httpx.TimeoutException:  # pragma: no cover
        return ErrorResult(error=f"Request timed out fetching user '{username}'")

    return UserProfile(
        username=data.get("username"),
        karma=data.get("karma"),
        about=data.get("about"),
        created_at=data.get("created_at"),
    )
