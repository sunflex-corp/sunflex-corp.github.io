(() => {
  'use strict';
  const section = document.querySelector('.home-families');
  if (!section) return;
  const stage = section.querySelector('.families-stage');
  const choices = [...section.querySelectorAll('[data-map-choice]')];
  const panels = [...section.querySelectorAll('.map-panel')];
  const scenes = [...section.querySelectorAll('.family-scene')];
  const visual = section.querySelector('.map-visual');
  const counter = section.querySelector('.families-count');
  const guidance = section.querySelector('.families-guidance > span');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let active = -1, pinned = false, start = 0, step = 1, frame = 0;
  section.querySelector('.map-panels').setAttribute('aria-live', 'off');
  // Keep both panels rendered for a real crossfade; inert prevents hidden links taking focus.
  panels.forEach(panel => { panel.hidden = false; });
  section.classList.add('is-enhanced');
  function select(index) {
    if (index === active) return;
    active = index;
    section.dataset.family = String(index);
    visual.dataset.mode = String(index);
    choices.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
    panels.forEach((panel, i) => {
      panel.classList.toggle('is-active', i === index);
      panel.inert = i !== index;
      panel.setAttribute('aria-hidden', String(i !== index));
    });
    scenes.forEach((scene, i) => scene.setAttribute('aria-hidden', String(i !== index)));
    counter.textContent = `0${index + 1} / 04`;
  }
  function update() {
    frame = 0;
    if (!pinned) return;
    const y = window.scrollY;
    const position = (y - start) / step;
    let next = Math.max(0, Math.min(3, Math.floor(position)));
    // A small dead band avoids flickering between adjacent steps around a boundary.
    if (next === active + 1 && position < next + .035) next = active;
    if (next === active - 1 && position > active - .035) next = active;
    const focusedPanel = panels[active];
    // When natural scrolling changes the visible panel, keep keyboard focus in this region.
    if (next !== active && focusedPanel?.contains(document.activeElement)) choices[next].focus({preventScroll:true});
    select(next);
    // Update only the active underline, at the same cadence as native scrolling.
    const progress = Math.max(0, Math.min(1, position - active)).toFixed(4);
    if (choices[active].style.getPropertyValue('--family-progress') !== progress)
      choices[active].style.setProperty('--family-progress', progress);
  }
  const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };
  function configure() {
    const viewport = document.documentElement.clientHeight;
    const top = matchMedia('(max-width:760px)').matches ? 76 : 82;
    section.style.setProperty('--family-view-height', `${viewport - top}px`);
    step = Math.max(380, viewport * .82);
    section.style.setProperty('--family-travel', `${step * 4}px`);
    pinned = !reduced.matches && viewport >= 580;
    section.classList.toggle('is-pinned', pinned);
    if (pinned) {
      const bounds = stage.getBoundingClientRect();
      const content = section.querySelector('.home-family-layout');
      const image = visual.getBoundingClientRect();
      // Measure layout boxes, not scrollHeight: the outgoing panel's 16px
      // transform is a visual transition, not additional content height.
      const panelHeight = section.querySelector('.map-panels').offsetHeight;
      const needed = matchMedia('(max-width:760px)').matches
        ? visual.offsetHeight + panelHeight + parseFloat(getComputedStyle(content).rowGap)
        : Math.max(visual.offsetHeight, panelHeight);
      const overflows = stage.scrollHeight > stage.clientHeight + 2 || needed > content.clientHeight + 2 || image.height < 119;
      if (overflows || bounds.height < 400) { pinned = false; section.classList.remove('is-pinned'); }
    }
    start = section.getBoundingClientRect().top + window.scrollY - top;
    guidance.textContent = pinned ? '스크롤하여 솔루션 살펴보기' : '제품군을 선택하여 살펴보기';
    if (pinned) update();
  }
  choices.forEach((button, index) => {
    button.addEventListener('click', () => {
      select(index);
      if (pinned) {
        // Jump to the selected chapter without sweeping through the intervening chapters.
        window.scrollTo({top: start + step * (index + .18), behavior: 'instant'});
        update();
      }
    });
    button.addEventListener('keydown', event => {
      const delta = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0;
      if (!delta && event.key !== 'Home' && event.key !== 'End') return;
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? 3 : (index + delta + 4) % 4;
      choices[next].focus({preventScroll:true});
      choices[next].click();
    });
  });
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', configure);
  addEventListener('pageshow', configure);
  reduced.addEventListener('change', configure);
  // Decode the four images before the reader reaches the pinned sequence.
  if ('IntersectionObserver' in window) {
    const preload = new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) return;
      scenes.forEach(scene => { const img = scene.querySelector('img'); img.loading = 'eager'; if (img.decode) img.decode().catch(() => {}); });
      preload.disconnect();
    }, {rootMargin:'100% 0px'});
    preload.observe(section);
  }
  select(0);
  configure();
  document.fonts.ready.then(configure);
})();
