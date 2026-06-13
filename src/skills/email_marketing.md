# Email Marketing Template

Generate a branded email template as a standalone HTML file.

## Output Format
- Single HTML file using TABLE-based layout (email client compatible)
- Max width 600px, centered
- Inline styles on every element (email clients strip <style> tags)

## Section Structure
1. **Header** — Logo placeholder (styled text), brand color bar
2. **Hero** — Large image placeholder (colored div), headline
3. **Body** — 2-3 paragraphs of content with clear hierarchy
4. **CTA Button** — Table-based button (Outlook compatible pattern)
5. **Footer** — Unsubscribe link, company info, social icons (emoji)

## Design Rules
- 600px max width, centered with margin: 0 auto
- ALL styles must be inline (style="" attribute on every element)
- Use tables for layout (not div/float)
- Button: table > tr > td with background-color, padding, border-radius
- Font stack: Arial, Helvetica, sans-serif (email safe)
- Background: #f4f4f4 outer, #ffffff inner content
- Generous padding (20-40px) between sections
