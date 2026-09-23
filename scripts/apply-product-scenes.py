"""Apply approved product-specific scenes to their six existing placements only."""
import json
import re
from product_scene_assets import ROOT, SCENES, apply_scene_overrides, replace_scene_figure

data = ROOT / 'data/product-infographics.json'
figures = apply_scene_overrides(json.loads(data.read_text()))
data.write_text(json.dumps(figures, ensure_ascii=False, indent=2) + '\n')
count = 0
for scene_id, scene in SCENES.items():
    slug, _ = scene_id.rsplit('-', 1)
    path = ROOT / 'products' / slug / 'index.html'
    text = path.read_text()
    def replace(match):
        global count
        markup = match[0]
        if 'context-safety-preparation.webp' not in markup and scene['asset'] not in markup:
            return markup
        count += 1
        return replace_scene_figure(markup, scene_id)
    text = re.sub(r'<figure\b[^>]*>.*?</figure>', replace, text, flags=re.S)
    path.write_text(text)
assert count == 6, count
print(f'Applied {len(SCENES)} product scenes to {count} placements.')
