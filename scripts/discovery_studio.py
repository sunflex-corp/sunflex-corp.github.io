"""Product discovery and support presentation; existing catalog/search own state."""
from bs4 import BeautifulSoup

def fragment(html):
    return BeautifulSoup(html, 'html.parser')

def symbol(kind):
    """Original vector marks: decorative navigation cues, never product diagrams."""
    paths = {
        'find': '<circle cx="43" cy="43" r="27"/><circle cx="43" cy="43" r="15"/><path d="m63 63 24 24"/>',
        'ask': '<path d="M12 18h62v44H40L22 77V62H12z"/><path d="M44 35h44v43H77v12L62 78H44"/>',
        'connect': '<path d="M20 80 80 20M20 20h60v60"/><path d="M20 47v33h33"/>',
        'detect': '<circle cx="50" cy="50" r="30"/><circle cx="50" cy="50" r="12"/><path d="M50 4v18M50 78v18M4 50h18M78 50h18"/>',
        'alert': '<path d="M24 62 50 18l26 44zM18 80h64M8 94h84"/>',
        'respond': '<path d="M50 8 84 24v29L50 90 16 53V24zM50 28v40M30 48h40"/>',
        'record': '<path d="M20 10h60v80H20zM34 32h32M34 48h32M34 64h20"/>'}
    return fragment(f'<svg class="discovery-symbol" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true" focusable="false">{paths[kind]}</svg>')

def enhance_discovery(soup, path):
    catalog = path == 'products/index.html'
    soup.body['class'].append('discovery-catalog' if catalog else 'discovery-support')
    hero = soup.select_one('.page-head')
    hero['class'] = ['discovery-hero', 'wrap']
    copy = hero.select_one('.wrap')
    copy['class'] = ['discovery-hero-copy']
    if catalog:
        stage = soup.new_tag('div', attrs={'class':'discovery-product-stage', 'aria-label':'제품 미리보기'})
        stage.append(fragment('<div class="discovery-stage-label"><span>PRODUCT SELECTION</span><span>현장에 맞는 선택</span></div>'))
        for slug, label in [('mobile-cctv','이동식 CCTV'),('digital-radio','디지털 무전기'),('compact-gas-detector','소형 복합가스 측정기')]:
            source = soup.select_one(f'.solar-card a[href="/products/{slug}/"] img')
            image = fragment(str(source)).img
            image['loading'] = 'eager'
            image['sizes'] = '(max-width:760px) 40vw, 300px'
            link = soup.new_tag('a', href=f'/products/{slug}/', attrs={'class':'discovery-stage-product'})
            image['alt'] = ''
            link.append(image)
            span = soup.new_tag('span'); span.string=label+' ↗'; link.append(span)
            stage.append(link)
        hero.append(stage)
        stage['class'].append('discovery-exhibit')
        for i,link in enumerate(stage.select('.discovery-stage-product')):
            index=soup.new_tag('small',attrs={'class':'discovery-exhibit-index','aria-hidden':'true'})
            index.string=f'0{i+1}';link.insert(0,index)
        note=soup.new_tag('div',attrs={'class':'discovery-range'})
        note.append(fragment('<strong>48</strong><span>제품을<br>기능과 현장 조건으로</span><a href="#catalog">제품 찾기 <span aria-hidden="true">↓</span></a>'))
        copy.append(note)
        labels={'':'전체 제품','detect':'감지','alert':'경보','respond':'대응','record':'기록'}
        for b in soup.select('.catalog-tabs button'):
            category=b.get('data-category',''); count=b.small.extract(); b.clear()
            b.append(fragment(f'<span class="discovery-filter-name">{labels[category]}</span><span class="discovery-filter-en">'+('ALL PRODUCTS' if not category else 'Solar '+category.title())+'</span>'))
            b.append(count)
            if category:b.insert(0,symbol(category))
        for card in soup.select('[data-catalog-card]'):
            # Search the visible, current copy in addition to legacy catalog keywords.
            card['data-search'] += ' ' + card.get_text(' ',strip=True)
        results=soup.new_tag('h2',attrs={'class':'discovery-results-title'}); results.string='제품 둘러보기'
        soup.select_one('.catalog-count').insert(0,results)
    else:
        choices=soup.select_one('.support-choices')
        oldwrap=choices.parent
        choices.extract();oldwrap.decompose()
        choices['class']=['discovery-support-routes']
        choices.insert(0,fragment('<div class="discovery-section-label">문의 목적을 선택하세요</div>'))
        for i,a in enumerate(choices.select('a')):
            a['class']=['discovery-support-route']
            number=soup.new_tag('span',attrs={'class':'discovery-route-number','aria-hidden':'true'});number.string=f'{i+1:02}'
            a.insert(0,number)
            a.append(symbol(['find','ask','connect'][i]))
        hero.append(choices)
        # A visible contact shortcut keeps the artistic opening useful.
        quick=soup.new_tag('div',attrs={'class':'discovery-quick-contact'})
        quick.append(fragment('<span>바로 문의하기</span>'))
        for original in soup.select('#chapter-2 .contact-methods a'):
            link=fragment(str(original)).a
            link['class']=['discovery-quick-link']
            quick.append(link)
        copy.append(quick)
        soup.select_one('.chapter-links')['class']=['discovery-support-index','wrap']
        faq=soup.select_one('.faq')
        empty=fragment('<div class="discovery-faq-empty" hidden><h3>찾으시는 안내가 없나요?</h3><p>검색어를 바꾸거나 제품명과 함께 문의해 주세요.</p><button type="button" data-support-reset>전체 질문 보기 ↺</button><a href="#chapter-2">전화·이메일 확인 ↗</a></div>')
        faq.append(empty)
        contact=soup.select_one('#chapter-2');contact['class']=['discovery-contact']
        for a in contact.select('.contact-methods a'):
            arrow=soup.new_tag('span',attrs={'class':'discovery-contact-arrow','aria-hidden':'true'});arrow.string='↗';a.append(arrow)
        contact.select_one('.wrap').append(fragment('<div class="discovery-contact-prep"><span>문의 전에 확인하면 좋은 정보</span><ul><li>제품명 · 모델명</li><li>증상 · 발생 시점</li><li>설치 장소 · 전원 · 통신</li></ul></div>'))

        helpdesk=soup.new_tag('div',attrs={'class':'discovery-helpdesk wrap'})
        faq_section=soup.select_one('#support-guide')
        faq_section.insert_before(helpdesk)
        helpdesk.append(contact.extract());helpdesk.append(faq_section.extract())
        search=soup.select_one('#support-search')
        search['aria-describedby']='discovery-search-scope'
        scope=soup.new_tag('span',attrs={'id':'discovery-search-scope','class':'discovery-search-scope'})
        scope.string='이 페이지의 질문과 답변을 검색합니다.'
        search.insert_after(scope)
