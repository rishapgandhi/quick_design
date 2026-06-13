"""Compose the full prompt from skill template + design system + craft rules + user brief.

Prompt layers (in order):
1. System role + PDF constraints
2. Craft rules (anti-slop, color discipline, typography)
3. Design System (brand tokens)
4. Skill (workflow + output contract)
5. User brief + context
"""

from pathlib import Path

# Sources
LOCAL_SKILLS_DIR = Path(__file__).parent.parent / "skills"
REPO_SKILLS_DIR = Path("/var/www/html/test/open-design/skills")
REPO_TEMPLATES_DIR = Path("/var/www/html/test/open-design/design-templates")
DESIGN_SYSTEMS_DIR = Path("/var/www/html/test/open-design/design-systems")
CRAFT_DIR = Path("/var/www/html/test/open-design/craft")

if not DESIGN_SYSTEMS_DIR.exists():
    DESIGN_SYSTEMS_DIR = Path(__file__).parent.parent.parent / "design_systems"

# --- PDF constraints for wkhtmltopdf ---
PDF_CONSTRAINTS = """## PDF RENDERING CONSTRAINTS (wkhtmltopdf)
- All CSS inlined in <style> — no external files, no CDN
- No CSS variables (var()) — hardcode values
- No display:flex/grid — use display:table/table-cell for centering, float for columns
- No vh/vw — use mm or px
- No gradients on large areas — solid colors only (small accent gradients OK)
- No box-shadow — use borders
- Font: Arial, Helvetica, sans-serif only
- @page { size: A4 landscape; margin: 0; }
- Each slide/section: width:297mm; height:210mm; padding:30mm 40mm; page-break-after:always; overflow:hidden;
- Vertical centering: display:table on section + display:table-cell; vertical-align:middle on inner wrapper
- Last section: page-break-after:avoid
- Inline SVG for charts (polyline, rect, circle) — no JS chart libraries"""

# --- Craft rules (loaded once) ---
_craft_cache = {}


def _load_craft() -> str:
    """Load core craft rules: anti-slop + color + typography."""
    if "combined" in _craft_cache:
        return _craft_cache["combined"]

    parts = []
    for name in ["anti-ai-slop.md", "color.md", "typography.md"]:
        path = CRAFT_DIR / name
        if path.exists():
            parts.append(path.read_text(encoding="utf-8"))

    combined = "\n\n---\n\n".join(parts)
    _craft_cache["combined"] = combined
    return combined


# --- Design system loader ---
def load_design_system(system_id: str) -> str:
    """Load a design system DESIGN.md by ID with fuzzy matching."""
    # Exact match
    path = DESIGN_SYSTEMS_DIR / system_id / "DESIGN.md"
    if path.exists():
        return path.read_text(encoding="utf-8")

    # Try -app suffix
    path = DESIGN_SYSTEMS_DIR / f"{system_id}-app" / "DESIGN.md"
    if path.exists():
        return path.read_text(encoding="utf-8")

    # Partial match
    for d in DESIGN_SYSTEMS_DIR.iterdir():
        if d.is_dir() and system_id in d.name and (d / "DESIGN.md").exists():
            return (d / "DESIGN.md").read_text(encoding="utf-8")

    # Fallback
    path = DESIGN_SYSTEMS_DIR / "default" / "DESIGN.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _truncate_design_system(ds: str, max_chars: int = 4000) -> str:
    """Keep color + typography + components sections, trim the rest."""
    if len(ds) <= max_chars:
        return ds
    # Cut at layout/depth/responsive sections
    for cutoff in ["## 5.", "## 5 ", "## Layout Principles", "## Depth", "## Do's", "## 8.", "## 9."]:
        idx = ds.find(cutoff)
        if 500 < idx < max_chars:
            return ds[:idx].strip()
    return ds[:max_chars]


# --- Skill loader ---
def _find_skill(skill_id: str) -> Path | None:
    """Search for a skill across all sources."""
    # 1. Repo design-templates (highest quality — has full workflow)
    repo_template = REPO_TEMPLATES_DIR / skill_id / "SKILL.md"
    if repo_template.exists():
        return repo_template

    # 2. Repo skills
    repo_skill = REPO_SKILLS_DIR / skill_id / "SKILL.md"
    if repo_skill.exists():
        return repo_skill

    # 3. Local PDF-optimized skills (fallback)
    local_md = LOCAL_SKILLS_DIR / f"{skill_id}.md"
    if local_md.exists():
        return local_md

    # 4. Fuzzy (replace _ with -)
    alt_id = skill_id.replace("_", "-")
    for path in [REPO_TEMPLATES_DIR / alt_id / "SKILL.md", REPO_SKILLS_DIR / alt_id / "SKILL.md"]:
        if path.exists():
            return path
    return None


