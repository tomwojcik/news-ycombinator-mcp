"""Tests for app-level helpers: _count_descendants, _prune_comment."""

from hn_mcp.app import _count_descendants, _prune_comment

# Synthetic tree for testing pruning logic in isolation.
TREE = {
    "id": 100,
    "author": "alice",
    "text": "root",
    "children": [
        {
            "id": 101,
            "author": "bob",
            "text": "Top-level comment 1",
            "children": [
                {
                    "id": 201,
                    "author": "carol",
                    "text": "Reply to bob",
                    "children": [
                        {
                            "id": 301,
                            "author": "dave",
                            "text": "Deep reply",
                            "children": [],
                        },
                    ],
                },
                {
                    "id": 202,
                    "author": "eve",
                    "text": "Another reply to bob",
                    "children": [],
                },
            ],
        },
        {"id": 102, "author": "frank", "text": "Top-level comment 2", "children": []},
        {"id": 103, "author": None, "text": None, "children": []},  # deleted
    ],
}


class TestCountDescendants:
    def test_empty(self):
        assert _count_descendants([]) == 0

    def test_flat(self):
        children = [
            {"author": "a", "children": []},
            {"author": "b", "children": []},
        ]
        assert _count_descendants(children) == 2

    def test_nested(self):
        # bob(1) + carol(1) + dave(1) + eve(1) + frank(1) = 5  (deleted #103 excluded)
        assert _count_descendants(TREE["children"]) == 5

    def test_skips_deleted(self):
        children = [
            {"author": None, "children": []},
            {"author": "a", "children": []},
        ]
        assert _count_descendants(children) == 1


class TestPruneComment:
    def test_deleted_returns_none(self):
        assert _prune_comment({"author": None, "children": []}, depth=-1) is None

    def test_depth_0_no_replies_key(self):
        pruned = _prune_comment(TREE["children"][0], depth=0)
        assert pruned["id"] == 101
        assert pruned["author"] == "bob"
        assert pruned["reply_count"] == 3  # carol + dave + eve
        assert "replies" not in pruned

    def test_depth_1_one_level(self):
        pruned = _prune_comment(TREE["children"][0], depth=1)
        assert "replies" in pruned
        assert len(pruned["replies"]) == 2
        assert "replies" not in pruned["replies"][0]  # carol's children not included

    def test_depth_2_two_levels(self):
        pruned = _prune_comment(TREE["children"][0], depth=2)
        carol = pruned["replies"][0]
        assert "replies" in carol
        assert carol["replies"][0]["author"] == "dave"

    def test_depth_minus_1_full_tree(self):
        pruned = _prune_comment(TREE["children"][0], depth=-1)
        carol = pruned["replies"][0]
        assert "replies" in carol
        assert carol["replies"][0]["author"] == "dave"
        assert carol["replies"][0]["reply_count"] == 0

    def test_leaf_comment(self):
        pruned = _prune_comment(
            {"id": 999, "author": "z", "text": "leaf", "children": []}, depth=-1
        )
        assert "replies" not in pruned
        assert pruned["reply_count"] == 0

    def test_deleted_child_skipped_in_replies(self):
        """Branch: _prune_comment returns None for a deleted child inside the loop."""
        node = {
            "id": 1,
            "author": "alice",
            "text": "parent",
            "children": [
                {"id": 2, "author": None, "text": None, "children": []},
                {"id": 3, "author": "bob", "text": "reply", "children": []},
            ],
        }
        pruned = _prune_comment(node, depth=-1)
        assert len(pruned["replies"]) == 1
        assert pruned["replies"][0]["author"] == "bob"
