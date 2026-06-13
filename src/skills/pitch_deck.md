# Pitch Deck

Generate a multi-slide pitch deck as a single HTML file optimized for PDF export via wkhtmltopdf.

## CRITICAL PDF RULES (wkhtmltopdf compatibility)
- Do NOT use CSS variables (var(--xxx)) — use hardcoded values directly
- Do NOT use display: flex or display: grid — use display: table / table-cell for centering
- Do NOT use 100vh — use fixed height in mm or use page-break-after: always with auto height
- Do NOT use CSS gradients for backgrounds (wkhtmltopdf renders them poorly) — use solid colors
- Do NOT use box-shadow — use borders instead
- Do NOT use position: absolute for layout — only for small decorative elements
- Each slide should be a standalone block that fits on one A4 landscape page
- Use @page { size: landscape; margin: 0; } for proper orientation
- Font stacks must be system fonts only

## Output Format
- Single HTML file with a <style> block containing @page { size: A4 landscape; margin: 0; }
- Each slide is a <div> with: width: 297mm; height: 210mm; padding: 40mm; page-break-after: always;
- Text centering via: display: table; width: 100%; height: 100%; and inner div with display: table-cell; vertical-align: middle;
- Last slide has page-break-after: avoid;

## Slide Structure (default 5 slides)
1. **Title Slide** — Product name (large, bold), tagline, simple colored circle or square as logo
2. **Problem** — The pain point (3 bullet max, left-aligned)
3. **Solution** — How it solves it (short paragraph + 2-3 key points)
4. **Features** — 3-4 features with emoji bullets
5. **Call to Action** — Next steps, contact

## Design Rules
- Dark solid backgrounds (#0d0d0d or #1a1a2e) — NO gradients
- White text (#ffffff) for headings, light gray (#b0b0b0) for body
- ONE accent color for emphasis (use it on headings or keywords only)
- Font sizes: title 60px, headings 40px, body 22px
- Slide numbers: bottom-right, small text, gray
- Bullet points: colored bullet character, left-aligned text
- Keep it minimal — one idea per slide, lots of whitespace
