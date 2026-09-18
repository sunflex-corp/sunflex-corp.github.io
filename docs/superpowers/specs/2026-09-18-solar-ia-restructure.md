# SUNFLEX 사이트 — SOLAR 정보구조(IA) 재편 (Phase 2a)

## 배경

Phase 2 비주얼 디자인(다크 히어로 등) 작업 중, 사용자가 사이트의 제품 분류 체계 자체를
바꾸기로 결정했다: 기존 "MOVING" 브랜드 + 오감(시각·청각·공간·보호·기록) 5분류를 폐기하고,
**"SOLAR"** 브랜드 + 회사 기존 카피에 이미 있는 "신호 흐름"(감지→판단→알림→조치→기록) 개념을
4단계로 압축한 새 분류로 교체한다. 비주얼 Phase 2보다 **이 IA 재편을 먼저** 진행하기로
합의했다 — 비주얼(히어로/컬러블록)이 새 분류 체계 위에서 만들어져야 하기 때문.

## 새 분류 체계

```
SOLAR
 ├─ 01 감지 DETECT   (key: detect)
 ├─ 02 경보 ALERT    (key: alert)
 ├─ 03 대응 RESPOND  (key: respond)
 └─ 04 기록 RECORD   (key: record)
```

기존 5개(`eyes/sound/air/guard/story`) → 4개로 압축. `air`(공간)의 제품들은 성격에 따라
detect/alert 두 곳으로 나뉘어 흡수된다. `product-menu-data.js`(현재 사이트의 메가메뉴 구조
데이터, 5개 sense 키 기준)를 **유일한 소스 오브 트루스**로 삼아 아래처럼 정확히 재매핑한다.

## 제품 재매핑 (48개 전부, `product-menu-data.js` 기준 정확한 목록)

### 01 감지 DETECT (17개)
기존 `eyes`(시각·관제) 전체 8개 + `air`(공간)의 "환경·가스 측정"/"구조물 계측"/"화재·불꽃 감지" 9개

- CCTV·카메라: `mobile-cctv`, `mobile-bodycam`, `hook-bottom-camera`, `chatgpt-cctv`
- 통합 관제: `safety-box`, `site-cms`
- 시각 안내: `led-logo-light`, `vehicle-entry-alert`
- 환경·가스 측정: `co2-temp-humidity`, `iot-mist`, `lte-anemometer`, `smart-environment-board`, `compact-gas-detector`, `gas-alarm`
- 구조물 계측: `tilt-acceleration-sensor`
- 화재·불꽃 감지: `fire-detection`, `ir3-flame-detector`

### 02 경보 ALERT (14개)
기존 `sound`(청각·경보) 전체 10개 + `air`(공간)의 "작업자 안전·위치"/"현장 통신" 4개

- 방송·소통: `ai-broadcast`, `wireless-emergency-broadcast`, `digital-radio`, `tbm-solution`
- 접근·위험 경보: `ai-equipment-collision`, `opening-open-close-sensor`, `equipment-approach-alarm`, `tower-crane-hook-collision`
- 응급·위험 안내: `emergency-signal-location`, `hazard-area-broadcast`
- 작업자 안전·위치: `pedestrian-collision-prevention`, `alcohol-detection`, `smart-beacon`
- 현장 통신: `wireless-network`

### 03 대응 RESPOND (7개)
기존 `guard`(보호·안전장구) 전체 그대로

- 착용 보호구: `power-assist-suit`, `smart-safety-hook`, `smart-helmet`, `smart-airbag`
- 출입·출역 관리: `worker-attendance-card`, `worker-access-gate`
- 건강 관리: `healthcare-heart-band`

### 04 기록 RECORD (10개)
기존 `story`(기록·콘텐츠) 전체 그대로

- AI 안전관리: `ai-quick-risk-assessment`, `ai-risk-assessment-review`, `ai-safety-index`, `ai-subcontractor-safety`
- 영상 점검·기록: `ai-drone-inspection`, `inspectcut`
- 안전교육·사례: `ai-similar-accident-alert`, `safebridge`
- 시공·운영 관리: `iot-small-tower-crane`, `concrete-curing`

## 변경 대상 파일

1. **`product-menu-data.js`** — 최상위 5개 sense 객체(`eyes/sound/air/guard/story`)를 4개
   (`detect/alert/respond/record`)로 재구성. `air`의 5개 하위 카테고리를 위 매핑대로
   detect/alert 두 파일로 분리 삽입. 하위 `categories`(CCTV·카메라, 방송·소통 등)와 개별
   제품 항목(slug/name/href)은 **내용 변경 없이 그대로 이동**만 한다.
