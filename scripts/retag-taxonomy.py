#!/usr/bin/env python3
"""Retag data-font-axis and per-product data-sense attributes from the old
5-sense taxonomy (eyes/sound/air/guard/story) to the new SOLAR 4-stage
taxonomy (detect/alert/respond/record).

See docs/superpowers/specs/2026-09-18-solar-ia-restructure.md.

Scope (see spec Task B for full rationale):
  - data-font-axis="X": one per products/*/index.html (48 files) and per
    solutions/{air,eyes,guard,safety-box,sound,story}/index.html (6 files).
    Looked up via SLUG_TO_STAGE (product pages) or a direct category rename
    (solutions category pages).
  - data-sense="X": per-product-card tags in products/index.html and in
    solutions/{air,eyes,guard,safety-box,sound,story}/index.html. Each
    occurrence is matched to its product via nearby context (data-slug on
    products/index.html cards, or the next href="/products/{slug}" on
    solutions/* cards) and looked up via SLUG_TO_STAGE -- NOT a blind
    global string replace, since e.g. "air" cards split between detect and
    alert depending on which specific product they are.

Deliberately NOT touched (documented as SKIP in the output, not silently
dropped):
  - company/index.html's 5 sense-tab buttons and the homepage's 5
    sense-circle orbit dots: a structural 5-tabs -> 4-tabs widget rebuild
    is a separate task, not a mechanical attribute rename.
  - products/index.html's 5 "chapter-nav__item" data-sense attributes: on
    inspection these are a page-level jump-nav widget (one entry per OLD
    sense category, linking to on-page anchors like #sense-eyes), not
    per-product-card tags. They are structurally identical to the two
    widgets above and are left alone for the same reason -- there is no
    single product to attribute them to, and mechanically renaming 4 of
    them while leaving "air" unresolved would leave the widget in a worse,
    inconsistent state.
  - solutions/air/index.html's own data-font-axis="air": this is the
    category page's own self-identity attribute. Unlike the per-product
    solutions/safety-box/index.html case (which the spec explicitly says
    to treat as "detect"), the spec gives no single-value mapping for
    "air" itself -- it explicitly splits across detect/alert depending on
    product, and the spec says category-level "air" references are
    deferred to the sibling solutions/ folder-restructuring task. Same
    treatment as leaving href="/solutions/air" links untouched.
  - href="/solutions/{eyes,sound,air,guard,story}" links anywhere: out of
    scope per spec, handled by the solutions/ folder restructuring task.

Run: python3 scripts/retag-taxonomy.py
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXCLUDE_DIRS = {".git", "brand/sunflex-ci", "docs/superpowers/plans"}

# Verified mapping -- do not re-derive, use exactly this (matches the
# sibling task restructuring product-menu-data.js).
SLUG_TO_STAGE = {
    # detect (17)
    "mobile-cctv": "detect", "mobile-bodycam": "detect", "hook-bottom-camera": "detect",
    "chatgpt-cctv": "detect", "safety-box": "detect", "site-cms": "detect",
    "led-logo-light": "detect", "vehicle-entry-alert": "detect",
    "co2-temp-humidity": "detect", "iot-mist": "detect", "lte-anemometer": "detect",
    "smart-environment-board": "detect", "compact-gas-detector": "detect", "gas-alarm": "detect",
    "tilt-acceleration-sensor": "detect", "fire-detection": "detect", "ir3-flame-detector": "detect",
    # alert (14)
    "ai-broadcast": "alert", "wireless-emergency-broadcast": "alert", "digital-radio": "alert",
    "tbm-solution": "alert", "ai-equipment-collision": "alert", "opening-open-close-sensor": "alert",
    "equipment-approach-alarm": "alert", "tower-crane-hook-collision": "alert",
    "emergency-signal-location": "alert", "hazard-area-broadcast": "alert",
    "pedestrian-collision-prevention": "alert", "alcohol-detection": "alert",
    "smart-beacon": "alert", "wireless-network": "alert",
    # respond (7)
    "power-assist-suit": "respond", "smart-safety-hook": "respond", "smart-helmet": "respond",
    "smart-airbag": "respond", "worker-attendance-card": "respond", "worker-access-gate": "respond",
    "healthcare-heart-band": "respond",
    # record (10)
    "ai-quick-risk-assessment": "record", "ai-risk-assessment-review": "record",
    "ai-safety-index": "record", "ai-subcontractor-safety": "record",
    "ai-drone-inspection": "record", "inspectcut": "record",
    "ai-similar-accident-alert": "record", "safebridge": "record",
    "iot-small-tower-crane": "record", "concrete-curing": "record",
}

# Plain category-level rename for solutions/*/index.html's OWN
# data-font-axis, used only for the 4 non-special categories. "air" is
# intentionally omitted -- see module docstring.
CATEGORY_DIRECT = {
    "eyes": "detect",
    "sound": "alert",
    "guard": "respond",
    "story": "record",
}

FONT_AXIS_RE = re.compile(r'data-font-axis="(eyes|sound|air|guard|story)"')
DATA_SENSE_RE = re.compile(r'data-sense="(eyes|sound|air|guard|story)"')
DATA_SLUG_RE = re.compile(r'data-product-card[^>]*?data-slug="([a-z0-9-]+)"')
HREF_PRODUCT_RE = re.compile(r'href="/products/([a-z0-9-]+)"')
CHAPTER_NAV_RE = re.compile(
    r'class="chapter-nav__item"[^>]*?data-sense="(eyes|sound|air|guard|story)"'
)


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


def context_snippet(content, pos, radius=80):
    start = max(0, pos - radius)
    end = min(len(content), pos + radius)
    return content[start:end].replace("\n", " ")


def process_font_axis(path, content):
    """Return (new_content, count, notes) for the single data-font-axis
    attribute in a products/*/index.html or solutions/*/index.html page."""
    relpath = rel(path)
    m = FONT_AXIS_RE.search(content)
    if not m:
        return content, 0, []

    notes = []
    parts = relpath.split(os.sep)
    new_value = None

    if parts[0] == "products" and len(parts) == 3 and parts[2] == "index.html":
        slug = parts[1]
        if slug in SLUG_TO_STAGE:
            new_value = SLUG_TO_STAGE[slug]
        else:
            notes.append(f"BLOCKED data-font-axis: unknown product slug '{slug}'")
    elif parts[0] == "solutions" and len(parts) == 3 and parts[2] == "index.html":
        category = parts[1]
        if category == "safety-box":
            # Per spec: safety-box the product is 'detect', and this
            # solutions sub-page is a per-product page, so match the
            # product's own category directly.
            new_value = "detect"
        elif category == "air":
            notes.append(
                'SKIP data-font-axis="air" in solutions/air/index.html: '
                "page-level category self-identity, splits across "
                "detect/alert per product with no single-value mapping -- "
                "deferred to the solutions/ folder restructuring task "
                "(same treatment as href=\"/solutions/air\" links)"
            )
        elif category in CATEGORY_DIRECT:
            new_value = CATEGORY_DIRECT[category]
        else:
            notes.append(
                f"BLOCKED data-font-axis: unrecognized solutions category '{category}'"
            )

    if new_value is None:
        return content, 0, notes

    new_content, n = FONT_AXIS_RE.subn(f'data-font-axis="{new_value}"', content, count=1)
    return new_content, n, notes


def process_data_sense_products_index(content):
    """products/index.html: skip the 5 chapter-nav (category jump-nav)
    items, context-match the 48 per-product-card items via their nearby
    data-slug attribute."""
    notes = []

    chapter_nav_matches = list(CHAPTER_NAV_RE.finditer(content))
    if chapter_nav_matches:
        cats = ", ".join(m.group(1) for m in chapter_nav_matches)
        notes.append(
            f"SKIP {len(chapter_nav_matches)} chapter-nav__item data-sense "
            f"attrs ({cats}): page-level jump-nav widget (one per OLD sense "
            "category, linking to on-page anchors #sense-eyes etc.), not "
            "per-product-card tags -- structurally identical to the "
            "excluded company/index.html tabs & homepage sense-circle "
            "widgets, a 5->4 rebuild belongs to a separate task"
        )
        for m in chapter_nav_matches:
            notes.append(
                f"  chapter-nav context @ {m.start()}: "
                f"...{context_snippet(content, m.start())}..."
            )

    slug_matches = list(DATA_SLUG_RE.finditer(content))

    pieces = []
    last_end = 0
    replaced = 0
    for i, sm in enumerate(slug_matches):
        slug = sm.group(1)
        window_start = sm.end()
        window_end = (
            slug_matches[i + 1].start() if i + 1 < len(slug_matches) else len(content)
        )
        window = content[window_start:window_end]
        dm = DATA_SENSE_RE.search(window)
        if not dm:
            notes.append(f"BLOCKED: no data-sense found near data-slug=\"{slug}\"")
            continue
        if slug not in SLUG_TO_STAGE:
            notes.append(f"BLOCKED: slug '{slug}' not in SLUG_TO_STAGE")
            continue
        new_stage = SLUG_TO_STAGE[slug]
        abs_start = window_start + dm.start()
        abs_end = window_start + dm.end()
        pieces.append(content[last_end:abs_start])
        pieces.append(f'data-sense="{new_stage}"')
        last_end = abs_end
        replaced += 1
    pieces.append(content[last_end:])
    new_content = "".join(pieces)
    return new_content, replaced, notes


def process_data_sense_solutions(path, content):
    """solutions/{air,eyes,guard,safety-box,sound,story}/index.html:
    context-match each data-sense via the next href="/products/{slug}"
    occurring before the following data-sense (or EOF)."""
    notes = []
    sense_matches = list(DATA_SENSE_RE.finditer(content))
    pieces = []
    last_end = 0
    replaced = 0
    for i, sm in enumerate(sense_matches):
        window_start = sm.end()
        window_end = (
            sense_matches[i + 1].start()
            if i + 1 < len(sense_matches)
            else len(content)
        )
        window = content[window_start:window_end]
        hm = HREF_PRODUCT_RE.search(window)
        if not hm:
            notes.append(
                f'BLOCKED: data-sense="{sm.group(1)}" at offset {sm.start()} '
                f"in {rel(path)} has no href=\"/products/...\" before the "
                "next data-sense occurrence -- cannot attribute to a "
                f"product slug. Context: ...{context_snippet(content, sm.start())}..."
            )
            pieces.append(content[last_end:sm.end()])
            last_end = sm.end()
            continue
        slug = hm.group(1)
        if slug not in SLUG_TO_STAGE:
            notes.append(
                f"BLOCKED: slug '{slug}' (from data-sense context in "
                f"{rel(path)}) not in SLUG_TO_STAGE"
            )
            pieces.append(content[last_end:sm.end()])
            last_end = sm.end()
            continue
        new_stage = SLUG_TO_STAGE[slug]
        pieces.append(content[last_end:sm.start()])
        pieces.append(f'data-sense="{new_stage}"')
        last_end = sm.end()
        replaced += 1
    pieces.append(content[last_end:])
    new_content = "".join(pieces)
    return new_content, replaced, notes


def main():
    total_font_axis = 0
    total_data_sense = 0
    hard_blocked = []

    for path in sorted(find_html_files()):
        relpath = rel(path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        original = content
        file_font = 0
        file_sense = 0
        file_notes = []

        if FONT_AXIS_RE.search(content):
            content, n, notes = process_font_axis(path, content)
            file_font += n
            file_notes.extend(notes)

        if relpath in ("company/index.html", "index.html"):
            if DATA_SENSE_RE.search(content):
                count = len(DATA_SENSE_RE.findall(content))
                file_notes.append(
                    f"SKIP {count} data-sense attrs in {relpath} entirely: "
                    "structural sense-tab / sense-circle widget, 5->4 "
                    "rebuild is out of scope for this task (explicit spec "
                    "exclusion)"
                )
        elif relpath == "products/index.html":
            if DATA_SENSE_RE.search(content):
                content, n, notes = process_data_sense_products_index(content)
                file_sense += n
                file_notes.extend(notes)
        elif (
            relpath.startswith("solutions" + os.sep)
            and relpath.endswith(os.sep + "index.html")
        ):
            if DATA_SENSE_RE.search(content):
                content, n, notes = process_data_sense_solutions(path, content)
                file_sense += n
                file_notes.extend(notes)

        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

        if file_font or file_sense or file_notes:
            print(f"{relpath}: data-font-axis={file_font} data-sense={file_sense}")
            for note in file_notes:
                print(f"  - {note}")
                if note.startswith("BLOCKED"):
                    hard_blocked.append((relpath, note))

        total_font_axis += file_font
        total_data_sense += file_sense

    print()
    print(
        f"TOTAL: data-font-axis changed={total_font_axis}  "
        f"data-sense changed={total_data_sense}"
    )

    if hard_blocked:
        print(f"\n{len(hard_blocked)} unexpected BLOCKED item(s):")
        for relpath, note in hard_blocked:
            print(f"  {relpath}: {note}")
        sys.exit(1)


if __name__ == "__main__":
    main()
