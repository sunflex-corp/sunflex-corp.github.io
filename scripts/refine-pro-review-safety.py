#!/usr/bin/env python3
"""Scene-specific semantic fixes confirmed by Pro review 03."""
import json
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]; P=R/'data/product-infographics.json'
def S(x): return BeautifulSoup(x,'html.parser')
def sty(s,scene,css):
 for n in s.select('[data-pro-review="safety-style"]'):n.decompose()
 t=s.new_tag('style',attrs={'data-pro-review':'safety-style'});t.string=css;s.select_one(f'[data-infographic-scene="{scene}"]').insert(0,t)
def collision(x):
 s=S(x);box=s.select_one('.selection-box')
 for old in box.select('.qa-detected-person'): old.decompose()
 box.insert(0,BeautifulSoup('<svg aria-hidden="true" class="qa-detected-person" viewBox="0 0 40 56"><circle cx="20" cy="10" r="7"/><path d="M20 18v19M20 24 8 33M20 24l12 9M20 37l-8 14M20 37l8 14"/></svg>','html.parser'));sty(s,'ai-equipment-collision-2','.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-equipment-collision-2"] .selection-box{display:grid;place-items:center;padding:24px 8px 8px;background:rgb(26 37 44 / 35%)}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-equipment-collision-2"] .qa-detected-person{width:38px!important;height:52px!important;fill:none;stroke:var(--accent);stroke-width:2.5;pointer-events:none}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="ai-equipment-collision-2"] .selection-box>span{position:absolute;top:-25px;bottom:auto;left:0;right:auto;height:auto;padding:3px 6px;white-space:nowrap;font-size:12px;line-height:1.3}')
 return str(s)
def radio1(x):
 s=S(x);s.select_one('.group-target.is-active small').string='선택 대상';sty(s,'digital-radio-1','.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="digital-radio-1"] .group-link{width:34%;margin-left:16.5%;border-right:0}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="digital-radio-1"] .group-link::after{left:0;width:1px}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="digital-radio-1"] .group-target:not(.is-active)::before{display:none}')
 return str(s)
def radio2(x):
 s=S(x);target=s.select('.dual-panel .large-icon')[1];target.clear();target.append(BeautifulSoup('<svg aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="12" cy="7" r="3"/><path d="M6 21v-3a6 6 0 0 1 12 0v3"/></svg>','html.parser'));return str(s)
def broadcast(x):
 s=S(x);target=s.select('.time-symbol')[1];target.clear();target.append(BeautifulSoup('<svg aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" viewBox="0 0 24 24"><rect height="18" rx="1.5" width="8" x="3" y="3"/><path d="M5 7h4M5 11h4M5 15h4M14 12h8m-3-3 3 3-3 3"/></svg>','html.parser'));return str(s)
def approach(x):
 s=S(x);mark=s.select_one('.stop-mark');mark.decompose() if mark else None;labels=s.select_one('.scene-labels');labels.clear();labels.append(BeautifulSoup('<span>경고 확인 후, 정지·유도 판단</span><span>유도원 확인</span>','html.parser'));sty(s,'equipment-approach-alarm-3','.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="equipment-approach-alarm-3"] .scene-labels{grid-template-columns:2fr 1fr}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="equipment-approach-alarm-3"] .scene-labels span:first-child{font-weight:740;color:#f3ece0}')
 return str(s)
def main():
 d=json.loads(P.read_text());d['ai-equipment-collision'][1]=collision(d['ai-equipment-collision'][1]);d['digital-radio'][0]=radio1(d['digital-radio'][0]);d['digital-radio'][1]=radio2(d['digital-radio'][1]);d['wireless-emergency-broadcast'][1]=broadcast(d['wireless-emergency-broadcast'][1]);d['equipment-approach-alarm'][2]=approach(d['equipment-approach-alarm'][2]);P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Applied Pro review 03 safety fixes.')
if __name__=='__main__':main()
