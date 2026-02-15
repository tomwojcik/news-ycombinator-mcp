"""Typed return shapes for all MCP tools."""

from __future__ import annotations

from typing import NotRequired, TypedDict


class Comment(TypedDict):
    id: int | None
    author: str
    text: str
    reply_count: int
    replies: NotRequired[list[Comment]]


class Story(TypedDict):
    id: int | None
    title: str | None
    url: str | None
    author: str | None
    points: int | None
    num_comments: int


class Thread(Story):
    comments: list[Comment]


class StoryItem(TypedDict):
    id: int | None
    title: str | None
    url: str | None
    author: str | None
    points: int | None
    num_comments: int | None


class StorySearchResult(TypedDict):
    total_hits: int | None
    page: int | None
    total_pages: int | None
    stories: list[StoryItem]


class CommentHit(TypedDict):
    id: int | None
    story_id: int | None
    story_title: str | None
    parent_id: int | None
    author: str | None
    text: str | None


class CommentSearchResult(TypedDict):
    total_hits: int | None
    page: int | None
    total_pages: int | None
    comments: list[CommentHit]


class UserProfile(TypedDict):
    username: str | None
    karma: int | None
    about: str | None
    created_at: str | None


class ErrorResult(TypedDict):
    error: str
