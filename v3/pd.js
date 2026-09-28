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
      st.querySelectorAll('.pd-st-vis > .pd-st-fig, .pd-st-vis > .pd-fig').forEach((fg, i) => fg.classList.toggle('on', i === idx));
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

/* 교신 경로: mode tabs + auto-advance until the visitor picks one */
document.querySelectorAll("[data-radio]").forEach(function (rp) {
  var btns = rp.querySelectorAll(".rp-tabs button"), cur = 0, timer = null;
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function set(m) {
    cur = m; rp.setAttribute("data-mode", m);
    btns.forEach(function (b, i) { b.setAttribute("aria-selected", i === m ? "true" : "false"); });
    if (rp.classList.contains("is-auto")) { btns[m].querySelector(".rp-bar").style.animation = "none"; void btns[m].offsetWidth; btns[m].querySelector(".rp-bar").style.animation = ""; }
  }
  function stop() { clearInterval(timer); timer = null; rp.classList.remove("is-auto"); }
  btns.forEach(function (b, i) { b.addEventListener("click", function () { stop(); set(i); }); });
  if (still || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting && !timer && rp.dataset.picked !== "1") { rp.classList.add("is-auto"); set(cur); timer = setInterval(function () { set((cur + 1) % 3); }, 4200); }
      else if (!e.isIntersecting && timer) { clearInterval(timer); timer = null; }
    });
  }, { threshold: 0.4 }).observe(rp);
  btns.forEach(function (b) { b.addEventListener("click", function () { rp.dataset.picked = "1"; }); });
});

/* 관제 순서 tour: steps <-> hotspots, auto-advance until the visitor picks one */
document.querySelectorAll("[data-tour]").forEach(function (tr) {
  var lis = tr.querySelectorAll(".tour-steps li"), pins = tr.querySelectorAll(".tour-pin"), n = lis.length, cur = 0, timer = null;
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function set(k) {
    cur = k;
    lis.forEach(function (li, i) { li.classList.toggle("on", i === k); li.querySelector("button").setAttribute("aria-expanded", i === k ? "true" : "false"); });
    pins.forEach(function (p, i) { p.classList.toggle("on", i === k); });
    var bar = lis[k].querySelector(".tour-bar"); if (bar) { bar.style.animation = "none"; void bar.offsetWidth; bar.style.animation = ""; }
  }
  function pick(k) { clearInterval(timer); timer = null; tr.classList.remove("is-auto"); tr.dataset.picked = "1"; set(k); }
  lis.forEach(function (li, i) { li.querySelector("button").addEventListener("click", function () { pick(i); }); });
  pins.forEach(function (p, i) { p.addEventListener("click", function () { pick(i); }); });
  set(0);
  if (still || !("IntersectionObserver" in window)) return;
  new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting && !timer && tr.dataset.picked !== "1") { tr.classList.add("is-auto"); set(cur); timer = setInterval(function () { set((cur + 1) % n); }, 4200); }
      else if (!e.isIntersecting && timer) { clearInterval(timer); timer = null; tr.classList.remove("is-auto"); }
    });
  }, { threshold: 0.4 }).observe(tr);
});

/* explainer scenes: the scene pins (sticky) while scrolling walks it through 01 -> 02 -> 03,
   a pulse travels each newly lit link; tabs jump the scroll to their step */
