"""Portfolio presentation layer. Facts, routes and product source anchors stay intact."""
import hashlib,json
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
CAT={p['slug']:p for p in json.loads((ROOT/'data/solar-catalog.json').read_text())}
PROFILES=json.loads((ROOT/'data/product-editorial-map.json').read_text())
FAMILIES={'detect':'감지','alert':'경보','respond':'대응','record':'기록'}

def addclass(n,c):
    n['class']=list(dict.fromkeys(n.get('class',[])+[c]))

def transform_scene(soup, root, comparison=False):
    track=root.select_one('[data-scroll-flow]')
    if not track:return
    track.attrs.pop('data-scroll-flow',None)
    track['class']=['studio-scene']
    track['data-studio-scene']='compare' if comparison else 'tabs'
    stage=track.select_one('.product-flow-stage');stage['class']=['studio-scene-stage']
    tabs=track.select_one('[role=tablist]');tabs['class']=['studio-tabs']
    panels=track.select('[data-flow-panel]')
    for panel in panels:
        panel.attrs.pop('data-flow-panel',None)
        panel['class']=['studio-panel']
    listing=panels[0].parent;listing['class']=['studio-panels']
    if comparison:
        tabs['role']='group'
        addclass(track,'studio-comparison')
        for tab in tabs.select('button'):
            tab.attrs.pop('role',None);tab.attrs.pop('aria-selected',None)
            tab['aria-pressed']='false';tab.attrs.pop('tabindex',None)
    for number in tabs.select('.benefit-tab-number'):
        # These are feature choices, not a claimed process sequence.
        if not comparison:number['aria-hidden']='true'

def enhance(text,path):
    soup=BeautifulSoup(text,'html.parser')
    if soup.select_one('meta[http-equiv=refresh]'):return text
    body=soup.body
    if not body:return text
    addclass(body,'site-studio')
    parts=path.split('/')
    slug=parts[1] if len(parts)>2 and parts[0]=='products' else None
    if slug in CAT:
        product=CAT[slug];kind=PROFILES[slug]['archetype']
        body['data-studio-kind']=kind;body['data-studio-family']=product['category'];body['data-studio-product']=slug
        if slug not in ('compact-gas-detector','mobile-cctv'):
            addclass(body,'studio-product')
            hero=soup.select_one('.editorial-hero')
            hero['class']=['studio-hero']
            copy=hero.select_one('.editorial-hero-copy');copy['class']=['studio-hero-copy']
            media=hero.select_one('.editorial-hero-media');media['class']=['studio-hero-media']
            for h in hero.select('h1 br'):h.replace_with(' ')
            tagline=hero.select_one('.editorial-tagline')
            if tagline:tagline['class']=['studio-display']
            crumb=soup.new_tag('p',attrs={'class':'studio-breadcrumb'})
            crumb.string=f'Solar {product["category"].title()} / {product["subgroup"]}'
            copy.insert(0,crumb)
            media.insert(0,BeautifulSoup('<div class="studio-viewfinder" aria-hidden="true"><i></i><i></i><i></i><i></i></div>','html.parser'))
            first_image=media.select_one('img')
            if first_image:
                width=float(first_image.get('width',0) or 0);height=float(first_image.get('height',0) or 0)
                if height and width/height<=1.4:media['data-studio-image']='portrait'
            for image in media.select('img'):
                image['loading']='eager';image['fetchpriority']='high'
                image['sizes']='(max-width: 760px) 90vw, (max-width: 1100px) 48vw, 680px'
            for source in media.select('source'):source['sizes']='(max-width: 760px) 90vw, 680px'
            # Long factual paragraphs remain immediately after the hero, not deleted.
            lead=copy.select_one('.editorial-lead')
            longcopy=[]
            if lead:
                for n in list(lead.find_next_siblings('p')):
                    longcopy.append(n.extract())
            if longcopy:
                intro=soup.new_tag('section',attrs={'class':'studio-intro','aria-label':'제품 개요'})
                for n in longcopy:intro.append(n)
                hero.insert_after(intro)
            if kind=='wearable':
                heading=copy.select_one('h1')
                context=heading.find_previous_sibling('p')
                if context and not context.get('class'):
                    meta=soup.new_tag('div',attrs={'class':'studio-product-meta'})
                    context.insert_before(meta);meta.append(context.extract());meta.append(heading.extract())
                source_link=copy.select_one('.source-hero-link')
                if source_link:
                    source_link['class']=['studio-context-link']
                    hero.insert_after(source_link.extract())
            if kind=='workspace':
                aside=soup.new_tag('div',attrs={'class':'studio-hero-aside'})
                for n in list(copy.select('.editorial-lead,.source-hero-link')):aside.append(n.extract())
                aside.append(copy.select_one('.editorial-actions').extract())
                copy.append(aside)
            benefits=soup.select_one('#product-benefits')
            if benefits:
                benefits['class']=['studio-benefits']
                transform_scene(soup,benefits)
            if slug=='site-cms':
                section=soup.select_one('#process-transition-line')
                transform_scene(soup,section,True)
                note=soup.new_tag('p',attrs={'class':'studio-phase-note'})
                note.string='공정별 배치 검토를 설명하는 예시 이미지입니다.'
                section.select_one('.studio-scene').insert_before(note)
        elif slug=='mobile-cctv':addclass(body,'studio-cctv')
    else:
        body['data-studio-page']=parts[0] if path!='index.html' else 'home'
        if path!='index.html':addclass(body,'studio-corporate')
    for ext in ('css','js'):
        asset=ROOT/f'assets/sunflex-v2/site-studio.{ext}'
        url='/'+str(asset.relative_to(ROOT))+'?v='+hashlib.sha256(asset.read_bytes()).hexdigest()[:10]
        if ext=='css':soup.head.append(soup.new_tag('link',rel='stylesheet',href=url))
        else:
            tag=soup.new_tag('script',src=url);tag['defer']='';soup.body.append(tag)
    return str(soup)

def apply_all():
    pages=[ROOT/'index.html',ROOT/'404.html']+[p for d in ['products','solutions','company','cases','contact','privacy'] for p in (ROOT/d).rglob('index.html')]
    for p in pages:p.write_text(enhance(p.read_text(),str(p.relative_to(ROOT))))
