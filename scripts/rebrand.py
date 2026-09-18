#!/usr/bin/env python3
"""Rebrand jiyou-eng site HTML pages to SUNFLEX (company name + URL + logo refs only)."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "brand/sunflex-ci"}

# Order matters only in that each pair must not create a substring that a
# later pair would incorrectly match again; none of these overlap.
REPLACEMENTS = [
    ("brand/jiyou-wordmark.svg", "brand/sunflex-wordmark.svg"),
    ("brand/jiyou-wordmark.png", "brand/sunflex-wordmark.png"),
    ("jiyoueng.com", "jiyou-eng.github.io/sunflex-site"),
    ("지유이엔지", "썬플렉스"),
]


def is_excluded(path: pathlib.Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(rel == d or rel.startswith(d + "/") for d in EXCLUDE_DIRS)


def main() -> None:
    changed_files = 0
    total_replacements = 0
    for html_path in sorted(ROOT.rglob("*.html")):
        if is_excluded(html_path):
            continue
        text = html_path.read_text(encoding="utf-8")
        original = text
        file_count = 0
        for old, new in REPLACEMENTS:
            file_count += text.count(old)
            text = text.replace(old, new)
        if text != original:
            html_path.write_text(text, encoding="utf-8")
            changed_files += 1
            total_replacements += file_count
            print(f"{html_path.relative_to(ROOT)}: {file_count} replacements")
    print(f"\nTotal: {changed_files} files changed, {total_replacements} replacements")


if __name__ == "__main__":
    main()
