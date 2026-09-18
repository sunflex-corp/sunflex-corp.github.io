# SUNFLEX 신규 사이트 런칭 (지유이엔지 사이트 기반 리브랜딩) 설계

## 배경

지유이엔지와 대표가 같은 신설 독립 법인 SUNFLEX가 출범한다. SUNFLEX의 회사 공식 웹사이트를
새로 만들되, 제품군·솔루션 콘텐츠 구성은 지유이엔지 공식 사이트(`jiyou-eng/jiyou-eng.github.io`)와
동일하게 가져가고, 회사명과 로고만 SUNFLEX로 교체한 버전을 먼저 만든다.

기존 지유이엔지 사이트는 **절대 수정하지 않는다**. 완전히 별도의 새 레포/새 사이트로 만든다.

세부 페이지별 카피(제품 상세, 회사소개 서술 등)는 이번 작업 범위가 아니며, 사용자가 사이트를
직접 둘러보면서 순차적으로 다듬을 예정이다. 이번 작업은 "회사명 + 로고" 수준의 1차 리브랜딩만
기계적으로 처리하고, 남은 항목은 TODO로 명시한다.

## 소스 자산

- 지유이엔지 사이트 원본: `jiyou-eng/jiyou-eng.github.io` (GitHub, public) — Astro로 빌드된
  정적 산출물만 커밋되어 있음 (`src/`, `package.json` 없음). 62개 HTML 페이지.
- SUNFLEX CI 패키지: `~/Downloads/SUNFLEX_SOLAR_Revised_CI_v1.1/SUNFLEX_SOLAR_Reference_Revision_v1.1/`
  - `02_SUNFLEX/{svg,png,pdf,eps}/SUNFLEX_EN_Reference_Primary.*` — 심볼+워드마크 통합 CI (영문, Primary 컬러)
  - `02_SUNFLEX/{svg,png,pdf,eps}/SUNFLEX_Reference_Wordmark_{Blue,Ink,White}.*` — 텍스트 전용 워드마크
  - `02_SUNFLEX/{svg,png,pdf,eps}/SUNFLEX_KO_*.*` — 국문 CI
  - `01_SOLAR/**` — SOLAR 서브 제품라인 로고 (라인업/시스템/솔루션 레이아웃, 심볼 단독) — 이번 범위 밖, 보관용
  - `03_App_Icons/{svg,png,pdf}/SOLAR_App_Icon_{Blue,White}_Enlarged.*` — 완성된 512×512 앱 아이콘/파비콘용 자산

## 결과물

- 새 GitHub 레포: `jiyou-eng/sunflex-site` (기존 `jiyou-eng` 조직 안에 생성)
- GitHub Pages 배포: 프로젝트 페이지 방식, `https://jiyou-eng.github.io/sunflex-site/`
  (자체 도메인 없음 — CNAME 파일 없이 시작, 나중에 도메인 생기면 추가)

## 아키텍처

Astro 소스 없이, 지유이엔지 사이트의 빌드 결과물(정적 HTML/CSS/JS)을 그대로 새 레포의 시작점으로
복사한다. 빌드 파이프라인이 없으므로 즉시 배포 가능하지만, 헤더/푸터 같은 공통 요소를 페이지마다
개별 HTML 파일 안에서 반복 수정해야 하는 구조적 한계가 있다 (Astro 컴포넌트가 아니라 이미 각
페이지에 인라인된 최종 마크업이기 때문). 62개 페이지 규모에서는 스크립트 기반 일괄 치환으로
감당 가능하다고 판단했다.

## 로고/브랜드 자산 반영

| 용도 | 기존 (지유이엔지) | 신규 (SUNFLEX) |
|---|---|---|
| 헤더 로고 (전 페이지 공통, `brand/jiyou-wordmark.svg`) | 심볼(주황 점)+"JIYOU" 컬러 텍스트 | `SUNFLEX_EN_Reference_Primary.svg` → `brand/sunflex-wordmark.svg`로 저장 |
| JSON-LD `Organization.logo` (`brand/jiyou-wordmark.png`) | 위와 동일한 PNG | 동일 자산의 PNG → `brand/sunflex-wordmark.png` |
| 파비콘 (`favicon.ico/.png/.svg`) | 지유이엔지 전용 아이콘 | `03_App_Icons/svg/SOLAR_App_Icon_Blue_Enlarged.svg` 기반으로 재생성 (이미 완성된 512×512 정사각 아이콘이라 새로 자르지 않고 그대로 활용) |
| 미사용 자산 보관 | — | Flat/Ink/White 컬러 변형, KO CI, SOLAR 서브 레이아웃(라인업/시스템/솔루션) 전체를 `brand/sunflex/` 폴더에 원본 그대로 복사해 둠. 지금 어떤 페이지에도 적용하지 않고, 추후 사용자가 페이지별 작업 시 선택해서 쓸 수 있게 대기 |

