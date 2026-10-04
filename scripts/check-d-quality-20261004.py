"""Focused verification: assets, exact allowed markup changes, rebuild persistence."""
from pathlib import Path
import json,re,sys,hashlib,subprocess
from PIL import Image
from bs4 import BeautifulSoup
from product_quality_d import apply_quality_d
R=Path(__file__).resolve().parents[1];O=R/'output/d-quality-20261004'
records=json.loads((O/'records.json').read_text());checks=[]
for key,record in records.items():
 slug=key.rsplit('-d-',1)[0];path=R/f'products/{slug}/index.html'
 old=(O/f'{slug}-before.txt').read_text();new=path.read_text()
 a=BeautifulSoup(old,'html.parser');b=BeautifulSoup(new,'html.parser')
 oldpic=a.find(id=record['section']).find('picture');newpic=b.find(id=record['section']).find('picture')
 oldtags=oldpic.find_all(['source','img']);newtags=newpic.find_all(['source','img']);assert len(oldtags)==len(newtags)
 for x,y in zip(oldtags,newtags):
  assert {k:v for k,v in x.attrs.items() if k not in ('src','srcset','width','height')}=={k:v for k,v in y.attrs.items() if k not in ('src','srcset','width','height')}
  x.attrs=y.attrs.copy()
 assert str(a)==str(b),f'Out of scope markup: {slug}'
 # Byte-exact matching after masking just the permitted attributes in target region.
 def normalized(text):
  match=re.search(r'<section\b[^>]*id="'+record['section']+r'"[^>]*>.*?</section>',text,re.S)
  region=re.sub(r'<(?:source|img)\b[^>]*>',lambda m:re.sub(r'(?<![\w:-])(?:src|srcset|width|height)="[^"]*"','',m[0]),match[0])
  return text[:match.start()]+region+text[match.end():]
 assert normalized(old)==normalized(new)
 assert apply_quality_d(new,slug)==new
 # Test stale source HTML and current markup through same build hook without writing outside scope.
 # The build hook receives complete generated markup (including the hero), not body fragments.
 assert apply_quality_d(old,slug)==new
 for v in record['variants']:
  p=R/v['asset'].lstrip('/');im=Image.open(p);im.load()
  assert im.size==(v['width'],v['height'])
  assert hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256']
  assert p.stat().st_size==v['bytes']
 assert hashlib.sha256((R/record['reference'].lstrip('/')).read_bytes()).hexdigest()==record['original_sha256']
 for tag in newpic.find_all(['img','source']):
  for part in tag.get('srcset','').split(','):
   url,w=part.strip().split();assert (R/url.lstrip('/')).exists();assert Image.open(R/url.lstrip('/')).width==int(w[:-1])
 checks.append({'slug':slug,'only_allowed_attributes':True,'original_unchanged':True,'asset_variants':len(record['variants']),'rebuild_idempotent':True})
# Tracked diff includes only nine designated pages, metadata, build integration.
allowed={f'products/{c["slug"]}/index.html' for c in checks}|{'data/product-scene-overrides.json','scripts/generate-solar-site.py'}
changed=set(subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines());assert changed<=allowed,changed-allowed
for slug in ['iot-small-tower-crane','emergency-signal-location']:
 before=BeautifulSoup((O/f'{slug}-before.txt').read_text(),'html.parser').find(id='detail-4')
 after=BeautifulSoup((R/f'products/{slug}/index.html').read_text(),'html.parser').find(id='detail-4')
 assert str(before)==str(after)
opening=records['opening-open-close-sensor-d-6-20261004'];assert (R/opening['asset'].lstrip('/')).stat().st_size <= (R/opening['reference'].lstrip('/')).stat().st_size*1.5
# Preserve metadata outside this task exactly in value.
previous=json.loads(subprocess.check_output(['git','show','HEAD:data/product-scene-overrides.json'],cwd=R,text=True));current=json.loads((R/'data/product-scene-overrides.json').read_text())
assert all(current[k]==v for k,v in previous.items());assert set(current)-set(previous)==set(records)
(O/'verification.json').write_text(json.dumps({'status':'PASS','checks':checks,'skipped_detail_4_unchanged':True,'opening_byte_limit':True,'existing_metadata_unchanged':True},indent=2))
print(f'PASS: {len(checks)} placements, {sum(c["asset_variants"] for c in checks)} assets; exact markup scope, original hashes, skipped sections, rebuild hook and 1.5x cap')