2. **48개 제품 상세 페이지** (`products/*/index.html`) — 각 페이지에 박혀있는 `data-sense`
   속성 및 JSON-LD 등에서 쓰이는 구 sense 키(`eyes`/`sound`/`air`/`guard`/`story`)를 위
   매핑에 따라 신 stage 키(`detect`/`alert`/`respond`/`record`)로 치환. 페이지별로 정확히
   어떤 속성에 값이 박혀있는지 구현 단계에서 grep으로 재확인 후 스크립트 작성.
3. **`solutions/` 폴더** — 현재 5개 폴더(`eyes,sound,air,guard,story`)를 4개
   (`detect,alert,respond,record`)로 재편.
   - `solutions/eyes/` → `solutions/detect/` (내용 유지, 제목/설명에서 "시각·관제" 표현만
     "감지"로 다듬음 — 새 카피 창작 최소화, 기존 문장 재활용 우선)
   - `solutions/sound/` → `solutions/alert/`
   - `solutions/guard/` → `solutions/respond/`
   - `solutions/story/` → `solutions/record/`
   - `solutions/air/`는 **폐기하지 않고 감지/경보 두 방향으로 내용 분할**: 이 폴더의 기존
     본문 중 환경·가스·화재 관련 문단은 `solutions/detect/`로, 작업자 위치·통신 관련 문단은
     `solutions/alert/`로 이관. 정확한 문단 경계는 구현 단계에서 `solutions/air/index.html`
     본문을 직접 읽고 판단한다 (기계적 치환 불가, 사람이 확인 필요한 유일한 지점).
   - 예전 URL(`/solutions/eyes` 등)에서 새 URL로 301 대응이 불가능한 정적 사이트이므로,
     구 URL에는 새 URL로 안내하는 간단한 리다이렉트 페이지(`<meta http-equiv="refresh">`
     + 링크)를 남겨 깨진 링크를 방지한다.
4. **`solutions/index.html`** — 4개 카드로 목록 재구성 (5→4).
5. **메가메뉴 관련 파일** (`solution-menu.css`, `solution-menu.js`, `product-category-menu.css`,
   `product-category-menu.js`) — sense 키 문자열이 하드코딩되어 있는지 확인 후 필요시 치환.
6. **홈페이지/회사소개 페이지의 오감 위젯** — 실제로 인터랙티브 tab 위젯(`#sense-tab-eyes`
   등)은 `company/index.html`에 있음(홈페이지 자체 히어로는 별개의 "image-phrase" 글자별
   리빌 위젯). `company/index.html`의 sense-explorer 탭 5개를 4개로 재구성, 라벨을
   감지/경보/대응/기록으로, 각 탭의 설명 문구는 기존 `.sense-explorer__positioning` 텍스트를
   재활용(새 카피 최소화).
7. **`_astro/BaseLayout.a023156454.css`의 `--moving-*` 토큰** — 5색(eyes/sound/air/guard/story)
   → 4색으로 정리할지, 5색을 유지한 채 4개만 매핑해 쓸지는 구현 단계에서 실제 사용처를 보고
   결정 (색상 자체를 새로 만들지는 않음 — 기존 5색 중 4개를 재사용).

## 원칙

- **새 카피를 창작하지 않는다.** 기존 문구를 재배치/재사용하는 것이 원칙. 유일한 예외는
  `solutions/air` 분할 시 필요한 최소한의 문장 연결/전환구.
- **제품-카테고리 매핑은 위 표가 유일한 기준.** 구현 중 애매한 경우가 생기면 임의로 판단하지
  말고 위 표를 재확인한다.
- 헤더 텍스트 SUNFLEX 로고, 전화/이메일/주소 등 Phase 1에서 이미 확정한 내용은 건드리지 않는다.

## 검증

- 재구성 후 `product-menu-data.js`의 4개 키 아래 제품 총합이 48개인지, 위 표와 슬러그 단위로
  1:1 일치하는지 스크립트로 검증
- 48개 제품 상세 페이지 각각의 신 stage 키가 위 매핑과 일치하는지 검증
- `solutions/{detect,alert,respond,record}/` 4개 페이지가 모두 200 응답하는지, 구 URL
  (`/solutions/eyes` 등)이 새 URL로 안내되는지 로컬 서버로 확인
- 메가메뉴/company 페이지 sense-explorer가 4개 탭으로 정상 렌더링되는지 스크린샷 확인

## 범위 밖

- Phase 2b(다크 히어로, Asta Sans, 컬러블록, 헤더 스크롤 숨김 등 비주얼) — 이 IA 재편 완료 후 별도 진행
- 제품 상세 페이지 본문 카피 리라이팅
