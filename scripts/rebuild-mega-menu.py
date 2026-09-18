#!/usr/bin/env python3
"""Rebuild the sitewide header "솔루션"/"제품" mega-menu + mobile drawer quick
links from the old 5-sense taxonomy (eyes/sound/air/guard/story) to the new
SOLAR 4-stage taxonomy (detect/alert/respond/record), and fix up remaining
sitewide href="/solutions/X" links outside those rebuilt blocks.

See docs/superpowers/specs/2026-09-18-solar-ia-restructure.md.

This script targets THREE byte-identical shared blocks that appear on all
62 HTML pages (verified via diff before writing this script):

  1. The desktop "#mega-solutions" dropdown's "오감 축" list (5 plain links,
     no color marks) -> "4단계 축" list (4 links).
  2. The desktop "#mega-products" dropdown's 5 mark-icon columns, each with
     a full flat product list -> 4 columns regenerated from
     product-menu-data.js (single source of truth for which products now
     belong to which of the 4 stages, including the air/detect+alert
     split), preserving product name/href text verbatim.
  3. The mobile drawer's "MOVING 제품군" quick-filter list (5 axis-dot
     links to /products?category=X) -> 4 links using the new stage keys.

Then, a second pass does a plain literal href replace for any remaining
href="/solutions/{eyes,sound,guard,story}" occurrences sitewide (footer,
breadcrumbs, homepage hero ring, etc. -- anything not part of the 3 blocks
above, which are already rewritten by the time this pass runs).
href="/solutions/air" is defaulted to href="/solutions/detect" (documented
in the final count -- air's content splits detect/alert and a bare href
carries no context to disambiguate; detect absorbs the larger share, 9/13
products).

Run: python3 scripts/rebuild-mega-menu.py
"""
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", "brand/sunflex-ci", "docs/superpowers/plans"}

STAGES = [
    ("detect", "감지", "01"),
    ("alert", "경보", "02"),
    ("respond", "대응", "03"),
    ("record", "기록", "04"),
]

# ---------------------------------------------------------------------------
# Exact literal old block text (captured from index.html, verified
# byte-identical across a sample of 5+ pages spanning every page type before
# writing this script).
# ---------------------------------------------------------------------------

OLD_MEGA_SOLUTIONS = (
    '<section class="mega-menu__group" aria-label="오감 축" data-astro-cid-mvkkp5fy>'
    '<p class="mega-menu__title" data-astro-cid-mvkkp5fy>오감 축</p><ul data-astro-cid-mvkkp5fy>'
    '<li data-astro-cid-mvkkp5fy><a href="/solutions/eyes" data-astro-cid-mvkkp5fy>'
    '<strong data-astro-cid-mvkkp5fy>시각·관제</strong></a></li>'
    '<li data-astro-cid-mvkkp5fy><a href="/solutions/sound" data-astro-cid-mvkkp5fy>'
    '<strong data-astro-cid-mvkkp5fy>청각·경보</strong></a></li>'
    '<li data-astro-cid-mvkkp5fy><a href="/solutions/air" data-astro-cid-mvkkp5fy>'
    '<strong data-astro-cid-mvkkp5fy>공간</strong></a></li>'
    '<li data-astro-cid-mvkkp5fy><a href="/solutions/guard" data-astro-cid-mvkkp5fy>'
    '<strong data-astro-cid-mvkkp5fy>보호·안전장구</strong></a></li>'
    '<li data-astro-cid-mvkkp5fy><a href="/solutions/story" data-astro-cid-mvkkp5fy>'
    '<strong data-astro-cid-mvkkp5fy>기록·콘텐츠</strong></a></li></ul></section>'
)


def build_new_mega_solutions():
    lis = "".join(
        f'<li data-astro-cid-mvkkp5fy><a href="/solutions/{key}" data-astro-cid-mvkkp5fy>'
        f"<strong data-astro-cid-mvkkp5fy>{label}</strong></a></li>"
        for key, label, _mark in STAGES
    )
    return (
        '<section class="mega-menu__group" aria-label="4단계 축" data-astro-cid-mvkkp5fy>'
        '<p class="mega-menu__title" data-astro-cid-mvkkp5fy>4단계 축</p>'
        f"<ul data-astro-cid-mvkkp5fy>{lis}</ul></section>"
    )


