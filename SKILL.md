---
name: viettel-html-slide
description: Generate HTML slides following the Viettel slide theme from JSON data. Supports 17 modular layouts.
---

# Viettel HTML Slide Skill

This skill automates the generation of HTML slides based on the Viettel slide theme. It uses a master template and populates it with layout-specific components.

## Capabilities

- Generate consistent HTML slides from JSON data.
- Extract embedded images/diagrams from source documents (for example `.docx`, `.pptx`, `.pdf`) and map them into slide assets when visuals are relevant.
- Support for **17 modular layouts**:
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
  - Chart + Analysis
  - Bar + Insight
  - Background Image Overlay
  - Appendix / Technical

## Layout Decision Guide

Use this guide to choose layout before writing JSON.
Primary rule: **message fit first, variety second**.
A layout is correct when it makes the core message easier to understand in under 5 seconds.

| Layout                  | Use when                                            | Usually avoid when                              |
| ----------------------- | --------------------------------------------------- | ----------------------------------------------- |
| `section-divider`       | Starting a new section/chapter                      | Main content needs depth                        |
| `agenda`                | Opening slide with 3+ agenda items                  | Mid-deck detail slides                          |
| `timeline`              | Sequence, phases, milestones, causality over time   | Order does not matter                           |
| `highlight`             | One key KPI/stat to emphasize                       | Comparing many metrics                          |
| `comparison`            | Two clear alternatives (before/after, A vs B)       | More than 2 dimensions                          |
| `data-table`            | Structured values/benchmarks matrix                 | Narrative or single-point message               |
| `text-only`             | Concept explanation, policy, dense structured prose | Visual evidence is available and more effective |
| `icon-text-grid`        | 3-4 parallel concepts at equal rank                 | Time sequence or metric-heavy data              |
| `chart-analysis`        | KPI summary + chart breakdown on one slide          | Narrative-only content without numeric evidence |
| `bar-insight`           | Quarterly KPI bars + executive quick-read panel     | High-cardinality data needing full table detail |
| `background-overlay`    | Need high-impact visual atmosphere behind insights  | Dense tables or long text-heavy explanations    |
| `appendix-technical`    | Technical appendix, IOC flow, deep-dive checklist   | High-level intro or executive summary           |
| `grid`                  | 2x2 or 3x3 visual cards, portfolio snapshots        | No useful images; strict sequence needed        |
| `centered-image`        | One diagram/screenshot is the main message          | Multiple visuals are equally important          |
| `two-horizontal-images` | Direct side-by-side visual comparison               | One image only, or 3+ images                    |
| `image-text-split`      | One visual + one explanatory narrative              | Multiple independent concepts                   |
| `image-top-text-bottom` | Hero visual then interpretation/context             | Dense data requiring scan efficiency            |

**Layout variety policy:**

- 6-12 slides: aim for 4-6 layout types.
- 13+ slides: aim for 6+ layout types.
- Do not overuse `icon-text-grid` (normally max 2 per 10 slides).
- Repetition is allowed if it improves comprehension.

**Repetition rule (soft, with exceptions):**

- Default: avoid consecutive identical layouts.
- Exception is allowed when continuity/readability is stronger (for example, phased timeline).
- If repeating a layout, change rhythm by at least one: content density, visual emphasis (image-led vs text-led), or interaction pattern (compare vs explain).

**Layout selection heuristic (quick order):**

1. If the slide is mainly time/sequence, use `timeline`.
2. If the slide is mainly two-way contrast, use `comparison` or `two-horizontal-images`.
3. If the slide is mainly structured values, use `data-table`,`bar-insight` or `chart-analysis`.
4. If the slide is mainly a single proof visual, use `centered-image` or `image-top-text-bottom`.
5. If the slide needs high-impact narrative over imagery, use `background-overlay`.
6. If the slide is mainly concept explanation, use `text-only`, `image-text-split`, or `icon-text-grid`.
7. If the slide is technical detail, use `appendix-technical`.

**Pre-generation checklist:**

1. Draft the full slide outline with message + layout for each slide.
2. Check semantic fit first (`why this layout for this message`).
3. Check sequence rhythm; avoid unnecessary consecutive duplicates.
4. Verify variety target is met for deck length.
5. Final pass: do not choose a layout only for variety if it hurts clarity.

## Avoid (Common Mistakes)

