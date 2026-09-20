#!/usr/bin/env python3
"""Rebuild the complete SUNPLEX site from preserved product content."""
import importlib.util, json, re, hashlib
from pathlib import Path
from html import escape as e
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('corporate',ROOT/'scripts/generate-sunflex-v2.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
CAT=json.loads((ROOT/'data/solar-catalog.json').read_text())
BY={p['slug']:p for p in CAT}
GROUPS={
'detect':('Detect','감지','현장의 변화를 살피다.','작업 구역의 영상과 환경 정보를 확인하는 제품을 살펴보세요.','field-crane-hook-rigging-generated'),
'alert':('Alert','경보','위험을 알아차릴 수 있도록.','접근과 위험 상황을 소리와 빛으로 알리는 제품을 확인하세요.','field-vehicle-pedestrian-generated'),
'respond':('Respond','대응','대응이 필요한 순간을 위해.','작업자 보호와 현장 대응에 필요한 장비를 살펴보세요.','company-promise-night-worker-generated'),
'record':('Record','기록','현장의 정보를 남기다.','점검과 작업 정보를 기록하고 관리하는 제품을 확인하세요.','field-office-handover-generated')}
FACETS={
'problem':('필요한 기능',{'monitoring':'현장 모니터링','education-translation':'교육·통역','access-location':'출입·위치','crane-lifting':'양중·크레인','environment':'환경 관리','inspection-record':'점검·기록','worker-protection':'작업자 보호','emergency-alert':'비상 알림'}),
'installation':('설치 방식',{'fixed':'고정형','mobile':'이동형','wearable':'착용형','equipment-mounted':'장비 부착형','software':'소프트웨어'}),
'connectivity':('통신 방식',{'wired':'유선','wifi':'Wi-Fi','lte':'LTE','wireless':'무선','radio':'무전','standalone':'독립형','offline-capable':'오프라인 사용 지원'}),
'process':('업무 단계',{'detect':'감지','analyze':'분석','alert':'알림','respond':'대응','record':'기록','lifting':'양중'})}
for key in FACETS:
    for p in CAT:
        for value in p[key]: FACETS[key][1].setdefault(value,value)

def summary(p):
    s=p['outcome'].strip()
    return s.removeprefix(p['name']).strip() or p['subgroup']+' 제품의 주요 기능과 적용 조건을 확인하세요.'
def img(p,lazy=True):
    im=p['images'][0]
    return f'<img src="{e(im["src"])}" alt="{e(im["alt"] or p["name"])}" width="{im["width"]}" height="{im["height"]}" loading="{"lazy" if lazy else "eager"}" decoding="async">'
def card(p,filterable=False):
    attrs=''
    if filterable:
        attrs=' data-catalog-card '+ ' '.join(f'data-{k}="{e(" ".join(p[k]) if isinstance(p[k],list) else p[k])}"' for k in ['category','problem','installation','connectivity','process'])+f' data-search="{e(p["name"]+" "+summary(p)+" "+p["subgroup"])}"'
    return f'<article class="solar-card"{attrs}><a href="/products/{p["slug"]}/"><div class="solar-card-image">{img(p)}<span aria-hidden="true" class="card-arrow">↗</span></div><div class="solar-card-copy"><span class="eyebrow">Solar {GROUPS[p["category"]][0]} · {p["subgroup"]}</span><h3>{e(p["name"])}</h3><p>{e(summary(p))}</p></div></a></article>'
def family_links():
    return ''.join(f'<a href="/solutions/{k}/"><span>0{i+1} / {v[1]}</span><strong>Solar {v[0]}</strong><span aria-hidden="true">↗</span></a>' for i,(k,v) in enumerate(GROUPS.items()))
old_header=g.header
old_footer=g.footer
old_render=g.render

def header(active):
    s=old_header(active).replace('적용 분야','Solar 솔루션')
    # A native disclosure works with keyboard and without scripting.
    mega=f'<details class="solar-menu"><summary>제품군 둘러보기 <span aria-hidden="true">＋</span></summary><div class="solar-menu-panel"><div class="wrap family-links">{family_links()}</div><div class="wrap mega-bottom"><a href="/products/">48개 제품 전체 보기 ↗</a><a href="/solutions/safety-box/">안전종합상황판 ↗</a></div></div></details>'
    return s.replace('</header>',mega+'</header>')
def footer():
    return old_footer().replace('적용 분야','Solar 솔루션').replace('제품 정보부터 도입 상담까지 안내합니다.','Solar 제품군과 현장 도입을 안내합니다.')
def render(path,title,desc,body,active=''):
    g.ALLOWED.add(path)
    old_render(path,title,desc,body,active)
    p=ROOT/path;s=p.read_text()
    extra=''
    for ext in ['css','js']:
        v=hashlib.sha256((ROOT/f'assets/sunflex-v2/solar-site.{ext}').read_bytes()).hexdigest()[:10]
        extra+=f'<link rel="stylesheet" href="/assets/sunflex-v2/solar-site.css?v={v}">' if ext=='css' else f'<script defer src="/assets/sunflex-v2/solar-site.js?v={v}"></script>'
    s=s.replace('</head>',extra+'</head>')
    s=s.replace('적용 분야 보기','Solar 솔루션 보기').replace('적용 분야 살펴보기','Solar 솔루션 살펴보기')
    p.write_text(s)
g.header=header;g.footer=footer;g.render=render

def families():
    return '<div class="solar-families">'+''.join(f'<a class="solar-family" href="/solutions/{k}/" style="--family-index:{i}"><span class="eyebrow">0{i+1} / {v[1]}</span><h3>Solar<br>{v[0]}<span aria-hidden="true">↗</span></h3><p>{v[3]}</p><span class="family-count">{sum(p["category"]==k for p in CAT):02d} PRODUCTS</span></a>' for i,(k,v) in enumerate(GROUPS.items()))+'</div>'

def catalog():
    tabs='<button type="button" data-category="" aria-pressed="true">전체 <small>48</small></button>'+''.join(f'<button type="button" data-category="{k}" aria-pressed="false">Solar {v[0]} <small>{sum(p["category"]==k for p in CAT)}</small></button>' for k,v in GROUPS.items())
    filters=''.join(f'<label>{label}<select name="{key}"><option value="">전체</option>'+''.join(f'<option value="{val}">{lab}</option>' for val,lab in values.items() if any(val in p[key] for p in CAT))+'</select></label>' for key,(label,values) in FACETS.items())
    body=g.head('SUNPLEX / SOLAR PRODUCTS','현장을 위한<br><em>솔라 솔루션.</em>','보고, 듣고, 살피고, 지키고, 기록하는 제품.<br>우리 현장에 필요한 솔라 솔루션을 찾아보세요.',cls='solar-catalog-head')
    body+=f'<section class="wrap catalog-section" id="catalog"><div class="catalog-tools" hidden><label class="catalog-search">제품 검색<input name="q" type="search" placeholder="제품명 또는 필요한 기능을 입력하세요" autocomplete="off"></label><div class="catalog-tabs" role="group" aria-label="Solar 제품군">{tabs}</div><details class="catalog-filters"><summary>현장 조건으로 좁혀보기 <span aria-hidden="true">＋</span></summary><div class="filter-grid">{filters}</div></details><div class="catalog-count"><p role="status" aria-live="polite"><strong id="result-count">48</strong>개 제품</p><button type="button" data-reset>조건 초기화 ↺</button></div></div><div class="solar-grid">'+''.join(card(p,True) for p in CAT)+'</div><div class="catalog-empty" hidden><h2>조건에 맞는 제품이 없습니다.</h2><p>검색어를 짧게 입력하거나 선택한 조건을 줄여보세요.</p><button class="btn" type="button" data-reset>전체 제품 보기</button></div></section>'+g.cta()
    render('products/index.html','Solar 제품','Solar Detect, Alert, Respond, Record. 현장 조건과 필요한 기능으로 48개 산업안전 제품을 찾아보세요.',body,'/products/')

def detail(p):
    group=GROUPS[p['category']];slug=p['slug']
    thumbs=''.join(f'<button type="button" data-gallery-src="{e(im["src"])}" data-gallery-alt="{e(im["alt"])}" aria-label="제품 이미지 {i+1}: {e(im["alt"])}" aria-pressed="{str(i==0).lower()}"><img src="{e(im["src"])}" alt="" width="80" height="80" loading="lazy"></button>' for i,im in enumerate(p['images'][:4]))
    body=f'<div class="wrap breadcrumbs"><a href="/products/">제품</a><span>/</span><a href="/solutions/{p["category"]}/">Solar {group[0]}</a><span>/</span><span>{e(p["name"])}</span></div><section class="wrap product-hero"><div class="product-hero-copy"><span class="eyebrow">Solar {group[0]} / {group[1]}</span><h1>{e(p["name"])}</h1><p class="product-summary">{e(summary(p))}</p><span class="product-type">{e(p["subgroup"])}</span><div class="actions">{g.link("/contact/?product="+slug,"이 제품 문의","btn")}{g.link("#product-content","제품 상세 보기")}</div><p class="spec-note">구성과 적용 범위는 제품 사양 및 설치 환경에 따라 확인이 필요합니다.</p></div><div class="product-gallery"><div class="gallery-stage">{img(p,False)}</div><div class="gallery-thumbs" aria-label="제품 이미지 선택" hidden>{thumbs}</div></div></section>'
    nav=''.join(f'<a href="#{s["id"]}"><span>{i+1:02}</span>{e(s["title"])}</a>' for i,s in enumerate(p['sections']))
    content=(ROOT/f'data/solar-products/{slug}.html').read_text()
    body+=f'<div class="product-body wrap" id="product-content"><aside class="product-index"><span class="eyebrow">제품 상세</span><nav aria-label="제품 상세 목차">{nav}</nav>{g.link("/contact/?product="+slug,"도입 문의")}</aside><div class="product-story">{content}</div></div>'
    related=[BY[s] for s in p['related'] if s in BY][:3]
    if len(related)<3:
        related += [x for x in CAT if x['category']==p['category'] and x!=p and x not in related][:3-len(related)]
    body+='<section class="section wrap" id="related"><div class="lead"><h2>함께 살펴볼 제품</h2><p>관리할 구역과 필요한 기능을 기준으로 비교해 보세요.</p></div><div class="solar-grid">'+''.join(card(x) for x in related)+'</div></section>'
    body+=f'<div class="wrap" id="consultation"><section class="final-cta"><div><span class="eyebrow">{e(p["name"])}</span><h2>우리 현장에 적용할 수 있을까요?</h2><p>설치 위치와 사용 목적을 알려주세요.</p></div>{g.link("/contact/?product="+slug,"이 제품 문의","btn")}</section></div>'
    render(f'products/{slug}/index.html',p['name'],summary(p),body,'/products/')

def category(k):
    name,ko,title,desc,scene=GROUPS[k];products=[p for p in CAT if p['category']==k]
    groups=list(dict.fromkeys(p['subgroup'] for p in products))
    body=f'<section class="solar-category-hero"><div class="category-backdrop">{g.picture(scene,ko+" 제품을 검토할 산업현장",True,"100vw")}</div><div class="wrap"><span class="eyebrow">SUNPLEX / SOLAR SOLUTIONS / {ko}</span><h1>Solar<br><em>{name}</em></h1><div class="category-intro"><h2>{title}</h2><p>{desc}</p><a class="text-link" href="#category-products">{len(products)}개 제품 살펴보기 ↓</a></div></div></section><section class="section wrap"><div class="lead"><h2>현장에 필요한 기능부터.</h2><p>같은 제품군에서도 설치 방식과 적용 대상은 다릅니다.<br>제품별 기능과 사양을 확인해 주세요.</p></div><div class="category-topics">'+''.join(f'<a href="/products/?category={k}&q={e(s)}"><span>{i+1:02}</span><h3>{s}</h3><span aria-hidden="true">↗</span></a>' for i,s in enumerate(groups))+'</div></section>'
    body+=f'<section class="section wrap" id="category-products"><div class="lead"><h2>Solar {name}<br>제품 안내</h2><p>{len(products)}개 제품 · {ko}</p></div><div class="solar-grid">'+''.join(card(p) for p in products)+'</div></section><section class="section wrap"><div class="lead"><h2>다른 Solar 제품군</h2></div>'+families()+'</section>'+g.cta()
    render(f'solutions/{k}/index.html','Solar '+name+' · '+ko,desc,body,'/solutions/')

def solar_landing():
    # Preserve established industry anchor targets while adding a brand-first entry.
    g.solutions()
    path=ROOT/'solutions/index.html';soup=BeautifulSoup(path.read_text(),'html.parser')
    h=soup.select_one('.page-head')
    h.replace_with(BeautifulSoup(g.head('SUNPLEX / SOLAR SOLUTIONS','현장을 살피는 기술.<br><em>Solar.</em>','감지하고, 알리고, 대응하고, 기록합니다.<br>현장에 필요한 기능을 네 가지 Solar 제품군에서 찾아보세요.', '<a class="text-link" href="#solar-families">Solar 제품군 살펴보기 ↓</a>', 'solar-landing-head')+f'<section class="wrap section" id="solar-families">{families()}</section><section class="wrap solar-industry-title"><span class="eyebrow">산업별 적용 분야</span><h2>어떤 현장에서<br>사용하시나요?</h2><nav class="anchor-nav" aria-label="산업별 적용 분야"><a href="#construction">건설·토목</a><a href="#logistics">제조·물류</a><a href="#enclosed">밀폐·지하 공간</a></nav></section>','html.parser'))
    soup.title.string='Solar 솔루션 | 썬플렉스'
    for tag in soup.select('meta[name="description"],meta[property="og:description"]'): tag['content']='Solar Detect, Alert, Respond, Record. 현장에 필요한 산업안전 제품군과 적용 분야를 확인하세요.'
    soup.select_one('meta[property="og:title"]')['content']='Solar 솔루션 | SUNPLEX'
    path.write_text(str(soup))

def safety_box():
    # Preserve the original platform description and imagery in the shared detail system.
    import subprocess
    original=subprocess.check_output(['git','show','b71218a:solutions/safety-box/index.html'],cwd=ROOT,text=True)
    soup=BeautifulSoup(original,'html.parser');main=soup.find('main')
    for x in main.select('script,style,nav,noscript'):x.decompose()
    for x in main.find_all(True):
        for a in list(x.attrs):
            if a in ['class','style'] or a.startswith('data-'): 
                if a=='data-src': x['src']=x[a]
                del x[a]
        if x.name=='h1':x.name='h2'
        if x.name=='img':x['loading']='lazy';x['decoding']='async'
    for a in main.find_all('a',href=True):
        if a['href']=='/solutions#process': a['href']='/solutions/#solar-families'
    body=g.head('SOLAR / 현장 정보 관리','안전종합상황판','현장에서 확인할 정보를 한곳에서 살펴보세요. 제품의 구성과 연동 범위는 별도 확인이 필요합니다.')+f'<div class="wrap platform-story product-story"><section class="detail-block">{main.decode_contents()}</section></div>'+g.cta()
    render('solutions/safety-box/index.html','안전종합상황판','현장 안전정보를 확인하는 안전종합상황판의 구성과 주요 기능을 살펴보세요.',body,'/solutions/')

def enhance_corporate():
    # Useful interactions and consistent chapter navigation for long corporate pages.
    for name in ['company','cases','contact','privacy']:
        path=ROOT/f'{name}/index.html';soup=BeautifulSoup(path.read_text(),'html.parser')
        links=[]
        for i,section in enumerate(soup.select('main > section, main > div.legal > section')):
            h=section.find('h2')
            if not h or 'page-head' in section.get('class',[]):continue
            section['id']=section.get('id',f'chapter-{i}')
            links.append((section['id'],h.get_text(' ',strip=True)))
        if links:
            nav=BeautifulSoup('<div class="wrap chapter-links"><nav aria-label="페이지 목차">'+''.join(f'<a href="#{ident}"><small>{i+1:02}</small>{e(title)}</a>' for i,(ident,title) in enumerate(links))+'</nav></div>','html.parser')
            soup.select_one('.page-head').insert_after(nav)
        if name=='cases':
            faq=soup.select_one('.faq')
            faq.insert(0,BeautifulSoup('<div class="faq-search" hidden><label for="support-search">궁금한 내용 찾기</label><input id="support-search" type="search" placeholder="제품, 자료, 설치 등으로 검색"><p role="status" id="support-search-status"></p></div>','html.parser'))
        if name=='contact':
            data=soup.new_tag('script',type='application/json',id='product-names');data.string=json.dumps({p['slug']:p['name'] for p in CAT},ensure_ascii=False);soup.body.append(data)
            steps=BeautifulSoup('<ol class="inquiry-steps wrap"><li><span>01</span>현장 조건 정리</li><li><span>02</span>문의 내용 작성</li><li><span>03</span>이메일에서 확인·전송</li></ol>','html.parser');soup.select_one('.chapter-links').insert_after(steps)
        path.write_text(str(soup))

def redirects():
    for old,new in [('eyes','detect'),('sound','alert'),('guard','respond'),('story','record'),('air','detect')]:
        p=ROOT/f'solutions/{old}/index.html'
        # Preserve the historical destination, including air's existing mapping.
        import subprocess
        original=subprocess.check_output(['git','show',f'b71218a:solutions/{old}/index.html'],cwd=ROOT,text=True)
        match=re.search(r'url=([^";]+)',original)
        dest=match.group(1) if match else f'/solutions/{new}/'
        dest=dest.rstrip('/')+'/'
        body=g.head('SOLAR SOLUTIONS','페이지 이동 안내','Solar 솔루션 페이지로 이동합니다.',g.link(dest,'Solar 솔루션 보기','btn'))
        render(f'solutions/{old}/index.html','Solar 솔루션 이동 안내','Solar 솔루션의 새로운 페이지로 이동합니다.',body)
        s=p.read_text().replace('</head>',f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={dest}"></head>')
        s=re.sub(r'<link rel="canonical"[^>]+>',f'<link rel="canonical" href="{g.DOMAIN}{dest}">',s);p.write_text(s)

if __name__=='__main__':
    for fn in [g.home,g.company,g.support,g.contact,g.privacy,g.error]:fn()
    solar_landing();catalog()
    for p in CAT:detail(p)
    for k in GROUPS:category(k)
    safety_box();enhance_corporate();redirects()
    print('Generated 61 content pages and 5 redirects; preserved 48 product detail sources.')
