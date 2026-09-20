#!/usr/bin/env python3
"""One-time content migration from the pre-redesign Git baseline; do not run for normal builds."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE='b71218a'
def source(p):return subprocess.check_output(['git','-C',str(ROOT),'show',f'{BASE}:{p}']).decode()
menu=json.loads(source('product-menu-data.js').removeprefix('export default ').strip().rstrip(';'))
by={p['slug']:(g['key'],cat['label'],p['name']) for g in menu for cat in g['categories'] for p in cat['products']}
listing=BeautifulSoup(source('products/index.html'),'html.parser')
cards={t['data-slug']:t for t in listing.select('[data-product-card][data-slug]')}
records=[];manifest={}
# Preserve readable product content, stable fragment IDs, semantic figures and tables;
# retire old layout classes and script-driven image loading.
def clean(section):
 for node in list(section.select('script,style,noscript')):node.decompose()
 for node in list(section.find_all()):
  if node.name is None:continue
  if node.name in ['source','img']:
   for key in ['src','srcset','sizes']:
    if node.get('data-'+key):node[key]=node['data-'+key]
  old=' '.join(node.get('class',[]))
  cls=[]
  if node.name in ['div','ol','ul'] and re.search(r'(?:__|-)(?:grid|steps|cards|models|comparison|columns|list|items|stages|points|flow)$',old):cls.append('content-grid')
  if node.name in ['article','li'] and node.find(['h3','h4']):cls.append('content-tile')
  if node.name=='div' and ('__copy' in old):cls.append('content-copy')
  if node.name=='svg':cls.append('content-svg')
  for key in list(node.attrs):
   if key.startswith('data-') or key in ['style','class','aria-busy','fetchpriority']:del node[key]
  if cls:node['class']=cls
  if node.name=='img':
   node['loading']='lazy';node['decoding']='async'
   if not node.get('width'):node['width']='1280'
   if not node.get('height'):node['height']='800'
   if not node.has_attr('alt'):node['alt']=''
  if node.name=='mark':node.name='strong'
  if node.name=='figure' and node.find('figure',recursive=False):node.name='div'
  if node.name=='a' and node.get('href','').startswith('/contact'):node['href']='/contact/?product='+slug
 # The old structure sometimes nests layout sections; new top-level wrappers own spacing.
 for node in section.find_all('section'):node.name='div'
 for key in list(section.attrs):
  if key not in ['id','aria-labelledby','aria-label']:del section[key]
 section['class']='detail-block'
 return str(section)
for slug,(category,subgroup,name) in by.items():
 path=f'products/{slug}/index.html';raw=source(path);s=BeautifulSoup(raw,'html.parser');a=s.select_one('article.dedicated-product-page');story=a.select_one('.dedicated-product-page__story')
 card=cards[slug]
 meta={k.removeprefix('data-'):v for k,v in card.attrs.items() if k.startswith('data-')}
 imgs=[]
 for img in story.find_all('img'):
  src=img.get('src') or img.get('data-src');alt=img.get('alt','')
  if src and src not in [x['src'] for x in imgs]:imgs.append({'src':src,'alt':alt,'width':img.get('width','1280'),'height':img.get('height','800')})
 preferred=next((i for i in imgs if any(x in i['src'] for x in ['reference-white','restored-white','-device-'])),imgs[0])
 imgs=[preferred]+[i for i in imgs if i!=preferred]
 # Keep original sections including complete prose, model details, diagrams and captions.
 top=[t for t in story.find_all('section') if not any(parent.name=='section' and parent!=story for parent in t.parents if parent!=t)]
 if not top:top=[story]
 blocks=[]
 for i,section in enumerate(top):
  h=section.find(['h1','h2']);title=h.get_text(' ',strip=True) if h else f'제품 안내 {i+1}'
  if h and h.name=='h1':h.name='h2'
  sectionid=section.get('id') or f'detail-{i+1}';section['id']=sectionid
  blocks.append({'id':sectionid,'title':title if i else '제품 개요','html':clean(section)})
 highlights=a.select_one('.dedicated-product-page__highlights')
 if highlights:blocks.append({'id':highlights.get('id','highlights'),'title':'주요 특징','html':clean(highlights)})
 related=list(dict.fromkeys(x['href'].rstrip('/').split('/')[-1] for x in a.select('.product-related a[href]') if x['href'].startswith('/products/')))
 content='\n'.join(x['html'] for x in blocks)
 (ROOT/f'data/solar-products/{slug}.html').write_text(content)
 records.append({'slug':slug,'name':name,'category':category,'subgroup':subgroup,'outcome':meta.get('outcome',''),'problem':meta.get('problem','').split(),'process':meta.get('process','').split(),'installation':meta.get('installation','').split(),'connectivity':meta.get('connectivity','').split(),'images':imgs[:8],'sections':[{'id':x['id'],'title':x['title']} for x in blocks],'related':related})
 manifest[path]=hashlib.sha256(raw.encode()).hexdigest()
(ROOT/'data/solar-catalog.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(ROOT/'data/solar-source-manifest.json').write_text(json.dumps({'base':BASE,'pages':manifest},indent=2))
print(len(records),'products extracted; sections',sum(len(x['sections']) for x in records))
