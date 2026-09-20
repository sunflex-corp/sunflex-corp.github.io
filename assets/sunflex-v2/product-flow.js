(() => {
 'use strict';
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 document.querySelectorAll('[data-scroll-flow]').forEach(track=>{
  const stage=track.querySelector('.product-flow-stage'),controls=track.querySelector('.product-flow-tabs');
  const buttons=[...controls.querySelectorAll('button')],panels=[...track.querySelectorAll('[data-flow-panel]')];
  let selected=-1,enabled=false,span=0,top=80,raf=0;
  function select(index,focus=false){
   if(selected!==index){selected=index;buttons.forEach((b,i)=>{b.setAttribute('data-step-state',i===index?'current':i<index?'previous':'upcoming');b.setAttribute('aria-selected',String(i===index));b.tabIndex=i===index?0:-1;panels[i].hidden=i!==index;panels[i].setAttribute('role','tabpanel');panels[i].setAttribute('aria-labelledby',b.id);});}
   if(controls.scrollTo){const b=buttons[index];controls.scrollTo({left:Math.max(0,b.offsetLeft-controls.offsetLeft-(controls.clientWidth-b.offsetWidth)/2),behavior:'instant'});}
   if(focus)buttons[index].focus();
  }
  function draw(){raf=0;if(!enabled)return;const distance=top-track.getBoundingClientRect().top;select(Math.max(0,Math.min(panels.length-1,Math.floor(distance/(span/panels.length)))));}
  function schedule(){if(enabled&&!raf)raf=requestAnimationFrame(draw);}
  function seek(index,focus=false){select(index,focus);if(enabled){const start=window.scrollY+track.getBoundingClientRect().top-top;window.scrollTo({top:start+(index+.2)*span/panels.length,behavior:'instant'});}}
  buttons.forEach((b,i)=>{b.addEventListener('click',()=>seek(i));b.addEventListener('keydown',event=>{
   const next={ArrowRight:(i+1)%panels.length,ArrowLeft:(i+panels.length-1)%panels.length,Home:0,End:panels.length-1}[event.key];
   if(next===undefined)return;event.preventDefault();seek(next,true);
  });});
  controls.hidden=false;track.classList.add('flow-enhanced');select(0);
  function configure(){
   const nav=document.querySelector('.product-local-nav');top=(nav?nav.getBoundingClientRect().height:64)+12;
   track.style.setProperty('--flow-top',top+'px');track.style.setProperty('--flow-view',window.innerHeight+'px');
   // Measure every panel so long prose, zoom and narrow screens never get trapped in a pin.
   stage.style.setProperty('--flow-panel-height','0px');
   let max=0;
   panels.forEach((p,i)=>{p.hidden=false;max=Math.max(max,p.getBoundingClientRect().height);p.hidden=i!==selected;});
   stage.style.setProperty('--flow-panel-height',max+'px');
   enabled=!reduced.matches&&window.innerHeight>=680&&max+controls.getBoundingClientRect().height+top+48<window.innerHeight;
   if(enabled){top+=Math.max(0,(window.innerHeight-top-max-controls.getBoundingClientRect().height-48)/2);track.style.setProperty('--flow-top',top+'px');}
   span=window.innerHeight*.8*panels.length;
   track.style.setProperty('--flow-span',span+'px');track.classList.toggle('flow-pinned',enabled);schedule();
  }
  window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',configure);reduced.addEventListener('change',configure);
  track.querySelectorAll('img').forEach(image=>image.addEventListener('load',configure));
  // Warm the adjacent benefit scenes before the pinned story enters view.
  if(typeof IntersectionObserver!=='undefined'&&track.closest?.('.benefit-chapter')){
   const preload=new IntersectionObserver(entries=>{
    if(entries.some(entry=>entry.isIntersecting)){
     track.querySelectorAll('img').forEach(image=>{image.loading='eager';});
     preload.disconnect();
    }
   },{rootMargin:'600px 0px'});
   preload.observe(track);
  }
  if(document.fonts)document.fonts.ready.then(configure);
  configure();
 });
})();
