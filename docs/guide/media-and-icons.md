# Media and Icons Guide

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

Before generating HTML, validate all `icon_src` paths in JSON.

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
- Use random fallback mainly for contextual/decorative visuals, not chart-evidence that requires readable labels.
- For `background-overlay`, if text contrast is poor after assignment, replace image or switch layout.

## Image Readability in `slide_mode: "16x9"`

- Wide chart: aspect ratio `>= 1.8` -> prefer single-image slide.
- Ultra-wide chart: aspect ratio `>= 2.5` -> largest single-image treatment.
- Tall chart: aspect ratio `<= 0.75` -> single-image slide or vertical split.
- Layout enforcement from image shape:
  - default image narrative layout: `image-text-split`.
  - `image-top-text-bottom` is only for standard images (not wide/ultra-wide/tall).
  - if image is wide/ultra-wide/tall, keep image dominant and remove/deprioritize extra text block.
- If chart labels become unreadable, split content into multiple slides.
