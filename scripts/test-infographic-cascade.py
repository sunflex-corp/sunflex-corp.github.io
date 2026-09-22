"""Static CSS cascade regression: this does not measure browser layout.
Dev dependencies: cssselect2, tinycss2, lxml.
"""
from pathlib import Path
import json,re
import cssselect2,tinycss2,lxml.html
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/product-infographics.json').read_text())
def rules(nodes,cw):
 for r in nodes:
  if r.type=='qualified-rule':yield r
  elif r.type=='at-rule' and r.content:
   query=tinycss2.serialize(r.prelude)
   if r.lower_at_keyword not in ('media','container'):continue
   width=cw if r.lower_at_keyword=='container' else 1440
   limits=re.findall(r'(max|min)-width\s*:\s*(\d+)px',query)
   if any((kind=='max' and width>int(n)) or (kind=='min' and width<int(n)) for kind,n in limits):continue
   if 'prefers-reduced-motion' in query:continue
   yield from rules(tinycss2.parse_rule_list(r.content,skip_whitespace=True,skip_comments=True),cw)
def matcher(cw):
 m=cssselect2.Matcher()
 styles=[(ROOT/'assets/sunflex-v2'/name).read_text() for name in ['product-infographics.css','product-infographics-layout.css']]
 styles += [css for figures in DATA.values() for figure in figures for css in re.findall(r'<style[^>]*>(.*?)</style>',figure,re.S)]
 for css in styles:
  nodes=tinycss2.parse_stylesheet(css,skip_whitespace=True,skip_comments=True)
  for rule in rules(nodes,cw):
   selectors=cssselect2.compile_selector_list(tinycss2.serialize(rule.prelude))
   declarations=[(d.lower_name,tinycss2.serialize(d.value).strip(),d.important) for d in tinycss2.parse_declaration_list(rule.content,skip_whitespace=True,skip_comments=True) if d.type=='declaration']
   for s in selectors:
    if s.pseudo_element is None:m.add_selector(s,declarations)
 return m
def computed(m,node):
 result={};priority={}
 for spec,order,pseudo,ds in m.match(node):
  for prop,value,important in ds:
   key=(important,spec,order)
   if key>=priority.get(prop,(-1,(),-1)):result[prop]=value;priority[prop]=key
 return result
count=0
for width in [360,540,720]:
 m=matcher(width);large=0;renders=0;panels=0;pins=0
 for slug,figures in DATA.items():
  section='blind-corner' if slug=='pedestrian-collision-prevention' else 'product-benefits'
  root=cssselect2.ElementWrapper.from_html_root(lxml.html.fromstring(f'<div class="product-editorial"><section id="{section}">'+''.join(figures)+'</section></div>'))
  for n in root.iter_subtree():
   c=n.classes;style=computed(m,n)
   if n.local_name=='svg' and n.parent is not None and 'subject-scene' in n.parent.classes:
    assert style['width']=='100%' and style['height']=='auto' and style['min-height']=='0',(slug,width,style)
    large+=1
   if n.local_name=='svg' and n.parent is not None and n.parent.classes & {'bc-chest-focus','ctx-crane','ctx-cutaway','ctx-location-plan','ctx-drone-plan'}:
    assert style['width']=='100%' and style['height']=='auto',(slug,width,style)
   if 'render-stage' in c:
    assert style['aspect-ratio']==('4/3' if c&{'render-stage--focused','render-stage--portrait'} else '16/9'),(slug,style)
    renders+=1
   if 'dual-panels' in c and width<=420:assert style['grid-template-columns']=='1fr',(slug,style)
   if 'signal-route' in c and width<=480:assert style['grid-template-columns']=='minmax(0,1fr)',(slug,style)
   if 'diagram' in c:assert style['min-height']=='0',(slug,width,style['min-height'])
   if 'technical-pin' in c:
    assert style['width']=='26px' and '13px' in style['font'],(slug,width,style)
    pins+=1
   if 'sunflex-infographic' in c:panels+=1
 assert large==15 and renders==29 and panels==144 and pins==15,(width,large,renders,panels)
 count+=panels
print(f'PASS: {count} scene/width cascade checks; 15 full-size SVG scenes, 29 render frames, readable compact card/route rules')
