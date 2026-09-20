"""Product-specific benefit stories, backed by the preserved product references."""
import json
from product_story_visuals import scene
from pathlib import Path
from html import escape as esc
ROOT=Path(__file__).resolve().parents[1]
BENEFITS=json.loads((ROOT/'data/product-benefits.json').read_text())
IMAGES=json.loads((ROOT/'data/product-editorial-images.json').read_text())

def build(slug, name, kind, soup):
    if slug not in BENEFITS:return ''
    stages=BENEFITS[slug]['stages']
    # Detailed operating procedures stay accessible without another forced scroll journey.
    for track in list(soup.select('[data-scroll-flow]')):
        flow=track.select_one('.editorial-flow')
        if not flow:continue
        details=soup.new_tag('details',attrs={'class':'benefit-operation-details'})
        summary=soup.new_tag('summary');summary.string='작동 순서와 운영 방법 살펴보기';details.append(summary)
        flow.extract()
        flow['class']=['benefit-operation-list']
        for li in flow.find_all('li',recursive=False):
            li.attrs.pop('data-flow-panel',None)
        details.append(flow);track.replace_with(details)
    tabs='';panels=''
    for i,s in enumerate(stages):
        ident=f'{slug}-benefit-{i}'
        asset=IMAGES[slug][s['reference']].copy()
        # CMS uses the already-authored matching construction phase scenes.
        if slug=='site-cms':
            old=soup.select('#process-transition-line .editorial-flow img, #process-transition-line .benefit-operation-list img')
            if i<len(old):
                asset.update({k:old[i].get(k,asset.get(k,'')) for k in ['src','srcset','width','height']})
                asset['alt']=['굴착 구간과 현장 동선이 보이는 착공 초기 공사 현장 도식','타워크레인과 골조가 올라가는 중기 공사 현장 도식','상층 골조와 외장 작업이 진행되는 준공 전 공사 현장 도식'][i]
        tabs+=f'<button type="button" role="tab" id="{ident}-tab" aria-controls="{ident}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}"><span class="benefit-tab-number">{i+1:02}</span>{esc(s["label"])}</button>'
        figure=scene(slug,i,asset)
        panels+=f'<li class="benefit-panel" id="{ident}" data-flow-panel>{figure}<div class="benefit-copy"><p class="benefit-kicker">{esc(s["label"])}</p><h3>{esc(s["title"])}</h3><p class="benefit-description">{esc(s["body"])}</p><a class="benefit-detail-link" href="#{esc(s["reference"])}">관련 구성 자세히 보기 <span aria-hidden="true">↗</span></a></div></li>'
    return f'<section class="editorial-chapter benefit-chapter" id="product-benefits" data-benefit-kind="{kind}"><div class="editorial-section-inner"><header class="benefit-heading"><p class="editorial-kicker">{esc(name)}</p><h2>{esc(BENEFITS[slug]["heading"])}</h2></header><div class="product-flow-track" data-scroll-flow><div class="product-flow-stage"><div class="product-flow-tabs" role="tablist" aria-label="제품 강점 살펴보기" hidden>{tabs}</div><ol class="editorial-flow benefit-panels" aria-label="제품의 세 가지 강점">{panels}</ol></div></div></div></section>'
