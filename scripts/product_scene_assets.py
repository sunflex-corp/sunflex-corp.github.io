"""Product-photo scenes override generic Blender props without changing flow markup."""
import hashlib
import json
import re
from html import escape
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
_OVERRIDES = json.loads((ROOT / 'data/product-scene-overrides.json').read_text())
# Only legacy, unversioned numbered keys belong to infographic placements.
# Dated hero/highlight/benefit/section records are applied by their own helpers.
SCENES = {key: value for key, value in _OVERRIDES.items()
          if re.fullmatch(r'.+-[1-9]\d?', key)}
BENEFIT_SCENES = {
    (match[1], int(match[2])): value
    for key, value in _OVERRIDES.items()
    if (match := re.fullmatch(r'(.+)-benefit-(\d+)-20261004', key))
}
HERO_SCENES = {key.rsplit('-hero-', 1)[0]: value
               for key, value in _OVERRIDES.items() if '-hero-' in key}
HIGHLIGHT_SCENES = {key.rsplit('-hl-0-', 1)[0]: value
                    for key, value in _OVERRIDES.items() if '-hl-0-' in key}


def highlight_scene_figure(slug):
    """Keep the first highlight's approved 3D asset on source-based rebuilds."""
    scene = HIGHLIGHT_SCENES.get(slug)
    if not scene:
        return None
    stem = scene['asset'].removesuffix('-1280.webp')
    return (f'<figure class="pd-fig pd-card-fig is-hl3d"><img src="{stem}-640.webp" '
            f'srcset="{stem}-640.webp 640w, {stem}-1280.webp 1280w" '
            'sizes="(max-width:600px) 90vw, 420px" alt="" width="1280" height="960" '
            'loading="lazy" decoding="async" data-3d></figure>')


def hero_scene_picture(slug):
    scene = HERO_SCENES.get(slug)
    if not scene:
        return None
    stem = scene['asset'].removesuffix('-2560.webp')
    widths = (2560, 1600, 1280, 768, 480)
    def srcset(ext):
        return ', '.join(f'{stem}-{width}.{ext} {width}w' for width in widths)
    source_sizes = '(max-width: 760px) 90vw, 680px'
    image_sizes = '(max-width: 760px) 90vw, (max-width: 1100px) 48vw, 680px'
    return (f'<picture><source sizes="{source_sizes}" srcset="{srcset("avif")}" type="image/avif"/>'
            f'<source sizes="{source_sizes}" srcset="{srcset("webp")}" type="image/webp"/>'
            f'<img alt="{escape(scene["alt"], quote=True)}" decoding="async" fetchpriority="high" '
            f'height="{scene["height"]}" loading="eager" sizes="{image_sizes}" '
            f'src="{stem}-1280.webp" srcset="{srcset("webp")}" width="{scene["width"]}"/></picture>')


def scene_image(scene):
    path = ROOT / scene['asset'].lstrip('/')
    version = hashlib.sha256(path.read_bytes()).hexdigest()[:10]
    return {
        'src': scene['asset'] + '?v=' + version,
        'width': str(scene['width']),
        'height': str(scene['height']),
        'alt': scene['alt'],
    }


def replace_scene_figure(markup, scene_id):
    scene = SCENES.get(scene_id)
    if not scene:
        return markup
    image_match = re.search(r'<img\b[^>]*>', markup)
    if not image_match:
        raise ValueError(f'Missing image: {scene_id}')
    image = BeautifulSoup(image_match[0], 'html.parser').img
    image.attrs.update(scene_image(scene))
    markup = markup[:image_match.start()] + str(image) + markup[image_match.end():]
    markup = re.sub(r'data-visual-kind="[^"]*"', 'data-visual-kind="product-scene"', markup, count=1)
    markup = re.sub(r'(<figcaption\b[^>]*>).*?(</figcaption>)',
                    lambda m: m[1] + scene['caption'] + m[2], markup, count=1, flags=re.S)
    return markup


def apply_scene_overrides(figures):
    for scene_id in SCENES:
        slug, step = scene_id.rsplit('-', 1)
        figures[slug][int(step) - 1] = replace_scene_figure(figures[slug][int(step) - 1], scene_id)
    return apply_benefit_scene_overrides(figures)


def replace_benefit_scene(markup, slug, step):
    """Replace only image URLs and existing alt text; retain layout and copy."""
    scene = BENEFIT_SCENES.get((slug, step))
    if not scene:
        return markup
    match = re.search(r'<(?:img|image)\b[^>]*>', markup)
    if not match:
        raise ValueError(f'Missing benefit image: {slug}-{step}')
    image = match[0]
    stem = scene['asset'].removesuffix('-1280.webp')
    values = {
        'src': scene['asset'],
        'href': scene['asset'],
        'srcset': f'{stem}-640.webp 640w, {stem}-1280.webp 1280w',
        'alt': scene['alt'],
    }
    for attr, value in values.items():
        image = re.sub(r'(?<![\w:-])' + attr + r'="[^"]*"',
                       lambda m: f'{attr}="{escape(value, quote=True)}"', image)
    return markup[:match.start()] + image + markup[match.end():]


def apply_benefit_scene_overrides(figures):
    for slug, step in BENEFIT_SCENES:
        if slug in figures and step <= len(figures[slug]):
            figures[slug][step - 1] = replace_benefit_scene(
                figures[slug][step - 1], slug, step)
    return figures
