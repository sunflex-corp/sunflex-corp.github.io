/* Explicit controls own scene state. GSAP adds presentation without hiding source content. */
(()=>{
 'use strict';
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 document.querySelectorAll('[data-studio-scene]').forEach(root=>{
  const controls=root.querySelector('.studio-tabs');
  const buttons=[...controls.querySelectorAll('button')];
  const panels=[...root.querySelectorAll('.studio-panel')];
  const comparison=root.dataset.studioScene==='compare';
  if(!buttons.length||buttons.length!==panels.length)return;
  const select=(index,focus=false)=>{
   buttons.forEach((button,i)=>{
    button.setAttribute(comparison?'aria-pressed':'aria-selected',String(index===i));
    button.tabIndex=comparison?0:(index===i?0:-1);
    panels[i].hidden=!comparison&&index!==i;
    panels[i].classList.toggle('is-selected',index===i);
    if(!comparison){panels[i].role='tabpanel';panels[i].setAttribute('aria-labelledby',button.id);panels[i].tabIndex=0;}
   });
   root.dataset.active=String(index);
   if(focus)buttons[index].focus();
   // Shared motion already owns panel entrances; this layer owns only its image frame.
   const image=panels[index].querySelector('.benefit-visual img');
   if(image&&window.gsap&&!reduced.matches)gsap.fromTo(image,{scale:1.035},{scale:1,duration:.65,ease:'power3.out',overwrite:true,clearProps:'transform'});
   window.ScrollTrigger?.refresh();
  };
  buttons.forEach((button,index)=>{
   button.addEventListener('click',()=>select(index));
   button.addEventListener('keydown',event=>{
    const next={ArrowRight:(index+1)%buttons.length,ArrowLeft:(index+buttons.length-1)%buttons.length,Home:0,End:buttons.length-1}[event.key];
    if(next===undefined)return;event.preventDefault();select(next,true);
   });
  });
  controls.hidden=false;root.classList.add('is-enhanced');select(0);
  const hash=()=>{const index=panels.findIndex(p=>'#'+p.id===location.hash);if(index>=0)select(index);};
  hash();addEventListener('hashchange',hash);
 });
 if(!window.gsap||!window.ScrollTrigger)return;
 const mm=gsap.matchMedia();
 mm.add('(prefers-reduced-motion: no-preference)',()=>{
  const copy=document.querySelector('.studio-hero-copy');
  if(copy)gsap.from(copy.children,{y:24,opacity:0,stagger:.08,duration:.8,ease:'power3.out',clearProps:'opacity,transform'});
  const media=document.querySelector('.studio-hero-media');
  if(media){
   gsap.from(media,{y:30,opacity:0,duration:1,ease:'power3.out',clearProps:'opacity,transform'});
   gsap.from(media.querySelectorAll('.studio-viewfinder i'),{scale:.2,opacity:0,stagger:.08,duration:.9,ease:'power3.out',clearProps:'opacity,transform'});
  }
 });
})();
