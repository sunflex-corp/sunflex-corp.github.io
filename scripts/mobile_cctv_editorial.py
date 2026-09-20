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
    assets=['/media/derived/product-mobile-cctv-problem-1280.webp','/media/editorial/network-field-1536.webp','/media/editorial/control-review-1536.webp']
    descriptions=['공정이 달라지면, 확인할 구간부터 다시 살핍니다.','담당자가 장비를 옮기고 전원과 통신을 연결합니다.','관제 화면에서 촬영 범위와 연결 상태를 확인합니다.']
    alts=['건설 현장에서 작업 구간을 살피는 관리자','현장에서 장비 연결을 확인하는 작업자','관제 화면을 확인하는 담당자']
    for i in range(3):
        panel=soup.new_tag('article',attrs={'class':'cctv-stage','id':f'cctv-stage-{i}','data-cctv-stage':''})
        panel.append(fragment(f'<img src="{assets[i]}" alt="{alts[i]}" width="1536" height="1024" loading="lazy" decoding="async"><div class="cctv-stage-caption"><span>0{i+1} / 촬영 위치 변경</span><h3>{descriptions[i]}</h3></div>'))
        copy=soup.new_tag('div',attrs={'class':'cctv-stage-facts'})
        copy.append(children[[0,1,3][i]].extract())
        if i==2:copy.append(children[2].extract())
        panel.append(copy);diagram.append(panel)
    diagram.append(fragment('<p class="cctv-process-note">설치 과정을 설명하는 현장 연출 이미지입니다. 장비의 이동과 재설치는 담당자가 진행합니다.</p>'))
    # Close the story with configuration, not a second oversized lineup presentation.
    choice=soup.find(id='detail-8');rest.remove(choice);rest.append(choice)
