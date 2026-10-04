# 이미지·문구 후속 작업 지시서 (스크롤 점검 2026-10-03)

`SCROLL_REVIEW_AUDIT.md`의 "고치지 않은 항목" 중 **새 이미지**와 **새 문구**가 필요한 것을 모았습니다.

- **이미지(A~D):** Codex 에이전트가 생성하고 적용합니다.
- **문구(E):** 내용 확정이 필요하므로 담당자 확인 후 반영합니다.

## 작업 원칙 (Codex용)

1. **공유 파일은 덮어쓰지 않는다.** `/img/3d/*.webp`, `/media/derived/*` 상당수는 여러 제품 페이지가 같이 씁니다(예: `office-integrated-review` 13개 페이지, `context-record-review` 16개 페이지). 새 파일명으로 만들고, **해당 페이지의 해당 위치** `<img>`/`srcset`만 바꿉니다.
2. **2026-09-23 장면 교체와 같은 절차를 따른다.** 참고: `docs/product-scenes-20260923.md`
   - 실제 제품 사진을 참조해 생성합니다. 원본에서 확인할 수 없는 기능(수치, 화면, 부품)은 그려 넣지 않습니다.
   - 출처 사진, 프롬프트, 생성 파일명, 해시를 `data/product-scene-overrides.json`에 기록합니다.
   - 재생성 스크립트 경로에도 같은 교체를 반영해서, 다시 생성해도 결과가 유지되게 합니다.
3. **크기와 형식**
   - 3D 일러스트: 1280×960(4:3), 흰 배경. `-640`, `-1280` 두 크기의 webp
   - 장면(가로) 이미지: 2560×1441 기준. `-480`, `-768`, `-1280`, `-1600`, `-2560`의 avif와 webp
   - 각 파일은 기존 같은 위치 파일의 용량대(webp 100~200KB)를 넘지 않게 합니다.
4. **스타일 기준:** 강점 3D 카드는 `/img/hl/hl-<slug>-<n>-{640,1280}.webp`(흰 배경, 부드러운 3D 인물·장비)에 맞춥니다.
5. **적용 후 검증**
   - `python3 -m http.server 8765` 실행 후 `node scripts/qa/scroll-audit.cjs <slug> mobile,tablet,pc`
   - 404 0건, 깨진 이미지 0건, 가로 넘침 0건
   - `scripts/test-product-scenes.py`, `scripts/test-product-navigation.cjs` 통과
   - 바뀐 페이지는 390 / 820 / 1440 폭에서 화면으로 확인

---

## A. 강점 카드: 첫 카드만 실사 사진 (3D와 혼용) — 29개 페이지

`#highlights`의 첫 카드만 실사 또는 제품 누끼 사진이고, 나머지 카드는 3D 일러스트입니다. 대부분 히어로와 같은 사진이 반복된 것이기도 합니다.

- **할 일:** 제품별 첫 카드용 3D 이미지 `/img/hl/hl-<slug>-0-{640,1280}.webp`를 생성합니다. 카드 제목이 말하는 내용을 그림으로 보여 주고, 제품 외형은 실제 사진과 같게 합니다.
- **마크업:** 첫 카드의 `<figure>`를 나머지 카드와 같은 형식으로 바꿉니다.

```html
<figure class="pd-fig pd-card-fig is-hl3d"><img src="/img/hl/hl-<slug>-0-640.webp" srcset="/img/hl/hl-<slug>-0-640.webp 640w, /img/hl/hl-<slug>-0-1280.webp 1280w" sizes="(max-width:600px) 90vw, 420px" alt="" width="1280" height="960" loading="lazy" decoding="async" data-3d></figure>
```

