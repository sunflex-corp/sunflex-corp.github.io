#!/usr/bin/env python3
"""Generate only the seven SUNPLEX corporate pages. Product assets are read-only."""
from pathlib import Path
from html import escape
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'index.html', 'company/index.html', 'solutions/index.html', 'cases/index.html', 'contact/index.html', 'privacy/index.html', '404.html'}
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'
DOMAIN = 'https://sunflex-corp.github.io'
def link(href, text, cls='text-link'):
    return f'<a class="{cls}" href="{href}">{text}{ARROW}</a>'

def picture(name, alt='', eager=False, sizes='(max-width: 760px) 100vw, 50vw'):
    widths = [w for w in (480, 768, 1280, 1920) if (ROOT / f'media/derived/{name}-{w}.webp').exists()]
    if not widths:
        raise ValueError(f'Missing image {name}')
    srcset = ', '.join(f'/media/derived/{name}-{w}.webp {w}w' for w in widths)
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<picture><img src="/media/derived/{name}-{widths[-1]}.webp" srcset="{srcset}" sizes="{sizes}" alt="{escape(alt)}" width="1920" height="1080" {load} decoding="async"></picture>'

def header(active):
    items = [('/solutions/', '적용 분야'), ('/products/', '제품'), ('/company/', '기업소개'), ('/cases/', '고객지원')]
    links = ''.join(f'<a href="{url}"' + (' aria-current="page"' if url == active else '') + f'>{text}</a>' for url, text in items)
    return f'''<a class="skip" href="#main-content">본문으로 건너뛰기</a>
<header class="site-header"><div class="wrap header-inner"><a class="logo" href="/" aria-label="썬플렉스 홈"><img src="/brand/sunplex-wordmark-white.svg" width="150" height="35" alt="SUNPLEX"></a><nav class="desktop-nav" aria-label="주 메뉴">{links}</nav><a class="header-cta" href="/contact/">도입 문의 {ARROW}</a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" hidden>메뉴</button></div><nav class="mobile-nav" id="mobile-nav" aria-label="모바일 메뉴">{links}<a href="/contact/">도입 문의 {ARROW}</a></nav></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="wrap"><div class="footer-top"><div class="footer-brand"><a href="/" aria-label="썬플렉스 홈"><img src="/brand/sunplex-wordmark-white.svg" width="170" height="39" alt="SUNPLEX" loading="lazy"></a><p>산업현장을 위한 스마트 안전 솔루션.<br>제품 정보부터 도입 상담까지 안내합니다.</p></div><nav class="footer-links" aria-label="하단 메뉴"><a href="/solutions/">적용 분야</a><a href="/products/">제품</a><a href="/company/">기업소개</a><a href="/cases/">고객지원</a><a href="/contact/">도입 문의</a></nav><div class="footer-contact"><strong>(주)썬플렉스</strong><a href="tel:0319912285">031-991-2285</a><a href="mailto:jiyoueng@daum.net">jiyoueng@daum.net</a><p>경기도 시흥시 신천동 845-18</p></div></div><div class="footer-bottom"><span>© 2026 SUNPLEX. All rights reserved.</span><a href="/privacy/">개인정보·현장 데이터 안내</a></div><div class="wordmark-end" aria-hidden="true">SUNPLEX</div></div></footer>'''

def cta():
    return f'<div class="wrap"><section class="final-cta"><div><h2>우리 현장에 맞는 제품이 궁금하신가요?</h2><p>관심 제품과 설치 환경을 알려주시면 상담에 도움이 됩니다.</p></div>{link("/contact/", "도입 문의", "btn")}</section></div>'

def head(label, title, desc='', extra='', cls=''):
    return f'<section class="page-head {cls}"><div class="wrap"><span class="eyebrow">{label}</span><h1>{title}</h1>' + (f'<p>{desc}</p>' if desc else '') + extra + '</div></section>'