- Do not repeat the same layout for more than two consecutive slides unless sequence continuity requires it.
- Do not use `text-only` when a source visual provides stronger evidence.
- Do not ship low-contrast text or icons against the background.
- Do not allow text overflow or clipping in `"slide_mode": "16x9"`.
- Do not leave placeholder content in final output (for example `lorem`, `xxxx`, `TBD`).
- Do not overload a single `data-table`; if scan speed drops, split the content into multiple slides.

## Layout Options by Message Type

- Sequence or process flow: use `timeline`; fallback to `agenda` for meeting/program format.
- Two-way contrast: use `comparison` or `two-horizontal-images`.
- KPI summary plus segmented breakdown: use `chart-analysis` or `bar-insight`; fallback to `data-table`.
- Single proof visual: use `centered-image` or `image-top-text-bottom`.
- Parallel concepts at equal rank: use `icon-text-grid` or `grid`.

## Data Display Rules

- Keep one primary numeric message per slide.
- For 16:9 slides, keep tables compact (typically up to 6 rows x 5 columns per table).
- For chart slides, always provide labels, units, and time context.
- For comparisons, keep units, scales, and numeric formatting consistent across both sides.
- Prefer large key-number callouts first, then supporting detail.

## Visual Polish

- Keep a consistent typography scale across the deck (title, section header, body, caption).
- Keep spacing rhythm consistent between content blocks (for example 24px or 32px systems).
- Left-align body paragraphs and lists; reserve centered alignment for titles or short labels.
- Use one recurring visual motif across the deck (for example icon circles, card treatment, or border style).
- Keep icon style consistent per slide and use only `./assets/viettel-icon-v1/icons/` for bundled icons.

## Agent Workflow From User Prompt

1. Read the user's natural-language slide request.
2. If the user provides a source file, extract and collect reusable visuals (charts, diagrams, screenshots) into the output `assets/` folder first.
3. Select the most suitable built-in layout using the guide above. **Deliberately vary layouts** across slides.
4. Convert the request into JSON data for that layout, wiring extracted assets via `image_src` / `image_1_src` / `image_2_src` / grid item image fields.
5. Save the JSON input file near the intended output.
6. Run `python3 scripts/generator.py <input.json> template.html <output.html>` from this skill directory.
7. Return the generated HTML path and a short summary of the chosen layout.

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

## Source Image Extraction Rules

- When the source content includes embedded visuals, prefer reusing those original visuals instead of redrawing them manually.
- Extract source visuals into the deck-local `assets/` directory and reference them with relative paths (for example `./assets/semantic-router-pipeline.png`).
- Keep extracted filenames descriptive and stable so JSON/HTML mapping is easy to audit.
- If multiple visuals exist, map each visual to the slide whose message depends on that evidence (diagram-proof alignment first, decoration second).
- If a source visual is unreadable at slide scale, split into multiple slides or use a single-image layout with `slide_mode: "16x9"` before considering omission.

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

## Icon Asset Library

- Main icon library path: `./assets/viettel-icon-v1/icons/`
- Library browser page: `./assets/viettel-icon-v1/viettel-icon-library.html`
- Library docs: `./assets/viettel-icon-v1/README.md`
- Each icon is a standalone SVG with:
  - circular red/dark background
  - white foreground glyph
  - `viewBox="0 0 64 64"` for consistent scaling

When generating any layout that uses icons, always source icons from `./assets/viettel-icon-v1/icons/`.
Always verify the selected file exists before writing JSON/HTML.
Do not hand-draw new inline SVGs unless the requested icon does not exist in the library.

## Icon Usage Rules (Short)

- Prefer icon-enabled layouts when content has categorized concepts, drivers, steps, or tracks.
- Do not force icons into: `data-table`, `centered-image`, `two-horizontal-images`.
- Use only `./assets/viettel-icon-v1/icons/` for bundled icon assets.
- Keep icon density balanced: typically `3–8` icons per slide.
- Keep one consistent icon style per slide; avoid mixing styles.

## Icon Coverage Rules

- Deck-level coverage target:
  - `6-9` slides: at least `2` icon-enabled slides.
  - `10-15` slides: at least `3-5` icon-enabled slides.
  - `16+` slides: at least `25%-40%` icon-enabled slides.
- Prioritize icon-enabled layouts first when semantic fit is similar:
  - `icon-text-grid` for parallel concepts
  - `chart-analysis` for labeled categories/KPIs
  - `appendix-technical` for process/flow/risk steps
- For `icon-text-grid`, each item should include one icon (no empty icon slots).
- For `chart-analysis`, each bar should include `icon_src` when category labels are shown.
- For `appendix-technical`, each `attack_steps` item should include `icon_src` or `icon_svg`.

