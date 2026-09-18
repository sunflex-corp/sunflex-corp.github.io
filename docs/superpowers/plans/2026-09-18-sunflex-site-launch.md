# SUNFLEX 신규 사이트 런칭 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 지유이엔지 공식 사이트(`jiyou-eng/jiyou-eng.github.io`)의 빌드 결과물을 베이스로, 회사명과
로고만 SUNFLEX로 치환한 새 정적 사이트를 `jiyou-eng/sunflex-site` 레포에 만들고 GitHub Pages로
배포한다. 지유이엔지 기존 사이트는 전혀 건드리지 않는다.

**Architecture:** Astro 소스 없이 이미 빌드된 정적 HTML/CSS/JS를 그대로 복사해 새 레포의 시작점으로
쓴다. 회사명·URL·로고 파일 참조는 Python 스크립트로 62개 HTML 파일 전체에 걸쳐 기계적으로
일괄 치환한다. 연락처·주소·본문 카피 등 사실관계를 모르는 항목은 건드리지 않고 TODO로 남긴다.

**Tech Stack:** 순수 정적 HTML/CSS/JS, Python 3(치환 스크립트), `sips`/`magick`(ImageMagick, 아이콘
리사이즈), GitHub CLI(`gh`), GitHub Pages

**참조 경로:**
- 새 레포 로컬 작업 디렉토리: `/Users/mac/Documents/지유이엔지/sunflex-site` (이미 git 초기화됨, 설계 문서 1커밋 있음)
- 지유이엔지 사이트 클론(베이스 소스, 읽기 전용): `/Users/mac/Documents/지유이엔지/site`
- SUNFLEX CI 패키지(압축 해제됨, 읽기 전용): `/Users/mac/Downloads/SUNFLEX_SOLAR_Revised_CI_v1.1/SUNFLEX_SOLAR_Reference_Revision_v1.1`

---

### Task 1: GitHub 레포 생성 및 원격 연결

**Files:** 없음 (레포 메타데이터 작업)

- [ ] **Step 1: 새 레포 생성 (아직 push는 하지 않음)**

```bash
cd /Users/mac/Documents/지유이엔지/sunflex-site
gh repo create jiyou-eng/sunflex-site --public \
  --description "썬플렉스(SUNFLEX) 공식 웹사이트" \
  --source=. --remote=origin
```

Expected: `✓ Created repository jiyou-eng/sunflex-site on GitHub` 출력, `git remote -v`에
`origin  https://github.com/jiyou-eng/sunflex-site.git (fetch/push)` 표시됨.

- [ ] **Step 2: 확인**

```bash
gh repo view jiyou-eng/sunflex-site --json name,visibility,isEmpty
```

Expected: `{"isEmpty":true,"name":"sunflex-site","visibility":"PUBLIC"}` (design 문서 커밋을 아직
push하지 않았으므로 GitHub 상 레포는 비어 있는 상태가 정상)

---

### Task 2: 지유이엔지 사이트 빌드 결과물을 베이스로 가져오기

**Files:**
- Copy: `/Users/mac/Documents/지유이엔지/site/*` → `/Users/mac/Documents/지유이엔지/sunflex-site/` (`.git`, `CNAME` 제외)
- Delete: `brand/jiyou-logo.png` (HTML에서 참조하는 곳이 없어 미사용 확인됨)

- [ ] **Step 1: rsync로 복사 (`.git`, `CNAME` 제외)**

```bash
cd /Users/mac/Documents/지유이엔지/sunflex-site
rsync -a --exclude='.git' --exclude='CNAME' /Users/mac/Documents/지유이엔지/site/ ./
rm -f brand/jiyou-logo.png
```

- [ ] **Step 2: 복사 결과 확인**

```bash
test -f CNAME && echo "FAIL: CNAME exists" || echo "OK: no CNAME"
test -f brand/jiyou-logo.png && echo "FAIL: jiyou-logo.png exists" || echo "OK: jiyou-logo.png removed"
find . -maxdepth 1 -not -name '.git' -not -name 'docs' -not -name '.' | sort
```

