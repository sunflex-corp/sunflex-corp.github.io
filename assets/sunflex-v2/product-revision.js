(() => {
 'use strict';
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 function reveal(hash,animate=false){
  if(!hash||hash==='#')return;
  let target;try{target=document.getElementById(decodeURIComponent(hash.slice(1)));}catch{return;}
  if(!target)return;
  // A deep link into a story uses the same controller as its numbered tabs.
  const flowPanel=target.closest('[data-flow-panel]');
  if(flowPanel){document.querySelector(`[aria-controls="${flowPanel.id}"]`)?.click();return;}
  const panel=target.closest('[data-model-panel],[data-use-panel]');
  if(panel?.hidden)document.querySelector(`[aria-controls="${panel.id}"]`)?.click();
  const nav=document.querySelector('.product-local-nav');
  const top=window.scrollY+target.getBoundingClientRect().top-(nav?.offsetHeight||66)-24;
  window.scrollTo({top:Math.max(0,top),behavior:animate&&!reduced.matches?'smooth':'instant'});
  if(target.hasAttribute('tabindex'))target.focus({preventScroll:true});
 }
 document.addEventListener('click',event=>{
  const link=event.target.closest('a[href^="#"]');
  if(!link||event.defaultPrevented||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
  if(!link.hash||link.hash==='#')return;
  event.preventDefault();history.pushState(null,'',link.hash);reveal(link.hash,true);
 });
 window.addEventListener('hashchange',()=>reveal(location.hash));
 if(location.hash)(document.fonts?.ready||Promise.resolve()).then(()=>requestAnimationFrame(()=>reveal(location.hash)));
 // Reserve the tallest tab panel before switching, avoiding page-height jumps.
 document.querySelectorAll('[data-model-selector],.bodycam-use').forEach(root=>{
  const host=root.querySelector('.model-panels,.use-panels');if(!host)return;
  let pending=0;
  function measure(){pending=0;host.style.minHeight='';if(root.classList.contains('models-comparing'))return;
   root.classList.add('tabs-measuring');
   const height=Math.max(...[...host.children].map(panel=>panel.offsetHeight));
   root.classList.remove('tabs-measuring');host.style.minHeight=height+'px';
  }
  const schedule=()=>{if(!pending)pending=requestAnimationFrame(measure);};
  root.addEventListener('click',schedule);window.addEventListener('resize',schedule);document.fonts?.ready.then(schedule);schedule();
 });
})();
