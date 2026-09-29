/* session-2 scripts. window.pdPin.make(section, target, steps, onProgress) pins a target while scrolling. */
(function () {
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var pin = window.pdPin;
  // step a component with scroll when it can pin (wide screens); otherwise advance as its parts come into view
  // parts[i] in view -> step i + off (story: off 0, follows scroll both ways; checklist: off 1, only moves forward)
  function drive(sec, target, n, set, parts, off) {
    off = off === undefined ? 1 : off;
    var it = pin && !still ? pin.make(sec, target, n, function (p) { set(Math.floor(p * n), p * n % 1); }) : null;
    if (still) { set(n - 1, 1); return it; }
    if (!("IntersectionObserver" in window)) { set(n - 1, 1); return it; }
    var seen = -1;
    var io = new IntersectionObserver(function (es) {
      if (it && it.on) return;
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var i = parts.indexOf(e.target), k = Math.min(n - 1, i + off);
        if (off === 0 || i > seen) { seen = Math.max(seen, i); set(k, 0); }
      });
    }, off === 0 ? { threshold: 0, rootMargin: "-55% 0px -30% 0px" } : { threshold: 0.6, rootMargin: "0px 0px -35% 0px" });
    parts.forEach(function (el) { io.observe(el); });
    return it;
  }
  window.s2drive = drive;
  // count a number between data-a and data-b (used by stage counters)
  function count(el, to) {
    var from = +el.textContent || 0, t0 = null;
    if (still) { el.textContent = to; return; }
    function f(ts) { if (!t0) t0 = ts; var q = Math.min(1, (ts - t0) / 900); el.textContent = Math.round(from + (to - from) * (1 - Math.pow(1 - q, 3))); if (q < 1) requestAnimationFrame(f); }
    requestAnimationFrame(f);
  }
  window.s2hooks = {
    "tunnel-call@emergency-signal-location": function (k, sy) { var b = sy.querySelector(".esl-n"); if (b) count(b, k >= 2 ? 5 : 0); },
    "band-functions@healthcare-heart-band": function (k, sy) { var b = sy.querySelector(".hhb-n"); if (b) { if (k === 0) b.textContent = "--"; else count(b, k >= 2 ? 128 : 84); } },
    "detail-2@power-assist-suit": function (k, sy) { var b = sy.querySelector(".pas-n"); if (b && k === 0) { b.textContent = 0; count(b, 36); } },
    "detail-4@safebridge": function (k, sy) { var b = sy.querySelector(".sbl-n"); if (b) count(b, k >= 1 ? 15 : 1); },
    "detail-2@worker-access-gate": function (k, sy) { sy.querySelectorAll(".wag-n").forEach(function (b) { count(b, +(k >= 2 ? b.dataset.b : b.dataset.a)); }); }
  };
  // stage canvases are drawn at 600x440 and scaled to the box like a picture
  var stages = [].slice.call(document.querySelectorAll(".s2-stage"));
  function fit() { stages.forEach(function (s) { s.style.setProperty("--sc", (s.clientWidth / 600).toFixed(4)); }); }
  fit(); addEventListener("resize", fit);
  if ("ResizeObserver" in window) { var ro = new ResizeObserver(fit); stages.forEach(function (s) { ro.observe(s); }); }

  /* 상담 준비 체크리스트: rows check off one by one, the ring fills, the CTA lifts at 3/3 */
  document.querySelectorAll("[data-s2ck]").forEach(function (ck) {
    var sec = ck.closest("section"), li = [].slice.call(ck.querySelectorAll(".s2-ck-list li"));
    var fg = ck.querySelector(".s2-ck-meter .fg"), num = ck.querySelector(".s2-ck-n"), k0 = -2;
    function set(k) {
      if (k === k0) return; k0 = k;
      ck.setAttribute("data-k", k);
      li.forEach(function (e, i) { e.classList.toggle("done", i < k); e.classList.toggle("cur", i === k); });
      if (fg) fg.style.strokeDashoffset = (326.7 * (1 - Math.max(0, k) / 3)).toFixed(1);
      if (num) num.textContent = Math.max(0, k);
    }
    set(0);
    li.forEach(function (e, i) { e.addEventListener("click", function () { set(i + 1); }); });
    // 4 steps: nothing checked, 1, 2, all three
    drive(sec, ck, 4, set, li);
  });

  /* 문제→해결 story: copy steps + stage parts ([data-s]) light up with scroll */
  document.querySelectorAll("[data-s2sy]").forEach(function (sy) {
    var sec = sy.closest("section"), li = [].slice.call(sy.querySelectorAll(".s2-sy-steps li")), n = li.length;
    var parts = [].slice.call(sy.querySelectorAll(".s2-stage [data-s]")), k0 = -1;
    function set(k, f) {
      sy.style.setProperty("--f", (f || 0).toFixed(3));
      if (k === k0) return; k0 = k;
      sy.setAttribute("data-k", k);
      li.forEach(function (e, i) { e.classList.toggle("on", i === k); e.classList.toggle("done", i < k); });
      parts.forEach(function (e) { var s = +e.getAttribute("data-s"); e.classList.toggle("on", k >= s); e.classList.toggle("now", k === s); });
      var h = window.s2hooks && window.s2hooks[sec.id + "@" + (document.querySelector("main[data-pd]") || {}).dataset.pd];
      if (h) h(k, sy);
    }
    set(0, 0);
    li.forEach(function (e, i) { e.addEventListener("click", function () { set(i, 0); }); });
    if (n > 1) drive(sec, sy, n, set, li, 0); else set(0, 1);
  });
})();
