"""Import reviewed local compositions into versioned site assets and durable fragments.
Usage: python3 scripts/import-product-infographics.py /absolute/path/to/review-draft
"""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
DRAFT=Path(sys.argv[1]).resolve()
page=BeautifulSoup((DRAFT/'index.html').read_text(),'html.parser')
assets=ROOT/'assets/sunflex-infographics';assets.mkdir(exist_ok=True)
manifest={};used=set();media=[]
for product in page.select('.product[data-slug]'):
 slug=product['data-slug'];items=[]
 for i,stage in enumerate(product.select('.stage'),1):
  shell=stage.select_one('.visual-shell')
  assert shell is not None,(slug,i)
  for redundant in shell.select('.terms,.diagram-top,.technical-eyebrow,.technical-lead'):
   redundant.decompose()
  wrapper=page.new_tag('div',attrs={'class':'sunflex-infographic','data-infographic-scene':f'{slug}-{i}','role':'group','aria-label':stage.select_one('.stage-title h3').get_text(),'style':product['style']})
  wrapper.append(shell.extract())
  for node in wrapper.select('img[src]'):
   src=DRAFT/node['src'];data=src.read_bytes();target=f'{src.stem}.{hashlib.sha256(data).hexdigest()[:10]}{src.suffix}'
   (assets/target).write_bytes(data);node['src']='/assets/sunflex-infographics/'+target
   node['width']='1600';node['height']='900';node['loading']='lazy';node['decoding']='async'
   media.append(node['src'])
  for node in wrapper.select('[class]'):used.update(node['class'])
  figure=page.new_tag('figure',attrs={'class':'benefit-visual infographic-visual','data-infographic-version':'20260922'})
  figure.append(wrapper)
  caption=page.new_tag('figcaption');caption.string='기능을 설명한 구성 예시 · 실제 제품·설치 환경에 따라 달라질 수 있습니다';figure.append(caption)
  items.append(str(figure).replace('Asta Sans','Asta'))
 assert len(items)==3,slug
 manifest[slug]=items
assert len(manifest)==48
(ROOT/'data/product-infographics.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/product-infographic-classes.json').write_text(json.dumps(sorted(used),ensure_ascii=False)+'\n')
print(f'Imported {len(manifest)} products / {sum(map(len,manifest.values()))} scenes / {len(set(media))} render assets')
