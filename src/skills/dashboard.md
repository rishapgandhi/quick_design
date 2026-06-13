# Dashboard

Generate an analytics/admin dashboard as a standalone HTML file.

## Output Format
- Single HTML file with a sidebar + main content layout
- Use float-based layout (sidebar fixed width, main fluid)
- For PDF: use `page-break-after: always` if content overflows one page

## Layout Structure
1. **Sidebar** — Nav items with emoji icons, app name at top
2. **Header** — Page title, date range, user avatar placeholder
3. **KPI Cards Row** — 3-4 metric cards (number, label, trend arrow)
4. **Charts Section** — Placeholder chart visualizations using CSS (bar charts with div heights, or table-based data)
5. **Table** — Recent activity or data table with 5-8 rows

## Design Rules
- Sidebar: 240px width, dark background
- KPI cards: white/light background, subtle shadow, colored accent borders
- Use CSS-only bar charts (colored divs with percentage heights)
- Table: alternating row colors, clean borders
- Responsive feel but optimized for desktop/PDF viewing
- Typography: data numbers 32-48px bold, labels 14-16px
