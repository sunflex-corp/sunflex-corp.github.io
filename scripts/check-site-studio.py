#!/usr/bin/env python3
"""All-route presentation contract, compared with the pre-redesign published baseline."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
import subprocess,json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE='c540937af3ae6a5cba6d598be9f8472ebe748d77'
# The reviewed gas pilot replaces these generic reference scenes with the actual
# instrument and an HTML measurement/remote-reading explanation. Product photos stay.
REPLACED_REFERENCES={
 'products/compact-gas-detector/index.html':{
 '/media/external-renders/industrial-pipe-inspection.webp?v=9c5ba63ed9',
 '/media/external-renders/office-integrated-review.webp?v=30c00bbe89',
 '/media/external-renders/context-record-review.webp?v=403ebcb2e8'}}
paths=[ROOT/'index.html',ROOT/'404.html']+[p for d in ['company','cases','contact','privacy','products','solutions'] for p in (ROOT/d).rglob('index.html')]
cache={p:BeautifulSoup(p.read_text(),'html.parser') for p in paths}
errors=[];rows=[]
def norm(t):return re.sub(r'\s+',' ',t).strip()
def fail(p,t):errors.append(f'{p.relative_to(ROOT)}: {t}')
for p,soup in cache.items():
 rel=str(p.relative_to(ROOT));redirect=bool(soup.select_one('meta[http-equiv=refresh]'))
 if len(soup.select('h1'))!=1:fail(p,'h1 count')
 ids=[n['id'] for n in soup.select('[id]')]
 if len(ids)!=len(set(ids)):fail(p,'duplicate IDs')
 if soup.html.get('lang')!='ko':fail(p,'language')
 if not redirect and 'site-studio' not in soup.body.get('class',[]):fail(p,'missing studio presentation')
 for node in soup.select('[href],[src]'):
  value=node.get('href') or node.get('src');u=urlsplit(value)
  if u.scheme or u.netloc:continue
  target=ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else p.parent/unquote(u.path)
  if not u.path:target=p
  if target.is_dir():target=target/'index.html'
  if not target.exists():fail(p,'missing '+value);continue
  if u.fragment and target.suffix=='.html':
   dest=cache.get(target) or BeautifulSoup(target.read_text(),'html.parser')
   if not dest.find(id=unquote(u.fragment)):fail(p,'missing anchor '+value)
 for node in soup.select('[srcset]'):
  for item in node['srcset'].split(','):
   value=item.strip().split()[0];u=urlsplit(value)
   if value.startswith('/') and not (ROOT/unquote(u.path).lstrip('/')).exists():fail(p,'missing srcset '+value)
 for image in soup.select('img'):
  if not image.has_attr('alt'):fail(p,'image alt missing')
 old=BeautifulSoup(subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT,text=True),'html.parser')
 actual=norm(soup.get_text(' ',strip=True))
 for n in old.select('main p,main h1,main h2,main h3,main dd,main dt'):
  t=norm(n.get_text(' ',strip=True))
  if t and t not in actual:fail(p,'published text changed: '+t[:100])
 for image in old.select('main img[src]'):
  if not soup.find('img',src=image['src']) and image['src'] not in REPLACED_REFERENCES.get(rel,set()):fail(p,'published image removed: '+image['src'])
 for n in old.select('main [id]'):
  if not soup.find(id=n['id']):fail(p,'published anchor removed: '+n['id'])
 for root in soup.select('[data-studio-scene]'):
  buttons=root.select('.studio-tabs button');panels=root.select('.studio-panel')
  if len(buttons)!=len(panels) or not panels:fail(p,'scene controls mismatch')
  for b,n in zip(buttons,panels):
   if b.get('aria-controls')!=n['id']:fail(p,'scene association')
   if n.has_attr('hidden') or n.get('aria-hidden')=='true':fail(p,'no-JS scene hidden')
 for node in soup.select('link[href*="site-studio."],script[src*="site-studio."]'):
  u=urlsplit(node.get('href') or node.get('src'));asset=ROOT/u.path.lstrip('/')
  if u.query!='v='+hashlib.sha256(asset.read_bytes()).hexdigest()[:10]:fail(p,'stale studio asset version')
 rows.append({'path':rel,'redirect':redirect,'type':soup.body.get('data-studio-kind',soup.body.get('data-studio-page','redirect'))})
assert len(rows)==66
assert sum(not r['redirect'] for r in rows)==61
report={'baseline':BASE,'routes':rows,'errors':errors}
reportpath=ROOT/'docs/verification/site-studio-static.json';reportpath.parent.mkdir(parents=True,exist_ok=True);reportpath.write_text(json.dumps(report,ensure_ascii=False,indent=2))
if errors:print('\n'.join(errors));raise SystemExit(1)
print('PASS: 66 routes (61 content + 5 redirects), published text/anchors, assets, IDs, no-JS scene markup, versioned studio assets')
