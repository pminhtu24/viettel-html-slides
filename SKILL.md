---
name: viettel-html-slide
description: Generate HTML slides following the Viettel slide theme from JSON data. Supports 13 modular layouts.
---

# Viettel HTML Slide Skill

This skill automates the generation of HTML slides based on the Viettel slide theme. It uses a master template and populates it with layout-specific components.

## Capabilities

- Generate consistent HTML slides from JSON data.
- Support for **13 modular layouts**:
  - Two horizontal images
  - One large centered image
  - Image + Text (horizontal)
  - Image top, Text below
  - Data table
  - Text only (with HTML support)
  - Comparison (Before/After)
  - Timeline/Process Flow
  - Image Grid (2x2 or 3x3)
  - Icon + Text Grid
  - Quote/Highlight Number
  - Section Divider
  - Agenda

## Layout Decision Guide

Use this guide to pick the right layout before writing any JSON. **Vary layouts across a deck** — using the same layout repeatedly makes slides feel repetitive and flat.

| Layout | When to use | When NOT to use |
|--------|------------|-----------------|
| `section-divider` | Major deck sections / chapter transitions | As a content slide |
| `agenda` | Opening slide listing topics or agenda items | Mid-deck content; needs ≥3 items to look good |
| `timeline` | Sequential evolution, phased roadmap, chronological steps | When order doesn't matter; items are equal-rank |
| `highlight` | One big number / key stat to punch in | Multiple metrics; detailed content |
| `comparison` | Problem vs solution, before vs after, two approaches side-by-side | More than 2 sides; list-only content |
| `data-table` | Structured numeric/text data, benchmarks, structured lists | Narrative prose; single idea |
| `text-only` | Structured prose, concept explanation, detailed bullets | When a table or timeline fits better |
| `icon-text-grid` | 3–4 parallel concepts with visual icons (overview cards) | When order/sequence matters; when data is structured |
| `grid` | 2×2 or 3×3 image+text cards | No images available; ordered/side-by-side content |
| `centered-image` | Single diagram, screenshot, architecture visual | Multiple images; no image provided |
| `two-horizontal-images` | Two diagrams side-by-side, before/after visuals | Single image; more than 2 images |
| `image-text-split` | One image with a paragraph alongside | Multiple concepts; no image |
| `image-top-text-bottom` | Image as hero with explanation below | Tight data; multiple independent concepts |

**Deck layout variety rule:** In a deck of N slides, aim to use at least 5–6 different layout types. If you find yourself reaching for `icon-text-grid` more than twice, stop and ask: could `timeline`, `comparison`, or `data-table` communicate this content better?

**⚠️ Strict no-consecutive-repetition rule:** Two slides back-to-back must never share the same layout type. This applies to _all_ layouts — not just `icon-text-grid`. For example, two `timeline` slides in a row is just as flat as two `icon-text-grid` in a row. Before finalizing a deck, run through the layout sequence and confirm no two adjacent slides repeat the same layout. If the content naturally flows as a timeline, break it up with a `comparison` or `data-table` or `text-only` slide between consecutive timeline blocks.

**Layout sequence checklist (do this before generating any slide):**
1. Draft the full slide list with layout types before writing any JSON.
2. Scan for consecutive duplicates — if found, swap one to a different layout type.
3. Aim for at least 5–6 distinct layout types across a 10-slide deck.
4. Reserve `icon-text-grid` for the final summary/conclusion slide or when no other layout fits better.

## Agent Workflow From User Prompt

1. Read the user's natural-language slide request.
2. Select the most suitable built-in layout using the guide above. **Deliberately vary layouts** across slides.
3. Convert the request into JSON data for that layout.
4. Save the JSON input file near the intended output.
5. Run `python3 scripts/generator.py <input.json> template.html <output.html>` from this skill directory.
6. Return the generated HTML path and a short summary of the chosen layout.

For a deck, create one JSON file and one HTML output per slide, then merge into a single scrollable deck (see Deck Building below).

Example user prompts:

