"""Release invariants for consolidated, source-preserving product pages."""
from pathlib import Path
import json
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
scenes=json.loads((R/'data/product-story-scenes.json').read_text())
assert len(scenes)==48
for slug,spec in scenes.items():
    page=BeautifulSoup((R/'products'/slug/'index.html').read_text(),'html.parser')
    assert page.select_one('[data-story-revision="20260920"]'),slug
    assert len(page.select('[data-scroll-flow]'))>=1,slug
    for flow in page.select('[data-scroll-flow]'):
        assert len(flow.select('.product-flow-tabs button'))==len(flow.select('[data-flow-panel]'))>=2,slug
    assert not page.select('.benefit-operation-list'),slug
    assert not page.select('[data-product-motion], [data-cctv-process]'),slug
    assert len(page.select('.revision-criteria li'))==3,slug
    css=[n['href'].split('?')[0].rsplit('/',1)[-1] for n in page.select('link[rel=stylesheet]')]
    assert css.index('product-revision.css') < css.index('product-infographics.css') < css.index('product-infographics-layout.css'),slug
    for card in page.select('[data-highlight-card=feature]'):assert card.find('img'),slug
    assert page.select_one('.product-story > .revision-source'),slug
    assert not page.select('main details'),slug
    assert page.select_one('[data-layout-family]'),slug
    assert not page.select('.revision-disclosure'),slug
    for link in page.select('a[href^="#"]'):
        assert page.find(id=link['href'][1:]),(slug,link['href'])
    for image in page.select('svg image[href]'):
        assert (R/image['href'].lstrip('/')).is_file(),(slug,image['href'])
    assert page.select_one('script[src^="/assets/sunflex-v2/product-revision.js"]'),slug
cms=BeautifulSoup((R/'products/site-cms/index.html').read_text(),'html.parser')
assert [x['data-infographic-scene'] for x in cms.select('#product-benefits .sunflex-infographic')]==[f'site-cms-{i}' for i in [1,2,3]]
assert len(cms.select('#product-benefits img'))==2
assert cms.select_one('#product-benefits .diagram-route')
for slug in ['smart-airbag','chatgpt-cctv','inspectcut','safebridge']:
    page=BeautifulSoup((R/'products'/slug/'index.html').read_text(),'html.parser')
    assert page.select_one('.revision-proof img'),slug
print('PASS: 48 revised pages, primary and operating stories retained, original detail access, SVG assets, three CMS phases and four proof sources.')
