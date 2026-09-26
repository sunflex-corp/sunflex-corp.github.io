"""Company editorial layout, preserving published facts and source anchors."""
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

def enhance_company(soup):
    soup.body['class'].append('company-editorial')
    soup.main['data-company-owned']=''
    hero=soup.select_one('.company-head');hero['class']=['company-hero']
    wrap=hero.select_one('.wrap');wrap['class']=['company-hero-inner']
    mark=wrap.select_one('.big-name');mark.decompose()
    photo=soup.select_one('.company-photo');photo.extract();photo['class']=['company-hero-photo']
    image=photo.select_one('img');image['sizes']='(max-width: 760px) 100vw, 55vw'
    caption=soup.new_tag('p',attrs={'class':'company-image-caption'});caption.string='현장 적용 상황을 설명하는 이미지';hero.append(caption)
    hero.append(photo)
    links=BeautifulSoup('<div class="company-hero-links"><a href="/products/">제품 살펴보기 <span aria-hidden="true">↗</span></a><a href="/contact/">도입 문의 <span aria-hidden="true">↗</span></a></div>','html.parser')
    wrap.append(links)
    intro=soup.select_one('.company-intro');intro['class']=['company-introduction','wrap']
    nav=soup.select_one('.chapter-links');nav['class']=['company-chapters','wrap']
    # Four functional categories, not an asserted process or an integrated system.
    home=BeautifulSoup((ROOT/'data/home-solar-page.html').read_text(),'html.parser')
    section=soup.new_tag('section',attrs={'class':'company-fields wrap','id':'company-fields','aria-labelledby':'company-fields-title'})
    section.append(BeautifulSoup('<header class="company-fields-heading"><span class="eyebrow">SOLAR SOLUTIONS</span><h2 id="company-fields-title">현장의 질문에서.<br>필요한 기능으로.</h2><p>각 제품군의 기능을 살펴보고, 현장 조건에 맞는 제품을 확인하세요.</p></header><nav class="company-field-nav" aria-label="기능별 소개"></nav><div class="company-field-layout"><div class="company-field-stage" aria-hidden="true"></div><div class="company-field-stories"></div></div>','html.parser'))
    names=[('detect','감지'),('alert','경보'),('respond','대응'),('record','기록')]
    questions=['무엇을 확인해야 할까요?','누구에게 알려야 할까요?','어떤 대응 장비가 필요할까요?','어떤 정보를 남겨야 할까요?']
    for i,(slug,label) in enumerate(names):
        panel=home.select_one(f'#map-panel-{i}')
        picture=home.select_one(f'.family-scene-{i} picture')
        stage_image=BeautifulSoup(str(picture),'html.parser').picture
        stage_image['class']=['company-field-image'];stage_image['data-company-image']=str(i)
        stage_image.img['alt']='';stage_image.img['sizes']='(max-width: 1000px) 1px, 55vw'
        section.select_one('.company-field-stage').append(stage_image)
        story=soup.new_tag('article',attrs={'class':'company-field-story','id':f'company-{slug}','data-company-field':str(i)})
        story.append(BeautifulSoup(f'<p class="company-field-category">Solar {slug.title()}</p><h3>{label}</h3><p class="company-field-question">{questions[i]}</p><p>{panel.p.get_text()}</p>','html.parser'))
        mobile=BeautifulSoup(str(picture),'html.parser').picture;mobile['class']=['company-field-mobile'];mobile.img['sizes']='(max-width: 1000px) 90vw, 1px';story.append(mobile)
        link=BeautifulSoup(str(panel.a),'html.parser').a;story.append(link)
        section.select_one('.company-field-stories').append(story)
        a=soup.new_tag('a',href=f'#company-{slug}');a.string=label;section.select_one('.company-field-nav').append(a)
    section.select_one('.company-field-stage').append(BeautifulSoup('<span class="company-field-crosshair" aria-hidden="true"></span><span class="company-field-stage-caption">적용 환경을 설명하는 이미지</span>','html.parser'))
    intro.insert_after(section)
    for p in soup.select('.principle'):p['class']=['company-principle']
    principle=soup.select_one('.principles');principle['class']=['company-principles']
    soup.select_one('#chapter-2')['class']=['company-criteria']
    for section_id in ('chapter-3','company-info'):
        soup.select_one('#'+section_id)['class']=['company-information','wrap']