| 페이지 | 지금 첫 카드 이미지 |
|---|---|
| ai-broadcast | product-ai-broadcast-restored-white-20260912 (히어로와 같음) |
| ai-drone-inspection | product-ai-drone-inspection-device |
| ai-equipment-collision | product-ai-equipment-collision-device |
| alcohol-detection | product-alcohol-studio-20260910 (히어로와 같음) |
| concrete-curing | product-concrete-curing-restored-white-20260912 (히어로와 같음) |
| digital-radio | field-radio-handover-generated |
| gas-alarm | field-confined-space-generated |
| hazard-area-broadcast | field-broadcast-generated |
| healthcare-heart-band | field-heart-band-wrist-generated |
| inspectcut | product-inspectcut-device (회색 여백 안에 작게 들어감) |
| lte-anemometer | field-office-handover-generated |
| mobile-bodycam | product-mobile-bodycam-restored-white-20260912 (히어로와 같음, 위아래 잘림) |
| pedestrian-collision-prevention | product-pedestrian-collision-prevention-reference-white-stage3 (히어로와 같음) |
| safebridge | product-safebridge-device (어두운 스크린샷) |
| safety-box | product-safety-box-device |
| site-cms | product-site-cms-device |
| smart-airbag | product-smart-airbag-reference-white-stage3 (히어로와 같음) |
| smart-beacon | product-smart-beacon-white-approved (히어로와 같음) |
| smart-environment-board | product-smart-environment-board-reference-white (히어로와 같음, 전광판 윗줄 잘림) |
| smart-helmet | product-smart-helmet-reference-white (히어로와 같음) |
| smart-safety-hook | field-hook-safety-check-generated |
| tbm-solution | product-tbm-solution-reference-white (히어로와 같음) |
| tilt-acceleration-sensor | field-office-handover-generated (lte-anemometer와 같음) |
| tower-crane-hook-collision | field-crane-hook-rigging-generated |
| vehicle-entry-alert | field-vehicle-pedestrian-generated |
| wireless-emergency-broadcast | field-broadcast-generated (hazard-area-broadcast와 같음) |
| wireless-network | field-mobile-cctv-generated |
| worker-access-gate | field-worker-entry-generated |
| worker-attendance-card | product-worker-attendance-card-reference-white (히어로와 같음, 회색 테두리선) |

## B. 한 페이지 안에서 같은 이미지 반복

**3D 장면 반복(우선):** 강점(product-benefits)에 쓴 장면이 바로 아래 작동 흐름이나 상세 섹션에 다시 나옵니다. 뒤쪽 위치를 그 단계 설명에 맞는 새 장면으로 바꿉니다.

| 페이지 | 반복 이미지 | 위치 |
|---|---|---|
| ai-equipment-collision | img/3d/construction-excavator-access | product-benefits → warning-state(2곳) |
| ai-quick-risk-assessment | img/3d/chatgpt-cctv-selection | product-benefits → ai-quick-risk-assessment-flow |
| ai-risk-assessment-review | img/3d/office-integrated-review | product-benefits → ai-risk-assessment-review-flow |
| ai-safety-index | img/3d/office-integrated-review | product-benefits → morning-index-line(2곳) |
| ai-similar-accident-alert | img/3d/office-training-briefing | product-benefits → ai-similar-accident-alert-flow |
| ai-subcontractor-safety | img/3d/office-integrated-review | product-benefits → ai-subcontractor-safety-flow |
| concrete-curing | img/3d/industrial-concrete-record, img/3d/context-record-review | product-benefits → curing-rail(각 2곳) |
| healthcare-heart-band | media/product-scenes/healthcare-heart-band-wearing-20260923 | product-benefits → band-functions |
| hook-bottom-camera | img/pd/hookfit-3d-01, img/pd/hookcp-3d-01 | product-fit → highlights / hook-checkpoints |
| inspectcut | img/3d/chatgpt-cctv-selection | product-benefits → inspectcut-editing-desk |
| iot-mist | img/3d/industrial-pipe-inspection | product-benefits → dust-gate (CO₂ 페이지와도 같음) |
| led-logo-light | img/3d/context-site-lighting | product-benefits → night-route-plan |
| lte-anemometer | img/3d/construction-tower-crane-operation | product-benefits → vertical-wind-section |
| mobile-bodycam | media/derived/product-mobile-bodycam-problem | detail-2 → bodycam-film |
| safebridge | img/3d/office-training-briefing | product-benefits → safebridge-training-timeline(2곳) |
| safety-box | img/3d/office-integrated-review | product-benefits → control-screen |
| smart-beacon | img/3d/construction-site-entry-warning | product-benefits → beacon-flow |
| tilt-acceleration-sensor | img/3d/context-record-review | product-benefits → tilt-decision-record(2곳) |
| tower-crane-hook-collision | img/3d/construction-tower-crane-operation | hook-warning-flow(2곳) → detail-4 |
| wireless-emergency-broadcast | img/3d/context-broadcast-planning | product-benefits → broadcast-reach-line(2곳) |
| wireless-network | img/3d/context-network-connection | product-benefits → network-signal-path |
| worker-access-gate | img/3d/construction-site-entry-warning | product-benefits → access-gate-rhythm |
| worker-attendance-card | img/3d/construction-site-entry-warning | product-benefits → attendance-card-flow |

