# 제품별 강점 전환 개선 — 2026-09-20

기존 보행자 충돌방지 페이지의 장면 전환을 기준으로 나머지 47개 제품의 메시지와 장면을 개별 작성했다. 신규 제품 기능·수치·인증을 추가하지 않고 보존된 제품 자료의 역할과 한계를 유지했다. AI 초안과 사람의 최종 판단, 감지·경고와 현장 대응을 구분했다.

## 적용

- 47개 제품, 141개 강점 장면. 제품별 제목·설명·짧은 탭 이름과 관련 구성 링크.
- 기존 제품·현장 이미지를 제품별로 연결. 제품 단독 사진은 전체 형태, 현장 사진은 장면 중심으로 표시. CMS에는 기존 착공·중기·준공 전 도식을 사용.
- 현재 단계 강조, 다음 단계 어둡게 표시, 자연 스크롤과 클릭·키보드 동기화.
- 기존 사양·표·원문은 유지. 중복된 일반 단계 전환은 ‘작동 순서와 운영 방법’ 펼침 영역으로 정리. CCTV와 CMS의 특화 구성은 유지.
- 화면에 진입하기 전 인접 장면 이미지를 준비. 작은 화면·동작 줄이기 설정에서는 고정을 사용하지 않는 기존 동작 유지.

## 검증

Chrome의 보이는 화면에서 47개 페이지를 차례로 열고, 각 페이지의 모바일 390px / 데스크톱 1100px 화면을 직접 확인했다. 페이지 내부 검수 도구가 각 화면의 01·02·03을 선택해 총 282개 상태의 패널 선택, 이미지 로딩, 상세 링크, 넘침·고정 영역 잘림, 본문 색상을 검사했다. 결과는 `browser-results.json`에 보관했다.

사진 문맥 수정 후 해당 페이지들을 재확인했다. 390×844 / 768×900의 AI 위험성평가, 375×667 / 768×900의 CCTV도 확인했다. 이는 Chrome 뷰포트 검수이며 전체 운영체제·실기기 검수를 뜻하지 않는다.

정적 검사: `scripts/check-solar-site.py`, `scripts/test-product-benefits.py`. 회귀 검사: `test-product-flow.cjs`, `test-product-editorial.cjs`, `test-mobile-cctv.cjs`.

## 제품별 핵심 메시지

