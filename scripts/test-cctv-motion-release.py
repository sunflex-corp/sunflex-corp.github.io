"""Production route, asset and rebuild contract for the approved motion page."""
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import subprocess
from site_studio import enhance
ROOT=Path(__file__).resolve().parents[1]
page=ROOT/'products/mobile-cctv/index.html'
s=BeautifulSoup(page.read_text(),'html.parser')
source=(ROOT/'data/mobile-cctv-motion-page.html').read_text()
assert page.read_text()==enhance(source,'products/mobile-cctv/index.html')
assert str(s.main)==str(BeautifulSoup(source,'html.parser').main)
assert s.body['data-page-design']=='cctv-motion-20260923'
assert not s.select('#motion-toggle,.preview-label,meta[name=robots]')
assert '로컬' not in s.get_text() and 'LOCAL PREVIEW' not in s.get_text()
assert s.select_one('link[rel=canonical]')['href']=='https://sunflex-corp.github.io/products/mobile-cctv/'
assert len(s.select('.story-panel'))==3 and len(s.select('[data-model]'))==3
ids=[n['id'] for n in s.select('[id]')];assert len(ids)==len(set(ids))
for n in s.select('[aria-controls]'): assert n['aria-controls'] in ids
for n in s.select('a[href^="#"]'): assert n['href'][1:] in ids
for n in s.select('script[src],link[href],img[src],a[href]'):
 v=n.get('src',n.get('href'));u=urlsplit(v)
 if u.scheme or not u.path:continue
 path=ROOT/u.path.lstrip('/')
 assert path.is_file() or (path/'index.html').is_file(),v
js=ROOT/'assets/sunflex-v2/cctv-motion/motion.js'
assert 'toggle.' not in js.read_text()
assert 'prefers-reduced-motion' in js.read_text()
subprocess.run(['node','--check',str(js)],check=True)
print('PASS: production route, metadata, 3 scenes, 3 models, local assets, anchors, rebuild source and JS syntax')
