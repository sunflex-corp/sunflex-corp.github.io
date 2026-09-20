# 단계별 스크롤 전환 적용

현장 CMS 등 31개 순차형 제품 페이지와 이동식 CCTV 전용 장면에 적용. 다음 단계는 낮은 밝기, 현재 단계는 선명한 선택선. 직접 선택/방향키/역방향 스크롤 지원. 낮은 화면, 긴 콘텐츠, 동작 줄이기는 고정 없이 탭으로 제공. 디지털 무전기·LTE 풍속계·IoT 소형 타워크레인은 병렬 비교 정보여서 제외.

- [AI 드론 구조물 진단](/products/ai-drone-inspection/)
- [AI 중장비 충돌 감지기](/products/ai-equipment-collision/)
- [AI 1분 위험성평가](/products/ai-quick-risk-assessment/)
- [AI 위험성평가 누락 검토 시스템](/products/ai-risk-assessment-review/)
- [AI 종합안전평가 시스템](/products/ai-safety-index/)
- [AI 작업 공종별 유사사망사고 알림·전파](/products/ai-similar-accident-alert/)
- [AI 협력업체 안전관리](/products/ai-subcontractor-safety/)
- [근로자 스마트 음주감지 시스템](/products/alcohol-detection/)
- [챗GPT 기반 지능형 CCTV](/products/chatgpt-cctv/)
- [CO₂·온습도 탐지 시스템](/products/co2-temp-humidity/)
- [소형 복합가스 측정기](/products/compact-gas-detector/)
- [스마트 콘크리트 양생 솔루션](/products/concrete-curing/)
- [건설장비 접근경보 시스템](/products/equipment-approach-alarm/)
- [화재 발생 감지 시스템](/products/fire-detection/)
- [유해가스 및 폭발성 가스 경보 시스템](/products/gas-alarm/)
- [위험지역 안내방송 장치](/products/hazard-area-broadcast/)
- [인스펙트컷](/products/inspectcut/)
- [안전 사각지대 LED 로고라이트](/products/led-logo-light/)
- [개구부 개폐 감지 시스템](/products/opening-open-close-sensor/)
- [공사현장 주변 보행자 충돌방지 시스템](/products/pedestrian-collision-prevention/)
- [세이프브릿지](/products/safebridge/)
- [현장 CMS 구축](/products/site-cms/)
- [스마트 환경전광판 · IoT 원격관리](/products/smart-environment-board/)
- [안전 조회장 & TBM 솔루션 구축](/products/tbm-solution/)
- [기울기변위 · 가속도변화 알림센서](/products/tilt-acceleration-sensor/)
- [타워크레인 후크 이동 경고방송](/products/tower-crane-hook-collision/)
- [출입게이트 차량 진출입 알림](/products/vehicle-entry-alert/)
- [무선방송장치(비상방송)](/products/wireless-emergency-broadcast/)
- [통신 음영지역 무선 네트워크망 구성](/products/wireless-network/)
- [근로자 출입관리 게이트 · 출역현황 실시간관리](/products/worker-access-gate/)
- [근로자 출역관리 · 전자카드 시스템](/products/worker-attendance-card/)

## 검증
- Chrome에서 로컬 QA 화면의 검사 버튼을 직접 실행. 31개 경로 × 390/768/1440px = 93개 조합, 각 단계 전환/단일 패널 표시/가로 넘침/고정 영역 하단 잘림 검사: 93/93, errors 0.
- 현장 CMS 데스크톱 01→02→03→02 직접 스크롤 및 390/768px 화면 검수. 이동식 CCTV 스크롤 전환, 5단계 콘크리트 양생 화면 확인.
- 3/4/5단계 정방향/역방향/클릭 동기화, 키보드, 다음 단계 밝기 상태, reduced-motion, 낮은 화면/긴 콘텐츠 fallback 단위 테스트 통과.
- 66페이지 출처 텍스트·자산·링크 검사 및 기존 제품/홈/사이트 회귀 테스트 통과. 실제 모바일 OS별 검사나 4K FPS 측정은 포함하지 않음.

## 보행자 충돌방지: 기능에서 이점으로

일반적인 단계 제목과 짧은 설명만 교체하던 영역을 같은 출입구의 SVG 장면 3개로 개선했다. 방음벽으로 가려진 시야 → 인체감지 센서가 접근 감지 → 차량·보행자 양쪽 전광판과 경광등 알림을 시각적으로 연결한다. 실제 설치 배치를 단정하지 않는 작동 원리 예시이며, 감지·경고 제품의 범위를 넘어 자동 제동이나 사고 예방 보장을 주장하지 않는다.

기존 설치 도식은 ‘설치 구성 살펴보기’에 보존했다. 현재 단계 강조, 다음 단계 밝기 낮춤, 클릭과 스크롤 동기화를 유지했다. 센서와 신호 표현은 짧은 일회성 애니메이션이며 동작 줄이기 설정에서는 정지한다.

검수: Chrome 데스크톱 02 직접 선택 및 03 스크롤 전환, 390px·768px 뷰포트의 01~03 장면을 직접 확인했다. 실기기 전체 플랫폼 검수를 의미하지 않는다.