OLD_MOBILE_DRAWER = (
    '<nav class="drawer__axes" aria-label="제품 축 바로가기" data-astro-cid-3xbwrhqs>'
    '<p class="drawer__axes-label" data-astro-cid-3xbwrhqs>MOVING 제품군</p>'
    '<div data-astro-cid-3xbwrhqs><ul data-astro-cid-3xbwrhqs>'
    '<li style="--axis-dot:var(--moving-eyes-badge)" data-astro-cid-3xbwrhqs>'
    '<a href="/products?category=eyes" data-astro-cid-3xbwrhqs>시각·관제</a></li>'
    '<li style="--axis-dot:var(--moving-sound-badge)" data-astro-cid-3xbwrhqs>'
    '<a href="/products?category=sound" data-astro-cid-3xbwrhqs>청각·경보</a></li>'
    '<li style="--axis-dot:var(--moving-air-badge)" data-astro-cid-3xbwrhqs>'
    '<a href="/products?category=air" data-astro-cid-3xbwrhqs>공간</a></li>'
    '<li style="--axis-dot:var(--moving-guard-badge)" data-astro-cid-3xbwrhqs>'
    '<a href="/products?category=guard" data-astro-cid-3xbwrhqs>보호·안전장구</a></li>'
    '<li style="--axis-dot:var(--moving-story-badge)" data-astro-cid-3xbwrhqs>'
    '<a href="/products?category=story" data-astro-cid-3xbwrhqs>기록·콘텐츠</a></li>'
    "</ul></div></nav>"
)


def build_new_mobile_drawer():
    lis = "".join(
        f'<li style="--axis-dot:var(--moving-{key}-badge)" data-astro-cid-3xbwrhqs>'
        f'<a href="/products?category={key}" data-astro-cid-3xbwrhqs>{label}</a></li>'
        for key, label, _mark in STAGES
    )
    return (
        '<nav class="drawer__axes" aria-label="제품 축 바로가기" data-astro-cid-3xbwrhqs>'
        '<p class="drawer__axes-label" data-astro-cid-3xbwrhqs>MOVING 제품군</p>'
        f"<div data-astro-cid-3xbwrhqs><ul data-astro-cid-3xbwrhqs>{lis}</ul></div></nav>"
    )


def load_product_menu_data():
    path = os.path.join(REPO_ROOT, "product-menu-data.js")
    raw = open(path, encoding="utf-8").read()
    raw = raw.replace("export default ", "", 1).rstrip().rstrip(";")
    return json.loads(raw)


def build_new_mega_products(stage_data):
    """stage_data: list of {"key","label","mark","categories":[{"products":[...]}]}."""
    by_key = {s["key"]: s for s in stage_data}
    cells = []
    for key, label, mark in STAGES:
        stage = by_key[key]
        products = []
        for cat in stage["categories"]:
            products.extend(cat["products"])
        lis = "".join(
            f'<li data-astro-cid-mvkkp5fy><a href="{p["href"]}" data-astro-cid-mvkkp5fy>'
            f'{p["name"].replace("&", "&amp;")}</a></li>'
            for p in products
        )
        cells.append(
            '<div class="mega-menu__product-cell" data-astro-cid-mvkkp5fy>'
            '<section class="mega-menu__product-column" data-astro-cid-mvkkp5fy>'
            '<p class="mega-menu__column-title" data-astro-cid-mvkkp5fy>'
            f'<a href="/solutions/{key}" data-astro-cid-mvkkp5fy>'
            '<span class="mega-menu__mark" aria-hidden="true" '
            f'style="--sense-badge:var(--moving-{key}-badge);'
            f'--sense-on-badge:var(--moving-{key}-on-badge)" '
            f'data-astro-cid-mvkkp5fy>{mark}</span>'
            f'<span class="mega-menu__column-label" data-astro-cid-mvkkp5fy>{label}</span>'
            "</a></p>"
            f"<ul data-astro-cid-mvkkp5fy>{lis}</ul>"
            "</section></div>"
        )
    return (
        '<section id="mega-products" class="mega-menu" hidden data-mega-menu '
        'aria-label="제품 세부 메뉴" data-astro-cid-mvkkp5fy>'
        '<div class="mega-menu__product-shell" data-astro-cid-mvkkp5fy>'
        '<header class="mega-menu__product-head" data-astro-cid-mvkkp5fy>'
        '<p class="mega-menu__title" data-astro-cid-mvkkp5fy>제품</p>'
        '<a href="/products" data-astro-cid-mvkkp5fy>전체 제품 보기</a></header>'
        '<div class="mega-menu__product-grid" data-astro-cid-mvkkp5fy>'
        + "".join(cells)
        + "</div></div></section>"
    )