- "Read @file and use viettel-html-slide to create slides for me."
- "Use viettel-html-slide to turn @proposal.md into a Viettel-style HTML deck."
- "Use viettel-html-slide to create one 16:9 slide from this content: ..."

## Brand Requirements

- Always use the real Viettel logo asset: `./assets/viettel-logo.png`.
- Do not recreate the logo with text, initials, CSS circles, SVG marks, emoji, or placeholder lockups.
- Keep the logo markup from `template.html` unless the user explicitly provides a replacement approved brand asset.
- Generated slide outputs must include/copy the `assets/` directory next to the HTML file, or the logo path must be adjusted so `viettel-logo.png` resolves correctly.

## Layout Positioning

- The main slide content region uses `--slide-content-offset-x: -170px` and `--slide-content-offset-y: -115px` for 16:9 decks.
- This intentionally moves `h1.slide-title`, subtitle, and the body content left and up while keeping the logo and slide status fixed.
- Default output is a free-scrolling page for long content; do not split long content with forced page breaks.
- Set `"slide_mode": "16x9"` in input JSON only for presentation slides that should lock to one viewport and use left/right navigation instead of vertical scrolling.
- `metric-card` panels have no red left edge and use three rounded corners with a square bottom-left corner.
- Page and slide backgrounds must stay plain white; do not add pink/red gradient, halo, or tinted page backgrounds.

## Image Readability Rules

- The generator reads local PNG, JPEG, and GIF image dimensions with the bundled Python script; do not require external imaging packages.
- In `"slide_mode": "16x9"`, images with aspect ratio `>= 1.8` are treated as wide readable charts and should occupy one slide.
- Images with aspect ratio `>= 2.5` are treated as ultra-wide charts and should use the largest single-image scale.
- Images with aspect ratio `<= 0.75` are treated as tall readable charts and should occupy one slide or be split vertically.
- Multi-image layouts that contain wide/tall readable charts must be split by the caller/deck builder into one image per slide; the generator emits a warning instead of silently shrinking charts until labels are unreadable.
- Single-image layouts add readability classes automatically so CSS can scale charts larger in 16:9 mode.

## Data Structure

The skill uses a `layout` field to determine which template to use. Common fields across all layouts:

- `title`: Slide Title
- `subtitle`: Slide Subtitle (Optional)
- `layout`: Name of the layout (see below)
- `slide_mode`: Optional. Use `"16x9"` to lock a slide to a 16:9 presentation viewport.

Slide numbering must be shown only through the deck navigation status, for example `<span id="deck-status">01 / 16</span>`. Place `.deck-control` at the bottom right. Keep navigation status text-only: no previous/next buttons, red circular controls, bordered pills, or standalone slide-number elements such as `#deck-slide-number` or `.slide-number`.

### 1. two-horizontal-images

```json
{
  "layout": "two-horizontal-images",
  "image_1_src": "./assets/img1.png",
  "image_1_alt": "Alt 1",
  "image_2_src": "./assets/img2.png",
  "image_2_alt": "Alt 2"
}
```

### 2. centered-image

```json
{
  "layout": "centered-image",
  "image_src": "./assets/img.png",
  "image_alt": "Description"
}
```

### 3. image-text-split

```json
{
  "layout": "image-text-split",
  "image_src": "./assets/img.png",
  "eyebrow": "Label",
  "title": "Main Heading",
  "copy": "Primary description",
  "additional_text": "Supporting details"
}
```

### 4. image-top-text-bottom

```json
{
  "layout": "image-top-text-bottom",
  "image_src": "./assets/img.png",
  "title": "Section Title",
  "copy": "Detailed explanation text below the image."
}
```

### 5. data-table

```json
{
  "layout": "data-table",
  "headers": ["Metric", "Value", "Status"],
  "rows": [
    ["Speed", "100ms", "OK"],
    ["Cost", "$1.2", "High"]
  ]
}
```

### 6. text-only

```json
{
  "layout": "text-only",
  "eyebrow": "Note",
  "title": "Announcement",
  "copy": "Short summary",
  "html_content": "<p>Detailed <b>HTML</b> content goes here.</p><ul><li>List item</li></ul>"
}
```

### 7. comparison

