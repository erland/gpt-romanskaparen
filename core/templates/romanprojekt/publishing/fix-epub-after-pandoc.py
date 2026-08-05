#!/usr/bin/env python3
"""Efterbearbetar en Pandoc-EPUB enligt Romanskaparens standard v4.

Mål:
1. Behåll den navigerbara EPUB-TOC:en/nav.xhtml som index i läsaren.
2. Visa inte nav.xhtml som en vanlig innehållsförteckningssida i bokflödet.
3. Neutralisera CSS-regler som kan skapa tom sida före kapitelrubriken.

Viktigt: Ta normalt inte bort nav-itemref helt. Sätt hellre linear="no" för
bättre kompatibilitet med EPUB-läsare som förväntar sig nav i spine men inte
ska visa den i den linjära läsordningen.
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


def find_nav_ids(opf_text: str) -> set[str]:
    ids: set[str] = set()
    item_re = re.compile(r"<item\b[^>]*>", re.IGNORECASE)
    id_re = re.compile(r'\bid=["\']([^"\']+)["\']', re.IGNORECASE)
    prop_re = re.compile(r'\bproperties=["\'][^"\']*\bnav\b[^"\']*["\']', re.IGNORECASE)
    href_nav_re = re.compile(r'\bhref=["\'][^"\']*(?:nav|toc)[^"\']*\.xhtml["\']', re.IGNORECASE)
    for m in item_re.finditer(opf_text):
        item = m.group(0)
        if prop_re.search(item) or href_nav_re.search(item):
            id_m = id_re.search(item)
            if id_m:
                ids.add(id_m.group(1))
    if not ids:
        ids.add("nav")
    return ids


def hide_nav_in_spine(opf_text: str) -> str:
    nav_ids = find_nav_ids(opf_text)
    for nav_id in nav_ids:
        # itemref self-closing without linear: add linear="no"
        opf_text = re.sub(
            rf'(<itemref\b(?=[^>]*\bidref=["\']{re.escape(nav_id)}["\'])(?![^>]*\blinear=)[^>]*)/?>',
            lambda m: m.group(1).rstrip().rstrip('/') + ' linear="no"/>',
            opf_text,
            flags=re.IGNORECASE,
        )
        # itemref with linear yes/true: change to no
        opf_text = re.sub(
            rf'(<itemref\b(?=[^>]*\bidref=["\']{re.escape(nav_id)}["\'])[^>]*\blinear=)["\'](?:yes|true|1)["\']',
            r'\1"no"',
            opf_text,
            flags=re.IGNORECASE,
        )
    return opf_text


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: fix-epub-after-pandoc.py input.epub [output.epub]")
        return 2

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) == 3 else src
    if not src.exists():
        print(f"Missing file: {src}")
        return 2

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        with zipfile.ZipFile(src) as zf:
            zf.extractall(tmp)

        for opf in tmp.rglob("*.opf"):
            text = opf.read_text(encoding="utf-8")
            text = hide_nav_in_spine(text)
            opf.write_text(text, encoding="utf-8")

        for css in tmp.rglob("*.css"):
            text = css.read_text(encoding="utf-8")
            text = text.replace("page-break-before: always;", "page-break-before: auto;")
            text = text.replace("break-before: page;", "break-before: auto;")
            css.write_text(text, encoding="utf-8")

        out = dst
        if out == src:
            backup = src.with_suffix(src.suffix + ".bak")
            shutil.copy2(src, backup)
        if out.exists():
            out.unlink()
        with zipfile.ZipFile(out, "w") as zf:
            mimetype = tmp / "mimetype"
            if mimetype.exists():
                zf.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
            for path in sorted(tmp.rglob("*")):
                if path.is_file() and path.name != "mimetype":
                    zf.write(path, path.relative_to(tmp).as_posix(), compress_type=zipfile.ZIP_DEFLATED)

    print(f"Fixed EPUB: {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
