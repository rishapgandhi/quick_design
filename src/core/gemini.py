"""Gemini API client for generating HTML artifacts."""

import os
import google.generativeai as genai

# gemini-3.1-flash-lite: 500 RPD free tier (vs 20 for 2.5-flash)
# 65536 output tokens, good enough for HTML generation
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite")


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key or api_key.startswith("PASTE"):
        raise RuntimeError("GEMINI_API_KEY not set in .env")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL)


async def generate_html(prompt: str) -> str:
    """Call Gemini and return the generated HTML string."""
    model = get_client()
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=30000,
        ),
    )
    text = response.text
    # Extract HTML if wrapped in code fences
    if "```html" in text:
        text = text.split("```html", 1)[1].split("```", 1)[0]
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0]
    return text.strip()
