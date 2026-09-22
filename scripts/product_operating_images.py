"""Pair each secondary operating step with an existing, context-matched image.

No generated geometry or new product representations. The source copy, step IDs,
navigation and shared scroll controller remain intact.
"""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGES = json.loads((ROOT / 'data/product-editorial-images.json').read_text())
# Section keys refer to the already reviewed editorial image catalogue.
# Render keys refer to downloaded-model Blender compositions already in production.
STEPS = {
 'chatgpt-cctv': ['scene-to-record', 'detail-2', 'detail-4'],
 'vehicle-entry-alert': ['detail-2', 'entry-alert-flow', 'detail-4'],
 'co2-temp-humidity': ['detail-2', 'air-check-line', 'detail-4'],
 'smart-environment-board': ['environment-link', 'detail-2', '@industrial-utility-management'],
 'compact-gas-detector': ['gas-measurement-flow', '@industrial-pipe-inspection', '@context-record-review'],
 'gas-alarm': ['entrance-decision-line', 'detail-2', 'detail-4'],
 'tilt-acceleration-sensor': ['detail-2', 'tilt-decision-record', '@office-integrated-review', '@context-record-review'],
 'fire-detection': ['detail-2', 'first-signal-line', 'detail-4'],
 'wireless-emergency-broadcast': ['detail-2', '@context-broadcast-planning', 'broadcast-reach-line', 'detail-4'],
 'tbm-solution': ['@context-prework-record', 'detail-4', 'detail-2'],
 'ai-equipment-collision': ['detail-4', 'detail-2', 'warning-state'],
 'opening-open-close-sensor': ['detail-2', '@context-field-broadcast', 'detail-4'],
 'equipment-approach-alarm': ['detail-2', 'detail-4', 'work-radius-line'],
 'tower-crane-hook-collision': ['@construction-tower-crane-operation', 'detail-2', 'hook-warning-flow'],
 'hazard-area-broadcast': ['walking-boundary', 'detail-2', 'detail-4'],
 'alcohol-detection': ['shift-start-gate', 'detail-2', 'detail-4'],
 'wireless-network': ['detail-2', 'network-signal-path', 'detail-4'],
 'worker-attendance-card': ['attendance-card-flow', 'detail-2', 'detail-4'],
 'ai-quick-risk-assessment': ['ai-quick-risk-assessment-flow', 'detail-2', 'detail-4'],
 'ai-risk-assessment-review': ['ai-risk-assessment-review-flow', 'detail-2', 'detail-4'],
 'ai-safety-index': ['detail-2', '@office-integrated-review', 'morning-index-line'],
 'ai-subcontractor-safety': ['detail-2', 'detail-4', 'ai-subcontractor-safety-flow'],
 'ai-drone-inspection': ['detail-4', 'detail-2', 'flight-route'],
 'ai-similar-accident-alert': ['detail-4', '@office-document-comparison', 'detail-2'],
 'safebridge': ['safebridge-training-timeline', '@office-training-briefing', 'detail-4', '@context-record-review'],
 'concrete-curing': ['detail-2', 'curing-rail', 'detail-4', '@industrial-concrete-record', '@context-record-review'],
}

def refine_operating_images(soup, root, slug):
 if slug not in STEPS:
  return
 panels = root.select('.editorial-flow-step[data-flow-panel]')
 assert len(panels) == len(STEPS[slug]), (slug, len(panels))
 for panel, key in zip(panels, STEPS[slug]):
  if 'operating-image-panel' in panel.get('class', []):
   continue
  # Keep the existing illustrated warning stage and its semantic facts.
  existing = panel.select_one('.external-detail-render')
  if existing:
   visual = existing.extract()
   fit = 'contain'
  else:
   visual = soup.new_tag('figure')
   if key.startswith('@'):
    src = f'/media/external-renders/{key[1:]}.webp'
    asset = {'src': src, 'fit': 'contain', 'alt': '설치·운영 상황을 설명하는 참고 장면', 'width': 1800, 'height': 1200}
   else:
    asset = IMAGES[slug][key]
   fit = asset['fit']
   # Prefer the larger existing export for large desktop cards.
   candidates = asset.get('srcset', '').split(', ')
   src = candidates[-1].split(' ')[0] if candidates[0] else asset['src']
   width, height = Image.open(ROOT / src.lstrip('/')).size
   image = soup.new_tag('img', attrs={'src': src, 'alt': asset['alt'], 'width': str(width), 'height': str(height), 'loading': 'lazy', 'decoding': 'async'})
   if asset.get('srcset'):
    image['srcset'] = asset['srcset']
    image['sizes'] = '(max-width:760px) calc(100vw - 40px), (max-width:1200px) 50vw, 600px'
   visual.append(image)
  visual['class'] = ['operating-step-image']
  visual['data-fit'] = fit
  copy = soup.new_tag('div', attrs={'class': 'operating-step-copy'})
  for child in list(panel.contents):
   copy.append(child.extract())
  panel.append(visual)
  panel.append(copy)
  panel['class'] = panel.get('class', []) + ['operating-image-panel']
