# Social Media Post

Generate a social media post graphic as a standalone HTML file.

## Output Format
- Single HTML file rendering a square (1080x1080px) or platform-specific canvas
- The design is the post itself — will be exported as PDF/screenshot
- Center the canvas on page with a subtle shadow to show boundaries

## Platform Sizes
- Instagram: 1080x1080px (square) or 1080x1350px (portrait)
- Twitter/X: 1200x675px (landscape)
- LinkedIn: 1200x627px (landscape)

## Design Structure
1. **Background** — Bold gradient, solid color, or pattern
2. **Main Text** — Large, impactful headline (2-5 words max per line)
3. **Supporting Text** — Subtitle or context (optional, smaller)
4. **Brand Mark** — Logo text or handle in corner
5. **Visual Elements** — CSS shapes, borders, decorative elements

## Design Rules
- Maximum 3 colors from the design system palette
- Text should be readable at small sizes (phone screen)
- High contrast between text and background
- Bold/black font weight for headlines
- Use CSS text-shadow for depth if needed
- Center-aligned layout
- The canvas div should have exact pixel dimensions with overflow hidden
