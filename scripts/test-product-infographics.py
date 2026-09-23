"""Embedded infographic contract; not browser visual QA."""
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
import json,subprocess,re,sys
from PIL import Image
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
BASE=sys.argv[1] if len(sys.argv)>1 else 'd4e1f83d7780eb623295d0e7cef36b487b38364a'
FIGURES=json.loads((ROOT/'data/product-infographics.json').read_text());media=set();scenes=[]
EXTERNAL=json.loads((ROOT/'data/external-render-assets.json').read_text())
def canon(n):
 if isinstance(n,NavigableString):return re.sub(r'\s+',' ',str(n)).strip()
 return (n.name,sorted((k,tuple(v) if isinstance(v,list) else v) for k,v in n.attrs.items()),[v for c in n.children if (v:=canon(c))])
def preserved(p,slug):
 # Shared motion adds only owned runtime tags and a root ownership marker.
 for n in p.select('[data-site-motion]'):n.decompose()
 if p.html:p.html.attrs.pop('data-motion-engine',None)
 # These two buyer-facing sections have an explicit, idempotent revision.
 # Normalize only that reviewed transform; unrelated source content is compared.
 from product_buyer_proof import refine_proof
 refine_proof(p,p.select_one('.product-story'),slug)
 if slug=='mobile-cctv':
  from product_buyer_mobile import refine_mobile
  refine_mobile(p,p.select_one('.product-story'))
  for n in p.select('link[href*="/product-buyer-mobile.css"]'):n.decompose()
 from product_external_contexts import refine_external_contexts
 refine_external_contexts(p,p.select_one('.product-story'),slug)
 if slug=='mobile-cctv':
  from product_buyer_mobile import refine_installation_brief
  refine_installation_brief(p,p.select_one('.product-story'))
 from product_operating_images import refine_operating_images
 refine_operating_images(p,p.select_one('.product-story'),slug)
 # Intentional removal of one repeated photo; all checkpoint prose remains compared.
 if slug=='hook-bottom-camera':
  duplicate=p.select_one('#hook-checkpoints figure')
  if duplicate and duplicate.select_one('img[src="/media/derived/product-hook-bottom-camera-problem-2560.avif"]'):
   duplicate.decompose()
 # Layout assets intentionally change in this review; their cache keys are not prose.
 for n in p.select('link[href],script[src]'):
  key='href' if n.name=='link' else 'src'
  if re.search(r'/product-(flow|revision|motion)\.(css|js)\?v=',n[key]):
   n[key]=n[key].split('?')[0]
 # Approved copy revisions are constrained to their exact page and exact former/new pairs.
 copy_revisions={
  'mobile-bodycam':{
   '운영 환경에 맞는 모델':'지나간 장면도 기록으로',
   '일반형·WiFi형·LTE형 중 현장의 저장·전송 방식에 맞춰 구성을 검토합니다.':'되돌아가기 어려운 작업 장면을 그때 그대로 남겨 둡니다.'},
  'ai-drone-inspection':{
   '사진과 위치를, 점검 자료로 함께':'이제, 위치 기록은 드론이 합니다',
   '촬영 위치와 사진을 함께 확인해 보수나 추가 점검이 필요한 구간을 논의합니다.':'촬영 위치와 사진을 함께 확인해 점검한 구간을 찾을 수 있습니다. 회의에서도 같은 자료를 보며 보수나 추가 점검이 필요한 곳을 논의합니다.'},
  'concrete-curing':{
   '기록을 현장 기준과 대조해':'감이 아니라 측정으로 보는 탈형 시점',
   '온도·적산온도·강도 추정값을 현장 기준과 비교해 다음 공정을 검토합니다.':'온도·적산온도·강도 추정값을 현장 기준과 비교하며 탈형 시점과 다음 공정 일정을 검토합니다.',
   '온도 기록에서강도 추정까지':'적산온도강도 추정까지',
   '타설 위치별 온도 기록이 적산온도와 강도 추정값으로 이어집니다.':'타설 위치별 온도가 적산온도와 강도 추정값으로 이어져 같은 기록에 남습니다.',
   '위치별 기록을 비교해':'위치마다 쌓이는 온도 기록',
   '부재와 구간에 따른 온도 변화를 비교해 양생 상태를 살펴봅니다.':'타설 위치별 온도 변화가 기록됩니다. 담당자는 기록과 강도 추정값을 현장 기준과 비교해 양생 상태를 검토합니다.'},
  'iot-small-tower-crane':{
   '조종석 한 화면에서 함께 확인':'3 가지를 한 번에',
   '인양 중량·후크 거리·지브각·풍속을 조종석에서 함께 확인합니다.':'흩어져 있던 확인이 조종석 한 화면에 모입니다. 계기를 번갈아 보지 않고 직관적으로 한눈에 확인할 수 있습니다.'}}
 copy=copy_revisions.get(slug,{})
 approved={''.join(text.split()):old for new,old in copy.items() for text in (new,old)}
 for n in p.select('#highlights h3,#highlights p'):
  signature=''.join(n.get_text().split())
  if signature in approved:n.string=approved[signature]
 # Intentional layout-only component variants; preserve all their contents.
 for n in p.select('[data-revision-surface],[data-highlight-card]'):
  n.attrs.pop('data-revision-surface',None);n.attrs.pop('data-highlight-card',None)
 for n in p.select('.pedestrian-story-panel.flow-with-image'):
  n['class']=[c for c in n['class'] if c!='flow-with-image']
 # BeautifulSoup lowercases UTF-8 during serialization; encoding names are case-insensitive.
 for im in p.select('img[src*="/site-cms-stage-"]'):
  im['alt']=''
  im.find_parent('figure').figcaption.clear()
 for n in p.select('meta[charset]'):n['charset']=n['charset'].lower()
 for n in p.select('#product-benefits [data-flow-panel] > .benefit-visual, #blind-corner [data-flow-panel] > .pedestrian-scene, #blind-corner [data-flow-panel] > .infographic-visual, link[href*="/product-infographics"]'):n.decompose()
 return canon(p)
