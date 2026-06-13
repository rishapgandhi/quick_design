# Quick Design

> An MCP server that generates professional design artifacts (HTML, PDF, PPTX) in seconds — powered by Open Design's 150 design systems and 270+ skills.

Built on top of [Open Design](https://github.com/nexu-io/open-design) — the open-source Claude Design alternative. Quick Design reimagines it as a **lightweight MCP server** that any AI agent (OpenClaw, Claude Code, Kiro, Cursor) can call for instant design generation.

## What It Does

```
Your message → AI Agent → Quick Design MCP → Gemini generates HTML → PDF/PPTX → Delivered
```

**Feed a design system as a skill. Get production-quality HTML in one shot.**

## Features

- 🎨 **150 Design Systems** — Airbnb, Apple, Tesla, Linear, Stripe, Notion, Ferrari, and 144 more
- ⚡ **270+ Skills** — Dashboards, pitch decks, landing pages, email templates, social posts, animations
- 📄 **Multi-format output** — HTML, PDF (via wkhtmltopdf), PPTX (via python-pptx)
- 🎞️ **HyperFrames** — HTML/GSAP animations for motion graphics
- 🚗 **Custom brand skills** — Bake exact CSS into skills for consistent one-shot output
- 🔌 **MCP protocol** — Works with OpenClaw, Claude Code, Kiro, Cursor, any MCP-compatible agent
- 📱 **WhatsApp delivery** — Via OpenClaw bridge (send PDFs directly to WhatsApp)

## Quick Start

```bash
# Clone
git clone https://github.com/rishapgandhi/quick_design.git
cd quick_design

# Install dependencies
pip install -e .

# Set your Gemini API key
cp .env.example .env
# Edit .env → paste your key from https://aistudio.google.com/apikey

# Test
python3 -c "from src.core.prompt_builder import list_available_skills; print(f'{len(list_available_skills())} skills loaded')"
```

## MCP Server Setup

### With OpenClaw

Add to `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "quick_design": {
        "command": "python3",
        "args": ["-m", "src.server"],
        "cwd": "/path/to/quick_design"
      }
    }
  }
}
```

### With Claude Code / Kiro

```bash
claude mcp add quick_design python3 -m src.server --cwd /path/to/quick_design
```

## Available Tools

| Tool | Output | Description |
|------|--------|-------------|
| `generate_pitch_deck` | PDF | Multi-slide pitch deck |
| `generate_pitch_deck_pptx` | PPTX | PowerPoint file |
| `generate_landing_page` | PDF | Marketing landing page |
| `generate_dashboard` | PDF | Analytics/KPI dashboard |
| `generate_email_template` | PDF | Branded email |
| `generate_social_post` | PDF | Social media graphic |
| `generate_hyperframes` | HTML | GSAP animation |
| `list_design_systems` | JSON | All 150 design systems |
| `list_skills` | JSON | All 270+ skills |

## Example: Ferrari Design for Mahindra

This is the power of Quick Design — take any design system, apply it to any brand:

**Prompt:**
```
Create a landing page for MAHINDRA using the ferrari_automotive skill.
Models: Thar Roxx, XUV700, Scorpio-N, XUV 3XO, BE 6e
Tagline: "Explore the Impossible"
```

**Result:** A full cinematic red-and-black landing page with Ferrari's design DNA — gradients, red glows, razor-sharp buttons, editorial layout — applied to Mahindra's brand.

The `ferrari_automotive` skill has exact CSS patterns baked in:
- Red (#DA291C) and black gradients throughout
- Red ambient glow effects behind vehicles
- Full red stats section
- Chiaroscuro editorial rhythm
- 2px border-radius (razor precision)

**This approach works for any brand × any design system.** Feed a skill with exact CSS, get consistent output every time.

## How It Works

```
┌─────────────────────────────────────────────────┐
│         Quick Design MCP Server                  │
│                                                  │
│  Prompt = Skill + Design System + Brief          │
│                                                  │
│  1. Load skill (CSS patterns + layout rules)     │
│  2. Load design system (brand tokens)            │
│  3. Load craft rules (anti-AI-slop quality)      │
│  4. Compose prompt → send to Gemini              │
│  5. Save HTML → convert to PDF/PPTX             │
│  6. Return file path to agent                    │
└─────────────────────────────────────────────────┘
```

## Adding Custom Skills

Drop a `.md` file in `src/skills/`:

```markdown
# My Custom Skill

## EXACT CSS Patterns To Use
(paste your CSS here — the model copies it)

## Page Section Structure
1. Section name — description
2. Section name — description
...
```

The key insight: **don't describe what you want — give the model exact CSS to copy.** Small models follow templates perfectly but fail at creative interpretation.

## Design Systems

150 systems from [Open Design](https://github.com/nexu-io/open-design/tree/main/design-systems):

`airbnb` · `apple` · `bmw` · `claude` · `cursor` · `discord` · `ferrari` · `figma` · `github` · `linear-app` · `meta` · `nike` · `notion` · `nvidia` · `shopify` · `spotify` · `stripe` · `supabase` · `tesla` · `uber` · `vercel` · and 130 more...

## Tech Stack

- **Python 3.10+**
- **MCP protocol** (stdio server)
- **Google Gemini 3.1 Flash Lite** (500 req/day free tier)
- **wkhtmltopdf** (HTML → PDF)
- **python-pptx** (PPTX generation)
- **Open Design repo** (skills + design systems source)

## Acknowledgements

This project is built on [Open Design](https://github.com/nexu-io/open-design) (Apache-2.0) — the open-source Claude Design alternative by [nexu-io](https://github.com/nexu-io). We use their:
- 150 design systems (`DESIGN.md` files)
- 270+ skill prompts (`SKILL.md` files)
- Craft rules (anti-AI-slop, typography, color discipline)

Quick Design doesn't replace Open Design — it's a lightweight MCP adapter that makes the same design intelligence available as a single-shot tool call for any AI agent.

## License

MIT
