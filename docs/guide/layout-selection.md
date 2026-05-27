# Layout Selection Guide

Use this guide before writing slide JSON.
Primary rule: **message fit first, variety second**.

## Decision Matrix

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
| `org-hierarchy`         | Organization/team hierarchy with reporting lines     | Deep KPI trend analysis or process timeline                |
| `background-overlay`    | Need high-impact visual atmosphere behind insights  | Dense tables or long text-heavy explanations               |
| `appendix-technical`    | Technical appendix, IOC flow, deep-dive checklist   | High-level intro or executive summary                      |
| `grid`                  | 2x2 or 3x3 visual cards, portfolio snapshots        | No useful images; strict sequence needed                   |
| `centered-image`        | One diagram/screenshot is the main message          | Multiple visuals are equally important                     |
| `two-horizontal-images` | Direct side-by-side visual comparison               | One image only, or 3+ images                               |
| `image-text-split`      | One visual + one explanatory narrative              | Multiple independent concepts                              |
| `image-top-text-bottom` | Hero visual then interpretation/context             | Dense data requiring scan efficiency                       |

## Variety Policy

- 6-12 slides: aim for 4-6 layout types.
- 13+ slides: aim for 6+ layout types.
- Do not overuse `icon-text-grid`, `data-table` (normally max 2 per 10 slides).
- `section-divider` has no hard cap; use it whenever a real section boundary improves structure.
- Repetition is allowed if it improves comprehension.

## Repetition Rule (Soft)

- Default: avoid consecutive identical layouts.
- Exception: allow when continuity/readability is stronger (for example, phased timeline).
- If repeating, change at least one of: content density, visual emphasis, interaction pattern.

## Quick Layout Selection Heuristic

1. Time/sequence -> `timeline`.
2. Two-way contrast -> `comparison` or `two-horizontal-images`.
3. Structured numeric values -> `data-table`, `kpi-grid`, `bar-insight`, `chart-analysis`, `chart-pie`, or `gantt`.
4. Single proof visual -> `centered-image` or `image-top-text-bottom`.
5. High-impact narrative with image atmosphere -> `background-overlay`.
6. Concept explanation -> `text-only`, `image-text-split`, or `icon-text-grid`.
7. Technical deep detail -> `appendix-technical`.

## Image Availability Strategy (Required)

1. Audit available images before choosing layouts (`user images` + `./assets/background_picture/*`).
2. If usable images = `0`, avoid image-heavy layouts and prioritize low-image layouts.
3. If usable images = `1-2`, allow only single-image layouts and avoid `two-horizontal-images` and image-heavy `grid`.
4. If usable images `>=3`, all layouts are allowed.
5. If assigned image reduces readability or overlaps content, switch to a lower-image layout.

## Image Shape Mapping (Required)

1. Prefer `image-text-split` as the default when a slide needs both image + explanation text.
2. Use `image-top-text-bottom` only when image is not extreme in shape and has enough vertical room.
3. If image is wide (`aspect_ratio >= 1.8`), ultra-wide (`>= 2.5`), or tall (`<= 0.75`), avoid `image-top-text-bottom`.
4. For wide/ultra-wide/tall images, preserve readability first:
   - prioritize `centered-image` or `image-top-text-bottom` with text block removed.
   - do not force side/bottom text blocks that over-shrink the image.
5. If image is standard (`0.75 < aspect_ratio < 1.8`), `image-top-text-bottom` is allowed.
6. If ambiguous, fallback in order:
   - `centered-image`
   - `image-text-split`
   - `image-top-text-bottom`.

## Pre-generation Checklist

1. Draft full slide outline with message + layout per slide.
2. Check semantic fit first (`why this layout for this message`).
3. Check sequence rhythm and avoid unnecessary consecutive duplicates.
4. Verify variety target for deck length.
5. Final pass: do not choose a layout only for variety if it hurts clarity.

## Avoid

- Do not repeat the same layout for more than two consecutive slides.
- Do not use `text-only` when a source visual provides stronger evidence.
- Do not ship low-contrast text/icons against background.
- Do not allow overflow/clipping in `slide_mode: "16x9"`.
- Do not leave placeholders (`lorem`, `xxxx`, `TBD`).
- Do not overload a single `data-table`; split if scan speed drops.
- Do not force image-heavy layouts when image inventory is insufficient.
- Do not keep random backgrounds if readability is degraded.

## Layout Options by Message Type

- Sequence/process flow: `timeline`; fallback `agenda` for meeting/program format.
- Two-way contrast: `comparison` or `two-horizontal-images`.
- KPI summary + segmented breakdown: `chart-analysis`, `bar-insight`, `chart-pie`; fallback `kpi-grid` or `data-table`.
- Multi-workstream plan over fixed periods: `gantt`; fallback `timeline` when dependencies are mostly sequential.
- Organization/team reporting structure: `org-hierarchy`.
- Single proof visual: `centered-image` or `image-top-text-bottom`.
- Parallel concepts at equal rank: `icon-text-grid` or `grid`.
- Low image inventory: prefer `comparison` over `two-horizontal-images`, and text/icon cards over image-based `grid`.

## Data Display Rules

- Keep one primary numeric message per slide.
- For `16:9`, keep tables compact (typically up to 6 rows x 5 columns per table).
- For `kpi-grid`, keep 3-6 KPIs per slide; split if more.
- For `chart-pie`, keep categories concise (typically 3-7 slices).
- For `gantt`, keep 4-8 rows and a clear fixed period scale (for example W1-W12).
- For chart slides, always include labels, units, and time context.
- For comparisons, keep units/scales/formatting consistent across both sides.
- Prefer large key-number callouts first, then supporting detail.

## Visual Polish

- Keep consistent typography scale (title, section header, body, caption).
- Keep spacing rhythm consistent (for example 24px or 32px system).
- Left-align body paragraphs/lists; reserve centered alignment for titles or short labels.
- Use one recurring visual motif across the deck.
- Keep icon style consistent per slide and use only `./assets/viettel-icon-v1/icons/` for bundled icons.
