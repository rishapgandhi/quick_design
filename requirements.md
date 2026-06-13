# Open Design MCP Server — Requirements & Implementation Plan

## Project Overview

Build a lightweight MCP server at `/var/www/html/mcp_server/open_design/` that generates design artifacts (pitch decks, landing pages, dashboards, etc.) using Google Gemini API + Open Design's skill prompts and design systems. Outputs are converted to PDF and delivered via OpenClaw's WhatsApp bridge.

---

## System Context

| Component | Detail |
|-----------|--------|
| Location | `/var/www/html/mcp_server/open_design/` |
| Language | Python 3.10 |
| MCP Framework | `mcp` (same as google_mcp/jira_mcp) |
| LLM Provider | Google Gemini 2.5 Flash (free tier) |
| PDF Engine | `wkhtmltopdf` with `QT_QPA_PLATFORM=offscreen` |
| Delivery | OpenClaw WhatsApp bridge (`upload-file` action) |
| Consumer | OpenClaw agent (via MCP server config in `openclaw.json`) |
| Design Intelligence | Open Design skill prompts (`SKILL.md`) + design systems (`DESIGN.md`) bundled locally |

---

## Architecture

```
User (WhatsApp)
    │
    ▼
OpenClaw Gateway (receives message)
    │
    ▼
OpenClaw Agent (Gemini 2.5 Flash)
    │  Decides to call open_design MCP tool
    ▼
┌─────────────────────────────────────────┐
│  open_design MCP Server (stdio)         │
│                                         │
│  Tools:                                 │
│  ├── generate_pitch_deck                │
│  ├── generate_landing_page              │
│  ├── generate_dashboard                 │
│  ├── generate_email_template            │
│  ├── generate_social_post               │
│  ├── list_design_systems                │
│  └── list_skills                        │
│                                         │
│  Flow per generation tool:              │
│  1. Load SKILL.md prompt template       │
│  2. Load DESIGN.md (brand system)       │
│  3. Compose prompt (skill + brand +     │
│     user brief)                         │
│  4. Call Gemini API → get HTML           │
│  5. Save standalone HTML to output/     │
│  6. Convert HTML → PDF via wkhtmltopdf  │
│  7. Return PDF path + summary text      │
└─────────────────────────────────────────┘
    │
    ▼
OpenClaw Agent receives PDF path
    │  Agent sends file via WhatsApp
    ▼
User receives PDF on WhatsApp 📄
```

---

## Directory Structure

```
/var/www/html/mcp_server/open_design/
├── src/
│   ├── __init__.py
│   ├── server.py              # MCP server entry point
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── generate.py        # All generation tools
│   │   └── catalog.py         # list_design_systems, list_skills
│   ├── core/
│   │   ├── __init__.py
│   │   ├── gemini.py          # Gemini API client
│   │   ├── renderer.py        # HTML → PDF conversion
│   │   └── prompt_builder.py  # Composes skill + design system + brief
│   └── skills/                # Bundled skill prompts (from Open Design repo)
│       ├── pitch_deck.md
│       ├── landing_page.md
│       ├── dashboard.md
│       ├── email_marketing.md
│       └── social_post.md
├── design_systems/            # Bundled DESIGN.md files (subset from Open Design)
│   ├── default/DESIGN.md      # Neutral Modern (fallback)
│   ├── linear/DESIGN.md
│   ├── stripe/DESIGN.md
│   ├── notion/DESIGN.md
│   ├── vercel/DESIGN.md
│   └── ... (10-15 popular systems)
├── output/                    # Generated artifacts (HTML + PDF)
│   └── .gitkeep
├── .env                       # GEMINI_API_KEY
├── .env.example
├── pyproject.toml
├── requirements.md            # This file
└── README.md
```

---

## MCP Tools Specification

### 1. `generate_pitch_deck`

| Field | Detail |
|-------|--------|
| Description | Generate a pitch deck PDF for a product/project |
| Input: `brief` (required) | Description of the product/project (text or GitHub URL) |
| Input: `design_system` (optional) | Brand system to use (default: "default") |
| Input: `slides` (optional) | Number of slides (default: 5) |
| Output | JSON with `pdf_path`, `html_path`, `summary` |

### 2. `generate_landing_page`

| Field | Detail |
|-------|--------|
| Description | Generate a landing page design as PDF |
| Input: `brief` (required) | What the page is for |
| Input: `design_system` (optional) | Brand system (default: "default") |
| Input: `sections` (optional) | Sections to include (hero, features, pricing, cta) |
| Output | JSON with `pdf_path`, `html_path`, `summary` |

