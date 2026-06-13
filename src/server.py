"""Open Design MCP Server — generates design artifacts via Gemini, delivers PDF."""

import asyncio
from pathlib import Path

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

load_dotenv(Path(__file__).parent.parent / ".env")

from src.tools.generate import GENERATE_TOOLS, handle_generate
from src.tools.catalog import CATALOG_TOOLS, handle_catalog

app = Server("open-design-mcp")

ALL_TOOLS = GENERATE_TOOLS + CATALOG_TOOLS

HANDLERS = {
    **{t.name: handle_generate for t in GENERATE_TOOLS},
    **{t.name: handle_catalog for t in CATALOG_TOOLS},
}


@app.list_tools()
async def list_tools() -> list[Tool]:
    return ALL_TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    handler = HANDLERS.get(name)
    if not handler:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    try:
        result = await handler(name, arguments)
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {type(e).__name__}: {e}")]


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
