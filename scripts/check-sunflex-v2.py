#!/usr/bin/env python3
"""Release checks for corporate routes, links, images and protected baseline files."""
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index.html','company/index.html','solutions/index.html','cases/index.html','contact/index.html','privacy/index.html','404.html']
BASE = sys.argv[1] if len(sys.argv)>1 else '6a7143a'
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.links=[];self.assets=[];self.h1=0;self.high=0;self.images=[];self.inputs=[];self.labels=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        if tag=='h1':self.h1+=1
        if tag=='a':self.links.append(d.get('href',''))
        if tag in ['img','script','source'] and d.get('src'):self.assets.append(d['src'])
        if tag=='link' and d.get('rel') in ['stylesheet','icon','preload']:self.assets.append(d['href'])
        if 'srcset' in d:self.assets.extend(x.strip().split()[0] for x in d['srcset'].split(','))
        if tag=='img':self.images.append(d)
        if d.get('fetchpriority')=='high':self.high+=1
        if tag in ['input','textarea']:self.inputs.append(d.get('id'))
        if tag=='label':self.labels.append(d.get('for'))

docs={p:Document((ROOT/p).read_text()) for p in PAGES}
def local_path(url, origin):
    u=urlsplit(url)
    if u.scheme or u.netloc:return None,u.fragment
    p=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else (ROOT/origin).parent/u.path
    if not u.path:p=ROOT/origin
    if p.is_dir():p=p/'index.html'
    return p,unquote(u.fragment)

count=0
for name,d in docs.items():
    assert d.h1==1,(name,'h1')
    assert len(d.ids)==len(set(d.ids)),(name,'duplicate IDs')
    assert d.high<=1,(name,'multiple LCP priorities')
    for img in d.images:
        assert 'alt' in img and 'width' in img and 'height' in img,(name,'image dimensions/alt')
    assert set(d.inputs)<=set(d.labels),(name,'unlabelled input')
    for url in d.links+d.assets:
        assert url,(name,'empty URL')
        target,fragment=local_path(url,name)
        if target is None:continue
        assert target.is_file(),(name,url,'missing file')
        if fragment:
            dest=Document(target.read_text())
            assert fragment in dest.ids,(name,url,'missing anchor')
        count+=1
    content=(ROOT/name).read_text()
    for forbidden in ['네 가지 감각','오감','사람이 놓친 순간까지','오직 안전','기술의 기준','바로 닿도록','/_astro/']:
        assert forbidden not in content,(name,forbidden)
    assert '/assets/sunflex-v2/site.css?v=' in content
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',content):
        import json
        assert json.loads(block)['name']=='(주)썬플렉스'

# Compare repository blob hashes, not timestamps: all old assets and product pages stay intact.
tree=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=ROOT,text=True)
protected=0
for line in tree.splitlines():
    meta,path=line.split('\t',1)
    if path in PAGES:continue
    data=(ROOT/path).read_bytes()
    digest=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
    assert digest==meta.split()[2],('protected file changed',path)
    protected+=1

css=(ROOT/'assets/sunflex-v2/site.css').read_text()
for path in re.findall(r"url\(['\"]?([^'\")]+)",css):assert (ROOT/path.lstrip('/')).is_file(),path

# Regeneration must be deterministic.
before={p:(ROOT/p).read_bytes() for p in PAGES}
subprocess.run([sys.executable,str(ROOT/'scripts/generate-sunflex-v2.py')],check=True)
assert all((ROOT/p).read_bytes()==b for p,b in before.items()),'non-deterministic generation'
print(f'PASS: {len(PAGES)} pages; {count} local links/assets; {protected} protected files unchanged; deterministic generation.')
