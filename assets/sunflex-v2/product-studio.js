/* One owner for the gas scene's state; content stays visible without JavaScript. */
(() => {
  'use strict';
  const root = document.querySelector('[data-gas-scene]');
  if (!root) return;
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const panels = [...root.querySelectorAll('.gas-scene-panel')];
  const controls = root.querySelector('.gas-scene-tabs');
  const frame = root.querySelector('.gas-frame-outline');
  let animateFrame = false;
  if (tabs.length !== panels.length || tabs.length === 0) return;
  const select = (index, focus = false) => {
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
      panels[i].setAttribute('role', 'tabpanel');
      panels[i].setAttribute('aria-labelledby', tab.id);
      panels[i].tabIndex = 0;
    });
    root.dataset.gasStep = String(index);
    if (animateFrame) {
      gsap.to(frame, {width: index === 0 ? '46%' : '100%', duration: .75, ease: 'power3.inOut', overwrite: true});
      gsap.to(root.querySelector('.gas-frame-visual img'), {scale: index === 0 ? 1 : .88, duration: .75, ease: 'power3.inOut', overwrite: true});
    }
    if (focus) tabs[index].focus();
    window.ScrollTrigger?.refresh();
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => select(index));
    tab.addEventListener('keydown', e => {
      const next = {ArrowRight: (index + 1) % tabs.length, ArrowLeft: (index + tabs.length - 1) % tabs.length, Home: 0, End: tabs.length - 1}[e.key];
      if (next === undefined) return;
      e.preventDefault(); select(next, true);
    });
  });
  const syncHash = () => {
    const index = panels.findIndex(panel => '#' + panel.id === location.hash);
    if (index >= 0) select(index);
  };
  controls.hidden = false;
  select(0); syncHash();
  addEventListener('hashchange', syncHash);
  if (!window.gsap || !window.ScrollTrigger) return;
  const mm = gsap.matchMedia();
  mm.add('(min-width: 761px) and (prefers-reduced-motion: no-preference)', () => {
    animateFrame = true;
    root.classList.add('is-frame-animated');
    gsap.set(frame, {width: root.dataset.gasStep === '0' ? '46%' : '100%'});
    return () => {
      animateFrame = false;
      root.classList.remove('is-frame-animated');
      gsap.set([frame, root.querySelector('.gas-frame-visual img')], {clearProps: 'width,transform'});
    };
  });
  mm.add('(prefers-reduced-motion: no-preference)', () => {
    gsap.from('.gas-title-group > *, .gas-hero-copy > .editorial-actions', {y: 22, opacity: 0, duration: .8, stagger: .08, ease: 'power3.out', clearProps: 'all'});
    gsap.from('.gas-product-media figure', {y: 36, opacity: 0, duration: 1.1, ease: 'power3.out', clearProps: 'all'});
    gsap.from('.gas-elements li', {y: 15, opacity: 0, duration: .7, stagger: .1, ease: 'power3.out', clearProps: 'all', scrollTrigger: {trigger: '.gas-elements', start: 'top 95%', once: true}});
  });
})();