def render(path, title, desc, body, active=''):
    if path not in ALLOWED:
        raise ValueError(f'Refusing to write protected path {path}')
    url = '/' if path == 'index.html' else ('/404.html' if path == '404.html' else '/' + path.removesuffix('index.html'))
    css = hashlib.sha256((ROOT/'assets/sunflex-v2/site.css').read_bytes()).hexdigest()[:10]
    js = hashlib.sha256((ROOT/'assets/sunflex-v2/site.js').read_bytes()).hexdigest()[:10]
    schema = {'@context':'https://schema.org','@type':'Organization','name':'(주)썬플렉스','url':DOMAIN,'logo':DOMAIN+'/brand/sunplex-wordmark.png','telephone':'031-991-2285','email':'jiyoueng@daum.net','address':{'@type':'PostalAddress','streetAddress':'신천동 845-18','addressLocality':'시흥시','addressRegion':'경기도','addressCountry':'KR'}}
    robots = '<meta name="robots" content="noindex">' if path == '404.html' else ''
    page = f'''<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | 썬플렉스</title><meta name="description" content="{escape(desc)}"><meta name="theme-color" content="#08090b">{robots}<link rel="canonical" href="{DOMAIN}{url}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="{escape(title)} | SUNPLEX"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{DOMAIN}{url}"><meta property="og:image" content="{DOMAIN}/brand/sunplex-wordmark.png"><link rel="preload" href="/fonts/AstaSans-Medium.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/sunflex-v2/site.css?v={css}"><script src="/assets/sunflex-v2/site.js?v={js}" defer></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><style>@media(min-width:761px){{.mobile-nav{{display:none}}}}</style></head><body class="sunflex-v2">{header(active)}<main id="main-content" tabindex="-1">{body}</main>{footer()}</body></html>\n'''
    (ROOT/path).write_text(page, encoding='utf-8')

def product_links(items):
    return '<ul class="product-links">' + ''.join(f'<li>{link("/products/"+slug+"/",name, "")}</li>' for slug,name in items) + '</ul>'