(function () {
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var NS = "http://www.w3.org/2000/svg", all = [], HEAD = 121, STEP = 0.55;
  function headH() {
    var b = 0;
    document.querySelectorAll("header.gh, .pd-local").forEach(function (e) { var r = e.getBoundingClientRect(); if (getComputedStyle(e).position !== "static") b = Math.max(b, r.bottom); });
    return Math.max(64, Math.min(160, b || HEAD));
  }
  document.querySelectorAll("[data-scene]").forEach(function (sc) {
    var states = sc.getAttribute("data-states").split("|").map(function (s) { return s.split(","); });
    var btns = sc.querySelectorAll(".sc-tabs button"), pans = sc.querySelectorAll(".sc-pan"), svg = sc.querySelector(".sc-svg");
    // pin > hold > [section heading..., scene]; the whole hold sticks when it fits, else only the scene
    var pin = document.createElement("div"), hold = document.createElement("div");
    pin.className = "sc-pin"; hold.className = "sc-hold";
    var lead = [], prev = sc.previousElementSibling;
    while (prev) { lead.unshift(prev); prev = prev.previousElementSibling; }
    sc.parentNode.insertBefore(pin, sc); pin.appendChild(hold);
    lead.forEach(function (e) { hold.appendChild(e); }); hold.appendChild(sc);
    var room = document.createElement("div"); room.className = "sc-room"; room.setAttribute("aria-hidden", "true"); hold.appendChild(room);
    var st = { sc: sc, pin: pin, hold: hold, room: room, el: null, n: states.length, cur: -1, on: false };
    function travel(path) {
      if (still || !path.getTotalLength) return;
      var L = path.getTotalLength(), dot = document.createElementNS(NS, "circle"), t0 = null;
      dot.setAttribute("r", "7"); dot.setAttribute("class", "sc-dot"); svg.appendChild(dot);
      function step(ts) {
        if (!t0) t0 = ts; var q = Math.min(1, (ts - t0) / 650), e = 1 - Math.pow(1 - q, 3), pt = path.getPointAtLength(L * e);
        dot.setAttribute("cx", pt.x); dot.setAttribute("cy", pt.y); dot.style.opacity = q < .85 ? 1 : (1 - q) / .15;
        if (q < 1) requestAnimationFrame(step); else dot.remove();
      }
      requestAnimationFrame(step);
    }
    st.set = function (k) {
      if (k === st.cur) return;
      var on = states[k], was = st.cur >= 0 ? states[st.cur] : [];
      sc.querySelectorAll("[data-n],[data-l]").forEach(function (el) {
        var id = el.getAttribute("data-n") || el.getAttribute("data-l"), lit = on.indexOf(id) >= 0;
        el.classList.toggle("on", lit);
        el.classList.toggle("cur", lit && was.indexOf(id) < 0);
        if (lit && was.indexOf(id) < 0 && el.classList.contains("sc-l")) travel(el);
      });
      btns.forEach(function (b, i) { b.setAttribute("aria-selected", i === k ? "true" : "false"); b.classList.toggle("done", i < k); });
      pans.forEach(function (p, i) { p.classList.toggle("on", i === k); });
      st.cur = k;
    };
    // tab click: scroll to that step inside the pinned range (or just show it when not pinned)
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () {
        if (st.on) {
          var y0 = pin.getBoundingClientRect().top + window.scrollY + st.off - st.top;
          window.scrollTo({ top: y0 + st.range * (i + .5) / st.n, behavior: still ? "auto" : "smooth" });
        }
        st.set(i);
      });
    });
    st.set(0);
    all.push(st);
  });
  if (!all.length) return;
  function layout() {
    var vh = window.innerHeight, hh = headH(), wide = window.innerWidth > 900, room = vh - hh;
    all.forEach(function (st) {
      [st.hold, st.sc].forEach(function (e) { e.style.top = ""; e.classList.remove("is-sticky"); });
      st.pin.style.height = ""; st.room.style.height = "0px";
      st.on = false; st.el = null;
      if (st.n < 2) return;
      if (wide && st.hold.offsetHeight + 32 < room) st.el = st.hold;
      else if (st.sc.offsetHeight + 24 < room) st.el = st.sc;
      if (!st.el) return;
      var h = st.el.offsetHeight;
      st.off = st.el.getBoundingClientRect().top - st.pin.getBoundingClientRect().top;
      st.top = Math.round(hh + Math.max(16, (room - h) / 2));
      st.range = st.n * vh * STEP;
      // the scroll room must live in the sticky element's own parent: pin for the hold, hold for the scene
      if (st.el === st.hold) st.pin.style.height = (st.hold.offsetHeight + st.range) + "px";
      else st.room.style.height = st.range + "px";
      st.el.classList.add("is-sticky"); st.el.style.top = st.top + "px";
      st.on = true;
    });
  }
  var ticking = false;
  function update() {
    ticking = false;
    var vh = window.innerHeight;
    all.forEach(function (st) {
      var r = st.pin.getBoundingClientRect(), p;
      if (r.bottom < -50 || r.top > vh + 50) return;
      if (st.on) p = (st.top - (r.top + st.off)) / st.range;   // 0 when it pins, 1 when it releases
      else return;   // not pinned (does not fit the screen): steps change only by tapping the tabs
      var f = Math.max(0, Math.min(.999, p)) * st.n, k = Math.floor(f);
      st.set(k);
      st.sc.querySelectorAll(".sc-tabs .rp-bar").forEach(function (b, i) { b.style.width = (i < k ? 100 : i === k ? (f - k) * 100 : 0) + "%"; });
      st.sc.classList.toggle("is-stuck", st.on && p > 0 && p < 1);
    });
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); setTimeout(function () { if (ticking) update(); }, 120); } }, { passive: true });
  window.addEventListener("resize", function () { layout(); update(); });
  var lastY = -1;
  setInterval(function () { if (window.scrollY !== lastY) { lastY = window.scrollY; update(); } }, 200);
  layout(); update();
  window.addEventListener("load", function () { layout(); update(); });
  // late (lazy) images or font swaps change the heights: re-measure whenever pinned content resizes
  var relayoutT = null;
  function relayout() { clearTimeout(relayoutT); relayoutT = setTimeout(function () { layout(); update(); }, 60); }
  if ("ResizeObserver" in window) {
    var ro = new ResizeObserver(relayout);
    // watch only what sits above the scene (late images, headings); the scene itself changes height per step
    all.forEach(function (st) { [].forEach.call(st.hold.children, function (c) { if (c !== st.room && c !== st.sc) ro.observe(c); }); });
  }
  all.forEach(function (st) { st.hold.querySelectorAll("img").forEach(function (im) { if (!im.complete) im.addEventListener("load", relayout); }); });
})();
