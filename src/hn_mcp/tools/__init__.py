"""Import all tool modules so their @mcp.tool() decorators run at import time."""

from . import (
    get_comment_tree,
    get_stories,
    get_thread,
    get_user,
    search_comments,
    search_stories,
)

__all__ = [
    "get_comment_tree",
    "get_stories",
    "get_thread",
    "get_user",
    "search_comments",
    "search_stories",
]
