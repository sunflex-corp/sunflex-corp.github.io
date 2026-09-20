# Apple 제품 소개 구조 조사와 SUNPLEX 적용

2026-09-20. 대상: 제품 상세 48개와 제품 목록. 기존 사양·제품 이미지·모델 코드·주의 조건·URL을 보존한다. Apple 자산과 문구는 사용하지 않는다.

## 조사에서 확인한 구조

- [MacBook Pro](https://www.apple.com/kr/macbook-pro/): 제품 중심 도입, 하이라이트 갤러리, 제품 자세히 보기, 3개 칩별 대상 사용자, 비교와 기능 상세. SUNPLEX는 실제 S/M/L와 W/L 모델을 비교한다. Apple의 성능 수치를 옮기지 않는다.
- [AirPods Pro](https://www.apple.com/kr/airpods-pro/): 밝은 단독 제품 장면과 착용/사용 장면을 번갈아 배치, 기능별 챕터, 청취 경험 선택 갤러리. 바디캠은 착용/자석 크래들/삼각대와 기록 흐름으로 번역한다.
- [Apple Watch](https://www.apple.com/kr/apple-watch-series-12/), [AirTag](https://www.apple.com/kr/airtag/): 감지 기능을 사용자가 확인할 수 있는 정보와 연결. 측정 대상 → 정보 전송 → 담당자 확인 구조에 적용한다. 건강/안전 성능 수치를 추정하지 않는다.
- [HomePod](https://www.apple.com/homepod-2nd-generation/): 기기·음향 경험·연결·공간 활용을 순차 소개. 방송 장비는 신호 전달과 현장 배치로 대응한다. 방진·방수·방송 거리는 원문에 있는 값만 유지한다.
- [iPad Pro](https://www.apple.com/kr/ipad-pro/), [Mac Studio](https://www.apple.com/kr/mac-studio/): 화면을 크게 보여주고 업무, 연결, 구성을 단계적으로 설명. 관제·현장 정보 제품은 현장 화면/구성도 중심으로 배치한다.
- [Apple Intelligence](https://www.apple.com/kr/apple-intelligence/): 기능별 작업 예시와 사용하는 흐름을 우선 배치. AI 제품은 입력 → 처리 → 사람의 검토를 원문 그대로 분리한다.

Chrome에서 위 8개 공식 페이지를 직접 스크롤했다. MacBook Pro에서는 고정된 노트북 옆의 M5→M5 Pro 전환과 칩 상세 모달을, AirPods에서는 큰 라운드 갤러리와 다음 챕터 사이 여백을 확인했다. Watch에서는 센서 클로즈업에서 측정 정보로, iPad에서는 기울어진 기기에서 큰 화면과 작업 장면으로 전환되는 구간을 보았다. HomePod는 기기 단독 장면에서 공간 이미지로, AirTag는 밝은 배경의 두 열 설명으로 이어졌다. Mac Studio는 두 칩 선택을 가운데 배치했고, Apple Intelligence는 가로 기능 카드와 큰 챕터 간격을 사용했다. 모든 애니메이션의 모든 프레임을 기록한 것은 아니다.

SUNPLEX에는 제품 특성에 맞는 여섯 구조를 적용했다. CCTV 제품이 스크롤에 따라 펼쳐지고 다시 모이는 동작은 자체 구현이며 Apple 영상·이미지·코드를 복제하지 않았다. 착용형은 제품 크기와 위치가 부드럽게 정리되고, 관제형은 큰 장면이 펼쳐진다. 센서·업무 단계는 현재 설명할 단계를 강조한다. 짧은 화면, 내용이 넘치는 화면, 동작 줄이기 환경은 고정을 해제한다.

## 한국어 어조와 문구

Apple 한국어 제품 페이지에서 관찰한 편집 특징은 짧은 제목의 리듬, 기능과 연결되는 언어유희, 제목 뒤의 구체적인 설명, 별도로 남기는 사용 조건이다. 이는 페이지를 보고 정리한 해석이며 Apple의 공식 카피 가이드는 아니다.

SUNPLEX는 현장 담당자가 기능을 바로 이해하도록 어조를 조절했다. CCTV ‘공정은 바뀌어도. 시야는 이어지도록.’, 바디캠 ‘작업은 두 손으로. 기록은 몸으로.’, 인스펙트컷 ‘긴 영상에서, 필요한 장면으로.’처럼 기능과 연결되는 제목을 썼다. 위험 감지·건강 측정·AI 초안은 예방 보장·진단·확정 판단으로 바꾸지 않았다.

`data/product-editorial-copy.json`에 48개 제품의 제목·첫 설명·도입 챕터 문구와 변경 전 문자열을 기록했다. 생성기가 원문과 일치하는 항목만 교체하며, 원본 자료는 수정하지 않는다. 제품 목록과 관련 제품 카드도 같은 첫 설명을 사용한다. 사양, 모델 코드, 수치, 주의 조건과 기타 상세 본문은 보존 검사를 통과해야 한다.

## 설계

종이색 #f5f5f7, 흰색 #fff, 본문 #1d1d1f, 보조 #63636b, 기술 강조 #1766c2, 다크 챕터 #101216. 기존 한국어 글꼴을 유지하고 제목은 48–80px/단정한 굵기, 본문 17–21px, 사양 13–15px로 분리한다. 제품 자체가 첫 화면의 중심이다. 제품별 고정 목차 → 큰 제품 이미지 → 핵심 선택 → 기능 챕터 → 비교/도입 문의. 긴 좌측 목차와 중복 소개는 제거한다. 숫자 장식 대신 실제 모델명과 업무 단계만 표기한다.

## 수용 기준

48개 전부 명시적으로 레퍼런스/유형 지정. 명시한 문구 교체 외의 기존 텍스트·이미지·앵커 보존. CCTV 모델 선택과 전체 비교, 바디캠 사용 방식 선택, 제품별 목차/문의 정상. 모바일 320px부터 가로 넘침 없이 사용. 숨은 패널 포커스 방지, 키보드 탭 이동, JS 없는 상태에서 모든 내용 노출. 축소 동작 설정 존중. 전체 정적 검사 및 유형별 브라우저 검증 후 배포한다.

## 제품별 대응

|제품|유형|Apple 대응|설명 흐름|
|---|---|---|---|
|이동식 CCTV|lineup|[MacBook Pro](https://www.apple.com/kr/macbook-pro/)|전체 라인업 → 모델 선택 → 통신 비교 → 지지 구조 → 현장 적용|
|이동식 바디캠 (일반 / WiFi & LTE)|wearable|[AirPods Pro · Apple Watch](https://www.apple.com/kr/airpods-pro/)|제품 클로즈업 → 착용/사용 장면 → 동작 방식 → 관리 조건|
|이동형 크레인 후크 하방 카메라|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|챗GPT 기반 지능형 CCTV|workflow|[Apple Intelligence · iPad Pro](https://www.apple.com/kr/apple-intelligence/)|사용 결과 → 입력/처리/검토 단계 → 담당자 역할 → 적용 조건|
|안전종합상황판|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|현장 CMS 구축|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|안전 사각지대 LED 로고라이트|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|출입게이트 차량 진출입 알림|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|CO₂·온습도 탐지 시스템|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
|IoT 기반 미스트 분사 시스템|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|네트워크(LTE) 풍속계|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
|스마트 환경전광판 · IoT 원격관리|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|소형 복합가스 측정기|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
|유해가스 및 폭발성 가스 경보 시스템|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
|기울기변위 · 가속도변화 알림센서|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
|화재 발생 감지 시스템|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
|스마트 화재감지기|lineup|[MacBook Pro](https://www.apple.com/kr/macbook-pro/)|전체 라인업 → 모델 선택 → 통신 비교 → 지지 구조 → 현장 적용|
|AI 방송시스템 · 다국어 자동번역|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|무선방송장치(비상방송)|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|유니모 SE-400 디지털 무전기|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|안전 조회장 & TBM 솔루션 구축|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|AI 중장비 충돌 감지기|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|개구부 개폐 감지 시스템|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
|건설장비 접근경보 시스템|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|타워크레인 후크 이동 경고방송|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|안전모 응급호출·위치알림|wearable|[AirPods Pro · Apple Watch](https://www.apple.com/kr/airpods-pro/)|제품 클로즈업 → 착용/사용 장면 → 동작 방식 → 관리 조건|
|위험지역 안내방송 장치|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|공사현장 주변 보행자 충돌방지 시스템|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|근로자 스마트 음주감지 시스템|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
|위험지역 근로자 위치확인 · 스마트 비콘|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
|통신 음영지역 무선 네트워크망 구성|communication|[HomePod · AirPods](https://www.apple.com/homepod-2nd-generation/)|기기 소개 → 전달/연결 방식 → 공간별 사용 → 설치 구성|
|근력보조 웨어러블 슈트|wearable|[AirPods Pro · Apple Watch](https://www.apple.com/kr/airpods-pro/)|제품 클로즈업 → 착용/사용 장면 → 동작 방식 → 관리 조건|
|스마트 안전고리|wearable|[AirPods Pro · Apple Watch](https://www.apple.com/kr/airpods-pro/)|제품 클로즈업 → 착용/사용 장면 → 동작 방식 → 관리 조건|
|스마트 안전모 · 착용 · 턱끈 체결 감지|wearable|[AirPods Pro · Apple Watch](https://www.apple.com/kr/airpods-pro/)|제품 클로즈업 → 착용/사용 장면 → 동작 방식 → 관리 조건|
|스마트 에어백 · 추락위험 대응|wearable|[AirPods Pro · Apple Watch](https://www.apple.com/kr/airpods-pro/)|제품 클로즈업 → 착용/사용 장면 → 동작 방식 → 관리 조건|
|근로자 출역관리 · 전자카드 시스템|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|근로자 출입관리 게이트 · 출역현황 실시간관리|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|스마트 헬스케어 심박수밴드|wearable|[AirPods Pro · Apple Watch](https://www.apple.com/kr/airpods-pro/)|제품 클로즈업 → 착용/사용 장면 → 동작 방식 → 관리 조건|
|AI 1분 위험성평가|workflow|[Apple Intelligence · iPad Pro](https://www.apple.com/kr/apple-intelligence/)|사용 결과 → 입력/처리/검토 단계 → 담당자 역할 → 적용 조건|
|AI 위험성평가 누락 검토 시스템|workflow|[Apple Intelligence · iPad Pro](https://www.apple.com/kr/apple-intelligence/)|사용 결과 → 입력/처리/검토 단계 → 담당자 역할 → 적용 조건|
|AI 종합안전평가 시스템|workflow|[Apple Intelligence · iPad Pro](https://www.apple.com/kr/apple-intelligence/)|사용 결과 → 입력/처리/검토 단계 → 담당자 역할 → 적용 조건|
|AI 협력업체 안전관리|workflow|[Apple Intelligence · iPad Pro](https://www.apple.com/kr/apple-intelligence/)|사용 결과 → 입력/처리/검토 단계 → 담당자 역할 → 적용 조건|
|AI 드론 구조물 진단|workflow|[Apple Intelligence · iPad Pro](https://www.apple.com/kr/apple-intelligence/)|사용 결과 → 입력/처리/검토 단계 → 담당자 역할 → 적용 조건|
|인스펙트컷|workflow|[Apple Intelligence · iPad Pro](https://www.apple.com/kr/apple-intelligence/)|사용 결과 → 입력/처리/검토 단계 → 담당자 역할 → 적용 조건|
|AI 작업 공종별 유사사망사고 알림·전파|workflow|[Apple Intelligence · iPad Pro](https://www.apple.com/kr/apple-intelligence/)|사용 결과 → 입력/처리/검토 단계 → 담당자 역할 → 적용 조건|
|세이프브릿지|workflow|[Apple Intelligence · iPad Pro](https://www.apple.com/kr/apple-intelligence/)|사용 결과 → 입력/처리/검토 단계 → 담당자 역할 → 적용 조건|
|IoT 소형 타워크레인 운영관리|workspace|[iPad Pro · Mac Studio](https://www.apple.com/kr/ipad-pro/)|화면/현장 전체상 → 정보 흐름 → 구성 요소 → 운영 조건|
|스마트 콘크리트 양생 솔루션|sensing|[Apple Watch · AirTag](https://www.apple.com/kr/apple-watch-series-12/)|기기 소개 → 감지 대상과 알림 흐름 → 설치 위치 → 확인 조건|
