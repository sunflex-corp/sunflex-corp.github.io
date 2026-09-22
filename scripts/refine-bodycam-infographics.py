#!/usr/bin/env python3
"""Create the two product-specific mobile bodycam infographic fragments."""

from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "product-infographics.json"
CAPTION = "기능을 설명한 구성 예시 · 실제 제품·설치 환경에 따라 달라질 수 있습니다"


def fragment(scene: str, aria: str, title: str, body: str, css: str) -> str:
    shared = """
      .product-editorial .sunflex-infographic[data-infographic-scene=\"SCENE\"] .bc-board{display:grid;gap:18px;padding:clamp(18px,3.4cqi,30px);background:linear-gradient(145deg,#172530,#101921);color:#f3f7f9}
      .product-editorial .sunflex-infographic[data-infographic-scene=\"SCENE\"] .bc-board *, .product-editorial .sunflex-infographic[data-infographic-scene=\"SCENE\"] .bc-board *::before, .product-editorial .sunflex-infographic[data-infographic-scene=\"SCENE\"] .bc-board *::after{box-sizing:border-box}
      .product-editorial .sunflex-infographic[data-infographic-scene=\"SCENE\"] :is(.bc-title,.bc-label,.bc-copy){margin:0!important}
      .product-editorial .sunflex-infographic[data-infographic-scene=\"SCENE\"] .bc-title{font-size:clamp(22px,3.1cqi,31px);font-weight:760;letter-spacing:-.05em;line-height:1.28}
      .product-editorial .sunflex-infographic[data-infographic-scene=\"SCENE\"] .bc-label{color:var(--accent)!important;font-size:14px;font-weight:760;letter-spacing:.03em;line-height:1.4}
      .product-editorial .sunflex-infographic[data-infographic-scene=\"SCENE\"] .bc-copy{color:#d4e0e5!important;font-size:16px;font-weight:590;letter-spacing:-.025em;line-height:1.55}
      .product-editorial .sunflex-infographic[data-infographic-scene=\"SCENE\"] .bc-shell{min-width:0;border:1px solid rgb(224 238 244 / 24%);border-radius:18px;background:rgb(31 47 58 / 92%);box-shadow:inset 0 1px 0 rgb(255 255 255 / 8%)}
      @container sunflex-infographic (max-width:480px){[data-infographic-scene=\"SCENE\"] .bc-board{padding:18px;gap:14px}[data-infographic-scene=\"SCENE\"] .bc-title{font-size:24px}}
    """.replace("SCENE", scene)
    styles = dedent(shared + "\n" + css).strip()
    styles = styles.replace('.product-editorial .sunflex-infographic', '')
    styles = styles.replace('[data-infographic-scene=', '.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene=')
    return (
        f'<figure class="benefit-visual infographic-visual" data-infographic-version="20260922" '
        f'data-visual-kind="diagram"><div aria-label="{aria}" class="sunflex-infographic" '
        f'data-infographic-scene="{scene}" role="group" style="--accent:#a9bfdf"><style>{styles}</style>'
        f'<div class="visual-shell"><div aria-label="{aria}" class="diagram bc-diagram" role="group">'
        f'<div class="bc-board"><h4 class="bc-title">{title}</h4>{dedent(body).strip()}'
        f'</div></div></div></div><figcaption>{CAPTION}</figcaption></figure>'
    )


