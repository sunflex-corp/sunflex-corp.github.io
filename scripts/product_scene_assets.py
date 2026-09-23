"""Product-photo scenes override generic Blender props without changing flow markup."""
import hashlib
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SCENES = json.loads((ROOT / 'data/product-scene-overrides.json').read_text())


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
    return figures