**제품 사진 반복(다음 순위):** 히어로의 제품 사진이 상세 섹션(detail-4, detail-5, detail-6 등)에 크게 다시 나옵니다. 해당 상세 섹션은 설치나 사용 장면으로 바꾸는 것을 권장합니다.

| 페이지 | 반복 위치 |
|---|---|
| compact-gas-detector | product-benefits |
| digital-radio | detail-4 |
| emergency-signal-location | detail-4 |
| equipment-approach-alarm | detail-5 |
| gas-alarm | detail-5 |
| hazard-area-broadcast | detail-5 |
| healthcare-heart-band | detail-5 |
| hook-bottom-camera | hook-two-views |
| iot-small-tower-crane | detail-4 |
| led-logo-light | night-route-plan, detail-4 |
| lte-anemometer | detail-4 |
| mobile-bodycam | bodycam-film |
| power-assist-suit | detail-5 |
| tilt-acceleration-sensor | detail-5 |
| tower-crane-hook-collision | detail-6 |
| vehicle-entry-alert | detail-5 |
| wireless-emergency-broadcast | detail-5 |

- 히어로와 highlights 첫 카드가 겹치는 경우는 A에서 함께 해결됩니다.

## C. 제품 내용과 맞지 않는 범용 일러스트

| 페이지 | 위치 | 지금 이미지 | 바꿀 내용 |
|---|---|---|---|
| ai-quick-risk-assessment | 강점 01 "빈 문서 대신, 검토할 초안부터" | chatgpt-cctv-selection (CCTV와 모니터) | 사진을 올리면 위험성평가 초안 문서가 만들어지는 장면 |
| inspectcut | 강점 01 "긴 촬영본에서, 필요한 장면만", 02 | chatgpt-cctv-selection, chatgpt-cctv-report-draft | 현장 PC에서 타임라인을 잘라 내는 영상 편집 장면 |
| mobile-bodycam | 강점 01 "다시 보기 어려운 과정도 기록으로" | chatgpt-cctv-selection (고정 CCTV) | 작업자 가슴에 착용한 바디캠과 촬영 시야 |
| power-assist-suit | 강점 02 "충전 대신, 착용과 상태 점검" | context-prework-record (안전모와 클립보드) | 슈트 착용 상태와 탄성 구조 점검 |
| vehicle-entry-alert | 강점 03 "경고를 확인하고, 사람의 안내로" | context-access-route (범용 동선) | 경고 표시를 보고 유도원이 차량을 안내하는 장면 |
| healthcare-heart-band | 강점 02 "설정 범위를 벗어나면, 손목에 진동", 03 | context-prework-record, context-record-review | 손목 진동 알림, 담당자 화면 확인 |
| ai-subcontractor-safety | 강점 01 "업체마다 다른 계획을 한자리에" | office-integrated-review (13개 페이지 공용) | 협력업체별 계획이 한 화면에 모이는 장면 |

