import json
import os
import sys
import re
import shutil
import struct


def copy_skill_assets(skill_dir, output_path):
    source_assets_dir = os.path.join(skill_dir, "assets")
    if not os.path.isdir(source_assets_dir):
        raise FileNotFoundError(f"Missing bundled assets directory: {source_assets_dir}")

    output_dir = os.path.dirname(os.path.abspath(output_path)) or os.getcwd()
    target_assets_dir = os.path.join(output_dir, "assets")
    os.makedirs(output_dir, exist_ok=True)
    shutil.copytree(
        source_assets_dir,
        target_assets_dir,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(".DS_Store"),
    )


def read_png_size(handle):
    handle.seek(16)
    return struct.unpack(">II", handle.read(8))


def read_gif_size(handle):
    handle.seek(6)
    return struct.unpack("<HH", handle.read(4))


def read_jpeg_size(handle):
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
        if marker in {b"\xc0", b"\xc1", b"\xc2", b"\xc3", b"\xc5", b"\xc6", b"\xc7", b"\xc9", b"\xca", b"\xcb", b"\xcd", b"\xce", b"\xcf"}:
            handle.read(3)
            height, width = struct.unpack(">HH", handle.read(4))
            return width, height
        segment_length_data = handle.read(2)
        if len(segment_length_data) != 2:
            break
        segment_length = struct.unpack(">H", segment_length_data)[0]
        handle.seek(segment_length - 2, os.SEEK_CUR)
    raise ValueError("Unsupported JPEG structure")


def read_image_size(path):
    with open(path, "rb") as handle:
        signature = handle.read(12)
        if signature.startswith(b"\x89PNG\r\n\x1a\n"):
            return read_png_size(handle)
        if signature[:6] in {b"GIF87a", b"GIF89a"}:
            return read_gif_size(handle)
        if signature.startswith(b"\xff\xd8"):
            return read_jpeg_size(handle)
    raise ValueError(f"Unsupported image format: {path}")


def resolve_image_path(src, data_path, output_path):
    if not src or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", src):
        return None
    if os.path.isabs(src):
        return src if os.path.exists(src) else None

    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(data_path)), src),
        os.path.join(os.path.dirname(os.path.abspath(output_path)), src),
        os.path.abspath(src),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return None


def classify_image(src, data_path, output_path):
    path = resolve_image_path(src, data_path, output_path)
    if not path:
        return {"image_readability_class": "", "image_aspect_ratio": ""}
    try:
        width, height = read_image_size(path)
    except Exception:
        return {"image_readability_class": "", "image_aspect_ratio": ""}

    if height == 0:
        return {"image_readability_class": "", "image_aspect_ratio": ""}

    ratio = width / height
    if ratio >= 2.5:
        image_class = "image-readable-single image-ultra-wide"
    elif ratio >= 1.8:
        image_class = "image-readable-single image-wide"
    elif ratio <= 0.75:
        image_class = "image-readable-single image-tall"
    else:
        image_class = "image-standard"

    return {
        "image_width": width,
        "image_height": height,
        "image_aspect_ratio": f"{ratio:.2f}",
        "image_readability_class": image_class,
    }


def enrich_image_metadata(data, data_path, output_path):
    readable_images = []

    def enrich_field(src_key, prefix=""):
        src = data.get(src_key)
        metadata = classify_image(src, data_path, output_path)
        for key, value in metadata.items():
            data[f"{prefix}{key}"] = value
            if prefix and key.startswith("image_"):
                data[f"{prefix}{key[len('image_'):]}"] = value
        if "image-readable-single" in metadata.get("image_readability_class", ""):
            readable_images.append(src)

    if "image_src" in data:
        enrich_field("image_src")
    for index in (1, 2):
        key = f"image_{index}_src"
        if key in data:
            enrich_field(key, f"image_{index}_")

    for item in data.get("items", []):
        if not isinstance(item, dict) or "image_src" not in item:
            continue
        metadata = classify_image(item.get("image_src"), data_path, output_path)
        item.update(metadata)
        if "image-readable-single" in metadata.get("image_readability_class", ""):
            readable_images.append(item.get("image_src"))

    single_image_layouts = {"centered-image", "image-top-text-bottom"}
    if (
        data.get("slide_mode") == "16x9"
        and len(readable_images) > 0
        and data.get("layout") not in single_image_layouts
    ):
        data["readability_warning"] = (
            "16:9 readable chart detected. Use one wide/tall chart per slide "
            f"for: {', '.join(filter(None, readable_images))}"
        )
    else:
        data["readability_warning"] = ""


