"""Apply the reviewed 2026-09-22 composition corrections to durable fragments.

Edits are idempotent. Source specifications and product claims are unchanged.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json, re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'data/product-infographics.json'
data = json.loads(path.read_text())

for slug, figures in data.items():
    for index, markup in enumerate(figures):
        soup = BeautifulSoup(markup, 'html.parser')
        figure = soup.select_one('figure')
        figure['data-visual-kind'] = ('render' if soup.select_one('.render-stage') else 'scene' if soup.select_one('.subject-scene,.technical-graphic') else 'diagram')
        # Crop empty SVG viewBox margins, preserving every leader and its marker.
        svg = soup.select_one('.technical-svg')
        if svg:
            for decoration in svg.select('g[transform="translate(70 420)"],g[transform="translate(675 134)"]'):
                decoration.decompose()
        if svg and not svg.has_attr('data-focus-crop'):
            x, y, width, height = 195, 100, 630, 395
            svg['viewbox'] = f'{x} {y} {width} {height}'
            svg['data-focus-crop'] = '20260922'
            for pin in soup.select('.technical-pin'):
                a, b = map(float, re.findall(r'([\d.]+)%', pin['style']))
                pin['style'] = f'left:{(a*10-x)/width*100:.3f}%;top:{(b*5.6-y)/height*100:.3f}%'
        # The A/B/C feature legend already explains these duplicate numbered rows.
        for flow in soup.select('.technical-flow'):
            flow.decompose()
        # Do not invent names for unmarked objects; the descriptions suffice.
        if soup.select_one('.scene-labels') and not soup.select_one('.technical-pin'):
            for number in soup.select('.scene-labels b'):
                number.decompose()
        for node in soup.select('.caption-rule'):
            node.decompose()
        # The scene already has its own inset; remove redundant blank SVG margins.
        scene = soup.select_one('.subject-scene>svg')
        if scene:
            scene['viewbox'] = '25 40 590 255'
        # Correct a brand mismatch in the illustrative attendance card.
        for node in soup.find_all(string=lambda t: t and t.strip() == 'SUNFLEX'):
            node.replace_with('SUNPLEX')
        for image in soup.select('img'):
            w, h = Image.open(ROOT / image['src'].lstrip('/')).size
            image['width'], image['height'] = str(w), str(h)
            image['loading'], image['decoding'] = 'lazy', 'async'
        figures[index] = str(soup)

# A mesh is a network relation, not three disconnected equipment cards.
mesh = BeautifulSoup(data['wireless-network'][1], 'html.parser')
old = mesh.select_one('.flow-tiles')
if old:
    old.replace_with(BeautifulSoup('''<div class="mesh-network" role="img" aria-label="현장 사무실의 AP와 중계 AP, 작업 구간 AP를 연결하는 메시 네트워크 구성 예시">
      <svg viewBox="0 0 560 210" aria-hidden="true"><path d="M90 110L280 48L470 110M90 110H470M280 48V174M90 110L280 174L470 110"/><circle cx="90" cy="110" r="20"/><circle cx="280" cy="48" r="20"/><circle cx="470" cy="110" r="20"/><circle cx="280" cy="174" r="20"/></svg>
      <div class="mesh-labels"><span><strong>현장 사무실</strong>정보 연결</span><span><strong>무선 AP</strong>구간 사이 중계</span><span><strong>작업 구간</strong>현장에서 확인</span></div>
    </div>''', 'html.parser'))
data['wireless-network'][1] = str(mesh)

# Keep three information sources visibly inside one board, including on phones.
board = BeautifulSoup(data['safety-box'][0], 'html.parser')
tiles = board.select_one('.flow-tiles')
if tiles:
    tiles['class'] = list(dict.fromkeys(tiles.get('class', []) + ['unified-board']))
data['safety-box'][0] = str(board)

corner = BeautifulSoup(data['pedestrian-collision-prevention'][2], 'html.parser')
diagram = corner.select_one('.diagram')
if diagram:
    diagram.clear()
    diagram.append(BeautifulSoup('''<h4>모퉁이 양쪽에 알림</h4><div class="corner-plan" role="img" aria-label="시야를 가리는 모퉁이의 양쪽 통행 구간에 경고를 전달하는 설치 구성 예시">
    <div class="corner-wall-label">시야를 가리는<br/>구조물</div>
    <div class="corner-vehicle"><strong>운전자</strong><span>진입 구간에서 확인</span><b aria-hidden="true">→</b></div>
    <div class="corner-beacon"><span aria-hidden="true">◉</span><strong>접근 경고</strong></div>
    <div class="corner-person"><b aria-hidden="true">↑</b><strong>보행자</strong><span>통행 구간에서 확인</span></div>
    </div><p class="diagram-note">교차하는 두 동선에 같은 위험을 알립니다.</p>''','html.parser'))
data['pedestrian-collision-prevention'][2] = str(corner)

environment = BeautifulSoup(data['smart-environment-board'][1], 'html.parser')
screen = environment.select_one('.instrument-readout')
if screen and not screen.has_attr('data-output-screen'):
    screen['data-output-screen'] = 'environment'
    heading = environment.new_tag('div', attrs={'class':'environment-display-title'})
    heading.string = '현장 환경전광판'
    screen.insert(0, heading)
    for row in screen.select('.instrument-row'):
        small = row.select_one('small')
        if small: small.decompose()
        value = environment.new_tag('b', attrs={'class':'environment-display-value'})
        value.string = '측정값'
        row.append(value)
data['smart-environment-board'][1] = str(environment)

# Use action-specific icons instead of the former generic camera/eye placeholders.
icons = [
 ('alcohol-detection',1,'.route-stop svg',0,'M8 15a6 6 0 1 1 8-8M8 21h9M20 18h6M20 22h6M29 14h7v20H23V26'),
 ('smart-beacon',1,'.board-cell svg',1,'M8 15a17 17 0 0 1 24 0M13 21a10 10 0 0 1 14 0M17 27a4 4 0 0 1 6 0M20 32v3'),
 ('worker-access-gate',2,'.event-icon svg',1,'M35 21a15 15 0 1 1-30 0 15 15 0 0 1 30 0M20 11v11l8 5'),
 ('concrete-curing',1,'.history-title svg',0,'M15 25V8a5 5 0 0 1 10 0v17a9 9 0 1 1-10 0M20 12v18M29 10h6M29 17h4'),
 ('ai-safety-index',2,'.board-cell svg',1,'M14 9h22M14 21h17M14 33h12M5 6v29M2 31l3 4 3-4'),
 ('fire-detection',1,'.time-symbol svg',1,'M8 17h7l10-9v26l-10-9H8Z M30 14q10 7 0 14'),
 ('fire-detection',1,'.time-symbol svg',2,'M6 36V6h16v7M13 35V14h9M22 24h14M30 18l6 6-6 6'),
]
for slug, index, selector, item, drawing in icons:
    soup = BeautifulSoup(data[slug][index], 'html.parser')
    svg = soup.select(selector)[item]
    svg.clear()
    svg.append(soup.new_tag('path', attrs={'d':drawing}))
    data[slug][index] = str(soup)

path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('Refined 144 durable figures: visual types, focused SVGs, consolidated legends.')
