#!/usr/bin/env python3
"""Replace five reviewed infographic examples without changing product copy.

Run this script only after the surrounding infographic stylesheet is in place:
    python3 scripts/refine-infographic-examples.py
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "product-infographics.json"
CAPTION = "기능을 설명한 구성 예시 · 실제 제품·설치 환경에 따라 달라질 수 있습니다"


def figure(scene: str, aria: str, accent: str, title: str, content: str, scene_css: str) -> str:
    """Return a self-contained, container-responsive HTML infographic."""
    shared_css = """
      [data-infographic-scene=\"SCENE\"] .rf-board{box-sizing:border-box;display:grid;gap:16px;padding:clamp(16px,2.8cqi,26px);border:1px solid color-mix(in srgb,var(--accent) 36%,#ffffff);border-radius:22px;background:linear-gradient(145deg,#17242d,#101a21);color:#f7fafb;box-shadow:inset 0 1px 0 rgb(255 255 255 / 9%),0 20px 45px rgb(0 0 0 / 18%)}
      [data-infographic-scene=\"SCENE\"] .rf-board *,[data-infographic-scene=\"SCENE\"] .rf-board *::before,[data-infographic-scene=\"SCENE\"] .rf-board *::after{box-sizing:border-box}
      [data-infographic-scene=\"SCENE\"] .rf-title,[data-infographic-scene=\"SCENE\"] .rf-label,[data-infographic-scene=\"SCENE\"] .rf-copy{margin:0;line-height:1.4}
      [data-infographic-scene=\"SCENE\"] .rf-title{font-size:clamp(20px,2.4cqi,30px);font-weight:760;letter-spacing:-.045em}
      [data-infographic-scene=\"SCENE\"] .rf-label{color:var(--accent);font-size:16px;font-weight:720;letter-spacing:-.025em}
      [data-infographic-scene=\"SCENE\"] .rf-copy{color:#dce6e9;font-size:16px;font-weight:580;letter-spacing:-.025em}
      [data-infographic-scene=\"SCENE\"] .rf-card{min-width:0;padding:14px;border:1px solid rgb(231 242 245 / 23%);border-radius:16px;background:rgb(38 57 68 / 88%)}
      [data-infographic-scene=\"SCENE\"] .rf-arrow{align-self:center;color:var(--accent);font-size:24px;font-weight:800;line-height:1;text-align:center}
      @container sunflex-infographic (max-width:480px){[data-infographic-scene=\"SCENE\"] .rf-board{padding:16px;gap:14px}[data-infographic-scene=\"SCENE\"] .rf-title{font-size:23px}[data-infographic-scene=\"SCENE\"] .rf-arrow{transform:rotate(90deg);padding:0}}
    """.replace("SCENE", scene)
    css = dedent(shared_css + "\n" + scene_css).strip()
    return (
        f'<figure class="benefit-visual infographic-visual" data-infographic-version="20260922" '
        f'data-visual-kind="diagram"><div aria-label="{aria}" class="sunflex-infographic" '
        f'data-infographic-scene="{scene}" role="group" style="--accent:{accent}"><style>{css}'
        f'</style><div class="visual-shell"><div aria-label="{aria}" class="diagram rf-diagram" role="group">'
        f'<div class="rf-board"><h4 class="rf-title">{title}</h4>{dedent(content).strip()}'
        f'</div></div></div></div><figcaption>{CAPTION}</figcaption></figure>'
    )


def risk_review() -> str:
    return figure(
        "ai-risk-assessment-review-1",
        "작성한 평가와 표준 위험요인을 대조해 담당자가 추가 검토할 내용을 확인하는 흐름",
        "#c6b0db",
        "작성한 평가를, 같은 기준으로 다시 대조",
        """
        <div class="rf-risk-flow">
          <section class="rf-card"><p class="rf-label">작성한 위험성평가</p><div class="rf-risk-list"><span>작업 내용</span><span>위험요인</span><span>개선대책</span></div></section>
          <div class="rf-arrow" aria-hidden="true">→</div>
          <section class="rf-card rf-risk-check"><p class="rf-label">공종별 기준과 대조</p><p class="rf-copy">빠진 위험요인과 보완할 대책을 살펴봅니다.</p><div class="rf-review-mark">담당자 확인</div></section>
        </div>
        """,
        """
        [data-infographic-scene="ai-risk-assessment-review-1"] .rf-risk-flow{display:grid;grid-template-columns:minmax(0,1fr) 34px minmax(0,1fr);gap:14px;align-items:stretch}
        [data-infographic-scene="ai-risk-assessment-review-1"] .rf-risk-list{display:grid;gap:9px;margin-top:16px}
        [data-infographic-scene="ai-risk-assessment-review-1"] .rf-risk-list span{padding:10px 12px;border-radius:9px;background:#192933;color:#f4f8fa;font-size:16px;font-weight:650}
        [data-infographic-scene="ai-risk-assessment-review-1"] .rf-risk-check{display:grid;gap:14px;align-content:start;background:linear-gradient(145deg,#372c43,#263544)}
        [data-infographic-scene="ai-risk-assessment-review-1"] .rf-review-mark{padding:10px 12px;border-radius:999px;background:var(--accent);color:#211f27;font-size:16px;font-weight:800;text-align:center}
        @container sunflex-infographic (max-width:480px){[data-infographic-scene="ai-risk-assessment-review-1"] .rf-risk-flow{grid-template-columns:1fr}[data-infographic-scene="ai-risk-assessment-review-1"] .rf-arrow{height:20px}}
        """,
    )


def quick_risk_assessment() -> str:
    return figure(
        "ai-quick-risk-assessment-1",
        "현장 사진에서 작업 구역을 선택하고 작업 설명을 더해 위험성평가 초안을 시작하는 흐름",
        "#bca5d9",
        "현장 사진에서, 평가할 작업을 분명하게",
        """
        <section class="rf-quick-photo"><div class="rf-photo-head"><span>현장 사진</span><span>선택 범위</span></div><img alt="수로 공사 현장의 작업 구역을 확인하는 담당자" src="/media/derived/product-ai-quick-risk-assessment-scene-768.webp"/><div class="rf-photo-focus"><strong>작업 구역</strong><span>사진에서 선택</span></div></section>
        <section class="rf-card rf-quick-next"><p class="rf-label">작업 설명을 함께 입력</p><div><strong>사진과 작업 설명</strong><span aria-hidden="true">→</span><strong>위험성평가 초안</strong></div><p class="rf-copy">담당자가 실제 작업 조건과 대조해 보완합니다.</p></section>
        """,
        """
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-photo{position:relative;overflow:hidden;min-height:178px;border:1px solid rgb(231 242 245 / 28%);border-radius:16px;background:#18252e}
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-photo img{display:block;width:100%;height:178px;object-fit:cover;object-position:center;color:transparent;filter:saturate(.78) contrast(1.06)}
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-photo-head{position:absolute;z-index:2;top:0;right:0;left:0;display:flex;justify-content:space-between;gap:12px;padding:11px 14px;background:linear-gradient(180deg,rgb(14 24 30 / 86%),transparent);color:#f4f8fa;font-size:16px;font-weight:730}
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-photo-head span:last-child{color:var(--accent)}
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-photo-focus{position:absolute;left:11%;bottom:15%;display:grid;gap:3px;padding:9px 11px;border:2px solid var(--accent);border-radius:8px;background:rgb(19 29 36 / 83%);color:#fff;font-size:16px;line-height:1.25}
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-photo-focus::before{position:absolute;right:-10%;bottom:-28%;width:30%;height:36%;border-right:2px solid var(--accent);border-bottom:2px solid var(--accent);content:""}
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-photo-focus strong{font-weight:800}[data-infographic-scene="ai-quick-risk-assessment-1"] .rf-photo-focus span{color:#e5dff0;font-weight:630}
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-next{display:grid;gap:12px;background:linear-gradient(145deg,#372e43,#263441)}
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-next>div{display:grid;grid-template-columns:minmax(0,1fr) 26px minmax(0,1fr);gap:8px;align-items:center;color:#f5f8fa;font-size:16px;line-height:1.35}
        [data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-next strong{font-weight:760}[data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-next span{color:var(--accent);font-size:22px;font-weight:800;text-align:center}
        @container sunflex-infographic (max-width:480px){[data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-photo,[data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-photo img{min-height:154px;height:154px}[data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-next>div{grid-template-columns:1fr}[data-infographic-scene="ai-quick-risk-assessment-1"] .rf-quick-next span{transform:rotate(90deg)}}
        """,
    )


def safety_index() -> str:
    return figure(
        "ai-safety-index-1",
        "여러 현장의 안전 자료를 같은 기준으로 비교해 먼저 살펴볼 현장을 확인하는 흐름",
        "#baa2bf",
        "여러 현장 자료를, 같은 기준으로 비교",
        """
        <div class="rf-index-flow">
          <section class="rf-card"><p class="rf-label">공통 입력 자료</p><div class="rf-source-tags"><span>CCTV 영상</span><span>위험성평가</span><span>출역·기상</span></div></section>
          <div class="rf-arrow" aria-hidden="true">→</div>
          <section class="rf-card rf-index-result"><p class="rf-label">현장별 안전지수</p><div class="rf-site-lines"><div><b>현장 A</b><i></i><span>비교</span></div><div><b>현장 B</b><i></i><span>비교</span></div><div><b>현장 C</b><i></i><span>비교</span></div></div><p class="rf-copy">먼저 살펴볼 현장을 확인합니다.</p></section>
        </div>
        """,
        """
        [data-infographic-scene="ai-safety-index-1"] .rf-index-flow{display:grid;grid-template-columns:minmax(0,.9fr) 34px minmax(0,1.1fr);gap:14px;align-items:stretch}
        [data-infographic-scene="ai-safety-index-1"] .rf-source-tags{display:grid;gap:9px;margin-top:16px}
        [data-infographic-scene="ai-safety-index-1"] .rf-source-tags span{padding:10px 12px;border-left:3px solid var(--accent);border-radius:7px;background:#192933;color:#f4f8fa;font-size:16px;font-weight:650}
        [data-infographic-scene="ai-safety-index-1"] .rf-index-result{display:grid;gap:14px;background:linear-gradient(145deg,#342b38,#28333f)}
        [data-infographic-scene="ai-safety-index-1"] .rf-site-lines{display:grid;gap:10px}
        [data-infographic-scene="ai-safety-index-1"] .rf-site-lines div{display:grid;grid-template-columns:58px minmax(48px,1fr) 34px;gap:9px;align-items:center;color:#eef4f6;font-size:16px}
        [data-infographic-scene="ai-safety-index-1"] .rf-site-lines b{font-weight:720}[data-infographic-scene="ai-safety-index-1"] .rf-site-lines i{height:8px;border-radius:999px;background:linear-gradient(90deg,var(--accent),rgb(255 255 255 / 16%))}[data-infographic-scene="ai-safety-index-1"] .rf-site-lines span{color:#dce6e9;font-weight:650}
        @container sunflex-infographic (max-width:480px){[data-infographic-scene="ai-safety-index-1"] .rf-index-flow{grid-template-columns:1fr}[data-infographic-scene="ai-safety-index-1"] .rf-arrow{height:20px}}
        """,
    )


def subcontractor_safety() -> str:
    return figure(
        "ai-subcontractor-safety-1",
        "협력업체별 작업 계획과 위험성평가를 같은 항목으로 한곳에서 확인하는 구성",
        "#c8b89a",
        "업체별 계획을, 같은 항목으로 한곳에서",
        """
        <section class="rf-card rf-partner-table"><div class="rf-partner-head"><span>협력업체</span><span>작업 계획</span><span>위험성평가</span></div><div class="rf-partner-row"><b>A사</b><span>당일 작업</span><span>확인 자료</span></div><div class="rf-partner-row"><b>B사</b><span>당일 작업</span><span>확인 자료</span></div><div class="rf-partner-row"><b>C사</b><span>당일 작업</span><span>확인 자료</span></div></section>
        <div class="rf-share-band"><strong>한 화면에서 대조</strong><span>업체별 현황을 같은 기준으로 살펴봅니다.</span></div>
        """,
        """
        [data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-table{display:grid;gap:8px;padding:14px;background:linear-gradient(145deg,#283234,#1a272c)}
        [data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-head,[data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-row{display:grid;grid-template-columns:76px minmax(0,1fr) minmax(0,1fr);gap:9px;align-items:center}
        [data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-head{padding:5px 8px;color:var(--accent);font-size:16px;font-weight:800}
        [data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-row{padding:12px 8px;border-radius:10px;background:#20343d;color:#e9f0f2;font-size:16px;font-weight:620}
        [data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-row b{color:#fff;font-weight:800}[data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-row span{min-width:0;padding-left:10px;border-left:1px solid rgb(231 242 245 / 22%)}
        [data-infographic-scene="ai-subcontractor-safety-1"] .rf-share-band{display:flex;gap:12px;align-items:center;justify-content:space-between;padding:14px 16px;border:1px solid color-mix(in srgb,var(--accent) 52%,#ffffff);border-radius:14px;background:rgb(200 184 154 / 13%);color:#e9f0f2;font-size:16px;line-height:1.4}
        [data-infographic-scene="ai-subcontractor-safety-1"] .rf-share-band strong{color:var(--accent);font-weight:800;white-space:nowrap}
        @container sunflex-infographic (max-width:480px){[data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-head{display:none}[data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-row{grid-template-columns:48px 1fr;gap:8px}[data-infographic-scene="ai-subcontractor-safety-1"] .rf-partner-row span:last-child{grid-column:2}[data-infographic-scene="ai-subcontractor-safety-1"] .rf-share-band{align-items:flex-start;flex-direction:column}}
        """,
    )


def inspectcut() -> str:
    return figure(
        "inspectcut-2",
        "선택한 검측 구간에 자막과 시간 정보를 더해 제출 화면을 만드는 흐름",
        "#adb7d4",
        "선택한 장면에, 시간과 설명을 함께",
        """
        <section class="rf-cut-screen"><div class="rf-screen-head"><span>촬영 원본</span><span>선택 장면</span></div><div class="rf-site-view"><i class="rf-column"></i><i class="rf-slab"></i><div class="rf-focus"><b>검측 자막</b><span>확인할 위치</span></div></div><div class="rf-time-row"><strong>시간 정보</strong><span>선택 구간에 함께 표시</span></div></section>
        <section class="rf-card rf-cut-timeline"><p class="rf-label">제출할 구간 선택</p><div><span></span><b></b><span></span></div><p class="rf-copy">원본은 보관하고, 선택한 구간만 제출 화면으로 정리합니다.</p></section>
        """,
        """
        [data-infographic-scene="inspectcut-2"] .rf-cut-screen{overflow:hidden;border:1px solid rgb(231 242 245 / 28%);border-radius:16px;background:#18252e}
        [data-infographic-scene="inspectcut-2"] .rf-screen-head,[data-infographic-scene="inspectcut-2"] .rf-time-row{display:flex;justify-content:space-between;gap:12px;padding:11px 14px;color:#edf4f6;font-size:16px;font-weight:720}
        [data-infographic-scene="inspectcut-2"] .rf-screen-head span:last-child{color:var(--accent)}[data-infographic-scene="inspectcut-2"] .rf-site-view{position:relative;min-height:132px;overflow:hidden;border-block:1px solid rgb(231 242 245 / 16%);background:linear-gradient(148deg,#455861 0 28%,#263946 28% 66%,#15242d 66%)}
        [data-infographic-scene="inspectcut-2"] .rf-column{position:absolute;left:16%;bottom:0;width:15%;height:76%;border:5px solid #b4c2c7;border-bottom:0;background:#647980;box-shadow:inset 8px 0 #7f969d}
        [data-infographic-scene="inspectcut-2"] .rf-slab{position:absolute;right:0;bottom:18%;width:63%;height:20%;transform:skewY(-12deg);border-block:4px solid #bbcbcf;background:#71878e}
        [data-infographic-scene="inspectcut-2"] .rf-focus{position:absolute;right:13%;top:20%;display:grid;gap:4px;padding:10px 12px;border:2px solid var(--accent);border-radius:8px;background:rgb(18 29 36 / 78%);color:#fff;font-size:16px;line-height:1.25}[data-infographic-scene="inspectcut-2"] .rf-focus b{font-weight:800}[data-infographic-scene="inspectcut-2"] .rf-focus span{color:#e1e9ec;font-weight:600}
        [data-infographic-scene="inspectcut-2"] .rf-time-row{background:#1d2e38}[data-infographic-scene="inspectcut-2"] .rf-time-row span{color:#dbe5e8;font-weight:620}
        [data-infographic-scene="inspectcut-2"] .rf-cut-timeline{display:grid;gap:12px;background:#21303a}[data-infographic-scene="inspectcut-2"] .rf-cut-timeline>div{display:grid;grid-template-columns:1fr .72fr 1fr;gap:5px;height:12px}[data-infographic-scene="inspectcut-2"] .rf-cut-timeline span,[data-infographic-scene="inspectcut-2"] .rf-cut-timeline b{border-radius:999px;background:#647780}[data-infographic-scene="inspectcut-2"] .rf-cut-timeline b{background:var(--accent);box-shadow:0 0 0 4px rgb(173 183 212 / 18%)}
        @container sunflex-infographic (max-width:480px){[data-infographic-scene="inspectcut-2"] .rf-screen-head,[data-infographic-scene="inspectcut-2"] .rf-time-row{align-items:flex-start;flex-direction:column}[data-infographic-scene="inspectcut-2"] .rf-focus{right:7%;top:16%}}
        """,
    )


def similar_accident() -> str:
    return figure(
        "ai-similar-accident-alert-2",
        "오늘 작업의 공종과 위험요인을 유사 사고사례와 연결해 작업 전 확인 자료로 활용하는 흐름",
        "#c9b18b",
        "오늘 작업과 닮은 사례를, 공통 위험으로 연결",
        """
        <div class="rf-accident-rows"><section class="rf-route-row"><p class="rf-label">오늘의 작업</p><strong>공종 · 위험요인</strong><span>위험성평가와 TBM 자료</span></section><section class="rf-route-row rf-risk-link"><p class="rf-label">공통 위험요소</p><strong>공종 · 작업 내용 · 위험요인</strong><span>관련 기준으로 연결</span></section><section class="rf-route-row"><p class="rf-label">유사 사고사례</p><strong>작업 전 확인 자료</strong><span>관련 사례를 함께 살펴봅니다.</span></section></div>
        """,
        """
        [data-infographic-scene="ai-similar-accident-alert-2"] .rf-board{min-height:320px;align-content:space-between}
        [data-infographic-scene="ai-similar-accident-alert-2"] .rf-accident-rows{display:grid;gap:16px}
        [data-infographic-scene="ai-similar-accident-alert-2"] .rf-route-row{position:relative;display:grid;grid-template-columns:124px minmax(0,1fr) minmax(0,.78fr);gap:14px;align-items:center;min-height:60px;padding:12px 14px;border:1px solid rgb(231 242 245 / 23%);border-radius:14px;background:#24333c}
        [data-infographic-scene="ai-similar-accident-alert-2"] .rf-route-row:not(:last-child)::after{position:absolute;z-index:2;bottom:-18px;left:50%;width:2px;height:18px;background:var(--accent);content:""}
        [data-infographic-scene="ai-similar-accident-alert-2"] .rf-route-row:not(:last-child)::before{position:absolute;z-index:2;bottom:-21px;left:calc(50% - 3px);border-top:6px solid var(--accent);border-right:4px solid transparent;border-left:4px solid transparent;content:""}
        [data-infographic-scene="ai-similar-accident-alert-2"] .rf-route-row strong{color:#fff;font-size:18px;font-weight:790;letter-spacing:-.04em;line-height:1.35}
        [data-infographic-scene="ai-similar-accident-alert-2"] .rf-route-row>span{color:#dce6e9;font-size:16px;font-weight:620;line-height:1.35}
        [data-infographic-scene="ai-similar-accident-alert-2"] .rf-risk-link{border-color:color-mix(in srgb,var(--accent) 66%,#ffffff)!important;background:linear-gradient(145deg,#453c2c,#29333a)!important}
        @container sunflex-infographic (max-width:480px){[data-infographic-scene="ai-similar-accident-alert-2"] .rf-board{min-height:0}[data-infographic-scene="ai-similar-accident-alert-2"] .rf-route-row{grid-template-columns:1fr;gap:5px;padding:14px}[data-infographic-scene="ai-similar-accident-alert-2"] .rf-route-row:not(:last-child)::after{left:24px}}
        """,
    )


REPLACEMENTS = {
    ("ai-quick-risk-assessment", 0): quick_risk_assessment(),
    ("ai-risk-assessment-review", 0): risk_review(),
    ("ai-safety-index", 0): safety_index(),
    ("ai-subcontractor-safety", 0): subcontractor_safety(),
    ("inspectcut", 1): inspectcut(),
    ("ai-similar-accident-alert", 1): similar_accident(),
}


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for (slug, index), html in REPLACEMENTS.items():
        if slug not in data or len(data[slug]) <= index:
            raise KeyError(f"Missing infographic state: {slug}[{index}]")
        data[slug][index] = html
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if DATA_PATH.read_text(encoding="utf-8") != rendered:
        DATA_PATH.write_text(rendered, encoding="utf-8")
    print(f"Prepared {len(REPLACEMENTS)} reviewed infographic examples.")


if __name__ == "__main__":
    main()
