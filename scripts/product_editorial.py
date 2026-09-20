"""Product-specific editorial layouts. Source facts remain untouched."""
import json
from pathlib import Path
from html import escape as e
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
PROFILES=json.loads((ROOT/'data/product-editorial-map.json').read_text())

COPY=json.loads((ROOT/'data/product-editorial-copy.json').read_text())

def apply_copy(soup,slug):
    """Only explicit, source-matched editorial substitutions may change source prose."""
    for edit in COPY[slug]['edits']:
        tag=soup.select(edit['selector'])[edit['index']]
        assert tag.get_text(' ',strip=True)==edit['before'],f'Copy source changed: {slug} {edit["selector"]}'
        tag.clear();tag.append(edit['after'])
        if edit['role']=='headline':
            tag.name='p';tag['class']=['editorial-tagline']
            lead=soup.new_tag('p',attrs={'class':'editorial-lead'});lead.string=COPY[slug]['lead'];tag.insert_after(lead)
    return soup

def addclass(tag,*names):tag['class']=tag.get('class',[])+list(names)

def build(p,group,g):
    slug=p['slug'];profile=PROFILES[slug];kind=profile['archetype']
    soup=BeautifulSoup((ROOT/f'data/solar-products/{slug}.html').read_text(),'html.parser')
    apply_copy(soup,slug)
    sections=soup.select('section.detail-block');hero=sections[0]
    hero['class']=['editorial-hero'];hero['data-product-hero']=''
    heading=hero.find('h2');heading.name='h1'
    for link in hero.find_all('a'):addclass(link,'source-hero-link')
    # Normalize first-page copy and media, preserving their complete source content.
    children=list(hero.find_all(recursive=False))
    copy=soup.new_tag('div',attrs={'class':'editorial-hero-copy'})
    media=soup.new_tag('div',attrs={'class':'editorial-hero-media'})
    for child in children:(media if child.find('img') or child.name=='figure' else copy).append(child.extract())
    hero.append(copy);hero.append(media)
    for image in media.find_all('img'):image['loading']='eager';image['sizes']='(max-width:760px) 90vw, 1100px'
    actions=BeautifulSoup(f'<div class="editorial-actions"><a class="editorial-button" href="/contact/?product={slug}">도입 문의</a><a href="#{profile["focus"]}">핵심 기능 살펴보기 <span aria-hidden="true">↓</span></a></div>','html.parser')
    copy.append(actions)
    # All source sections and anchors stay available; only the reading sequence changes.
    rest=sections[1:];focus=next(x for x in rest if x['id']==profile['focus'])
    if kind in ['lineup','workflow','workspace','communication','sensing']:
        rest.remove(focus);rest.insert(0,focus)
    for i,section in enumerate(rest):
        section['class']=['editorial-chapter']
        if section==focus:addclass(section,'chapter-focus')
        if section['id']=='highlights':addclass(section,'chapter-highlights')
        if section.find('img'):addclass(section,'chapter-media')
        else:addclass(section,'chapter-information')
        if i%3==1:addclass(section,'chapter-soft')
        # Restore visual grouping for semantic source diagrams without changing their text.
        for node in section.find_all(['div','article']):
            if node.find('strong',recursive=False) and node.find('p',recursive=False) and not node.find(['h2','h3'],recursive=False):
                addclass(node,'editorial-step-card')
        for node in section.find_all('div'):
            children=node.find_all(recursive=False)
            if len(children)>=2 and all('editorial-step-card' in c.get('class',[]) for c in children):
                addclass(node,'editorial-step-grid')
        # The source's meaningful figure/table structure remains intact.
        for table in section.find_all('table'):
            holder=soup.new_tag('div',attrs={'class':'editorial-table','tabindex':'0','role':'region','aria-label':'제품 구성 비교표'})
            table.wrap(holder)
        for svg in section.find_all('svg'):
            if svg.has_attr('viewbox'):svg['viewBox']=svg.attrs.pop('viewbox')
        if section==focus and kind in ['workflow','sensing','communication','workspace']:
            flow=section.find('ol')
            if flow and 2<=len(flow.find_all('li',recursive=False))<=6:
                addclass(flow,'editorial-flow')
                flow['aria-label']='제품 작동 단계'
                for step in flow.find_all('li',recursive=False):addclass(step,'editorial-flow-step')
        inner=soup.new_tag('div',attrs={'class':'editorial-section-inner'})
        for child in list(section.contents):inner.append(child.extract())
        section.append(inner)
    special=''
    if slug=='mobile-cctv':
        lineup=soup.find(id='mobile-cctv-lineup');grid=lineup.select_one('.content-grid')
        addclass(grid,'model-panels')
        controls='<div class="model-controls" hidden><div class="model-tabs" role="tablist" aria-label="무빙캠 모델 선택">'
        for i,(article,label) in enumerate(zip(grid.find_all('article',recursive=False),['S','M','L'])):
            article['id']='model-'+label.lower();article['data-model-panel']='';addclass(article,'model-panel')
            controls+=f'<button type="button" id="model-tab-{label.lower()}" role="tab" aria-controls="model-{label.lower()}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">무빙캠 {label}</button>'
        controls+='</div><button type="button" class="compare-models" aria-pressed="false">세 모델 비교하기</button></div>'
        grid.insert_before(BeautifulSoup(controls,'html.parser'))
        lineup['data-model-selector']=''
    if slug=='mobile-bodycam':
        modes=[('착용','이동하는 작업자의 시선에서.','바디캠을 몸에 착용해 이동하는 작업 구간을 기록합니다.'),('자석 크래들','구조물 가까이, 촬영 위치를 잡고.','촬영할 작업면 가까이에 자석 크래들로 거치하는 구성을 확인합니다.'),('삼각대','정해 둔 작업면을 기록하고.','같은 위치에서 촬영할 때는 삼각대 거치를 검토합니다.')]
        special='<section class="bodycam-use editorial-chapter" id="bodycam-use"><div class="editorial-section-inner"><p class="editorial-kicker">사용 방식</p><h2>몸에 착용하고.<br>작업면에 거치하고.</h2><div class="use-controls" role="tablist" aria-label="바디캠 사용 방식" hidden>'
        for i,(name,_,_) in enumerate(modes):special+=f'<button type="button" role="tab" id="use-tab-{i}" aria-controls="use-panel-{i}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{name}</button>'
        special+='</div><div class="use-panels">'
        for i,(name,title,desc) in enumerate(modes):special+=f'<article id="use-panel-{i}" data-use-panel><span class="editorial-kicker">{name}</span><h3>{title}</h3><p>{desc}</p><a href="#bodycam-film">현장 기록 흐름 보기 ↓</a></article>'
        special+='</div></div></section>'
    # A short, visual overview points to real chapters, not invented capabilities.
    overview=[]
    for sec in rest:
        if sec['id']=='highlights':continue
        h=sec.find('h2')
        if h:overview.append((sec['id'],h.get_text(' ',strip=True),sec.find('img')))
        if len(overview)==3:break
    rail='<section class="editorial-overview" id="product-content"><div class="editorial-section-inner"><div class="overview-heading"><h2>주요 기능 살펴보기.</h2><div class="overview-controls" hidden><button type="button" data-rail-prev aria-label="이전 기능">←</button><button type="button" data-rail-next aria-label="다음 기능">→</button></div></div><div class="overview-rail" tabindex="0" role="region" aria-label="주요 기능 바로가기">'
    for ident,title,image in overview:
        visual=f'<img src="{e(image["src"])}" alt="" loading="lazy" width="640" height="400">' if image else '<span class="overview-solar" aria-hidden="true">Solar.</span>'
        rail+=f'<a class="overview-card" href="#{ident}"><span>{e(title)}</span>{visual}<span class="overview-arrow" aria-hidden="true">↗</span></a>'
    rail+='</div></div></section>'
    firsttarget='mobile-cctv-lineup' if slug=='mobile-cctv' else 'product-content'
    firstlabel='라인업' if slug=='mobile-cctv' else '주요 기능'
    body=f'<div class="product-local-nav"><div class="wrap"><a class="product-local-name" href="#detail-1">{e(p["name"])}</a><nav aria-label="제품 메뉴"><a href="#{firsttarget}">{firstlabel}</a><a href="#{profile["focus"]}">자세히 보기</a><a class="editorial-button" href="/contact/?product={slug}">문의</a></nav></div></div>'
    hero_html=str(hero)
    if slug=='mobile-cctv' or kind in ['wearable','workspace']:
        motion='lineup' if slug=='mobile-cctv' else kind
        hero_html=f'<div class="editorial-hero-scroll" data-product-motion="{motion}">{hero}</div>'
    body+=f'<div class="product-story editorial-story" data-archetype="{kind}">{hero_html}{rail}'
    for i,sec in enumerate(rest):
        body+=str(sec)
        if kind=='wearable' and i==0:body+=special
    body+='</div>'
    return body