def home():
    rows = [('field-vehicle-pedestrian-generated','차량·작업자 이동 구역','차량과 작업자의 이동 경로, 진출입 구간에 필요한 경보·안내 장비를 살펴보세요.','logistics'),('product-gas-alarm-problem','밀폐공간·작업 환경','가스 농도와 온습도 등 작업 환경을 확인하는 측정·경보 장비를 살펴보세요.','enclosed'),('field-office-handover-generated','현장 영상·운영 관리','작업 구역의 영상을 확인하고 현장 정보를 관리하는 제품을 살펴보세요.','construction')]
    # Use an existing scene if the product problem asset is unavailable.
    rows[1] = ('home-role-field-tunnel', *rows[1][1:])
    row_html=''.join(f'<a class="field-row" href="/solutions/#{anchor}">{picture(img)}<div><h3>{name}</h3><p>{desc}</p></div>{ARROW}</a>' for img,name,desc,anchor in rows)
    products=[('mobile-cctv','이동식 CCTV','영상 확인','product-mobile-cctv-reference-white-20260912'),('compact-gas-detector','소형 복합가스 측정기','작업 환경 확인','product-compact-gas-detector-reference-white-20260912'),('site-cms','현장 CMS 구축','현장 정보 관리','product-site-cms-reference-white-20260912')]
    # Extract each product's existing primary product illustration; never alter it.
    from html.parser import HTMLParser
    class Images(HTMLParser):
        def __init__(self): super().__init__(); self.paths=[]
        def handle_starttag(self,tag,attrs):
            d=dict(attrs)
            if tag=='img' and '/media/derived/' in d.get('src',''): self.paths.append((d['src'],d.get('alt','')))
    cards=[]
    for slug,name,category,_ in products:
        parser=Images();parser.feed((ROOT/f'products/{slug}/index.html').read_text())
        src=next((s for s,a in parser.paths if 'reference' in s or 'restored' in s),parser.paths[0][0])
        cards.append(f'<a class="product-spotlight" href="/products/{slug}/"><div class="image"><img src="{src}" alt="{name}" width="640" height="480" loading="lazy" decoding="async"></div><div><h3>{name}{ARROW}</h3><p>{category}</p></div></a>')
    aliases=['construction','civil','logistics','tunnel','manufacturing','plant','environment','facility','training','headquarters']
    body=f'''<section class="hero"><div class="wrap hero-copy"><span class="eyebrow">썬플렉스 · 산업안전 솔루션</span><h1>산업현장을 위한<br><span>스마트 안전 솔루션.</span></h1><p class="intro">영상관제, 위험 알림, 작업 환경 측정까지.<br>현장에 필요한 안전장비를 확인하세요.</p><div class="actions">{link('/solutions/','적용 분야 보기','btn')}{link('/products/','제품 전체 보기')}</div></div><div class="hero-image">{picture('field-crane-hook-rigging-generated','크레인 인양 장비를 점검하는 작업 장면',True)}</div></section>
<div class="wrap"><div class="hero-bottom"><span>건설 · 제조 · 물류 현장</span><a href="#fields">적용 분야 살펴보기 <span aria-hidden="true">↓</span></a></div></div>
<section class="section wrap" id="fields"><div class="legacy-anchors">{''.join(f'<span id="field-site-{a}"></span>' for a in aliases)}</div><div class="lead"><h2>작업 환경에 맞는<br>안전장비를 살펴보세요.</h2><p>차량이 오가는 구역과 밀폐된 작업 공간은 관리 방법이 다릅니다. 현장의 위험요인에 따라 필요한 제품을 확인하세요.</p></div><div class="field-rows">{row_html}</div></section>
<section class="section feature"><div class="wrap feature-grid"><figure class="feature-visual">{picture('consultation-field-planning-generated','도면 위에서 설치 위치와 작업 구역을 살펴보는 장면')}<figcaption class="caption">설치와 운영 조건을 살펴보는 장면</figcaption></figure><div class="feature-copy"><span class="eyebrow">도입 전 확인할 것</span><h2>도입 전에는<br>설치 환경을 확인하세요.</h2><p>설치 위치와 전원·통신 환경에 따라 사용할 수 있는 장비와 구성이 달라집니다. 도입을 검토할 때 함께 확인해 주세요.</p><ul class="checks"><li>설치 위치<small>고정·이동 여부와 확인할 범위</small></li><li>전원·통신<small>전원 공급과 통신 가능 구역</small></li><li>알림과 기록<small>확인할 담당자와 필요한 정보</small></li></ul>{link('/contact/#prepare','문의에 필요한 정보 확인')}</div></div></section>
<section class="section wrap"><div class="lead"><h2>주요 제품 안내</h2><p>제품별 주요 기능과 적용 조건을 확인하고,<br>현장에 필요한 장비를 검토하세요.</p></div><div class="product-spotlights">{''.join(cards)}</div><div class="actions">{link('/products/','모든 제품 보기')}</div></section>
<section class="company-band"><div class="copy"><span class="eyebrow">기업소개</span><h2>현장 안전관리에 필요한<br>기술을 제안합니다.</h2><p>썬플렉스는 산업현장에서 사용하는 안전장비와 솔루션을 안내합니다. 제품의 기능은 물론 설치·운영에 필요한 조건도 함께 살펴보실 수 있습니다.</p>{link('/company/','썬플렉스 알아보기')}</div>{picture('company-promise-night-worker-generated','조명이 켜진 산업현장을 걸어가는 작업자')}</section>
<section class="section wrap"><div class="lead"><h2>제품 자료와 문의 안내</h2><p>제품 사양을 확인하거나 사용 중 궁금한 점이 있으신가요? 필요한 안내를 선택해 주세요.</p></div><div class="resource-list">{link('/products/','<span><strong>제품 정보</strong><small>관심 제품의 기능과 상세 안내</small></span>','row-link')}{link('/cases/#support-guide','<span><strong>사용 관련 문의</strong><small>제품명과 확인이 필요한 상황을 알려주세요</small></span>','row-link')}{link('/cases/#notices','<span><strong>공지사항</strong><small>썬플렉스의 새로운 안내</small></span>','row-link')}</div></section>{cta()}'''
    render('index.html','산업현장을 위한 스마트 안전 솔루션','영상관제, 위험 알림, 작업 환경 측정 등 산업현장에 필요한 스마트 안전장비. 썬플렉스의 제품 정보와 도입 상담을 확인하세요.',body)

