#!/usr/bin/env python3
"""
Extract and audit visual assets from user-provided report files.

Supported inputs:
- .pptx, .docx: extract images from zip media folders
- .pdf: extract embedded images (pdfimages) and optional page renders (pdftoppm)
- image files: copy directly

Outputs (inside deck assets):
- assets/source_extracted/*
- assets/source-image-manifest.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable


IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def slugify(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", text.strip().lower())
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "asset"


def command_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run_command(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(args, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def sha1_file(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def read_png_size(handle) -> tuple[int, int]:
    handle.seek(16)
    return struct.unpack(">II", handle.read(8))


def read_gif_size(handle) -> tuple[int, int]:
    handle.seek(6)
    return struct.unpack("<HH", handle.read(4))


def read_jpeg_size(handle) -> tuple[int, int]:
    handle.seek(2)
    while True:
        marker_start = handle.read(1)
        if not marker_start:
            break
        if marker_start != b"\xff":
            continue
        marker = handle.read(1)
        while marker == b"\xff":
            marker = handle.read(1)
        if marker in {
            b"\xc0",
            b"\xc1",
            b"\xc2",
            b"\xc3",
            b"\xc5",
            b"\xc6",
            b"\xc7",
            b"\xc9",
            b"\xca",
            b"\xcb",
            b"\xcd",
            b"\xce",
            b"\xcf",
        }:
            handle.read(3)
            height, width = struct.unpack(">HH", handle.read(4))
            return width, height
        segment_length_data = handle.read(2)
        if len(segment_length_data) != 2:
            break
        segment_length = struct.unpack(">H", segment_length_data)[0]
        handle.seek(segment_length - 2, os.SEEK_CUR)
    raise ValueError("Unsupported JPEG structure")


def read_bmp_size(handle) -> tuple[int, int]:
    handle.seek(18)
    width = struct.unpack("<I", handle.read(4))[0]
    height = struct.unpack("<I", handle.read(4))[0]
    return width, abs(height)


def read_webp_size(handle) -> tuple[int, int]:
    handle.seek(0)
    data = handle.read(30)
    if len(data) < 16 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError("Unsupported WEBP format")
    chunk = data[12:16]
    if chunk == b"VP8X":
        handle.seek(24)
        raw = handle.read(6)
        width = 1 + int.from_bytes(raw[0:3], "little")
        height = 1 + int.from_bytes(raw[3:6], "little")
        return width, height
    if chunk == b"VP8 ":
        handle.seek(26)
        width, height = struct.unpack("<HH", handle.read(4))
        return width & 0x3FFF, height & 0x3FFF
    if chunk == b"VP8L":
        handle.seek(21)
        b1, b2, b3, b4 = handle.read(4)
        width = 1 + (((b2 & 0x3F) << 8) | b1)
        height = 1 + (((b4 & 0x0F) << 10) | (b3 << 2) | ((b2 & 0xC0) >> 6))
        return width, height
    raise ValueError("Unsupported WEBP chunk")


def read_image_size(path: Path) -> tuple[int | None, int | None]:
    try:
        with path.open("rb") as fh:
            signature = fh.read(12)
            if signature.startswith(b"\x89PNG\r\n\x1a\n"):
                return read_png_size(fh)
            if signature[:6] in {b"GIF87a", b"GIF89a"}:
                return read_gif_size(fh)
            if signature.startswith(b"\xff\xd8"):
                return read_jpeg_size(fh)
            if signature.startswith(b"BM"):
                return read_bmp_size(fh)
            if signature.startswith(b"RIFF") and signature[8:12] == b"WEBP":
                return read_webp_size(fh)
    except Exception:
        return None, None
    return None, None


def quality_score(width: int | None, height: int | None, name: str) -> tuple[int, str]:
    if not width or not height:
        return 0, "unknown"

    pixels = width * height
    ratio = width / height if height else 0
    score = 0

    if pixels >= 4_000_000:
        score += 50
    elif pixels >= 2_000_000:
        score += 40
    elif pixels >= 1_000_000:
        score += 30
    elif pixels >= 500_000:
        score += 18
    else:
        score += 6

    if 1.2 <= ratio <= 2.3:
        score += 10
    elif ratio >= 2.3:
        score += 7
    elif ratio <= 0.75:
        score += 5

    if min(width, height) < 500:
        score -= 15
    if min(width, height) < 320:
        score -= 20

    text = name.lower()
    if any(k in text for k in ("chart", "graph", "dashboard", "report", "diagram", "architecture")):
        score += 8
    if any(k in text for k in ("icon", "logo", "avatar", "thumb")):
        score -= 10

    if score >= 55:
        band = "high"
    elif score >= 20:
        band = "medium"
    else:
        band = "low"
    return max(score, 0), band


def classify_aspect(width: int | None, height: int | None) -> str:
    if not width or not height:
        return "unknown"
    ratio = width / height
    if ratio >= 2.5:
        return "ultra-wide"
    if ratio >= 1.8:
        return "wide"
    if ratio <= 0.75:
        return "tall"
    return "standard"


def suggest_tags(name: str) -> list[str]:
    text = name.lower()
    tags = []
    mapping = {
        "chart": "chart",
        "graph": "chart",
        "dashboard": "dashboard",
        "diagram": "diagram",
        "architecture": "architecture",
        "network": "network",
        "security": "security",
        "attack": "security",
        "threat": "security",
        "revenue": "business",
        "growth": "business",
        "kpi": "kpi",
        "ddos": "security",
    }
    for key, value in mapping.items():
        if key in text and value not in tags:
            tags.append(value)
    return tags[:4]


def extract_zip_media(src_file: Path, out_dir: Path, member_prefix: str, source_kind: str) -> list[dict]:
    records: list[dict] = []
    with zipfile.ZipFile(src_file, "r") as zf:
        for member in zf.namelist():
            lower = member.lower()
            suffix = Path(lower).suffix
            if not lower.startswith(member_prefix) or suffix not in IMAGE_EXTENSIONS:
                continue
            target_name = slugify(f"{src_file.stem}-{Path(member).name}")
            target = out_dir / target_name
            with zf.open(member, "r") as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            records.append(
                {
                    "path": target,
                    "origin_kind": source_kind,
                    "origin_source": str(src_file),
                    "origin_member": member,
                }
            )
    return records


def extract_pdf_media(src_file: Path, out_dir: Path, render_pages: bool) -> tuple[list[dict], list[str]]:
    records: list[dict] = []
    notes: list[str] = []

    if command_exists("pdfimages"):
        prefix = out_dir / slugify(f"{src_file.stem}-embedded")
        code, _, err = run_command(["pdfimages", "-all", str(src_file), str(prefix)])
        if code == 0:
            for p in sorted(out_dir.glob(f"{prefix.name}-*")):
                if p.suffix.lower() in IMAGE_EXTENSIONS:
                    records.append(
                        {
                            "path": p,
                            "origin_kind": "pdf-embedded",
                            "origin_source": str(src_file),
                            "origin_member": p.name,
                        }
                    )
        else:
            notes.append(f"pdfimages failed for {src_file.name}: {err or 'unknown error'}")
    else:
        notes.append("pdfimages not found; skip embedded-image extraction for PDF")

    if render_pages:
        if command_exists("pdftoppm"):
            prefix = out_dir / slugify(f"{src_file.stem}-page")
            code, _, err = run_command(["pdftoppm", "-jpeg", "-r", "150", str(src_file), str(prefix)])
            if code == 0:
                for p in sorted(out_dir.glob(f"{prefix.name}-*.jpg")):
                    records.append(
                        {
                            "path": p,
                            "origin_kind": "pdf-page-render",
                            "origin_source": str(src_file),
                            "origin_member": p.name,
                        }
                    )
            else:
                notes.append(f"pdftoppm failed for {src_file.name}: {err or 'unknown error'}")
        else:
            notes.append("pdftoppm not found; skip PDF page render extraction")

    return records, notes


def collect_from_source(src_file: Path, temp_dir: Path, render_pdf_pages: bool) -> tuple[list[dict], list[str]]:
    suffix = src_file.suffix.lower()
    notes: list[str] = []
    records: list[dict] = []

    if suffix in {".pptx", ".pptm"}:
        records.extend(extract_zip_media(src_file, temp_dir, "ppt/media/", "pptx-media"))
    elif suffix in {".docx", ".docm"}:
        records.extend(extract_zip_media(src_file, temp_dir, "word/media/", "docx-media"))
    elif suffix == ".pdf":
        pdf_records, pdf_notes = extract_pdf_media(src_file, temp_dir, render_pdf_pages)
        records.extend(pdf_records)
        notes.extend(pdf_notes)
    elif suffix in IMAGE_EXTENSIONS:
        target = temp_dir / slugify(src_file.name)
        shutil.copy2(src_file, target)
        records.append(
            {
                "path": target,
                "origin_kind": "image-file",
                "origin_source": str(src_file),
                "origin_member": src_file.name,
            }
        )
    else:
        notes.append(f"Unsupported source type: {src_file.name}")

    return records, notes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract and audit report images for a deck.")
    parser.add_argument("inputs", nargs="+", help="Input files (.pptx/.docx/.pdf/image)")
    parser.add_argument("--deck-dir", required=True, help="Deck directory, e.g. preview/my-deck")
    parser.add_argument(
        "--target-subdir",
        default="assets/source_extracted",
        help="Output subdirectory inside deck-dir",
    )
    parser.add_argument(
        "--manifest-name",
        default="source-image-manifest.json",
        help="Manifest filename inside deck assets",
    )
    parser.add_argument(
        "--render-pdf-pages",
        action="store_true",
        help="Also render each PDF page to JPEG (requires pdftoppm)",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=20,
        help="Recommended image threshold (default: 20)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    deck_dir = Path(args.deck_dir).resolve()
    if not deck_dir.exists():
        print(f"Error: deck directory not found: {deck_dir}", file=sys.stderr)
        return 1

    target_dir = (deck_dir / args.target_subdir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = (deck_dir / "assets").resolve()
    assets_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = assets_dir / args.manifest_name

    source_paths: list[Path] = []
    for item in args.inputs:
        p = Path(item).expanduser().resolve()
        if not p.exists():
            print(f"Warning: input not found, skip: {item}")
            continue
        source_paths.append(p)

    if not source_paths:
        print("Error: no valid input files", file=sys.stderr)
        return 1

    extracted: list[dict] = []
    notes: list[str] = []
    with tempfile.TemporaryDirectory(prefix="ingest-assets-") as tmp:
        tmp_dir = Path(tmp)
        for src_file in source_paths:
            try:
                records, local_notes = collect_from_source(src_file, tmp_dir, args.render_pdf_pages)
                extracted.extend(records)
                notes.extend(local_notes)
            except Exception as exc:
                notes.append(f"Failed to process {src_file.name}: {exc}")

        dedupe: dict[str, dict] = {}
        kept: list[dict] = []
        for rec in extracted:
            p = rec["path"]
            file_hash = sha1_file(p)
            if file_hash in dedupe:
                continue
            dedupe[file_hash] = rec
            kept.append({**rec, "hash": file_hash})

        manifest_images: list[dict] = []
        for idx, rec in enumerate(sorted(kept, key=lambda x: x["path"].name), start=1):
            src_path: Path = rec["path"]
            ext = src_path.suffix.lower()
            file_name = f"{idx:03d}-{slugify(src_path.stem)}{ext}"
            dst_path = target_dir / file_name
            shutil.copy2(src_path, dst_path)

            width, height = read_image_size(dst_path)
            ratio = round((width / height), 3) if width and height else None
            pixels = (width * height) if width and height else None
            score, quality = quality_score(width, height, file_name)

            rel_path = dst_path.relative_to(deck_dir).as_posix()
            manifest_images.append(
                {
                    "id": idx,
                    "relative_path": f"./{rel_path}",
                    "file_name": file_name,
                    "origin_kind": rec["origin_kind"],
                    "origin_source": rec["origin_source"],
                    "origin_member": rec["origin_member"],
                    "hash_sha1": rec["hash"],
                    "width": width,
                    "height": height,
                    "aspect_ratio": ratio,
                    "aspect_class": classify_aspect(width, height),
                    "pixels": pixels,
                    "score": score,
                    "quality_band": quality,
                    "recommended": score >= args.min_score,
                    "tags": suggest_tags(file_name),
                }
            )

    manifest_images.sort(
        key=lambda x: (
            0 if x["recommended"] else 1,
            -x["score"],
            -(x["pixels"] or 0),
            x["id"],
        )
    )
    for new_id, item in enumerate(manifest_images, start=1):
        item["id"] = new_id

    summary = {
        "input_files": len(source_paths),
        "extracted_raw": len(extracted),
        "kept_unique": len(manifest_images),
        "recommended_count": sum(1 for x in manifest_images if x["recommended"]),
        "high_quality_count": sum(1 for x in manifest_images if x["quality_band"] == "high"),
        "medium_quality_count": sum(1 for x in manifest_images if x["quality_band"] == "medium"),
        "low_quality_count": sum(1 for x in manifest_images if x["quality_band"] == "low"),
    }

    manifest = {
        "generated_at_utc": utc_now(),
        "deck_dir": str(deck_dir),
        "target_dir": str(target_dir),
        "source_files": [str(p) for p in source_paths],
        "summary": summary,
        "notes": notes,
        "recommended_image_paths": [x["relative_path"] for x in manifest_images if x["recommended"]][:24],
        "images": manifest_images,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Ingest completed: {manifest_path}")
    print(f"- Raw extracted: {summary['extracted_raw']}")
    print(f"- Unique images: {summary['kept_unique']}")
    print(f"- Recommended (score>={args.min_score}): {summary['recommended_count']}")
    if notes:
        print("- Notes:")
        for msg in notes:
            print(f"  - {msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
