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
KEEP={'mobile-cctv':['mobile-cctv-lineup','movingcam-network'],'ir3-flame-detector':['ir3-configurations'],'mobile-bodycam':['bodycam-use'],'pedestrian-collision-prevention':['blind-corner']}

def refine(body,slug):
 s=BeautifulSoup(body,'html.parser');spec=SCENES[slug];root=s.select_one('.product-story');root['data-story-revision']='20260920'
 overview=root.select_one('.editorial-overview')
 if overview:overview.decompose()
 for link in s.select('a[href="#product-content"]'):link['href']='#blind-corner' if slug=='pedestrian-collision-prevention' else '#product-benefits'
 # The product's initial state should be readable without scrolling through a second pin.
 for wrapper in root.select('.editorial-hero-scroll'):wrapper.unwrap()
 hero=root.select_one('.editorial-hero');hero['data-story-family']=spec['reference'][0]
 # Fix nested source wrapper widths while keeping factual hero content.
 for node in hero.select('.content-wrap,.content-copy'):node['class']=node.get('class',[])+['revision-hero-content']
 for track in root.select('[data-scroll-flow]'):
  if track.find_parent(class_='benefit-chapter') or slug=='pedestrian-collision-prevention' and track.find_parent(id='blind-corner'):continue
  track.attrs.pop('data-scroll-flow',None)
  controls=track.select_one('.product-flow-tabs')
  if controls:controls.decompose()
  for panel in track.select('[data-flow-panel]'):panel.attrs.pop('data-flow-panel',None)
 # Old CCTV scroll sequence is now a static optional reference, not another pin.
 for node in root.select('[data-cctv-process]'):node.attrs.pop('data-cctv-process',None)
 for controls in root.select('.cctv-step-controls'):controls.decompose()
 summary=s.new_tag('section',attrs={'class':'editorial-chapter revision-choices','id':'product-fit'})
 inner=s.new_tag('div',attrs={'class':'editorial-section-inner'})
 inner.append(BeautifulSoup('<p class="editorial-kicker">현장에 맞는 구성</p><h2>도입 전에 확인할 세 가지.</h2><p>설치할 곳과 운영 방식을 함께 살펴보세요. 상담할 때 아래 조건을 알려주시면 구성을 검토하는 데 도움이 됩니다.</p>','html.parser'))
 listing=s.new_tag('ul',attrs={'class':'revision-criteria'})
 for n,c in enumerate(spec['criteria'],1):
  li=s.new_tag('li');li.append(BeautifulSoup(f'<span aria-hidden="true">{n:02}</span><strong>{e(c)}</strong>','html.parser'));listing.append(li)
 inner.append(listing);summary.append(inner)
 appendix=s.new_tag('section',attrs={'class':'editorial-chapter revision-details','id':'product-specifications'})
 inset=s.new_tag('div',attrs={'class':'editorial-section-inner'})
 inset.append(BeautifulSoup('<p class="editorial-kicker">제품 상세</p><h2>구성과 운영, 더 자세히.</h2><p>필요한 항목을 펼쳐 제품 구성과 설치 조건을 확인하세요.</p>','html.parser'))
 for sec in list(root.find_all('section',recursive=False)):
  ident=sec.get('id','')
  if sec==hero or ident in ['product-benefits']+KEEP.get(slug,[]):continue
  details=s.new_tag('details',attrs={'class':'revision-disclosure'})
  h=sec.find('h2');label=h.get_text(' ',strip=True) if h else '제품 구성과 운영 안내'
  title=s.new_tag('summary');title.string=label;details.append(title)
  sec['class']=sec.get('class',[])+['revision-source']
  details.append(sec.extract());inset.append(details)
 appendix.append(inset)
 if slug in PROOF:
  filename,alt,title=PROOF[slug]
  from PIL import Image
  w,h=Image.open(ROOT/'media/derived'/filename).size
  evidence=f'<section class="editorial-chapter revision-proof"><div class="editorial-section-inner"><p class="editorial-kicker">제품 자료로 살펴보기</p><h2>{e(title)}</h2><a href="/media/derived/{filename}" target="_blank" rel="noopener" aria-label="{e(alt)} — 원본 크게 보기"><img src="/media/derived/{filename}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"><span>자료 크게 보기 ↗</span></a></div></section>'
  root.append(BeautifulSoup(evidence,'html.parser'))
 root.append(summary);root.append(appendix)
 # Links into optional details must reveal their targets; progressive enhancement in revision.js.
 nav=s.select_one('.product-local-nav nav')
 if nav:
  links=nav.find_all('a');links[1]['href']='#product-specifications';links[1].string='구성·사양'
 return str(s)
