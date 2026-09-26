/* SUNPLEX v3 shared kit: header/mega menu, reveal, parallax, expand, count-up, ticks */
(() => {
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const cl = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const ease = t => 1 - Math.pow(1 - t, 3);

  // header + mega menu
  const gh = $('.gh');
  if (gh) {
    const btn = $('[data-mega]', gh), burger = $('.burger', gh);
    let t;
    const open = v => { gh.classList.toggle('open', v); btn && btn.setAttribute('aria-expanded', v); };
    if (btn) {
      const zone = [btn, $('.mega', gh)];
      zone.forEach(z => z && z.addEventListener('mouseenter', () => { clearTimeout(t); open(true); }));
      zone.forEach(z => z && z.addEventListener('mouseleave', () => { t = setTimeout(() => open(false), 160); }));
      btn.addEventListener('click', () => open(!gh.classList.contains('open')));
    }
    burger && burger.addEventListener('click', () => open(!gh.classList.contains('open')));
    addEventListener('keydown', e => { if (e.key === 'Escape') open(false); });
    // preview image follows hovered column
    const pv = $$('.mega .pv img', gh), pvText = $('.mega .pv p', gh);
    $$('.mega .col', gh).forEach((c, i) => c.addEventListener('mouseenter', () => {
      pv.forEach((im, k) => im.classList.toggle('on', k === i));
      if (pvText) pvText.textContent = c.dataset.tag || '';
    }));
  }

  // reveal (stagger siblings)
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('in'); io.unobserve(e.target);
  }), { threshold: .12, rootMargin: '0px 0px -6% 0px' });
  $$('[data-reveal]').forEach(el => {
    const sib = [...el.parentElement.children].filter(n => n.hasAttribute('data-reveal'));
    el.style.transitionDelay = (Math.min(sib.indexOf(el), 6) * 0.07) + 's';
    RM ? el.classList.add('in') : io.observe(el);
  });

  // count-up
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return; cio.unobserve(e.target);
    const el = e.target, to = +el.dataset.count, t0 = performance.now(), d = 1100;
    if (RM) { el.textContent = to; return; }
    const step = n => { const p = cl((n - t0) / d); el.textContent = Math.round(to * ease(p)); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }), { threshold: .6 });
  $$('[data-count]').forEach(el => cio.observe(el));

  // scroll-linked: parallax images + expanding cards + header + ticks
  const par = $$('[data-par]'), exp = $$('[data-expand]'), secs = $$('[data-sec]');
  let ticks;
  if (secs.length > 2 && !document.getElementById('ticks')) {
    ticks = document.createElement('div'); ticks.className = 'ticks'; ticks.setAttribute('aria-hidden', 'true');
    secs.forEach(() => ticks.appendChild(document.createElement('i'))); document.body.appendChild(ticks);
  }
  function frame() {
    const H = innerHeight, W = innerWidth;
    gh && gh.classList.toggle('scrolled', scrollY > 30);
    if (!RM) {
      par.forEach(el => {
        const r = el.parentElement.getBoundingClientRect(), p = cl((H - r.top) / (H + r.height));
        el.style.transform = `translateY(${(p - .5) * -8}%) scale(1.12)`;
      });
      exp.forEach(el => {
        // card at content width grows to full-bleed as it reaches the viewport center
        const r = el.getBoundingClientRect(), p = ease(cl((H - r.top) / (H * .75)));
        const side = Math.max(0, (W - Math.min(W - 48, 1224)) / 2) * (1 - p) + (W < 900 ? 16 : 0) * (1 - p);
        el.style.clipPath = `inset(0 ${side}px round ${52 * (1 - p) + 0}px)`;
      });
    }
    if (ticks) {
      let cur = 0; secs.forEach((s, i) => { if (s.getBoundingClientRect().top < H * .5) cur = i; });
      [...ticks.children].forEach((d, i) => d.classList.toggle('on', i === cur));
    }
  }
  let q = false;
  const req = () => { if (!q) { q = true; requestAnimationFrame(() => { q = false; frame(); }); } };
  addEventListener('scroll', req, { passive: true }); addEventListener('resize', req); frame();
})();
/* toss place floating consult bar: appears after the hero, hides over the footer */
(() => {
  const bar = document.querySelector('[data-fbar]'); if (!bar) return;
  const foot = document.querySelector('.gf');
  const f = () => {
    const past = scrollY > innerHeight * .6;
    const nearFoot = foot && foot.getBoundingClientRect().top < innerHeight - 40;
    bar.classList.toggle('on', past && !nearFoot);
  };
  addEventListener('scroll', () => requestAnimationFrame(f), { passive: true }); f();
})();
