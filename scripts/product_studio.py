"""Product-specific presentation over the existing, preserved product content."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
from copy import deepcopy
ROOT = Path(__file__).resolve().parents[1]

def enhance(text, slug):
    if slug != 'compact-gas-detector':
        return text
    soup = BeautifulSoup(text, 'html.parser')
    soup.body['class'] = soup.body.get('class', []) + ['gas-studio']
    hero = soup.select_one('.editorial-hero')
    hero['class'] = ['gas-hero']
    copy = hero.select_one('.editorial-hero-copy')
    copy['class'] = ['gas-hero-copy']
    media = hero.select_one('.editorial-hero-media')
    media['class'] = ['gas-product-media']
    content = copy.select_one('.content-copy')
    content['class'] = ['gas-title-group']
    h1 = content.h1
    for br in h1.select('br'): br.replace_with(' ')
    tagline = content.select_one('.editorial-tagline')
    tagline['class'] = ['gas-display']
    tagline.clear()
    tagline.append('작업보다 먼저.')
    tagline.append(soup.new_tag('br'))
    tagline.append('공기를 살피다.')
    intro = soup.new_tag('section', attrs={'class':'gas-intro', 'aria-label':'제품 개요'})
    longcopy = content.select_one('.editorial-lead').find_next_sibling('p')
    intro.append(longcopy.extract())
    link = content.select_one('.source-hero-link')
    if link: intro.append(link.extract())
    image = media.img
    image['fetchpriority'] = 'high'
    image['loading'] = 'eager'
    image['sizes'] = '(max-width: 760px) 66vw, 400px'
    media.insert(0, BeautifulSoup('<span class="gas-media-label">SOLAR DETECT / GAS MONITORING</span><div class="gas-product-frame" aria-hidden="true"><i></i><i></i><i></i><i></i></div>', 'html.parser'))
    media.append(BeautifulSoup('<span class="gas-media-note">소형 복합가스 측정기</span>', 'html.parser'))
    hero.insert_after(intro)
    rail = soup.new_tag('ul', attrs={'class':'gas-elements','aria-label':'측정 대상 가스'})
    for symbol, name in [('O₂','산소'),('CO','일산화탄소'),('CH₄','메탄'),('H₂S','황화수소')]:
        li=soup.new_tag('li');strong=soup.new_tag('strong');strong.string=symbol
        label=soup.new_tag('span');label.string=name;li.extend([strong,label]);rail.append(li)
    hero.append(rail)
    benefits = soup.select_one('#product-benefits')
    benefits['class'] = ['gas-benefits']
    track=benefits.select_one('[data-scroll-flow]');del track['data-scroll-flow'];track['class']=['gas-scene'];track['data-gas-scene']=''
    stage=track.select_one('.product-flow-stage');stage['class']=['gas-scene-stage']
    controls=stage.select_one('.product-flow-tabs');controls['class']=['gas-scene-tabs']
    panels=stage.select_one('.benefit-panels');panels['class']=['gas-scene-panels']
    for panel in panels.select('[data-flow-panel]'):
        del panel['data-flow-panel'];panel['class']=['gas-scene-panel']
        # A shared, factual product photograph replaces generic stock illustrations.
        panel.select_one('.benefit-visual').decompose()
    layout = soup.new_tag('div', attrs={'class':'gas-frame-layout'})
    visual = soup.new_tag('figure', attrs={'class':'gas-frame-visual'})
    product = deepcopy(image)
    product['loading'] = 'lazy'
    product.attrs.pop('fetchpriority', None)
    visual.append(product)
    visual.append(BeautifulSoup('<figcaption>현장 측정<span>O₂ · CO · CH₄ · H₂S</span></figcaption>', 'html.parser'))
    layout.append(BeautifulSoup('<svg class="gas-frame-outline" viewBox="0 0 1000 400" preserveAspectRatio="none" aria-hidden="true"><rect x="1" y="1" width="998" height="398" vector-effect="non-scaling-stroke"/></svg>', 'html.parser'))
    layout.append(visual)
    layout.append(panels.extract())
    stage.append(layout)
    benefits.select_one('h2')['data-studio-visible'] = ''
    # Clear deep-link targets from sticky bars, including the existing source detail.
    for node in soup.select('.product-story [id]'):node['data-gas-anchor']=''
    for ext in ('css','js'):
        path=f'/assets/sunflex-v2/product-studio.{ext}'
        version=hashlib.sha256((ROOT/path.lstrip('/')).read_bytes()).hexdigest()[:10]
        if ext=='css': soup.head.append(soup.new_tag('link',rel='stylesheet',href=f'{path}?v={version}'))
        else:
            tag=soup.new_tag('script',src=f'{path}?v={version}');tag['defer']='';soup.body.append(tag)
    return str(soup)
