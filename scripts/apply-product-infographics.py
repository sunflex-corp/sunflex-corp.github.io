"""Replace only existing benefit figures and append scoped styles; safe to rerun."""
from pathlib import Path
import hashlib,json,re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
FIGURES=json.loads((ROOT/'data/product-infographics.json').read_text())
PATTERN=re.compile(r'<figure\b(?=[^>]*\bclass="[^"]*\bbenefit-visual\b)[^>]*>.*?</figure>',re.S)
for slug,figures in FIGURES.items():
    file=ROOT/'products'/slug/'index.html';text=file.read_text()
    page=BeautifulSoup(text,'html.parser')
    if slug=='pedestrian-collision-prevention':
        old=page.select('#blind-corner [data-flow-panel] > .pedestrian-scene, #blind-corner [data-flow-panel] > .infographic-visual')
        assert len(old)==3,slug
        for node,figure in zip(old,figures):node.replace_with(BeautifulSoup(figure,'html.parser'))
        for link in page.select('link[href*="/product-infographics"]'):link.decompose()
        text=str(page)
        old=None
    else:
        old=page.select('#product-benefits [data-flow-panel] > .benefit-visual')
    assert old is None or len(old)==3,slug
    # Nested figures in new technical diagrams require a balanced DOM replacement
    # on subsequent runs, but initial import retains every other original byte.
    if old is None:
        pass
    elif page.select_one('#product-benefits .sunflex-infographic'):
        for node,figure in zip(old,figures):node.replace_with(BeautifulSoup(figure,'html.parser'))
        for link in page.select('link[href*="/product-infographics"]'):link.decompose()
        text=str(page)
    else:
        section=re.search(r'<section\b(?=[^>]*\bid="product-benefits")[^>]*>.*?</section>',text,re.S)
        assert section,slug
        region=section.group();matches=list(PATTERN.finditer(region))
        assert len(matches)==3,(slug,len(matches))
        for match,figure in reversed(list(zip(matches,figures))):region=region[:match.start()]+figure+region[match.end():]
        text=text[:section.start()]+region+text[section.end():]
    if slug=='site-cms':
        # These informative process images need descriptions after every site rebuild.
        page=BeautifulSoup(text,'html.parser')
        for phase,description in {
            'early':'굴착 장비와 차량이 작업 중인 착공 초기 현장',
            'mid':'타워크레인과 여러 층의 골조가 형성된 공정 전환 현장',
            'late':'외벽 공사와 지상부 정리가 진행 중인 준공 전 현장',
        }.items():
            image=page.select_one(f'img[src="/media/derived/site-cms-stage-{phase}-768.avif"]')
            assert image,phase
            image['alt']=description
            image.find_parent('figure').figcaption.string=description
        text=str(page)
    styles=''
    for name in ['product-infographics','product-infographics-layout']:
        asset=ROOT/f'assets/sunflex-v2/{name}.css';version=hashlib.sha256(asset.read_bytes()).hexdigest()[:10]
        styles+=f'<link rel="stylesheet" href="/assets/sunflex-v2/{name}.css?v={version}">'
    text=text.replace('</head>',styles+'</head>')
    file.write_text(text)
print(f'Applied {len(FIGURES)} product pages / 144 benefit figures')
