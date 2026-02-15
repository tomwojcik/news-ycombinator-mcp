from hn_mcp.tools.get_user import get_user
from tests.conftest import USERNAME, my_vcr


async def test_basic():
    with my_vcr.use_cassette("tools/get_user.yaml"):
        result = await get_user(USERNAME)
    assert result["username"] == USERNAME
    assert isinstance(result["karma"], int)
    assert result["karma"] > 0
