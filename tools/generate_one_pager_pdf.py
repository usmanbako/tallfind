from pathlib import Path
import textwrap

SRC_MD = Path('docs/tallfind-one-page-summary.md')
OUT_PDF = Path('docs/tallfind-one-page-summary.pdf')

PAGE_WIDTH = 612   # Letter portrait
PAGE_HEIGHT = 792
LEFT = 50
TOP = 760
BODY_FONT_SIZE = 10
TITLE_FONT_SIZE = 16
LEADING = 16
MAX_CHARS = 90


def pdf_escape(text: str) -> str:
    return text.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')


def markdown_to_lines(md_text: str) -> list[str]:
    """Convert simple markdown to wrapped plain-text lines for single-page PDF rendering."""
    out: list[str] = []
    for raw in md_text.splitlines():
        line = raw.rstrip()

        if not line:
            out.append("")
            continue

        if line.startswith('# '):
            out.append(line[2:].strip())
            continue

        if line.startswith('## '):
            out.append(line[3:].strip())
            continue

        if line.startswith('- '):
            wrapped = textwrap.wrap(line[2:].strip(), width=MAX_CHARS - 4)
            if wrapped:
                out.append(f"• {wrapped[0]}")
                out.extend([f"  {w}" for w in wrapped[1:]])
            else:
                out.append('•')
            continue

        # Numbered list support, e.g. "1. ..."
        if len(line) > 3 and line[0].isdigit() and line[1:3] == '. ':
            marker = line[:3]
            wrapped = textwrap.wrap(line[3:].strip(), width=MAX_CHARS - len(marker))
            if wrapped:
                out.append(f"{marker}{wrapped[0]}")
                out.extend(["   " + w for w in wrapped[1:]])
            else:
                out.append(marker.strip())
            continue

        out.extend(textwrap.wrap(line, width=MAX_CHARS) or [""])

    return out


def build_pdf(lines: list[str]) -> bytes:
    objects: list[bytes] = []

    def add_obj(data: bytes):
        objects.append(data)

    # 1 Catalog, 2 Pages, 3 Page, 4 Font
    add_obj(b"<< /Type /Catalog /Pages 2 0 R >>")
    add_obj(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    add_obj(
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
    )
    add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    content_lines: list[str] = []
    y = TOP

    for i, line in enumerate(lines):
        if y < 40:
            raise ValueError("Content overflow: one-page layout exceeded. Shorten the summary.")
        safe = pdf_escape(line)
        if i == 0:
            content_lines.append(f"BT /F1 {TITLE_FONT_SIZE} Tf {LEFT} {y} Td ({safe}) Tj ET")
            y -= 24
        else:
            content_lines.append(f"BT /F1 {BODY_FONT_SIZE} Tf {LEFT} {y} Td ({safe}) Tj ET")
            y -= LEADING

    stream = "\n".join(content_lines).encode('latin-1', errors='replace')
    add_obj(f"<< /Length {len(stream)} >>\nstream\n".encode('latin-1') + stream + b"\nendstream")

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{i} 0 obj\n".encode('ascii'))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_pos = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode('ascii'))
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode('ascii'))

    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode('ascii')
    )
    return bytes(pdf)


def main():
    if not SRC_MD.exists():
        raise FileNotFoundError(f"Missing source markdown: {SRC_MD}")

    lines = markdown_to_lines(SRC_MD.read_text(encoding='utf-8'))
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    OUT_PDF.write_bytes(build_pdf(lines))
    print(f"Wrote {OUT_PDF}")


if __name__ == '__main__':
    main()