## D. 저해상도와 원본 품질

| 페이지 | 위치 | 지금 | 할 일 |
|---|---|---|---|
| ir3-flame-detector | 히어로(전체 폭 배경) | product-ir3-flame-detector **461×425** | 2560×1441 장면 이미지를 새로 생성(5개 크기). 가장 시급 |
| ai-quick-risk-assessment, ai-risk-assessment-review, ai-similar-accident-alert, ai-subcontractor-safety | 히어로(전체 폭 배경) | *-scene 최대 1280×720 | 2560 크기 추가(PC 1440 폭과 고해상도 화면 대응) |
| wireless-emergency-broadcast | 히어로 | 최대 707×548 | 1254 이상 제품 누끼 |
| compact-gas-detector | detail-2 시스템 구성도 | product-compact-gas-detector-diagram **453px**. 잘림은 2026-10-03 `contain`으로 해결했고 저해상도는 남음 | 고해상도로 다시 그리기 |
| iot-small-tower-crane | 히어로와 detail-4 표시기 사진 | 1280×772, 확대 시 계단 현상 | 고해상도 제품 사진 |
| worker-attendance-card | 히어로, 강점 첫 카드 | ~~회색 테두리선~~ 2026-10-03 위·오른쪽 1px 선을 지워 해결 | (완료) |
| emergency-signal-location | 히어로, detail-4 | 안전모 사진에 흰·회색 사각 배경이 비침 | 배경을 제거한 누끼 |
| opening-open-close-sensor | 히어로(PC 전체 폭) | 압축 흔적이 보임 | 품질을 높여 다시 내보내기 |

**참고(이미지가 아닌 CSS 목업):** 다음은 HTML/CSS 목업 안의 자리표시입니다. 필요하면 작은 썸네일 이미지를 넣습니다.
- inspectcut의 편집기 목업 영상 미리보기: 빈 회색 격자
- wireless-network 사진 위 미니 카드의 "사진·영상" 썸네일과 "연결 장비" 타일

---

## E. 새 문구가 필요한 항목 (담당자 확인 후 반영)

### E-1. "도입 전에 확인할 세 가지" 카드 설명 — 19개 페이지

지금은 번호와 라벨만 있어서, 휴대폰·태블릿에서 큰 카드가 비어 보입니다. 설명이 있는 형식은 `hook-bottom-camera` 한 곳뿐입니다.

**적용 방법**
- `<ol class="pd-crit bf-cards" data-bf>`에 `is-desc` 클래스를 추가합니다.
- 각 `.bf-c` 안 `<b>` 뒤에 `<em>설명 한 줄</em>`을 넣습니다.
- 설명은 hook-bottom-camera처럼 "상담 때 무엇을 알려주면 되는지"를 한 줄로 씁니다. 예: `후크에 부착하고 운전석에 영상이 들어오는지 확인`

**문구 초안 (2026-10-03, 확인 대기)** — 제품 사양은 지어내지 않고, 상담 때 고객이 알려 줄 내용으로만 썼습니다.

