from hn_mcp.tools.get_comment_tree import get_comment_tree
from tests.conftest import COMMENT_AUTHOR, COMMENT_ID, my_vcr


async def test_full_subtree():
    with my_vcr.use_cassette("tools/get_comment_tree_full.yaml"):
        result = await get_comment_tree(COMMENT_ID, depth=-1)
    assert result["id"] == COMMENT_ID
    assert result["author"] == COMMENT_AUTHOR
    assert result["reply_count"] > 0
    assert "replies" in result
    assert len(result["replies"]) > 0


async def test_depth_0():
    with my_vcr.use_cassette("tools/get_comment_tree_depth0.yaml"):
        result = await get_comment_tree(COMMENT_ID, depth=0)
    assert result["id"] == COMMENT_ID
    assert result["author"] == COMMENT_AUTHOR
    assert result["reply_count"] > 0
    assert "replies" not in result


async def test_depth_1():
    with my_vcr.use_cassette("tools/get_comment_tree_depth1.yaml"):
        result = await get_comment_tree(COMMENT_ID, depth=1)
    assert "replies" in result
    for reply in result["replies"]:
        assert "replies" not in reply