## Icon Fallback Mechanism

Use this fallback chain when an exact icon is not available.

1. Try exact semantic match from `./assets/viettel-icon-v1/icons/` (filename keyword match).
2. If no exact match, use domain fallback mapping:
   - growth/performance -> `chart-line.svg`
   - strategy/plan -> `strategy.svg`
   - security/risk -> `shield.svg`
   - cloud/platform -> `cloud.svg`
   - data/analytics -> `database.svg`
   - network/infrastructure -> `network.svg`
   - team/people -> `team.svg`
   - operations/process -> `settings.svg`
   - logistics/transport -> `truck-delivery.svg`
3. If mapped icon is missing, use the neutral default: `info.svg`.
4. Always verify every icon path exists before writing final JSON/HTML.
5. Never leave icon fields blank in icon-required blocks:
   - For `icon-text-grid`, fill `icon_svg` with an `<img>` tag pointing to a valid fallback icon path.
   - For `chart-analysis` and `appendix-technical`, fill `icon_src` with a valid fallback icon path.

### Icon Download from Trusted Sources

If an icon is not available in `./assets/viettel-icon-v1/icons/` and the fallback mapping above does not provide a suitable match, download from these trusted sources:

**Recommended Icon Libraries:**

- **Feather Icons** (https://feathericons.com) – minimal, clean, monochrome SVGs with 24x24 viewBox
- **Heroicons** (https://heroicons.com) – well-designed, multiple styles (outline, solid), 24x24 viewBox
- **FontAwesome** (https://fontawesome.com) – comprehensive, use solid SVGs only
- **Bootstrap Icons** (https://icons.getbootstrap.com) – clean, consistent, monochrome, 16x16 viewBox
- **Material Design Icons** (https://fonts.google.com/icons) – Google's official icons, various viewBox sizes

**Processing Downloaded Icons:**

1. Download the SVG file in monochrome or single-color format.
2. Open the SVG in a text editor and adjust the `viewBox` to `"0 0 64 64"` for consistency with existing icons.
3. If the icon uses a solid background (e.g., circle), wrap it in a `<g>` group within the SVG.
4. Place the processed SVG in `./assets/viettel-icon-v1/icons/` with a descriptive filename (e.g., `custom-security.svg`).
5. Update the relevant JSON or HTML to reference the new icon path.
6. Test the icon rendering before finalizing the slide output.

**Quality Checklist for Downloaded Icons:**

- SVG is monochrome (single color) or follows Viettel brand colors.
- `viewBox` is set correctly for consistent scaling.
- Icon is small enough to fit inside a 64x64 square without overflow.
- File size is under 5 KB (optimize using tools like https://svgomg.web.app if needed).

### Runtime Fallback (Deck Preview)

- In addition to data-time fallback, apply runtime fallback in deck preview pages.
- Add icon fallback binding in `preview/<deck-name>/index.html` after each iframe slide load:
  - listen to `frame.addEventListener("load", ...)`
  - find icon images under `img[src*="viettel-icon-v1/icons/"]`
  - attach `error` handler and swap to mapped similar icon.
- Keep fallback map semantic and deterministic (same broken icon -> same replacement icon).
- Use neutral safe default (`security.svg` or `info.svg`) when no mapped replacement exists.

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

---

### 14. chart-analysis

Used when one slide needs both quick KPI context and a chart breakdown by segment.

```json
{
  "layout": "chart-analysis",
  "title": "Regional Review",
  "subtitle": "North America performance snapshot",
  "metrics": [
    { "label": "Underlying Revenue", "value": "$15,694M", "value_class": "v1" },
    {
      "label": "Organic Revenue Growth",
      "value": "+7.7%",
      "value_class": "v2"
    },
    {
      "label": "Underlying Operating Profit",
      "value": "$1,290M",
      "value_class": "v3"
    },
    {
      "label": "Underlying Operating Margin",
      "value": "8.2%",
      "value_class": "v4"
    }
  ],
  "chart_title": "Regional Mix by Vertical",
  "chart_note": "Snapshot Q2/2026",
  "bars": [
    {
      "value": "32%",
      "pct": "86",
      "color": "#ff5a1f",
      "icon_src": "./assets/viettel-icon-v1/icons/briefcase.svg",
      "icon_alt": "Business icon",
      "label": "Business & Industry"
    }
  ],
  "slide_mode": "16x9"
}
```

Fields:

- `metrics` (list, required) — each item: `label`, `value`, optional `value_class` (for color tuning)
- `chart_title` (str, optional) — title above bars
- `chart_note` (str, optional) — sub-note above bars
- `bars` (list, required) — each bar: `value`, `pct` (`0-100`), `color`, `label`, and optional `icon_src`/`icon_svg`

---

### 15. background-overlay

Used for narrative insight slides with a background image plus a readability overlay.

```json
{
  "layout": "background-overlay",
  "title": "Tổng quan",
  "subtitle": "Xu hướng và cảnh báo",
  "background_image_src": "./assets/city-night.jpg",
  "background_image_alt": "Urban background",
  "overlay_title": "Tổng quan xu hướng và cảnh báo vận hành",
  "overlay_copy": "Mẫu phù hợp cho insight cấp chiến lược bám theo bối cảnh thị trường.",
  "focus_label": "FOCUS: Từ dữ liệu nền sang hành động ưu tiên",
  "insights": [
    {
      "title": "Gia tăng lừa đảo có mục tiêu",
      "copy": "Threat intelligence ghi nhận nhiều lỗ hổng theo ngành."
    },
    {
      "title": "Khuyến nghị triển khai",
      "copy": "Thiết lập playbook phản ứng nhanh và phân tầng IOC."
    }
  ],
  "slide_mode": "16x9"
}
```

Fields:

- `background_image_src` (str, required) — full background image path
- `overlay_title` (str, required) — main narrative heading on top of image
- `overlay_copy` (str, required) — short narrative text
- `focus_label` (str, optional) — highlighted focus line
- `insights` (list, required) — right-side insight cards (`title`, `copy`)

---

### 16. appendix-technical

Used for technical appendix pages with operation notes, attack flow, and quick detection signals.

```json
{
  "layout": "appendix-technical",
  "title": "Appendix",
  "subtitle": "Technical details",
  "appendix_eyebrow": "Phụ lục kỹ thuật APT TA-SC-33",
  "overview_title": "1. Tổng quan chiến dịch",
  "overview_copy": "TA-SC-33 sử dụng spear-phishing kết hợp C2 động để thu thập dữ liệu.",
  "overview_bullets": [
    "Phạm vi ảnh hưởng: VN, Lào, Thái Lan",
    "Tần suất IOC mới: 2-3 batch/ngày"
  ],
  "recommendations_title": "2. Khuyến nghị xử lý",
  "recommendation_bullets": [
    "Giám sát DNS bất thường",
    "Sandbox tệp macro trước khi mở"
  ],
  "tags": ["SOC", "Threat Intel", "CSIRT"],
  "attack_flow_title": "Chuỗi tấn công chính",
  "attack_steps": [
    {
      "icon_src": "./assets/viettel-icon-v1/icons/mail.svg",
      "icon_alt": "Mail icon",
      "title": "Spear Phishing"
    },
    {
      "icon_src": "./assets/viettel-icon-v1/icons/network.svg",
      "icon_alt": "Network icon",
      "title": "C2 Server"
    }
  ],
  "signals_title": "3. Dấu hiệu nhận biết nhanh",
  "quick_signals": [
    "Domain mới < 72h nhưng traffic tăng đột biến",
    "PowerShell chạy nền từ tệp Office macro"
  ],
  "slide_mode": "16x9"
}
```

Fields:

- `appendix_eyebrow` (str, optional) — top technical label
- `overview_title`, `overview_copy`, `overview_bullets` — left block, campaign summary
- `recommendations_title`, `recommendation_bullets`, `tags` — left block, recommendations
- `attack_flow_title`, `attack_steps` — right block, attack chain
- `signals_title`, `quick_signals` — right block, quick detection cues

## Workflow

1. Read the `template.html` and the corresponding file in `layouts/`.
2. Map the data to placeholders in both files.
3. Handle loops (`#each`) for tables, timelines, and grids.
4. Inject the layout HTML into the master template's `{{layout_content}}`.
5. Copy the bundled `assets/` directory into the output HTML folder.
6. If building a multi-slide preview deck (`preview/<deck-name>/index.html`), wire runtime icon fallback in iframe load handler.
7. Write the final HTML to a new file.

## Templates

- Master: `./template.html`
- Layouts: `./layouts/*.html`
- Styles: Uses `./assets/slide-viettel-theme.css`
- Brand logo: Uses the bundled `./assets/viettel-logo.png`; never recreate the logo in HTML/CSS.
