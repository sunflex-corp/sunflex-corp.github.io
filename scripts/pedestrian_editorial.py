"""A coherent, illustrative entrance scene for the bidirectional warning story."""
from bs4 import BeautifulSoup

def visual(i):
    person_y=[130,220,265][i]
    active=i==2
    signal='#ffc45e' if active else '#596677'
    sensor='#69ded0' if i>=1 else '#768598'
    return f'''<svg class="pedestrian-scene" viewBox="0 0 800 480" role="img" aria-label="{['방음벽 때문에 서로 보이지 않는 차량 출입로와 보행로','방음벽 옆 인체감지 센서가 보행자의 접근을 감지하는 예시','차량 쪽과 보행자 쪽 전광판 및 경광등이 함께 알리는 예시'][i]}" xmlns="http://www.w3.org/2000/svg">
<rect width="800" height="480" rx="24" fill="#151e2a"/>
<path d="M0 365H800M675 0V480" stroke="#303e50" stroke-width="108"/>
<path d="M0 365H800" stroke="#8894a4" stroke-width="2" stroke-dasharray="20 18"/>
<path d="M632 20V296" stroke="#7e8d9e" stroke-width="2" stroke-dasharray="8 10"/>
<rect x="270" y="70" width="330" height="205" rx="8" fill="#3c4c60"/>
<path d="M270 265H600V70" stroke="#8094ac" stroke-width="9" fill="none"/>
<path d="M305 90V250M350 90V250M395 90V250M440 90V250M485 90V250M530 90V250M575 90V250" stroke="#50647d" stroke-width="2"/>
<text x="425" y="160" fill="#d0dbea" text-anchor="middle" font-size="22">방음벽</text>
<text x="425" y="190" fill="#9eafc4" text-anchor="middle" font-size="15">서로의 시야를 가리는 구조물</text>
<g transform="translate(95 320)"><rect width="115" height="70" rx="9" fill="#e5edf5"/><rect x="85" y="8" width="37" height="54" rx="6" fill="#b8cce0"/><rect x="105" y="17" width="10" height="36" rx="2" fill="#24364b"/><path d="M14 -5H35M70 -5H91M14 75H35M70 75H91" stroke="#070c12" stroke-width="9"/></g>
<text x="96" y="430" fill="#d9e4f1" font-size="20">차량 출입로</text>
<text x="654" y="444" fill="#d9e4f1" font-size="20">보행로</text>
<g transform="translate(675 {person_y})" class="scene-person"><circle cy="-14" r="11" fill="#e8f0fa"/><path d="M0 3V30M0 10L-17 23M0 10L17 23M0 30L-12 49M0 30L12 49" stroke="#e8f0fa" stroke-width="8" stroke-linecap="round"/></g>
<g><rect x="585" y="203" width="28" height="34" rx="7" fill="{sensor}"/><circle cx="599" cy="220" r="7" fill="#17232f"/>
<path class="{'scene-sense' if i>=1 else ''}" d="M625 197Q645 220 625 243M640 180Q678 220 640 260" stroke="{sensor}" stroke-width="4" fill="none" opacity="{1 if i>=1 else .2}"/>
<text x="530" y="315" fill="{sensor}" font-size="17">인체감지 센서</text></g>
<g fill="{signal}"><rect x="235" y="319" width="78" height="38" rx="5"/><rect x="699" y="75" width="78" height="38" rx="5"/></g>
<g fill="#122033" font-size="13" text-anchor="middle"><text x="274" y="344">{ '충돌주의' if active else '전광판'}</text><text x="738" y="100">{'충돌주의' if active else '전광판'}</text></g>
<g fill="{signal}"><circle cx="274" cy="301" r="9"/><circle cx="738" cy="57" r="9"/></g>
{('<path class="scene-alert" d="M599 238L599 290L324 290M613 210L750 210L750 123" stroke="#ffc45e" stroke-width="3" stroke-dasharray="8 7" fill="none"/><circle class="scene-halo" cx="274" cy="301" r="19" stroke="#ffc45e" stroke-width="2" fill="none"/><circle class="scene-halo" cx="738" cy="57" r="19" stroke="#ffc45e" stroke-width="2" fill="none"/>') if active else ''}
<text x="28" y="38" fill="#91a4bc" font-size="14">작동 원리 예시 · 실제 설치 배치와 다를 수 있습니다</text>
</svg>'''

def enhance(soup):
    section=soup.find(id='blind-corner')
    diagram=section.select_one('[aria-label="가려진 교차로의 양방향 경고 구조"]')
    details=soup.new_tag('details',attrs={'class':'pedestrian-structure'})
    summary=soup.new_tag('summary');summary.string='설치 구성 살펴보기';details.append(summary)
    diagram.wrap(details)
    # Put the old schematic reference after the central story, keeping all source facts.
    flow=section.select_one('.editorial-flow');flow.insert_after(details.extract())
    labels=['가려진 시야','접근 감지','양쪽에 알림']
    for i,step in enumerate(flow.find_all('li',recursive=False)):
        step['class']=step.get('class',[])+['pedestrian-story-panel']
        step['data-flow-label']=labels[i]
        copy=soup.new_tag('div',attrs={'class':'pedestrian-story-copy'})
        span=step.find('span',recursive=False);span.name='h3'
        for node in list(step.contents):copy.append(node.extract())
        from product_infographics import figure as infographic_figure
        step.append(BeautifulSoup(infographic_figure('pedestrian-collision-prevention',i) or visual(i),'html.parser'));step.append(copy)
