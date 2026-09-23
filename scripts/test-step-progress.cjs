const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
function setup(kind,count=3,reduce=false){
 const element=()=>({id:'',dataset:{},attrs:{},events:{},children:[],offsetHeight:100,style:{values:{},setProperty(k,v){this.values[k]=v}},classList:{add(){},remove(){}},setAttribute(k,v){this.attrs[k]=v},removeAttribute(){},addEventListener(k,v){this.events[k]=v},contains(){return false},focus(){},getBoundingClientRect(){return {top:1000,bottom:1600}},querySelector(){return null},querySelectorAll(){return []}});
 const buttons=Array.from({length:count},element),panels=Array.from({length:count},element);
 buttons.forEach(b=>{b.bar=element();b.querySelector=()=>b.bar});
 const stage=element(),controls=element(),track=element(),root=element();stage.offsetHeight=400;controls.offsetHeight=50;
 controls.querySelectorAll=()=>buttons;
 track.querySelector=s=>s==='.product-flow-stage'?stage:s==='.product-flow-tabs'?controls:null;
 track.querySelectorAll=s=>s==='[data-flow-panel]'?panels:[];
 const media={matches:reduce,addEventListener(){}};
 let flow,tweens=0;const triggers=[];
 const ScrollTrigger={create(config){const t={vars:config,progress:0,start:1000,end:3000,kill(){}};triggers.push(t);if(config.onUpdate)flow=t;return t},refresh(){triggers.forEach(t=>t.vars.onRefresh?.(t))},update(){}};
 const gsap={registerPlugin(){},killTweensOf(){},set(){},from(){},to(){},fromTo(){tweens++},context(fn){fn();return{revert(){}}},matchMedia(){return{add(){}}},ticker:{add(){},remove(){},lagSmoothing(){}}};
 root.dataset={motionEngine:'gsap'};root.scrollHeight=10000;
 const document={documentElement:root,activeElement:null,addEventListener(){},getElementById(){return null},fonts:{ready:{then(fn){if(kind==='cctv')fn()}}},querySelector(s){if(s==='.story-stage')return stage;return null},querySelectorAll(s){if(s==='[data-scroll-flow]')return [track];if(s==='.story-panel')return panels;if(s==='.story-tabs button')return buttons;return []}};
 const env={document,gsap,ScrollTrigger,URLSearchParams,location:{search:'',hash:''},innerWidth:390,innerHeight:844,scrollY:0,matchMedia:s=>s.includes('prefers-reduced')?media:{matches:false,addEventListener(){}},addEventListener(){},scrollTo(){},requestAnimationFrame:f=>f(),cancelAnimationFrame(){},history:{pushState(){}}};env.window=env;
 vm.runInNewContext(fs.readFileSync(kind==='shared'?'assets/sunflex-v2/site-motion.js':'assets/sunflex-v2/cctv-motion/motion.js','utf8'),env);
 return {buttons,panels,flow,values:()=>buttons.map(b=>kind==='shared'?Number(b.style.values['--step-progress']):Number(b.bar.style.transform.match(/scaleX\((.+)\)/)[1])),update(p){flow.progress=p;flow.vars.onUpdate(flow)},refresh(p){flow.progress=p;flow.vars.onRefresh(flow)},tweens:()=>tweens};
}
for(const kind of ['shared','cctv']){
 for(const count of kind==='shared'?[3,4,5]:[3]){
  const t=setup(kind,count);
  const close=expected=>t.values().forEach((v,i)=>assert(Math.abs(v-expected[i])<1e-8,kind+' '+t.values()));
  close(Array(count).fill(0));
  t.update(.25/count);close([.25,...Array(count-1).fill(0)]);
  const before=t.tweens();t.update(.75/count);close([.75,...Array(count-1).fill(0)]);assert.equal(t.tweens(),before,'progress must not restart panel/text tween');
  t.update(1.5/count);close([1,.5,...Array(count-2).fill(0)]);assert.equal(t.buttons[1].attrs['aria-selected'],'true');
  t.update(1);close(Array(count).fill(1));
  t.update(.2/count);close([.2,...Array(count-1).fill(0)]);assert.equal(t.buttons[0].attrs['aria-selected'],'true');
  t.refresh(1.25/count);close([1,.25,...Array(count-2).fill(0)]);
 }
 assert.equal(setup(kind,3,true).flow,undefined,'reduced motion uses normal tabs');
}
console.log('PASS: shared 3/4/5-step and CCTV bars track forward/reverse scroll, boundaries and refresh; no same-step text tween; reduced-motion tabs preserved');
