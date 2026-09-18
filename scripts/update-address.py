#!/usr/bin/env python3
"""Update the SUNFLEX address (JSON-LD + visible footer '오시는 길' block) to the
confirmed single address, and drop the now-redundant '본사·제1공장'/'제2공장'
two-site split — SUNFLEX only has one address."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "brand/sunflex-ci"}

REPLACEMENTS = [
    (
        '"address":{"@type":"PostalAddress","addressCountry":"KR",'
        '"streetAddress":"경기도 김포시 양촌읍 석모로45번길 93-1"},'
        '"location":{"@type":"Place","name":"썬플렉스 제2공장",'
        '"address":{"@type":"PostalAddress","addressCountry":"KR",'
        '"streetAddress":"경기도 시흥시 신천동 845-18"}},'
        '"contactPoint":',
        '"address":{"@type":"PostalAddress","addressCountry":"KR",'
        '"streetAddress":"경기도 시흥시 신천동 845-18"},'
        '"contactPoint":',
    ),
    (
        '<span data-astro-cid-kl7gxbjz><strong data-astro-cid-kl7gxbjz>본사·제1공장</strong>'
        '<br data-astro-cid-kl7gxbjz>경기도 김포시 양촌읍 석모로45번길 93-1</span>'
        '<span data-astro-cid-kl7gxbjz><strong data-astro-cid-kl7gxbjz>제2공장</strong>'
        '<br data-astro-cid-kl7gxbjz>경기도 시흥시 신천동 845-18</span>',
        '<span data-astro-cid-kl7gxbjz>경기도 시흥시 신천동 845-18</span>',
    ),
    (
        # contact/index.html: two separate <address> blocks with per-word tokens
        '<address data-astro-cid-6bfsojfh><strong data-astro-cid-6bfsojfh>본사·제1공장</strong>'
        '<br data-astro-cid-6bfsojfh><span class="address-token" data-astro-cid-6bfsojfh>경기도</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>김포시</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>양촌읍</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>석모로45번길</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>93-1</span></address>'
        '<address data-astro-cid-6bfsojfh><strong data-astro-cid-6bfsojfh>제2공장</strong>'
        '<br data-astro-cid-6bfsojfh><span class="address-token" data-astro-cid-6bfsojfh>경기도</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>시흥시</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>신천동</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>845-18</span></address>',
        '<address data-astro-cid-6bfsojfh><span class="address-token" data-astro-cid-6bfsojfh>경기도</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>시흥시</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>신천동</span> '
        '<span class="address-token" data-astro-cid-6bfsojfh>845-18</span></address>',
    ),
    (
        # company/index.html: 기업정보 dl/dt/dd facts table
        '<div data-astro-cid-zpwr3yl4><dt data-astro-cid-zpwr3yl4>본사·제1공장</dt>'
        '<dd data-astro-cid-zpwr3yl4>경기도 김포시 양촌읍 석모로45번길 93-1</dd></div>'
        '<div data-astro-cid-zpwr3yl4><dt data-astro-cid-zpwr3yl4>제2공장</dt>'
        '<dd data-astro-cid-zpwr3yl4>경기도 시흥시 신천동 845-18</dd></div>',
        '<div data-astro-cid-zpwr3yl4><dt data-astro-cid-zpwr3yl4>주소</dt>'
        '<dd data-astro-cid-zpwr3yl4>경기도 시흥시 신천동 845-18</dd></div>',
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
