#!/usr/bin/env python3
"""Release checks: every public route, content preservation, links and design system."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, unquote
import json,re,sys,subprocess,hashlib
from product_editorial import apply_copy, COPY, PROFILES
ROOT=Path(__file__).resolve().parents[1]
paths=[ROOT/'index.html',ROOT/'404.html']+[p for d in ['company','cases','contact','privacy','products','solutions'] for p in (ROOT/d).rglob('index.html')]
errors=[];cache={p:BeautifulSoup(p.read_text(),'html.parser') for p in paths}
def fail(p,msg):errors.append(str(p.relative_to(ROOT))+': '+msg)
for p,soup in cache.items():
    if len(soup.find_all('h1'))!=1:fail(p,'must have exactly one h1')
    if soup.find('html').get('lang')!='ko':fail(p,'missing Korean lang')
    if not soup.select_one('link[href^="/assets/sunflex-v2/solar-site.css"]') and soup.body.get('data-page-design')!='cctv-motion-20260923':fail(p,'missing shared design system')
    if re.search(r'\bMOVING\s+(DETECT|ALERT|RESPOND|RECORD)|MOVING 제품군|SUNFLEX',soup.get_text(' ',strip=True)):fail(p,'old public branding')
    ids=[x['id'] for x in soup.select('[id]')]
    if len(ids)!=len(set(ids)):fail(p,'duplicate IDs: '+str([x for x in set(ids) if ids.count(x)>1]))
    for node in soup.select('[href],[src]'):
        raw=node.get('href') or node.get('src');url=urlsplit(raw)
        if url.scheme or url.netloc:continue
        target=(ROOT/unquote(url.path).lstrip('/')) if url.path.startswith('/') else p.parent/unquote(url.path)
        if not url.path:target=p
        if target.is_dir():target=target/'index.html'
        if not target.exists():fail(p,'missing asset/link '+raw);continue
        if url.fragment and target.suffix=='.html':
            dest=cache.get(target) or BeautifulSoup(target.read_text(),'html.parser')
            if not dest.find(id=unquote(url.fragment)):fail(p,'missing fragment '+raw)
    for node in soup.select('[srcset]'):
        for candidate in node['srcset'].split(','):
            asset=candidate.strip().split()[0]
            if asset.startswith('/') and not (ROOT/asset.lstrip('/')).is_file():fail(p,'missing srcset asset '+asset)
    for im in soup.find_all('img'):
        if not im.has_attr('alt'):fail(p,'missing image alt')
        if not im.get('src'):fail(p,'missing image src')
manifest=json.loads((ROOT/'data/solar-source-manifest.json').read_text())
for name,digest in manifest['pages'].items():
    baseline=subprocess.check_output(['git','show',manifest['base']+':'+name],cwd=ROOT)
    assert hashlib.sha256(baseline).hexdigest()==digest,'Baseline mismatch: '+name
catalog=json.loads((ROOT/'data/solar-catalog.json').read_text())
assert len(catalog)==48
assert set(COPY)==set(PROFILES)=={p["slug"] for p in catalog}
for item in catalog:
    p=ROOT/f'products/{item["slug"]}/index.html';soup=cache[p]
    source=BeautifulSoup((ROOT/f'data/solar-products/{item["slug"]}.html').read_text(),'html.parser')
    original=BeautifulSoup(subprocess.check_output(['git','show',manifest['base']+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True),'html.parser').select_one('.dedicated-product-page__story')
    for tag in original.select('script,style,noscript'):tag.decompose()
    snapshot=' '.join(source.stripped_strings)
    for text in original.stripped_strings:
        if text not in snapshot:fail(p,'lost baseline text '+text[:70])
    if item['slug']=='mobile-cctv' and soup.body.get('data-page-design')=='cctv-motion-20260923':
        subprocess.run([sys.executable,str(ROOT/'scripts/test-cctv-motion-release.py')],cwd=ROOT,check=True)
        continue
    # Only explicit, source-matched editorial edits are allowed; all other facts remain.
    apply_copy(source,item["slug"])
    actual=' '.join(soup.select_one('.product-story').stripped_strings)
    for text in source.stripped_strings:
        if text not in actual:fail(p,'lost source text '+text[:70])
    for image in source.find_all('img'):
        if not soup.select_one('.product-story').find('img',src=image.get('src')):fail(p,'lost product image '+str(image.get('src')))
    if not soup.find('a',href='/contact/?product='+item['slug']):fail(p,'missing product-specific inquiry')
if len(cache[ROOT/'products/index.html'].select('[data-catalog-card]'))!=48:errors.append('catalog count mismatch')
if len(cache[ROOT/'index.html'].select('[data-map-choice]'))!=4:errors.append('Solar infographic requires 4 choices')
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(paths)} pages, 48 preserved product sources with explicit editorial substitutions, four Solar families, links, assets, IDs, headings, metadata and contact routes.')
