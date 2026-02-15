from hn_mcp.tools.search_stories import search_stories
from tests.conftest import my_vcr


async def test_relevance():
    with my_vcr.use_cassette("tools/search_stories_relevance.yaml"):
        result = await search_stories("Dropbox", sort_by="relevance", count=5)
    assert result["total_hits"] > 0
    assert len(result["stories"]) > 0
    assert any("Dropbox" in (s.get("title") or "") for s in result["stories"])


async def test_date_sort():
    with my_vcr.use_cassette("tools/search_stories_date.yaml"):
        result = await search_stories("Dropbox", sort_by="date", count=5)
    assert result["total_hits"] > 0
    assert len(result["stories"]) > 0
