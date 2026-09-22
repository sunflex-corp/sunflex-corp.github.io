"""Consolidated product journeys. Original specifications and anchors remain reachable."""
import json
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape as e
from product_story_visuals import SCENES
ROOT=Path(__file__).resolve().parents[1]
PROFILES=json.loads((ROOT/'data/product-editorial-map.json').read_text())
PROOF={
 'smart-airbag':('manual-smart-airbag-figure-1280.webp','미전개 상태와 전개 후 보호부를 비교한 제품 자료','전개 전과 후. 보호부의 변화를 살펴보세요.'),
 'chatgpt-cctv':('manual-chatgpt-cctv-figure-768.webp','CCTV 선택 목록과 영상 분석 보고서가 함께 표시된 제품 화면','선택한 장면과 보고서를 함께.'),
 'inspectcut':('manual-inspectcut-figure-1280.webp','건설 현장 영상과 재생 컨트롤이 있는 인스펙트컷 화면','필요한 장면을 찾는 실제 작업 화면.'),
 'safebridge':('manual-safebridge-figure-1280.webp','중국어·힌디어·영어 번역 패널이 나란히 표시된 세이프브릿지 화면','한 화면에 나란히, 언어별 자막.')}
# Key choices remain open; duplicate explanations become a single compact specification area.
KEEP={'mobile-cctv':['mobile-cctv-lineup','movingcam-engineering','movingcam-network'],'ir3-flame-detector':['ir3-configurations'],'mobile-bodycam':['bodycam-use'],'pedestrian-collision-prevention':['blind-corner']}