| 제품 | 중심 메시지 | 전환 포인트 |
|---|---|---|
| [이동식 CCTV](https://sunflex-corp.github.io/products/mobile-cctv/#product-benefits) | 달라지는 현장에 맞추는 시야. | 옮기는 시야 → 현장별 선택 → 통신 구성 |
| [스마트 화재감지기](https://sunflex-corp.github.io/products/ir3-flame-detector/#product-benefits) | 불꽃을 감지한 다음까지 생각한 구성. | 불꽃 감지 → 경보·알림 → 영상 확인 |
| [이동식 바디캠](https://sunflex-corp.github.io/products/mobile-bodycam/#product-benefits) | 작업자의 시선이 현장의 기록으로. | 작업자 시선 → 검측 기록 → 기록 활용 |
| [안전모 응급호출·위치알림](https://sunflex-corp.github.io/products/emergency-signal-location/#product-benefits) | 호출을 받았을 때, 위치도 알 수 있도록. | 버튼 호출 → 위치 전달 → 대응 준비 |
| [근력보조 웨어러블 슈트](https://sunflex-corp.github.io/products/power-assist-suit/#product-benefits) | 반복해서 드는 일에 보조를 더하다. | 착용 보조 → 탄성 구조 → 배터리 없이 |
| [스마트 안전고리](https://sunflex-corp.github.io/products/smart-safety-hook/#product-benefits) | 체결이 필요한 순간을 함께 확인. | 이동 구간 → 체결 안내 → 미체결 알림 |
| [스마트 안전모](https://sunflex-corp.github.io/products/smart-helmet/#product-benefits) | 안전모 착용을 확인하는 또 하나의 방법. | 기존 안전모 → 상태 감지 → 담당자 확인 |
| [스마트 에어백](https://sunflex-corp.github.io/products/smart-airbag/#product-benefits) | 작업복 위에 더하는 충격 완화. | 착용 보호 → 감지·전개 → 운영 점검 |
| [스마트 헬스케어 심박수밴드](https://sunflex-corp.github.io/products/healthcare-heart-band/#product-benefits) | 손목의 신호를 함께 살피다. | 심박 측정 → 착용자 알림 → 관리자 확인 |
| [CO₂·온습도 탐지 시스템](https://sunflex-corp.github.io/products/co2-temp-humidity/#product-benefits) | 공기의 상태를 읽고, 변화를 남기다. | 동시 측정 → 기준 알림 → 변화 기록 |
| [네트워크(LTE) 풍속계](https://sunflex-corp.github.io/products/lte-anemometer/#product-benefits) | 높은 곳의 바람을 가까운 화면에서. | 상부 측정 → 기준 알림 → 작업 판단 |
| [소형 복합가스 측정기](https://sunflex-corp.github.io/products/compact-gas-detector/#product-benefits) | 측정할 곳과 확인할 곳이 달라도. | 원격 측정 → 복합 측정 → 기록 검토 |
| [유해가스 및 폭발성 가스 경보 시스템](https://sunflex-corp.github.io/products/gas-alarm/#product-benefits) | 밀폐공간에 들어가기 전, 확인할 근거. | 진입 전 측정 → 현장 표시 → 출입 판단 |
| [기울기·가속도 변화 알림센서](https://sunflex-corp.github.io/products/tilt-acceleration-sensor/#product-benefits) | 작은 변화도 검토할 기록으로. | 변화 계측 → 이상 알림 → 기록 검토 |
| [화재 발생 감지 시스템](https://sunflex-corp.github.io/products/fire-detection/#product-benefits) | 감지 신호가 필요한 안내로 이어지도록. | 불꽃 감지 → 대피 안내 → 관리자 알림 |
| [개구부 개폐 감지 시스템](https://sunflex-corp.github.io/products/opening-open-close-sensor/#product-benefits) | 열린 덮개를 함께 알아차리도록. | 열림 감지 → 현장 방송 → 담당자 알림 |
| [근로자 스마트 음주감지 시스템](https://sunflex-corp.github.io/products/alcohol-detection/#product-benefits) | 측정과 확인을 출입 절차 안에. | 출입 전 측정 → 결과 전달 → 재확인 |
| [위험지역 근로자 위치확인 스마트 비콘](https://sunflex-corp.github.io/products/smart-beacon/#product-benefits) | 구역별 인원 확인의 기준을 세우다. | 구역 확인 → 인원·접근 → 상황 대조 |
| [스마트 콘크리트 양생 솔루션](https://sunflex-corp.github.io/products/concrete-curing/#product-benefits) | 다음 공정을 검토할 양생 기록. | 온도 기록 → 강도 추정 → 공정 검토 |
| [안전 사각지대 LED 로고라이트](https://sunflex-corp.github.io/products/led-logo-light/#product-benefits) | 어두운 길에 더하는 분명한 안내. | 빛으로 안내 → 경계 표시 → 현장 배치 |
| [출입게이트 차량 진출입 알림](https://sunflex-corp.github.io/products/vehicle-entry-alert/#product-benefits) | 출입구의 움직임을 주변에 알리다. | 진출입 감지 → 지점별 경고 → 유도원 안내 |
| [IoT 기반 미스트 분사 시스템](https://sunflex-corp.github.io/products/iot-mist/#product-benefits) | 차량이 드나드는 자리에서 먼지에 대응. | 넓게 분사 → 먼지 흡착 → 가동 조절 |
| [AI 방송시스템 · 다국어 자동번역](https://sunflex-corp.github.io/products/ai-broadcast/#product-benefits) | 여러 언어로 전하는 하나의 안전 안내. | 다국어 안내 → 음성·화면 → 현장 전달 |
| [무선 비상방송 장치](https://sunflex-corp.github.io/products/wireless-emergency-broadcast/#product-benefits) | 공정이 바뀌어도 필요한 방송이 닿도록. | 무선 연결 → 이동 설치 → 일상·비상 |
| [유니모 SE-400 디지털 무전기](https://sunflex-corp.github.io/products/digital-radio/#product-benefits) | 전할 내용에 맞춰 통화 대상을 선택. | 조별 통화 → 개별 호출 → 전체 공지 |
| [안전 조회장·TBM 솔루션](https://sunflex-corp.github.io/products/tbm-solution/#product-benefits) | 함께 보고 듣는 작업 전 안전교육. | 자료와 설명 → 조회장 구성 → 공종별 안내 |
| [타워크레인 후크 이동 경고방송](https://sunflex-corp.github.io/products/tower-crane-hook-collision/#product-benefits) | 후크의 움직임이 아래까지 전해지도록. | 이동 감지 → 다국어 경고 → 주변 확인 |
| [위험지역 안내방송 장치](https://sunflex-corp.github.io/products/hazard-area-broadcast/#product-benefits) | 위험 경계에서 전하는 현장의 안내. | 접근 감지 → 문구 설정 → 설치 구성 |
| [통신 음영구간 무선 네트워크망 구성](https://sunflex-corp.github.io/products/wireless-network/#product-benefits) | 통신이 약한 곳에도 작업 정보를. | 음영 구간 → 메시 연결 → 자료 확인 |
| [이동형 크레인 후크 하방 카메라](https://sunflex-corp.github.io/products/hook-bottom-camera/#product-benefits) | 운전석의 시야에 후크 아래를 더하다. | 후크의 시야 → 영상 전송 → 함께 확인 |
| [안전종합상황판](https://sunflex-corp.github.io/products/safety-box/#product-benefits) | 현장 확인에 필요한 정보를 한곳에. | 정보 통합 → CCTV 연결 → 함께 검토 |
| [현장 CMS 구축](https://sunflex-corp.github.io/products/site-cms/#product-benefits) | 착공부터 준공까지, 공정에 맞는 관제. | 착공 초기 → 공정 전환 → 준공 전 |
| [스마트 환경전광판](https://sunflex-corp.github.io/products/smart-environment-board/#product-benefits) | 환경 확인과 설비 관리를 연결하다. | 환경 측정 → 전광판 표시 → 설비 관리 |
| [AI 중장비 충돌 감지기](https://sunflex-corp.github.io/products/ai-equipment-collision/#product-benefits) | 장비 사각지대에 더하는 확인 수단. | 사각지대 → 사람 감지 → 동시 경고 |
| [건설장비 접근경보 시스템](https://sunflex-corp.github.io/products/equipment-approach-alarm/#product-benefits) | 접근을 알리는 신호는 양쪽으로. | 접근 감지 → 양쪽 경고 → 현장 대응 |
| [근로자 출역관리 전자카드 시스템](https://sunflex-corp.github.io/products/worker-attendance-card/#product-benefits) | 카드에 남긴 출입을 현장의 명단으로. | 카드 인식 → 명단 확인 → 인원 대조 |
| [근로자 출입관리 게이트](https://sunflex-corp.github.io/products/worker-access-gate/#product-benefits) | 인증과 통과, 출역 기록을 이어서. | 출입 인증 → 게이트 통과 → 출역 기록 |
| [IoT 소형 타워크레인 운영관리](https://sunflex-corp.github.io/products/iot-small-tower-crane/#product-benefits) | 인양을 판단할 정보를 한눈에. | 인양 정보 → 풍속 확인 → 함께 검토 |
| [챗GPT 기반 지능형 CCTV](https://sunflex-corp.github.io/products/chatgpt-cctv/#product-benefits) | 장면 확인에서 보고서 검토까지. | 장면 선택 → AI 초안 → 관리자 검토 |
| [AI 1분 위험성평가](https://sunflex-corp.github.io/products/ai-quick-risk-assessment/#product-benefits) | 사진에서 시작하는 위험성평가 초안. | 사진 입력 → 초안 작성 → 현장 보완 |
| [AI 위험성평가 누락 검토 시스템](https://sunflex-corp.github.io/products/ai-risk-assessment-review/#product-benefits) | 작성한 평가에 검토의 기회를 한 번 더. | 평가 비교 → 누락 제안 → 보완 기록 |
| [AI 종합 안전평가 시스템](https://sunflex-corp.github.io/products/ai-safety-index/#product-benefits) | 많은 현장 중 먼저 확인할 곳을 찾다. | 자료 통합 → 지수 분석 → 우선순위 |
| [AI 협력업체 안전관리](https://sunflex-corp.github.io/products/ai-subcontractor-safety/#product-benefits) | 업체별 작업을 같은 곳에서 확인. | 계획 공유 → 진행 확인 → 보고 정리 |
| [AI 드론 구조물 진단](https://sunflex-corp.github.io/products/ai-drone-inspection/#product-benefits) | 구조물의 장면과 위치를 한 기록에. | 외관 촬영 → 위치 기록 → 보고서 검토 |
| [인스펙트컷](https://sunflex-corp.github.io/products/inspectcut/#product-benefits) | 검측에 필요한 영상으로 정리하다. | 구간 선택 → 자막·시간 → 원본·제출본 |
| [AI 작업 공종별 유사사망사고 알림·전파](https://sunflex-corp.github.io/products/ai-similar-accident-alert/#product-benefits) | 오늘의 작업에 참고할 사고사례. | 작업 분석 → 사례 검색 → 현장 전파 |
| [세이프브릿지](https://sunflex-corp.github.io/products/safebridge/#product-benefits) | 같은 교육을 각자의 언어로 이해하도록. | 교육자 설명 → 언어별 자막 → 교육 기록 |