| 페이지 | 01 | 02 | 03 |
|---|---|---|---|
| ai-broadcast | **등록 음원** — 자주 내보낼 안내 문구와 녹음 음원이 있는지 알려주세요 | **지원 언어** — 근무하는 외국인 작업자의 국적과 필요한 언어를 알려주세요 | **송출 구성** — 방송할 구역 수와 스피커를 둘 위치를 알려주세요 |
| chatgpt-cctv | **입력 장면** — 보고서에 쓸 영상이 어느 카메라·구역에서 나오는지 알려주세요 | **보고서 항목** — 현장에서 쓰는 보고서 양식과 꼭 들어갈 항목을 알려주세요 | **검토 담당자** — 초안을 검토하고 확정할 담당자를 알려주세요 |
| co2-temp-humidity | **측정 위치** — 밀폐·지하 공간 등 측정할 위치와 개수를 알려주세요 | **기준 설정** — 알림을 보낼 이산화탄소·온도·습도 기준을 정해 주세요 | **시간별 기록** — 기록을 얼마나 자주, 얼마 동안 남길지 알려주세요 |
| compact-gas-detector | **측정 가스** — 현장에서 확인해야 할 가스 종류를 알려주세요 | **단독·원격 구성** — 측정기만 쓸지, 원격 확인까지 할지 정해 주세요 | **기록 내보내기** — 측정 기록을 어떤 형식으로 보관·제출하는지 알려주세요 |
| digital-radio | **호출 대상** — 무전으로 연결할 팀과 인원 수를 알려주세요 | **충전·휴대** — 하루 사용 시간과 충전·보관 장소를 알려주세요 | **사용 환경** — 지하·터널·고층 등 통화가 필요한 구간을 알려주세요 |
| fire-detection | **감지 장치** — 감지기를 둘 자재·전기 설비 위치와 개수를 알려주세요 | **방송 연동** — 대피 안내에 쓸 스피커·방송 장치가 있는지 알려주세요 | **발생 위치** — 알림에서 위치를 어떻게 부를지(층·구역 이름) 알려주세요 |
| gas-alarm | **측정 대상** — 확인할 가스 종류와 밀폐공간 위치를 알려주세요 | **센서·경보부** — 센서와 경보등·전광판을 둘 위치를 알려주세요 | **출입 운영 절차** — 측정 뒤 출입을 허가하는 현장 절차를 알려주세요 |
| iot-mist | **급수·전원** — 물을 끌어올 위치와 전원 공급 방식을 알려주세요 | **분사 범위** — 먼지를 줄일 통로·작업 구역의 폭과 길이를 알려주세요 | **제어 구성** — 분사를 언제, 어떻게 켜고 끌지 정해 주세요 |
| ir3-flame-detector | **기본형·CCTV형** — 경보·알림만 필요한지, 영상 확인까지 필요한지 정해 주세요 | **설치 위치** — 감지할 구역과 설치할 높이·거리를 알려주세요 | **경보 연동** — 연결할 경보 장치와 알림 받을 담당자를 알려주세요 |
| led-logo-light | **표시 문구** — 바닥에 비출 문구나 로고를 알려주세요 | **거리·설치면** — 설치할 높이와 비출 바닥까지의 거리를 알려주세요 | **주변 밝기** — 주간·야간, 실내·실외 등 사용할 곳의 밝기를 알려주세요 |
| lte-anemometer | **설치 높이** — 풍속계를 설치할 위치와 높이를 알려주세요 | **전원·수신** — 전원 공급 방식과 LTE 수신 환경을 알려주세요 | **기준값 설정** — 알림을 보낼 풍속 기준을 정해 주세요 |
| mobile-bodycam | **장착 방식** — 가슴·어깨·안전모 중 어디에 달아 쓸지 알려주세요 | **저장·전송** — 영상을 기기에 저장할지, 바로 전송할지 정해 주세요 | **일반형·WiFi형·LTE형** — 현장 통신 환경을 알려주시면 맞는 모델을 안내합니다 |
| safety-box | **표시 항목** — 상황판에 띄울 정보(CCTV·출역·기상 등)를 알려주세요 | **연동 범위** — 이미 쓰는 시스템 중 연결할 것을 알려주세요 | **운영 체계** — 상황판을 보고 대응할 담당자와 운영 방식을 알려주세요 |
| site-cms | **공정별 구역** — 공정에 따라 나눠 볼 구역을 알려주세요 | **CCTV·바디캠** — 사용할 CCTV와 바디캠 수량을 알려주세요 | **관제 범위** — 어디에서 누가 영상을 볼지 알려주세요 |
| smart-environment-board | **측정 항목** — 전광판에 표시할 측정 항목을 알려주세요 | **원격 관리** — 전원과 표시 내용을 원격으로 관리할지 정해 주세요 | **연계 설비** — 미스트 등 함께 작동시킬 설비를 알려주세요 |
| tbm-solution | **조회장 크기** — TBM을 하는 장소의 크기와 참석 인원을 알려주세요 | **시청 거리** — 맨 뒷줄에서 화면까지의 거리를 알려주세요 | **화면·음향** — 야외·지하 등 화면과 스피커를 둘 환경을 알려주세요 |
| tilt-acceleration-sensor | **설치 방향** — 계측할 구조물과 센서를 붙일 방향을 알려주세요 | **측정 항목** — 기울기·가속도 중 확인할 항목을 알려주세요 | **알림 기준** — 알림을 보낼 기준값과 받을 담당자를 정해 주세요 |
| vehicle-entry-alert | **차량 방향** — 차량이 들어오고 나가는 방향을 알려주세요 | **감지 위치** — 차량을 감지할 지점과 보행로 위치를 알려주세요 | **표시 장치** — 경고를 보여 줄 전광판·경광등 위치를 알려주세요 |
| wireless-emergency-broadcast | **송수신 구성** — 방송을 보낼 곳과 받을 곳의 수를 알려주세요 | **전원** — 설치 위치의 전원 공급 방식을 알려주세요 | **거리·장애물** — 장치 사이 거리와 벽·구조물 같은 장애물을 알려주세요 |

