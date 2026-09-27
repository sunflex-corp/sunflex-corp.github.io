/* bespoke product pages: reveal + pinned step list driven by scroll */
(() => {
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .1, rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('.pd [data-rv]').forEach((el, i, all) => {
    const sib = [...el.parentElement.children].filter(n => n.hasAttribute('data-rv'));
    el.style.transitionDelay = Math.min(sib.indexOf(el), 4) * .06 + 's';
    RM ? el.classList.add('in') : io.observe(el);
  });
  const steps = [...document.querySelectorAll('[data-steps]')];
  const f = () => {
    if (innerWidth < 900) return;
    steps.forEach(st => {
      const r = st.getBoundingClientRect(), n = +getComputedStyle(st).getPropertyValue('--n') || 1;
      const p = Math.min(.999, Math.max(0, (140 - r.top) / (r.height - innerHeight * .6)));
      const idx = Math.floor(p * n);
      st.querySelectorAll('.pd-st').forEach((li, i) => li.classList.toggle('on', i === idx));
      st.querySelectorAll('.pd-st-vis .pd-fig').forEach((fg, i) => fg.classList.toggle('on', i === idx));
    });
  };
  addEventListener('scroll', () => requestAnimationFrame(f), { passive: true }); addEventListener('resize', f); f();
  steps.forEach(st => st.querySelectorAll('.pd-st').forEach((li, i) => li.addEventListener('click', () => {
    const r = st.getBoundingClientRect(), n = +getComputedStyle(st).getPropertyValue('--n') || 1;
    scrollTo({ top: scrollY + r.top - 140 + (r.height - innerHeight * .6) * ((i + .5) / n), behavior: RM ? 'auto' : 'smooth' });
  })));
  // statement: split into words, light them up with scroll progress
  document.querySelectorAll('.pd-stmt .pd-head .pd-p').forEach(p => {
    const walk = n => [...n.childNodes].forEach(c => {
      if (c.nodeType === 3) { const f = document.createDocumentFragment(); c.textContent.split(/(\s+)/).forEach(w => { if (!w) return; if (/^\s+$/.test(w)) f.append(w); else { const s = document.createElement('span'); s.className = 'wd'; s.textContent = w; f.append(s); } }); c.replaceWith(f); }
      else if (c.nodeType === 1 && c.tagName !== 'BR') walk(c);
    });
    walk(p);
  });
  const wds = [...document.querySelectorAll('.pd-stmt')].map(s => [s, [...s.querySelectorAll('.wd')]]);
  const hero = document.querySelector('.pd-hero.is-photo .pd-hero-fig');
  const g = () => {
    wds.forEach(([s, ws]) => {
      if (RM) { ws.forEach(w => w.classList.add('on')); return; }
      const r = s.getBoundingClientRect(), p = Math.min(1, Math.max(0, (innerHeight * .85 - r.top) / (innerHeight * .6)));
      const k = Math.round(p * ws.length); ws.forEach((w, i) => w.classList.toggle('on', i < k));
    });
    if (hero && innerWidth >= 900 && !RM) {
      const r = hero.getBoundingClientRect(), w = hero.offsetWidth;
      const p = Math.min(1, Math.max(0, (innerHeight * .75 - r.top) / (innerHeight * .55)));
      hero.style.setProperty('--hp', p.toFixed(3));
    }
  };
  addEventListener('scroll', () => requestAnimationFrame(g), { passive: true }); addEventListener('resize', g); g();
})();

// benefits tabs (roving tabindex, arrow keys)
document.querySelectorAll('[data-tabs]').forEach(w => {
  const bs = [...w.querySelectorAll('[role=tab]')], ps = [...w.querySelectorAll('.pd-tab-p')];
  const go = (i, f) => { bs.forEach((b, j) => { b.setAttribute('aria-selected', j === i); b.tabIndex = j === i ? 0 : -1; }); ps.forEach((p, j) => p.classList.toggle('on', j === i)); if (f) bs[i].focus(); };
  bs.forEach((b, i) => { b.addEventListener('click', () => go(i)); b.addEventListener('keydown', e => { if (e.key === 'ArrowRight') go((i + 1) % bs.length, 1); if (e.key === 'ArrowLeft') go((i - 1 + bs.length) % bs.length, 1); }); });
});
