---
name: viettel-html-slide
description: Generate Viettel-branded HTML slides from JSON with 21 modular layouts and offline assets.
---

# Viettel HTML Slide Skill

## Scope

- Generate consistent Viettel-style HTML slides from JSON data.
- Reuse source visuals (docx/pptx/pdf exports) when they improve evidence quality.
- Use offline-first assets (`./assets/*`).

## Core Rules

- Message fit first, variety second.
- Avoid unnecessary consecutive duplicate layouts.
- Do not use placeholder text (`lorem`, `TBD`, `xxxx`) in final output.
- In `slide_mode: "16x9"`, avoid overflow/clipping; split content into more slides if needed.
- Keep backgrounds plain white by default (no global page tint/gradient), except `background-overlay`.
- Always use real logo asset: `./assets/viettel-logo.png`.
- Always generate slides through the master template `./template.html`; do not bypass or replace template shell elements (logo/header/deck structure).
- For wide/tall chart-like images in `16x9`, prioritize readable single-image treatment.

## Layout Catalog (21)

1. `two-horizontal-images`
2. `centered-image`
3. `image-text-split`
4. `image-top-text-bottom`
5. `data-table`
6. `text-only`
7. `comparison`
8. `timeline`
9. `grid`
10. `icon-text-grid`
11. `highlight`
12. `section-divider`
13. `agenda`
14. `chart-analysis`
15. `bar-insight`
16. `chart-pie`
17. `gantt`
18. `background-overlay`
19. `appendix-technical`
20. `kpi-grid`
21. `org-hierarchy`

## Standard Workflow

1. Read user request and available source files.
2. If source files contain visuals, run ingest:
   - `python3 scripts/ingest_assets.py --deck-dir preview/<deck-name> <source-files...>`
3. Audit image inventory (`0`, `1-2`, `>=3` usable images) using:
   - `preview/<deck-name>/assets/source-image-manifest.json`
   - fallback pool `./assets/background_picture/*`
4. Must consult `./docs/guide/layout-selection.md` and `./docs/guide/media-and-icons.md`, then select layout per slide by semantic fit and image-availability rules.
5. Build JSON data per selected layout.
6. Generate slide HTML using the required master template:
   - `python3 scripts/generator.py <input.json> template.html <output.html>`
7. Ensure output has working `assets/` paths.
8. For preview decks (`preview/<deck-name>/index.html`), wire iframe icon runtime fallback.

## Reference Map

Use these references for detailed rules; keep this file as the quick operational entrypoint.
Before any layout selection or JSON authoring, agent must read:
- `./docs/guide/layout-selection.md`
- `./docs/guide/media-and-icons.md`

- Layout strategy and quality rules:
  - `./docs/guide/layout-selection.md`
- Icon policy and image handling:
  - `./docs/guide/media-and-icons.md`
- Deck navigation and canonical reference policy:
  - `./docs/guide/deck-policy.md`
- Layout JSON index and naming convention:
  - `./docs/layout-json/README.md`

## Templates and Assets

- Master template (required): `./template.html`
- Layout partials: `./layouts/*.html`
- Theme CSS: `./assets/slide-viettel-theme.css`
- Icon library browser: `./assets/viettel-icon-v1/viettel-icon-library.html`
- Icon library docs: `./assets/viettel-icon-v1/README.md`

## Quick Validation

- Syntax:
  - `python3 -m py_compile scripts/generator.py`
  - `python3 -m py_compile scripts/ingest_assets.py`
- Smoke generate:
  - `python3 scripts/generator.py docs/layout-json/21-org-hierarchy.json template.html preview/org-hierarchy-layout-demo/skill-smoke-org-hierarchy.html`
