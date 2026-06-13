"""Catalog tools - list available skills and design systems."""

import json
from mcp.types import Tool

from src.core.prompt_builder import list_available_skills, list_available_design_systems

CATALOG_TOOLS = [
    Tool(
        name="list_design_systems",
        description="List all available design systems for generation",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="list_skills",
        description="List all available generation skills",
        inputSchema={"type": "object", "properties": {}},
    ),
]


async def handle_catalog(name: str, arguments: dict) -> str:
    """Handle catalog tool calls."""
    if name == "list_design_systems":
        systems = list_available_design_systems()
        return json.dumps(systems, indent=2)
    elif name == "list_skills":
        skills = list_available_skills()
        return json.dumps(skills, indent=2)
    return "Unknown catalog tool"
