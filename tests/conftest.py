"""Shared test configuration and fixtures."""

import os

import pytest
import vcr

from hn_mcp.client import HNClient

CASSETTE_DIR = os.path.join(os.path.dirname(__file__), "cassettes")

my_vcr = vcr.VCR(cassette_library_dir=CASSETTE_DIR, record_mode="none")

# Known test data: story 8863 ("My YC app: Dropbox") and comment 9224
STORY_ID = 8863
COMMENT_ID = 9224
STORY_TITLE = "My YC app: Dropbox - Throw away your USB drive"
STORY_AUTHOR = "dhouston"
COMMENT_AUTHOR = "BrandonM"
USERNAME = "norvig"


@pytest.fixture
async def hn_client():
    client = HNClient()
    yield client
    await client.aclose()
