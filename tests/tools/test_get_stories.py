from hn_mcp.tools.get_stories import get_stories
from tests.conftest import my_vcr


async def test_top():
    with my_vcr.use_cassette("tools/get_stories_top.yaml"):
        result = await get_stories("top", count=5)
    assert len(result) == 5
    for s in result:
        assert "id" in s
        assert "title" in s
        assert "author" in s


async def test_new():
    with my_vcr.use_cassette("tools/get_stories_new.yaml"):
        result = await get_stories("new", count=3)
    assert len(result) == 3


async def test_ask_hn():
    with my_vcr.use_cassette("tools/get_stories_ask.yaml"):
        result = await get_stories("ask_hn", count=3)
    assert len(result) == 3


async def test_show_hn():
    with my_vcr.use_cassette("tools/get_stories_show.yaml"):
        result = await get_stories("show_hn", count=3)
    assert len(result) == 3


async def test_invalid_category():
    result = await get_stories("invalid")  # type: ignore[arg-type]
    assert result["error"].startswith("Invalid category")
