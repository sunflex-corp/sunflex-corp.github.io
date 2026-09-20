(() => {
 'use strict';
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 document.querySelectorAll('[data-scroll-flow]').forEach(track=>{
  const stage=track.querySelector('.product-flow-stage'),controls=track.querySelector('.product-flow-tabs');
  if(!stage||!controls)return;
  const buttons=[...controls.querySelectorAll('button')],panels=[...track.querySelectorAll('[data-flow-panel]')];
  if(!buttons.length||buttons.length!==panels.length)return;
  let selected=0,enabled=false,span=0,top=12,raf=0,inView=true;
  panels.forEach((panel,index)=>{
   const button=buttons[index];
   if(!panel.id)panel.id=`flow-panel-${index}`;
   button.setAttribute('role','tab');button.setAttribute('aria-controls',panel.id);
   panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby',button.id);
  });
  controls.setAttribute('role','tablist');
  function update(index,focus=false){
   selected=Math.max(0,Math.min(panels.length-1,index));
   buttons.forEach((button,i)=>{
    const current=i===selected;
    button.setAttribute('data-step-state',current?'current':i<selected?'previous':'upcoming');
    button.setAttribute('aria-selected',String(current));button.tabIndex=current?0:-1;
    // A static flow leaves every scene readable in document order.
    panels[i].hidden=enabled&&!current;
   });
   const button=buttons[selected];
   if(controls.scrollTo)controls.scrollTo({left:Math.max(0,button.offsetLeft-controls.offsetLeft-(controls.clientWidth-button.offsetWidth)/2),behavior:'instant'});
   if(focus)button.focus();
  }
  function draw(){
   raf=0;if(!inView)return;
   if(enabled){
    const distance=top-track.getBoundingClientRect().top;
    update(Math.floor(distance/(span/panels.length)));return;
   }
   // In the static fallback, reflect the scene nearest the readable viewport.
   const target=top+Math.max(48,(window.innerHeight-top)/2);let closest=0,delta=Infinity;
   panels.forEach((panel,index)=>{
    const rect=panel.getBoundingClientRect(),distance=Math.abs((rect.top+rect.bottom)/2-target);
    if(distance<delta){delta=distance;closest=index;}
   });
   update(closest);
  }
  function schedule(){if(inView&&!raf)raf=requestAnimationFrame(draw);}
  function seek(index,focus=false){
   update(index,focus);const rect=panels[selected].getBoundingClientRect();
   if(enabled){
    const start=window.scrollY+track.getBoundingClientRect().top-top;
    window.scrollTo({top:start+(selected+.2)*span/panels.length,behavior:'instant'});
   }else window.scrollTo({top:Math.max(0,window.scrollY+rect.top-top-12),behavior:'instant'});
  }
  buttons.forEach((button,index)=>{
   button.addEventListener('click',()=>seek(index));
   button.addEventListener('keydown',event=>{
    const next={ArrowRight:(index+1)%panels.length,ArrowLeft:(index+panels.length-1)%panels.length,Home:0,End:panels.length-1}[event.key];
    if(next===undefined)return;event.preventDefault();seek(next,true);
   });
  });
  function localNavOffset(){
   const nav=document.querySelector('.product-local-nav');if(!nav)return 12;
   const rect=nav.getBoundingClientRect();
   // The local navigation is sticky. Its height is the safe edge after the main header scrolls away.
   return Math.max(12,Math.ceil(rect.height)+12);
  }
  function configure(){
   top=localNavOffset();track.style.setProperty('--flow-top',top+'px');track.style.setProperty('--flow-view',window.innerHeight+'px');
   // Measure the unhidden, real content before deciding whether it can safely pin.
   stage.style.setProperty('--flow-panel-height','0px');panels.forEach(panel=>{panel.hidden=false;});
   const panelHeight=Math.max(...panels.map(panel=>panel.getBoundingClientRect().height));
   const controlsHeight=controls.getBoundingClientRect().height;
   const fits=top+controlsHeight+panelHeight+48<=window.innerHeight;
   enabled=!reduced.matches&&(!window.innerWidth||window.innerWidth>760)&&window.innerHeight>=720&&fits;
   if(enabled){
    top+=Math.max(0,Math.floor((window.innerHeight-(top+controlsHeight+panelHeight+48))/2));
    track.style.setProperty('--flow-top',top+'px');stage.style.setProperty('--flow-panel-height',panelHeight+'px');
   }
   span=Math.max(window.innerHeight*.78,panelHeight*.65)*panels.length;
   track.style.setProperty('--flow-span',span+'px');track.classList.toggle('flow-pinned',enabled);update(selected);schedule();
  }
  controls.hidden=false;track.classList.add('flow-enhanced');
  window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',configure);reduced.addEventListener('change',configure);
  track.querySelectorAll('img').forEach(image=>image.addEventListener('load',configure,{once:true}));
  if(typeof IntersectionObserver!=='undefined'){
   const observer=new IntersectionObserver(entries=>{inView=entries.some(entry=>entry.isIntersecting);if(inView)schedule();},{rootMargin:'240px 0px'});
   observer.observe(track);
  }
  if(document.fonts)document.fonts.ready.then(configure);
  configure();
 });
})();