def normalize_agenda_active_item(data):
    if data.get("layout") != "agenda":
        return

    items = data.get("items", [])
    if not isinstance(items, list) or not items:
        return

    active_row_idx = None

    active_index_raw = data.get("active_index")
    active_index = None
    if isinstance(active_index_raw, int):
        active_index = active_index_raw
    elif isinstance(active_index_raw, str) and active_index_raw.strip().isdigit():
        active_index = int(active_index_raw.strip())

    if isinstance(active_index, int) and 1 <= active_index <= len(items):
        active_row_idx = active_index - 1

    if active_row_idx is None:
        active_number_raw = data.get("active_number", "")
        active_number = str(active_number_raw).strip() if active_number_raw is not None else ""
        if active_number:
            for idx, item in enumerate(items):
                if not isinstance(item, dict):
                    continue
                if str(item.get("number", "")).strip() == active_number:
                    active_row_idx = idx
                    break

    if active_row_idx is None:
        for idx, item in enumerate(items):
            if isinstance(item, dict) and bool(item.get("active", False)):
                active_row_idx = idx
                break

    if active_row_idx is None:
        active_row_idx = 0

    for idx, item in enumerate(items):
        if isinstance(item, dict):
            item["active"] = idx == active_row_idx

def process_template(template, data):
    # Handle nested {{#each}} and {{#if}} using a stack-based approach
    def coerce_scalar(value):
        if value is None:
            return ""
        if isinstance(value, (dict, list, tuple, set)):
            return ""
        return str(value)
    
    def get_closing_tag(text, start_tag, end_tag):
        depth = 0
        pos = 0
        while pos < len(text):
            if text[pos:].startswith(start_tag):
                depth += 1
                pos += len(start_tag)
            elif text[pos:].startswith(end_tag):
                depth -= 1
                if depth == 0:
                    return pos
                pos += len(end_tag)
            else:
                pos += 1
        return -1

    # Process {{#each}}
    while "{{#each" in template:
        match = re.search(r'{{#each\s+([\w_]+)}}', template)
        if not match: break
        
        start_index = match.start()
        content_start = match.end()
        
        # Find matching {{/each}}
        remaining = template[start_index:]
        closing_relative = get_closing_tag(remaining, "{{#each", "{{/each}}")
        if closing_relative == -1: break
        
        closing_index = start_index + closing_relative
        
        list_name = match.group(1)
        item_template = template[content_start:closing_index]
        
        items = []
        if list_name == "this" and isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get(list_name, [])
        
        processed_items = ""
        if isinstance(items, list):
            for item in items:
                processed_items += process_template(item_template, item)
        
        template = template[:start_index] + processed_items + template[closing_index + 9:]

    # Process {{#if}}
    while "{{#if" in template:
        match = re.search(r'{{#if\s+([\w_]+)}}', template)
        if not match: break
        
        start_index = match.start()
        content_start = match.end()
        
        remaining = template[start_index:]
        closing_relative = get_closing_tag(remaining, "{{#if", "{{/if}}")
        if closing_relative == -1: break
        
        closing_index = start_index + closing_relative
        
        condition = match.group(1)
        content = template[content_start:closing_index]
        
        val = False
        if isinstance(data, dict):
            val = data.get(condition)
        
        processed_content = ""
        if val:
            processed_content = process_template(content, data)
        
        template = template[:start_index] + processed_content + template[closing_index + 7:]

    # Handle variables
    if isinstance(data, dict):
        for key, value in data.items():
            str_val = coerce_scalar(value)
            template = template.replace(f"{{{{{{ {key} }}}}}}", str_val)
            template = template.replace(f"{{{{{{{key}}}}}}}", str_val)
            template = template.replace(f"{{{{ {key} }}}}", str_val)
            template = template.replace(f"{{{{{key}}}}}", str_val)
    else:
        str_val = coerce_scalar(data)
        template = template.replace("{{this}}", str_val)
        template = template.replace("{{ this }}", str_val)
        template = template.replace("{{{this}}}", str_val)
        template = template.replace("{{{ this }}}", str_val)

    # Remove any unresolved simple placeholders to avoid leaking template tokens
    template = re.sub(r"{{{?\s*[\w_]+\s*}?}}", "", template)

    return template

