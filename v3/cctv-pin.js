/* 이동식 CCTV "사이즈는 셋": the model block pins while scrolling steps S -> M -> L (tabs still work) */
(function () {
  var sec = document.getElementById("models"), lay = sec && sec.querySelector(".model-layout");
  if (!lay) return;
  var btns = [].slice.call(sec.querySelectorAll("[data-model]")), n = btns.length, cur = 0, on = false, top = 0, range = 0;
  var pin = document.createElement("div"); pin.className = "model-pin";
  lay.parentNode.insertBefore(pin, lay); pin.appendChild(lay);
  function headH() { var l = document.querySelector(".pd-local"); return l ? Math.max(0, l.getBoundingClientRect().bottom) : 64; }
  function layout() {
    pin.style.height = ""; lay.classList.remove("is-pinned"); lay.style.top = "";
    var vh = innerHeight, h = lay.offsetHeight, hh = 121;
    on = innerWidth > 900 && h + 24 < vh - hh;
    if (!on) return;
    top = Math.round(hh + Math.max(12, (vh - hh - h) / 2));
    range = n * vh * 0.55;
    pin.style.height = (h + range) + "px";
    lay.classList.add("is-pinned"); lay.style.top = top + "px";
  }
  function update() {
    if (!on) return;
    var r = pin.getBoundingClientRect(), p = (top - r.top) / range, k = Math.max(0, Math.min(n - 1, Math.floor(Math.max(0, Math.min(.999, p)) * n)));
    if (k !== cur) { cur = k; btns[k].click(); }
    lay.style.setProperty("--model-p", Math.max(0, Math.min(1, p)));
  }
  btns.forEach(function (b, i) {
    b.addEventListener("click", function (e) {
      cur = i;
      if (on && e.isTrusted) scrollTo({ top: pin.getBoundingClientRect().top + scrollY - top + range * (i + .5) / n, behavior: "smooth" });
    });
  });
  addEventListener("scroll", update, { passive: true });
  addEventListener("resize", function () { layout(); update(); });
  var lastY = -1; setInterval(function () { if (scrollY !== lastY) { lastY = scrollY; update(); } }, 200);
  addEventListener("load", function () { layout(); update(); });
  layout(); update();
})();
