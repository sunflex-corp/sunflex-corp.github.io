#!/usr/bin/env python3
"""Apply confirmed Pro review 04 information and motion fixes."""
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/product-infographics.json'

def doc(markup): return BeautifulSoup(markup, 'html.parser')
def target(s, name):
    n = s.select_one(f'[data-infographic-scene="{name}"]')
    if not n: raise ValueError(name)
    return n
def css(s, name, rules):
    for n in s.select('[data-pro-review="zone-motion"]'): n.decompose()
    n=s.new_tag('style',attrs={'data-pro-review':'zone-motion'}); n.string=rules; target(s,name).insert(0,n)

def beacon(markup):
    s=doc(markup); bottom=s.select_one('.diagram-bottom'); bottom.clear(); bottom.append(BeautifulSoup('<strong>확인 구역: A 작업 구역</strong>','html.parser'))
    css(s,'smart-beacon-1','''.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-beacon-1"] .map-a{border-color:var(--accent);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 45%,transparent)}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-beacon-1"] .map-pin{left:11%;top:42%;max-width:20%;gap:5px}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-beacon-1"] .map-pin span{font-size:12px;line-height:1.25;word-break:keep-all}@container sunflex-infographic (max-width:480px){.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-beacon-1"] .map-pin{left:10%;top:43%;max-width:22%}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-beacon-1"] .map-pin span{display:none}}''')
    return str(s)

def suit(markup):
    s=doc(markup); g=s.select_one('.technical-graphic'); g.clear()
    g.append(BeautifulSoup('''<svg aria-label="몸을 굽힌 상태에서 자재를 들어 올리는 두 자세의 개념도" class="technical-svg qa-lift-poses" role="img" viewBox="0 0 760 310"><defs><linearGradient id="qa-suit-metal" x1="0" x2="1"><stop stop-color="#d8ebe1"/><stop offset="1" stop-color="#8eaa9b"/></linearGradient></defs><path class="qa-floor" d="M66 282H694"/><g class="qa-pose" transform="translate(76 8)"><path opacity=".55" d="M89 184 65 220 64 264h22M130 115 160 151 171 177"/><circle cx="152" cy="72" r="19"/><path d="M131 62q4-26 26-20 14 4 15 22h-44"/><path class="qa-torso" d="M131 96 156 115 112 191 83 178 96 138Z"/><path d="M106 189 128 222 113 264h25M146 118 184 149 189 176"/><path class="qa-suit" d="M126 103 108 138 95 177 114 205"/><path class="qa-box" d="M163 175h57v42h-57Z"/></g><path class="qa-arrow" d="M355 157h58"/><path class="qa-arrow-head" d="m400 144 14 13-14 13"/><g class="qa-pose" transform="translate(437 8)"><path opacity=".55" d="M102 177 89 220 83 264h22M111 109 145 146 165 149"/><circle cx="127" cy="58" r="19"/><path d="M107 47q5-25 26-18 13 4 15 22h-44"/><path class="qa-torso" d="M108 82 136 88 140 166 112 189 92 171Z"/><path d="M127 182 142 221 146 264h24M136 105 163 136 184 148"/><path class="qa-suit" d="M109 90 103 134 105 168 115 203"/><path class="qa-box" d="M163 148h57v42h-57Z"/></g></svg><div class="qa-pose-labels"><span>몸을 굽힌 자세</span><span>들어 올리는 자세</span></div><p class="qa-lift-caption"><strong>탄성 구조</strong><span>자세 변화에 따라 들기 동작을 보조</span></p>''','html.parser'))
    for pin in s.select('.technical-pin,.technical-callouts .technical-marker'): pin.decompose()
    css(s,'power-assist-suit-2','''.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] .qa-lift-poses{display:block;width:100%;height:auto;background:radial-gradient(circle at 50% 35%,rgb(178 195 161 / 13%),transparent 52%)}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] .qa-floor{fill:none;stroke:#6e867b;stroke-width:2}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] .qa-pose{fill:none;stroke:#dceae2;stroke-linecap:round;stroke-linejoin:round;stroke-width:7}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] .qa-suit{fill:none;stroke:url(#qa-suit-metal);stroke-width:12}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] .qa-box{fill:rgb(178 195 161 / 18%);stroke:#d9ead3;stroke-width:4}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] :is(.qa-arrow,.qa-arrow-head){fill:none;stroke:var(--accent);stroke-width:4}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] .qa-lift-poses text{fill:#f1f6f2;font-family:inherit;font-size:19px;font-weight:780;text-anchor:middle}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] .qa-lift-caption{display:flex;align-items:baseline;justify-content:center;gap:10px;margin:0;padding:12px 18px;border-top:1px solid rgb(213 235 224 / 16%);color:#c8d4cd;font-size:14px;line-height:1.45;text-align:center}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] .qa-lift-caption strong{color:var(--accent);font-size:15px}@container sunflex-infographic (max-width:480px){.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] .qa-lift-caption{display:grid;gap:2px;font-size:13px}}''')
    extra_css = '.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="power-assist-suit-2"] '
    rules = extra_css + '.qa-torso{fill:#2d413a}'+extra_css+'.qa-pose-labels{display:grid;grid-template-columns:1fr 1fr;gap:28px;padding:0 16px 16px;color:#f1f6f2;font-size:16px;text-align:center;word-break:keep-all}'+extra_css+'.qa-pose-labels span{padding:0;border:0}'+extra_css+'.technical-callout{display:block}'
    s.select_one('[data-pro-review="zone-motion"]').append(rules)
    return str(s)

def checklist(markup, heading):
    s=doc(markup); h=s.select_one('.sheet-head > span'); h.clear();h.append(heading)
    for row in s.select('.data-row'):
        st=row.select_one('strong')
        if st and st.get_text(strip=True) in {'재측정 대상','탄성 상태','지급·회수'}:
            for extra in row.select('span:not(.row-number)'): extra.decompose()
    return str(s)

def main():
    data=json.loads(DATA.read_text())
    data['smart-beacon'][0]=beacon(data['smart-beacon'][0])
    data['power-assist-suit'][1]=suit(data['power-assist-suit'][1])
    data['alcohol-detection'][2]=checklist(data['alcohol-detection'][2],'재확인 항목')
    data['power-assist-suit'][2]=checklist(data['power-assist-suit'][2],'착용·운영 점검 항목')
    DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Applied confirmed Pro review 04 zone and motion fixes.')
if __name__=='__main__': main()
