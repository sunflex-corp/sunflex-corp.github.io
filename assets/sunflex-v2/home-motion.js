(() => {
  'use strict';
  const hero = document.querySelector('.cinema');
  if (!hero) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const slides = [...hero.querySelectorAll('.scene')];
  const selectors = [...hero.querySelectorAll('[data-select]')];
  const play = hero.querySelector('[data-play]');
  const caption = hero.querySelector('.scene-caption');
  const scenes = [
    ['건설·토목', '시야가 닿기 어려운 곳까지', '인양 구역과 작업 동선을 영상으로 확인하세요.'],
    ['제조·물류', '차량과 사람이 만나는 현장', '이동 구역에 필요한 접근 경보와 안내 장비를 살펴보세요.'],
    ['현장 운영', '현장의 변화를 확인하는 기술', '영상과 측정 정보를 활용해 현장 관리에 필요한 정보를 확인하세요.']
  ];
  const duration = 7000;
  let current = 0, timer = null, progress = null, request = 0;
  let paused = reduced.matches, inView = true, hovering = false;
  const stop = () => { clearTimeout(timer); timer = null; if (progress) progress.cancel(); progress = null; };
  const updatePlayback = () => {
    stop();
    hero.classList.toggle('is-paused', paused || hovering || !inView || document.hidden);
    play.textContent = reduced.matches ? '다음 장면' : paused ? '자동 재생' : '일시정지';
    play.setAttribute('aria-label', reduced.matches ? '다음 장면으로 이동' : paused ? '장면 자동 전환 시작' : '자동 전환 일시정지');
    caption.setAttribute('aria-live', paused ? 'polite' : 'off');
    if (paused || hovering || !inView || document.hidden || reduced.matches) return;
    const bar = selectors[current].querySelector('i');
    if (bar.animate) progress = bar.animate([{transform:'scaleX(0)'},{transform:'scaleX(1)'}],{duration,easing:'linear',fill:'forwards'});
    timer = setTimeout(() => show(current + 1, false), duration);
  };
  async function show(index, manual = true) {
    const target = (index + slides.length) % slides.length;
    const serial = ++request;
    stop();
    const img = slides[target].querySelector('img');
    img.loading = 'eager';
    try { if (img.decode) await img.decode(); } catch {
      if (serial === request) {
        hero.querySelector('#scene-status').textContent = '이미지를 불러오지 못했습니다. 다른 장면을 선택해 주세요.';
        paused = true; updatePlayback();
      }
      return;
    }
    if (serial !== request) return;
    current = target;
    slides.forEach((slide,i) => { slide.classList.toggle('is-active', i === current); slide.setAttribute('aria-hidden',String(i !== current)); });
    selectors.forEach((button,i) => button.setAttribute('aria-pressed',String(i === current)));
    ['.scene-topic','.scene-title','.scene-description'].forEach((selector,i) => { caption.querySelector(selector).textContent = scenes[current][i]; });
    caption.classList.remove('changing'); void caption.offsetWidth; caption.classList.add('changing');
    if (manual) { paused = true; hero.querySelector('#scene-status').textContent = `${current+1} / ${slides.length} · ${scenes[current][0]}`; }
    hero.dataset.current = String(current);
    updatePlayback();
  }
  selectors.forEach((button,i) => button.addEventListener('click', () => show(i)));
  hero.querySelector('[data-next]').addEventListener('click', () => show(current+1));
  hero.querySelector('[data-prev]').addEventListener('click', () => show(current-1));
  play.addEventListener('click', () => { if (reduced.matches) { show(current+1); return; } ++request; paused = !paused; updatePlayback(); });
  // Keyboard interaction pauses rotation until the visitor explicitly restarts it.
  hero.addEventListener('focusin', event => { if (event.target !== play) { ++request; paused = true; updatePlayback(); } });
  hero.addEventListener('pointerenter', event => { if (event.pointerType === 'mouse') { hovering = true; updatePlayback(); } });
  hero.addEventListener('pointerleave', () => { hovering = false; updatePlayback(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) ++request; updatePlayback(); });
  reduced.addEventListener('change', () => { ++request; paused = true; updatePlayback(); });
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => { inView = entries[0].isIntersecting; if (!inView) ++request; updatePlayback(); },{threshold:.15}).observe(hero);
  hero.querySelector('.scene-controls').hidden = false;
  hero.dataset.current = '0';
  updatePlayback();

  const map = document.querySelector('.map-visual');
  if (!map) return;
  const mapMotion = document.querySelector('.map-motion-toggle');
  if (mapMotion) {
  mapMotion.hidden = false;
  mapMotion.addEventListener('click', () => {
    const off = map.classList.toggle('motion-off');
    mapMotion.setAttribute('aria-pressed', String(off));
    mapMotion.textContent = off ? '그래픽 재생' : '그래픽 정지';
  });
  }
  const choices = [...document.querySelectorAll('[data-map-choice]')];
  const panels = [...document.querySelectorAll('.map-panel')];
  choices.forEach((button,index) => button.addEventListener('click', () => {
    choices.forEach((b,i) => b.setAttribute('aria-pressed',String(i === index)));
    panels.forEach((panel,i) => { panel.hidden = i !== index; });
    document.querySelectorAll('.family-scene').forEach((scene,i) => scene.setAttribute('aria-hidden',String(i !== index)));
    map.dataset.mode = String(index);
  }));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); entry.target.classList.remove('will-reveal'); observer.unobserve(entry.target); }
    }),{threshold:.08});
    const targets = document.querySelectorAll('main .lead, main .field-row, main .feature-visual, main .feature-copy, main .product-spotlight, main .company-band .copy, main .resource-list, main .final-cta');
    targets.forEach((element,i) => {
      element.dataset.reveal = '';
      element.style.setProperty('--reveal-delay',`${i % 3 * 70}ms`);
      if (!reduced.matches && element.getBoundingClientRect().top > window.innerHeight) element.classList.add('will-reveal');
      observer.observe(element);
    });
    new IntersectionObserver(entries => map.classList.toggle('is-visible',entries[0].isIntersecting),{threshold:.1}).observe(map);
  } else map.classList.add('is-visible');
})();
