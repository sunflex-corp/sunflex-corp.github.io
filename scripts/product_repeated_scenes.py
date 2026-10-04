"""Keep the reviewed later-section images without rewriting surrounding HTML."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEMENTS = {
    'ai-equipment-collision': ('warning-state', 'construction-excavator-access', 2),
    'ai-quick-risk-assessment': ('ai-quick-risk-assessment-flow', 'chatgpt-cctv-selection', 1),
    'ai-risk-assessment-review': ('ai-risk-assessment-review-flow', 'office-integrated-review', 1),
    'ai-safety-index': ('morning-index-line', 'office-integrated-review', 2),
    'ai-similar-accident-alert': ('ai-similar-accident-alert-flow', 'office-training-briefing', 1),
}


def apply_repeated_scenes(text, slug):
    """Patch only existing media attributes in the named section; safe to rerun.

    The published v3 page has separate mobile/desktop images for two scenes.
    Older source rebuilds have one copy there and use the first scene. Both
    /img/3d exports and legacy /media/external-renders URLs are recognized.
    """
    if slug not in PLACEMENTS:
        return text
    section_id, old_stem, count = PLACEMENTS[slug]
    records = json.loads((ROOT / 'data/product-scene-overrides.json').read_text())
    scenes = [records[f'{slug}-{section_id}-{n}-20261004'] for n in range(1, count + 1)]
    section = re.search(r'<section\b[^>]*\bid="' + re.escape(section_id)
                        + r'"[^>]*>.*?</section>', text, re.S)
    if not section:
        return text
    region = section[0]
    known = [old_stem] + [Path(s['asset']).name.removesuffix('-1280.webp') for s in scenes]
    occurrence = 0

    def replace_tag(match):
        nonlocal occurrence
        tag = match[0]
        if not any(stem in tag for stem in known):
            return tag
        # A picture's sources precede its img and share the same scene.
        scene = scenes[min(occurrence, count - 1)]
        new_stem = scene['asset'].removesuffix('-1280.webp')

        def replace_url(url):
            size = re.search(r'-(640|1280)\.webp(?:\?[^\s,]*)?$', url)
            return new_stem + '-' + (size[1] if size else '1280') + '.webp'

        def replace_attr(attr):
            name, value = attr[1], attr[2]
            if name in ('src', 'href', 'xlink:href', 'srcset'):
                value = re.sub(r'/(?:img/3d|media/external-renders)/[^\s,\"]+',
                               lambda u: replace_url(u[0]) if any(s in u[0] for s in known) else u[0], value)
            elif name == 'alt':
                value = escape(scene['alt'], quote=True)
            elif name in ('width', 'height'):
                value = str(scene[name])
            return f'{name}="{value}"'

        tag = re.sub(r'(?<![\w:-])(srcset|src|xlink:href|href|alt|width|height)="([^"]*)"',
                     replace_attr, tag)
        if re.match(r'<(?:img|image)\b', tag):
            occurrence += 1
        return tag

    region = re.sub(r'<(?:source|img|image)\b[^>]*>', replace_tag, region)
    return text[:section.start()] + region + text[section.end():]


if __name__ == '__main__':
    for slug in PLACEMENTS:
        path = ROOT / 'products' / slug / 'index.html'
        before = path.read_text()
        after = apply_repeated_scenes(before, slug)
        if after != before:
            path.write_text(after)
            print(f'Updated later section: {slug}')