Expected: 두 `echo`가 모두 `OK`로 출력되고, 마지막 `find`에서 `404.html`, `brand`, `cases`,
`company`, `contact`, `downloads`, `favicon.ico`, `favicon.png`, `favicon.svg`, `fonts`,
`index.html`, `media`, `products`, `robots.txt`, `sitemap-0.xml`, `sitemap-index.xml`,
`solutions` 등 62개 페이지에 대응하는 디렉토리/파일들이 보인다.

- [ ] **Step 3: 커밋**

```bash
git add -A
git commit -m "$(cat <<'EOF'
Import jiyou-eng site build output as SUNFLEX site base

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LXQv4Pgf9Fwi8p3AEEZWoX
EOF
)"
```

---

### Task 3: SUNFLEX CI 패키지 전체를 참조용으로 보관

**Files:**
- Create: `brand/sunflex-ci/` (SUNFLEX CI 패키지 전체 복사본)

- [ ] **Step 1: 복사**

```bash
cd /Users/mac/Documents/지유이엔지/sunflex-site
mkdir -p brand/sunflex-ci
rsync -a "/Users/mac/Downloads/SUNFLEX_SOLAR_Revised_CI_v1.1/SUNFLEX_SOLAR_Reference_Revision_v1.1/" brand/sunflex-ci/
```

- [ ] **Step 2: 확인**

```bash
ls brand/sunflex-ci
```

Expected: `01_SOLAR  02_SUNFLEX  03_App_Icons  04_Review  05_Web  06_Specification  README_KO.md`

- [ ] **Step 3: 커밋**

```bash
git add brand/sunflex-ci
git commit -m "$(cat <<'EOF'
Add full SUNFLEX SOLAR CI package for reference

Not wired into any page yet. Contains SOLAR sub-brand lineup/system/
solution layouts, KO CI, and Flat/Ink/White color variants for future
page-by-page use.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LXQv4Pgf9Fwi8p3AEEZWoX
EOF
)"
```

---

### Task 4: 헤더 로고 · 파비콘 자산 교체

**Files:**
- Create: `brand/sunflex-wordmark.svg`, `brand/sunflex-wordmark.png`
- Delete: `brand/jiyou-wordmark.svg`, `brand/jiyou-wordmark.png`
- Modify: `favicon.svg`, `favicon.png`, `favicon.ico`

- [ ] **Step 1: 워드마크 파일 교체**

```bash
cd /Users/mac/Documents/지유이엔지/sunflex-site
cp brand/sunflex-ci/02_SUNFLEX/svg/SUNFLEX_EN_Reference_Primary.svg brand/sunflex-wordmark.svg
cp brand/sunflex-ci/02_SUNFLEX/png/SUNFLEX_EN_Reference_Primary.png brand/sunflex-wordmark.png
rm brand/jiyou-wordmark.svg brand/jiyou-wordmark.png
```

- [ ] **Step 2: 파비콘 교체**

```bash
cp brand/sunflex-ci/03_App_Icons/svg/SOLAR_App_Icon_Blue_Enlarged.svg favicon.svg
sips -z 192 192 brand/sunflex-ci/03_App_Icons/png/SOLAR_App_Icon_Blue_Enlarged.png --out favicon.png
magick brand/sunflex-ci/03_App_Icons/png/SOLAR_App_Icon_Blue_Enlarged.png \
  -define icon:auto-resize=16,32,48,64,128,256 favicon.ico
```

- [ ] **Step 3: 확인**

```bash
file favicon.ico
sips -g pixelWidth -g pixelHeight favicon.png
ls brand/sunflex-wordmark.svg brand/sunflex-wordmark.png
test -f brand/jiyou-wordmark.svg && echo "FAIL: still exists" || echo "OK: removed"
```

Expected:
- `favicon.ico: MS Windows icon resource - ...`
- `pixelWidth: 192` / `pixelHeight: 192`
- 두 `sunflex-wordmark.*` 파일이 정상 존재
- `OK: removed`

