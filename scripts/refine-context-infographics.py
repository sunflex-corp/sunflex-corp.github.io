#!/usr/bin/env python3
"""Replace four generic product diagrams with site-context infographics.

The script is intentionally idempotent: it only replaces the four named
benefit states and preserves every other entry in product-infographics.json.
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "product-infographics.json"
CAPTION = "기능을 설명한 구성 예시 · 실제 제품·설치 환경에 따라 달라질 수 있습니다"


def figure(scene: str, accent: str, aria: str, content: str, css: str) -> str:
    prefix = f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'
    shared = f"""
      {prefix} .ctx-board{{display:grid;gap:18px;padding:clamp(18px,3.4cqi,30px);border-radius:20px;background:linear-gradient(145deg,#18252d,#101820);color:#f3f7f8;box-shadow:inset 0 1px 0 rgb(255 255 255 / 8%)}}
      {prefix} .ctx-board *,{prefix} .ctx-board *::before,{prefix} .ctx-board *::after{{box-sizing:border-box}}
      {prefix} :is(.ctx-kicker,.ctx-title,.ctx-copy,.ctx-label){{margin:0!important}}
      {prefix} .ctx-kicker{{color:var(--accent)!important;font-size:14px;font-weight:780;letter-spacing:.04em;line-height:1.4}}
      {prefix} .ctx-title{{color:#f7fafb!important;font-size:clamp(22px,3.2cqi,31px);font-weight:780;letter-spacing:-.055em;line-height:1.28}}
      {prefix} .ctx-copy{{color:#d6e2e7!important;font-size:16px;font-weight:590;letter-spacing:-.025em;line-height:1.55}}
      {prefix} .ctx-label{{color:#e9f0f3!important;font-size:14px;font-weight:740;line-height:1.4}}
      {prefix} svg{{display:block;width:100%;height:auto}}
      {prefix} .ctx-board svg text{{stroke:none}}
      {prefix} :is(.ctx-map-bg,.ctx-cut-bg,.ctx-drone-bg),{prefix} .ctx-crane svg>rect:first-of-type{{stroke:none}}
      @container sunflex-infographic (max-width:480px){{{prefix} .ctx-board{{gap:14px;padding:18px;border-radius:16px}}{prefix} .ctx-title{{font-size:24px}}}}
    """
    styles = dedent(shared + "\n" + css).strip()
    return (
        f'<figure class="benefit-visual infographic-visual" data-infographic-version="20260922" '
        f'data-visual-kind="diagram"><div aria-label="{aria}" class="sunflex-infographic" '
        f'data-infographic-scene="{scene}" role="group" style="--accent:{accent}">'
        f'<style>{styles}</style><div class="visual-shell"><div class="diagram ctx-diagram" '
        f'role="group"><div class="ctx-board">{dedent(content).strip()}</div></div></div></div>'
        f'<figcaption>{CAPTION}</figcaption></figure>'
    )


def crane() -> str:
    scene = "iot-small-tower-crane-1"
    return figure(
        scene, "#d9bc7b", "타워크레인 상부 풍속계와 훅 인양 센서의 장착 위치를 보여주는 도해",
        """
        <header><p class="ctx-kicker">장착 위치 구성</p><h4 class="ctx-title">상부 풍속과 훅의 인양 정보를 함께</h4></header>
        <section class="ctx-crane" aria-label="크레인 장착점"><svg role="img" viewBox="0 -28 620 294"><defs><linearGradient id="ctx-crane-metal" x1="0" x2="1"><stop stop-color="#8ea3aa"/><stop offset="1" stop-color="#40545d"/></linearGradient><linearGradient id="ctx-crane-sky" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#22333c"/><stop offset="1" stop-color="#16232b"/></linearGradient></defs><rect fill="url(#ctx-crane-sky)" height="238" rx="16" width="620" y="6"/><path class="ctx-crane-ground" d="M35 220H586"/><path class="ctx-crane-mast" d="M164 217 192 50 220 217Z"/><path class="ctx-crane-jib" d="M192 53 506 53 506 67 192 67Z"/><path class="ctx-crane-brace" d="M192 53 281 15 355 53M281 15v38M281 15 422 53M220 218 192 53M164 217 192 53"/><path class="ctx-crane-cable" d="M441 67v109"/><path class="ctx-crane-hook" d="M428 174v25c0 18 27 18 27 0v-7"/><rect class="ctx-crane-load" height="31" rx="5" width="62" x="409" y="205"/><g class="ctx-anemometer"><path d="M281 15V1M267 7h28M276 1c-10-14-20 0-4 7M288 1c10-14 20 0 4 7"/></g><g class="ctx-hook-sensor"><rect height="19" rx="4" width="28" x="427" y="150"/><circle cx="441" cy="159" r="4"/></g><g class="ctx-callout"><circle cx="326" cy="18" r="22"/><text x="326" y="28">1</text><path d="M304 18 284 10"/><circle cx="489" cy="151" r="22"/><text x="489" y="161">2</text><path d="M467 151h-21"/></g></svg></section>
        <ol class="ctx-callout-list" aria-label="장착점 설명"><li><span>01</span><div><strong>상부 풍속계</strong><small>풍속</small></div></li><li><span>02</span><div><strong>훅 인양 센서</strong><small>하중·훅 거리</small></div></li></ol>
        """,
        f"""
        {f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-crane{{overflow:hidden;border:1px solid rgb(226 239 242 / 20%);border-radius:16px;background:#16242c}}
        {f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-crane svg{{min-height:0}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} :is(.ctx-crane-ground,.ctx-crane-mast,.ctx-crane-jib,.ctx-crane-brace,.ctx-crane-cable,.ctx-crane-hook){{fill:none;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-crane-ground{{stroke:#637982;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} :is(.ctx-crane-mast,.ctx-crane-jib){{fill:url(#ctx-crane-metal);stroke:#c4d3d8;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-crane-brace{{stroke:#8ca3ab;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-crane-cable{{stroke:#d2ba8c;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-crane-hook{{stroke:#dfc58e;stroke-width:7}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-crane-load{{fill:#465c65;stroke:#bdcdd1;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-anemometer{{fill:none;stroke:#f2d89f;stroke-linecap:round;stroke-width:3;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-hook-sensor rect{{fill:#dbbd7a;stroke:#fff1ca;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-hook-sensor circle{{fill:#20313a}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout circle{{fill:var(--accent);stroke:#fff2cf;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout text{{fill:#16232b;font-family:inherit;font-size:28px;font-weight:850;text-anchor:middle}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout path{{fill:none;stroke:var(--accent);stroke-width:2;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout-list{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0!important;padding:0!important;list-style:none}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout-list li{{display:flex;align-items:center;gap:10px;min-width:0;padding:12px;border:1px solid rgb(220 234 238 / 16%);border-radius:12px;background:rgb(255 255 255 / 4%)}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout-list span{{color:var(--accent);font-size:13px;font-weight:800}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout-list div{{display:grid;gap:2px}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout-list strong{{color:#f4f7f8;font-size:14px}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout-list small{{color:#cbd8dc;font-size:14px}}@container sunflex-infographic (max-width:480px){{{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-callout-list{{grid-template-columns:1fr}}}}
        """,
    )


def curing() -> str:
    scene = "concrete-curing-1"
    return figure(
        scene, "#bdd1a5", "콘크리트 타설 단면 안에 삽입한 온도 프로브와 위치별 기록점을 보여주는 도해",
        """
        <header><p class="ctx-kicker">타설 단면 구성</p><h4 class="ctx-title">단면 안의 온도를, 위치별로 기록</h4></header>
        <section class="ctx-cutaway" aria-label="콘크리트 단면과 온도 프로브"><svg role="img" viewBox="0 0 620 280"><defs><linearGradient id="ctx-concrete-face" x1="0" x2="1"><stop stop-color="#88928d"/><stop offset="1" stop-color="#59645f"/></linearGradient><pattern height="16" id="ctx-concrete-grain" patternUnits="userSpaceOnUse" width="16"><circle cx="3" cy="4" fill="#dce4dc" opacity=".23" r="1.5"/><circle cx="12" cy="10" fill="#24312d" opacity=".18" r="1.2"/></pattern></defs><rect class="ctx-cut-bg" height="244" rx="16" width="620" y="6"/><path class="ctx-cut-shadow" d="M80 222 154 241H552l-76-20Z"/><path class="ctx-concrete" d="M87 68 145 38H540l-58 30v145H87Z"/><path class="ctx-concrete-side" d="M482 68 540 38v145l-58 30Z"/><path class="ctx-concrete-top" d="m87 68 58-30h395l-58 30Z"/><rect class="ctx-grain" height="145" width="395" x="87" y="68"/><path class="ctx-probe" d="M252 34v148"/><circle class="ctx-probe-tip" cx="252" cy="184" r="8"/><path class="ctx-depth" d="M225 68v116M215 68h20M215 184h20"/><path class="ctx-depth-line" d="M215 68h-55M215 184h-55"/><g class="ctx-record"><circle cx="350" cy="126" r="10"/><circle cx="420" cy="165" r="10"/><path d="M350 109v-18M420 148v-18"/></g><g class="ctx-note"><rect height="40" rx="8" width="130" x="100" y="97"/><text x="165" y="126">삽입 깊이</text><rect height="40" rx="8" width="120" x="430" y="84"/><text x="490" y="113">기록점</text></g></svg></section>
        <div class="ctx-legend"><span><i class="ctx-probe-key"></i>내부 온도 프로브</span><span><i class="ctx-section-key"></i>타설 단면</span></div>
        """,
        f"""
        {f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-cutaway{{overflow:hidden;border:1px solid rgb(230 239 226 / 17%);border-radius:16px;background:#1a2522}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-cutaway svg{{min-height:0}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-cut-bg{{fill:#1a2522}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-cut-shadow{{fill:#08110f;opacity:.45}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-concrete{{fill:url(#ctx-concrete-face);stroke:#d2dbd2;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-concrete-side{{fill:#4e5953;stroke:#c7d1c7;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-concrete-top{{fill:#a8b0a7;stroke:#dce4db;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-grain{{fill:url(#ctx-concrete-grain);opacity:.75}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-probe{{fill:none;stroke:#d7edc0;stroke-width:8;stroke-linecap:round;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-probe-tip{{fill:var(--accent);stroke:#f3ffe7;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} :is(.ctx-depth,.ctx-depth-line){{fill:none;stroke:#dce8db;stroke-width:1.6;stroke-dasharray:3 3;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-record circle{{fill:#d9efc5;stroke:#fff;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-record path{{stroke:#d9efc5;stroke-width:2;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-note rect{{fill:#17231f;stroke:#bcd0b5;stroke-width:1}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-note text{{fill:#e5efe2;font-family:inherit;font-size:28px;font-weight:740;text-anchor:middle}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-legend{{display:flex;flex-wrap:wrap;gap:10px}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-legend span{{display:inline-flex;align-items:center;gap:8px;padding:10px 12px;border:1px solid rgb(220 235 215 / 17%);border-radius:999px;color:#edf4ea;font-size:14px;font-weight:700}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-legend i{{display:block;width:18px;height:10px}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-probe-key{{border-radius:999px;background:#d7edc0}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-section-key{{border:1px solid #d3dcd1;border-radius:2px;background:#78837b}}
        """,
    )


def emergency_location() -> str:
    scene = "emergency-signal-location-2"
    return figure(
        scene, "#e1adb5", "안전모 호출이 작업 통로와 출입구를 기준으로 수신 담당자에게 전달되는 위치 안내 도해",
        """
        <header><p class="ctx-kicker">현장 기준 위치</p><h4 class="ctx-title">호출과 함께, 어디인지도</h4></header>
        <section class="ctx-location-plan" aria-label="통로와 출입구를 기준으로 한 호출 위치"><svg role="img" viewBox="0 0 620 258"><defs><marker id="ctx-location-arrow" markerHeight="8" markerWidth="8" orient="auto" refX="7" refY="4"><path d="M0 0 8 4 0 8Z" fill="#e1adb5"/></marker></defs><rect class="ctx-map-bg" height="232" rx="16" width="620" y="8"/><path class="ctx-map-corridor" d="M72 92h315v76H72Z"/><path class="ctx-map-branch" d="M243 46v46M243 168v42"/><path class="ctx-map-entry" d="M72 92V59h63v33M72 168v33h63v-33"/><path class="ctx-map-lines" d="M135 59h50M135 201h50M387 92h74v76h-74"/><g class="ctx-helmet"><path d="M202 133c0-17 13-29 30-29 16 0 29 12 29 29v8h-59Z"/><path d="M196 141h71"/><circle cx="231" cy="122" r="5"/></g><g class="ctx-pin"><path d="M232 160c-12-13-18-22-18-31a18 18 0 1 1 36 0c0 9-6 18-18 31Z"/><circle cx="232" cy="128" r="5"/></g><path class="ctx-send" d="M263 128h185" marker-end="url(#ctx-location-arrow)"/><g class="ctx-manager"><rect height="98" rx="11" width="104" x="461" y="79"/><path d="M482 105h62M482 128h45M482 151h31"/><circle cx="539" cy="151" r="8"/></g><g class="ctx-map-text"><text x="104" y="50">출입구</text><text x="266" y="84">작업 통로</text><text x="513" y="66">수신 담당자</text><text x="264" y="190">호출 위치</text></g></svg></section>
        <div class="ctx-location-flow"><strong>안전모 호출</strong><i aria-hidden="true">→</i><strong>통로·출입구 기준</strong><i aria-hidden="true">→</i><strong>위치 문자 확인</strong></div>
        """,
        f"""
        {f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-location-plan{{overflow:hidden;border:1px solid rgb(247 226 229 / 20%);border-radius:16px;background:#1d272c}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-location-plan svg{{min-height:0}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-map-bg{{fill:#1d272c}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} :is(.ctx-map-corridor,.ctx-map-branch,.ctx-map-entry,.ctx-map-lines){{fill:none;stroke-linejoin:round;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-map-corridor{{fill:#34444a;stroke:#9bafb2;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-map-branch{{stroke:#72868d;stroke-width:20}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-map-entry{{stroke:#e1adb5;stroke-width:4}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-map-lines{{stroke:#61767d;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-helmet{{fill:#d7e4e5;stroke:#fbffff;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-pin{{fill:#e1adb5;stroke:#fff1f2;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-send{{fill:none;stroke:#e1adb5;stroke-width:3;stroke-dasharray:6 6;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-manager rect{{fill:#2c3e46;stroke:#d6e5e6;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-manager path{{stroke:#d6e5e6;stroke-width:2;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-manager circle{{fill:#e1adb5}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-map-text text{{fill:#edf4f4;font-family:inherit;font-size:28px;font-weight:740;text-anchor:middle}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-location-flow{{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:9px;padding:12px;border-top:1px solid rgb(239 222 225 / 15%);color:#edf4f4;font-size:14px;text-align:center}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-location-flow strong{{font-weight:760}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-location-flow i{{color:var(--accent);font-size:19px;font-style:normal;font-weight:800}}
        """,
    )


def drone_location() -> str:
    scene = "ai-drone-inspection-2"
    return figure(
        scene, "#b8d7c2", "드론의 촬영 방향과 구조물 면, 기록 위치를 보여주는 점검 도해",
        """
        <header><p class="ctx-kicker">촬영 장면과 위치 기록</p><h4 class="ctx-title">촬영 방향과 기록 위치를 함께</h4></header>
        <section class="ctx-drone-plan" aria-label="드론 촬영 방향과 구조물 기록 위치"><svg role="img" viewBox="0 0 620 266"><defs><marker id="ctx-drone-arrow" markerHeight="8" markerWidth="8" orient="auto" refX="7" refY="4"><path d="M0 0 8 4 0 8Z" fill="#b8d7c2"/></marker></defs><rect class="ctx-drone-bg" height="242" rx="16" width="620" y="8"/><g class="ctx-facade"><rect height="164" rx="8" width="222" x="342" y="34"/><path d="M379 34v164M416 34v164M453 34v164M490 34v164M527 34v164M342 79h222M342 125h222M342 171h222"/></g><path class="ctx-target-plane" d="M342 58 300 76v99l42 18"/><g class="ctx-drone"><path d="M132 116h78M171 78v76M142 89l58 56M200 89l-58 56"/><circle cx="132" cy="116" r="10"/><circle cx="210" cy="116" r="10"/><circle cx="171" cy="78" r="10"/><circle cx="171" cy="154" r="10"/><rect height="24" rx="6" width="34" x="154" y="104"/></g><path class="ctx-flight" d="M222 116h103" marker-end="url(#ctx-drone-arrow)"/><g class="ctx-record-pin"><path d="M452 153c-13-14-19-24-19-34a19 19 0 1 1 38 0c0 10-6 20-19 34Z"/><circle cx="452" cy="118" r="5"/></g><g class="ctx-drone-text"><text x="171" y="190">촬영 방향</text><text x="453" y="240">구조물 면 · 기록 위치</text></g></svg></section>
        <div class="ctx-drone-flow"><span>촬영 방향</span><i aria-hidden="true">→</i><span>구조물 면</span><i aria-hidden="true">→</i><span>사진과 위치 기록</span></div>
        """,
        f"""
        {f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-drone-plan{{overflow:hidden;border:1px solid rgb(225 241 229 / 18%);border-radius:16px;background:#172521}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-drone-plan svg{{min-height:0}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-drone-bg{{fill:#172521}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-facade rect{{fill:#354b44;stroke:#d4e7da;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-facade path{{fill:none;stroke:#739086;stroke-width:1.6;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-target-plane{{fill:#b8d7c2;fill-opacity:.14;stroke:#b8d7c2;stroke-width:2;stroke-dasharray:5 5;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-drone :is(path,circle,rect){{fill:#cfe4d5;stroke:#f0fff4;stroke-width:2;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-drone path{{fill:none;stroke:#cfe4d5;stroke-width:3}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-flight{{fill:none;stroke:#b8d7c2;stroke-width:3;stroke-dasharray:6 6;vector-effect:non-scaling-stroke}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-record-pin{{fill:#b8d7c2;stroke:#f2fff5;stroke-width:2}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-drone-text text{{fill:#ebf5ee;font-family:inherit;font-size:28px;font-weight:740;text-anchor:middle}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-drone-flow{{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:9px;padding:12px;border-top:1px solid rgb(226 241 231 / 16%);color:#edf6f0;font-size:14px;font-weight:760;text-align:center}}{f'.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="{scene}"]'} .ctx-drone-flow i{{color:var(--accent);font-size:19px;font-style:normal;font-weight:800}}
        """,
    )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    replacements = {
        ("iot-small-tower-crane", 0): crane(),
        ("concrete-curing", 0): curing(),
        ("emergency-signal-location", 1): emergency_location(),
        ("ai-drone-inspection", 1): drone_location(),
    }
    for (slug, index), markup in replacements.items():
        states = data.get(slug)
        if not isinstance(states, list) or len(states) != 3:
            raise ValueError(f"Expected three infographic states for {slug}")
        states[index] = markup
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated four context-specific infographic states.")


if __name__ == "__main__":
    main()
