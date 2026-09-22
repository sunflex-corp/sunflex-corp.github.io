#!/usr/bin/env python3
"""Apply only confirmed, scene-scoped fixes from Pro review 05."""
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/product-infographics.json'

def load(markup): return BeautifulSoup(markup,'html.parser')
def scene(soup,name):
 node=soup.select_one(f'[data-infographic-scene="{name}"]')
 if not node: raise ValueError(name)
 return node
def style(soup,name,rules):
 for n in soup.select('[data-pro-review="wearable-style"]'): n.decompose()
 n=soup.new_tag('style',attrs={'data-pro-review':'wearable-style'});n.string=rules;scene(soup,name).insert(0,n)
def put(soup,selector,html,where='append'):
 target=soup.select_one(selector)
 if not target: raise ValueError(selector)
 node=BeautifulSoup(html,'html.parser')
 getattr(target,where)(node)

def heart_one(markup):
 s=load(markup); name='healthcare-heart-band-1'; tech=s.select_one('.technical-graphic')
 for n in tech.select('.technical-pin')[1:]: n.decompose()
 # Remove the leaders with their functional pins, plus the cropped decorative trace.
 for n in tech.select('path[d="M570 326 L745 227"], path[d="M588 348 L744 371"], g[transform="translate(71 435)"]'): n.decompose()
 calls=s.select_one('.technical-callouts'); calls.clear()
 calls.append(BeautifulSoup('<li class="technical-callout"><span class="technical-marker">A</span><span class="technical-callout-copy"><strong>심박 신호 측정</strong><span>착용 중 신호를 확인</span></span></li><li class="qa-alert-targets"><span><strong>착용자 알림</strong><small>설정 범위 알림 · 진동 안내</small></span><span><strong>담당자 알림</strong><small>지정 담당자에게 함께 전달</small></span></li>','html.parser'))
 style(s,name,'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="healthcare-heart-band-1"] .technical-callouts{grid-template-columns:1fr}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="healthcare-heart-band-1"] .qa-alert-targets{border:0;padding:0;background:none;box-shadow:none;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;list-style:none}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="healthcare-heart-band-1"] .qa-alert-targets>span{display:grid;gap:4px;padding:12px;border:1px solid rgb(215 166 174 / 35%);border-radius:12px;background:rgb(215 166 174 / 8%)}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="healthcare-heart-band-1"] .qa-alert-targets strong{color:#fff;font-size:16px}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="healthcare-heart-band-1"] .qa-alert-targets small{color:#d7e2de;font-size:14px;line-height:1.45}@container sunflex-infographic (max-width:480px){.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="healthcare-heart-band-1"] .qa-alert-targets{grid-template-columns:1fr}}')
 return str(s)
def heart_two(markup):
 s=load(markup);name='healthcare-heart-band-2';band=s.select_one('.threshold-band')
 if band: band.replace_with(BeautifulSoup('<div class="qa-range-condition"><strong>설정 범위 이탈 시</strong><span aria-hidden="true">↓</span></div>','html.parser'))
 style(s,name,'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="healthcare-heart-band-2"] .qa-range-condition{display:grid;justify-items:center;gap:6px;margin:12px 0;color:var(--ink)}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="healthcare-heart-band-2"] .qa-range-condition strong{font-size:16px;font-weight:780}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="healthcare-heart-band-2"] .qa-range-condition span{color:var(--accent);font-size:22px;font-weight:800;line-height:1}')
 return str(s)
def gate(markup):
 s=load(markup);name='worker-access-gate-2';style(s,name,'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="worker-access-gate-2"] .scene-labels{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;text-align:center}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="worker-access-gate-2"] .scene-labels span{min-width:0;margin:0;word-break:keep-all;overflow-wrap:normal}')
 return str(s)
