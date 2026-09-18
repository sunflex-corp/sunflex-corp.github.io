/* Phase 2 Figma design system: header slides up on scroll-down (past 80px), reappears on
   scroll-up. position:sticky stays put on the header itself -- this only toggles a
   translateY transform on top of it. Respects prefers-reduced-motion like the rest of the
   site's motion code (brand/consultation-light.js, site-image-motion.js): reduced motion
   means the header simply never hides. */
(() => {
  'use strict';
  const header = document.querySelector('.site-header[data-astro-cid-6stfpryv]');
  if (!header) return;

  const THRESHOLD = 80;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let lastY = window.scrollY || window.pageYOffset || 0;
  let ticking = false;

  const show = () => header.removeAttribute('data-header-hidden');

  function update() {
    ticking = false;
    if (reduce.matches) { show(); return; }
    const y = window.scrollY || window.pageYOffset || 0;
    if (y > lastY && y > THRESHOLD) {
      header.setAttribute('data-header-hidden', '');
    } else {
      show();
    }
    lastY = y;
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  reduce.addEventListener('change', () => { if (reduce.matches) show(); });
  document.addEventListener('astro:before-swap', show);
})();