- [ ] **Step 4: 커밋**

```bash
git add -A
git commit -m "$(cat <<'EOF'
Swap jiyou wordmark/favicon for SUNFLEX brand assets

Header wordmark -> SUNFLEX_EN_Reference_Primary (symbol + wordmark,
Primary color). Favicon -> SOLAR_App_Icon_Blue_Enlarged (already a
finished square icon asset in the CI package, reused as-is).

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LXQv4Pgf9Fwi8p3AEEZWoX
EOF
)"
```

---

### Task 5: 회사명 · URL 텍스트 일괄 치환 스크립트

**Files:**
- Create: `scripts/rebrand.py`

배경: 사이트 62개 HTML 페이지 전체에서 `지유이엔지`는 951회, `jiyoueng.com`은 626회,
`brand/jiyou-wordmark.svg`는 186회, `brand/jiyou-wordmark.png`는 62회 등장한다 (베이스 복사본
기준 실측치). 반대로 `jiyoueng`이라는 문자열이 `jiyoueng.com`이 아닌 형태로 등장하는 곳(이메일
`jiyoueng@daum.net`, OG 이미지 파일명 `jiyoueng-og.jpg` 등)은 322회이며, 이건 실제 연락처/자산이라
**의도적으로 그대로 둔다** (`jiyoueng.com`이라는 정확한 문자열만 치환 대상).

- [ ] **Step 1: 스크립트 작성**

```python
#!/usr/bin/env python3
"""Rebrand jiyou-eng site HTML pages to SUNFLEX (company name + URL + logo refs only)."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "brand/sunflex-ci"}

# Order matters only in that each pair must not create a substring that a
# later pair would incorrectly match again; none of these overlap.
REPLACEMENTS = [
    ("brand/jiyou-wordmark.svg", "brand/sunflex-wordmark.svg"),
    ("brand/jiyou-wordmark.png", "brand/sunflex-wordmark.png"),
    ("jiyoueng.com", "jiyou-eng.github.io/sunflex-site"),
    ("지유이엔지", "썬플렉스"),
]


def is_excluded(path: pathlib.Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(rel == d or rel.startswith(d + "/") for d in EXCLUDE_DIRS)


def main() -> None:
    changed_files = 0
    total_replacements = 0
    for html_path in sorted(ROOT.rglob("*.html")):
        if is_excluded(html_path):
            continue
        text = html_path.read_text(encoding="utf-8")
        original = text
        file_count = 0
        for old, new in REPLACEMENTS:
            file_count += text.count(old)
            text = text.replace(old, new)
        if text != original:
            html_path.write_text(text, encoding="utf-8")
            changed_files += 1
            total_replacements += file_count
            print(f"{html_path.relative_to(ROOT)}: {file_count} replacements")
    print(f"\nTotal: {changed_files} files changed, {total_replacements} replacements")


if __name__ == "__main__":
    main()
```

