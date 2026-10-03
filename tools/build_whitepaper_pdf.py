"""Build WHITEPAPER.pdf from WHITEPAPER.md.

Requires: pip install markdown playwright && python -m playwright install chromium
Usage (from the repository root): python tools/build_whitepaper_pdf.py
"""
import asyncio
from pathlib import Path

import markdown
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC, HTML, PDF = ROOT / "WHITEPAPER.md", ROOT / "whitepaper.tmp.html", ROOT / "WHITEPAPER.pdf"

CSS = """
body { font-family: "DejaVu Serif", Georgia, serif; font-size: 10.5pt; line-height: 1.5; color: #1a1a1a; }
h1 { font-size: 20pt; line-height: 1.2; margin: 0 0 4pt; color: #1C2B3A; }
h3 { font-size: 12pt; font-weight: normal; font-style: italic; margin: 0 0 12pt; color: #333; }
h2 { font-size: 13.5pt; margin: 18pt 0 6pt; color: #1C2B3A; border-bottom: 1px solid #c5d3c2; padding-bottom: 3pt; page-break-after: avoid; }
h3 + p, h2 + p { margin-top: 4pt; }
h3:not(:first-of-type) { font-style: normal; font-weight: bold; font-size: 11pt; margin: 12pt 0 4pt; }
p { margin: 6pt 0; text-align: justify; }
hr { border: 0; border-top: 1px solid #c5d3c2; margin: 12pt 0; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9.5pt; page-break-inside: avoid; }
th, td { border-bottom: 1px solid #c5d3c2; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #eef2ec; }
pre { background: #f4f6f3; border-left: 3px solid #1F5FA8; padding: 8pt 10pt; font-size: 8.6pt; line-height: 1.35; white-space: pre-wrap; page-break-inside: avoid; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; }
a { color: #1F5FA8; text-decoration: none; word-break: break-all; }
"""

FOOTER = ("<div style='font-size:8pt;width:100%;text-align:center;color:#666'>"
          "Locational Break-Even Analysis Without Plotting &nbsp;|&nbsp; "
          "<span class='pageNumber'></span></div>")


async def main():
    body = markdown.markdown(SRC.read_text(encoding="utf-8"), extensions=["tables", "fenced_code"])
    HTML.write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style>"
                    f"</head><body>{body}</body></html>", encoding="utf-8")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(HTML.as_uri())
        await page.pdf(path=str(PDF), format="A4", print_background=True,
                       margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"},
                       display_header_footer=True, header_template="<span></span>",
                       footer_template=FOOTER)
        await browser.close()
    HTML.unlink()
    print(f"Wrote {PDF}")


if __name__ == "__main__":
    asyncio.run(main())
