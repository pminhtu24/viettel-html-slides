---
name: viettel-html-slide
description: Generate Viettel-branded HTML slides from JSON with 20 modular layouts and offline assets.
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

## Layout Catalog (20)

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

## Layout Decision Guide

Use this guide to choose layout before writing JSON.
Primary rule: **message fit first, variety second**.

| Layout                  | Use when                                            | Usually avoid when                                         |
| ----------------------- | --------------------------------------------------- | ---------------------------------------------------------- |
| `section-divider`       | Starting a new section/chapter                      | Main content needs depth                                   |
| `agenda`                | Opening slide with 3+ agenda items                  | Mid-deck detail slides                                     |
| `timeline`              | Sequence, phases, milestones, causality over time   | Order does not matter                                      |
| `highlight`             | One key KPI/stat to emphasize                       | Comparing many metrics                                     |
| `comparison`            | Two clear alternatives (before/after, A vs B)       | More than 2 dimensions                                     |
| `data-table`            | Structured values/benchmarks matrix                 | Narrative or single-point message                          |
| `text-only`             | Concept explanation, policy, dense structured prose | Visual evidence is available and more effective            |
| `icon-text-grid`        | 3-4 parallel concepts at equal rank                 | Time sequence or metric-heavy data                         |
| `chart-analysis`        | KPI summary + chart breakdown on one slide          | Narrative-only content without numeric evidence            |
| `chart-pie`             | Share-of-total breakdown with clear category ratio  | Dense trend-over-time story or deep segmented drill-down   |
| `gantt`                 | Multi-workstream timeline across weeks/months       | Single KPI snapshot or category share-only message         |
| `kpi-grid`              | KPI snapshot with 3-6 peer metrics for fast scan    | Deep segment drill-down or long time-series trend analysis |
| `bar-insight`           | Quarterly KPI bars + executive quick-read panel     | High-cardinality data needing full table detail            |
| `background-overlay`    | Need high-impact visual atmosphere behind insights  | Dense tables or long text-heavy explanations               |
| `appendix-technical`    | Technical appendix, IOC flow, deep-dive checklist   | High-level intro or executive summary                      |
| `grid`                  | 2x2 or 3x3 visual cards, portfolio snapshots        | No useful images; strict sequence needed                   |
| `centered-image`        | One diagram/screenshot is the main message          | Multiple visuals are equally important                     |
| `two-horizontal-images` | Direct side-by-side visual comparison               | One image only, or 3+ images                               |
| `image-text-split`      | One visual + one explanatory narrative              | Multiple independent concepts                              |
| `image-top-text-bottom` | Hero visual then interpretation/context             | Dense data requiring scan efficiency                       |

**Layout variety policy:**

- 6-12 slides: aim for 4-6 layout types.
- 13+ slides: aim for 6+ layout types.
- Do not overuse `icon-text-grid`, `data-table` (normally max 2 per 10 slides).
- `section-divider` has no hard cap; use it whenever a real section boundary improves structure (often more than 2 in long decks).
- Repetition is allowed if it improves comprehension.

**Repetition rule (soft, with exceptions):**

- Default: avoid consecutive identical layouts.
- Exception is allowed when continuity/readability is stronger (for example, phased timeline).
- If repeating a layout, change rhythm by at least one: content density, visual emphasis (image-led vs text-led), or interaction pattern (compare vs explain).

**Layout selection heuristic (quick order):**

1. If the slide is mainly time/sequence, use `timeline`.
2. If the slide is mainly two-way contrast, use `comparison` or `two-horizontal-images`.
3. If the slide is mainly structured values, use `data-table`, `kpi-grid`, `bar-insight`, `chart-analysis`, `chart-pie`, or `gantt`.
4. If the slide is mainly a single proof visual, use `centered-image` or `image-top-text-bottom`.
5. If the slide needs high-impact narrative over imagery, use `background-overlay`.
6. If the slide is mainly concept explanation, use `text-only`, `image-text-split`, or `icon-text-grid`.
7. If the slide is technical detail, use `appendix-technical`.

**Image availability strategy (required):**

1. Audit available images before choosing layouts (`user images` + `./assets/background_picture/*`).
2. If usable images = `0`, avoid image-heavy layouts and prioritize low-image layouts.
3. If usable images = `1-2`, allow only single-image layouts and avoid `two-horizontal-images` and image-heavy `grid`.
4. If usable images `>=3`, all layouts are allowed.
5. If assigned image reduces readability or overlaps content, switch to a lower-image layout instead of forcing that image.

**Image shape to layout mapping (required):**