### 3. `generate_dashboard`

| Field | Detail |
|-------|--------|
| Description | Generate an analytics/admin dashboard design as PDF |
| Input: `brief` (required) | What metrics/data to show |
| Input: `design_system` (optional) | Brand system (default: "default") |
| Output | JSON with `pdf_path`, `html_path`, `summary` |

### 4. `generate_email_template`

| Field | Detail |
|-------|--------|
| Description | Generate a branded email template as PDF |
| Input: `brief` (required) | Email purpose and content |
| Input: `design_system` (optional) | Brand system (default: "default") |
| Output | JSON with `pdf_path`, `html_path`, `summary` |

### 5. `generate_social_post`

| Field | Detail |
|-------|--------|
| Description | Generate a social media post design (1080x1080) as PDF |
| Input: `brief` (required) | Post topic/content |
| Input: `design_system` (optional) | Brand system (default: "default") |
| Input: `platform` (optional) | instagram, twitter, linkedin (default: instagram) |
| Output | JSON with `pdf_path`, `html_path`, `summary` |

### 6. `list_design_systems`

| Field | Detail |
|-------|--------|
| Description | List all available design systems |
| Input | None |
| Output | JSON array of `{id, name, description}` |

### 7. `list_skills`

| Field | Detail |
|-------|--------|
| Description | List all available generation skills |
| Input | None |
| Output | JSON array of `{id, name, description}` |

---

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Standalone single-file HTML | All CSS/JS inlined, no external deps, works offline |
| `wkhtmltopdf` for PDF (not Playwright) | Already installed, lightweight, fast |
| `QT_QPA_PLATFORM=offscreen` env var | Required on headless/Wayland Ubuntu |
| Gemini 2.5 Flash (free tier) | Already configured in OpenClaw, sufficient for HTML generation |
| Bundled skills (not full Open Design clone) | Only need the prompt templates, not the 36k-line monorepo |
| 10-15 design systems (not all 150) | Keep it lean, add more on demand |
| Output stored under MCP server | Self-contained, easy cleanup, no external paths |
| GitHub URL support | Agent fetches README from GitHub to understand the project before generating |

---

## Dependencies

```
mcp>=1.0.0
google-generativeai==0.8.3
python-dotenv==1.0.1
httpx==0.27.0          # For fetching GitHub READMEs
```

System dependencies (already present):
- `wkhtmltopdf` ✅
- Python 3.10 ✅

---

## Configuration

### `.env`
```
GEMINI_API_KEY=your_gemini_api_key_here
OUTPUT_DIR=/var/www/html/mcp_server/open_design/output
```

### OpenClaw Integration (`~/.openclaw/openclaw.json` → `mcp.servers`)
```json
{
  "open_design": {
    "command": "python3",
    "args": ["-m", "src.server"],
    "cwd": "/var/www/html/mcp_server/open_design"
  }
}
```

---

## Example End-to-End Flow

**User sends on WhatsApp:**
> "Generate a pitch deck for TaskMind - it's an AI task management app at https://github.com/rishapgandhi/taskmind"

**OpenClaw agent:**
1. Recognizes design generation intent
2. Calls `generate_pitch_deck` tool with:
   - `brief`: "AI task management app - TaskMind"
   - GitHub README content (fetched by agent or MCP tool)
   - `design_system`: "default"
   - `slides`: 5

**MCP server internally:**
1. Loads `skills/pitch_deck.md` prompt
2. Loads `design_systems/default/DESIGN.md`
3. Composes full prompt: skill instructions + design tokens + user brief
4. Calls Gemini → receives standalone HTML with 5 slides
5. Saves HTML to `output/taskmind-pitch-20260611-134500.html`
6. Runs `wkhtmltopdf` → `output/taskmind-pitch-20260611-134500.pdf`
7. Returns: `{"pdf_path": "/var/www/html/mcp_server/open_design/output/taskmind-pitch-20260611-134500.pdf", "summary": "5-slide pitch deck for TaskMind generated with Neutral Modern design system."}`

**OpenClaw agent:**
- Sends the PDF file to user on WhatsApp
- Sends text: "Here's your TaskMind pitch deck! 5 slides covering problem, solution, features, traction, and ask."

---

## Tasks & Status

