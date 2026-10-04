// Usage (from repo root): python3 -m http.server 8765 & node scripts/qa/scroll-audit.cjs [slug,slug] [mobile,tablet,pc]
// Writes per-step screenshots + metrics.json to ./scroll-audit-out/<slug>/<viewport>/ (see SCROLL_REVIEW_AUDIT.md)
// Slow scroll audit: every product page x {mobile, tablet, pc}.
// For each page: scroll one step (~70% of viewport) at a time with real wheel input,
// wait for animations, screenshot, and record per-step metrics.
const { chromium } = (()=>{try{return require('playwright')}catch(e){return require('/opt/node22/lib/node_modules/playwright')}})();
const fs = require('fs'), path = require('path');
const OUT = process.env.OUT || path.join(process.cwd(), 'scroll-audit-out');
const BASE = process.env.BASE || 'http://127.0.0.1:8765';
// the Pretendard CDN stylesheet may be unreachable in sandboxes: serve the site's own @font-face rules instead
const FONT_CSS = (fs.readFileSync('_astro/BaseLayout.a023156454.css', 'utf8').match(/@font-face\{font-family:Pretendard Variable[^}]*\}/g) || []).join('');
const VPS = {
  mobile: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 1 },
  tablet: { viewport: { width: 820, height: 1180 }, isMobile: true, hasTouch: true, deviceScaleFactor: 1 },
  pc: { viewport: { width: 1440, height: 900 }, isMobile: false, hasTouch: false, deviceScaleFactor: 1 },
};
const slugs = (process.argv[2] ? process.argv[2].split(',') : fs.readdirSync('products').filter(d => fs.existsSync(`products/${d}/index.html`)));
const only = process.argv[3] ? process.argv[3].split(',') : Object.keys(VPS);

// runs in page: inspect the current viewport
function probe() {
  const W = innerWidth, H = innerHeight, out = {};
  const de = document.documentElement;
  out.scrollW = Math.max(de.scrollWidth, document.body.scrollWidth);
  out.y = scrollY;
  const vis = el => { const cs = getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const effOpacity = el => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= +getComputedStyle(n).opacity; return o; };
  const desc = el => {
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    if (el.classList.length) s += '.' + [...el.classList].slice(0, 3).join('.');
    const sec = el.closest('section,[id]');
    if (sec && sec !== el) s = (sec.id ? '#' + sec.id : sec.tagName.toLowerCase() + '.' + [...sec.classList].slice(0, 2).join('.')) + ' > ' + s;
    return s;
  };
  // clipped by ancestor overflow?
  const clippedX = el => { for (let n = el.parentElement; n && n !== document.body; n = n.parentElement) { const ox = getComputedStyle(n).overflowX; if (ox !== 'visible') return true; } return false; };
  const all = [...document.body.querySelectorAll('*')];
  // elements wider than viewport horizontally (not inside clipping/scroll containers)
  out.overflowX = [];
  // text in viewport that is invisible (opacity ~0) -> reveal never fired
  out.hiddenText = [];
  out.tinyText = [];
  out.textClip = [];
  out.smallTap = [];
  out.brokenImg = [];
  out.overlapHeader = null;
  for (const el of all) {
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const inView = r.bottom > 0 && r.top < H;
    const inViewX = r.right > 0 && r.left < W;
    if ((r.right > W + 1 || r.left < -1) && !clippedX(el) && getComputedStyle(el).position !== 'fixed') {
      if (out.overflowX.length < 8) out.overflowX.push(desc(el) + ` [${Math.round(r.left)}..${Math.round(r.right)}]`);
    }
    if (!inView) continue;
    const ownText = [...el.childNodes].some(c => c.nodeType === 3 && c.textContent.trim().length > 1);
    if (ownText && inViewX && r.top > 60 && r.bottom < H - 10) {
      const op = effOpacity(el);
      if (op < 0.15 && out.hiddenText.length < 6) out.hiddenText.push(desc(el) + ` op=${op.toFixed(2)} "${el.textContent.trim().slice(0, 30)}"`);
      const fs = parseFloat(getComputedStyle(el).fontSize);
      if (fs < 11 && op > 0.5 && out.tinyText.length < 6) out.tinyText.push(desc(el) + ` ${fs}px "${el.textContent.trim().slice(0, 20)}"`);
      const cs = getComputedStyle(el);
      if ((cs.overflow === 'hidden' || cs.textOverflow === 'ellipsis' || cs.overflowX === 'hidden') && (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 4) && out.textClip.length < 6)
        out.textClip.push(desc(el) + ` sw${el.scrollWidth}/cw${el.clientWidth} sh${el.scrollHeight}/ch${el.clientHeight} "${el.textContent.trim().slice(0, 24)}"`);
    }
    if ((el.tagName === 'A' || el.tagName === 'BUTTON' || el.getAttribute('role') === 'tab') && W < 900 && (r.height < 32 || r.width < 32) && effOpacity(el) > 0.5 && out.smallTap.length < 6)
      out.smallTap.push(desc(el) + ` ${Math.round(r.width)}x${Math.round(r.height)} "${el.textContent.trim().slice(0, 16)}"`);
    if (el.tagName === 'IMG' && el.complete && el.naturalWidth === 0 && el.getAttribute('src')) out.brokenImg.push(el.getAttribute('src'));
  }
  // fixed/sticky things covering the viewport
  out.fixed = [];
  for (const el of all) {
    const cs = getComputedStyle(el);
    if ((cs.position === 'fixed' || cs.position === 'sticky') && vis(el) && +cs.opacity > 0.05) {
      const r = el.getBoundingClientRect();
      if (r.width * r.height > 0 && r.bottom > 0 && r.top < H && r.width > W * 0.3) out.fixed.push(desc(el) + ` ${cs.position} top${Math.round(r.top)} h${Math.round(r.height)}`);
    }
  }
  // which section is at viewport center
  const c = document.elementFromPoint(W / 2, H / 2);
  const sec = c && c.closest('section');
  out.center = sec ? (sec.id || sec.className.split(' ').slice(0, 2).join('.')) : (c ? c.tagName : '');
  return out;
}

