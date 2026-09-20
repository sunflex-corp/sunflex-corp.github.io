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
    assert len(page.select('[data-scroll-flow]'))==1,slug
    assert not page.select('[data-product-motion], [data-cctv-process]'),slug
    assert len(page.select('.revision-criteria li'))==3,slug
    assert page.select_one('.revision-disclosure'),slug
    for link in page.select('a[href^="#"]'):
        assert page.find(id=link['href'][1:]),(slug,link['href'])
    for image in page.select('svg image[href]'):
        assert (R/image['href'].lstrip('/')).is_file(),(slug,image['href'])
    assert page.select_one('script[src^="/assets/sunflex-v2/product-revision.js"]'),slug
cms=BeautifulSoup((R/'products/site-cms/index.html').read_text(),'html.parser')
assert [x['src'] for x in cms.select('#product-benefits img')]==[f'/media/derived/site-cms-stage-{phase}-768.avif' for phase in ['early','mid','late']]
for slug in ['smart-airbag','chatgpt-cctv','inspectcut','safebridge']:
    page=BeautifulSoup((R/'products'/slug/'index.html').read_text(),'html.parser')
    assert page.select_one('.revision-proof img'),slug
print('PASS: 48 revised pages, one story each, original detail access, SVG assets, three CMS phases and four proof sources.')
