#!/usr/bin/env python3
"""One-time domain migration: jiyou-eng.github.io/sunflex-site -> sunflex-corp.github.io (org root page, no path prefix)."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "brand/sunflex-ci"}
OLD = "jiyou-eng.github.io/sunflex-site"
NEW = "sunflex-corp.github.io"


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
        count = text.count(OLD)
        if count:
            html_path.write_text(text.replace(OLD, NEW), encoding="utf-8")
            changed_files += 1
            total_replacements += count
            print(f"{html_path.relative_to(ROOT)}: {count} replacements")
    print(f"\nTotal: {changed_files} files changed, {total_replacements} replacements")


if __name__ == "__main__":
    main()