def company():
    body=head('기업소개','현장 안전관리에 필요한<br>기술을 제안합니다.','건설·제조·물류 현장의 안전장비와 솔루션. 썬플렉스는 현장 담당자가 필요한 제품을 검토할 수 있도록 제품 정보와 상담을 제공합니다.','<div class="big-name" aria-hidden="true">SUNPLEX</div>','company-head')
    body+=f'<div class="company-photo">{picture("field-tbm-briefing-generated","작업 전 현장 도면을 함께 확인하는 장면",True,"100vw")}</div>'
    body+=f'''<section class="section wrap company-intro"><div><span class="eyebrow">썬플렉스</span><h2>현장에 필요한 장비를<br>선택하실 수 있도록.</h2></div><div><p class="statement">영상관제와 위험 알림,<br>작업 환경 측정과 출입 관리.<br>현장에 필요한 기능을 살펴보세요.</p><p>썬플렉스는 산업현장의 안전관리에 필요한 제품을 안내합니다. 설치할 장소와 사용 목적에 맞춰 제품별 기능을 확인하고, 도입에 필요한 사항을 문의하실 수 있습니다.</p>{link('/solutions/','적용 분야 살펴보기')}</div></section>
<section class="section feature"><div class="wrap"><div class="lead"><h2>제품 도입 시<br>함께 확인할 사항</h2><p>기능이 같아 보여도 설치 조건과 사용 방식은 다를 수 있습니다. 현장 적용 여부는 아래 사항을 바탕으로 확인합니다.</p></div><div class="principles"><article class="principle"><h3>사용 목적</h3><p>관리할 구역과 필요한 기능을 정리해 주세요. 차량 접근 알림, 작업 구역 영상 확인, 가스 농도 측정 등 사용 목적이 제품 선택의 기준이 됩니다.</p></article><article class="principle"><h3>설치 환경</h3><p>실내·실외 여부, 설치 위치, 전원 공급과 통신 환경을 확인합니다. 기존 장비와 연결해야 한다면 모델명과 연결 방식도 필요합니다.</p></article><article class="principle"><h3>운영 방식</h3><p>알림 수신자와 운영 담당자를 정하고, 확인할 정보와 기록 범위를 검토합니다. 제품에 따라 연동 기능과 데이터 처리 조건은 별도 확인이 필요합니다.</p></article></div></div></section>
<section class="section wrap"><div class="lead"><h2>제품 정보와 상담 안내</h2><p>제품별 기능과 적용 조건은 상세 안내에서 확인할 수 있습니다. 추가로 필요한 자료는 제품명과 함께 문의해 주세요.</p></div><div class="resource-list">{link('/products/','<strong>제품별 상세 안내</strong>','row-link')}{link('/cases/','<strong>자료와 사용 관련 문의</strong>','row-link')}</div></section>
<section class="section wrap" id="company-info"><div class="lead"><h2>기업정보</h2><p>썬플렉스의 연락처와 사업장 안내입니다.</p></div><dl class="info-table"><div><dt>법인명</dt><dd>(주)썬플렉스</dd></div><div><dt>사업장</dt><dd>경기도 시흥시 신천동 845-18</dd></div><div><dt>전화</dt><dd><a href="tel:0319912285">031-991-2285</a></dd></div><div><dt>이메일</dt><dd><a href="mailto:jiyoueng@daum.net">jiyoueng@daum.net</a></dd></div></dl></section>{cta()}'''
    render('company/index.html','기업소개','썬플렉스가 소개하는 산업안전 제품과 적용 분야, 도입 전 확인할 조건 및 기업정보를 알아보세요.',body,'/company/')