def load_skill(skill_id: str) -> str:
    """Load a skill prompt template by ID."""
    path = _find_skill(skill_id)
    if not path:
        raise FileNotFoundError(f"Skill not found: {skill_id}")
    return path.read_text(encoding="utf-8")


# --- Catalog ---
def list_available_skills() -> list[dict]:
    """List all available skills from all sources."""
    skills = []
    seen = set()

    for src_dir, source_name in [(LOCAL_SKILLS_DIR, "local"), (REPO_SKILLS_DIR, "repo"), (REPO_TEMPLATES_DIR, "template")]:
        if not src_dir.exists():
            continue
        if source_name == "local":
            for path in sorted(src_dir.glob("*.md")):
                skill_id = path.stem
                if skill_id in seen:
                    continue
                seen.add(skill_id)
                first_line = path.read_text(encoding="utf-8").split("\n", 1)[0].strip("# ")
                skills.append({"id": skill_id, "name": skill_id.replace("_", " ").title(), "description": first_line, "source": source_name})
        else:
            for skill_dir in sorted(src_dir.iterdir()):
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    skill_id = skill_dir.name
                    if skill_id in seen:
                        continue
                    content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                    if len(content.split("\n")) < 20:
                        continue
                    seen.add(skill_id)
                    desc = skill_id.replace("-", " ").title()
                    for line in content.split("\n"):
                        if line.strip().startswith("description:"):
                            desc = line.split(":", 1)[1].strip().strip("|").strip('"')[:80]
                            break
                    skills.append({"id": skill_id, "name": desc[:60], "description": desc, "source": source_name})
    return skills


def list_available_design_systems() -> list[dict]:
    """List all available design systems."""
    systems = []
    for path in sorted(DESIGN_SYSTEMS_DIR.iterdir()):
        if path.is_dir() and (path / "DESIGN.md").exists():
            content = (path / "DESIGN.md").read_text(encoding="utf-8")
            first_line = content.split("\n", 1)[0].strip("# ")
            systems.append({"id": path.name, "name": path.name.replace("-", " ").title(), "description": first_line})
    return systems


# --- Prompt composition ---
def build_prompt(skill_id: str, design_system_id: str, brief: str, **kwargs) -> str:
    """Compose the full generation prompt with all quality layers."""
    skill = load_skill(skill_id)
    design_system = _truncate_design_system(load_design_system(design_system_id))
    craft = _load_craft()

    # Custom skills with baked-in CSS don't need PDF constraints
    skip_pdf = skill_id in ("ferrari_automotive",) or "EXACT CSS" in skill

    prompt = f"""You are a senior design engineer at a top-tier design agency.
You produce artifacts that look like they were handcrafted by a human designer who has shipped real products — NOT like generic AI output.

{'' if skip_pdf else PDF_CONSTRAINTS}

---

## CRAFT RULES (quality gates — apply these strictly)

{craft}

---

## DESIGN SYSTEM (use these EXACT colors, fonts, spacing — do NOT invent tokens)

{design_system}

---

## SKILL (follow this workflow precisely)

{skill}

---

## USER BRIEF

{brief}

{kwargs.get('context', '')}

---

## FINAL INSTRUCTIONS

1. Use ONLY hex colors from the Design System above. Never use default AI colors (#6366f1, #4f46e5, purple-blue gradients).
2. Never use emoji as icons — use text labels or CSS-drawn shapes.
3. Charts must be inline SVG (polyline/rect), not JS libraries.
4. Generate realistic, specific data — not "Metric A", "Feature 1".
5. Maximum 2 uses of accent color per visible screen/slide.
6. ALL CAPS text must have letter-spacing: 0.06em minimum.
7. Display text (32px+) must have negative letter-spacing (-0.01em to -0.03em).
8. Limit body text width to ~65 characters.
9. Self-check: would a human designer at Linear/Stripe/Vercel ship this? If not, refine.

OUTPUT: Return ONLY the complete HTML starting with <!DOCTYPE html>. No markdown fences. No explanation."""

    return prompt
