"""Static release contract. Browser interactions are recorded separately."""
from pathlib import Path
import hashlib,re,subprocess,sys
from bs4 import BeautifulSoup
from site_motion import enhance
ROOT=Path(__file__).resolve().parents[1]
BASE=sys.argv[1] if len(sys.argv)>1 else '894eece4d4800a3790513adbc91fd4ff21b4523c'
owned=['gsap.min.js','ScrollTrigger.min.js','lenis.min.js','site-motion.js']
changed=['product-motion.js','product-flow.js','home-simple.js','home-families.js']
def content(text):
 text=re.sub(r'<(?:script|link)\b[^>]*data-site-motion="[^"]*"[^>]*>(?:</script>)?','',text)
 text=text.replace(' data-motion-engine="gsap"','')
 for name in changed:text=re.sub(re.escape('/assets/sunflex-v2/'+name)+r'(?:\?v=[a-zA-Z0-9]+)?','/assets/sunflex-v2/'+name,text)
 return text
pages=[]
for p in ROOT.rglob('*.html'):
 if any(part in {'node_modules','.git','data','brand','docs'} for part in p.relative_to(ROOT).parts):continue
 text=p.read_text()
 if 'data-motion-engine="gsap"' not in text:continue
 rel=str(p.relative_to(ROOT));pages.append(rel)
 old=subprocess.check_output(['git','show',f'{BASE}:{rel}'],cwd=ROOT,text=True)
 assert content(text)==content(old),(rel,'unrelated page content changed')
 assert enhance(text)==text,(rel,'non-idempotent enhancement')
 soup=BeautifulSoup(text,'html.parser')
 scripts=[n.get('src','').split('?')[0].rsplit('/',1)[-1] for n in soup.select('script[src]')]
 assert all(scripts.count(name)==1 for name in owned),(rel,'duplicated dependency')
 assert scripts.index('gsap.min.js')<scripts.index('ScrollTrigger.min.js')<scripts.index('site-motion.js')
 for name in changed:
  if name in scripts:assert scripts.index('ScrollTrigger.min.js')<scripts.index(name)<scripts.index('site-motion.js'),(rel,name)
 for n in soup.select('[data-site-motion]'):
  url=n.get('src',n.get('href'));path,key=url.split('?v=')
  assert hashlib.sha256((ROOT/path.lstrip('/')).read_bytes()).hexdigest()[:10]==key,(rel,path)
 assert not soup.select('[data-motion-toggle]'),rel
assert len(pages)==60,len(pages)
p=ROOT/'products/mobile-cctv/index.html'
assert enhance(p.read_text())==p.read_text()
print('PASS: 60 shared-motion pages preserve exact source content; dependency order, cache keys, idempotence, standalone CCTV and no manual motion control')
