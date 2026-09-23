"""Check product identity mapping, six replacements and unchanged page interactions."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from product_scene_assets import ROOT, SCENES, apply_scene_overrides
from product_external_contexts import refine_external_contexts

base = sys.argv[1] if len(sys.argv) > 1 else 'fbf5b374b469600be30f74dfb69c93da77f3b2b1'
figures = json.loads((ROOT / 'data/product-infographics.json').read_text())
assert apply_scene_overrides(json.loads(json.dumps(figures))) == figures
count = 0
for scene_id, scene in SCENES.items():
    slug, _ = scene_id.rsplit('-', 1)
    asset = ROOT / scene['asset'].lstrip('/')
    assert Image.open(asset).size == (scene['width'], scene['height'])
    assert hashlib.sha256(asset.read_bytes()).hexdigest() == scene['sha256']
    assert (ROOT / scene['reference'].lstrip('/')).is_file()
    assert asset.stat().st_size < 250_000
    rel = f'products/{slug}/index.html'
    old = BeautifulSoup(subprocess.check_output(['git', 'show', f'{base}:{rel}'], cwd=ROOT, text=True), 'html.parser')
    new = BeautifulSoup((ROOT / rel).read_text(), 'html.parser')
    previous = old.select('img[src*="context-safety-preparation.webp"], img[src*="/product-scenes/"]')
    current = new.select('img[src*="/product-scenes/"]')
    assert len(previous) == len(current) == (2 if slug == 'healthcare-heart-band' else 1)
    for before, after in zip(previous, current):
        assert after['src'].split('?')[0] == scene['asset']
        assert after['alt'] == scene['alt']
        # Mask the permitted image/caption changes; every other DOM node, product
        # photo, link, script, flow selector and piece of copy must be unchanged.
        before.attrs = after.attrs.copy()
        before_figure, after_figure = before.find_parent('figure'), after.find_parent('figure')
        before_figure.attrs = after_figure.attrs.copy()
        before_figure.figcaption.string = after_figure.figcaption.get_text()
    # Motion bundles have independently verified content hashes and may change
    # between image releases. Ignore only their version query, not path/order.
    for document in (old, new):
        for tag in document.select('script[src], link[href]'):
            attr = 'src' if tag.name == 'script' else 'href'
            path = tag[attr].split('?')[0]
            if path in ('/assets/sunflex-v2/site-motion.js', '/assets/sunflex-v2/site-motion.css'):
                tag[attr] = path
    assert str(old) == str(new), (slug, 'unrelated page change')
    assert new.select_one('#product-benefits [data-visual-kind="product-scene"] img')
    assert len(new.select('#product-benefits [data-flow-panel]')) == 3
    count += len(current)

    # A clean detail build must choose this product scene, not the generic props.
    fixture = BeautifulSoup('<main><div class="editorial-diagram"><p>착용 확인</p></div></main>', 'html.parser')
    refine_external_contexts(fixture, fixture.main, slug)
    assert fixture.select_one('.external-detail-render img')['src'].split('?')[0] == scene['asset']

assert count == 6 and len(SCENES) == 5
assert not any('context-safety-preparation.webp' in p.read_text() for p in (ROOT / 'products').glob('*/index.html'))
print('PASS: 5 distinct product scenes / 6 placements; sources, dimensions, sizes, hashes, rebuild persistence and unchanged copy/flow markup.')