(async () => {
  const browser = await chromium.launch();
  for (const vpName of only) {
    for (const slug of slugs) {
      const dir = path.join(OUT, slug, vpName);
      fs.mkdirSync(dir, { recursive: true });
      const ctx = await browser.newContext({ ...VPS[vpName], locale: 'ko-KR' });
      await ctx.route('https://cdn.jsdelivr.net/**', r => r.fulfill({ status: 200, contentType: 'text/css', body: FONT_CSS }));
      const page = await ctx.newPage();
      const errors = [], failed = [];
      page.on('pageerror', e => errors.push(String(e.message).slice(0, 200)));
      page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text().slice(0, 200)); });
      page.on('response', r => { if (r.status() >= 400) failed.push(r.status() + ' ' + r.url().replace(BASE, '')); });
      page.on('requestfailed', r => failed.push('FAIL ' + r.url().replace(BASE, '')));
      await page.addInitScript(() => {
        window.__cls = 0;
        new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
      });
      await page.goto(`${BASE}/products/${slug}/`, { waitUntil: 'networkidle', timeout: 60000 }).catch(e => errors.push('goto ' + e.message));
      await page.waitForTimeout(1200);
      const H = VPS[vpName].viewport.height, W = VPS[vpName].viewport.width;
      const step = Math.round(H * 0.7);
      const steps = [];
      let i = 0, stuck = 0, lastY = -1;
      await page.mouse.move(W / 2, H / 2);
      while (i < 80) {
        const m = await page.evaluate(probe);
        const docH = await page.evaluate(() => document.documentElement.scrollHeight);
        const file = `${String(i).padStart(2, '0')}.jpg`;
        await page.screenshot({ path: path.join(dir, file), type: 'jpeg', quality: 62 });
        steps.push({ i, file, docH, ...m });
        if (m.y + H >= docH - 2) break;
        if (m.y === lastY) { if (++stuck >= 3) { steps.push({ i, note: 'scroll stuck at ' + m.y }); break; } } else stuck = 0;
        lastY = m.y;
        // slow wheel scroll in small notches
        for (let k = 0; k < 7; k++) { await page.mouse.wheel(0, step / 7); await page.waitForTimeout(45); }
        await page.waitForTimeout(750);
        i++;
      }
      const tail = await page.evaluate(() => ({ cls: window.__cls, docH: document.documentElement.scrollHeight, title: document.title }));
      // scroll back to top quickly to see if anything breaks on reverse
      await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(800);
      await page.screenshot({ path: path.join(dir, 'zz-back-top.jpg'), type: 'jpeg', quality: 62 });
      fs.writeFileSync(path.join(dir, 'metrics.json'), JSON.stringify({ slug, vp: vpName, W, H, ...tail, errors, failed: [...new Set(failed)], steps }, null, 1));
      console.log(vpName, slug, 'steps', steps.length, 'docH', tail.docH, 'err', errors.length, 'fail', failed.length, 'cls', tail.cls.toFixed(3));
      await ctx.close();
    }
  }
  await browser.close();
})();
