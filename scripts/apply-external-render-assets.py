"""Apply validated external-model Blender renders while keeping product copy as HTML."""
from pathlib import Path
import json,hashlib,html
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parent/'drafts/sunflex-external-assets-v5'
MAPPING=ROOT/'data/external-render-assets.json'
mapping=json.loads(MAPPING.read_text())
requirements={s['scene_id']:s for s in json.loads((SOURCE/'scene-requirements.json').read_text())['scenes']}
figures=json.loads((ROOT/'data/product-infographics.json').read_text())
out=ROOT/'media/external-renders';out.mkdir(parents=True,exist_ok=True)
converted={}
for scene,m in mapping.items():
 req=requirements[scene];p=SOURCE/'renders'/m['render'];assert p.is_file(),p
 im=Image.open(p).convert('RGBA');assert im.size==(1800,1200)
 dest=out/Path(m['render']).with_suffix('.webp').name
 if dest.name not in converted:
  if not dest.exists() or dest.stat().st_mtime<p.stat().st_mtime:im.save(dest,'WEBP',quality=90,method=6)
  converted[dest.name]=True
 version=hashlib.sha256(dest.read_bytes()).hexdigest()[:10]
 # Supporting copy lives beside the render; omit the repeated bottom labels.
 caption=m.get('caption','설치·운영 상황을 설명하는 참고 장면입니다.')
 figure=f'''<figure class="benefit-visual infographic-visual external-render" data-infographic-version="20260923-external" data-visual-kind="render"><div class="sunflex-infographic" data-infographic-scene="{scene}" role="group" aria-label="{html.escape(req['functional_message'],quote=True)}"><div class="visual-shell"><div class="external-render-stage"><img src="/media/external-renders/{dest.name}?v={version}" width="1800" height="1200" loading="lazy" decoding="async" alt="{html.escape(m['alt'],quote=True)}"></div></div></div><figcaption>{html.escape(caption)}</figcaption></figure>'''
 figures[req['slug']][req['step']-1]=figure
(ROOT/'data/product-infographics.json').write_text(json.dumps(figures,ensure_ascii=False,indent=2)+'\n')
print(f'Applied {len(mapping)} external Blender figures from {len(converted)} context renders')
