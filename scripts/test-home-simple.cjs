const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const source=fs.readFileSync(require('node:path').join(__dirname,'../assets/sunflex-v2/home-simple.js'),'utf8');
function setup(reduce=false){
 const classes=new Set(),storyClasses=new Set(),events={},docEvents={},hevents={},props={};let focused=false,open=false,id=0,time=0;const frames=new Map();
 const cl=set=>({add:v=>set.add(v),remove:v=>set.delete(v),toggle(v,on){on?set.add(v):set.delete(v)}});
 const header={classList:cl(classes),contains:()=>focused,querySelector:()=>open?{}:null,addEventListener:(k,f)=>hevents[k]=f};
 const copy={},stage={offsetHeight:800},story={offsetHeight:2720,classList:cl(storyClasses),style:{setProperty:(k,v)=>props[k]=+v},getBoundingClientRect:()=>({top:800-win.scrollY}),querySelector:s=>s.includes('copy')?copy:stage};
 const media={matches:reduce,addEventListener(k,f){this.change=f}};
 const win={scrollY:0,matchMedia:()=>media,addEventListener(k,f){(events[k]??=[]).push(f)}};
 const doc={hidden:false,activeElement:{},querySelector:s=>s.includes('site-header')?header:story,addEventListener:(k,f)=>docEvents[k]=f};
 vm.runInNewContext(source,{document:doc,window:win,requestAnimationFrame:f=>{frames.set(++id,f);return id},cancelAnimationFrame:i=>frames.delete(i)});
 const flush=()=>{let n=0;while(frames.size){assert(++n<200,'animation must settle');time+=16.67;const batch=[...frames.values()];frames.clear();batch.forEach(f=>f(time));}};
 return{classes,storyClasses,props,copy,media,doc,stage,story,hevents,flush,scroll(y){win.scrollY=y;events.scroll.forEach(f=>f());flush()},focus(v){focused=v},open(v){open=v},resize(){events.resize.forEach(f=>f())},visibility(v){doc.hidden=v;docEvents.visibilitychange()},reduce(v){media.matches=v;media.change()},progress(p){this.scroll(800+1920*p)}};
}
const t=setup();assert(t.storyClasses.has('is-scrubbing'));assert.equal(t.props['--word-scale'],1);assert(t.copy.inert);
t.scroll(220);assert(t.classes.has('is-away'));t.scroll(180);assert(!t.classes.has('is-away'));
t.focus(true);t.scroll(400);assert(!t.classes.has('is-away'));t.focus(false);t.open(true);t.scroll(600);assert(!t.classes.has('is-away'));t.open(false);
t.progress(.3);assert(t.props['--word-scale']>1);assert.equal(t.props['--white-opacity'],0);assert.equal(t.props['--mask-opacity'],1);const middle=t.props['--word-scale'];
t.progress(.6);assert(t.props['--word-scale']>middle);assert(t.props['--mask-opacity']>0&&t.props['--mask-opacity']<1);assert(t.copy.inert);
t.progress(.9);assert.equal(t.props['--mask-opacity'],0);assert.equal(t.props['--copy-opacity'],1);assert(!t.copy.inert);
t.progress(.3);assert.equal(t.props['--word-scale'],middle);assert(t.copy.inert);
t.progress(-1);assert.equal(t.props['--word-scale'],1);t.progress(3);assert.equal(t.props['--word-scale'],24);
t.reduce(true);assert(!t.storyClasses.has('is-scrubbing'));assert(!t.copy.inert);t.reduce(false);assert(t.storyClasses.has('is-scrubbing'));
t.progress(.5);t.stage.offsetHeight=600;t.resize();assert(Number.isFinite(t.props['--word-scale']));t.visibility(true);t.scroll(0);t.visibility(false);assert.equal(t.props['--word-scale'],1);
const r=setup(true);assert(!r.storyClasses.has('is-scrubbing'));assert(!r.copy.inert);
console.log('PASS: header, scrub phases, reverse, overscroll, settling, resize, visibility, reduced-motion and hidden-link focus.');
