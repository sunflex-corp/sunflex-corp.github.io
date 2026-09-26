#!/usr/bin/env python3
"""Focused gas pilot checks, independent of pre-existing catalog copy failures."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from product_editorial import apply_copy
ROOT = Path(__file__).resolve().parents[1]
slug = 'compact-gas-detector'
page = ROOT / f'products/{slug}/index.html'
soup = BeautifulSoup(page.read_text(), 'html.parser')
source = BeautifulSoup((ROOT / f'data/solar-products/{slug}.html').read_text(), 'html.parser')
apply_copy(source, slug)
actual = ' '.join(soup.select_one('.product-story').stripped_strings)
assert all(t in actual for t in source.stripped_strings), 'Product fact removed'
assert len(soup.select('h1')) == 1
ids = [n['id'] for n in soup.select('[id]')]
assert len(ids) == len(set(ids)), 'Duplicate ID'
for img in source.select('img'):
    assert soup.find('img', src=img['src']), 'Source image removed'
for node in soup.select('[href],[src]'):
    value = node.get('href') or node.get('src')
    u = urlsplit(value)
    if u.scheme or u.netloc: continue
    dest = ROOT / unquote(u.path).lstrip('/') if u.path.startswith('/') else page.parent / unquote(u.path)
    if not u.path: dest = page
    if dest.is_dir(): dest /= 'index.html'
    assert dest.exists(), value
    if u.fragment and dest.suffix == '.html':
        assert BeautifulSoup(dest.read_text(), 'html.parser').find(id=unquote(u.fragment)), value
controls = soup.select_one('.gas-scene-tabs')
assert controls.has_attr('hidden'), 'No-JS tabs must stay hidden'
tabs = controls.select('[role=tab]')
panels = soup.select('.gas-scene-panel')
assert len(tabs) == len(panels) == 3
for tab, panel in zip(tabs, panels):
    assert tab['aria-controls'] == panel['id']
    assert not panel.has_attr('hidden'), 'No-JS product content must be readable'
assert soup.select_one('.gas-product-media img')['fetchpriority'] == 'high'
assert BeautifulSoup((ROOT/'index.html').read_text(), 'html.parser').main.get_text(' ',strip=True) == BeautifulSoup((ROOT/'data/home-solar-page.html').read_text(), 'html.parser').main.get_text(' ',strip=True), 'Authored home content changed during build'
print('PASS: gas source copy/images, local links/anchors, tab ownership, no-JS markup, hero priority, authored home preservation')
