#!/usr/bin/env python3
"""Wire site-header-scroll.js into every page that already loads
brand/consultation-light.js (i.e. every real page that renders the shared
site-header component). Follows the same literal-string-insertion approach
as scripts/rebrand.py / scripts/remove-placeholder-links.py -- no regex
guessing.

Skips the handful of pages that don't have a site-header at all (the
solutions/{air,guard,sound,eyes,story} SOLAR-migration redirect stubs, and
brand/sunflex-ci/05_Web/, an internal CI mockup page) since they simply
don't have the anchor to insert after.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ANCHOR = '<script defer src="/brand/consultation-light.js?v=20260910-site-glow-v2"></script>'
NEW_SCRIPT = '<script defer src="/site-header-scroll.js?v=1"></script>'


def main():
    html_files = sorted(REPO.rglob('*.html'))
    updated, skipped_no_anchor, skipped_already = [], [], []

    for path in html_files:
        text = path.read_text(encoding='utf-8')
        if ANCHOR not in text:
            skipped_no_anchor.append(path)
            continue
        if NEW_SCRIPT in text:
            skipped_already.append(path)
            continue
        new_text = text.replace(ANCHOR, ANCHOR + NEW_SCRIPT, 1)
        assert new_text.count(NEW_SCRIPT) == 1
        path.write_text(new_text, encoding='utf-8')
        updated.append(path)

    print(f"Updated: {len(updated)}")
    print(f"Already had it: {len(skipped_already)}")
    print(f"No anchor (skipped, no site-header): {len(skipped_no_anchor)}")
    for p in skipped_no_anchor:
        print(f"  - {p.relative_to(REPO)}")


if __name__ == '__main__':
    main()