1. Prefer `image-text-split` as the default layout when a slide needs both image + explanation text.
2. Use `image-top-text-bottom` only when the image is not extreme in shape and has enough vertical room.
3. If image is wide (`aspect_ratio >= 1.8`), ultra-wide (`>= 2.5`), or tall (`<= 0.75`), avoid `image-top-text-bottom`.
4. For wide/ultra-wide/tall images, preserve image readability first:
   - prioritize single-image layouts: `centered-image` or `image-top-text-bottom` with text block removed.
   - do not force side/bottom text blocks that shrink the image too much.
5. If image is small/standard ratio (`0.75 < aspect_ratio < 1.8`), `image-top-text-bottom` is allowed.
6. If layout choice is ambiguous, choose readability-safe fallback in this order:
   - `centered-image` (image evidence first)
   - `image-text-split` (balanced narrative + image)
   - `image-top-text-bottom` (only for non-extreme images)

**Pre-generation checklist:**

1. Draft the full slide outline with message + layout for each slide.
2. Check semantic fit first (`why this layout for this message`).
3. Check sequence rhythm; avoid unnecessary consecutive duplicates.
4. Verify variety target is met for deck length.
5. Final pass: do not choose a layout only for variety if it hurts clarity.

## Avoid

- Do not repeat the same layout for more than two consecutive slides.
- Do not use `text-only` when a source visual provides stronger evidence.
- Do not ship low-contrast text or icons against the background.
- Do not allow text overflow or clipping in `"slide_mode": "16x9"`.
- Do not leave placeholder content in final output (for example `lorem`, `xxxx`, `TBD`).
- Do not overload a single `data-table`; if scan speed drops, split the content into multiple slides.
- Do not force `two-horizontal-images` or image-heavy `grid` when image inventory is insufficient.
- Do not keep random background images if text readability is degraded.

## Layout Options by Message Type

- Sequence or process flow: use `timeline`; fallback to `agenda` for meeting/program format.
- Two-way contrast: use `comparison` or `two-horizontal-images`.
- KPI summary plus segmented breakdown: use `chart-analysis`, `bar-insight`, or `chart-pie`; fallback to `kpi-grid` or `data-table`.
- Multi-workstream plan over fixed periods: use `gantt`; fallback to `timeline` when dependencies are mostly sequential.
- Single proof visual: use `centered-image` or `image-top-text-bottom`.
- Parallel concepts at equal rank: use `icon-text-grid` or `grid`.
- With low image inventory, prefer `comparison` over `two-horizontal-images`, and prefer text/icon cards over image-based `grid`.

## Data Display Rules

- Keep one primary numeric message per slide.
- For 16:9 slides, keep tables compact (typically up to 6 rows x 5 columns per table).
- For `kpi-grid`, keep 3-6 KPIs per slide; if more, split into multiple slides.
- For `chart-pie`, keep category count concise (typically 3-7 slices) to preserve label readability.
- For `gantt`, keep 4-8 rows and a clear fixed period scale (for example W1-W12) to preserve scan speed.
- For chart slides, always provide labels, units, and time context.
- For comparisons, keep units, scales, and numeric formatting consistent across both sides.
- Prefer large key-number callouts first, then supporting detail.

## Visual Polish

- Keep a consistent typography scale across the deck (title, section header, body, caption).
- Keep spacing rhythm consistent between content blocks (for example 24px or 32px systems).
- Left-align body paragraphs and lists; reserve centered alignment for titles or short labels.
- Use one recurring visual motif across the deck (for example icon circles, card treatment, or border style).
- Keep icon style consistent per slide and use only `./assets/viettel-icon-v1/icons/` for bundled icons.

## Icon Rules

- Prefer Viettel icons from `./assets/viettel-icon-v1/icons/*.svg`.
- Selection order: `Viettel > semantic fallback in Viettel set > optional external source > no emoji`.
- Rendering:
  - Viettel icons: local SVG files.
  - External icons: download and convert to SVG if possible, else use as-is.

## Icon Fallback Mapping

- growth/performance -> `chart-line.svg`
- strategy/plan -> `strategy.svg`
- security/risk -> `shield.svg`
- cloud/platform -> `cloud.svg`
- data/analytics -> `database.svg`
- network/infrastructure -> `network.svg`
- team/people -> `team.svg`
- operations/process -> `settings.svg`
- logistics/transport -> `truck-delivery.svg`
- default -> `info.svg`

Always verify icon file existence before writing final JSON/HTML.

## Icon Existence Check (Required)

Before generating HTML, validate that all `icon_src` paths in JSON exist.

- If file exists: keep it.
- If file is missing: choose replacement via `Icon Fallback Mapping`.
- If no semantic match: set `icon_src` to `./assets/viettel-icon-v1/icons/info.svg`.
- Re-run validation until zero missing icons.

