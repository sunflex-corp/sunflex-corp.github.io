#!/usr/bin/env python3
"""Retire the legacy per-category "Jiyou {Visual,Hear,Protect,Record}" bespoke
display fonts in favor of the sitewide Asta Sans display face, across every
page that still references them via the inline `--product-title-family`
custom property.

See docs/superpowers/specs/2026-09-18-figma-design-system-phase1.md and
docs/superpowers/specs/2026-09-18-figma-design-system-phase2.md -- Phase 2
established Asta Sans (self-hosted, Korean-supporting) as the sitewide
display typeface (`--font-display-family`) at weight 500 for the homepage
hero. This script extends that same treatment to the pages Phase 2 left out:
every products/*/index.html detail page and every solutions/*/index.html
stage page that sets its own H1 typeface via an inline style on
`#main-content`, e.g.:

    style="--product-title-family:&quot;Jiyou Protect&quot;;--product-title-weight:600"

Scope (all *.html files repo-wide, excluding .git and brand/sunflex-ci):
  - `--product-title-family:&quot;Jiyou {Visual,Hear,Protect,Record}&quot;`
    -> `--product-title-family:&quot;Asta Sans&quot;`
  - `--product-title-weight:NNN` immediately following a Jiyou-family value
    just replaced -> normalized to `--product-title-weight:500` (uniform,
    matching the homepage hero's Asta Sans 500 treatment). NOT touched when
    it follows a non-Jiyou family value (e.g. the "Pretendard Variable"
    fallback already used on a few pages) -- that pairing is left exactly
    as-is, it was never a Jiyou reference.

Also updates brand/portal-link.css's header-cta/drawer-cta font stack:
    font-family:"Jiyou Record","Pretendard Variable",sans-serif;
    -> font-family:"Asta Sans","Pretendard Variable",sans-serif;
This is small nav text, not a headline -- its weight comes from the
surrounding rule's own font-weight declaration, so no weight override is
added here.

Deliberately NOT touched (documented, not silently dropped):
  - @font-face declarations for Jiyou Visual/Hear/Protect/Record in
    _astro/BaseLayout.a023156454.css (and its orphaned, unreferenced sibling
    copy _astro/BaseLayout.ONpCcpb0.css) -- these still declare the font
    faces but nothing uses them anymore after this script runs. Left in
    place per explicit instruction: other things might still reference them,
    and deleting @font-face rules is out of scope for a font-swap pass.
  - page-hero-typography.css's `font-family: "Jiyou Record", ...` rule
    (governs #contact-title/#catalog-title/#solutions-title/#support-title)
    -- this is a real *usage*, not a mechanical inline-style pattern, and is
    handled by hand as part of the Phase 3 spacing/typography touch-up
    (matches hero-typography.css's `var(--font-display-family)` pattern),
    not by this script.

Run: python3 scripts/apply-asta-sans-titles.py
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXCLUDE_DIRS = {".git", "brand/sunflex-ci"}

JIYOU_FAMILIES = ("Jiyou Visual", "Jiyou Hear", "Jiyou Protect", "Jiyou Record")

# Matches --product-title-family:&quot;Jiyou X&quot;;--product-title-weight:NNN
# as one unit so the weight is only touched when it follows a Jiyou family.
PRODUCT_TITLE_RE = re.compile(
    r'--product-title-family:&quot;(Jiyou (?:Visual|Hear|Protect|Record))&quot;'
    r'(;--product-title-weight:)\d+'
)

PORTAL_LINK_RE = re.compile(r'font-family:"Jiyou Record"')


def is_excluded(path):
    rel = os.path.relpath(path, REPO_ROOT)
    if rel == ".":
        return False
    for excl in EXCLUDE_DIRS:
        if rel == excl or rel.startswith(excl + os.sep):
            return True
    if rel.split(os.sep)[0] == ".git":
        return True
    return False


def rel(path):
    return os.path.relpath(path, REPO_ROOT)


def find_html_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [
            d for d in dirnames if not is_excluded(os.path.join(dirpath, d))
        ]
        for fn in filenames:
            if fn.endswith(".html"):
                full = os.path.join(dirpath, fn)
                if not is_excluded(full):
                    yield full


def process_html(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    def repl(m):
        return '--product-title-family:&quot;Asta Sans&quot;' + m.group(2) + "500"

    new_content, n = PRODUCT_TITLE_RE.subn(repl, content)
    if n == 0:
        return 0

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return n


def process_portal_link():
    path = os.path.join(REPO_ROOT, "brand", "portal-link.css")
    if not os.path.exists(path):
        print("SKIP: brand/portal-link.css not found")
        return 0
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, n = PORTAL_LINK_RE.subn('font-family:"Asta Sans"', content)
    if n == 0:
        return 0
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return n


def main():
    html_files_changed = 0
    html_replacements = 0
    for path in sorted(find_html_files()):
        n = process_html(path)
        if n:
            html_files_changed += 1
            html_replacements += n
            print(f"{rel(path)}: {n} replacement(s)")

    portal_n = process_portal_link()
    if portal_n:
        print(f"brand/portal-link.css: {portal_n} replacement(s)")

    print()
    print(f"HTML files changed: {html_files_changed}")
    print(f"HTML replacements: {html_replacements}")
    print(f"portal-link.css replacements: {portal_n}")

    if html_files_changed == 0 and portal_n == 0:
        print("Nothing changed -- check the patterns against a sample file.")
        sys.exit(1)


if __name__ == "__main__":
    main()
