"""Buyer-readability treatment for the 이동식 CCTV detail sections.

This runs after the source detail has been converted to the editorial shell.  It
does not change source specifications or model codes; it only gives the existing
facts a clearer selection and installation order.
"""
from bs4 import BeautifulSoup


def _tag(soup, name, attrs=None, text=None):
    node = soup.new_tag(name, attrs=attrs or {})
    if text is not None:
        node.string = text
    return node


def _add_class(node, name):
    classes = node.get('class', [])
    if name not in classes:
        classes.append(name)
    node['class'] = classes


def _make_model_selector(soup, root):
    section = root.select_one('#mobile-cctv-lineup')
    if not section or section.select_one('.buyer-model-selector'):
        return
    grid = section.select_one('.content-grid')
    if not grid:
        return
    header = section.select_one('header')
    if header:
        _add_class(header, 'buyer-section-intro')
        if not header.select_one('.buyer-section-eyebrow'):
            kicker = _tag(soup, 'p', {'class': 'buyer-section-eyebrow'}, '크기와 통신을 먼저 고르세요')
            header.insert(0, kicker)
    # Keep the original model-panels host, panel IDs and ARIA ownership. The
    # existing controller changes each article into a tabpanel after hydration.
    _add_class(grid, 'buyer-model-selector')
    for article in grid.find_all('article', recursive=False):
        title = article.select_one('h3')
        model = title.get_text(' ', strip=True).replace('무빙캠 ', '') if title else ''
        _add_class(article, 'buyer-model-card')
        article['data-buyer-model'] = model
        prompt = article.select_one(':scope > p')
        if prompt:
            _add_class(prompt, 'buyer-model-summary')
        codes = article.select_one('ul')
        if codes:
            _add_class(codes, 'buyer-model-codes')
            codes['aria-label'] = f'무빙캠 {model} 통신별 모델 코드'
        figure = article.select_one('figure')
        if figure:
            _add_class(figure, 'buyer-model-photo')
            figcaption = figure.select_one('figcaption')
            if figcaption:
                figcaption.decompose()
        detail = article.find_all('p', recursive=False)
        if detail:
            _add_class(detail[-1], 'buyer-model-detail')


def _make_network_matrix(soup, root):
    section = root.select_one('#movingcam-network')
    if not section or section.select_one('.buyer-network-matrix'):
        return
    table = section.select_one('table')
    if not table:
        return
    holder = _tag(soup, 'div', {'class': 'buyer-network-matrix'})
    table.extract()
    table['class'] = table.get('class', []) + ['buyer-network-table']
    holder.append(table)
    example = section.select_one('.content-grid > p')
    if example:
        example.extract()
        example['class'] = example.get('class', []) + ['buyer-network-example']
        holder.append(example)
    section.select_one('.content-grid').replace_with(holder)
    notes = section.select_one('dl')
    if notes:
        _add_class(notes, 'buyer-network-notes')
    section['data-buyer-section'] = 'network'


def _make_installation_flow(soup, root):
    process = root.select_one('#moving-control-pin .cctv-process')
    if process:
        _add_class(process, 'buyer-install-process')
        detail = process.select_one('.cctv-process-detail')
        if detail:
            _add_class(detail, 'buyer-install-detail')
        source_checks = root.select_one('#moving-control-pin > .editorial-section-inner > div > dl')
        if source_checks:
            _add_class(source_checks, 'buyer-install-source-checks')
    engineering = root.select_one('#movingcam-engineering')
    if engineering and not engineering.select_one('.buyer-install-flow'):
        source = engineering.select_one('dl')
        if source:
            flow = _tag(soup, 'ol', {'class': 'buyer-install-flow', 'aria-label': '무빙캠 설치 위치를 고르는 순서'})
            for row in source.find_all('div', recursive=False):
                item = _tag(soup, 'li')
                dt = row.select_one('dt')
                dd = row.select_one('dd')
                label = _tag(soup, 'span', {'class': 'buyer-flow-model'}, dt.get_text(' ', strip=True) if dt else '')
                copy = _tag(soup, 'p', {'class': 'buyer-flow-copy'}, dd.get_text(' ', strip=True) if dd else '')
                item.append(label); item.append(copy); flow.append(item)
            source.replace_with(flow)
        else:
            flow = _tag(soup, 'ol', {'class': 'buyer-install-flow', 'aria-label': '무빙캠 설치 위치를 고르는 순서'})
            for model, copy in [
                ('무빙캠 S', '촬영 위치를 자주 바꾸는 곳의 휴대 구성을 살펴봅니다.'),
                ('무빙캠 M', '설치할 바닥과 고정 방식을 함께 확인합니다.'),
                ('무빙캠 L', '필요한 촬영 높이와 이동 경로를 함께 검토합니다.'),
            ]:
                item = _tag(soup, 'li')
                item.append(_tag(soup, 'span', {'class': 'buyer-flow-model'}, model))
                item.append(_tag(soup, 'p', {'class': 'buyer-flow-copy'}, copy))
                flow.append(item)
            (engineering.select_one('.revision-visible-detail') or engineering).append(flow)
        engineering['data-buyer-section'] = 'installation'
    coverage = root.select_one('#movingcam-coverage')
    if coverage and not coverage.select_one('.buyer-relocation-checks'):
        figure = coverage.select_one('figure')
        if figure:
            # This photo repeats the S product image and does not explain the
            # relocation check. The product remains represented in the selector.
            figure.decompose()
        detail = coverage.select_one('.revision-visible-detail') or coverage
        checks = _tag(soup, 'ol', {'class': 'buyer-relocation-checks', 'aria-label': '이설 후 확인 순서'})
        for number, title, copy in [
            ('01', '촬영 범위 다시 맞춤', '작업 동선과 장비 접근 구간이 화면에 들어오는지 확인합니다.'),
            ('02', '전원·통신 연결 확인', '설치 위치의 전원 방식과 무선망 또는 LTE 연결 상태를 확인합니다.'),
            ('03', '관제 화면에서 확인', '바뀐 작업면이 관제 화면에서 확인되는지 살펴봅니다.'),
        ]:
            item = _tag(soup, 'li')
            item.append(_tag(soup, 'span', {'aria-hidden': 'true'}, number))
            body = _tag(soup, 'div'); body.append(_tag(soup, 'strong', text=title)); body.append(_tag(soup, 'p', text=copy)); item.append(body); checks.append(item)
        detail.append(checks)
        coverage['data-buyer-section'] = 'relocation'


