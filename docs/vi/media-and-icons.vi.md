# Huong Dan Icon va Hinh Anh

## Quy Tac Icon

- Uu tien icon Viettel trong `./assets/viettel-icon-v1/icons/*.svg`.
- Thu tu fallback: `Viettel > semantic fallback trong bo Viettel > external source > khong dung emoji`.
- Uu tien SVG de giu chat luong hien thi.

## Mapping Fallback Icon

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

## Kiem Tra Icon Truoc Khi Generate (Bat Buoc)

- Kiem tra tat ca `icon_src` co ton tai.
- Neu thieu file: thay bang icon theo fallback mapping.
- Neu khong co semantic match: dung `./assets/viettel-icon-v1/icons/info.svg`.
- Lap lai den khi khong con icon bi thieu.

## Quy Tac Hinh Anh

- Neu nguoi dung cung cap `pptx/docx/pdf/image`, chay ingest truoc:
  - `python3 scripts/ingest_assets.py --deck-dir preview/<deck-name> <source-files...>`
- Co the them `--render-pdf-pages` khi can render tung trang PDF.
- Uu tien anh trong `source-image-manifest.json` truoc khi dung fallback.
- Fallback pool: `./assets/background_picture/*`.

## Readability Trong `slide_mode: "16x9"`

- Anh/chart rong (`>=1.8`) hoac doc (`<=0.75`): uu tien bo cuc mot anh.
- Anh sieu rong (`>=2.5`): uu tien treatment anh lon nhat tren slide.
- `image-top-text-bottom` chi nen dung cho anh ti le chuan.
- Neu nhan chart khong doc duoc, tach thanh nhieu slide.

## Tham Chieu

- Ban EN day du: `../guide/media-and-icons.md`
- Huong dan icon bo sung: `../icon-sourcing.md`