def refine(body,slug):
 s=BeautifulSoup(body,'html.parser');spec=SCENES[slug];root=s.select_one('.product-story');root['data-story-revision']='20260920'
 # The adjacent checkpoint story repeats the preceding scene without new visual information.
 if slug=='hook-bottom-camera':
  duplicate=root.select_one('#hook-checkpoints figure')
  if duplicate and duplicate.select_one('img[src="/media/derived/product-hook-bottom-camera-problem-2560.avif"]'):
   duplicate.decompose()
 overview=root.select_one('.editorial-overview')
 if overview:overview.decompose()
 for link in s.select('a[href="#product-content"]'):link['href']='#blind-corner' if slug=='pedestrian-collision-prevention' else '#product-benefits'
 # The product's initial state should be readable without scrolling through a second pin.
 for wrapper in root.select('.editorial-hero-scroll'):wrapper.unwrap()
 hero=root.select_one('.editorial-hero');hero['data-story-family']=spec['reference'][0]
 # Fix nested source wrapper widths while keeping factual hero content.
 for node in hero.select('.content-wrap,.content-copy'):node['class']=node.get('class',[])+['revision-hero-content']
 # Existing operating sequences retain their numbered, pinned navigation.
 # Convert the older CCTV scene markup to the same controller to avoid competing scroll owners.
 for old in root.select('[data-cctv-process]'):
  old.attrs.pop('data-cctv-process',None)
  track=old.select_one('.cctv-scroll-track');stage=old.select_one('.cctv-scroll-stage')
  controls=old.select_one('.cctv-step-controls')
  if track and stage and controls:
   track['class']=['product-flow-track'];track['data-scroll-flow']=''
   stage['class']=['product-flow-stage'];controls['class']=['product-flow-tabs']
   listing=s.new_tag('ol',attrs={'class':'editorial-flow benefit-panels'})
   for panel in list(stage.select('.cctv-stage')):
    panel.name='li';panel['class']=['benefit-panel'];panel['data-flow-panel']=''
    image=panel.find('img');visual=s.new_tag('figure',attrs={'class':'benefit-visual story-photo-scene'})
    visual.append(image.extract());panel.insert(0,visual)
    panel.select_one('.cctv-stage-caption')['class']=['benefit-copy']
    listing.append(panel.extract())
   stage.append(listing)
 summary=s.new_tag('section',attrs={'class':'editorial-chapter revision-choices','id':'product-fit','data-revision-surface':'checklist'})
 inner=s.new_tag('div',attrs={'class':'editorial-section-inner'})
 inner.append(BeautifulSoup('<p class="editorial-kicker">현장에 맞는 구성</p><h2>도입 전에 확인할 세 가지.</h2><p>설치할 곳과 운영 방식을 함께 살펴보세요. 상담할 때 아래 조건을 알려주시면 구성을 검토하는 데 도움이 됩니다.</p>','html.parser'))
 listing=s.new_tag('ul',attrs={'class':'revision-criteria'})
 for n,c in enumerate(spec['criteria'],1):
  li=s.new_tag('li');li.append(BeautifulSoup(f'<span aria-hidden="true">{n:02}</span><strong>{e(c)}</strong>','html.parser'));listing.append(li)
 inner.append(listing);summary.append(inner)
 appendix=s.new_tag('section',attrs={'class':'editorial-chapter revision-details','id':'product-specifications'})
 inset=s.new_tag('div',attrs={'class':'editorial-section-inner'})
 inset.append(BeautifulSoup('<p class="editorial-kicker">제품 상세</p><h2>구성과 운영, 더 자세히.</h2><p>제품 구성부터 설치 조건까지, 아래에서 차례로 확인하세요.</p>','html.parser'))
 for sec in list(root.find_all('section',recursive=False)):
  ident=sec.get('id','')
  if sec==hero or ident in ['product-benefits']+KEEP.get(slug,[]):continue
  sec['class']=sec.get('class',[])+['revision-source']
  inset.append(sec.extract())
 appendix.append(inset)
 if slug in PROOF:
  filename,alt,title=PROOF[slug]
  from PIL import Image
  w,h=Image.open(ROOT/'media/derived'/filename).size
  evidence=f'<section class="editorial-chapter revision-proof"><div class="editorial-section-inner"><p class="editorial-kicker">제품 자료로 살펴보기</p><h2>{e(title)}</h2><a href="/media/derived/{filename}" target="_blank" rel="noopener" aria-label="{e(alt)} — 원본 크게 보기"><img src="/media/derived/{filename}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"><span>자료 크게 보기 ↗</span></a></div></section>'
  root.append(BeautifulSoup(evidence,'html.parser'))
 root.append(summary);root.append(appendix)
 # Give each product family its own editorial rhythm instead of a stack of identical cards.
 family=root.get('data-archetype','workflow')
 root['data-layout-family']=family
 root['data-motion-profile']=spec['kind']
 sections=list(inset.select(':scope > .revision-source'))
 tail=appendix
 for index,section in enumerate(sections):
  section.extract();tail.insert_after(section);tail=section
  section['data-layout-position']=str(index)
  pairs=section.select('.content-grid[data-items="2"]')
  for grid in pairs:
   if grid.find('figure',recursive=False) and grid.select_one(':scope > .content-copy'):
    layout={'lineup':'panorama','wearable':'portrait','sensing':'instrument','workspace':'canvas','workflow':'canvas','communication':'panorama'}.get(family,'portrait')
    if index%2 and layout=='panorama':layout='editorial'
    grid['data-composition']=layout
  for grid in section.select('.content-grid'):
   cards=grid.find_all('article',recursive=False)
   if len(cards)>=3:grid['data-composition']='mosaic'
   if section.get('id')=='highlights' and cards:
    grid['data-revision-surface']='highlights'
    for card_index,card in enumerate(cards):
     card['data-highlight-card']='feature' if card_index==0 and card.find('img') else 'detail'
 # Replace a repeated benefit with a distinct, documented model-selection point.
 if slug=='mobile-bodycam':
  for card in root.select('#highlights article'):
   title=card.find('h3')
   if title and title.get_text(strip=True)=='지나간 장면도 기록으로':
    title.string='운영 환경에 맞는 모델'
    card.find('p').string='일반형·WiFi형·LTE형 중 현장의 저장·전송 방식에 맞춰 구성을 검토합니다.'
 # Give repeated highlight statements one documented role each: mechanism, record, then use.
 if slug=='ai-drone-inspection':
  for card in root.select('#highlights article'):
   title=card.find('h3')
   if title and title.get_text(strip=True)=='이제, 위치 기록은 드론이 합니다':
    title.string='사진과 위치를, 점검 자료로 함께'
    card.find('p').string='촬영 위치와 사진을 함께 확인해 보수나 추가 점검이 필요한 구간을 논의합니다.'
 if slug=='concrete-curing':
  for card in root.select('#highlights article'):
   title=card.find('h3')
   if title and title.get_text(strip=True)=='감이 아니라 측정으로 보는 탈형 시점':
    title.string='기록을 현장 기준과 대조해'
    card.find('p').string='온도·적산온도·강도 추정값을 현장 기준과 비교해 다음 공정을 검토합니다.'
   elif title and title.get_text(strip=True)=='위치마다 쌓이는 온도 기록':
    title.string='위치별 기록을 비교해'
    card.find('p').string='부재와 구간에 따른 온도 변화를 비교해 양생 상태를 살펴봅니다.'
   elif card.get_text(' ',strip=True).startswith('적산온도 강도 추정까지'):
    lines=card.find_all('p',recursive=False)
    lines[0].clear();lines[0].append(BeautifulSoup('<span>온도 기록에서</span><span>강도 추정까지</span>','html.parser'))
    lines[1].string='타설 위치별 온도 기록이 적산온도와 강도 추정값으로 이어집니다.'
 if slug=='iot-small-tower-crane':
  for card in root.select('#highlights article'):
   if card.get_text(' ',strip=True).startswith('3 가지를 한 번에'):
    lines=card.find_all('p',recursive=False)
    lines[0].clear();lines[0].append(BeautifulSoup('<span>조종석 한 화면</span><span>에서 함께 확인</span>','html.parser'))
    lines[1].string='인양 중량·후크 거리·지브각·풍속을 조종석에서 함께 확인합니다.'
 # Preserve parallel comparisons as actual columns instead of tall nested boxes.
 for diagram in root.select('.editorial-diagram'):
  children=diagram.find_all(recursive=False)
  if len(children)==3 and children[1].get('aria-hidden')=='true' and all(c.get('aria-hidden')!='true' for c in [children[0],children[2]]):
   diagram['data-diagram-layout']='transfer-2'
  elif len(children)==5 and all(children[i].get('aria-hidden')=='true' for i in [1,3]):
   diagram['data-diagram-layout']='transfer-3'
  elif len(children)==2 and children[0].name=='ul' and 'editorial-step-card' in children[1].get('class',[]):
   diagram['data-diagram-layout']='summary-2'
 for empty in root.select('dl:empty'):empty.decompose()
 for br in root.select('#movingcam-engineering h2 br'):br.replace_with(' ')
 # Lead software pages with available actual output, before the operating story.
 if family in ['workspace','workflow']:
  proof=root.select_one('.revision-proof')
  if proof:hero.insert_after(proof.extract())
 # Product information stays visible without disclosure controls, including nested source details.
 for detail in list(s.select('details:not(.solar-menu)')):
  detail.name='div'
  detail.attrs.pop('open',None)
  detail['class']=detail.get('class',[])+['revision-visible-detail']
  title=detail.find('summary',recursive=False)
  if title:
   title.name='p'
   title['class']=['revision-detail-label']
 # Existing section IDs continue to support direct navigation.
 nav=s.select_one('.product-local-nav nav')
 if nav:
  links=nav.find_all('a');links[1]['href']='#product-specifications';links[1].string='구성·사양'
 from product_buyer_proof import refine_proof
 refine_proof(s,root,slug)
 if slug=='mobile-cctv':
  from product_buyer_mobile import refine_mobile
  refine_mobile(s,root)
 from product_external_contexts import refine_external_contexts
 refine_external_contexts(s,root,slug)
 from product_operating_images import refine_operating_images
 refine_operating_images(s,root,slug)
 return str(s)
