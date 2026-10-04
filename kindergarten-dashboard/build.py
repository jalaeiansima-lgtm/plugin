#!/usr/bin/env python3
"""Build the kindergarten dashboard from src/dashboard.html.

  python3 build.py demo <data.xlsx> <out.html>
      Page fragment with the Excel file embedded as the first-run data
      (used for the online preview).

  python3 build.py desktop <out.html> [--seed <data.xlsx>]
      Complete standalone HTML document to open from the desktop.
      Without --seed it asks for the Excel file on first run.
"""
import base64
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src" / "dashboard.html"
SEED_TAG = '<script id="seed-xlsx" type="text/plain"></script>'


def with_seed(html: str, xlsx: pathlib.Path | None) -> str:
    if not xlsx:
        return html
    data = base64.b64encode(xlsx.read_bytes()).decode("ascii")
    if SEED_TAG not in html:
        sys.exit("seed placeholder not found in src/dashboard.html")
    return html.replace(SEED_TAG, f'<script id="seed-xlsx" type="text/plain">{data}</script>')


def as_document(fragment: str) -> str:
    return (
        '<!doctype html>\n<html lang="fa" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        "</head>\n<body>\n" + fragment + "\n</body>\n</html>\n"
    )


def main(argv: list[str]) -> None:
    if len(argv) < 2 or argv[0] not in ("demo", "desktop"):
        sys.exit(__doc__)
    html = SRC.read_text(encoding="utf-8")
    if argv[0] == "demo":
        if len(argv) != 3:
            sys.exit(__doc__)
        out = pathlib.Path(argv[2])
        out.write_text(with_seed(html, pathlib.Path(argv[1])), encoding="utf-8")
    else:
        out = pathlib.Path(argv[1])
        seed = pathlib.Path(argv[argv.index("--seed") + 1]) if "--seed" in argv else None
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(as_document(with_seed(html, seed)), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main(sys.argv[1:])