def generate_slide(data_path, master_template_path, output_path):
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        enrich_image_metadata(data, data_path, output_path)
        normalize_agenda_active_item(data)
        body_classes = data.get("body_class", "")
        normalized_mode = str(data.get("slide_mode", "")).strip().lower()
        is_16x9 = normalized_mode in {"16x9", "16:9", "16-9"}
        legacy_mode_class = "mode-16x9" in body_classes.split()
        if is_16x9 or legacy_mode_class:
            body_classes = f"{body_classes} slide-16x9".strip()
        data["body_class"] = " ".join(dict.fromkeys(body_classes.split()))

        with open(master_template_path, 'r', encoding='utf-8') as f:
            master_html = f.read()

        layout_name = data.get("layout", "text-only")
        show_header = data.get("show_header")
        if show_header is None:
            show_header = layout_name not in {"agenda"}
        data["show_header"] = bool(show_header)
        if not data["show_header"]:
            body_classes = f"{body_classes} slide-no-header".strip()
            data["body_class"] = " ".join(dict.fromkeys(body_classes.split()))

        base_dir = os.path.dirname(os.path.abspath(master_template_path))
        layout_path = os.path.join(base_dir, "layouts", f"{layout_name}.html")

        if not os.path.exists(layout_path):
            print(f"Error: Layout '{layout_name}' not found at {layout_path}")
            return

        with open(layout_path, 'r', encoding='utf-8') as f:
            layout_template = f.read()
        
        layout_content = process_template(layout_template, data)
        final_html = master_html.replace("{{layout_content}}", layout_content)
        final_html = process_template(final_html, data)

        copy_skill_assets(base_dir, output_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Slide generated: {output_path} (Layout: {layout_name})")
        print(f"Assets copied: {os.path.join(os.path.dirname(os.path.abspath(output_path)), 'assets')}")
        if data.get("readability_warning"):
            print(f"Warning: {data['readability_warning']}")
    except Exception as e:
        print(f"Error generating slide: {e}")

# ---------------------------------------------------------------------------
# section-divider
# ---------------------------------------------------------------------------
def render_section_divider(data: dict) -> str:
    """
    JSON fields:
      title          (str, required)  – tên phần / chương
      subtitle       (str, optional)  – mô tả phụ hoặc tên tiếng Anh
      section_number (str, optional)  – số chương, ví dụ "01", "02"
      tags           (list, optional) – danh sách thẻ tag nhỏ
    """
    section_number = data.get("section_number", "")
    title = data.get("title", "")
    subtitle = data.get("subtitle", "")
    tags = data.get("tags", [])
 
    number_html = ""
    if section_number:
        number_html = f'<div class="sd-big-number">{section_number}</div>'
 
    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<p class="sd-subtitle">{subtitle}</p>'
 
    tags_html = ""
    if tags:
        tag_items = "".join(f'<span class="sd-tag">{t}</span>' for t in tags)
        tags_html = f'<div class="sd-tag-row">{tag_items}</div>'
 
    return f"""<div class="layout-section-divider">
  <div class="sd-accent-bar"></div>
  <div class="sd-content">
    {number_html}
    <div class="sd-title-block">
      <h1 class="sd-title">{title}</h1>
      {subtitle_html}
    </div>
    {tags_html}
  </div>
</div>"""
 
 
# ---------------------------------------------------------------------------
# agenda
# ---------------------------------------------------------------------------
def render_agenda(data: dict) -> str:
    """
    JSON fields:
      title    (str, required)   – tiêu đề cột trái, ví dụ "Chương trình buổi họp"
      subtitle (str, optional)   – ngày / tên sự kiện
      eyebrow  (str, optional)   – nhãn nhỏ trên tiêu đề, ví dụ "Nội dung trình bày"
      items    (list, required)  – danh sách mục agenda
        Mỗi item:
          number  (str)           – số thứ tự, ví dụ "1", "2"
          title   (str)           – tên mục
          time    (str, optional) – khung giờ, ví dụ "09:00 – 09:30"
          active  (bool, optional)– true = đánh dấu mục đang diễn ra
    """
    eyebrow = data.get("eyebrow", "")
    title = data.get("title", "")
    subtitle = data.get("subtitle", "")
    items = data.get("items", [])
 
    eyebrow_html = ""
    if eyebrow:
        eyebrow_html = f'<div class="ag-eyebrow">{eyebrow}</div>'
 
    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<p class="ag-meta">{subtitle}</p>'
 
    # Resolve a single active agenda row with the following priority:
    # 1) active_index (1-based)
    # 2) active_number (matches item.number)
    # 3) first item that has active=true
    # 4) fallback to the first row
    active_row_idx = None

    active_index = data.get("active_index")
    if isinstance(active_index, int) and 1 <= active_index <= len(items):
        active_row_idx = active_index - 1

    if active_row_idx is None:
        active_number_raw = data.get("active_number", "")
        active_number = str(active_number_raw).strip() if active_number_raw is not None else ""
        if active_number:
            for idx, item in enumerate(items):
                if str(item.get("number", "")).strip() == active_number:
                    active_row_idx = idx
                    break

    if active_row_idx is None:
        for idx, item in enumerate(items):
            if bool(item.get("active", False)):
                active_row_idx = idx
                break

    if active_row_idx is None and items:
        active_row_idx = 0

    items_html_parts = []
    for idx, item in enumerate(items):
        num = item.get("number", "")
        item_title = item.get("title", "")
        time_str = item.get("time", "")
        active = idx == active_row_idx
        active_class = " ag-item--active" if active else ""
 
        time_html = f'<div class="ag-item-time">{time_str}</div>' if time_str else ""
 
        items_html_parts.append(f"""    <div class="ag-item{active_class}">
      <div class="ag-num">{num}</div>
      <div class="ag-item-body">
        <div class="ag-item-title">{item_title}</div>
        {time_html}
      </div>
    </div>""")
 
    items_html = "\n".join(items_html_parts)
 
    return f"""<div class="layout-agenda">
  <div class="ag-left">
    {eyebrow_html}
    <h1 class="ag-heading">{title}</h1>
    {subtitle_html}
  </div>
  <div class="ag-items">
{items_html}
  </div>
</div>"""

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generator.py <data.json> <template.html> <output.html>")
    else:
        generate_slide(sys.argv[1], sys.argv[2], sys.argv[3])
