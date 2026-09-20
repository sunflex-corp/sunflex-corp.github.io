(() => {
  'use strict';
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#mobile-nav');
  if (toggle && nav) {
    const close = (focus = false) => {
      nav.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = '메뉴';
      if (focus) toggle.focus();
    };
    // Without JavaScript the mobile navigation remains available.
    toggle.hidden = false;
    close();
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      nav.hidden = !open;
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? '닫기' : '메뉴';
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !nav.hidden) close(true);
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
    window.matchMedia('(min-width: 761px)').addEventListener('change', event => { if (event.matches) close(); });
  }
  const form = document.querySelector('#inquiry-form');
  if (!form) return;
  const status = document.querySelector('#inquiry-status');
  const makeDraft = () => {
    const data = new FormData(form);
    return ['썬플렉스 도입 문의', '', ...[
      ['현장 유형', 'field'], ['설치·관리할 구역', 'area'], ['관심 제품·필요한 기능', 'need'],
      ['전원·통신 조건', 'connection'], ['회신 연락처', 'reply']
    ].map(([label, key]) => `${label}: ${String(data.get(key) || '').trim() || '미정'}`)].join('\n');
  };
  form.addEventListener('submit', event => {
    event.preventDefault();
    window.location.href = 'mailto:jiyoueng@daum.net?subject=' + encodeURIComponent('썬플렉스 도입 문의') + '&body=' + encodeURIComponent(makeDraft());
    status.textContent = '이메일 앱에서 내용을 확인한 뒤 직접 보내주세요. 앱이 열리지 않으면 문의 내용 복사를 이용하세요.';
  });
  document.querySelector('#copy-inquiry').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(makeDraft());
      status.textContent = '문의 내용을 복사했습니다. 이메일에 붙여 넣어 보내주세요.';
    } catch {
      const draft = document.querySelector('#draft-fallback');
      draft.hidden = false;
      draft.querySelector('textarea').value = makeDraft();
      draft.querySelector('textarea').focus();
      draft.querySelector('textarea').select();
      status.textContent = '아래 내용을 선택해 복사한 뒤 이메일에 붙여 넣어 주세요.';
    }
  });
  document.querySelector('.form-actions').hidden = false;
})();
