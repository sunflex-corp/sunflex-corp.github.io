"""Embedded infographic contract; not browser visual QA."""
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
import json,subprocess,re,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE=sys.argv[1] if len(sys.argv)>1 else 'd4e1f83d7780eb623295d0e7cef36b487b38364a'
FIGURES=json.loads((ROOT/'data/product-infographics.json').read_text());media=set();scenes=[]
def canon(n):
 if isinstance(n,NavigableString):return re.sub(r'\s+',' ',str(n)).strip()
 return (n.name,sorted((k,tuple(v) if isinstance(v,list) else v) for k,v in n.attrs.items()),[v for c in n.children if (v:=canon(c))])
def preserved(p):
 # BeautifulSoup lowercases UTF-8 during serialization; encoding names are case-insensitive.
 for im in p.select('img[src*="/site-cms-stage-"]'):
  im['alt']=''
  im.find_parent('figure').figcaption.clear()
 for n in p.select('meta[charset]'):n['charset']=n['charset'].lower()
 for n in p.select('#product-benefits [data-flow-panel] > .benefit-visual, #blind-corner [data-flow-panel] > .pedestrian-scene, #blind-corner [data-flow-panel] > .infographic-visual, link[href*="/product-infographics"]'):n.decompose()
 return canon(p)
for slug in FIGURES:
 file=f'products/{slug}/index.html';p=BeautifulSoup((ROOT/file).read_text(),'html.parser');embeds=p.select('.sunflex-infographic');assert len(embeds)==3,slug
 for i,n in enumerate(embeds,1):
  assert n['data-infographic-scene']==f'{slug}-{i}' and n.get('role')=='group' and n.get('aria-label'),slug
  assert not n.select('button,[role=tab],script') and n.find_parent('li').has_attr('data-flow-panel'),slug
  scenes.append(n['data-infographic-scene'])
  for im in n.select('img'):
   assert im.get('alt') and (ROOT/im['src'].lstrip('/')).is_file(),slug
   assert (int(im['width']),int(im['height']))==Image.open(ROOT/im['src'].lstrip('/')).size,slug
   assert im.get('width')=='1600' and im.get('height') in ['900','1200'],slug
   media.add(im['src'])
  assert len(n.find_parent('figure').select('figcaption'))==1,slug
  if n.select('img'):assert len(n.select('.object-marker'))==len(n.select('.render-annotations li'))>0,(slug,i)
  assert not n.select('.data-row>b'),(slug,i)
 ids=[n['id'] for n in p.select('[id]')];assert len(ids)==len(set(ids)),slug
 for n in p.select('[aria-controls]'):assert p.find(id=n['aria-controls']),(slug,n['aria-controls'])
 for n in p.select('a[href^="#"]'):
  if n['href']!='#':assert p.find(id=n['href'][1:]),(slug,n['href'])
 for name in ['product-infographics','product-infographics-layout']:assert len(p.select(f'link[href*="/{name}.css?"]'))==1,slug
 old=BeautifulSoup(subprocess.check_output(['git','show',f'{BASE}:{file}'],cwd=ROOT,text=True),'html.parser')
 assert preserved(p)==preserved(old),f'Unexpected non-visual change: {slug}'
assert len(scenes)==len(set(scenes))==144 and len(media)==31
for slug,langs in {'ai-broadcast':['베트남어','태국어','중국어'],'tower-crane-hook-collision':['한국어','중국어','베트남어'],'safebridge':['중국어','힌디어','영어']}.items():
 p=BeautifulSoup((ROOT/f'products/{slug}/index.html').read_text(),'html.parser')
 assert [n.get_text() for n in p.select('.sunflex-infographic .language-lanes strong')]==langs
for slug in ['chatgpt-cctv','ai-quick-risk-assessment']:
 assert 'data-sheet' in FIGURES[slug][1] and 'operation-chain' in FIGURES[slug][2],slug
for slug,selector,count in [('co2-temp-humidity','.metric-mark path',3),('smart-environment-board','.instrument-icon path',3),('safety-box','.hub-node path,.tile-icon path',4)]:
 s=BeautifulSoup(FIGURES[slug][1 if slug=='smart-environment-board' else 0],'html.parser')
 assert len({n['d'] for n in s.select(selector)})==count,slug
for slug,step in [('wireless-network',1),('ai-safety-index',0)]:assert '전체 공지' not in FIGURES[slug][step],slug
cms=BeautifulSoup((ROOT/'products/site-cms/index.html').read_text(),'html.parser')
for key,alt in {'early':'굴착 장비와 차량이 작업 중인 착공 초기 현장','mid':'타워크레인과 여러 층의 골조가 형성된 공정 전환 현장','late':'외벽 공사와 지상부 정리가 진행 중인 준공 전 현장'}.items():
 im=cms.select_one(f'img[src="/media/derived/site-cms-stage-{key}-768.avif"]')
 assert im['alt']==im.find_parent('figure').figcaption.get_text()==alt
print('PASS: 48 pages / 144 scenes / 31 assets; non-visual content, anchors, controls and language examples preserved')
