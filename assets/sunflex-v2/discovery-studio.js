/* Page-specific polish; solar-site.js remains the single filter state owner. */
(()=>{
 'use strict';
 const root=document.querySelector('.discovery-hero');if(!root)return;
 const search=document.querySelector('#support-search'),empty=document.querySelector('.discovery-faq-empty');
 if(search&&empty){
  search.addEventListener('input',()=>{empty.hidden=[...document.querySelectorAll('.faq details')].some(d=>!d.hidden);});
  document.querySelector('[data-support-reset]')?.addEventListener('click',()=>{search.value='';search.dispatchEvent(new Event('input',{bubbles:true}));search.focus();});
 }
 if(!window.gsap)return;
 gsap.matchMedia().add('(prefers-reduced-motion:no-preference)',()=>{
  gsap.from(root.querySelector('h1'),{y:12,duration:.45,ease:'power3.out',clearProps:'transform'});
  const products=root.querySelectorAll('.discovery-stage-product img');
  if(products.length)gsap.from(products,{y:12,duration:.45,stagger:.04,ease:'power3.out',clearProps:'transform'});
 });
 if(window.ScrollTrigger){
  gsap.registerPlugin(ScrollTrigger);
  gsap.matchMedia().add('(min-width:761px) and (prefers-reduced-motion:no-preference)',()=>{
   const exhibit=root.querySelector('.discovery-exhibit');
   if(exhibit)gsap.to(exhibit,{'--orbit-angle':'8deg',ease:'none',scrollTrigger:{trigger:root,start:'top top',end:'bottom top',scrub:.4}});
   const marks=root.querySelectorAll('.discovery-support-route .discovery-symbol');
   if(marks.length)gsap.from(marks,{rotation:-12,scale:.85,duration:.7,stagger:.08,ease:'power3.out',clearProps:'transform'});
  });
 }
})();