def solutions():
    body=head('적용 분야','산업별 적용 분야','건설·제조·물류 등 작업 환경별로 검토할 수 있는 제품을 안내합니다. 실제 적용 범위는 설치 환경과 제품 사양에 따라 확인이 필요합니다.','<nav class="anchor-nav" aria-label="적용 분야 바로가기"><a href="#construction">건설·토목</a><a href="#logistics">제조·물류</a><a href="#enclosed">밀폐·지하 공간</a></nav>')
    sectors=[('construction','건설·토목','인양 작업과 이동 구역의<br>영상 확인','크레인 인양 구역과 시야 확보가 어려운 작업 구간에 사용할 수 있는 영상장비를 확인하세요. 설치 위치와 필요한 촬영 범위에 따라 제품을 검토할 수 있습니다.','field-crane-hook-rigging-generated',[('hook-bottom-camera','이동형 크레인 후크 하방 카메라'),('mobile-cctv','이동식 CCTV'),('site-cms','현장 CMS 구축')]),('logistics','제조·물류','차량 접근 알림과<br>작업 구역 안내','차량과 작업자가 함께 이동하는 구역에서 접근 경보와 시각 안내가 필요한 위치를 살펴보세요. 이동 경로와 현장 소음도 제품 선택 시 확인할 사항입니다.','field-vehicle-pedestrian-generated',[('equipment-approach-alarm','건설장비 접근경보 시스템'),('pedestrian-collision-prevention','공사현장 주변 보행자 충돌방지 시스템'),('led-logo-light','안전 사각지대 LED 로고라이트')]),('enclosed','밀폐·지하 공간','가스 농도 측정과<br>작업 환경 확인','터널·탱크 등 작업 공간의 가스 농도 측정과 통신 환경을 검토할 수 있습니다. 측정 대상, 작업 위치, 알림 전달 방식에 맞는 제품을 확인하세요.','home-role-field-tunnel',[('compact-gas-detector','소형 복합가스 측정기'),('gas-alarm','유해가스 및 폭발성 가스 경보 시스템'),('wireless-network','통신 음영지역 무선 네트워크망 구성')])]
    body+='<div class="wrap">'
    for ident,label,title,desc,img,items in sectors:
        body+=f'<section class="sector" id="{ident}"><div class="sector-image">{picture(img,label+"의 작업 환경을 설명하는 장면")}<p class="caption">적용 검토 예시</p></div><div><div class="sector-label">{label}</div><h2>{title}</h2><p>{desc}</p>{product_links(items)}<div class="actions">{link("/contact/","현장 조건 문의")}</div></div></section>'
    body+='</div><section class="section wrap"><div class="lead"><h2>설치·연동 검토 사항</h2><p>제품의 연결 방식과 설치·운영 범위는 개별 검토가 필요합니다. 아래 정보를 준비하면 문의할 내용을 정리하기 쉽습니다.</p></div><ul class="checks"><li>설치 구역<small>실내·실외, 이동 범위, 설치 위치</small></li><li>전원과 통신<small>전원 공급, 유선·무선 통신 환경</small></li><li>기존 장비<small>사용 중인 모델과 연결 방식</small></li><li>확인할 정보<small>영상·알림·측정값·기록</small></li></ul></section>'+cta()
    render('solutions/index.html','적용 분야','건설·토목, 제조·물류, 밀폐·지하 공간의 조건에 따라 산업안전 제품과 도입 전 확인 사항을 살펴보세요.',body,'/solutions/')

def support():
    body=head('고객지원','제품 문의와<br>기술자료 안내','제품 정보, 추가 자료, 사용 중 문의사항을 안내합니다. 문의 목적에 맞는 항목을 선택해 주세요.')
    body+=f'''<div class="wrap"><div class="support-choices"><a class="support-choice" href="/products/"><h2>제품 정보 찾기</h2><p>제품별 기능과 상세 안내</p>{ARROW}</a><a class="support-choice" href="#support-guide"><h2>사용 중인 제품 문의</h2><p>상황을 설명할 때 필요한 정보</p>{ARROW}</a><a class="support-choice" href="/contact/"><h2>도입 상담</h2><p>새로운 현장과 제품 검토</p>{ARROW}</a></div></div>
<section class="section wrap support-layout" id="support-guide"><div><h2>자주 묻는 질문</h2><p class="label-p">알고 계신 내용만 적어주셔도 됩니다.<br>사진이 있다면 이메일에 함께 첨부해 주세요.</p></div><div class="faq"><details open><summary>제품 사용 문의는 어떻게 하나요?</summary><p>제품명 또는 모델명, 확인이 필요한 증상, 발생한 시점을 정리해 주세요. 설치 장소와 전원·통신 상태도 함께 알려주시면 상황을 설명하는 데 도움이 됩니다.</p></details><details><summary>추가 제품 자료는 어디에 요청하나요?</summary><p>먼저 제품 상세 안내를 확인해 주세요. 추가로 필요한 자료가 있다면 제품명과 문서 종류를 이메일로 알려주세요. <a class="text-link" href="/products/">제품 목록 열기 {ARROW}</a></p></details><details><summary>제품을 정하지 않아도 상담할 수 있나요?</summary><p>현장에서 확인하려는 상황과 설치할 구역을 알려주세요. 관심 있는 기능이나 기존에 사용 중인 장비가 있다면 함께 적어주세요.</p></details><details><summary>설치·연동 상담에는 어떤 정보가 필요한가요?</summary><p>관심 제품, 설치 위치, 전원 공급과 통신 환경을 정리해 주세요. 기존 장비와의 연결 여부는 모델과 연결 방식에 따라 별도 확인이 필요합니다.</p></details></div></section>
<section class="section feature"><div class="wrap support-layout"><div><h2>제품명과 함께<br>문의해 주세요.</h2><p class="label-p">제품 자료와 사용 관련 문의를<br>전화 또는 이메일로 전달할 수 있습니다.</p></div><div class="contact-methods"><a href="tel:0319912285"><small>전화</small><strong>031-991-2285</strong></a><a href="mailto:jiyoueng@daum.net?subject=%EC%8D%AC%ED%94%8C%EB%A0%89%EC%8A%A4%20%EC%A0%9C%ED%92%88%20%EB%AC%B8%EC%9D%98"><small>이메일</small><strong>jiyoueng@daum.net</strong></a></div></div></section>
<section class="section wrap support-layout" id="notices"><h2>공지사항</h2><div class="notice"><h3>등록된 공지가 없습니다.</h3><p>제품 정보는 제품별 상세 안내에서 확인해 주세요.</p><div class="actions">{link('/products/','제품 정보 확인')}</div></div></section>'''
    render('cases/index.html','고객지원','제품 정보와 자료, 사용 중인 제품 문의, 도입 상담 및 공지사항을 안내합니다.',body,'/cases/')