def bodycam_view() -> str:
    return fragment(
        "mobile-bodycam-1",
        "가슴에 장착한 바디캠이 작업자의 이동 시야 안에서 작업 장면을 기록하는 구성",
        "몸에 장착한 카메라로, 작업 시야를 기록",
        """
        <section class="bc-shell bc-chest-focus"><div class="bc-chest-head"><p class="bc-label">가슴 장착 확대</p><p class="bc-copy">작업자의 이동 시야 안에서 장면을 기록</p></div><svg aria-label="가슴에 장착한 바디캠에서 작업 구간으로 이어지는 시야" role="img" viewBox="0 0 620 300"><defs><linearGradient id="bc-bodycam-vest" x1="0" x2="1"><stop stop-color="#587486"/><stop offset="1" stop-color="#233d4e"/></linearGradient><linearGradient id="bc-bodycam-view" x1="0" x2="1"><stop stop-color="#9fc3e2" stop-opacity=".32"/><stop offset="1" stop-color="#9fc3e2" stop-opacity=".04"/></linearGradient></defs><path d="M34 258H586" class="bc-ground"/><path d="M64 238V86l104-55 93 55v152" class="bc-work-frame"/><path d="M94 192h139M128 86v152M194 86v152" class="bc-work-lines"/><path d="M328 260c0-100 48-168 107-168s107 68 107 168" class="bc-torso"/><path d="M366 128l69 48 70-48" class="bc-vest"/><rect class="bc-camera" height="52" rx="11" width="84" x="393" y="169"/><circle class="bc-lens" cx="435" cy="195" r="15"/><path d="M393 182 255 136 255 238 393 211Z" class="bc-sight"/><path d="M302 169h-30M302 205h-30" class="bc-measure"/><circle class="bc-pin" cx="260" cy="188" r="9"/></svg><div class="bc-chest-caption"><strong>가슴 장착</strong><span aria-hidden="true">→</span><strong>작업자 시야</strong><span aria-hidden="true">→</span><strong>작업 구간 기록</strong></div></section>
        """,
        """
        [data-infographic-scene="mobile-bodycam-1"] .bc-chest-focus{display:grid;gap:14px;padding:18px;background:linear-gradient(145deg,#263946,#1b2c37)}
        [data-infographic-scene="mobile-bodycam-1"] .bc-chest-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px}[data-infographic-scene="mobile-bodycam-1"] .bc-chest-head .bc-copy{font-size:14px;text-align:right}
        [data-infographic-scene="mobile-bodycam-1"] .bc-chest-focus svg{display:block;width:100%;height:auto;max-height:270px}[data-infographic-scene="mobile-bodycam-1"] :is(.bc-ground,.bc-work-frame,.bc-work-lines,.bc-torso,.bc-vest,.bc-camera,.bc-lens,.bc-measure){vector-effect:non-scaling-stroke}
        [data-infographic-scene="mobile-bodycam-1"] .bc-ground{stroke:#8ca0ab;stroke-width:2}[data-infographic-scene="mobile-bodycam-1"] .bc-work-frame{fill:none;stroke:#94a9b5;stroke-width:4}[data-infographic-scene="mobile-bodycam-1"] .bc-work-lines{stroke:#617a88;stroke-width:3}[data-infographic-scene="mobile-bodycam-1"] .bc-torso{fill:url(#bc-bodycam-vest);stroke:#afc4cf;stroke-width:3}[data-infographic-scene="mobile-bodycam-1"] .bc-vest{fill:none;stroke:#d9e7ed;stroke-width:3}[data-infographic-scene="mobile-bodycam-1"] .bc-camera{fill:#14232d;stroke:#d8e7ef;stroke-width:2}[data-infographic-scene="mobile-bodycam-1"] .bc-lens{fill:var(--accent);stroke:#eaf4f8;stroke-width:2}[data-infographic-scene="mobile-bodycam-1"] .bc-sight{fill:url(#bc-bodycam-view);stroke:var(--accent);stroke-width:2}[data-infographic-scene="mobile-bodycam-1"] .bc-measure{stroke:#dcebf1;stroke-width:2}[data-infographic-scene="mobile-bodycam-1"] .bc-pin{fill:var(--accent);stroke:#e8f2f6;stroke-width:2}
        [data-infographic-scene="mobile-bodycam-1"] .bc-chest-caption{display:flex;align-items:center;justify-content:center;gap:10px;padding:12px;border-top:1px solid rgb(220 235 242 / 17%);color:#e6f0f4;font-size:14px;line-height:1.4;text-align:center}[data-infographic-scene="mobile-bodycam-1"] .bc-chest-caption strong{font-weight:760}[data-infographic-scene="mobile-bodycam-1"] .bc-chest-caption span{color:var(--accent);font-size:18px;font-weight:800}
        @container sunflex-infographic (max-width:480px){[data-infographic-scene="mobile-bodycam-1"] .bc-chest-focus{padding:14px}[data-infographic-scene="mobile-bodycam-1"] .bc-chest-head{display:grid;gap:4px}[data-infographic-scene="mobile-bodycam-1"] .bc-chest-head .bc-copy{text-align:left}[data-infographic-scene="mobile-bodycam-1"] .bc-chest-focus svg{max-height:216px}[data-infographic-scene="mobile-bodycam-1"] .bc-chest-caption{gap:6px;font-size:14px}}
        """,
    )


