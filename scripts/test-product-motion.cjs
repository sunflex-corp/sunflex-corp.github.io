const assert=require('node:assert/strict');
const {plan,pose}=require('../assets/sunflex-v2/product-motion.js');
assert.notEqual(plan('wear').from,plan('site').from);
assert.notEqual(plan('dashboard').from,plan('network').from);
assert(plan('site',-1).from.includes('-48px'));
for(const mobile of [false,true])for(const progress of [-10,0,.25,.5,.75,1,10]){
 const p=pose(progress,mobile);assert(p.scale>=1&&p.scale<=1.065);assert(Math.abs(p.y)<=(mobile?6:18));
}
assert.deepEqual(pose(-1,false),pose(0,false));assert.deepEqual(pose(2,false),pose(1,false));
assert(pose(.2,false).y>pose(.8,false).y);
console.log('PASS: distinct motion profiles, reverse direction, clamped scale/depth, mobile amplitude');
// Exercise scheduling and accessibility against the actual runtime, without a browser driver.
const vm=require('node:vm'),fs=require('node:fs');
const listeners={},observers=[],queue=new Map();let next=0,cancelled=0,animated=0;
const media={matches:false,addEventListener:(name,fn)=>listeners.reduced=fn};
const style={transform:'',removeProperty(name){delete this[name];}};
const picture={classList:{add(){}},querySelector:()=>({style}),getBoundingClientRect:()=>({top:100,height:300})};
const heading={matches:()=>false,animate(){animated++;return {cancel(){cancelled++;this.oncancel?.();}};}};
const root={dataset:{motionProfile:'site'},querySelectorAll(selector){if(selector.includes('.revision-proof a'))return [picture];if(selector.includes('.editorial-hero-media'))return [heading];return [];}};
const doc={hidden:false,querySelector:()=>root,addEventListener:(name,fn)=>listeners[name]=fn};
const context={document:doc,Element:function(){},IntersectionObserver:class{constructor(callback){this.callback=callback;observers.push(this);}observe(){}unobserve(){}},MutationObserver:class{},matchMedia:q=>q.includes('reduced')?media:{matches:false},window:{addEventListener:(name,fn)=>listeners[name]=fn},innerHeight:900,requestAnimationFrame:fn=>{queue.set(++next,fn);return next;},cancelAnimationFrame:id=>queue.delete(id),Set,WeakMap};
context.Element.prototype.animate=()=>{};
vm.runInNewContext(fs.readFileSync(require.resolve('../assets/sunflex-v2/product-motion.js'),'utf8'),context);
observers[0].callback([{target:picture,isIntersecting:true}]);listeners.scroll();listeners.scroll();assert.equal(queue.size,1,'coalesces scroll updates');
let callback=[...queue.values()][0];queue.clear();callback();assert(style.transform.includes('scale('));assert.equal(queue.size,0,'no perpetual frame loop');
observers[1].callback([{target:heading,isIntersecting:true}]);assert.equal(animated,1);
media.matches=true;listeners.reduced();assert.equal(cancelled,1);assert.equal(style.transform,undefined);listeners.scroll();assert.equal(queue.size,0);
observers[1].callback([{target:heading,isIntersecting:true}]);assert.equal(animated,1,'reduced motion prevents animation');
media.matches=false;doc.hidden=true;listeners.visibilitychange();listeners.scroll();assert.equal(queue.size,0,'hidden document does no work');
console.log('PASS: one frame per scroll batch, idle stops, reduced-motion cancellation, hidden-page suspension');
