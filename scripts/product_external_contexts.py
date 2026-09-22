"""Readable detail text alongside external Blender usage-context imagery."""
import json
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def refine_external_contexts(s,root,slug):
 mapping=json.loads((ROOT/'data/external-render-assets.json').read_text())
 m=mapping.get(f'{slug}-1')
 if not m:return
 image=ROOT/'media/external-renders'/Path(m['render']).with_suffix('.webp').name
 if not image.exists():return
 # Actual product-photo galleries are preserved. Only drawn HTML illustrations are replaced.
 candidates=[d for d in root.select('.editorial-diagram,.cctv-process-detail') if not d.find('img') and not any(not a.find('img') for a in d.find_parents(class_='editorial-diagram'))]
 for d in candidates:
  groups=[]
  for child in d.find_all(recursive=False):
   if child.get('aria-hidden')=='true':continue
   for deco in child.select('svg,[aria-hidden="true"]'):deco.decompose()
   parts=list(dict.fromkeys(x.strip() for x in child.stripped_strings if x.strip() not in {'→','↔','↓','◉','▣'}))
   text=' · '.join(parts)
   if text and text not in groups:groups.append(text)
  readable_groups={
   'safety-box':[
    '현장 선택 · 현장 목록에서 확인할 현장을 선택합니다.',
    '현장 핵심정보 · 현장명, 발주처, 공사규모, 공정률을 운영 범위에 맞춰 구성합니다.',
    '출역·장비 · 근로자 출역과 건설장비 현황을 현장별로 확인합니다.',
    '안전 통계 · 고위험작업과 안전점검 등 필요한 통계를 선택해 구성합니다.',
    'CCTV 열람 · 선택한 현장의 CCTV 목록에서 필요한 화면을 엽니다.',
    '표시 항목과 연동 범위는 계약 전 현장 운영 체계에 따라 다를 수 있습니다.'
   ],
   'smart-beacon':[
    '출입 지점에서 작업 구역으로 이동한 인원의 위치 신호를 확인합니다.',
    '구역 A(수직구)의 현재 인원과 구역 B(지하 통로)의 이동 중인 인원을 구분해 봅니다.',
    '접근 경고 구간의 경계를 지나면 경고하고, 관제 화면에서 구역별 인원을 확인합니다.',
    '표시는 설명을 위한 예시입니다. 실제 구역 경계와 비콘 위치는 현장 동선에 맞춰 정합니다.'
   ],
   'lte-anemometer':[
    '상부 측정 · 최상단 풍속계가 실제 바람을 측정합니다. 작업 구간에서 느끼는 바람과 함께 살펴봅니다.',
    'LTE 전송 · 운전석에서 상부 풍속을 확인하고, 운전원이 작업 전후로 신호를 점검합니다.',
    '현장사무실 검토 · 안전관리자가 측정값을 현장 기준과 비교합니다.',
    '작업 판단 · 작업을 이어 갈지, 대기할지는 현장 책임자가 결정합니다.'
   ],
   'led-logo-light':[
    '01 · 경계 확인 — 사람과 장비의 길이 가까워지는 지점을 확인합니다.',
    '02 · 안내 투사 — 바닥·벽면에 위험 경계와 통행 방향을 빛으로 표시합니다.',
    '03 · 통행 안내 — 사람이 발밑의 안내를 읽고 다음 이동 방향을 판단합니다.'
   ],
   'worker-access-gate':[
    '01 · 인증 — 단말 앞에서 얼굴인식 또는 QR로 출입을 확인합니다.',
    '02 · 통과 — 인증이 끝나면 스피드게이트를 통과합니다.',
    '03 · 출역 현황 — 출입 내역을 바탕으로 오늘 들어온 인원과 현재 현장 인원을 한 화면에서 확인합니다.'
   ]
  }
  groups=readable_groups.get(slug,groups)
  d.clear();d['class']=['external-detail-context'];d.attrs.pop('role',None)
  figure=s.new_tag('figure',attrs={'class':'external-detail-render'})
  im=s.new_tag('img',src='/media/external-renders/'+image.name,alt=m['alt'],width='1800',height='1200',loading='lazy',decoding='async')
  figure.append(im);cap=s.new_tag('figcaption');cap.string='설치·운영 상황을 설명하는 참고 장면';figure.append(cap);d.append(figure)
  facts=s.new_tag('div',attrs={'class':'external-detail-facts'})
  for text in groups:
   p=s.new_tag('p');p.string=text;facts.append(p)
  d.append(facts)
 if slug=='digital-radio':
  panels=root.select('#product-benefits .benefit-copy')
  if panels:
   h=panels[0].find(['h2','h3'])
   if h:h.string='작업 지시는, 해당 작업조에.'
   ps=panels[0].find_all('p')
   for p in ps:
    if len(p.get_text())>40:
     p.string='연락할 작업조를 선택해 지시를 전달합니다. 개인 연락은 개별 호출, 현장 공지는 전체 공지로 구분합니다.';break

 if slug=='chatgpt-cctv':
  text=[('보고할 장면을, 영상에서 고르고.','CCTV 영상에서 보고서에 남길 장면을 선택합니다.'),('선택한 장면이, AI 보고서 초안으로.','선택한 장면을 바탕으로 AI가 보고서 초안을 작성합니다.'),('초안은 AI가. 검토는 관리자가.','관리자가 초안을 검토하고, 추가로 확인할 내용을 판단합니다.')]
  for panel,(title,body) in zip(root.select('#product-benefits .benefit-copy'),text):
   h=panel.find(['h2','h3'])
   if h:h.string=title
   description=panel.select_one('.benefit-description')
   if description:description.string=body
