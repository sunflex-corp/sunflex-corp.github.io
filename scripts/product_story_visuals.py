"""Product-specific explanatory scenes, deliberately separate from real application UI."""
import json
from pathlib import Path
from html import escape as e
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
SCENES=json.loads((ROOT/'data/product-story-scenes.json').read_text())

def scene(slug,index,asset):
    spec=SCENES[slug]; kind=spec['kind']; labels=spec['nodes']; active='#80c7ff'; muted='#75869d'
    # Reuse authored matching scenes where they explain more than a schematic.
    if slug in ['mobile-cctv','site-cms']:
        if slug=='mobile-cctv':
            src=['/media/derived/product-mobile-cctv-problem-1280.webp','/media/editorial/cctv-relocation-1536.webp','/media/editorial/cctv-monitor-1536.webp'][index]
            caption=['촬영할 작업 구역 확인','새 위치에 카메라 설치','이설 후 관제 화면 확인'][index]
        else:
            src=asset['src'];caption=['굴착 구간의 카메라 배치','골조 작업에 맞춰 시야 재검토','마감·부대 작업 구역 확인'][index]
        return f'<figure class="benefit-visual story-photo-scene"><img src="{e(src)}" alt="{e(caption)} — 현장 연출 이미지" width="1280" height="900" loading="lazy" decoding="async"><figcaption><strong>{e(caption)}</strong><span>현장 이해를 돕는 연출 이미지 · 실제 배치는 현장에 맞춰 검토합니다.</span></figcaption></figure>'
    if slug=='smart-airbag' and index==1:
        return '<figure class="benefit-visual story-proof-scene"><img src="/media/derived/manual-smart-airbag-figure-1280.webp" alt="에어백 미전개·전개 후의 앞면과 뒷면 제품 자료" width="1280" height="481" loading="lazy" decoding="async"><figcaption>제품 자료 · 미전개 상태와 전개 후 보호부 비교</figcaption></figure>'

    def t(x,y,text,size=20,color='#e8f0fc',anchor='start'):
        return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" text-anchor="{anchor}">{e(text)}</text>'
    def box(x,y,w,h,r=14,fill='#213349',stroke='#405770'):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    def line(x1,y1,x2,y2,color=active,dash=''):
        return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="3" fill="none"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
    def person(x,y,color='#dce8f7'):
        return f'<g transform="translate({x} {y})" stroke="{color}" stroke-width="9" stroke-linecap="round"><circle cy="-24" r="12" fill="{color}" stroke="none"/><path d="M0 -4V48M-25 20L0 0L25 20M0 48L-19 79M0 48L19 79" fill="none"/></g>'
    diagram=''
    if kind=='opening':
        opened=index>0
        diagram=box(100,132,390,205,8,'#283748')+box(135,168,318,130,3,'#060d17')
        diagram+=f'<path d="M135 168L453 168L{425 if opened else 453} {64 if opened else 298}L{160 if opened else 135} {64 if opened else 298}Z" fill="#576d80" stroke="#adbdcc" stroke-width="3"/>'
        diagram+=box(450,168,24,34,4,active)+t(295,377,'열림 감지' if opened else '닫힌 덮개',28,active,'middle')
        if index==2:diagram+=box(355,47,205,59,12,'#263d50')+t(457,85,'방송 · 담당자 알림',18,active,'middle')+line(469,165,469,108,active,'6 6')
    elif kind=='site':
        diagram=box(36,64,528,323,18,'#142335')+line(58,236,539,236,'#42526b')+line(325,82,325,367,'#42526b')
        diagram+=box(62,91,176,86,4,'#35465b')+t(151,140,'작업 구역',21,'#e4ebf5','middle')
        diagram+=box(372,90,160,79,4,'#35465b')+t(450,137,'현장 동선',21,'#e4ebf5','middle')
        x=[130,294,462][index]
        diagram+=f'<path d="M{x} 304L{x-60} 208L{x+62} 208Z" fill="#80c7ff" opacity=".18"/><circle cx="{x}" cy="304" r="17" fill="{active}"/>'+person(440,263)
        if slug=='site-cms':diagram+=t(100,350,['굴착 구간','골조 작업','마감 구간'][index],22,active)
        elif slug=='mobile-cctv':diagram+=t(60,350,['촬영할 구역 확인','카메라 위치 조정','새 작업면 확인'][index],22,active)
        else:diagram+=t(60,350,labels[index],22,active)
        if slug in ['vehicle-entry-alert','ai-equipment-collision','equipment-approach-alarm']:
            diagram+=box(85,265,142,63,8,'#b8a26d')+box(187,245,50,74,8,'#d6bf88')
            diagram+='<circle cx="115" cy="335" r="17" fill="#0b1420"/><circle cx="211" cy="335" r="17" fill="#0b1420"/>'
            diagram+=line(243,307,419,307,active,'8 8')
            if index>0:diagram+=f'<rect x="408" y="221" width="66" height="132" rx="10" fill="none" stroke="{active}" stroke-width="3"/>'
        else:diagram+=line(150,304,425,304,active,'8 8')
    elif kind in ['network','broadcast']:
        for j,(x,y) in enumerate([(56,112),(224,214),(403,112)]):
            col=active if j==index else muted
            diagram+=box(x,y,140,98,15,'#1e3045',col)+t(x+70,y+58,labels[j],17,col,'middle')
            diagram+=f'<path d="M{x+50} {y-14}Q{x+70} {y-38} {x+90} {y-14}M{x+40} {y-25}Q{x+70} {y-61} {x+100} {y-25}" stroke="{col}" fill="none" stroke-width="3"/>'
        diagram+=line(193,176,223,235,active,'7 7')+line(365,235,402,176,active,'7 7')
        diagram+=t(300,367,labels[index],28,active,'middle')
    elif kind in ['wear','hook']:
        source=BeautifulSoup((ROOT/f'data/solar-products/{slug}.html').read_text(),'html.parser')
        product=source.find('img');src=product['src'] if product else asset['src']
        if index==0:
            diagram=box(105,24,390,312,20,'#fff','#fff')+f'<image href="{e(src)}" x="125" y="40" width="350" height="276" preserveAspectRatio="xMidYMid meet"/>'
            diagram+=t(300,389,labels[index],27,active,'middle')
        elif kind=='hook':
            diagram='<path d="M232 123C138 111 130 307 235 320C335 334 335 227 294 196L294 149" fill="none" stroke="#b8cce1" stroke-width="20" stroke-linecap="round"/>'
            diagram+=line(294,151,237,122,active if index==1 else '#edbf7c','')
            diagram+=t(300,379,'체결 상태 확인' if index==1 else '미체결 알림 전달',27,active,'middle')
            if index==2:diagram+=box(377,145,137,128,16)+t(446,202,'담당자',22,active,'middle')+t(446,238,'알림',22,active,'middle')+line(313,237,374,211,active,'6 7')
        elif slug in ['smart-helmet','emergency-signal-location']:
            diagram='<path d="M135 202Q143 85 275 85Q406 85 414 202Z" fill="#d2c092"/><path d="M108 206H443" stroke="#d2c092" stroke-width="19" stroke-linecap="round"/><path d="M156 216Q185 350 275 329Q365 346 397 216" fill="none" stroke="#adc5df" stroke-width="9"/>'
            diagram+=box(357,176,43,35,7,active)+t(300,392,labels[index],27,active,'middle')
            if index==2:diagram+=box(405,265,151,72,12)+t(480,310,'담당자 확인',19,active,'middle')
        elif slug=='power-assist-suit':
            diagram+=person(274,166)+f'<path d="M254 162L246 246L266 271M292 162L307 244L282 271" fill="none" stroke="{active}" stroke-width="9"/>'
            diagram+=t(300,335,'착용 · 탄성 구조',27,active,'middle')+t(300,383,labels[index],22,'#c3d6e9','middle')
        else:
            # Explain a state or operation, rather than reuse an unrelated person photograph.
            for j,label in enumerate(labels):
                y=59+j*105;col=active if j==index else muted
                diagram+=box(75,y,450,79,15,'#20354c',col)+t(108,y+48,label,25,col)
            diagram+=t(300,416,'사용 · 확인 흐름',19,'#b7c8db','middle')
    elif kind=='chart':
        if slug=='co2-temp-humidity' and index==0:
            for j,label in enumerate(labels):diagram+=box(48+j*175,130,154,150)+t(125+j*175,216,label,22,active,'middle')
        else:
            diagram+=line(75,320,538,320,'#64778e')+line(75,76,75,320,'#64778e')
            diagram+=line(78,168,538,168,'#a5b5c7','6 8')+t(535,152,'설정 기준',17,'#bacadd','end')
            diagram+='<path d="M80 270L140 240L196 258L245 197L294 211L347 132L393 156L439 203L493 174L535 187" fill="none" stroke="#80c7ff" stroke-width="5" stroke-linejoin="round"/>'
            diagram+=f'<circle cx="{[196,347,493][index]}" cy="{[258,132,174][index]}" r="10" fill="#a9e3d1"/>'
            diagram+=t(75,357,'시간',18,'#bacadd')+t(300,406,labels[index],26,active,'middle')
    elif kind=='crane':
        diagram+=line(98,331,98,73,'#d5c192')+line(58,75,514,75,'#d5c192')+line(145,75,440,34,'#d5c192')+line(360,77,360,209,'#d5c192')
        diagram+='<path d="M360 209V237Q387 257 399 232" fill="none" stroke="#d5c192" stroke-width="7"/>'+person(466,270)
        diagram+=box(140,282,170,59,5,'#344e69')+t(225,321,'인양 구역',20,'#e4edf9','middle')
        diagram+=f'<path d="M371 245L296 348L441 348Z" fill="{active}" opacity=".16"/>'+t(300,400,labels[index],25,active,'middle')
        if index==2:diagram+=box(28,180,150,85,10)+t(103,216,'경고 방송' if slug=='tower-crane-hook-collision' else '확인 화면',18,active,'middle')+line(178,223,350,223,active,'8 8')
    elif kind=='entry':
        diagram+=person(149,155)+box(265,94,86,125,14)+box(281,111,53,60,6,'#80c7ff')
        diagram+=box(378,162,34,161,8,'#4e6279')+box(491,162,34,161,8,'#4e6279')
        diagram+=line(398,180,505 if index<1 else 410,264,'#a9cce3')
        diagram+=line(176,232,250,232,active,'6 5')+t(300,384,labels[index],26,active,'middle')
    elif kind=='projection':
        diagram+=box(75,52,105,61,14,'#d4dce7')
        diagram+='<path d="M125 112L227 309L502 309Z" fill="#80c7ff" opacity=".13"/><path d="M200 291L487 291L547 377L157 377Z" fill="#22364c" stroke="#597590" stroke-width="2"/>'
        diagram+=t(351,344,['안전 통로','접근 주의','안내 위치'][index],32,'#fff','middle')+t(300,423,'표시 구성 예시',17,'#b7c8db','middle')
    elif kind=='mist':
        diagram+=line(70,84,530,84,'#bed1e8')
        for x in [112,238,364,490]:
            diagram+=box(x-9,80,18,25,4,active)
            diagram+=f'<path d="M{x} 106L{x-43} 255L{x+43} 255Z" fill="#80c7ff" opacity="{.10 if index==0 else .24}"/>'
            if index>0:
                for a,bv in [(-20,180),(10,210),(-9,243)]:diagram+=f'<circle cx="{x+a}" cy="{bv}" r="4" fill="#abd9ff"/>'
        diagram+=line(45,292,558,292,'#66798d')+t(300,362,labels[index],27,active,'middle')
    elif kind=='dashboard':
        diagram+=box(39,46,522,332,18,'#17283c')+t(69,86,'확인할 정보',20,'#b7c8db')
        for j,label in enumerate(labels):
            y=109+j*77;col=active if index==j else '#62768f'
            diagram+=box(65,y,470,63,10,'#233b54',col)+t(89,y+40,label,23,col)
            diagram+=f'<circle cx="502" cy="{y+31}" r="7" fill="{col}"/>'
        diagram+=t(300,416,'정보 구성 예시',17,'#b7c8db','middle')
    elif kind=='timeline':
        diagram+=box(56,44,488,210,12,'#253d55')+t(300,155,labels[index],30,active,'middle')
        for j in range(7):diagram+=box(56+j*70,284,61,59,3,'#36516d')
        diagram+='<rect x="196" y="278" width="205" height="72" rx="6" fill="#80c7ff" fill-opacity=".18" stroke="#80c7ff" stroke-width="3"/>'
        diagram+=line([204,293,389][index],264,[204,293,389][index],371,'#c7edec')+t(300,407,'원본에서 필요한 구간을 선택',21,'#b7c8db','middle')
    elif kind=='translation':
        diagram+=box(45,75,510,83,16)+t(300,126,'한국어 안전교육',25,active,'middle')
        for j,label in enumerate(['교육자료','언어별 자막','음성 · 텍스트 기록']):
            diagram+=box(45,186+j*69,510,53,12,'#253b52')+t(70,220+j*69,label,22,active if index==j else '#b7c8db')
    else: # document workflow with transparent explanatory cards, not pretend screenshots
        for j,label in enumerate(labels):
            y=43+j*113;col=active if j==index else muted
            diagram+=box(60,y,480,88,15,'#20354c',col)+t(89,y+34,f'0{j+1}',16,col)+t(155,y+52,label,25,col)
            if j<2:diagram+=line(300,y+90,300,y+108,col)
        diagram+=t(300,414,'자료가 결과로 이어지는 과정',19,'#b7c8db','middle')
    svg=f'<svg class="story-scene-svg" viewBox="0 0 600 450" role="img" aria-label="{e(labels[index])} 설명 도식" xmlns="http://www.w3.org/2000/svg"><rect width="600" height="450" rx="20" fill="#112033"/>{diagram}</svg>'
    note='제품 사진 · 사용 흐름 설명 도식' if kind in ['wear','hook'] else '작동 흐름 예시 · 실제 화면·설치 배치와 다를 수 있습니다'
    return f'<figure class="benefit-visual" data-scene="{kind}">{svg}<figcaption>{note}</figcaption></figure>'
