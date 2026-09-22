"""Check image/copy operating cards against the shipped source and navigation."""
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from product_operating_images import STEPS
ROOT = Path(__file__).resolve().parents[1]
BASE = '0c1f29433c21afa6b0f0e7fb669cab0e71503246'
count = 0
for slug, assets in STEPS.items():
 path = f'products/{slug}/index.html'
 old = BeautifulSoup(subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT,text=True),'html.parser')
 new = BeautifulSoup((ROOT/path).read_text(),'html.parser')
 panels = new.select('.operating-image-panel')
 assert len(panels) == len(assets), slug
 before = old.select('.editorial-flow-step[data-flow-panel]')
 for panel, previous in zip(panels, before):
  assert panel['id'] == previous['id'], slug
  # Existing image captions move with the image from the old trailing position.
  a,b = (BeautifulSoup(str(node),'html.parser') for node in (panel,previous))
  assert [n.text for n in a.select('figcaption')] == [n.text for n in b.select('figcaption')], slug
  for n in a.select('figcaption') + b.select('figcaption'): n.decompose()
  assert ' '.join(a.stripped_strings) == ' '.join(b.stripped_strings), (slug, 'copy changed')
  assert panel.select_one(':scope > .operating-step-copy'), slug
  image = panel.select_one(':scope > .operating-step-image img')
  assert image and image.get('alt') and image['loading']=='lazy', slug
  file = ROOT / image['src'].lstrip('/')
  assert Image.open(file).size == (int(image['width']),int(image['height'])), slug
  assert panel.find_parent(attrs={'data-scroll-flow':True}), slug
  count += 1
 for previous in old.select('.product-flow-tabs button'):
  button = new.find(id=previous['id'])
  assert button and button.attrs==previous.attrs and button.text==previous.text, (slug,'navigation changed')
 # The photographic mobile CCTV reference and primary benefit figures stay unchanged.
 assert str(old.select_one('#product-benefits')) == str(new.select_one('#product-benefits')), slug
assert subprocess.check_output(['git','diff',BASE,'--','assets/sunflex-v2/product-flow.js'],cwd=ROOT)==b''
print(f'PASS: {len(STEPS)} products / {count} image-copy cards; source prose, numbered controls, primary benefits and pin controller preserved')