| # | Task | Status | Details |
|---|------|--------|---------|
| 1 | Create project directory structure | ⬜ Pending | Dirs: src/, src/tools/, src/core/, output/ |
| 2 | Create `pyproject.toml` with dependencies | ⬜ Pending | mcp, google-generativeai, httpx, dotenv |
| 3 | Create `.env.example` and `.env` | ⬜ Pending | Need Gemini API key from user |
| 4 | Build `src/server.py` (MCP entry point) | ⬜ Pending | Same pattern as google_mcp |
| 5 | Build `src/core/gemini.py` (API client) | ⬜ Pending | Call Gemini with composed prompt |
| 6 | Build `src/core/prompt_builder.py` | ⬜ Pending | Merge skill + design system + brief |
| 7 | Build `src/core/renderer.py` (HTML→PDF) | ⬜ Pending | wkhtmltopdf wrapper with offscreen env |
| 8 | Build `src/tools/generate.py` (generation tools) | ⬜ Pending | All 5 generation tools |
| 9 | Build `src/tools/catalog.py` (list tools) | ⬜ Pending | list_design_systems, list_skills |
| 10 | Bundle skill prompts from Open Design repo | ⬜ Pending | Download and adapt 5 key skill prompt files |
| 11 | Bundle design systems from Open Design repo | ⬜ Pending | Download 10-15 popular DESIGN.md files |
| 12 | Register in OpenClaw config (`openclaw.json`) | ⬜ Pending | Add to mcp.servers section |
| 13 | Test: generate HTML via Gemini | ⬜ Pending | Verify quality of output |
| 14 | Test: HTML → PDF conversion | ⬜ Pending | Verify rendering fidelity |
| 15 | Test: Full flow via OpenClaw WhatsApp | ⬜ Pending | End-to-end message → PDF on WhatsApp |
| 16 | Add GitHub README fetching for project briefs | ⬜ Pending | httpx fetch raw README.md from GitHub URLs |
| 17 | Documentation (README.md) | ⬜ Pending | Usage, setup, troubleshooting |

---

## Limitations & Known Constraints

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Gemini free tier rate limits | 15 RPM, 1M TPM | Sufficient for personal use |
| No AI image generation | Decks use CSS/HTML visuals only, no photos | Use icons, gradients, shapes via CSS |
| wkhtmltopdf CSS support | Doesn't support flexbox/grid perfectly | Use float/table-based layouts in skill prompts |
| Multi-slide deck in PDF | Needs page breaks | Use `page-break-after: always` CSS in skill prompt |
| WhatsApp file size limit | Max 50MB per file | HTML decks produce ~50-200KB PDFs — well within limit |
| No interactive previews | PDF is static | HTML file also saved if user wants to view in browser later |

---

## Future Enhancements (Post-MVP)

- [ ] Add more design systems on demand
- [ ] Add `generate_mobile_app_mockup` skill
- [ ] Add `generate_resume` skill
- [ ] Image generation via paid API (OpenAI gpt-image-2) when user opts in
- [ ] HyperFrames video generation (requires Chrome + FFmpeg pipeline)
- [ ] Scheduled generation (weekly report decks via OpenClaw cron)
- [ ] Template memory — remember user's preferred design system
- [ ] Multi-format output — PPTX export alongside PDF

---

## Verified System Requirements ✅

| Requirement | Status | Verified |
|-------------|--------|----------|
| Python 3.10 | ✅ Installed | `python3 --version` → 3.10.12 |
| wkhtmltopdf | ✅ Installed | `/usr/bin/wkhtmltopdf` (needs `QT_QPA_PLATFORM=offscreen`) |
| OpenClaw 2026.6.1 | ✅ Running | WhatsApp bridge active |
| WhatsApp file sending | ✅ Confirmed | Tested: sent .txt and .pdf successfully on 2026-06-11 |
| Gemini API access | ✅ Configured | Already in OpenClaw as `google/gemini-2.5-flash` |
| MCP server pattern | ✅ Established | google_mcp + jira_mcp working |
| OpenClaw MCP integration | ✅ Configured | `openclaw.json` → `mcp.servers` pattern known |

---

## Approval Checklist (Before Implementation)

- [ ] Gemini API key — is it in OpenClaw's config or do you have a separate key for this server?
- [ ] Preferred design systems to bundle (or start with defaults + add later?)
- [ ] Any specific branding for your own projects (TaskMind, etc.)?
- [ ] OK to proceed with the 17-task implementation plan?
