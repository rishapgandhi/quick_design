"""Generation tools for Open Design MCP server."""

import json
from mcp.types import Tool

from src.core.gemini import generate_html
from src.core.prompt_builder import build_prompt, load_design_system, PDF_CONSTRAINTS
from src.core.renderer import render
from src.core.pptx_builder import PPTX_PROMPT, create_pptx, get_color_scheme

GENERATE_TOOLS = [
    Tool(
        name="generate_pitch_deck",
        description="Generate a pitch deck HTML for a product/project. Returns the HTML file path for sending.",
        inputSchema={
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "Product/project description or GitHub URL"},
                "design_system": {"type": "string", "description": "Design system ID (e.g. default, linear, stripe, airbnb, apple, tesla, notion — 150 available)", "default": "dark-modern"},
                "slides": {"type": "integer", "description": "Number of slides (default 5)", "default": 5},
            },
            "required": ["brief"],
        },
    ),
    Tool(
        name="generate_pitch_deck_pptx",
        description="Generate a PowerPoint (.pptx) pitch deck file. Returns the PPTX file path for sending.",
        inputSchema={
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "Product/project description"},
                "design_system": {"type": "string", "description": "Design system ID for color scheme", "default": "dark-modern"},
                "slides": {"type": "integer", "description": "Number of slides (default 5)", "default": 5},
            },
            "required": ["brief"],
        },
    ),
    Tool(
        name="generate_landing_page",
        description="Generate a landing page design as HTML. Returns the HTML file path for sending.",
        inputSchema={
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "What the landing page is for"},
                "design_system": {"type": "string", "description": "Design system ID (150 available)", "default": "default"},
            },
            "required": ["brief"],
        },
    ),
    Tool(
        name="generate_dashboard",
        description="Generate an analytics/admin dashboard design as HTML. Returns the HTML file path for sending.",
        inputSchema={
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "What metrics/data to show"},
                "design_system": {"type": "string", "description": "Design system ID", "default": "default"},
            },
            "required": ["brief"],
        },
    ),
    Tool(
        name="generate_email_template",
        description="Generate a branded email template as HTML. Returns the HTML file path for sending.",
        inputSchema={
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "Email purpose and content"},
                "design_system": {"type": "string", "description": "Design system ID", "default": "default"},
            },
            "required": ["brief"],
        },
    ),
    Tool(
        name="generate_social_post",
        description="Generate a social media post design as HTML. Returns the HTML file path for sending.",
        inputSchema={
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "Post topic/content"},
                "design_system": {"type": "string", "description": "Design system ID", "default": "default"},
                "platform": {"type": "string", "description": "instagram, twitter, or linkedin", "default": "instagram"},
            },
            "required": ["brief"],
        },
    ),
    Tool(
        name="generate_hyperframes",
        description="Generate an HTML animation/motion graphic (HyperFrames format) with GSAP. Returns HTML file path. Can be opened in browser for animated preview.",
        inputSchema={
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": "What animation/video to create (e.g. product reveal, logo animation, data visualization)"},
                "design_system": {"type": "string", "description": "Design system ID for colors/typography", "default": "dark-modern"},
                "duration": {"type": "integer", "description": "Duration in seconds (default 5)", "default": 5},
            },
            "required": ["brief"],
        },
    ),
]


