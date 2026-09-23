/* One owner for scroll position, scene blending, tab state and sticky geometry. */
(() => {
 'use strict';
 const clamp=(n,a=0,b=1)=>Math.min(b,Math.max(a,n));
 function sceneAt(progress,count){
  const p=clamp(progress,0,count),index=Math.min(count-1,Math.floor(p));
  const t=index===count-1?0:clamp((p-index-.65)/.35);
  const blend=t*t*(3-2*t);
  return {index,blend,selected:index+(blend>=.5?1:0)};
 }
 if(typeof module!=='undefined')module.exports={sceneAt};
 if(typeof document==='undefined')return;
 if(document.documentElement?.dataset.motionEngine==='gsap'&&window.gsap&&window.ScrollTrigger)return;
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 document.querySelectorAll('[data-scroll-flow]').forEach((track,flowIndex)=>{
  const stage=track.querySelector('.product-flow-stage'),controls=track.querySelector('.product-flow-tabs');
  if(!stage||!controls)return;
  const buttons=[...controls.querySelectorAll('button')],panels=[...track.querySelectorAll('[data-flow-panel]')];
  if(buttons.length<2||buttons.length!==panels.length)return;
  let selected=-1,enabled=false,span=0,top=12,frame=0,measureFrame=0,inView=true,lastWidth=0,lastHeight=0;
  const poses=new Map();
  panels.forEach((panel,i)=>{
   panel.id ||= `product-flow-${flowIndex}-${i}`;
   buttons[i].id ||= `${panel.id}-tab`;
   buttons[i].setAttribute('role','tab');buttons[i].setAttribute('aria-controls',panel.id);
   panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby',buttons[i].id);
   panel.hidden=false;
  });
  controls.setAttribute('role','tablist');controls.hidden=false;track.classList.add('flow-enhanced');
  function select(index,focus=false){
   index=clamp(index,0,panels.length-1);
   if(index!==selected){
    selected=index;
    buttons.forEach((button,i)=>{
     const active=i===index;
     button.setAttribute('data-step-state',active?'current':i<index?'previous':'upcoming');
     button.setAttribute('aria-selected',String(active));button.tabIndex=active?0:-1;
     panels[i].inert=enabled&&!active;
     panels[i].setAttribute('aria-hidden',String(enabled&&!active));
    });
   }
   if(focus)buttons[index].focus({preventScroll:true});
  }
  function paint(progress){
   const state=sceneAt(progress,panels.length);select(state.selected);
   panels.forEach((panel,i)=>{
    let alpha=i===state.index?1-state.blend:i===state.index+1?state.blend:0;
    if(reduced.matches)alpha=i===state.selected?1:0;
    const shift=reduced.matches?0:12*(i-state.index-state.blend);
    const key=`${alpha.toFixed(4)}:${shift.toFixed(2)}`;
    if(poses.get(panel)===key)return;poses.set(panel,key);
    panel.style.opacity=String(alpha);
    panel.style.setProperty('--flow-copy-alpha',String(Math.max(0,2*alpha-1)));
    panel.style.visibility=alpha>0?'visible':'hidden';
    panel.style.setProperty('--flow-shift',`${shift.toFixed(2)}px`);
   });
   track.style.setProperty('--flow-progress',String(clamp(progress/panels.length)));
  }
  function draw(){
   frame=0;if(!inView||document.hidden)return;
   if(enabled){paint((top-track.getBoundingClientRect().top)/(span/panels.length));return;}
   // Enlarged text/very short landscape screens retain sticky numbered navigation.
   const target=top+controls.offsetHeight+32;
   let closest=0,delta=Infinity;
   panels.forEach((panel,i)=>{const distance=Math.abs(panel.getBoundingClientRect().top-target);if(distance<delta){delta=distance;closest=i;}});
   select(closest);
  }
  function schedule(){if(inView&&!frame&&!document.hidden)frame=requestAnimationFrame(draw);}
  function seek(index,focus=false){
   index=clamp(index,0,panels.length-1);
   if(focus)buttons[index].focus({preventScroll:true});
   const destination=enabled
    ?window.scrollY+track.getBoundingClientRect().top-top+(index+.25)*span/panels.length
    :window.scrollY+panels[index].getBoundingClientRect().top-top-controls.offsetHeight-16;
   window.scrollTo({top:Math.max(0,destination),behavior:reduced.matches?'instant':'smooth'});
  }
  buttons.forEach((button,i)=>{
   button.addEventListener('click',()=>seek(i));
   button.addEventListener('keydown',event=>{
    const next={ArrowRight:(i+1)%panels.length,ArrowLeft:(i+panels.length-1)%panels.length,Home:0,End:panels.length-1}[event.key];
    if(next===undefined)return;event.preventDefault();seek(next,true);
   });
  });
  function configure(){
   measureFrame=0;
   const nav=document.querySelector('.product-local-nav');
   top=(nav?.offsetHeight||66)+12;
   // svh does not oscillate when mobile browser chrome collapses while scrolling.
   const probe=document.createElement('div');probe.style.cssText='position:fixed;height:100svh;visibility:hidden;pointer-events:none';
   document.body.append(probe);const view=probe.offsetHeight||window.innerHeight;probe.remove();
   const available=Math.max(180,view-top-24);
   track.style.setProperty('--flow-top',top+'px');track.style.setProperty('--flow-view',view+'px');
   track.style.setProperty('--flow-available',available+'px');
   track.classList.add('flow-measuring');
   const panelHeight=Math.max(...panels.map(panel=>panel.offsetHeight));
   const controlsHeight=controls.offsetHeight;
   enabled=panelHeight+controlsHeight+16<=available;
   track.classList.remove('flow-measuring');
   track.classList.toggle('flow-pinned',enabled);track.classList.toggle('flow-reading',!enabled);
   track.dataset.flowMode=enabled?'pinned':'reading';
   const stageHeight=panelHeight+controlsHeight+16;
   if(enabled){top+=Math.max(0,Math.floor((view-top-stageHeight-16)/2));track.style.setProperty('--flow-top',top+'px');}
   const visual=track.querySelector('.benefit-visual,.flow-with-image,.pedestrian-scene');
   span=Math.max(380,view*(visual ? .82 : .55))*panels.length;
   track.style.setProperty('--flow-stage-height',stageHeight+'px');track.style.setProperty('--flow-span',span+'px');
   poses.clear();selected=-1;
   if(!enabled)panels.forEach(panel=>{panel.style.removeProperty('opacity');panel.style.removeProperty('visibility');panel.style.removeProperty('--flow-shift');panel.inert=false;panel.setAttribute('aria-hidden','false');});
   draw();
  }
  function measure(){if(!measureFrame)measureFrame=requestAnimationFrame(configure);}
  window.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('resize',()=>{
   // Ignore toolbar-only height changes on touch screens; CSS svh remains stable.
   const width=window.innerWidth,height=window.innerHeight;
   if(width!==lastWidth||!window.matchMedia('(pointer:coarse)').matches&&height!==lastHeight)measure();
   lastWidth=width;lastHeight=height;
  });
  reduced.addEventListener('change',()=>{poses.clear();schedule();});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&frame){cancelAnimationFrame(frame);frame=0;}else schedule();});
  // Reserved media dimensions make image decoding independent from stage geometry.
  if(typeof IntersectionObserver!=='undefined')new IntersectionObserver(entries=>{
   inView=entries.some(entry=>entry.isIntersecting);if(inView)schedule();
  },{rootMargin:'200px 0px'}).observe(track);
  if(document.fonts)document.fonts.ready.then(measure);
  configure();
 });
})();
