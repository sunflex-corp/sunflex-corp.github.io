const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync(require('node:path').join(__dirname,'../assets/sunflex-v2/home-motion.js'),'utf8');
function element() {
 const classes=new Set();
 return {dataset:{},attrs:{},handlers:{},hidden:false,textContent:'',style:{setProperty(){}},classList:{add(x){classes.add(x)},remove(x){classes.delete(x)},contains(x){return classes.has(x)},toggle(x,on){if(on===undefined)on=!classes.has(x);if(on)classes.add(x);else classes.delete(x);return on}},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.handlers[k]=f},getBoundingClientRect(){return {top:1500}},animate(){return {cancel(){}}},querySelector(s){return this.children[s]},querySelectorAll(s){return this.children[s]},children:{}};
}
function setup(reduce=false){
 const hero=element(),map=element(),play=element(),caption=element(),mapMotion=element();
 const slides=Array.from({length:3},()=>{const s=element();s.children.img={decode:()=>Promise.resolve()};return s});
 const buttons=Array.from({length:3},()=>{const b=element();b.children.i=element();return b});
 const choices=Array.from({length:4},element),panels=Array.from({length:4},element);
 const next=element(),prev=element(),status=element();
 hero.children={'.scene':slides,'[data-select]':buttons,'[data-play]':play,'.scene-caption':caption,'[data-next]':next,'[data-prev]':prev,'#scene-status':status,'.scene-controls':element()};
 caption.children={'.scene-topic':element(),'.scene-title':element(),'.scene-description':element()};
 const media={matches:reduce,addEventListener(k,f){this.change=f}};
 const observers=[];
 class Observer{constructor(cb){this.cb=cb;observers.push(this)}observe(e){this.target=e}unobserve(){}}
 const doc={hidden:false,handlers:{},addEventListener(k,f){this.handlers[k]=f},querySelector(s){return {'.cinema':hero,'.map-visual':map,'.map-motion-toggle':mapMotion}[s]},querySelectorAll(s){if(s==='[data-map-choice]')return choices;if(s==='.map-panel')return panels;return []}};
 let serial=0;const timers=new Map();
 vm.runInNewContext(source,{document:doc,window:{matchMedia:()=>media,IntersectionObserver:Observer,innerHeight:900},IntersectionObserver:Observer,setTimeout(f){timers.set(++serial,f);return serial},clearTimeout(id){timers.delete(id)}});
 return {hero,map,play,slides,buttons,choices,panels,media,doc,observers,timers,next,prev,status,mapMotion,tick(){const [id,fn]=[...timers][0];timers.delete(id);fn()}};
}
const flush=()=>new Promise(resolve=>setImmediate(resolve));
(async()=>{
 const t=setup();assert.equal(t.timers.size,1);t.tick();await flush();assert.equal(t.hero.dataset.current,'1');
 t.play.handlers.click();assert.equal(t.timers.size,0);t.play.handlers.click();assert.equal(t.timers.size,1);
 t.prev.handlers.click();await flush();assert.equal(t.hero.dataset.current,'0');assert.equal(t.timers.size,0);
 t.prev.handlers.click();await flush();assert.equal(t.hero.dataset.current,'2');assert.equal(t.buttons[2].attrs['aria-pressed'],'true');
 t.choices[2].handlers.click();assert.equal(t.map.dataset.mode,'2');assert.equal(t.panels[2].hidden,false);assert.equal(t.panels[0].hidden,true);
 t.choices[3].handlers.click();assert.equal(t.map.dataset.mode,'3');assert.equal(t.panels[3].hidden,false);assert.equal(t.panels[2].hidden,true);
 t.mapMotion.handlers.click();assert.equal(t.map.classList.contains('motion-off'),true);
 t.play.handlers.click();t.doc.hidden=true;t.doc.handlers.visibilitychange();assert.equal(t.timers.size,0);
 t.doc.hidden=false;t.doc.handlers.visibilitychange();assert.equal(t.timers.size,1);
 t.observers[0].cb([{isIntersecting:false}]);assert.equal(t.timers.size,0);t.observers[0].cb([{isIntersecting:true}]);assert.equal(t.timers.size,1);
 t.hero.handlers.focusin({target:t.next});assert.equal(t.timers.size,0);
 const r=setup(true);assert.equal(r.timers.size,0);assert.equal(r.play.textContent,'다음 장면');r.next.handlers.click();await flush();assert.equal(r.hero.dataset.current,'1');assert.equal(r.timers.size,0);
 const fail=setup();fail.slides[1].children.img.decode=()=>Promise.reject(Error('offline'));fail.next.handlers.click();await flush();assert.equal(fail.hero.dataset.current,'0');assert.equal(fail.timers.size,0);assert.match(fail.status.textContent,/불러오지/);
 const race=setup();let resolve;race.slides[1].children.img.decode=()=>new Promise(r=>resolve=r);race.buttons[1].handlers.click();race.buttons[2].handlers.click();await flush();resolve();await flush();assert.equal(race.hero.dataset.current,'2');
 console.log('PASS: timed rotation, pause/resume, wraparound, manual selection, infographic selection/pause, visibility/offscreen/focus, reduced motion, failed image, rapid selection race.');
})();