def bodycam_review() -> str:
    return fragment(
        "mobile-bodycam-3",
        "촬영 기록에서 필요한 작업 구간을 선택해 다시 확인하는 영상 프레임과 시간 흐름",
        "찍은 기록에서, 필요한 작업 장면을 다시 확인",
        """
        <section class="bc-shell bc-record-screen"><div class="bc-screen-head"><span>촬영 기록</span><span>다시 확인</span></div><div class="bc-video-frame"><img alt="복구 전 검측 과정을 촬영하는 현장" height="432" src="/media/derived/product-mobile-bodycam-problem-768.webp" width="768"/><div class="bc-review-box"><strong>확인할 작업 구간</strong><span>촬영 장면을 다시 보기</span></div></div><div class="bc-control"><span class="bc-play" aria-hidden="true">▶</span><span>기록 영상</span><i></i><span>선택 구간</span></div></section>
        <section class="bc-record-flow"><p class="bc-label">촬영 기록에서 재확인까지</p><div class="bc-timeline"><div><strong>촬영</strong><span></span></div><i aria-hidden="true"></i><div class="bc-active"><strong>필요한 구간</strong><span></span></div><i aria-hidden="true"></i><div><strong>다시 확인</strong><span></span></div></div><p class="bc-copy">작업 중 남긴 장면에서 필요한 구간을 다시 살펴봅니다.</p></section>
        """,
        """
        [data-infographic-scene="mobile-bodycam-3"] .bc-record-screen{overflow:hidden;background:#172832}
        [data-infographic-scene="mobile-bodycam-3"] .bc-screen-head,[data-infographic-scene="mobile-bodycam-3"] .bc-control{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;color:#edf4f7;font-size:14px;font-weight:740}[data-infographic-scene="mobile-bodycam-3"] .bc-screen-head span:last-child{color:var(--accent)}
        [data-infographic-scene="mobile-bodycam-3"] .bc-video-frame{position:relative;overflow:hidden;border-block:1px solid rgb(225 239 244 / 18%);background:#14222b}[data-infographic-scene="mobile-bodycam-3"] .bc-video-frame img{display:block;width:100%;height:clamp(182px,45cqi,250px);object-fit:cover;object-position:center}
        [data-infographic-scene="mobile-bodycam-3"] .bc-review-box{position:absolute;top:18%;right:11%;display:grid;gap:4px;padding:10px 12px;border:2px solid var(--accent);border-radius:8px;background:rgb(15 27 34 / 84%);font-size:14px;line-height:1.35}[data-infographic-scene="mobile-bodycam-3"] .bc-review-box strong{color:#fff;font-weight:800}[data-infographic-scene="mobile-bodycam-3"] .bc-review-box span{color:#d8e5ea;font-weight:600}
        [data-infographic-scene="mobile-bodycam-3"] .bc-control{background:#1c303b}[data-infographic-scene="mobile-bodycam-3"] .bc-play{color:var(--accent);font-size:16px}[data-infographic-scene="mobile-bodycam-3"] .bc-control i{flex:1;height:6px;border-radius:999px;background:linear-gradient(90deg,#748893 0 35%,var(--accent) 35% 62%,#748893 62%)}[data-infographic-scene="mobile-bodycam-3"] .bc-control span:last-child{color:#d6e4e9}
        [data-infographic-scene="mobile-bodycam-3"] .bc-record-flow{display:grid;gap:14px;padding:16px;border:1px solid rgb(225 239 244 / 20%);border-radius:16px;background:rgb(37 55 66 / 82%)}
        [data-infographic-scene="mobile-bodycam-3"] .bc-timeline{display:grid;grid-template-columns:minmax(0,1fr) 22px minmax(0,1fr) 22px minmax(0,1fr);gap:7px;align-items:center}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline>div{display:grid;gap:8px;min-width:0;padding:11px 10px;border-radius:10px;background:#1c2d36;color:#e7f0f3;font-size:14px}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline strong{font-weight:760;white-space:nowrap}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline span{height:5px;border-radius:99px;background:#70838d}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline .bc-active{border:1px solid var(--accent);background:#2e4352}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline .bc-active span{background:var(--accent)}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline>i{height:2px;background:var(--accent);opacity:.8}
        @container sunflex-infographic (max-width:480px){[data-infographic-scene="mobile-bodycam-3"] .bc-video-frame img{height:182px}[data-infographic-scene="mobile-bodycam-3"] .bc-review-box{right:6%;top:14%}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline{grid-template-columns:1fr;gap:7px}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline>i{width:2px;height:12px;margin-left:20px}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline>div{grid-template-columns:120px 1fr;align-items:center}[data-infographic-scene="mobile-bodycam-3"] .bc-timeline strong{font-size:14px}}
        """,
    )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    states = data.get("mobile-bodycam")
    if not isinstance(states, list) or len(states) != 3:
        raise ValueError("Expected three mobile-bodycam infographic states")
    states[0] = bodycam_view()
    states[2] = bodycam_review()
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated mobile-bodycam infographic states 01 and 03.")


if __name__ == "__main__":
    main()