def contact():
    body=head('도입 문의','제품 도입 상담','제품 선정과 설치·연동 조건을 문의하실 수 있습니다. 관심 제품과 현장 정보를 작성해 이메일로 보내주세요.')
    fields=[('field','현장 유형','예: 건설현장, 제조공장, 물류센터'),('area','설치·관리할 구역','예: 차량 출입구, 지하 작업 공간'),('need','관심 제품·필요한 기능','제품명 또는 확인하고 싶은 상황'),('connection','전원·통신 조건','알고 계신 내용만 적어주세요'),('reply','회신 연락처','이메일 또는 전화번호')]
    form=''.join(f'<div class="form-field"><label for="{key}">{label}</label>'+(f'<textarea id="{key}" name="{key}" maxlength="1000" placeholder="{ph}"></textarea>' if key=='need' else f'<input id="{key}" name="{key}" maxlength="200" placeholder="{ph}"'+(' autocomplete="off"' if key=='reply' else '')+'>')+'</div>' for key,label,ph in fields)
    body+=f'''<section class="section wrap contact-grid" id="prepare"><div class="contact-info"><h2>관심 제품과<br>현장 정보를 알려주세요.</h2><p>제품을 정하지 않으셨다면 필요한 기능이나 현장에서 겪는 어려움을 적어주세요. 설치 위치, 전원·통신 환경 등 아직 확인하지 못한 항목은 비워두셔도 됩니다.</p><div class="contact-methods"><a href="tel:0319912285"><small>전화로 문의</small><strong>031-991-2285</strong></a><a href="mailto:jiyoueng@daum.net"><small>이메일로 문의</small><strong>jiyoueng@daum.net</strong></a></div><p>사진이나 도면은 이메일 앱에서 첨부해 주세요. 개인정보가 포함된 자료는 필요한 부분만 보내주세요.</p></div><div class="inquiry"><h2>문의 내용 정리</h2><p class="hint">입력 내용은 이 페이지에 저장하거나 서버로 전송하지 않습니다. 이메일 앱에서 직접 확인하고 보내주세요.</p><form id="inquiry-form">{form}<div class="form-actions" hidden><button class="btn" type="submit">이메일 앱에서 작성 {ARROW}</button><button class="btn outline" type="button" id="copy-inquiry">문의 내용 복사</button></div><noscript><p class="form-note">이메일 작성 도우미는 JavaScript가 필요합니다. <a href="mailto:jiyoueng@daum.net">jiyoueng@daum.net</a>으로 직접 문의해 주세요.</p></noscript><p id="inquiry-status" class="status" role="status" aria-live="polite"></p><div class="form-field" id="draft-fallback" hidden><label for="draft-text">복사할 문의 내용</label><textarea id="draft-text" readonly></textarea></div></form><p class="form-note">메일 전송 전 내용을 확인해 주세요.<br><a class="text-link" href="/privacy/">개인정보 안내 {ARROW}</a></p></div></section>
<section class="section wrap support-layout" id="location"><h2>사업장 안내</h2><div><h3>경기도 시흥시 신천동 845-18</h3><p class="muted" style="margin-top:20px">방문을 계획하고 계신다면 전화로 먼저 연락해 주세요.</p><div class="actions">{link('https://map.naver.com/p/search/%EA%B2%BD%EA%B8%B0%EB%8F%84%20%EC%8B%9C%ED%9D%A5%EC%8B%9C%20%EC%8B%A0%EC%B2%9C%EB%8F%99%20845-18','지도에서 위치 보기')}</div></div></section>'''
    render('contact/index.html','도입 문의','현장 유형과 관심 제품, 설치·통신 조건을 정리하고 썬플렉스에 전화 또는 이메일로 문의하세요.',body,'/contact/')

