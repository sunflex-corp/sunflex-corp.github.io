"""Remove duplicated network framing and distinguish wearer/manager outcomes."""
import json
from pathlib import Path
from bs4 import BeautifulSoup
p=Path(__file__).resolve().parents[1]/'data/product-infographics.json'
d=json.loads(p.read_text())
s=BeautifulSoup(d['wireless-network'][1],'html.parser')
for n in s.select('.hub-node,.branch-line,.diagram-note'):n.decompose()
d['wireless-network'][1]=str(s)
for step in [1,2]:
 s=BeautifulSoup(d['healthcare-heart-band'][step],'html.parser')
 if step==1:
  a=s.select_one('.threshold-source svg path');a['d']='M3 22h8l4-12 7 24 5-15 4 3h7'
  s.select_one('.threshold-source small').string='착용 중 측정'
  s.select_one('.threshold-result svg')['viewBox']='0 0 80 90'
  s.select_one('.threshold-result svg').clear()
  s.select_one('.threshold-result svg').append(BeautifulSoup('<path d="M28 21V5h24v16M28 69v16h24V69M23 21h34v48H23zM29 46h6l4-10 6 20 5-10M13 29q-11 16 0 32M67 29q11 16 0 32"/>','html.parser'))
  s.select_one('.threshold-result strong').string='손목 진동'
  s.select_one('.threshold-result small').string='착용자가 바로 인지'
  for n in s.select('.diagram-note'):n.decompose()
 else:
  s.select_one('.alert-icon svg path')['d']='M10 3h22v36H10zM17 7h8M19 34h4M15 20l4 4 8-10'
  s.select_one('.alert-card>small').string='담당자에게 전달'
  s.select_one('.alert-card>strong').string='착용자 상태 확인'
 css='''.product-editorial .sunflex-infographic[data-infographic-scene="healthcare-heart-band-2"] .threshold-result svg{width:64px!important;height:72px!important;stroke-width:2!important}.product-editorial .sunflex-infographic[data-infographic-scene="healthcare-heart-band-3"] .alert-icon svg{width:56px!important;height:64px!important}.product-editorial .sunflex-infographic[data-infographic-scene^="healthcare-heart-band-"] .threshold-logic{margin-block:24px 0}.product-editorial .sunflex-infographic[data-infographic-scene^="healthcare-heart-band-"] .alert-card{margin:24px 0 0}'''
 if not s.select_one('[data-signal-style]'):
  st=s.new_tag('style',attrs={'data-signal-style':''});st.string=css;s.select_one('.sunflex-infographic').append(st)
 d['healthcare-heart-band'][step]=str(s)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Refined network connection and heart-band outcomes')