```json
{
  "layout": "comparison",
  "side_1_title": "Before",
  "side_1_items": ["Old process", "Manual entry"],
  "side_2_title": "After",
  "side_2_items": ["Automated system", "Real-time sync"]
}
```

### 8. timeline

```json
{
  "layout": "timeline",
  "events": [
    {
      "date": "Q1 2026",
      "title": "Planning",
      "copy": "Defined scope and goals."
    },
    {
      "date": "Q2 2026",
      "title": "Alpha",
      "copy": "Initial prototype release."
    }
  ]
}
```

### 9. grid

```json
{
  "layout": "grid",
  "columns": 2,
  "rows": 2,
  "items": [
    { "image_src": "img1.png", "title": "Item 1", "copy": "Desc 1" },
    { "title": "Item 2 (No image)", "copy": "Desc 2" }
  ]
}
```

### 10. icon-text-grid

```json
{
  "layout": "icon-text-grid",
  "items": [
    {
      "icon_svg": "<svg>...</svg>",
      "title": "Speed",
      "copy": "Extremely fast."
    },
    {
      "icon_svg": "<svg>...</svg>",
      "title": "Secure",
      "copy": "End-to-end encryption."
    }
  ]
}
```

### 11. highlight

```json
{
  "layout": "highlight",
  "number": "99%",
  "quote": "The highest reliability in the industry.",
  "caption": "Verified by third-party audit."
}
```

### 12. section-divider

Used to separate major sections in a deck, serving as divider slides between chapters.

```json
{
  "layout": "section-divider",
  "title": "Business Strategy",
  "subtitle": "Phần 2 — Strategic Business Direction",
  "section_number": "02",
  "tags": ["2026 Plan", "International Market", "Innovation"],
  "slide_mode": "16x9"
}
```

Fields:

- `title` (str, required) — section or chapter title
- `subtitle` (str, optional) — supporting description, often the English name of the section
- `section_number` (str, optional) — chapter number as a string, for example `"01"`, `"02"`; displayed as a large faded label behind the title
- `tags` (list of str, optional) — list of small tags shown below the title

---

### 13. agenda

Used for meeting agenda slides or presentation outlines. Left column: title + event name. Right column: numbered agenda items with time slots and a highlight for the active item.

```json
{
  "layout": "agenda",
  "eyebrow": "Presentation Content",
  "title": "Meeting Agenda",
  "subtitle": "Executive Committee Meeting · 21/05/2025",
  "items": [
    {
      "number": "1",
      "title": "Opening and Introductions",
      "time": "09:00 – 09:10"
    },
    {
      "number": "2",
      "title": "Q3 2025 Results Report",
      "time": "09:10 – 09:40"
    },
    {
      "number": "3",
      "title": "5G Strategy — 2026 Roadmap",
      "time": "09:40 – 10:20",
      "active": true
    },
    { "number": "4", "title": "Discussion and Q&A", "time": "10:20 – 11:00" }
  ],
  "slide_mode": "16x9"
}
```

Fields:

- `title` (str, required) — left-column title, for example `"Meeting Agenda"`
- `eyebrow` (str, optional) — small label above the title, for example `"Presentation Content"`
- `subtitle` (str, optional) — event name or date/time
- `items` (list, required) — list of agenda items; each item includes:
  - `number` (str) — item number
  - `title` (str) — item title
  - `time` (str, optional) — time slot, for example `"09:00 – 09:10"`
  - `active` (bool, optional) — set `true` to highlight the current item; only one item should be active

## Workflow

1. Read the `template.html` and the corresponding file in `layouts/`.
2. Map the data to placeholders in both files.
3. Handle loops (`#each`) for tables, timelines, and grids.
4. Inject the layout HTML into the master template's `{{layout_content}}`.
5. Copy the bundled `assets/` directory into the output HTML folder.
6. Write the final HTML to a new file.

## Templates

- Master: `./template.html`
- Layouts: `./layouts/*.html`
- Styles: Uses `./assets/slide-viettel-theme.css`
- Brand logo: Uses the bundled `./assets/viettel-logo.png`; never recreate the logo in HTML/CSS.
