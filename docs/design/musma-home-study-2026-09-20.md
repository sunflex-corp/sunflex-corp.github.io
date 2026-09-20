# MUSMA reference study and SUNPLEX homepage simplification

Reference: https://musma.net/ (user-corrected domain). Inspected in visible Chrome from hero through footer, including the intermediate pinned-scroll states, upward-scroll header return, hardware category switching and detailed descriptions. Public HTML and the page bundle were read to distinguish final layouts from transitional states. No MUSMA assets or source code were incorporated.

## Observed structure

| Order | Reference section | Design / interaction observation |
|---|---|---|
| 1 | Hero | Full viewport video, transparent overlaid navigation, large left-aligned sentence, short supporting line, downward cue. |
| 2 | Business | Two business directions, orange/blue distinction, centered introduction, generous space and staged entry. |
| 3 | Safety brand | Large brand lettering becomes an image mask, expands into a full scene, then reveals brief copy and one detail link. |
| 4 | DX | Light title interlude into image-led content; category selection changes the description. |
| 5 | Hardware | Dark section, primary category and secondary device selectors; image beside a description and application tags. |
| 6 | Performance | Four large numerical facts with short labels on a subtle technical background. |
| 7 | Clients | A restrained horizontal logo strip. |
| 8 | News | Three image-led cards, date/source, short text and one detail action. |
| 9 | Contact / footer | One centered inquiry action, followed by a compact company/navigation footer on a contrasting light surface. |

The header is transparent at the top, disappears when scrolling down and returns with a dark translucent background when scrolling up. Inspection confirmed long pinned sequences on the reference (several viewport heights), rather than many independent content blocks.

## SUNPLEX adaptation

The homepage now has four main sections instead of seven. Main text fell from 1,736 to 641 characters as measured with BeautifulSoup `get_text(' ', strip=True)`; this includes nonvisual slide descriptions and the word in the reveal mask.

1. Full viewport existing three-image sequence, concise headline and a single Solar link. One-row transparent header replaces the two-row home header.
2. Four selectable Solar families in one region. An original SVG Solar word mask expands to reveal an existing SUNPLEX scene once; selections change the image, description and product-family link.
3. Three representative products and an all-products link.
4. One inquiry section, secondary company/support links and a quieter footer.

Long installation guidance, repeated industry introductions and resource lists now remain on their dedicated pages. No numerical performance claims, client logos or news were invented to mimic MUSMA. Existing image assets and the SUNPLEX design palette remain in use. A short reveal inside the Solar image replaces long pinned scroll sequences, keeping the page compact.

## Scope and verification

Home-only CSS and JavaScript keep all 65 non-home HTML pages byte-for-byte unchanged. Carousel controls, pause, keyboard interaction, reduced motion and no-JS fallback remain. The header stays visible during keyboard focus and while the mobile menu is open. The photo is visible without JavaScript and the mask is disabled for reduced motion.

Checks: 66-route static validation; product source preservation; carousel tests including a homepage without the old diagram pause button; header direction/focus/menu tests; reveal completion, manual override and reduced-motion tests. Visible Chrome: transparent desktop hero, downward hide/upward return, Record photo/copy switch, 320px and 390px mobile with no horizontal overflow or broken loaded images, mobile menu and Alert selection. Publication is verified separately against the matching GitHub Pages commit.

## 사용자 피드백 후 전환 구조 재구현

기존 작은 사진 영역의 1회 IntersectionObserver 확대는 레퍼런스의 핵심인 스크롤 진행과 화면 고정을 재현하지 못했다. 해당 결정을 폐기하고 독립적인 전체 화면 Solar 브랜드 구간을 추가했다.

- 참고: https://musma.net/#safety — 고정 화면에서 흰 글자 → 이미지가 채워진 확대 글자 → 전체 이미지 → 설명 순서. 실제 브라우저에서 중간 상태까지 확인했다. 코드와 이미지는 복제하지 않았다.
- SUNPLEX: 데스크톱 340svh, 모바일 280svh의 자연 스크롤 구간에 sticky 100svh 무대. 스크롤 위치를 0–1로 정규화한다.
- 9–24% 흰 글자가 사라지고, 12–69% 벡터 글자가 확대된다. 51–69% 마스크가 배경으로 연결되고, 68–84% 설명과 배경 음영이 등장한다. 마지막 구간은 내용을 읽는 시간이다.
- requestAnimationFrame과 시간 기반 감쇠(85ms)로 트랙패드/휠 입력을 부드럽게 연결한다. 역방향도 같은 시간축을 사용하며 입력을 가로채지 않는다. 안정된 후 프레임 요청을 멈춘다.
- 작은 사진의 기존 1회 재생 마스크는 삭제. 브랜드 소개 다음에는 네 가지 기능 선택, 제품, 문의로 이어진다.
- JS 미실행 및 동작 줄이기 설정에서는 고정 스크롤 없이 이미지와 설명을 바로 제공한다. 숨은 설명 링크는 inert로 포커스를 방지한다.
- 검증: 66페이지 링크/자산/48제품 원문 검사, 메인 타임라인 경계·역방향·크기변경·초과 스크롤·동작 줄이기 테스트 및 기존 기능 테스트 통과. Chrome 데스크톱 시작/중간/완료/역방향, 320px 모바일 마스크 및 설명 확인. 모바일 가로 넘침 없음. 홈페이지 외 HTML 변경 없음.