def _remove_gallery_caption_duplicates(root):
    gallery = root.select_one('#detail-8 .editorial-diagram')
    if not gallery:
        return
    _add_class(gallery, 'buyer-model-gallery')
    for item in gallery.find_all('div', recursive=False):
        figure = item.select_one('figure')
        outer = item.select_one(':scope > figcaption')
        if figure:
            inner = figure.select_one('figcaption')
            if inner:
                inner.decompose()
        if outer:
            _add_class(outer, 'buyer-gallery-label')


def refine_mobile(soup, root):
    """Return the same soup after the mobile-CCTV buyer-readability treatment."""
    _make_model_selector(soup, root)
    _make_network_matrix(soup, root)
    _make_installation_flow(soup, root)
    _remove_gallery_caption_duplicates(root)
    for card in root.select('#mobile-cctv-lineup .buyer-model-card'):
        if card.select_one('.buyer-model-copy'):
            continue
        copy = _tag(soup, 'div', {'class':'buyer-model-copy'})
        for child in list(card.find_all(recursive=False)):
            if child.name != 'figure':
                copy.append(child.extract())
        card.append(copy)
    return soup


def refine_installation_brief(soup, root):
    """Replace the repeated relocation diagram with a useful installation brief.

    Run after external-context conversion, including when normalizing old pages.
    The photographic three-step story remains the single explanation of moving.
    """
    section = root.select_one('#moving-control-pin')
    if not section or section.select_one('#movingcam-installation-brief'):
        return
    process = section.select_one('.cctv-process')
    if not process:
        return
    for repeated in process.select(':scope > .external-detail-context, :scope > .cctv-process-detail'):
        repeated.decompose()
    checks = section.select_one('.buyer-install-source-checks')
    if checks:
        checks.decompose()
    note = process.select_one('.cctv-process-note')
    if note:
        note.string = '현장 이해를 돕는 연출 이미지입니다. 실제 설치 구성은 현장 조건에 따라 달라집니다.'
    brief = BeautifulSoup('''
<section class="buyer-install-brief" id="movingcam-installation-brief" aria-labelledby="movingcam-installation-title">
  <div class="buyer-install-intro">
    <p class="buyer-install-eyebrow">설치·이설 전 확인</p>
    <h3 id="movingcam-installation-title">옮길 자리가 정해졌다면,<br>설치 조건을 확인하세요.</h3>
    <p class="buyer-install-lead">촬영할 구간과 현장의 전원·통신 여건을 알려주세요. 조건에 맞는 무빙캠 구성을 함께 검토합니다.</p>
    <a class="buyer-install-cta" href="/contact/?product=mobile-cctv">우리 현장에 맞는 구성 상담 <span aria-hidden="true">↗</span></a>
  </div>
  <dl class="buyer-install-conditions">
    <div><dt>촬영 범위</dt><dd><strong>작업 동선과 장비 주변</strong><p>옮긴 위치에서 필요한 작업 구간이 화면에 들어오는지 확인합니다.</p></dd></div>
    <div><dt>전원 방식</dt><dd><strong>상시전원·배터리·태양광 충전</strong><p>설치 위치에서 사용할 수 있는 전원에 맞춰 구성을 선택합니다.</p></dd></div>
    <div><dt>통신 방식</dt><dd><strong>WiFi형(W) 또는 LTE형(L)</strong><p>설치 위치의 무선망 연결 또는 LTE 수신 상태를 확인합니다.</p><a href="#movingcam-network">통신 방식과 모델명 확인 <span aria-hidden="true">↗</span></a></dd></div>
  </dl>
</section>
''', 'html.parser').section
    process.insert_after(brief)
