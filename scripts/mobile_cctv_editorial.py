"""CCTV-specific progressive disclosure; original facts and anchors are retained."""
from bs4 import BeautifulSoup

def enhance(soup, rest):
    def fragment(html): return BeautifulSoup(html, 'html.parser')
    lineup=soup.find(id='mobile-cctv-lineup')
    engineering=soup.find(id='movingcam-engineering')
    # Read physical details beside the model that they describe.
    for panel, detail in zip(lineup.select('.model-panel'), engineering.select('dl > div')):
        disclosure=soup.new_tag('details',attrs={'class':'cctv-physical'})
        summary=soup.new_tag('summary');summary.string='지지 구조 자세히 보기';disclosure.append(summary)
        listing=soup.new_tag('dl');listing.append(detail.extract());disclosure.append(listing);panel.append(disclosure)
    for ident,label in [('movingcam-engineering','설치 전에 확인할 조건'),('detail-8','현장 맞춤 구성과 제품 사진'),('movingcam-coverage','이설 후 확인할 항목')]:
        section=soup.find(id=ident);inner=section.select_one('.editorial-section-inner')
        disclosure=soup.new_tag('details',attrs={'class':'cctv-disclosure'})
        summary=soup.new_tag('summary');summary.string=label;disclosure.append(summary)
        for child in list(inner.contents):disclosure.append(child.extract())
        inner.append(disclosure);section['class'].append('cctv-compact')
    # Position supporting detail directly after the model selector.
    rest.remove(engineering);rest.insert(rest.index(lineup)+1,engineering)
    flow=soup.find(id='moving-control-pin')
    diagram=flow.select_one('[aria-label="어제 작업면에서 오늘 작업면으로 CCTV 이동"]')
    diagram['class']=['cctv-process'];diagram['data-cctv-process']=''
    children=diagram.find_all(recursive=False)
    controls=fragment('<div class="cctv-step-controls" role="tablist" aria-label="촬영 위치 변경 과정" hidden>'+''.join(f'<button type="button" role="tab" id="cctv-step-{i}" aria-controls="cctv-stage-{i}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">0{i+1} <span>{label}</span></button>' for i,label in enumerate(['작업면 확인','위치 이동','영상 확인']))+'</div>')
    diagram.insert(0,controls)
    assets=['/media/derived/product-mobile-cctv-problem-1280.webp','/media/editorial/cctv-relocation-1536.webp','/media/editorial/cctv-monitor-1536.webp']
    titles=['오늘 살펴볼 곳부터.','필요한 자리로, 다시.','바뀐 시야를 화면에서.']
    descriptions=['공정이 달라지면 작업 동선과 장비 주변을 살펴, 촬영할 구간을 정합니다.','담당자가 무빙캠을 옮겨 세우고, 설치 위치에 맞춰 전원과 통신을 연결합니다.','관제 화면에서 필요한 작업 구간이 보이는지, 영상이 연결되는지 확인합니다.']
    alts=['건설 현장에서 작업 구간을 살피는 관리자','같은 건설 현장에서 노란 삼각대형 무빙캠을 새 위치에 세우는 담당자','같은 건설 현장의 작업 동선을 크게 보여주는 관제 모니터']
    for child in children:child.extract()
    for i in range(3):
        panel=soup.new_tag('article',attrs={'class':'cctv-stage','id':f'cctv-stage-{i}','data-cctv-stage':''})
        small=assets[i].replace('-1536.webp','-768.webp').replace('-1280.webp','-768.webp')
        large_width=1280 if i==0 else 1536
        panel.append(fragment(f'<img src="{assets[i]}" srcset="{small} 768w, {assets[i]} {large_width}w" sizes="(max-width:760px) 92vw, min(88vw, 1400px)" alt="{alts[i]}" width="1536" height="864" loading="lazy" decoding="async"><div class="cctv-stage-caption"><h3>{titles[i]}</h3><p>{descriptions[i]}</p></div>'))
        diagram.append(panel)
    detail=soup.new_tag('details',attrs={'class':'cctv-process-detail'})
    summary=soup.new_tag('summary');summary.string='설치 흐름 자세히 보기';detail.append(summary)
    for child in children:detail.append(child)
    diagram.append(detail)
    diagram.append(fragment('<p class="cctv-process-note">현장 이해를 돕는 연출 이미지입니다. 실제 설치 구성은 현장 조건에 따라 달라집니다.</p>'))
    # Close the story with configuration, not a second oversized lineup presentation.
    choice=soup.find(id='detail-8');rest.remove(choice);rest.append(choice)
