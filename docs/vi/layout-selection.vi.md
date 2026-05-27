# Huong Dan Chon Layout

Tai lieu nay huong dan chon layout truoc khi viet JSON cho tung slide.
Nguyen tac uu tien: **hop thong diep truoc, da dang layout sau**.

## Chon Layout Theo Muc Dich

- Mo dau chuong/phan: `section-divider`.
- Chuong trinh hoac danh sach noi dung: `agenda`.
- Tien trinh, moc thoi gian, chuoi su kien: `timeline`.
- Mot KPI can nhan manh: `highlight`.
- So sanh 2 phuong an: `comparison` hoac `two-horizontal-images`.
- Du lieu dang bang: `data-table`, `kpi-grid`.
- Tong hop KPI + phan tich: `chart-analysis`, `bar-insight`, `chart-pie`.
- Ke hoach nhieu luong cong viec theo tuan/thang: `gantt`.
- So do to chuc/bao cao truc thuoc: `org-hierarchy`.
- Chuyen tai khong khi hinh anh manh: `background-overlay`.
- Phu luc ky thuat: `appendix-technical`.
- Mot hinh anh bang chung chinh: `centered-image`.
- Mot hinh + dien giai: `image-text-split`.
- 3-4 y ngang cap: `icon-text-grid` hoac `grid`.

## Quy Tac Da Dang Layout

- 6-12 slide: thuong dung 4-6 loai layout.
- 13+ slide: thuong dung 6+ loai layout.
- Tranh lap cung layout qua 2 slide lien tiep, tru khi can tinh lien mach.
- `icon-text-grid` va `data-table`: thuong toi da 2 slide tren moi 10 slide.

## Chon Layout Theo So Luong Anh

1. Kiem ke anh kha dung tu nguon + fallback pool.
2. Neu so anh kha dung = `0`: uu tien layout it phu thuoc anh.
3. Neu = `1-2`: uu tien layout mot anh, tranh `two-horizontal-images` va `grid` qua nang anh.
4. Neu `>=3`: co the dung day du layout.

## Quy Tac Ti Le Anh (Bat Buoc)

- Mac dinh slide can ca anh + mo ta: uu tien `image-text-split`.
- Anh rong (`>=1.8`), sieu rong (`>=2.5`) hoac doc (`<=0.75`): khong ep `image-top-text-bottom`.
- Voi anh cuc doan ti le, uu tien bo cuc mot anh de bao toan kha nang doc.

## Data va Readability

- Moi slide nen co 1 thong diep so lieu chinh.
- O che do `16:9`, bang nen gon (thuong toi da 6 hang x 5 cot).
- `kpi-grid`: 3-6 KPI/slide; neu nhieu hon thi tach slide.
- Neu nhan chart kho doc, tach noi dung thanh nhieu slide.

## Tranh

- Placeholder (`lorem`, `TBD`, `xxxx`).
- Chu/trang thai mau khong duong phan.
- Overflow/clipping noi dung trong `slide_mode: "16x9"`.
- Ep layout vi da dang neu lam giam do ro rang.

## Tham Chieu

- Ban EN day du: `../guide/layout-selection.md`
- Policy deck: `../guide/deck-policy.md`