def privacy():
    body=head('개인정보·현장 데이터 안내','개인정보 및<br>현장 데이터 안내','웹사이트 이용과 전화·이메일 문의, 제품 도입 시 확인할 내용을 구분해 안내합니다.')
    body+='''<div class="section wrap legal"><section><h2>웹사이트와 문의 작성 도우미</h2><p>이 웹사이트의 문의 작성 도우미는 입력 내용을 브라우저에서 이메일 초안으로 정리합니다. 작성한 내용은 이 사이트 서버로 전송하거나 저장하지 않습니다. 이메일 앱에서 직접 전송해야 썬플렉스에 전달됩니다.</p><p>새로 구성된 기업 안내 페이지에는 방문 분석용 스크립트나 광고 추적 도구를 사용하지 않습니다. 웹사이트 제공에 필요한 접속 정보의 처리는 호스팅 서비스의 정책을 따릅니다. 외부 지도나 이메일 서비스를 이용할 때는 해당 서비스의 정책도 확인해 주세요.</p></section><section><h2>전화·이메일 문의</h2><p>상담 과정에서 알려주신 회사명, 담당자, 현장 주소, 연락처와 문의 내용은 요청 확인 및 회신에 사용합니다. 문의 응대 목적 외에는 이용하지 않습니다.</p><p>상담 목적을 이룬 뒤에는 지체 없이 파기합니다. 관계 법령에 보존 의무가 있는 경우에는 해당 법령이 정한 기간 동안 보관합니다. 전자 파일은 복구할 수 없는 방법으로 삭제하고, 출력물은 분쇄하거나 소각합니다.</p><p>개인정보 관련 문의는 <a href="tel:0319912285">031-991-2285</a> 또는 <a href="mailto:jiyoueng@daum.net">jiyoueng@daum.net</a>으로 연락해 주세요.</p></section><section><h2>현장 데이터를 다루는 제품</h2><p>영상, 음성, 얼굴, 출입 및 위치 정보 등이 관련된 제품은 도입 전 데이터 처리 조건을 별도로 확인해야 합니다.</p><p>처리 주체, 저장 항목, 보관 기간, 접근 권한, 외부 전송과 위탁 여부를 계약 단계에서 문서로 정합니다. 제품 소개나 이 안내만으로 현장별 데이터 처리 조건이 확정되지는 않습니다.</p></section></div>'''
    render('privacy/index.html','개인정보·현장 데이터 안내','웹사이트의 문의 작성 도우미와 전화·이메일 문의, 현장 데이터 처리 조건에 관한 안내입니다.',body)

def error():
    body=f'<section class="wrap error-page"><div class="error-code">404</div><h1>페이지를<br>찾을 수 없습니다.</h1><p>주소를 다시 확인하거나 아래 메뉴에서 필요한 정보를 찾아주세요.</p><div class="actions">{link("/","홈으로","btn")}{link("/products/","제품 보기")}{link("/cases/","고객지원")}</div></section>'
    render('404.html','페이지를 찾을 수 없습니다','홈, 제품 또는 고객지원에서 필요한 정보를 찾아보세요.',body)

if __name__=='__main__':
    for build in (home,company,solutions,support,contact,privacy,error): build()
    print('Generated 7 corporate pages; product pages and shared assets untouched.')
