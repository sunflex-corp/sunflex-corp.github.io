const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../assets/sunflex-v2/home-simple.js'),'utf8');
function setup(reduce=false){
 const classes=new Set(),visualClasses=new Set(),events={},hevents={},buttons=Array.from({length:4},()=>({addEventListener(k,f){this[k]=f}}));let focused=false,open=false;
 const cl=set=>({add:v=>set.add(v),remove:v=>set.delete(v),toggle(v,on){on?set.add(v):set.delete(v)}});
 const header={classList:cl(classes),contains:()=>focused,querySelector:()=>open?{}:null,addEventListener:(k,f)=>hevents[k]=f};
 const visual={classList:cl(visualClasses)};let observer;
 class IO{constructor(fn){this.fn=fn;observer=this}observe(){}disconnect(){this.disconnected=true}}
 const media={matches:reduce,addEventListener(k,f){this.change=f}};
 const win={scrollY:0,IntersectionObserver:IO,matchMedia:()=>media,addEventListener:(k,f)=>events[k]=f};
 const doc={activeElement:{},querySelector:s=>s.endsWith('.site-header')?header:visual,querySelectorAll:()=>buttons};
 vm.runInNewContext(source,{document:doc,window:win,requestAnimationFrame:f=>f(),IntersectionObserver:IO});
 return{classes,visualClasses,events,hevents,media,buttons,get observer(){return observer},scroll(y){win.scrollY=y;events.scroll()},focus(v){focused=v},open(v){open=v}};
}
const t=setup();assert(!t.classes.has('is-scrolled'));assert(t.visualClasses.has('brand-reveal-ready'));
t.scroll(220);assert(t.classes.has('is-scrolled'));assert(t.classes.has('is-away'));
t.scroll(180);assert(!t.classes.has('is-away'));
t.focus(true);t.scroll(400);assert(!t.classes.has('is-away'));t.focus(false);t.open(true);t.scroll(600);assert(!t.classes.has('is-away'));
t.open(false);t.scroll(800);assert(t.classes.has('is-away'));t.hevents.focusin();assert(!t.classes.has('is-away'));t.scroll(0);assert(!t.classes.has('is-scrolled'));
t.observer.fn([{isIntersecting:true}]);assert(t.visualClasses.has('brand-revealed'));assert(t.observer.disconnected);
const manual=setup();manual.buttons[2].click();assert(manual.visualClasses.has('brand-revealed'));
const preference=setup();preference.media.change({matches:true});assert(preference.visualClasses.has('brand-revealed'));
const reduced=setup(true);assert(!reduced.visualClasses.has('brand-reveal-ready'));assert(!reduced.observer);
console.log('PASS: transparent/solid header, direction change, keyboard/open-menu visibility, top reset, one-time brand reveal, manual override and reduced motion.');
