#!/usr/bin/env python3
"""Apply confirmed Pro review 06 relationship improvements."""
import json
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/product-infographics.json'
def doc(x): return BeautifulSoup(x,'html.parser')
def target(s,n):
    r=s.select_one(f'[data-infographic-scene="{n}"]')
    if not r: raise ValueError(n)
    return r
def css(s,n,r):
    for x in s.select('[data-pro-review="final"]'):x.decompose()
    x=s.new_tag('style',attrs={'data-pro-review':'final'});x.string=r;target(s,n).insert(0,x)
def drone(x):
    s=doc(x);svg=s.select_one('.ctx-drone-plan svg')
    for label in svg.select('.ctx-drone-text text'):
        if '구조물 면' in label.get_text():label.decompose()
    if not s.select_one('.qa-location-caption'):s.select_one('.ctx-drone-plan').insert_after(BeautifulSoup('<p class="qa-location-caption">구조물 면 · 기록 위치</p>','html.parser'))
    css(s,'ai-drone-inspection-2','''.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-drone-inspection-2"] .qa-location-caption{margin:10px 2px 0!important;color:#dcebe0!important;font-size:14px!important;font-weight:720;line-height:1.4;text-align:right;word-break:keep-all}''')
    return str(s)
def inspectcut(x):
    s=doc(x);timeline=s.select_one('.timeline-visual')
    if timeline: timeline.replace_with(BeautifulSoup('''<div class="qa-range-story" aria-label="촬영 원본에서 선택 구간을 검토 장면으로 연결"><div class="qa-range-source"><span>촬영 원본</span><div class="qa-film"><i></i><b>선택 구간</b><i></i></div></div><span class="qa-range-arrow" aria-hidden="true">→</span><div class="qa-range-result"><span>검측 장면</span><strong>선택한 구간</strong></div></div>''','html.parser'))
    css(s,'inspectcut-1','''.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-range-story{display:grid;grid-template-columns:minmax(0,1.65fr) auto minmax(0,.85fr);gap:16px;align-items:center;margin:auto 0;padding:22px;border:1px solid #4d5d68;border-radius:14px;background:#202b31}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] :is(.qa-range-source,.qa-range-result){display:grid;gap:10px}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] :is(.qa-range-source>span,.qa-range-result>span){color:#bbc9ce;font-size:13px;font-weight:720}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-film{display:grid;grid-template-columns:1fr 1.25fr 1fr;gap:4px;padding:7px;border:1px solid #52636d;border-radius:9px;background:#172126}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-film :is(i,b){min-width:0;height:42px;border-radius:4px}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-film i{background:#35444c}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-film b{display:grid;place-items:center;outline:2px solid var(--accent);outline-offset:2px;background:color-mix(in srgb,var(--accent) 19%,#273238);color:#f1f4f5;font-size:13px;word-break:keep-all}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-range-arrow{color:var(--accent);font-size:27px;font-weight:800}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-range-result{align-self:stretch;padding:14px;border-radius:9px;background:rgb(173 183 212 / 10%)}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-range-result strong{color:#f1f3f7;font-size:18px;line-height:1.35;word-break:keep-all}@container sunflex-infographic (max-width:480px){.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-range-story{grid-template-columns:1fr;gap:12px}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="inspectcut-1"] .qa-range-arrow{justify-self:center;transform:rotate(90deg)}}''')
    return str(s)
def crane(x):
    s=doc(x);s.select_one('.ctx-title').string='훅 인양 정보와 상부 풍속을 함께'
    if not s.select_one('.qa-lift-output'):s.select_one('.ctx-callout-list').insert_after(BeautifulSoup('<div class="qa-lift-output"><span>훅 인양 센서</span><strong>하중 · 훅 거리 <b aria-hidden="true">→</b> 조종석 화면</strong></div>','html.parser'))
    css(s,'iot-small-tower-crane-1','''.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="iot-small-tower-crane-1"] .qa-lift-output{display:grid;gap:4px;margin:12px 0 0;padding:13px 16px;border:1px solid rgb(217 188 123 / 37%);border-radius:12px;background:rgb(217 188 123 / 8%)}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="iot-small-tower-crane-1"] .qa-lift-output span{color:#d9bc7b;font-size:13px;font-weight:760}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="iot-small-tower-crane-1"] .qa-lift-output strong{color:#f3f6f7;font-size:15px;line-height:1.45}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="iot-small-tower-crane-1"] .qa-lift-output b{color:var(--accent);font-size:18px}''')
    return str(s)
def curing(x):
    s=doc(x);r=s.select_one('.history-ruler');r.decompose() if r else None;e=s.select_one('.history-events')
    for a in e.select('.qa-curing-arrow'):a.decompose()
    for node in list(e.find_all('div',recursive=False))[:-1]:node.insert_after(BeautifulSoup('<i aria-hidden="true" class="qa-curing-arrow">→</i>','html.parser'))
    css(s,'concrete-curing-2','''.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="concrete-curing-2"] .history-events{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr) auto minmax(0,1fr);gap:10px;align-items:center}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="concrete-curing-2"] .qa-curing-arrow{color:var(--accent);font-size:22px;font-style:normal;font-weight:800}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="concrete-curing-2"] .history-events>div{min-width:0}@container sunflex-infographic (max-width:480px){.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="concrete-curing-2"] .history-events{grid-template-columns:1fr;gap:8px}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="concrete-curing-2"] .qa-curing-arrow{justify-self:center;transform:rotate(90deg)}}''')
    return str(s)
def accident(x):
    s=doc(x);p=s.select_one('.dual-panels')
    if not p.select_one('.qa-case-transfer'):
        cards=list(p.select(':scope > .dual-panel'));wrap=s.new_tag('div',attrs={'class':'qa-case-transfer'});cards[0].extract();cards[1].extract();wrap.append(cards[0]);wrap.append(BeautifulSoup('<span class="qa-case-arrow" aria-hidden="true">→</span>','html.parser'));wrap.append(cards[1]);p.append(wrap)
    for card,label,note in zip(p.select('.dual-panel'), ['유사 사례','안전조회·교육'], ['관련 사례를 확인','교육 자료로 활용']):
        card.select_one('small').string=label
        status=card.select_one('.status-line');status.clear();status.append(note)
    s.select_one('.shared-line span').string='관련 사고 사례를 현장 교육 자료로 활용'
    css(s,'ai-similar-accident-alert-3','''.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-similar-accident-alert-3"] .dual-panels{display:block}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-similar-accident-alert-3"] .qa-case-transfer{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);gap:14px;align-items:center}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-similar-accident-alert-3"] .qa-case-arrow{color:var(--accent);font-size:27px;font-weight:800}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-similar-accident-alert-3"] .shared-line{width:82%}@container sunflex-infographic (max-width:480px){.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-similar-accident-alert-3"] .qa-case-transfer{grid-template-columns:1fr}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-similar-accident-alert-3"] .qa-case-arrow{justify-self:center;transform:rotate(90deg)}}''')
    return str(s)
def main():
    d=json.loads(DATA.read_text());d['ai-drone-inspection'][1]=drone(d['ai-drone-inspection'][1]);d['inspectcut'][0]=inspectcut(d['inspectcut'][0]);d['iot-small-tower-crane'][0]=crane(d['iot-small-tower-crane'][0]);d['concrete-curing'][1]=curing(d['concrete-curing'][1]);d['ai-similar-accident-alert'][2]=accident(d['ai-similar-accident-alert'][2]);DATA.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Applied confirmed Pro review 06 relationship fixes.')
if __name__=='__main__':main()