HREF_REPLACEMENTS = [
    ('href="/solutions/eyes"', 'href="/solutions/detect"'),
    ('href="/solutions/sound"', 'href="/solutions/alert"'),
    ('href="/solutions/guard"', 'href="/solutions/respond"'),
    ('href="/solutions/story"', 'href="/solutions/record"'),
]
AIR_HREF_OLD = 'href="/solutions/air"'
AIR_HREF_NEW = 'href="/solutions/detect"'


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


def find_html_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if not is_excluded(os.path.join(dirpath, d))]
        for fn in sorted(filenames):
            if fn.endswith(".html"):
                full = os.path.join(dirpath, fn)
                if not is_excluded(full):
                    yield full


def main():
    stage_data = load_product_menu_data()
    new_mega_solutions = build_new_mega_solutions()
    new_mega_products = build_new_mega_products(stage_data)
    new_mobile_drawer = build_new_mobile_drawer()

    files_with_mega_solutions = 0
    files_with_mega_products = 0
    files_with_mobile_drawer = 0
    href_counts = {old: 0 for old, _ in HREF_REPLACEMENTS}
    air_href_count = 0
    total_files_changed = 0

    for path in find_html_files():
        relpath = os.path.relpath(path, REPO_ROOT)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        original = content

        did_mega_solutions = False
        did_mega_products = False
        did_mobile_drawer = False

        if OLD_MEGA_SOLUTIONS in content:
            content = content.replace(OLD_MEGA_SOLUTIONS, new_mega_solutions, 1)
            files_with_mega_solutions += 1
            did_mega_solutions = True
        elif "mega-menu__group" in content and 'aria-label="오감 축"' in content:
            print(f"BLOCKED: {relpath} has a mega-solutions block that did not "
                  "match the expected literal text exactly.")

        if OLD_MEGA_PRODUCTS_TEXT in content:
            content = content.replace(OLD_MEGA_PRODUCTS_TEXT, new_mega_products, 1)
            files_with_mega_products += 1
            did_mega_products = True
        elif 'id="mega-products"' in content:
            print(f"BLOCKED: {relpath} has a mega-products block that did not "
                  "match the expected literal text exactly.")

        if OLD_MOBILE_DRAWER in content:
            content = content.replace(OLD_MOBILE_DRAWER, new_mobile_drawer, 1)
            files_with_mobile_drawer += 1
            did_mobile_drawer = True
        elif 'aria-label="제품 축 바로가기"' in content:
            print(f"BLOCKED: {relpath} has a mobile-drawer axes block that did not "
                  "match the expected literal text exactly.")

        file_href_count = 0
        for old, new in HREF_REPLACEMENTS:
            n = content.count(old)
            if n:
                href_counts[old] += n
                file_href_count += n
                content = content.replace(old, new)
        n_air = content.count(AIR_HREF_OLD)
        if n_air:
            air_href_count += n_air
            file_href_count += n_air
            content = content.replace(AIR_HREF_OLD, AIR_HREF_NEW)

        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            total_files_changed += 1
            print(
                f"{relpath}: mega-solutions={int(did_mega_solutions)} "
                f"mega-products={int(did_mega_products)} "
                f"mobile-drawer={int(did_mobile_drawer)} "
                f"href-replacements={file_href_count}"
            )

    print()
    print(f"mega-solutions block rebuilt in {files_with_mega_solutions} files")
    print(f"mega-products block rebuilt in {files_with_mega_products} files")
    print(f"mobile-drawer block rebuilt in {files_with_mobile_drawer} files")
    for old, new in HREF_REPLACEMENTS:
        print(f"  {old} -> {new}: {href_counts[old]} replacements")
    print(f"  {AIR_HREF_OLD} -> {AIR_HREF_NEW} (default): {air_href_count} replacements")
    print(f"Total files changed: {total_files_changed}")


if __name__ == "__main__":
    # Loaded lazily so the literal block text above stays readable at the
    # top of the file.
    OLD_MEGA_PRODUCTS_TEXT = open(
        os.path.join(REPO_ROOT, "scripts", "rebuild-mega-menu.mega-products-old.txt"),
        encoding="utf-8",
    ).read()
    main()
