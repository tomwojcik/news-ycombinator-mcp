from unittest.mock import AsyncMock, patch

from hn_mcp.tools.get_thread import get_thread
from tests.conftest import (
    COMMENT_AUTHOR,
    COMMENT_ID,
    STORY_AUTHOR,
    STORY_ID,
    STORY_TITLE,
    my_vcr,
)


async def test_depth_0():
    with my_vcr.use_cassette("tools/get_thread_depth0.yaml"):
        result = await get_thread(STORY_ID, depth=0)
    assert result["id"] == STORY_ID
    assert result["title"] == STORY_TITLE
    assert result["author"] == STORY_AUTHOR
    assert result["num_comments"] > 0
    assert len(result["comments"]) == 0


async def test_depth_1():
    with my_vcr.use_cassette("tools/get_thread_depth1.yaml"):
        result = await get_thread(STORY_ID, depth=1)
    assert len(result["comments"]) > 0
    for c in result["comments"]:
        assert "replies" not in c
        assert "reply_count" in c


async def test_depth_minus_1_full_tree():
    with my_vcr.use_cassette("tools/get_thread_full.yaml"):
        result = await get_thread(STORY_ID, depth=-1)
    assert result["num_comments"] > 0

    def find_by_id(comments, target_id):
        for c in comments:
            if c["id"] == target_id:
                return c
            found = find_by_id(c.get("replies", []), target_id)
            if found:
                return found
        return None

    brandon = find_by_id(result["comments"], COMMENT_ID)
    assert brandon is not None
    assert brandon["author"] == COMMENT_AUTHOR
    assert brandon["reply_count"] > 0
    assert "replies" in brandon


async def test_deleted_top_level_comments_skipped():
    """Branch: top-level children with author=None are filtered out."""
    fake_data = {
        "id": 1,
        "title": "Test",
        "url": "https://example.com",
        "author": "alice",
        "points": 10,
        "children": [
            {"id": 2, "author": None, "text": None, "children": []},
            {"id": 3, "author": "bob", "text": "hello", "children": []},
        ],
    }
    with patch(
        "hn_mcp.app.client.get_item", new_callable=AsyncMock, return_value=fake_data
    ):
        result = await get_thread(1, depth=1)
    assert len(result["comments"]) == 1
    assert result["comments"][0]["author"] == "bob"
