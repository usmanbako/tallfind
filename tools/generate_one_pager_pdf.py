from pathlib import Path

out_path = Path('docs/tallfind-one-page-summary.pdf')
out_path.parent.mkdir(parents=True, exist_ok=True)

lines = [
"Tallfind — One-Page App Summary",
"",
"What it is",
"- Tallfind is a static web directory for finding tall-friendly clothing stores.",
"- It curates hand-reviewed entries for men and women, with verified sizing metadata.",
"",
"Who it's for",
"- Primary persona: tall shoppers (men ~6'2\"+ and women ~5'9\"+) who struggle to find",
"  reliable tall sizing across brands.",
"",
"What it does",
"- Loads separate men's and women's store datasets from local JSON files.",
"- Provides tabbed browsing (Home, Men's, Women's) with URL-synced filter state.",
"- Supports keyword search across store metadata (name, sizing, notes, categories).",
"- Filters by tall-only brands, tops, bottoms, favorites, and men's minimum inseam.",
"- Offers sort modes (tall-first, A–Z, and inseam for men's listings).",
"- Saves user favorites and analytics consent in localStorage.",
"- Collects store submissions and feedback via Formspree modal forms.",
"",
"How it works (repo evidence)",
"- Front end: index.html + assets/styles.css + assets/app.js rendered in-browser.",
"- Data layer: static JSON files (data/men.json, data/women.json, data/featured.json).",
"- Runtime flow: browser fetches JSON -> JS stores state -> applies search/filter/sort ->",
"  renders cards and homepage sections dynamically.",
"- Integrations: Google Analytics (gtag with consent banner), Formspree form endpoints.",
"- Backend service/API/database: Not found in repo.",
"",
"How to run (minimal)",
"1) From repo root, start any static web server (example):",
"   python3 -m http.server 8000",
"2) Open http://localhost:8000 in a browser.",
"3) Use the directory tabs and filters; submissions/feedback post to Formspree endpoints.",
"",
"Notes",
"- Formal local setup docs beyond a one-line README are Not found in repo.",
]

# Minimal PDF generator (single-page, Helvetica)
objects = []

def add_obj(data: bytes):
    objects.append(data)

# 1 Catalog
add_obj(b"<< /Type /Catalog /Pages 2 0 R >>")
# 2 Pages
add_obj(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
# 3 Page (letter size)
add_obj(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")
# 4 Font
add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

# 5 Content stream
content_lines = []
y = 760
leading = 18
for i, line in enumerate(lines):
    safe = line.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')
    if i == 0:
        content_lines.append(f"BT /F1 16 Tf 50 {y} Td ({safe}) Tj ET")
        y -= 26
    else:
        content_lines.append(f"BT /F1 10 Tf 50 {y} Td ({safe}) Tj ET")
        y -= leading

stream = "\n".join(content_lines).encode('latin-1', errors='replace')
add_obj(f"<< /Length {len(stream)} >>\nstream\n".encode('latin-1') + stream + b"\nendstream")

# Build file with xref
pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
offsets = [0]
for i, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf.extend(f"{i} 0 obj\n".encode('ascii'))
    pdf.extend(obj)
    pdf.extend(b"\nendobj\n")

xref_pos = len(pdf)
pdf.extend(f"xref\n0 {len(objects)+1}\n".encode('ascii'))
pdf.extend(b"0000000000 65535 f \n")
for off in offsets[1:]:
    pdf.extend(f"{off:010d} 00000 n \n".encode('ascii'))

pdf.extend(
    f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode('ascii')
)

out_path.write_bytes(pdf)
print(f"Wrote {out_path}")
