/* One company-specific motion owner; all facts and links work before enhancement. */
(()=>{
 'use strict';
 const root=document.querySelector('[data-company-owned]');
 if(!root||!window.gsap||!window.ScrollTrigger)return;
 gsap.registerPlugin(ScrollTrigger);
 const stories=[...root.querySelectorAll('[data-company-field]')];
 const images=[...root.querySelectorAll('[data-company-image]')];
 const links=[...root.querySelectorAll('.company-field-nav a')];
 const mm=gsap.matchMedia();
 mm.add({wide:'(min-width:1001px) and (min-height:600px) and (prefers-reduced-motion:no-preference)',motion:'(prefers-reduced-motion:no-preference)'},context=>{
  const {wide,motion}=context.conditions;
  if(wide)document.body.classList.add('company-motion-wide');
  const select=i=>{images.forEach((im,j)=>im.style.opacity=i===j?'1':'0');links.forEach((a,j)=>{if(i===j)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});};
  select(0);
  stories.forEach((story,i)=>{
   ScrollTrigger.create({trigger:story,start:'top 35%',end:'bottom 35%',onEnter:()=>select(i),onEnterBack:()=>select(i)});
  });
  if(motion){
   gsap.from(root.querySelector('.company-hero h1'),{y:24,duration:.7,ease:'power3.out',clearProps:'opacity,transform'});
   gsap.fromTo(root.querySelector('.company-hero-photo img'),{scale:1.05},{scale:1,duration:1.6,ease:'power3.out',clearProps:'transform'});
   if(wide)gsap.fromTo(root.querySelector('.company-field-stage'),{clipPath:'inset(0 15% 0 15%)'},{clipPath:'inset(0 0% 0 0%)',ease:'none',scrollTrigger:{trigger:'.company-field-layout',start:'top 90%',end:'top 30%',scrub:.35}});
   root.querySelectorAll('.company-principle,.company-information .row-link').forEach(el=>gsap.from(el,{y:24,duration:.7,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 90%',once:true},clearProps:'transform'}));
  }
  return()=>{document.body.classList.remove('company-motion-wide');images.forEach(im=>im.style.removeProperty('opacity'));links.forEach(a=>a.removeAttribute('aria-current'));};
 });
 document.fonts?.ready.then(()=>ScrollTrigger.refresh());
})();
