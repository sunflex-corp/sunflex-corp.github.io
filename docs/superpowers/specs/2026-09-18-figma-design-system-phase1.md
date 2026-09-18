# SUNFLEX 사이트 — Figma 디자인 시스템 도입 (Phase 1: 토큰/버튼/헤더·푸터)

## 배경

콘텐츠 검토 과정에서 사용자가 `design.hagicode.com/designs/figma/`에 정리된, Figma(디자인 툴
회사) 공개 웹사이트에서 역추출한 비공식 디자인 시스템(`DESIGN.md`, 출처:
[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/figma/DESIGN.md))을
SUNFLEX 사이트에 전면 적용하기로 결정했다. 이 자료는 SUNFLEX나 산업안전 도메인과 무관한
일반 참고 자료이며, 컬러까지 포함해 전면 채택하기로 확인받았다 — 즉 지금까지 유지해온
SUNFLEX 블루(#4351D8) 액센트는 UI 강조색에서 빠지고 로고에만 남는다.

범위가 매우 커서(폰트/버튼모양/카드/헤더/푸터/홈페이지 컬러블록 스토리텔링 섹션 전체)
단계를 나누기로 했다. 이 문서는 **Phase 1: 공통 토큰 + 버튼 + 헤더/푸터**만 다룬다.
홈페이지 컬러블록 스토리텔링 섹션, 회사소개/솔루션/문의 페이지 고유 레이아웃은 이후
단계(Phase 2+)로 미룬다.

## 원본 디자인 시스템 핵심 (DESIGN.md 요약)

- 모노크롬 코어: primary(#000000) + canvas(#ffffff)가 모든 CTA/헤딩/바디/헤더/푸터를 담당
- 파스텔 "컬러블록" 섹션(lime/lilac/cream/mint/pink/coral/navy) — Phase 2 대상, 이번엔 미적용
- 버튼은 전부 알약형(pill, radius 50px), 아이콘 버튼은 원형(radius 9999px) — 사각 버튼 없음
- `figmaSans`(가변 굵기 320/330/340/480/540/700), `figmaMono`(eyebrow/caption 전용, 대문자)
- 그림자를 거의 안 씀 — 컬러블록 자체가 깊이감 역할, 카드는 헤어라인 테두리만
- spacing 8px 기반 스케일, 헤더 높이 56px, 버튼 padding 10px 20px

## 폰트 결정 (원본과 다르게 가는 유일한 지점)

`figmaSans`/`figmaMono`는 한글 글리프가 없는 라틴 전용 서체다. 이 사이트는 본문 대부분이
한글이므로 그대로 쓰면 한글 텍스트는 아무 변화 없이 기존 폴백 폰트로 렌더링되고 만다.
따라서:

- **본문/헤딩**: 기존 Pretendard Variable 유지 (한글 대응 + 이미 지오메트릭 산세리프 성격이
  figmaSans와 결이 비슷함). 가변 굵기 축으로 위계를 표현하는 원칙만 Figma 방식에 맞춰 가져온다.
- **eyebrow/caption(영문·숫자 라벨 전용)**: `figmaMono` 역할을 JetBrains Mono로 대체.
  CDN(cdnjs 등)이 아니라 로컬에 폰트 파일을 번들해야 하면 이번 Phase 1 범위에서 웹폰트 로딩
  방식을 정한다 (제품/솔루션 라벨에 이미 쓰이는 대문자 라벨류가 대상).

## 색상 치환

| 기존 (SUNFLEX 블루 리스킨 후) | 신규 (Figma 모노크롬) |
|---|---|
| `--color-ink: oklch(18.4% .042 260.2)` (남색 틴트) | `--color-ink: #000000` (순수 블랙) |
| `--color-accent` 계열 (블루, 버튼/링크 강조) | 버튼 primary = 블랙/화이트로 대체 (액센트 컬러 개념 자체를 버튼에서 제거) |
| `--color-focus` (블루 포커스 링) | 블랙 기반 포커스 링으로 대체 |
| 헤더 `data-surface="glass"` 반투명 블러 | 완전 불투명 화이트 배경 |

`--moving-*` 오감 배지 색상, `--color-safety`/`--color-danger` 시맨틱 색상은 이번 범위 밖 —
그대로 유지.

## 버튼

- `.button--primary`: 배경 `--color-ink`(블랙), 텍스트 화이트, `border-radius: var(--radius-capsule)`(알약형),
  글로시 오버레이(`:before`/`:after` gloss)·그림자 제거
- `.button--secondary`: 배경 화이트, 텍스트 블랙, 헤어라인 테두리 1px, 알약형, 그림자 제거

## 헤더 / 푸터

- 헤더: `data-surface="glass"` 블러 제거 → 불투명 화이트, 텍스트 블랙, 높이 56px 기준으로 정리
- 푸터: 화이트 배경, 블랙 텍스트 (현재도 밝은 배경이라 텍스트 색상 위주로 조정)

## 검증

- 로컬 정적 서버로 홈/제품 상세/회사소개 페이지를 렌더링해 헤더가 불투명 화이트인지,
  버튼이 전부 알약형 블랙/화이트인지, 그림자가 제거됐는지 스크린샷으로 확인
- 62개 페이지 전체가 공용 CSS(`BaseLayout.a023156454.css`, `ProductPageShell.z7b2aNVH.css`
  등)를 참조하므로 해당 파일들만 수정하면 전체 페이지에 반영되는지 확인

## 범위 밖 (Phase 2+)

- 홈페이지 컬러블록 스토리텔링 섹션 신규 제작
- 회사소개/솔루션/문의 페이지 고유 레이아웃 재작업
- `--moving-*` 오감 배지, SOLAR 서브브랜드 자산 반영 여부
