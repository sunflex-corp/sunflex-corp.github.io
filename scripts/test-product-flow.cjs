const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
function run(count=3,height=900,reduce=false,panelHeight=300){
 const el=()=>({attrs:{},events:{},hidden:false,style:{setProperty(){}},classList:{add(){},toggle(k,v){this[k]=v}},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,v){this.events[k]=v},focus(){this.focused=true},getBoundingClientRect(){return{height:panelHeight}}});
 const panels=Array.from({length:count},el),buttons=Array.from({length:count},(_,i)=>Object.assign(el(),{id:'b'+i}));
 const controls=el();controls.querySelectorAll=()=>buttons;controls.getBoundingClientRect=()=>({height:60});
 const stage=el(),track=el();let y=0;track.querySelector=s=>s==='.product-flow-stage'?stage:controls;track.querySelectorAll=s=>s==='img'?[]:panels;track.getBoundingClientRect=()=>({top:1000-y});
 const media={matches:reduce,addEventListener(k,f){this.change=f}};const events={};let frame;
 const win={innerHeight:height,scrollY:0,matchMedia:()=>media,addEventListener(k,f){events[k]=f},scrollTo(p){this.scrollY=p.top;y=p.top;events.scroll();}};
 vm.runInNewContext(fs.readFileSync('assets/sunflex-v2/product-flow.js','utf8'),{window:win,document:{querySelectorAll:()=>[track],querySelector:()=>null},requestAnimationFrame:f=>{frame=f;return 1}});
 const flush=()=>{if(frame){let f=frame;frame=null;f()}};flush();
 return{buttons,panels,track,win,media,flush,scroll(n){win.scrollY=n;y=n;events.scroll();flush()}};
}
for(const count of [3,4,5]){
 const t=run(count);assert(t.track.classList['flow-pinned']);
 t.buttons[count-1].events.click();t.flush();assert.equal(t.panels[count-1].hidden,false);
 t.scroll(0);assert.equal(t.panels[0].hidden,false);assert.equal(t.buttons[1].attrs['data-step-state'],'upcoming');
 t.scroll(100000);assert.equal(t.panels[count-1].hidden,false);
 t.buttons[count-1].events.keydown({key:'Home',preventDefault(){}});t.flush();assert(t.buttons[0].focused);assert.equal(t.panels[0].hidden,false);
 t.media.matches=true;t.media.change();assert.equal(t.track.classList['flow-pinned'],false);
}
assert.equal(run(3,600).track.classList['flow-pinned'],false);
assert.equal(run(3,900,false,950).track.classList['flow-pinned'],false);
assert.equal(run(3,900,true).track.classList['flow-pinned'],false);
console.log('PASS: 3/4/5 stages, forward/reverse, click/scroll sync, keyboard, upcoming state, reduced motion and overflow fallback');
