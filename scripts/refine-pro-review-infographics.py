#!/usr/bin/env python3
"""Apply the bounded, scene-specific corrections from Pro review packet 02."""

from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "product-infographics.json"


ICONS = {
    "speaker": '<svg aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" viewBox="0 0 24 24"><path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M16 8a6 6 0 0 1 0 8"/></svg>',
    "person-check": '<svg aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" viewBox="0 0 24 24"><circle cx="9" cy="7" r="3"/><path d="M3.5 20c.8-4 2.7-6 5.5-6s4.7 2 5.5 6"/><path d="m16 16 2 2 3.5-4"/></svg>',
    "threshold-warning": '<svg aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" viewBox="0 0 24 24"><path d="M4 17h16"/><path d="M6 17V7h12v10"/><path d="M12 10v3"/><path d="M12 15h.01"/><path d="m12 4 3 3H9z"/></svg>',
}


def soup_for(markup: str) -> BeautifulSoup:
    return BeautifulSoup(markup, "html.parser")


def set_icon(soup: BeautifulSoup, selector: str, icon: str) -> None:
    target = soup.select_one(selector)
    if target is None:
        raise ValueError(f"Missing icon target: {selector}")
    target.clear()
    target.append(BeautifulSoup(ICONS[icon], "html.parser"))


def add_style(soup: BeautifulSoup, scene: str, rules: str) -> None:
    for node in soup.select('[data-pro-review="style"]'):
        node.decompose()
    style = soup.new_tag("style", attrs={"data-pro-review": "style"})
    style.string = rules
    infographic = soup.select_one(f'[data-infographic-scene="{scene}"]')
    if infographic is None:
        raise ValueError(f"Missing scene: {scene}")
    infographic.insert(0, style)


def replace_icon(markup: str, scene: str, selector: str, icon: str) -> str:
    soup = soup_for(markup)
    if not soup.select_one(f'[data-infographic-scene="{scene}"]'):
        raise ValueError(f"Unexpected scene: {scene}")
    set_icon(soup, selector, icon)
    return str(soup)


def mist_overlay(markup: str) -> str:
    scene = "iot-mist-2"
    soup = soup_for(markup)
    stage = soup.select_one(".render-stage")
    if stage is None:
        raise ValueError("Missing iot-mist render stage")
    for node in stage.select('[data-pro-review]'):
        node.decompose()
    # The render is 1600×900 and uses an equal 16:9 stage. The origin follows
    # the existing No. 01 callout target (about 615×160), not the full card.
    overlay = BeautifulSoup(
        '''<svg aria-hidden="true" data-pro-review="spray-overlay" preserveAspectRatio="xMidYMid meet" viewBox="0 0 1600 900"><defs><linearGradient id="pro-mist-fade" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#b8eee1" stop-opacity=".42"/><stop offset="1" stop-color="#b8eee1" stop-opacity="0"/></linearGradient></defs><path d="M615 160 C595 235 565 315 526 410 L675 370 C654 290 637 216 615 160Z" fill="url(#pro-mist-fade)"/><path d="M615 160 C595 235 565 315 526 410M615 160 C637 216 654 290 675 370" fill="none" stroke="#b8eee1" stroke-dasharray="9 10" stroke-linecap="round" stroke-width="3"/><circle cx="615" cy="160" fill="#b8eee1" r="8"/></svg><span data-pro-review="spray-label">미스트 분사</span>''',
        "html.parser",
    )
    stage.append(overlay)
    add_style(
        soup,
        scene,
        '''.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="iot-mist-2"] .render-stage>[data-pro-review="spray-overlay"]{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="iot-mist-2"] .render-stage>[data-pro-review="spray-label"]{position:absolute;left:8%;bottom:9%;padding:7px 10px;border:1px solid rgb(184 238 225 / 55%);border-radius:999px;background:rgb(16 31 35 / 78%);color:#e6fff8;font-size:14px;font-weight:740;line-height:1;letter-spacing:-.02em;pointer-events:none}''',
    )
    return str(soup)


def compact_gas_label(markup: str) -> str:
    scene = "compact-gas-detector-1"
    soup = soup_for(markup)
    stage = soup.select_one(".render-stage")
    if stage is None:
        raise ValueError("Missing compact gas render stage")
    for node in stage.select('[data-pro-review="diagram-label"]'):
        node.decompose()
    label = soup.new_tag("span", attrs={"data-pro-review": "diagram-label"})
    label.string = "측정 항목 설명용 도해"
    stage.append(label)
    add_style(
        soup,
        scene,
        '''.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="compact-gas-detector-1"] .render-stage>[data-pro-review="diagram-label"]{position:absolute;left:16px;top:16px;z-index:2;padding:7px 10px;border:1px solid rgb(222 237 183 / 46%);border-radius:999px;background:rgb(24 33 27 / 80%);color:#eff8d4;font-size:14px;font-weight:740;line-height:1;letter-spacing:-.02em;pointer-events:none}@container sunflex-infographic (max-width:480px){.product-editorial :is(#product-benefits,#blind-corner) .sunflex-infographic[data-infographic-scene="compact-gas-detector-1"] .render-stage>[data-pro-review="diagram-label"]{left:12px;top:12px;font-size:13px}}''',
    )
    return str(soup)


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data["co2-temp-humidity"][1] = replace_icon(
        data["co2-temp-humidity"][1],
        "co2-temp-humidity-2",
        ".threshold-result > span",
        "speaker",
    )
    data["gas-alarm"][2] = replace_icon(
        data["gas-alarm"][2],
        "gas-alarm-3",
        ".threshold-result > span",
        "person-check",
    )
    data["tilt-acceleration-sensor"][1] = replace_icon(
        data["tilt-acceleration-sensor"][1],
        "tilt-acceleration-sensor-2",
        ".route-stop:nth-of-type(2) > span",
        "threshold-warning",
    )
    data["iot-mist"][1] = mist_overlay(data["iot-mist"][1])
    data["compact-gas-detector"][0] = compact_gas_label(data["compact-gas-detector"][0])
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Applied five bounded Pro-review infographic corrections.")


if __name__ == "__main__":
    main()
