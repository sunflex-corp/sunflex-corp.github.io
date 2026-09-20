const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../assets/sunflex-v2/site.js'), 'utf8');
function setup(clipboardFails = false) {
  const elements = new Map();
  const el = selector => {
    if (!elements.has(selector)) elements.set(selector, { hidden: true, textContent: '', handlers: {}, attrs: {}, addEventListener(k,f){this.handlers[k]=f;}, setAttribute(k,v){this.attrs[k]=v;}, getAttribute(k){return this.attrs[k];}, focus(){this.focused=true;}, select(){this.selected=true;}, querySelector(){return el('fallback-text');} });
    return elements.get(selector);
  };
  let copied;
  const data = {field:'  테스트 물류센터  ',area:'출입구 & 통로',need:'영상 확인\n알림',reply:'test@example.com'};
  const document = { querySelector:el, addEventListener(k,f){this[k]=f;} };
  const window = {location:{href:''},matchMedia(){return {addEventListener(k,f){window.media=f;}};}};
  vm.runInNewContext(source,{document,window,FormData:class{get(k){return data[k];}},navigator:{clipboard:{async writeText(v){if(clipboardFails)throw Error('denied');copied=v;}}}});
  return {el,document,window,get copied(){return copied;}};
}
(async()=>{
  const t=setup();
  assert.equal(t.el('.menu-toggle').hidden,false);
  t.el('.menu-toggle').handlers.click();
  assert.equal(t.el('#mobile-nav').hidden,false);
  t.document.keydown({key:'Escape'});
  assert.equal(t.el('#mobile-nav').hidden,true);
  assert.equal(t.el('.menu-toggle').focused,true);
  let prevented=false;
  t.el('#inquiry-form').handlers.submit({preventDefault(){prevented=true;}});
  assert.ok(prevented);
  const draft=new URL(t.window.location.href);
  assert.equal(draft.pathname,'jiyoueng@daum.net');
  assert.equal(draft.searchParams.get('subject'),'썬플렉스 도입 문의');
  assert.match(draft.searchParams.get('body'),/현장 유형: 테스트 물류센터/);
  assert.match(draft.searchParams.get('body'),/출입구 & 통로/);
  assert.match(draft.searchParams.get('body'),/전원·통신 조건: 미정/);
  await t.el('#copy-inquiry').handlers.click();
  assert.equal(t.copied,draft.searchParams.get('body'));
  const fallback=setup(true);
  await fallback.el('#copy-inquiry').handlers.click();
  assert.equal(fallback.el('#draft-fallback').hidden,false);
  assert.equal(fallback.el('fallback-text').selected,true);
  assert.match(fallback.el('fallback-text').value,/테스트 물류센터/);
  console.log('PASS: menu keyboard control, encoded email draft, blank fields, clipboard success and fallback. No email sent.');
})();
