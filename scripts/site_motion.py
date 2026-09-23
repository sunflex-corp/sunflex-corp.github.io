"""Attach the shared GSAP runtime without rewriting page content."""
from pathlib import Path
import hashlib,re
ROOT=Path(__file__).resolve().parents[1]
BASE='/assets/sunflex-v2/'
VENDOR=BASE+'cctv-motion/vendor/'

def asset(path):
 return path+'?v='+hashlib.sha256((ROOT/path.lstrip('/')).read_bytes()).hexdigest()[:10]

def enhance(text):
 if 'sunflex-v2' not in text or 'http-equiv="refresh"' in text or 'data-page-design="cctv-motion-20260923"' in text:return text
 text=re.sub(r'<html(?![^>]*data-motion-engine)', '<html data-motion-engine="gsap"',text,count=1)
 # Idempotently refresh only owned tags and changed legacy owner cache keys.
 text=re.sub(r'<(?:script|link)\b[^>]*data-site-motion="[^"]*"[^>]*>(?:</script>)?','',text)
 for name in ['product-motion.js','product-flow.js','home-simple.js','home-families.js']:
  url=BASE+name
  text=re.sub(re.escape(url)+r'(?:\?v=[a-zA-Z0-9]+)?',asset(url),text)
 vendor='<link data-site-motion="lenis" rel="stylesheet" href="'+asset(VENDOR+'lenis.css')+'">'
 vendor+=''.join('<script data-site-motion="vendor" defer src="'+asset(VENDOR+name)+'"></script>' for name in ['gsap.min.js','ScrollTrigger.min.js','lenis.min.js'])
 # Dependencies execute before legacy files decide whether to yield ownership.
 text=text.replace('</title>','</title>'+vendor,1)
 text=text.replace('</head>','<link data-site-motion="style" rel="stylesheet" href="'+asset(BASE+'site-motion.css')+'"></head>',1)
 text=text.replace('</body>','<script data-site-motion="runtime" defer src="'+asset(BASE+'site-motion.js')+'"></script></body>',1)
 return text

if __name__=='__main__':
 pages=[]
 for path in sorted(ROOT.rglob('*.html')):
  if any(p in {'node_modules','.git','data','brand','docs'} for p in path.relative_to(ROOT).parts):continue
  text=path.read_text();updated=enhance(text)
  if updated!=text:path.write_text(updated);pages.append(str(path.relative_to(ROOT)))
 print('Updated',len(pages),'pages')
