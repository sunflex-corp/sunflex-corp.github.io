#!/usr/bin/env python3
"""Remove the Naver blog link and the internal-portal link — SUNFLEX doesn't
have its own yet; the user asked to exclude them for now and add them back
later when they exist."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "brand/sunflex-ci"}

REPLACEMENTS = [
    # JSON-LD Organization.sameAs (Naver blog)
    (
        ',"sameAs":["https://blog.naver.com/jiyou_eng"]',
        "",
    ),
    # Footer "오시는 길" block — Naver blog link
    (
        '<a href="https://blog.naver.com/jiyou_eng" rel="noopener noreferrer" '
        'data-astro-cid-kl7gxbjz>공식 블로그</a>',
        "",
    ),
    # company/index.html 기업정보 table — "공식 채널" row (Naver blog)
    (
        '<div data-astro-cid-zpwr3yl4><dt data-astro-cid-zpwr3yl4>공식 채널</dt>'
        '<dd data-astro-cid-zpwr3yl4><a href="https://blog.naver.com/jiyou_eng" '
        'rel="noreferrer" data-astro-cid-zpwr3yl4>썬플렉스 블로그 ↗</a></dd></div>',
        "",
    ),
    # Desktop header nav — internal portal link
    (
        '<a class="header-portal" href="https://pecan-reptilian-botanist.ngrok-free.dev/" '
        'target="_blank" rel="noopener noreferrer" aria-label="사내 포털 (새 탭)" '
        'data-astro-cid-6stfpryv>사내 포털<span aria-hidden="true" '
        'data-astro-cid-6stfpryv>↗</span></a>',
        "",
    ),
    # Mobile drawer nav — internal portal link (remove the whole <li>)
    (
        '<li class="drawer__nav-portal" style="--drawer-index:4" '
        'data-astro-cid-3xbwrhqs><a class="drawer__portal" '
        'href="https://pecan-reptilian-botanist.ngrok-free.dev/" target="_blank" '
        'rel="noopener noreferrer" aria-label="사내 포털 (새 탭)" '
        'data-astro-cid-3xbwrhqs>사내 포털</a></li>',
        "",
    ),
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
