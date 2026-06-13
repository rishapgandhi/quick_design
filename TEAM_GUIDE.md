# Quick Design MCP — Team Guide

**Repo:** https://github.com/rishapgandhi/quick_design
**Demo site:** https://rishapgandhi.github.io/quick_design/

---

## What is this?

Quick Design is an **MCP server** that generates production-quality HTML designs in seconds. You give it a prompt, it gives you back a complete HTML page (or PDF/PPTX).

It comes with:
- **150 design systems** — Apple, Ferrari, Tesla, Stripe, Linear, Notion, Airbnb, Nike, etc.
- **270+ skills** — Dashboards, pitch decks, landing pages, emails, social posts, animations
- **Custom skills** — Create your own brand template once, reuse it forever

Connect it to **any AI tool** — Gemini, Claude, OpenAI, OpenClaw, Kiro, Cursor, Claude Code — and generate designs from a single prompt.

---

## What it can really do

| Use case | What you get |
|----------|-------------|
| "Generate a pitch deck for our product" | 5-slide PDF/PPTX with brand colors, real layout, SVG charts |
| "Create a KPI dashboard for project management" | Full admin dashboard with sidebar, stats, charts, data table |
| "Make a landing page for our SaaS" | Hero + features + pricing + CTA — styled to any brand |
| "Design an email template for product launch" | Email-client-compatible HTML email |
| "Create a social post for Instagram" | 1080x1080 branded graphic |
| "Generate a motion graphic for logo reveal" | GSAP-animated HTML you can screen-record |
| **"Create Mahindra car html using ferrari theme"** | **Full cinematic red/black branded page in one shot** |

---

## The Ferrari → Mahindra Example (Real)

This is the killer feature. We created a `ferrari_automotive` skill that bakes Ferrari's exact CSS patterns into a template:

**What the skill contains:**
- Red (#DA291C) and black gradient backgrounds
- Red ambient glow effects
- Editorial section rhythm (dark → red stats → dark)
- Razor-sharp 2px buttons
- Exact CSS code the AI copies directly

**What you type:**
> "Create a landing page for MAHINDRA using ferrari_automotive skill. Models: Thar Roxx, XUV700, Scorpio-N."

**What you get back in ~10 seconds:**
A full dramatic landing page with:
- Red/black gradient hero with glowing emblem
- Vehicle lineup with red-tinted backgrounds
- Stats section on FULL RED background
- Editorial story sections with red ambient light
- Subscribe CTA on solid red
- Complete, self-contained, single-file HTML

**Works for ANY brand** — just swap the name. Tata, Maruti, Hyundai, MG, your own company.

---

## From WhatsApp (via OpenClaw)

If you have OpenClaw set up with WhatsApp bridge:

1. Send a message on WhatsApp: **"Create Mahindra car html using ferrari theme"**
2. OpenClaw reads it → calls Quick Design MCP → Gemini generates HTML → converts to PDF
3. You receive the **PDF on WhatsApp** in 10-15 seconds

That's it. Design from your phone. No laptop needed.

---

## Setup (5 minutes)

### Step 1: Clone and install

```bash
git clone https://github.com/rishapgandhi/quick_design.git
cd quick_design
pip install -r requirements.txt
cp .env.example .env
```

### Step 2: Add your API key

Edit `.env`:
```
GEMINI_API_KEY=your_key_here
```

**Free tier options:**
- `gemini-3.1-flash-lite` — 500 requests/day (default, recommended for testing)
- `gemini-2.5-flash` — 20 requests/day (better quality, lower limit)

Get a free key: https://aistudio.google.com/apikey

**Paid options (better quality):**
- Set `GEMINI_MODEL=gemini-2.5-pro` for Gemini Pro
- Or swap the API client in `src/core/gemini.py` for OpenAI/Claude

### Step 3: Connect to your AI tool

**OpenClaw** (add to `~/.openclaw/openclaw.json` → `mcp.servers`):
```json
"quick_design": {
  "command": "python3",
  "args": ["-m", "src.server"],
  "cwd": "/path/to/quick_design"
}
```

**Claude Code:**
```bash
claude mcp add quick_design python3 -- -m src.server --cwd /path/to/quick_design
```

**Kiro / Cursor / Any MCP-compatible tool:**
Add the same stdio server config to your tool's MCP settings.

### Step 4: Use it

From any connected AI agent:
```
"Generate a pitch deck for TaskMind using the stripe design system"
"Create a dashboard showing sales KPIs with the linear design"
"Make a landing page for my portfolio using apple design"
"Create Mahindra car html using ferrari_automotive skill"
```

---

## Available Design Systems (150)

**Tech:** apple, cursor, discord, figma, github, linear-app, notion, vercel, meta, nvidia, openai, claude

**Automotive:** bmw, bugatti, ferrari, lamborghini, renault, tesla

**Fintech:** binance, coinbase, stripe, mastercard, revolut, wise

**E-commerce:** airbnb, nike, shopify, starbucks, uber

**Styles:** brutalism, glassmorphism, retro, neon, minimal, elegant, futuristic, dramatic

All 150: run `list_design_systems` tool to see the full list.

---

## Creating Your Own Skill (5 minutes)

The secret sauce: **don't describe what you want — give the AI exact CSS to copy.**

1. Create `src/skills/your_brand.md`
2. Paste your exact CSS patterns as code blocks
3. Define a rigid section structure (numbered list)
4. The AI copies it perfectly every time

Example structure:
```markdown
# My Brand Skill

## EXACT CSS Patterns
.hero { background: linear-gradient(...); }
.card { border: 1px solid ...; border-radius: ...; }

## Page Sections (follow this order)
1. Hero — full height, centered text, gradient bg
2. Features — 3 cards in a row
3. Stats — numbers on colored background
4. CTA — single button, centered
```

---

## Tech Details

- **Server:** Python 3.10+ MCP stdio server
- **Model:** Gemini 3.1 Flash Lite (free, 500 req/day) — swap for any model
- **PDF:** wkhtmltopdf (local, no API needed)
- **PPTX:** python-pptx (local)
- **Protocol:** MCP (Model Context Protocol) — universal AI tool standard
- **Source:** Built on [Open Design](https://github.com/nexu-io/open-design) (Apache-2.0)

---

## Questions?

- Repo: https://github.com/rishapgandhi/quick_design
- Wiki: https://github.com/rishapgandhi/quick_design/wiki
- Discussions: https://github.com/rishapgandhi/quick_design/discussions