def airbag(markup):
 s=load(markup);name='smart-airbag-2'
 for old in s.select('.qa-deploy-flow'): old.decompose()
 put(s,'.technical-heading','<ol class="qa-deploy-flow"><li>움직임 감지</li><li>내장 CO₂ 가스</li><li>에어백 전개</li></ol>')
 style(s,name,'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-airbag-2"] .qa-deploy-flow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:16px 0 0;padding:0;list-style:none;color:var(--ink);font-size:14px;line-height:1.45}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-airbag-2"] .qa-deploy-flow li{min-width:0;margin:0;padding:10px 6px;border:1px solid var(--technical-line);border-radius:8px;background:rgb(255 255 255 / 4%);color:var(--ink);font-size:14px;text-align:center;word-break:keep-all}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-airbag-2"] .qa-deploy-flow li::before{content:none}')
 return str(s)
def helmet(markup):
 s=load(markup);name='smart-helmet-2'
 if not s.select_one('[data-pro-review="helmet-link"]'): put(s,'.render-stage','<svg aria-hidden="true" class="qa-part-link" data-pro-review="helmet-link" viewBox="0 0 1600 900"><path d="M475 645 C660 730 885 700 1030 510"/><circle cx="475" cy="645" r="8"/><circle cx="1030" cy="510" r="8"/></svg><span class="qa-part-label qa-helmet-label">안전모 착용 확인</span><span class="qa-part-label qa-strap-label">턱끈 체결 확인</span>')
 style(s,name,'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-helmet-2"] .qa-part-link{position:absolute;inset:0;width:100%!important;height:100%!important;fill:none!important;stroke:#c1ca93!important;stroke-width:2!important;pointer-events:none}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-helmet-2"] .qa-part-link path{vector-effect:non-scaling-stroke;stroke-dasharray:6 7}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-helmet-2"] .qa-part-label{position:absolute;padding:7px 10px;border:1px solid rgb(193 202 147 / 55%);border-radius:999px;background:rgb(20 29 27 / 82%);color:#f4f8e8;font-size:14px;font-weight:740;line-height:1;pointer-events:none}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-helmet-2"] .qa-helmet-label{left:10%;bottom:10%}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-helmet-2"] .qa-strap-label{right:8%;top:16%}')
 return str(s)
def hook(markup):
 s=load(markup);name='smart-safety-hook-2'
 for n in s.select('.render-annotations .qa-voice-flow'): n.decompose()
 if not s.select_one('.qa-voice-label'): put(s,'.render-stage','<span class="qa-voice-label">음성 안내</span>')
 if not s.select_one('.qa-voice-flow'):
  ol=s.select_one('.render-annotations'); ol.insert_after(BeautifulSoup('<p class="qa-voice-flow">체결이 필요한 상태 <b aria-hidden="true">→</b> 음성 안내</p>','html.parser'))
 style(s,name,'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-safety-hook-2"] .qa-voice-label{position:absolute;right:8%;top:27%;padding:7px 10px;border:1px solid rgb(211 179 121 / 56%);border-radius:999px;background:rgb(25 30 33 / 83%);color:#fff5dc;font-size:14px;font-weight:740;line-height:1;pointer-events:none}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-safety-hook-2"] .qa-voice-flow{display:flex;gap:9px;align-items:center;margin:0;padding:12px 20px;color:#dce6e9;font-size:14px}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="smart-safety-hook-2"] .qa-voice-flow b{color:var(--accent);font-size:18px}')
 return str(s)
def main():
 d=json.loads(DATA.read_text())
 d['healthcare-heart-band'][0]=heart_one(d['healthcare-heart-band'][0]);d['healthcare-heart-band'][1]=heart_two(d['healthcare-heart-band'][1]);d['worker-access-gate'][1]=gate(d['worker-access-gate'][1]);d['smart-airbag'][1]=airbag(d['smart-airbag'][1]);d['smart-helmet'][1]=helmet(d['smart-helmet'][1]);d['smart-safety-hook'][1]=hook(d['smart-safety-hook'][1])
 DATA.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Applied confirmed Pro review 05 wearable fixes.')
if __name__=='__main__':main()