Write this to `/Users/mac/Documents/지유이엔지/sunflex-site/scripts/rebrand.py` (create the
`scripts/` directory first if it doesn't exist).

- [ ] **Step 2: 실행**

```bash
cd /Users/mac/Documents/지유이엔지/sunflex-site
mkdir -p scripts
python3 scripts/rebrand.py
```

Expected: 62개 파일 각각에 대해 `<path>: N replacements` 줄이 출력되고, 마지막 줄이
`Total: 62 files changed, 1825 replacements` (186 + 62 + 626 + 951 = 1825)로 끝난다.
`changed_files`가 62보다 작으면 어떤 페이지가 치환 대상에서 빠졌다는 뜻이므로 원인을 찾아야 한다.

- [ ] **Step 3: 잔존 여부 검증**

```bash
grep -rl "지유이엔지" --include="*.html" . --exclude-dir=brand
grep -rl "jiyoueng\.com" --include="*.html" . --exclude-dir=brand
grep -ro "jiyoueng" --include="*.html" -r . --exclude-dir=brand | wc -l
```

Expected: 첫 두 `grep -rl` 명령은 **아무것도 출력하지 않아야 한다** (완전히 치환됨).
세 번째 명령(순수 `jiyoueng` 문자열 카운트, `jiyoueng.com`도 포함해서 셈)은 `322`가 나와야
한다 — 이건 이메일(`jiyoueng@daum.net`)과 OG 이미지 파일명(`jiyoueng-og.jpg`) 등 의도적으로
남겨둔 항목의 개수이며, 스크립트 실행 전후로 이 숫자가 변하지 않아야 정상이다.

- [ ] **Step 4: 커밋**

```bash
git add -A
git commit -m "$(cat <<'EOF'
Rebrand company name, canonical URLs, and logo refs to SUNFLEX

Mechanical find-and-replace across all 62 HTML pages via scripts/rebrand.py:
- 지유이엔지 -> 썬플렉스 (title, meta, JSON-LD, alt/aria-label text)
- jiyoueng.com -> jiyou-eng.github.io/sunflex-site (canonical/og:url)
- brand/jiyou-wordmark.{svg,png} -> brand/sunflex-wordmark.{svg,png}

Left untouched intentionally: phone number, jiyoueng@daum.net email,
factory addresses, Naver blog link, internal portal link, and all
product/solution body copy — tracked in SUNFLEX_TODO.md for manual review.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LXQv4Pgf9Fwi8p3AEEZWoX
EOF
)"
```

---

### Task 6: TODO 체크리스트 작성

**Files:**
- Create: `SUNFLEX_TODO.md`

- [ ] **Step 1: 파일 작성**

```markdown
# SUNFLEX 사이트 후속 작업 체크리스트

이번 1차 작업은 지유이엔지 사이트를 베이스로 **회사명과 로고만** SUNFLEX로 기계적으로
치환한 것입니다. 아래 항목은 실제 정보가 확정되면 직접 채워 넣어야 합니다.

## 사실관계 확인 필요 (임의로 지어내지 않고 그대로 둔 항목)

- [ ] 법인 등기명 확인 — 현재 JSON-LD `alternateName`에 `(주)썬플렉스`로 기본값을 넣어뒀는데,
      실제 등기명과 다르면 전체 페이지에서 재치환 필요 (`scripts/rebrand.py`에 규칙 추가 후 재실행)
- [ ] 전화번호 `031-991-2285` — SUNFLEX 전용 번호로 교체할지, 지유이엔지와 공유할지 결정
- [ ] 이메일 `jiyoueng@daum.net` — SUNFLEX 전용 주소로 교체
- [ ] 공장 주소(경기도 김포시 양촌읍 / 경기도 시흥시 신천동) — SUNFLEX 실제 사업장 주소로 교체
- [ ] 네이버 블로그 링크(`blog.naver.com/jiyou_eng`) — SUNFLEX 전용 블로그가 있으면 교체, 없으면 제거
- [ ] 헤더의 "사내 포털" 링크 — SUNFLEX 직원용 포털이 따로 있는지 확인, 없으면 제거

## 도메인

- [ ] 실제 도메인 확정 시 `scripts/rebrand.py`의 `jiyou-eng.github.io/sunflex-site` 규칙을
      새 도메인으로 바꿔 재실행하고, 레포 루트에 `CNAME` 파일 추가

## 콘텐츠

- [ ] 제품/솔루션 각 페이지 본문 카피에 지유이엔지 특유 표현이 남아있는지 페이지별로 검토
- [ ] OG 소셜 공유 이미지(`media/og/jiyoueng-og.jpg`)를 SUNFLEX 전용 이미지로 교체할지 검토
- [ ] `brand/sunflex-ci/`에 보관된 SOLAR 서브 브랜드 레이아웃(라인업/시스템/솔루션),
      Flat/Ink/White 색상 변형, 한글(KO) CI를 실제 페이지에 적용할지 검토
```

- [ ] **Step 2: 커밋**

```bash
cd /Users/mac/Documents/지유이엔지/sunflex-site
git add SUNFLEX_TODO.md
git commit -m "$(cat <<'EOF'
Add SUNFLEX_TODO.md tracking remaining rebrand work

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LXQv4Pgf9Fwi8p3AEEZWoX
EOF
)"
```

---

### Task 7: 로컬 검증

**Files:** 없음 (검증만 수행)

- [ ] **Step 1: 로컬 정적 서버 기동**

```bash
cd /Users/mac/Documents/지유이엔지/sunflex-site
python3 -m http.server 8123 >/tmp/sunflex-site-server.log 2>&1 &
echo $! > /tmp/sunflex-site-server.pid
sleep 1
```

- [ ] **Step 2: 홈페이지 핵심 요소 확인**

```bash
curl -s http://localhost:8123/ | grep -o "<title>[^<]*</title>"
curl -s http://localhost:8123/ | grep -o 'brand/sunflex-wordmark\.svg' | head -1
curl -s http://localhost:8123/ | grep -o 'aria-label="[^"]*홈"'
```

Expected:
- `<title>썬플렉스 | 현장 안전 운영</title>`
- `brand/sunflex-wordmark.svg`
- `aria-label="썬플렉스 홈"`

- [ ] **Step 3: 회사소개/문의 페이지도 확인**

```bash
curl -s http://localhost:8123/company/ | grep -o "<title>[^<]*</title>"
curl -s http://localhost:8123/contact/ | grep -o "<title>[^<]*</title>"
```

Expected: `<title>회사소개 | 썬플렉스</title>`, `<title>현장 조건 상담 | 썬플렉스</title>`

- [ ] **Step 4: 서버 종료**

```bash
kill "$(cat /tmp/sunflex-site-server.pid)"
rm /tmp/sunflex-site-server.pid /tmp/sunflex-site-server.log
```

---

### Task 8: GitHub에 push하고 Pages 활성화

**Files:** 없음

- [ ] **Step 1: push**

```bash
cd /Users/mac/Documents/지유이엔지/sunflex-site
git push -u origin master
```

Expected: `Branch 'master' set up to track remote branch 'master' from 'origin'.` 및 push 성공 로그

- [ ] **Step 2: GitHub Pages 활성화**

```bash
gh api --method POST repos/jiyou-eng/sunflex-site/pages \
  -f "source[branch]=master" -f "source[path]=/"
```

Expected: JSON 응답에 `"status":"building"` 또는 `"status":null`과 함께
`"html_url":"https://jiyou-eng.github.io/sunflex-site/"` 포함.

만약 권한 오류(403/404)가 나면, 브라우저에서
`https://github.com/jiyou-eng/sunflex-site/settings/pages`로 들어가 Source를
`Deploy from a branch` / Branch `master` / `/ (root)`로 수동 설정한다.

- [ ] **Step 3: 배포 확인 (1~2분 대기 후)**

```bash
sleep 90
curl -s -o /dev/null -w "%{http_code}\n" https://jiyou-eng.github.io/sunflex-site/
```

Expected: `200`. `404`가 나오면 Pages 빌드가 아직 안 끝난 것이니 30초 더 기다렸다가 재시도.

---

## 완료 기준

- [ ] `jiyou-eng/sunflex-site` 레포가 GitHub에 존재하고 public
- [ ] `https://jiyou-eng.github.io/sunflex-site/`가 200으로 응답
- [ ] 홈/회사소개/문의 페이지 title과 헤더 로고가 SUNFLEX 기준으로 바뀜
- [ ] `지유이엔지`, `jiyoueng.com` 문자열이 사이트 어디에도 남아있지 않음 (email/OG 이미지 제외)
- [ ] `SUNFLEX_TODO.md`에 남은 수작업 항목이 정리되어 있음
- [ ] 기존 `jiyou-eng/jiyou-eng.github.io` 레포는 전혀 수정되지 않음
