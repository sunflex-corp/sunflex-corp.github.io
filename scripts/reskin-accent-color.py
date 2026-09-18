#!/usr/bin/env python3
"""Recolor the inherited jiyou-eng green accent to SUNFLEX's brand hue.

The design-token system defines its accent/hover/focus/tint colors as
oklch(L% C H) triples all sharing hue 151.5 (green). SUNFLEX's brand color
(#4351D8) converts to oklch(50.9% 0.205 272.2) -- hue 272.2 (blue-indigo).

Rather than picking new colors by eye, this rotates the hue component of
each existing oklch() declaration from 151.5 to 272.2, keeping lightness
and chroma untouched. That preserves the exact same lightness ladder
(hover darker, focus/tints lighter) and contrast relationships the design
system already relies on -- only the hue changes, green to SUNFLEX blue.

Unrelated colors (safety/warning orange, danger red, the 5-sense "MOVING"
badge palette, the pre-existing separate --color-brand-blue token) are not
touched.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "brand/sunflex-ci"}

OLD_HUE = "151.5)"
NEW_HUE = "272.2)"


def is_excluded(path: pathlib.Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(rel == d or rel.startswith(d + "/") for d in EXCLUDE_DIRS)


def main() -> None:
    changed_files = 0
    total_replacements = 0
    for css_path in sorted(ROOT.rglob("*.css")):
        if is_excluded(css_path):
            continue
        text = css_path.read_text(encoding="utf-8")
        count = len(re.findall(r"oklch\([0-9.]+% [0-9.]+ " + re.escape(OLD_HUE), text))
        if count:
            new_text = re.sub(
                r"(oklch\([0-9.]+% [0-9.]+ )" + re.escape(OLD_HUE),
                r"\g<1>" + NEW_HUE,
                text,
            )
            css_path.write_text(new_text, encoding="utf-8")
            changed_files += 1
            total_replacements += count
            print(f"{css_path.relative_to(ROOT)}: {count} replacements")
    print(f"\nTotal: {changed_files} files changed, {total_replacements} replacements")


if __name__ == "__main__":
    main()
