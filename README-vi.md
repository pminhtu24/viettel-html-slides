# Viettel HTML Slide

Tạo slide HTML theo phong cách Viettel từ dữ liệu JSON.

Skill này gồm generator Python nhỏ gọn, các template layout HTML tái sử dụng, asset thương hiệu Viettel, và file CSS theme để tạo các trang slide HTML độc lập.

## Chức Năng

- Tạo slide HTML từ input JSON.
- Dùng logo Viettel thật từ `assets/viettel-logo.png`.
- Copy thư mục `assets/` sang cạnh file output.
- Hỗ trợ trang cuộn tự do và chế độ slide cố định `16x9`.
- Tự bổ sung metadata đọc ảnh cho ảnh rộng, siêu rộng, và ảnh dọc.
- Hỗ trợ 20 layout tái sử dụng.

## Cấu Trúc

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

## Yêu Cầu

- Python 3
- Không cần package Python bên ngoài

Generator chỉ dùng thư viện chuẩn của Python.

## Cách Dùng

### Trích Xuất Ảnh Từ File Nguồn (Khuyến Nghị)

Khi người dùng cung cấp báo cáo có hình (`.pptx/.docx/.pdf/ảnh`), nên chạy ingest trước:

```bash
python3 scripts/ingest_assets.py --deck-dir preview/<ten-deck> <file-nguon-1> [<file-nguon-2> ...]
```

Tùy chọn render từng trang PDF:

```bash
python3 scripts/ingest_assets.py --deck-dir preview/<ten-deck> --render-pdf-pages report.pdf
```

Lệnh này tạo:

- `preview/<ten-deck>/assets/source_extracted/*`
- `preview/<ten-deck>/assets/source-image-manifest.json`

Ưu tiên dùng `recommended_image_paths` trong manifest trước khi fallback sang ảnh nền mặc định.

### Dùng Với Claude Code Hoặc OpenClaw

Khi thư mục này được cài như một skill, người dùng chỉ cần hỏi bằng ngôn ngữ tự nhiên. Agent sẽ đọc nội dung, tự tạo JSON cần thiết, chạy generator, rồi trả về file HTML slide.

Prompt đơn giản:

```text
Đọc nội dung của tôi trong @file và sử dụng skill viettel-html-slide để tạo slide cho tôi.
```

Ví dụ khác:

```text
Dùng viettel-html-slide để chuyển @proposal.md thành một deck HTML theo style Viettel.
```

```text
Dùng viettel-html-slide tạo 5 slide từ @raw-content.md.
Viết ngắn gọn, phù hợp cho lãnh đạo.
```

```text
Dùng viettel-html-slide tạo một slide 16:9 từ nội dung sau:
<dán nội dung vào đây>
```

Agent sẽ tự chọn layout phù hợp. Người dùng chỉ cần nói thêm số lượng slide, đối tượng xem, giọng văn, hoặc format khi cần.

### Chạy Script Thủ Công

Chạy từ thư mục skills:

```bash
python3 viettel-html-slide/scripts/generator.py input.json viettel-html-slide/template.html output.html
```

Ví dụ:

```bash
python3 viettel-html-slide/scripts/generator.py /tmp/slide.json viettel-html-slide/template.html /tmp/slide.html
```

Lệnh trên tạo:

- `/tmp/slide.html`
- `/tmp/assets/` được copy từ `viettel-html-slide/assets/`

## Input Tối Thiểu

```json
{
  "title": "Platform Overview",
  "subtitle": "Architecture and delivery model",
  "layout": "text-only",
  "copy": "Short summary of the slide.",
  "html_content": "<p>Detailed HTML content.</p>"
}
```

## Trường Dữ Liệu Chung

- `title`: tiêu đề slide
- `subtitle`: phụ đề slide, không bắt buộc
- `layout`: tên layout template
- `slide_mode`: không bắt buộc, dùng `"16x9"` cho chế độ trình chiếu cố định
- `body_class`: không bắt buộc, thêm CSS class vào thẻ `<body>`

## Layouts

Các layout được hỗ trợ:

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

## Ví Dụ Layout

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

## Quy Tắc Thương Hiệu

- Dùng logo Viettel thật được bundle sẵn: `assets/viettel-logo.png`.
- Không dựng lại logo bằng text, CSS, SVG, chữ viết tắt, hoặc placeholder.
- Giữ markup logo trong `template.html`, trừ khi có asset thay thế được cung cấp rõ ràng.
- Giữ nền trang và nền slide màu trắng theo mặc định, trừ layout `background-overlay`.
- Dùng `assets/slide-viettel-theme.css` làm file theme chuẩn.

## Khả Năng Đọc Ảnh

Với file PNG, JPEG, và GIF local, generator đọc kích thước ảnh và phân loại:

- Tỷ lệ ảnh `>= 1.8`: ảnh rộng dễ đọc
- Tỷ lệ ảnh `>= 2.5`: ảnh siêu rộng dễ đọc
- Tỷ lệ ảnh `<= 0.75`: ảnh dọc dễ đọc

Trong chế độ `16x9`, chart rộng hoặc chart dọc thường nên đặt mỗi ảnh trên một slide riêng. Layout nhiều ảnh có chart cần đọc sẽ sinh warning để tránh làm ảnh bị thu nhỏ đến mức khó đọc nhãn.

## Ghi Chú Output

- HTML được tạo sẽ link tới `./assets/slide-viettel-theme.css`.
- Generator copy toàn bộ thư mục `assets/` được bundle sẵn sang cạnh file output.
- Đường dẫn ảnh tương đối được resolve từ thư mục của file JSON, thư mục output, hoặc current working directory.
- Layout không tồn tại sẽ bị từ chối với thông báo lỗi.

## Kiểm Tra

Kiểm tra syntax Python:

```bash
python3 -m py_compile viettel-html-slide/scripts/generator.py
python3 -m py_compile scripts/ingest_assets.py
```

Tạo slide smoke test:

```bash
python3 viettel-html-slide/scripts/generator.py /tmp/slide.json viettel-html-slide/template.html /tmp/slide.html
```
