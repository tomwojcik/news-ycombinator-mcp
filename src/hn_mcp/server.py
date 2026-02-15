"""HN MCP Server entrypoint."""

from hn_mcp.app import mcp  # noqa: F401 — re-export for convenience
import hn_mcp.tools  # noqa: F401 — registers all @mcp.tool() decorators


def main():  # pragma: no cover
    mcp.run(transport="stdio")
