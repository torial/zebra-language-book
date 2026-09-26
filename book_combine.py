#!/usr/bin/env python3
"""book_combine.py -- write the whole book as ONE markdown file, in SUMMARY.md's order.

    python book_combine.py OUT.md

build-pdf.sh and build-pdf.bat each used to carry a HAND-WRITTEN list of chapter files,
and both had drifted from the book: neither included 07b (Structs, Unions and Value
Types) or 18b (GUI Applications), so the committed PDF lacked both chapters -- and a
missing file was skipped with a one-line warning rather than failing the build.
book/SUMMARY.md is what the website is built from, so it is now the only list: a chapter
added there reaches the PDF with no second edit.

Part headings come from SUMMARY's `# ...` lines. A `reference/*.md` page that is only an
mdBook `{{#include ...}}` stub is resolved to the file it includes (pandoc would print the
directive literally). A referenced file that does not exist is an ERROR, not a skip.
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = ROOT / "book"
INCLUDE = re.compile(r"^\{\{#include\s+([^}]+?)\s*\}\}\s*$")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+\.md)\)")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def resolve(path: Path) -> Path:
    """Follow a page that is nothing but an mdBook include stub to its target."""
    text = path.read_text(encoding="utf-8").strip()
    m = INCLUDE.match(text)
    if m:
        return (path.parent / m.group(1)).resolve()
    return path


def plan():
    """[(kind, value)] in reading order: ('part', heading) or ('file', Path)."""
    out = []
    for line in (BOOK / "SUMMARY.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("# ") and line.strip() != "# Summary":
            out.append(("part", line[2:].strip()))
            continue
        for rel in LINK.findall(line):
            out.append(("file", BOOK / rel))
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python book_combine.py OUT.md")
        return 2
    steps = plan()
    files = [p for k, p in steps if k == "file"]
    missing = [str(p.relative_to(ROOT)) for p in files if not p.exists()]
    if missing:
        print("book_combine: REFUSING -- SUMMARY.md names files that do not exist:")
        for m in missing:
            print("   " + m)
        return 1
    if len(files) < 20:
        print(f"book_combine: REFUSING -- only {len(files)} chapter links parsed from "
              "SUMMARY.md; the link pattern has stopped matching")
        return 1

    parts = [
        "---",
        "title: The Zebra Programming Language",
        "subtitle: A guide from fundamentals through advanced patterns",
        "author: Sean McKay",
        f"date: {date.today().strftime('%B %Y')}",
        "lang: en",
        "toc: true",
        "toc-depth: 2",
        "number-sections: true",
        "---",
        "",
    ]
    for kind, value in steps:
        if kind == "part":
            parts += ["", f"# {value}", ""]
            print(f"  {value}")
        else:
            src = resolve(value)
            parts += ["", src.read_text(encoding="utf-8"), ""]
            print(f"    {value.relative_to(BOOK)}")
    Path(sys.argv[1]).write_text("\n".join(parts), encoding="utf-8", newline="\n")
    print(f"book_combine: {len(files)} files -> {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
