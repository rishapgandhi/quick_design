# Ferrari Automotive Branding

Generate a luxury automotive brand landing page using Ferrari's red-and-black cinematic design language. Apply to ANY car brand the user names.

## Output Format
- Single standalone HTML file, full-page scrolling website
- Dark dramatic aesthetic with red (#DA291C) and black gradients EVERYWHERE
- This is NOT subtle — red should be bold, visible, dramatic throughout

## EXACT CSS Patterns To Use (copy these directly)

### Background Classes (use these on sections)
```css
.bg-hero { background: linear-gradient(160deg, #1a0000 0%, #000000 40%, #1a0505 100%); }
.bg-red-dark { background: linear-gradient(180deg, #DA291C 0%, #8b0000 100%); }
.bg-black-red { background: linear-gradient(135deg, #0a0a0a 0%, #1a0505 50%, #2a0a0a 100%); }
.bg-deep { background: linear-gradient(180deg, #000000 0%, #120000 100%); }
.bg-red-subtle { background: linear-gradient(180deg, #1a0808 0%, #0a0a0a 100%); }
.bg-pure-red { background: #DA291C; }
```

### Red Glow Effects
```css
/* Behind logo/emblem */
box-shadow: 0 0 40px rgba(218,41,28,0.2);
/* Radial glow on hero */
background: radial-gradient(ellipse at center, rgba(218,41,28,0.08) 0%, transparent 60%);
/* Under car/product images */
background: radial-gradient(ellipse at center bottom, rgba(218,41,28,0.12) 0%, transparent 50%);
/* Red floor line */
background: linear-gradient(90deg, transparent, rgba(218,41,28,0.3), transparent);
```

### Red Divider Line
```css
.red-line { width: 60px; height: 3px; background: #DA291C; margin: 0 auto 24px auto; }
```

### Typography
- Font: 'Helvetica Neue', Arial, sans-serif
- h1: 60px, weight 600, letter-spacing -0.03em
- h2: 36px, weight 500
- Labels: 11px, uppercase, letter-spacing 1.2px, color rgba(255,255,255,0.5)
- Body: 15px, line-height 1.7, color rgba(255,255,255,0.6)

### Buttons (2px border-radius — razor sharp, no roundness)
- Primary: background #ffffff, color #000, uppercase, letter-spacing 1.5px
- Ghost: transparent, 1px solid rgba(255,255,255,0.4), white text
- Dark: background #000, color #fff (used on red backgrounds)

### Colors Quick Reference
- Red accent: #DA291C
- Dark red: #8b0000
- Black: #000000, #0a0a0a
- Red-tinted black: #1a0505, #2a0a0a, #120000
- Text primary: #ffffff
- Text muted: rgba(255,255,255,0.5)
- Text body: rgba(255,255,255,0.6)
- Borders: rgba(218,41,28,0.1) or rgba(255,255,255,0.05)
- Prices/highlights: #DA291C

## Page Section Structure (follow this EXACT order)

### 1. Fixed Nav
- Brand name in RED (#DA291C), uppercase, letter-spacing 3px
- 4 nav links, white, 12px
- Background: gradient fading from black to transparent

### 2. Hero (full viewport height)
- bg-hero background with radial red glow overlay
- Circular logo/emblem: 80px, 2px solid #DA291C border, red box-shadow glow
- Brand name inside logo or below it
- h1 headline (brand tagline)
- Subtitle in muted text
- White button CTA

### 3. Featured Vehicle Section
- bg-deep background
- "Now Introducing" label above
- Large showcase area with red ambient radial glow underneath
- Vehicle name as h2
- Description + ghost button

### 4. Vehicle Lineup (4 columns)
- bg-black-red background
- Red divider line at top center
- "The Collection" label
- 4 vehicles in table-cell columns, divided by rgba(218,41,28,0.1) borders
- Each: placeholder visual with red bottom glow, model name, category tag, PRICE IN RED

### 5. Stats Section (FULL RED GRADIENT BACKGROUND)
- bg-red-dark (this section MUST be full red — it's the dramatic centerpiece)
- 4 stat cells: large white numbers (52px), uppercase labels
- Divided by rgba(0,0,0,0.2) borders

### 6. Editorial Section A (story block)
- bg-red-subtle background
- 2-column: 55% image placeholder (with red ambient glow inside) + 45% text
- Label + red-line + h2 + body text + ghost button

### 7. Editorial Section B (story block)
- bg-deep background
- 2-column reversed: text on left, image on right
- Same pattern as above

### 8. Subscribe CTA (PURE SOLID RED background)
- bg-pure-red
- White heading, slightly transparent body text
- Dark button (black bg, white text)

### 9. Footer
- bg-deep, red top border (rgba(218,41,28,0.15))
- 4-column grid of links
- Section headings in RED (#DA291C)
- Links in rgba(255,255,255,0.5)
- Copyright line at bottom

## Content Rules
- Replace vehicle names with the user's brand models (research real models if possible)
- Use realistic Indian pricing in ₹ Lakh format if Indian brand
- Use real stats/achievements of the brand
- Generate a tagline that fits the brand personality
- NEVER use emoji — only text and CSS shapes
- ALL section borders/dividers use red tint not white