### E-2. tbm-solution 보조 카드 제목

`#tbm-essentials` 아래 `.sc-extra`의 카드 두 장이 서로 형식이 다릅니다.
- **왼쪽 카드:** 제목 없이 본문 한 줄("조회장 크기와 인원 배치에 맞춰 화면·스피커 구성을 상담하세요.")과 링크만 있습니다.
- **오른쪽 카드:** 굵은 제목과 본문이 있습니다.

할 일: 왼쪽 카드에 `<h3>` 제목을 추가합니다. 초안: **"조회장에 맞춘 구성 상담"** (확인 대기)

---

## 진행 상태

2026-10-04 처리 (문구는 PR #30 `b9ee97b`, 이미지는 브랜치 `codex/images-20261004`)

- [x] A. 강점 첫 카드 3D 이미지 (29) — `hl-<slug>-0-{640,1280}.webp`
- [x] B. 페이지 안 반복 이미지 — 3D 장면 (23) — 3곳(ai-subcontractor-safety, inspectcut 등)은 A·C 교체로 반복이 먼저 해소됨
- [x] B. 페이지 안 반복 이미지 — 제품 사진 (17) — 18곳을 설치·사용 장면으로
- [x] C. 범용 일러스트 교체 (7) — 9곳
- [x] D. 저해상도·원본 품질 — ir3 히어로 2560 장면, AI 4개 히어로 2560, 무선 비상방송 1254, 가스 구성도 1812, 소형 타워크레인 2560, 안전모 배경 제거, 개폐감지 재내보내기. 소형 타워크레인·안전모 detail-4는 B에서 장면으로 바뀌어 제외
- [x] 추가: 전체 폭 히어로 16개 페이지 `sizes`를 실제 그려지는 폭에 맞춤(PC에서 2560 선택)
- [x] 추가: 제품 사진 13종(파일 50개)에서 이전 회사 JIYOU 스티커·로고 제거 — `docs/jiyou-logo-removal-20261004.md`
- [x] E-1. "도입 전 확인" 카드 설명 (19) — 사용자 승인 후 반영(mobile-bodycam 01은 본문 거치 방식에 맞게 수정)
- [x] E-2. tbm 보조 카드 제목 — "조회장에 맞춘 구성 상담"

생성 출처·프롬프트·해시는 `data/product-scene-overrides.json`(키 끝 `-20261004`)에 있다.