async def handle_generate(name: str, arguments: dict) -> str:
    """Handle all generation tool calls."""
    brief = arguments["brief"]
    design_system = arguments.get("design_system", "default")

    # PPTX generation (different pipeline)
    if name == "generate_pitch_deck_pptx":
        return await _handle_pptx(brief, design_system, arguments.get("slides", 5))

    # HyperFrames generation (HTML animation, no PDF)
    if name == "generate_hyperframes":
        return await _handle_hyperframes(brief, design_system, arguments.get("duration", 5))

    # Standard HTML → PDF pipeline
    skill_map = {
        "generate_pitch_deck": "pitch_deck",
        "generate_landing_page": "landing_page",
        "generate_dashboard": "dashboard",
        "generate_email_template": "email_marketing",
        "generate_social_post": "social_post",
    }
    skill_id = skill_map[name]

    # Auto-detect custom skills from brief keywords
    brief_lower = brief.lower()
    if "ferrari" in brief_lower and ("theme" in brief_lower or "style" in brief_lower or "automotive" in brief_lower or "car" in brief_lower):
        skill_id = "ferrari_automotive"

    context_parts = []
    if name == "generate_pitch_deck":
        context_parts.append(f"Generate exactly {arguments.get('slides', 5)} slides.")
    if name == "generate_social_post":
        context_parts.append(f"Platform: {arguments.get('platform', 'instagram')}")

    prompt = build_prompt(skill_id, design_system, brief, context="\n".join(context_parts))
    html = await generate_html(prompt)

    safe_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in brief[:30]).strip("-").lower()
    filename = f"{safe_name}-{skill_id}"

    html_path, zip_path = render(html, filename)

    return json.dumps({
        "html_path": str(html_path),
        "zip_path": str(zip_path),
        "send_file": str(zip_path),
        "summary": f"Generated {skill_id.replace('_', ' ')} with '{design_system}' design system. Send this file to the user: {zip_path} (contains the HTML design, open in browser)",
    }, indent=2)


async def _handle_pptx(brief: str, design_system: str, slides: int) -> str:
    """Generate a .pptx file via Gemini JSON + python-pptx."""
    import google.generativeai as genai
    from src.core.gemini import get_client

    ds_content = load_design_system(design_system)
    prompt = f"""{PPTX_PROMPT}

Topic/Brief: {brief}
Number of slides: {slides}
Design style: {design_system}

Generate exactly {slides} slides as JSON array."""

    model = get_client()
    response = model.generate_content(prompt, generation_config=genai.GenerationConfig(temperature=0.7))
    text = response.text.strip()

    # Extract JSON from response
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0]
    text = text.strip()

    slides_data = json.loads(text)
    colors = get_color_scheme(design_system)

    safe_title = "".join(c if c.isalnum() or c in "-_" else "-" for c in brief[:30]).strip("-").lower()
    pptx_path = create_pptx(slides_data, safe_title, colors)

    return json.dumps({
        "pptx_path": str(pptx_path),
        "slides_count": len(slides_data),
        "summary": f"Generated {len(slides_data)}-slide PPTX deck with '{design_system}' colors. File: {pptx_path}",
    }, indent=2)


async def _handle_hyperframes(brief: str, design_system: str, duration: int) -> str:
    """Generate a HyperFrames HTML animation file."""
    ds_content = load_design_system(design_system)

    prompt = f"""You are a motion graphics engineer. Generate a SINGLE standalone HTML file that creates a smooth animation using GSAP (loaded from CDN: https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js).

REQUIREMENTS:
- Single HTML file with GSAP loaded from CDN
- Animation duration: {duration} seconds
- Resolution: 1920x1080px (16:9 canvas centered on page)
- Auto-plays on load, loops infinitely
- Smooth easing (power2.inOut, elastic, etc.)
- The canvas div should be exactly 1920x1080px with overflow:hidden
- Dark background, vibrant animated elements
- Include a timeline progress bar at the bottom

DESIGN SYSTEM COLORS:
{ds_content[:500]}

ANIMATION BRIEF:
{brief}

Generate kinetic typography, shape animations, or data visualizations as appropriate.
Use GSAP timeline for sequenced animations.

OUTPUT: Return ONLY the complete HTML file starting with <!DOCTYPE html>. No explanations."""

    html = await generate_html(prompt)

    # Save (no PDF conversion — this is meant to be viewed in browser)
    from src.core.renderer import save_html
    safe_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in brief[:30]).strip("-").lower()
    html_path = save_html(html, f"{safe_name}-hyperframes")

    return json.dumps({
        "html_path": str(html_path),
        "format": "hyperframes-html",
        "duration": f"{duration}s",
        "summary": f"Generated HyperFrames animation ({duration}s). Open in browser to view: {html_path}",
        "note": "This is an animated HTML file. Open in a browser to see the animation. It can be screen-recorded or rendered to MP4 with the hyperframes CLI.",
    }, indent=2)
