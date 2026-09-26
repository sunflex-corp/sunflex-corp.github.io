/* v3 layer for product detail pages: toss-style reveals + hero parallax on top of existing product scripts */
(() => {
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const sel = [
    '.benefit-heading', '.editorial-section-inner > header', '.editorial-section-inner > p', '.editorial-section-inner > h2',
    '.revision-criteria > li', '.content-tile', '.editorial-step-grid > *', '.content-grid > figure',
    '#related .lead', '.solar-card', '.final-cta'
  ].join(',');
  const els = [...document.querySelectorAll(sel)].filter(el => !el.closest('.product-flow-track, .studio-panels, .mega, .gf'));
  if (RM) return;
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('v3-in'); io.unobserve(e.target); }
  }), { threshold: .1, rootMargin: '0px 0px -5% 0px' });
  els.forEach(el => {
    const sib = [...el.parentElement.children].filter(n => els.includes(n));
    el.classList.add('v3-rv');
    el.style.transitionDelay = Math.min(sib.indexOf(el), 5) * 0.07 + 's';
    io.observe(el);
  });
  // gentle parallax on the hero media
  const hm = document.querySelector('.studio-hero-media img, .gas-hero img');
  if (hm) {
    const f = () => { const r = hm.getBoundingClientRect(), p = Math.min(1, Math.max(0, (innerHeight - r.top) / (innerHeight + r.height)));
      hm.style.transform = `translateY(${(p - .5) * -6}%) scale(1.1)`; };
    addEventListener('scroll', () => requestAnimationFrame(f), { passive: true }); f();
  }
})();
/* white-background product shots in the hero: detect by sampling corner pixels, then stage them whole */
(() => {
  const img = document.querySelector('.studio-hero-media img');
  if (!img) return;
  const fig = img.closest('figure');
  const test = () => {
    try {
      const c = document.createElement('canvas'), w = c.width = 40, h = c.height = 40, x = c.getContext('2d');
      x.drawImage(img, 0, 0, w, h);
      const px = [[1,1],[w-2,1],[1,h-2],[w-2,h-2]].map(([a,b]) => x.getImageData(a,b,1,1).data);
      const light = px.filter(d => d[0] > 225 && d[1] > 225 && d[2] > 225).length;
      if (light >= 3) fig && fig.classList.add('v3-stage');
    } catch (e) {
      if (/white|reference|device|restored|studio|approved|stage\d/.test(img.currentSrc || img.src)) fig && fig.classList.add('v3-stage');
    }
  };
  img.complete && img.naturalWidth ? test() : img.addEventListener('load', test, { once: true });
})();