## Image Handling Rules

- Extract and reuse source visuals into output `assets/` when available.
- Keep filenames descriptive and stable.
- If user provides source files with visuals (`pptx/docx/pdf/image`), run ingest first:
  - `python3 scripts/ingest_assets.py --deck-dir preview/<deck-name> <source-file-1> [<source-file-2> ...]`
  - Optional PDF page render: add `--render-pdf-pages`
  - Use generated manifest: `preview/<deck-name>/assets/source-image-manifest.json`
- Prioritize images from `./assets/source_extracted/*` (recommended images in manifest) before fallback pool.
- If source visuals are missing, use fallback images from `./assets/background_picture/*`.
- Random fallback is allowed for `image_src`, `image_1_src`, `image_2_src`, `background_image_src`.
- Use random fallback mainly for contextual/decorative visuals, not for chart-evidence that requires readable labels.
- For `background-overlay`, if text contrast is poor after assignment, replace image or switch layout.
- For `slide_mode: "16x9"` readability:
  - wide chart: aspect ratio `>= 1.8` -> prefer single-image slide.
  - ultra-wide chart: aspect ratio `>= 2.5` -> largest single-image treatment.
  - tall chart: aspect ratio `<= 0.75` -> single-image slide or vertical split.
- Layout enforcement from image shape:
  - default image narrative layout: `image-text-split`.
  - `image-top-text-bottom` is only for standard images (not wide/ultra-wide/tall).
  - if image is wide/ultra-wide/tall, keep image dominant and remove/deprioritize extra text block.
- If chart labels become unreadable, split into multiple slides.

## Deck and Navigation Rules

- Slide number must appear only in deck status text, e.g. `01 / 16`.
- Keep `.deck-control` at bottom-right.
- Do not add extra prev/next buttons, red circular controls, or standalone slide-number badges.

## Canonical Reference Deck Policy

Use `./preview/bao-cao-attt-from-textonly-skill/` as the canonical reference deck for future agents.

- One slide must use exactly one layout template (no mixed-layout slide composition).
- In the canonical reference deck, keep full layout coverage: each supported layout should appear at least once when deck length allows.
- `icon-text-grid` hard cap for the canonical reference deck: maximum 2 slides.
- Keep structure and visual rhythm aligned with the canonical folder: slide naming pattern, header hierarchy, spacing rhythm, logo placement, and deck navigation pattern.

## Standard Workflow

1. Read user request and available source files.
2. If source files contain visuals, run ingest:
   - `python3 scripts/ingest_assets.py --deck-dir preview/<deck-name> <source-files...>`
3. Audit image inventory (`0`, `1-2`, `>=3` usable images) using:
   - `preview/<deck-name>/assets/source-image-manifest.json`
   - fallback pool `./assets/background_picture/*`
4. Select layout per slide by semantic fit and image-availability rules.
5. Build JSON data per selected layout.
6. Generate slide HTML using:
   - `python3 scripts/generator.py <input.json> template.html <output.html>`
7. Ensure output has working `assets/` paths.
8. For preview decks (`preview/<deck-name>/index.html`), wire iframe icon runtime fallback.

## Templates and Assets

- Master template: `./template.html`
- Layouts: `./layouts/*.html`
- Theme CSS: `./assets/slide-viettel-theme.css`
- Icon library browser: `./assets/viettel-icon-v1/viettel-icon-library.html`
- Icon library docs: `./assets/viettel-icon-v1/README.md`

## JSON Examples

All layout JSON examples are moved to:

- `./docs/layout-json/01-two-horizontal-images.json`
- `./docs/layout-json/02-centered-image.json`
- `./docs/layout-json/03-image-text-split.json`
- `./docs/layout-json/04-image-top-text-bottom.json`
- `./docs/layout-json/05-data-table.json`
- `./docs/layout-json/06-text-only.json`
- `./docs/layout-json/07-comparison.json`
- `./docs/layout-json/08-timeline.json`
- `./docs/layout-json/09-grid.json`
- `./docs/layout-json/10-icon-text-grid.json`
- `./docs/layout-json/11-highlight.json`
- `./docs/layout-json/12-section-divider.json`
- `./docs/layout-json/13-agenda.json`
- `./docs/layout-json/14-chart-analysis.json`
- `./docs/layout-json/15-background-overlay.json`
- `./docs/layout-json/16-appendix-technical.json`
- `./docs/layout-json/17-kpi-grid.json`
- `./docs/layout-json/18-bar-insight.json`
- `./docs/layout-json/19-chart-pie.json`
- `./docs/layout-json/20-gantt.json`

Additional guide:

- Icon sourcing: `./docs/icon-sourcing.md`
