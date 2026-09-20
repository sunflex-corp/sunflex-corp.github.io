const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const source=fs.readFileSync(require('node:path').join(__dirname,'../assets/sunflex-v2/product-editorial.js'),'utf8');
function element(id=''){
 const classes=new Set();return{id,hidden:false,attrs:{},events:{},style:{values:{},setProperty(k,v){this.values[k]=v}},classList:{add:x=>classes.add(x),remove:x=>classes.delete(x),contains:x=>classes.has(x),toggle(x,on){on?classes.add(x):classes.delete(x)}},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},addEventListener(k,f){this.events[k]=f},click(){this.events.click?.()},focus(){this.focused=true},scrollIntoView(){this.scrolled=true}};
}
function setup(reduce=false,short=false,hash=''){
 const buttons=['s','m','l'].map(x=>element('model-tab-'+x)),panels=['s','m','l'].map(x=>element('model-'+x));
 const controls=element(),outer=element(),compare=element(),model=element();controls.querySelectorAll=()=>buttons;
 model.querySelector=s=>s==='.model-tabs'?controls:s==='.model-controls'?outer:compare;model.querySelectorAll=()=>panels;
 const stage={offsetHeight:700},motion=element();motion.offsetHeight=1700;motion.top=66;motion.querySelector=()=>stage;motion.getBoundingClientRect=()=>({top:motion.top});
 const media={matches:reduce,addEventListener(k,f){this.change=f}},compact={matches:short,addEventListener(k,f){this.change=f}};
 const win={innerHeight:800,events:{},matchMedia:q=>q.includes('reduced')?media:compact,addEventListener(k,f){(this.events[k]??=[]).push(f)}};
 const doc={hidden:false,events:{},querySelector(s){if(s==='[data-model-selector]')return model;if(s.startsWith('[aria-controls='))return buttons[2];return null},querySelectorAll:s=>s==='[data-product-motion]'?[motion]:[],getElementById:id=>panels.find(p=>p.id===id),addEventListener(k,f){this.events[k]=f}};
 panels.forEach(p=>p.closest=()=>p);
 let count=0,time=0;const frames=new Map();
 vm.runInNewContext(source,{window:win,document:doc,location:{hash},requestAnimationFrame:f=>{frames.set(++count,f);return count},cancelAnimationFrame:i=>frames.delete(i)});
 function flush(){let rounds=0;while(frames.size){assert(++rounds<200,'must settle');time+=16.67;const f=[...frames.values()];frames.clear();f.forEach(fn=>fn(time));}}
 return{buttons,panels,compare,motion,media,compact,doc,win,flush,scroll(p){motion.top=66-1000*p;win.events.scroll.forEach(f=>f());flush()}};
}
const t=setup();t.flush();assert.deepEqual(t.panels.map(p=>p.hidden),[false,true,true]);
t.buttons[1].click();assert.deepEqual(t.panels.map(p=>p.hidden),[true,false,true]);
t.buttons[1].events.keydown({key:'End',preventDefault(){}});assert(t.buttons[2].focused);assert.equal(t.buttons[2].attrs['aria-selected'],'true');
t.compare.click();assert(t.panels.every(p=>!p.hidden));assert.equal(t.compare.attrs['aria-pressed'],'true');
t.compare.click();assert.deepEqual(t.panels.map(p=>p.hidden),[true,true,false]);
t.buttons[2].events.keydown({key:'ArrowRight',preventDefault(){}});assert.equal(t.buttons[0].tabIndex,0);
t.scroll(0);assert.equal(t.motion.style.values['--fan-shift'],'95%');t.scroll(.5);const middle=parseFloat(t.motion.style.values['--fan-shift']);assert(middle>0&&middle<95);t.scroll(1);assert.equal(t.motion.style.values['--fan-shift'],'0%');t.scroll(.5);assert(Math.abs(parseFloat(t.motion.style.values['--fan-shift'])-middle)<.01);t.scroll(-2);assert.equal(t.motion.style.values['--fan-shift'],'95%');
t.media.matches=true;t.media.change();assert(!t.motion.classList.contains('motion-enabled'));t.media.matches=false;t.media.change();assert(t.motion.classList.contains('motion-enabled'));
assert(!setup(true).motion.classList.contains('motion-enabled'));assert(!setup(false,true).motion.classList.contains('motion-enabled'));
const linked=setup(false,false,'#model-l');assert(!linked.panels[2].hidden);assert(linked.panels[2].scrolled);assert.doesNotThrow(()=>setup(false,false,'#%zz'));
console.log('PASS: model selection, keyboard wrapping, comparison, deep links, malformed fragments, reversible scroll, settling and reduced/short-screen fallback.');
