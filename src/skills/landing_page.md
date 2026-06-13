# Landing Page

Generate a single-page marketing landing page as a standalone HTML file.

## Output Format
- Single HTML file, vertically scrolling
- Use `page-break-after: always` between major sections for PDF export
- Mobile-friendly layout using float/table-based CSS (no flexbox for PDF compat)

## Section Structure
1. **Hero** — Bold headline, subheadline, CTA button, gradient/pattern background
2. **Features** — 3-4 feature cards with emoji/CSS icons, short descriptions
3. **How It Works** — 3 numbered steps
4. **Social Proof** — Testimonial quotes or stats (use placeholder data if not provided)
5. **CTA** — Final call to action with button

## Design Rules
- Hero takes full viewport height
- Feature cards in 2x2 or 3-column grid (use float layout)
- Generous whitespace (padding 60-80px between sections)
- CTA buttons: rounded, contrasting color, large padding
- Typography: headings 36-56px, body 18-20px
- Use CSS gradients, shadows, borders for visual depth
