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
      const vis = st.querySelector('.pd-st-vis'); if (vis) { vis.setAttribute('data-n', String(idx + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0')); vis.style.setProperty('--sp', ((p * n) % 1).toFixed(3)); }
      st.querySelectorAll('.pd-st').forEach((li, i) => li.style.setProperty('--sp', i < idx ? 1 : i === idx ? ((p * n) % 1).toFixed(3) : 0));
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
    var ap = pins[k]; if (ap) { tr.style.setProperty("--px", ap.style.left); tr.style.setProperty("--py", ap.style.top); }
    tr.setAttribute("data-k", k); var ti = tr.querySelector(".tour-img"); if (ti) { ti.setAttribute("data-step", "0" + (k + 1)); ti.style.setProperty("--px", ap ? ap.style.left : "50%"); ti.style.setProperty("--py", ap ? ap.style.top : "50%"); }
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
  var NS = "http://www.w3.org/2000/svg", all = [], HEAD = 121, STEP = 0.55, STEP_NARROW = 0.4;
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
      sc.setAttribute("data-step", k);
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
      // phones/tablets too: pinning the heading with the scene keeps its title on screen instead of a blank band above it
      if (st.hold.offsetHeight + 32 < room) st.el = st.hold;
      else if (st.sc.offsetHeight + 24 < room) st.el = st.sc;
      if (!st.el) return;
      var h = st.el.offsetHeight;
      st.off = st.el.getBoundingClientRect().top - st.pin.getBoundingClientRect().top;
      st.top = Math.round(hh + Math.max(16, (room - h) / 2));
      st.range = st.n * vh * (wide ? STEP : STEP_NARROW);
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

/* generic scroll-pin: benefit tabs, 관제 순서 tour, 강점 rail hold still while scrolling steps / slides them */
(function () {
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches, items = [];
  function headH() { var l = document.querySelector(".pd-local"); var b = l ? l.getBoundingClientRect().bottom : 64; return Math.max(56, Math.min(160, b)); }
  function make(sec, target, n, onP, stepK) {
    var w = sec.querySelector(":scope > .pd-w") || target.parentNode;
    var pin = document.createElement("div"); pin.className = "gp-pin";
    var hold = document.createElement("div"); hold.className = "gp-hold";
    var room = document.createElement("div"); room.className = "gp-room"; room.setAttribute("aria-hidden", "true");
    // hold = everything in the section's inner wrapper (heading + target), so the title stays with it
    var host = w.contains(target) ? w : target.parentNode;
    while (host.firstChild) hold.appendChild(host.firstChild);
    // rail lives outside .pd-w: pull it in too
    if (!hold.contains(target)) hold.appendChild(target);
    pin.appendChild(hold); pin.appendChild(room); host.appendChild(pin);
    var roomIn = document.createElement("div"); roomIn.className = "gp-room"; roomIn.setAttribute("aria-hidden", "true");
    target.parentNode.insertBefore(roomIn, target.nextSibling);
    var it = { pin: pin, hold: hold, room: room, roomIn: roomIn, target: target, n: n, onP: onP, stepK: stepK, on: false, k: -1 };
    items.push(it);
    return it;
  }
  function layout() {
    var vh = innerHeight, hh = headH(), wide = innerWidth > 900;
    items.forEach(function (it) {
      [it.hold, it.target].forEach(function (e) { e.classList.remove("is-sticky"); e.style.top = ""; });
      it.room.style.height = it.roomIn.style.height = "0px"; it.on = false; it.el = null;
      if (!wide || still) return;
      if (it.hold.offsetHeight + 24 < vh - hh) { it.el = it.hold; it.r = it.room; }
      else if (it.target.offsetHeight + 24 < vh - hh) { it.el = it.target; it.r = it.roomIn; }
      else return;
      var h = it.el.offsetHeight;
      it.off = it.el.getBoundingClientRect().top - it.pin.getBoundingClientRect().top;
      it.top = Math.round(hh + Math.max(12, (vh - hh - h) / 2));
      it.range = it.n * vh * 0.5;
      it.r.style.height = it.range + "px";
      it.el.classList.add("is-sticky"); it.el.style.top = it.top + "px";
      it.on = true;
    });
  }
  function update() {
    items.forEach(function (it) {
      if (!it.on) return;
      var r = it.pin.getBoundingClientRect();
      if (r.bottom < -50 || r.top > innerHeight + 50) return;
      var p = Math.max(0, Math.min(.999, (it.top - (r.top + it.off)) / it.range));
      it.onP(p);
    });
  }
  function jump(it, i) {
    if (!it.on) return false;
    scrollTo({ top: it.pin.getBoundingClientRect().top + scrollY + it.off - it.top + it.range * (i + .5) / it.n, behavior: "smooth" });
    return true;
  }
  // 1) benefit tabs
  document.querySelectorAll(".pd-benefits.is-tabs").forEach(function (sec) {
    var tabs = sec.querySelector("[data-tabs]"); if (!tabs) return;
    var bs = [].slice.call(tabs.querySelectorAll("[role=tab]"));
    var it = make(sec, tabs, bs.length, function (p) {
      var k = Math.floor(p * bs.length);
      if (k !== it.k) { it.k = k; bs[k].click(); }
      tabs.style.setProperty("--tp", ((p * bs.length) % 1).toFixed(3));
    });
    bs.forEach(function (b, i) { b.addEventListener("click", function (e) { if (e.isTrusted) { it.k = i; jump(it, i); } }); });
  });
  // 2) 관제 순서 tour
  document.querySelectorAll("[data-tour]").forEach(function (tr) {
    var sec = tr.closest("section"), btns = [].slice.call(tr.querySelectorAll(".tour-steps li > button"));
    tr.dataset.picked = "1";   // scroll drives it; no auto-advance
    var it = make(sec, tr, btns.length, function (p) {
      var f = p * btns.length, k = Math.floor(f);
      if (k !== it.k) { it.k = k; btns[k].click(); }
      tr.style.setProperty("--tp", (f - k).toFixed(3));
    });
    btns.forEach(function (b, i) { b.addEventListener("click", function (e) { if (e.isTrusted) { it.k = i; jump(it, i); } }); });
  });
  // 3) 한눈에 보는 강점 rail: vertical scroll slides the cards sideways
  document.querySelectorAll(".pd-hl.is-rail").forEach(function (sec) {
    var rail = sec.querySelector(".pd-rail"); if (!rail) return;
    var cards = rail.querySelectorAll(".pd-card").length;
    var it = make(sec, rail, Math.max(2, cards - 1), function (p) {
      var max = rail.scrollWidth - rail.clientWidth;
      rail.style.scrollSnapType = "none"; rail.scrollLeft = max * Math.min(1, p / .96);
    });
  });
  // 5) 후크 하방 카메라 두 시선: blocked view fades as the hook-camera view comes up
  document.querySelectorAll("[data-pd=hook-bottom-camera] #hook-two-views").forEach(function (sec) {
    var cards = sec.querySelector(".pd-cards"); if (!cards) return;
    cards.classList.add("is-scrub");
    make(sec, cards, 2, function (p) { cards.style.setProperty("--tv", Math.max(0, Math.min(1, (p - .15) / .6)).toFixed(3)); });
  });
  // 6) 이동식 바디캠: viewfinder story (REC timecode runs with scroll, shots cut per step)
  document.querySelectorAll("[data-bc]").forEach(function (bc) {
    var sec = bc.closest("section"), fs = bc.querySelectorAll(".bc-f"), ps = bc.querySelectorAll(".bc-pan"), ls = bc.querySelectorAll(".bc-nav li");
    var tc = bc.querySelector(".bc-tc"), nn = bc.querySelector(".bc-n"), k0 = -1;
    function set(k) {
      if (k === k0) return; k0 = k; bc.setAttribute("data-step", k);
      [fs, ps, ls].forEach(function (g) { g.forEach(function (e, i) { e.classList.toggle("on", i === k); e.classList.toggle("done", i < k); }); });
      nn.textContent = "0" + (k + 1) + " / 03";
      bc.classList.remove("cut"); void bc.offsetWidth; bc.classList.add("cut");
    }
    ls.forEach(function (li, i) { li.addEventListener("click", function () { set(i); }); });
    // phones/tablets (no pin): the three notes are stacked, the viewfinder follows whichever note crosses mid-screen
    if (innerWidth <= 900 && "IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) set([].indexOf.call(ps, e.target)); }); }, { rootMargin: "-50% 0px -40% 0px" });
      ps.forEach(function (e) { io.observe(e); });
    }
    make(sec, bc, 3, function (p) {
      var f = p * 3, k = Math.floor(f);
      set(k);
      bc.style.setProperty("--bp", (f - k).toFixed(3));
      var s = 14 * 60 + 32 + Math.round(p * 420), hh = "00", mm = ("0" + Math.floor(s / 60)).slice(-2), ss = ("0" + (s % 60)).slice(-2);
      tc.textContent = hh + ":" + mm + ":" + ss;
    });
  });
  // 7) 후크 하방 카메라 도입 전 확인: rows step through, the 3D scene points at each part
  document.querySelectorAll("[data-hf]").forEach(function (g) {
    var sec = g.closest("section"), li = g.querySelectorAll(".hf-steps li"), sp = g.querySelectorAll(".hf-spot"), k0 = -1;
    function set(k) {
      if (k === k0) return; k0 = k; g.setAttribute("data-k", k);
      var n = g.querySelector(".hf-num"); if (n) n.textContent = "0" + (k + 1);
      [li, sp].forEach(function (a) { a.forEach(function (e, i) { e.classList.toggle("on", i === k); e.classList.toggle("done", i < k); }); });
    }
    li.forEach(function (e, i) { e.addEventListener("click", function () { set(i); }); });
    set(0);
    make(sec, g.querySelector(".hf-v"), 3, function (p) { var f = p * 3, k = Math.floor(f); set(k); g.style.setProperty("--hp", (f - k).toFixed(3)); });
  });
  // 8) 후크 하방 카메라 인양 전 체크포인트: hook-cam screen locks on to each checkpoint
  document.querySelectorAll("[data-cp]").forEach(function (g) {
    var sec = g.closest("section"), li = g.querySelectorAll(".cp-list li"), k0 = -1;
    function set(k) {
      if (k === k0) return; k0 = k; g.setAttribute("data-k", k);
      li.forEach(function (e, i) { e.classList.toggle("on", i === k); e.classList.toggle("done", i < k); });
    }
    li.forEach(function (e, i) { e.addEventListener("click", function () { set(i); }); });
    set(0);
    var n = li.length;
    // phones/tablets (no pin): the row crossing mid-screen drives the hook-cam view
    if (innerWidth <= 900 && "IntersectionObserver" in window) {
      var cio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) set([].indexOf.call(li, e.target)); }); }, { rootMargin: "-45% 0px -45% 0px" });
      li.forEach(function (e) { cio.observe(e); });
    }
    make(sec, g.querySelector(".cp-v"), n + 1, function (p) {
      var f = p * (n + 1), k = Math.min(n - 1, Math.floor(f));
      set(k); g.classList.toggle("all", f >= n);
      g.style.setProperty("--cp", Math.min(1, f - Math.floor(f)).toFixed(3));
    });
  });
  // 9) 바디캠 도입 전 확인: cards open one at a time with scroll
  document.querySelectorAll("[data-bf]").forEach(function (ol) {
    var sec = ol.closest("section"), li = ol.querySelectorAll("li"), k0 = -1;
    function set(k) { if (k === k0) return; k0 = k; li.forEach(function (e, i) { e.classList.toggle("on", i === k); e.classList.toggle("done", i < k); }); }
    li.forEach(function (e, i) { e.addEventListener("mouseenter", function () { if (innerWidth > 900 && !ol.closest(".is-sticky")) set(i); }); e.addEventListener("click", function () { set(i); }); });
    make(sec, ol, li.length, function (p) { var f = p * li.length; set(Math.floor(f)); ol.style.setProperty("--bfp", (f - Math.floor(f)).toFixed(3)); });
  });
  // 10) numbered rows -> pinned showcase
  document.querySelectorAll("[data-rs]").forEach(function (rs) {
    var sec = rs.closest("section"), nav = rs.querySelectorAll(".rs-i"), fs = rs.querySelectorAll(".rs-f"), ps = rs.querySelectorAll(".rs-pan"), big = rs.querySelector(".rs-big"), k0 = -1;
    function set(k) {
      if (k === k0) return; k0 = k; rs.setAttribute("data-k", k); big.textContent = (k < 9 ? "0" : "") + (k + 1);
      [nav, fs, ps].forEach(function (g) { g.forEach(function (e, i) { e.classList.toggle("on", i === k); e.classList.toggle("done", i < k); }); });
    }
    var it = make(sec, rs, nav.length, function (p) { var f = p * nav.length; set(Math.floor(f)); rs.style.setProperty("--rp", (f - Math.floor(f)).toFixed(3)); });
    nav.forEach(function (e, i) { e.querySelector("button").addEventListener("click", function (ev) { set(i); if (ev.isTrusted) jump(it, i); }); });
  });
  // 4) 안전종합상황판 확인 질문: scattered sources gather into the board as you scroll (and scatter back going up)
  document.querySelectorAll(".ss-story").forEach(function (sec) {
    var m = sec.querySelector(".ss-merge"); if (!m) return;
    m.classList.add("is-scrub");
    make(sec, m, 3, function (p) { m.style.setProperty("--mp", Math.min(1, p / .85).toFixed(3)); });
  });
  // shared for session-2 scripts (v3/pd-s2.js): pin a section target, step it with scroll
  window.pdPin = { make: function (sec, target, n, onP) { var it = make(sec, target, n, onP); layout(); update(); return it; }, jump: jump, relayout: function () { layout(); update(); } };
  addEventListener("scroll", function () { requestAnimationFrame(update); }, { passive: true });
  addEventListener("resize", function () { layout(); update(); });
  addEventListener("load", function () { layout(); update(); });
  var lastY = -1; setInterval(function () { if (scrollY !== lastY) { lastY = scrollY; update(); } }, 200);
  items.forEach(function (it) { it.hold.querySelectorAll("img").forEach(function (im) { if (!im.complete) im.addEventListener("load", function () { layout(); update(); }); }); });
  layout(); update();
})();