`brand/jiyou-logo.png`는 HTML에서 실제 참조하는 곳이 없어(그레핑으로 확인) 새 레포에서는 제외한다.

기존 "MOVING" 제품군 명칭·오감(시각/청각/공간/보호/기록) 색상 토큰, SOLAR 서브 레이아웃 적용 등은
이번 패스에서 건드리지 않는다 — "제품군은 기존 브랜드 그대로" 원칙.

## 텍스트 치환 (스크립트 기반, 전체 62개 HTML 대상)

| 패턴 | 치환 후 | 비고 |
|---|---|---|
| `지유이엔지` (951건) | `썬플렉스` | 표시 텍스트, title, meta, JSON-LD name 전부 포함 |
| `(주)지유이엔지` (JSON-LD alternateName) | `(주)썬플렉스` | 실제 법인 등기명이 다르면 나중에 정정 필요 — TODO에 명시 |
| `jiyoueng.com` (626건, canonical/og:url/og:image 절대경로) | `jiyou-eng.github.io/sunflex-site` 기준 절대경로 | 실도메인 확정 시 재치환 |
| 헤더 로고 `alt`/`aria-label` ("지유이엔지 홈" 등) | "썬플렉스 홈" | |

**의도적으로 그대로 두는 항목** (사실을 알 수 없어 임의로 지어내지 않음):
- 전화번호 `031-991-2285`, 이메일 `jiyoueng@daum.net`, 공장 주소(김포/시흥), 네이버 블로그
  `sameAs` 링크, "사내 포털" 내비게이션 링크
- 제품/솔루션 상세 페이지의 본문 카피 전체

## 검증

1. 치환 스크립트 실행 후 `grep -r "지유이엔지\|jiyoueng" --include="*.html"` 결과가 남은 항목
   리스트(위 "그대로 두는 항목")에 해당하는 문자열 외에는 0건이어야 한다.
2. 로컬 정적 서버로 새 사이트를 띄워 홈/회사소개/제품/문의 페이지에서 헤더 로고, 브라우저 탭
   파비콘, 페이지 타이틀이 SUNFLEX로 정확히 바뀌었는지 스크린샷으로 확인한다.
3. 새 GitHub 레포 push 후 GitHub Pages가 정상적으로 켜지고 실제 URL에서 페이지가 뜨는지 확인한다.

## 산출물: TODO 체크리스트

레포 루트에 `SUNFLEX_TODO.md`를 만들어 아래 항목을 정리해 남긴다:
- 실제 법인명(등기명), 연락처(전화/이메일), 주소가 확정되면 반영
- 커스텀 도메인 연결 시 canonical/og:url 재치환 + CNAME 추가
- "사내 포털" 링크가 SUNFLEX에도 유효한지 확인 (아니면 제거)
- 네이버 블로그 등 SNS 링크 확인
- 제품/솔루션 페이지 본문 카피 검토 (지유이엔지 특유 표현이 남아있는지)
- OG 소셜 공유 이미지(`media/og/jiyoueng-og.jpg`)는 이번에 그대로 복사됨 — SUNFLEX 전용 이미지로 교체 여부 검토
- 필요 시 SOLAR 서브 브랜드 레이아웃(`brand/sunflex/solar/`) 적용

## 범위 밖

- 지유이엔지 기존 사이트/레포 수정 — 절대 하지 않음
- Astro 소스 복원 또는 빌드 파이프라인 구축
- 개별 제품/솔루션 페이지 카피 리라이팅
- 실제 도메인 구매/DNS 설정
- SOLAR 서브 브랜드 레이아웃의 실제 페이지 적용
