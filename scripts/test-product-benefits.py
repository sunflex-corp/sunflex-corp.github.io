"""Generated product stories: coverage, reachable details, responsive assets and source links."""
import json
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/product-benefits.json').read_text())
profiles=json.loads((root/'data/product-editorial-map.json').read_text())
assert set(data)==set(profiles)-{'pedestrian-collision-prevention'}
for slug,story in data.items():
    assert (root/story['source']).is_file()
    page=BeautifulSoup((root/'products'/slug/'index.html').read_text(),'html.parser')
    section=page.find(id='product-benefits')
    assert section and section.h2.get_text()==story['heading'],slug
    tabs=section.select('[role=tab]');panels=section.select('[data-flow-panel]')
    assert len(tabs)==len(panels)==len(story['stages'])==3,slug
    assert page.select_one('.editorial-actions a[href="#product-benefits"]'),slug
    for tab,panel,stage in zip(tabs,panels,story['stages']):
        assert tab['aria-controls']==panel['id'],slug
        assert panel.h3.get_text()==stage['title'] and panel.select_one('.benefit-description').get_text()==stage['body'],slug
        assert page.find(id=stage['reference']),slug
        visual=panel.select_one('.benefit-visual svg[role=img]')
        assert (visual and visual.get('aria-label')) or panel.select_one('.benefit-visual img[alt]') or panel.select_one('.sunflex-infographic[role=group][aria-label]'),slug
        assert panel.select_one('.benefit-visual figcaption'),slug
        for image in visual.find_all('image') if visual else []:
            assert (root/image['href'].lstrip('/')).is_file(),slug
    # No orphaned ARIA relationships after replacing old tabbed procedures with disclosures.
    for tab in page.select('[role=tab][aria-controls]'):
        assert page.find(id=tab['aria-controls']),slug
    assert len([t['id'] for t in page.select('[id]')])==len(set(t['id'] for t in page.select('[id]'))),slug
print(f'PASS: {len(data)} stories / {len(data)*3} benefit panels, anchors, responsive media and preserved references')
