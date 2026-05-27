# Viettel HTML Slide

Generate branded Viettel-style HTML slides from JSON data.

This skill contains a small Python generator, reusable HTML layout templates, Viettel brand assets, and the CSS theme needed to produce standalone HTML slide pages.

## What It Does

- Builds HTML slides from JSON input.
- Uses the bundled Viettel logo from `assets/viettel-logo.png`.
- Copies the `assets/` folder next to generated output.
- Supports free-scrolling pages and locked `16x9` slide mode.
- Adds image readability metadata for wide, ultra-wide, and tall local images.
- Supports 21 reusable layouts.

## Structure

```text
viettel-html-slide/
├── SKILL.md
├── README.md
├── README-vi.md
├── template.html
├── layouts/
├── scripts/
│   └── generator.py
└── assets/
    ├── slide-viettel-theme.css
    ├── viettel-logo.png
    └── fonts/
```

## Documentation Map

Read in this order for fastest onboarding:

1. `SKILL.md` — entrypoint, quick rules, layout catalog, workflow.
2. `docs/guide/layout-selection.md` — layout strategy, selection heuristics, quality rules.
3. `docs/guide/media-and-icons.md` — icon policy, fallback mapping, image handling/readability.
4. `docs/guide/deck-policy.md` — deck navigation rules and canonical reference deck policy.
5. `docs/layout-json/README.md` — JSON example index + naming convention.

Vietnamese references:

- `docs/vi/layout-selection.vi.md`
- `docs/vi/media-and-icons.vi.md`

## Requirements

- Python 3
- No external Python packages required

The generator uses only the Python standard library.

## Usage

### Source Visual Ingest (Recommended)

When users provide report files with visuals (`.pptx/.docx/.pdf/image`), extract and audit images first:

```bash
python3 scripts/ingest_assets.py --deck-dir preview/<deck-name> <source-file-1> [<source-file-2> ...]
```

Optional for PDF page previews:

```bash
python3 scripts/ingest_assets.py --deck-dir preview/<deck-name> --render-pdf-pages report.pdf
```

This produces:

- `preview/<deck-name>/assets/source_extracted/*`
- `preview/<deck-name>/assets/source-image-manifest.json`

Use `recommended_image_paths` from the manifest before fallback backgrounds.

### Use With Claude Code Or OpenClaw

When this folder is installed as a skill, users can ask the agent in plain language. The agent will read the content, create the needed JSON internally, run the generator, and return HTML slide files.

Simple prompt:

```text
Read my content in @file and use the viettel-html-slide skill to create slides for me.
```

More examples:

```text
Use viettel-html-slide to turn @proposal.md into a Viettel-style HTML slide deck.
```

```text
Use viettel-html-slide to create 5 slides from @raw-content.md.
Make them concise and suitable for executives.
```

```text
Use viettel-html-slide to create one 16:9 slide from this content:
<paste content here>
```

The agent should decide layouts automatically. Users only need to specify slide count, audience, tone, or format when those details matter.

### Manual Script Usage

Run from the skills directory:

```bash
python3 viettel-html-slide/scripts/generator.py input.json viettel-html-slide/template.html output.html
```

Example:

```bash
python3 viettel-html-slide/scripts/generator.py /tmp/slide.json viettel-html-slide/template.html /tmp/slide.html
```

The command writes:

- `/tmp/slide.html`
- `/tmp/assets/` copied from `viettel-html-slide/assets/`

## Minimal Input

```json
{
  "title": "Platform Overview",
  "subtitle": "Architecture and delivery model",
  "layout": "text-only",
  "copy": "Short summary of the slide.",
  "html_content": "<p>Detailed HTML content.</p>"
}
```

## Common Fields

- `title`: slide title
- `subtitle`: optional slide subtitle
- `layout`: layout template name
- `slide_mode`: optional, use `"16x9"` for locked presentation mode
- `body_class`: optional extra CSS class on `<body>`

## Layouts

Supported layouts:

- `two-horizontal-images`
- `centered-image`
- `image-text-split`
- `image-top-text-bottom`
- `data-table`
- `text-only`
- `comparison`
- `timeline`
- `grid`
- `icon-text-grid`
- `highlight`
- `section-divider`
- `agenda`
- `chart-analysis`
- `bar-insight`
- `chart-pie`
- `gantt`
- `background-overlay`
- `appendix-technical`
- `kpi-grid`
- `org-hierarchy`

## Layout Examples

### Text Only

```json
{
  "title": "Executive Summary",
  "subtitle": "Key points",
  "layout": "text-only",
  "eyebrow": "Summary",
  "copy": "Primary message.",
  "html_content": "<ul><li>Point one</li><li>Point two</li></ul>"
}
```

### Centered Image

```json
{
  "title": "System Architecture",
  "subtitle": "High-level view",
  "layout": "centered-image",
  "image_src": "./assets/web-app-architecture-diagram.png",
  "image_alt": "Architecture diagram",
  "slide_mode": "16x9"
}
```

### Data Table

```json
{
  "title": "Performance Metrics",
  "subtitle": "Current baseline",
  "layout": "data-table",
  "headers": ["Metric", "Value", "Status"],
  "rows": [
    ["Latency", "100ms", "OK"],
    ["Availability", "99.9%", "OK"]
  ]
}
```

### Timeline

```json
{
  "title": "Delivery Roadmap",
  "layout": "timelinev2",
  "events": [
    {
      "date": "Q1 2026",
      "title": "Planning",
      "copy": "Define scope and architecture."
    },
    {
      "date": "Q2 2026",
      "title": "Launch",
      "copy": "Release production version."
    }
  ]
}
```

## Brand Rules

- Use the bundled real Viettel logo: `assets/viettel-logo.png`.
- Do not recreate the logo with text, CSS, SVG, initials, or placeholders.
- Keep the logo markup in `template.html` unless a replacement brand asset is explicitly provided.
- Keep slide and page backgrounds plain white by default, except `background-overlay`.
- Use `assets/slide-viettel-theme.css` as the canonical theme file.

## Image Readability

For local PNG, JPEG, and GIF files, the generator reads image dimensions and classifies images:

- Aspect ratio `>= 1.8`: wide readable image
- Aspect ratio `>= 2.5`: ultra-wide readable image
- Aspect ratio `<= 0.75`: tall readable image

In `16x9` mode, wide or tall charts should usually be placed one per slide. Multi-image layouts with readable charts produce a warning so content is not silently shrunk until labels are unreadable.

## Output Notes

- Generated HTML links to `./assets/slide-viettel-theme.css`.
- The generator copies the whole bundled `assets/` directory beside the output file.
- Relative image paths are resolved from the JSON file directory, output directory, or current working directory.
- Unknown layouts are rejected with an error message.

## Validation

Check Python syntax:

```bash
python3 -m py_compile viettel-html-slide/scripts/generator.py
python3 -m py_compile scripts/ingest_assets.py
```

Generate a smoke-test slide:

```bash
python3 viettel-html-slide/scripts/generator.py /tmp/slide.json viettel-html-slide/template.html /tmp/slide.html
```