/* feature tiles: image rises with scroll, tilt/glare follows the pointer */
(function () {
  var tiles = [].slice.call(document.querySelectorAll(".pd-tile")); if (!tiles.length) return;
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  tiles.forEach(function (t, i) {
    var n = t.querySelector(".pd-num"); t.setAttribute("data-n", n ? n.textContent.trim() : ("0" + (i + 1)));
    if (still) return;
    t.addEventListener("pointermove", function (e) {
      var r = t.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      t.style.setProperty("--ry", ((x - .5) * 6).toFixed(2) + "deg"); t.style.setProperty("--rx", ((.5 - y) * 6).toFixed(2) + "deg");
      t.style.setProperty("--gx", (x * 100).toFixed(1) + "%"); t.style.setProperty("--gy", (y * 100).toFixed(1) + "%");
    });
    t.addEventListener("pointerleave", function () { t.style.setProperty("--rx", "0deg"); t.style.setProperty("--ry", "0deg"); });
  });
  if (still) return;
  function upd() {
    var vh = innerHeight;
    tiles.forEach(function (t) {
      var r = t.getBoundingClientRect(), p = Math.max(0, Math.min(1, (vh - r.top) / (vh * .55)));
      t.style.setProperty("--tp2", p.toFixed(3));
    });
  }
  addEventListener("scroll", function () { requestAnimationFrame(upd); }, { passive: true }); addEventListener("resize", upd); upd();
})();

