from hn_mcp.tools.search_comments import search_comments
from tests.conftest import COMMENT_AUTHOR, STORY_ID, my_vcr


async def test_basic():
    with my_vcr.use_cassette("tools/search_comments_basic.yaml"):
        result = await search_comments("dropbox", count=5)
    assert result["total_hits"] > 0
    assert len(result["comments"]) > 0
    for c in result["comments"]:
        assert "author" in c
        assert "text" in c


async def test_story_filter():
    with my_vcr.use_cassette("tools/search_comments_story_filter.yaml"):
        result = await search_comments("dropbox", story_id=STORY_ID, count=5)
    assert result["total_hits"] > 0
    for c in result["comments"]:
        assert c["story_id"] == STORY_ID


async def test_author_filter():
    with my_vcr.use_cassette("tools/search_comments_author_filter.yaml"):
        result = await search_comments("dropbox", author=COMMENT_AUTHOR, count=5)
    assert result["total_hits"] > 0
    for c in result["comments"]:
        assert c["author"] == COMMENT_AUTHOR


async def test_date_sort():
    with my_vcr.use_cassette("tools/search_comments_date.yaml"):
        result = await search_comments("dropbox", sort_by="date", count=5)
    assert result["total_hits"] > 0
    assert len(result["comments"]) > 0
