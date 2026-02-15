"""Algolia HN API client with persistent session."""

from __future__ import annotations

import httpx

BASE_URL = "https://hn.algolia.com/api/v1"


class HNClient:
    """Async client for the Algolia Hacker News API."""

    def __init__(self) -> None:
        self._session: httpx.AsyncClient | None = None

    @property
    def session(self) -> httpx.AsyncClient:
        if self._session is None or self._session.is_closed:
            self._session = httpx.AsyncClient(
                base_url=BASE_URL,
                timeout=30,
                headers={"User-Agent": "hn-mcp/0.1.0"},
            )
        return self._session

    async def aclose(self) -> None:
        if self._session is not None and not self._session.is_closed:
            await self._session.aclose()
            self._session = None

    async def get_item(self, item_id: int) -> dict:
        """GET /items/:id — fetch an item (story or comment) with its full nested children."""
        resp = await self.session.get(f"/items/{item_id}")
        resp.raise_for_status()
        return resp.json()

    async def search(self, params: dict) -> dict:
        """GET /search — search by relevance."""
        resp = await self.session.get("/search", params=params)
        resp.raise_for_status()
        return resp.json()

    async def search_by_date(self, params: dict) -> dict:
        """GET /search_by_date — search sorted by date."""
        resp = await self.session.get("/search_by_date", params=params)
        resp.raise_for_status()
        return resp.json()

    async def get_user(self, username: str) -> dict:
        """GET /users/:username — fetch user profile."""
        resp = await self.session.get(f"/users/{username}")
        resp.raise_for_status()
        return resp.json()
