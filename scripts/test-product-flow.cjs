const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const {sceneAt}=require('../assets/sunflex-v2/product-flow.js');
for(const count of [3,4,5]){
 assert.equal(sceneAt(-1,count).selected,0);assert.equal(sceneAt(count+1,count).selected,count-1);
 for(let boundary=1;boundary<count;boundary++){
  const before=sceneAt(boundary-.001,count),after=sceneAt(boundary+.001,count);
  assert(Math.abs(before.index+before.blend-after.index-after.blend)<.002,'continuous scene handoff');
 }
 const midway=sceneAt(.825,count);assert(Math.abs(midway.blend-.5)<.00001,'both frames blend during the transition');
 assert.equal(sceneAt(.3,count).blend,0,'reading dwell before transition');
}
function run(count=3,height=900,reduce=false,panelHeight=300,width=1440){
 let writes=0,y=0,id=0;const queue=new Map();
 const el=()=>({attrs:{},events:{},dataset:{},offsetHeight:panelHeight,hidden:false,inert:false,
 style:{setProperty(k,v){this[k]=v},removeProperty(k){delete this[k]}},
 classList:{add(k){this[k]=true},remove(k){this[k]=false},toggle(k,v){this[k]=v}},
 setAttribute(k,v){writes++;this.attrs[k]=v},addEventListener(k,v){this.events[k]=v},focus(){this.focused=true},remove(){},
 getBoundingClientRect(){return{height:this.offsetHeight,top:1000-y}}});
 const panels=Array.from({length:count},el),buttons=Array.from({length:count},(_,i)=>Object.assign(el(),{id:'b'+i}));
 const controls=el();controls.offsetHeight=60;controls.querySelectorAll=()=>buttons;
 const stage=el(),track=el();track.querySelector=s=>s==='.product-flow-stage'?stage:controls;track.querySelectorAll=()=>panels;
 const media={matches:reduce,addEventListener(k,f){this.change=f}};const events={};
 const win={innerHeight:height,innerWidth:width,scrollY:0,matchMedia:q=>q.includes('reduced')?media:{matches:false},addEventListener(k,f){events[k]=f},scrollTo(p){this.scrollY=p.top;y=p.top;events.scroll();this.lastBehavior=p.behavior;}};
 const doc={hidden:false,body:{append(){}},createElement(){const node=el();node.offsetHeight=height;return node},querySelectorAll:()=>[track],querySelector:()=>null,addEventListener(){}};
 vm.runInNewContext(fs.readFileSync('assets/sunflex-v2/product-flow.js','utf8'),{window:win,document:doc,requestAnimationFrame:f=>{queue.set(++id,f);return id},cancelAnimationFrame:i=>queue.delete(i)});
 const flush=()=>{const callbacks=[...queue.values()];queue.clear();callbacks.forEach(f=>f())};flush();
 return{buttons,panels,track,win,media,flush,get writes(){return writes},get pending(){return queue.size},scroll(n){win.scrollY=n;y=n;events.scroll();flush()},events};
}
for(const count of [3,4,5]){
 const t=run(count);assert(t.track.classList['flow-pinned']);
 t.buttons[count-1].events.click();t.flush();assert.equal(t.buttons[count-1].attrs['aria-selected'],'true');assert.equal(t.win.lastBehavior,'smooth');
 t.scroll(0);assert.equal(t.panels[0].inert,false);assert.equal(t.buttons[1].attrs['data-step-state'],'upcoming');
 const writes=t.writes;t.scroll(1);assert.equal(t.writes,writes,'no repeated accessibility writes within a scene');
 const start=1000-parseFloat(t.track.style['--flow-top']);
 const stride=parseFloat(t.track.style['--flow-span'])/count;
 t.scroll(start+stride*.825);
 assert(t.panels.slice(0,2).every(p=>Number(p.style['--flow-copy-alpha'])<.00001),'text does not double-expose at crossfade midpoint');
 t.scroll(start+stride*1.25);
 assert.equal(t.panels[1].style['--flow-copy-alpha'],'1','next sentence is fully legible during dwell');
 t.scroll(100000);assert.equal(t.panels[count-1].inert,false);assert.equal(t.panels[0].inert,true);
 t.buttons[count-1].events.keydown({key:'Home',preventDefault(){}});t.flush();assert(t.buttons[0].focused);assert.equal(t.panels[0].inert,false);
 assert(t.panels.every(p=>!p.hidden),'shared layout retains all scene dimensions');
 t.media.matches=true;t.media.change();t.flush();assert.equal(t.track.classList['flow-pinned'],true,'reduced motion preserves numbered navigation');
 t.buttons[1].events.click();t.flush();assert.equal(t.win.lastBehavior,'instant');
 assert.equal(t.pending,0,'no permanent animation loop');
}
assert.equal(run(3,600).track.classList['flow-pinned'],true,'short desktop fits');
assert.equal(run(3,844,false,300,390).track.classList['flow-pinned'],true,'mobile fits');
const overflow=run(3,600,false,950,390);assert.equal(overflow.track.dataset.flowMode,'reading');assert(overflow.panels.every(p=>!p.inert&&!p.hidden),'enlarged content remains readable');
console.log('PASS: continuous forward/reverse blending, dwell, 3/4/5 steps, mobile/short pins, focus, reduced motion, readable overflow, no repeated ARIA writes or idle loop');