/* S1 pages (이동식 CCTV ~ TBM): big photos open up as they scroll in (inset card -> full, slow zoom-out) */
(function () {
  var main = document.querySelector("main[data-pd]"); if (!main) return;
  var S1 = ["mobile-bodycam","hook-bottom-camera","chatgpt-cctv","safety-box","site-cms","led-logo-light","vehicle-entry-alert","co2-temp-humidity","iot-mist","lte-anemometer","smart-environment-board","compact-gas-detector","gas-alarm","tilt-acceleration-sensor","fire-detection","ir3-flame-detector","ai-broadcast","wireless-emergency-broadcast","digital-radio","tbm-solution"];
  if (S1.indexOf(main.getAttribute("data-pd")) < 0) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var figs = [].slice.call(document.querySelectorAll(".pd-full-fig, .pd-scene .pd-split-fig, .pd-media .pd-fig:not(.is-stage)"));
  figs.forEach(function (f) { f.classList.add("px-rv"); });
  function upd() {
    var vh = innerHeight;
    figs.forEach(function (f) {
      var r = f.getBoundingClientRect(); if (r.bottom < -100 || r.top > vh + 100) return;
      var p = Math.max(0, Math.min(1, (vh - r.top) / (vh * .75)));
      f.style.setProperty("--px", p.toFixed(3));
    });
  }
  addEventListener("scroll", function () { requestAnimationFrame(upd); }, { passive: true }); addEventListener("resize", upd); upd();
})();
