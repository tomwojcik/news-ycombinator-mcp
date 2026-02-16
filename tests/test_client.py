"""Tests for HNClient — each method hits the Algolia API (replayed via VCR)."""

from hn_mcp.client import HNClient
from tests.conftest import (
    COMMENT_AUTHOR,
    COMMENT_ID,
    STORY_AUTHOR,
    STORY_ID,
    STORY_TITLE,
    USERNAME,
    my_vcr,
)


async def test_get_item_story(hn_client: HNClient):
    with my_vcr.use_cassette("client/get_item_story.yaml"):
        data = await hn_client.get_item(STORY_ID)
    assert data["id"] == STORY_ID
    assert data["title"] == STORY_TITLE
    assert data["author"] == STORY_AUTHOR
    assert isinstance(data["children"], list)
    assert len(data["children"]) > 0


async def test_get_item_comment(hn_client: HNClient):
    with my_vcr.use_cassette("client/get_item_comment.yaml"):
        data = await hn_client.get_item(COMMENT_ID)
    assert data["id"] == COMMENT_ID
    assert data["author"] == COMMENT_AUTHOR
    assert isinstance(data["children"], list)
    assert len(data["children"]) > 0


async def test_search(hn_client: HNClient):
    with my_vcr.use_cassette("client/search.yaml"):
        data = await hn_client.search(
            {"query": "Dropbox", "tags": "story", "hitsPerPage": 5}
        )
    assert data["nbHits"] > 0
    assert len(data["hits"]) > 0
    assert any("Dropbox" in (h.get("title") or "") for h in data["hits"])


async def test_search_by_date(hn_client: HNClient):
    with my_vcr.use_cassette("client/search_by_date.yaml"):
        data = await hn_client.search_by_date(
            {"query": "Dropbox", "tags": "story", "hitsPerPage": 5}
        )
    assert data["nbHits"] > 0
    assert len(data["hits"]) > 0


async def test_get_user(hn_client: HNClient):
    with my_vcr.use_cassette("client/get_user.yaml"):
        data = await hn_client.get_user(USERNAME)
    assert data["username"] == USERNAME
    assert isinstance(data["karma"], int)


async def test_aclose_without_session():
    """Branch: aclose() when no session has been created yet."""
    client = HNClient()
    await client.aclose()  # should be a no-op
    assert client._session is None
