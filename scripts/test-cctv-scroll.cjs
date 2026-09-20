const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
function setup(height=900,reduce=false){
 const element=()=>({attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,v){this.events[k]=v},focus(){this.focused=true}});
 const buttons=Array.from({length:3},(_,i)=>Object.assign(element(),{id:'tab'+i})),panels=buttons.map(element);
 let y=0,frame;const events={},classes={};
 const track={style:{setProperty(){}},classList:{toggle(k,v){classes[k]=v}},getBoundingClientRect:()=>({top:1000-y})};
 const controls={querySelectorAll:()=>buttons},root={querySelector:s=>s==='.cctv-step-controls'?controls:track,querySelectorAll:()=>panels};
 const media={matches:reduce,addEventListener(k,f){this.change=f}};
 const win={innerHeight:height,scrollY:0,matchMedia:()=>media,addEventListener(k,f){events[k]=f},scrollTo(p){y=p.top;this.scrollY=y;events.scroll();}};
 vm.runInNewContext(fs.readFileSync('assets/sunflex-v2/mobile-cctv.js','utf8'),{window:win,document:{querySelector:s=>s==='[data-cctv-process]'?root:null,getElementById:()=>null},location:{hash:''},requestAnimationFrame:f=>{frame=f;return 1}});
 const flush=()=>{if(frame){let f=frame;frame=null;f()}};flush();return{buttons,panels,classes,media,flush,scroll(n){y=n;win.scrollY=n;events.scroll();flush()}};
}
const t=setup();assert(t.classes['is-scroll-driven']);t.scroll(1800);assert.equal(t.panels[1].hidden,false);t.scroll(2500);assert.equal(t.panels[2].hidden,false);t.scroll(1000);assert.equal(t.panels[0].hidden,false);
t.buttons[2].events.click();t.flush();assert.equal(t.panels[2].hidden,false);t.buttons[0].events.click();t.flush();assert.equal(t.panels[0].hidden,false);
assert.equal(t.buttons[2].attrs['data-step-state'],'upcoming');t.media.matches=true;t.media.change();assert.equal(t.classes['is-scroll-driven'],false);
assert.equal(setup(600).classes['is-scroll-driven'],false);assert.equal(setup(900,true).classes['is-scroll-driven'],false);
console.log('PASS: CCTV scroll progression, reverse, click synchronization, dimmed future stages and motion fallback');