for slug in FIGURES:
 if slug=='mobile-cctv':
  subprocess.run([sys.executable,str(ROOT/'scripts/test-cctv-motion-release.py')],check=True)
  continue  # Approved standalone photo scenes are tested by their own contract.
 file=f'products/{slug}/index.html';p=BeautifulSoup((ROOT/file).read_text(),'html.parser');embeds=p.select('.sunflex-infographic');assert len(embeds)==3,slug
 for i,n in enumerate(embeds,1):
  assert n['data-infographic-scene']==f'{slug}-{i}' and n.get('role')=='group' and n.get('aria-label'),slug
  assert not n.select('button,[role=tab],script') and n.find_parent('li').has_attr('data-flow-panel'),slug
  scenes.append(n['data-infographic-scene'])
  for im in n.select('img'):
   assert im.get('alt') and (ROOT/urlsplit(im['src']).path.lstrip('/')).is_file(),slug
   assert (int(im['width']),int(im['height']))==Image.open(ROOT/urlsplit(im['src']).path.lstrip('/')).size,slug
   assert '/external-renders/' in im['src'],(slug,i,'Legacy illustration remains')
   assert im.get('width')=='1800' and im.get('height')=='1200',slug
   media.add(urlsplit(im['src']).path)
  assert not n.select('svg,.operation-chain,.scene-drawing,.data-sheet'),(slug,i,'HTML illustration remains')
  assert n.find_parent('figure').get('data-infographic-version')=='20260923-external'
  assert len(n.find_parent('figure').select('figcaption'))==1,slug
  for singleton in ['qa-deploy-flow','qa-detected-person','qa-part-link','qa-lift-poses','qa-case-transfer']:
   assert len(n.select('.'+singleton))<=1,(slug,i,'Repeated visual component',singleton)
  if n.select('.render-stage img'):assert len(n.select('.object-marker'))==len(n.select('.render-annotations li'))>0,(slug,i)
  assert not n.select('.data-row>b'),(slug,i)
 ids=[n['id'] for n in p.select('[id]')];assert len(ids)==len(set(ids)),slug
 for n in p.select('[aria-controls]'):assert p.find(id=n['aria-controls']),(slug,n['aria-controls'])
 for n in p.select('a[href^="#"]'):
  if n['href']!='#':assert p.find(id=n['href'][1:]),(slug,n['href'])
 for name in ['product-infographics','product-infographics-layout']:assert len(p.select(f'link[href*="/{name}.css?"]'))==1,slug
 old=BeautifulSoup(subprocess.check_output(['git','show',f'{BASE}:{file}'],cwd=ROOT,text=True),'html.parser')
 assert preserved(p,slug)==preserved(old,slug),f'Unexpected non-visual change: {slug}'
active_external={k:v for k,v in EXTERNAL.items() if not k.startswith('mobile-cctv-')}
assert len(scenes)==len(set(scenes))==len(active_external)==141
assert len(media)==len(set(x['render'] for x in active_external.values()))
for slug,langs in {'ai-broadcast':['베트남어','태국어','중국어'],'tower-crane-hook-collision':['한국어','중국어','베트남어'],'safebridge':['중국어','힌디어','영어']}.items():
 p=BeautifulSoup((ROOT/f'products/{slug}/index.html').read_text(),'html.parser')
 assert all(lang in p.get_text() for lang in langs),(slug,'Documented languages removed')
for slug,step in [('wireless-network',1),('ai-safety-index',0)]:assert '전체 공지' not in FIGURES[slug][step],slug
cms=BeautifulSoup((ROOT/'products/site-cms/index.html').read_text(),'html.parser')
for key,alt in {'early':'굴착 장비와 차량이 작업 중인 착공 초기 현장','mid':'타워크레인과 여러 층의 골조가 형성된 공정 전환 현장','late':'외벽 공사와 지상부 정리가 진행 중인 준공 전 현장'}.items():
 im=cms.select_one(f'img[src="/media/derived/site-cms-stage-{key}-768.avif"]')
 assert im['alt']==im.find_parent('figure').figcaption.get_text()==alt
print(f'PASS: 47 infographic pages / 141 external figures + 1 photographic motion page / {len(media)} context renders; non-visual content, anchors, controls and language examples preserved')

# Preserve all four specified gases, including hydrogen sulfide.
gas=(ROOT/"products/compact-gas-detector/index.html").read_text()
from bs4 import BeautifulSoup
labels=BeautifulSoup(gas,"html.parser").select_one("#product-benefits .benefit-description").get_text(" ",strip=True)
assert all(g in labels for g in ["O₂","CO","CH₄","H₂S"]),labels
