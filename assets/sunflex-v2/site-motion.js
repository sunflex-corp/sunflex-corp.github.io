/* Shared SUNPLEX motion. Content is visible before JS; one owner per animated surface. */
(() => {
 'use strict';
 if(!window.gsap||!window.ScrollTrigger||document.documentElement.dataset.motionEngine!=='gsap')return;
 gsap.registerPlugin(ScrollTrigger);
 const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
 const reduced=matchMedia('(prefers-reduced-motion: reduce)'),desktop=matchMedia('(min-width: 761px)');
 let lenis, ticker;
 const headerOffset=()=>($('.product-local-nav')?.offsetHeight||$('.site-header')?.offsetHeight||66)+16;
 function smoothSetup(){
  if(lenis){lenis.destroy();gsap.ticker.remove(ticker);lenis=null;}
  if(!reduced.matches&&desktop.matches&&window.Lenis&&!$('#inquiry-form')){
   lenis=new Lenis({lerp:.11,smoothWheel:true,syncTouch:false,anchors:false});
   lenis.on('scroll',ScrollTrigger.update);ticker=t=>lenis.raf(t*1000);gsap.ticker.add(ticker);gsap.ticker.lagSmoothing(0);
  }
 }
 function go(top,instant=false){if(lenis)lenis.scrollTo(top,{duration:1.05,immediate:instant});else window.scrollTo({top,behavior:instant||reduced.matches?'instant':'smooth'});}
 smoothSetup();desktop.addEventListener('change',smoothSetup);reduced.addEventListener('change',smoothSetup);
 // Preserve native navigation, modified clicks and form input. Only same-page anchors are enhanced.
 document.addEventListener('click',event=>{
  const link=event.target.closest('a[href^="#"]');if(!link||event.defaultPrevented||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
  let target;try{target=document.getElementById(decodeURIComponent(link.hash.slice(1)));}catch{return;}
  if(!target||target.closest('[data-flow-panel][aria-hidden=true]'))return;
  event.preventDefault();go(target.getBoundingClientRect().top+scrollY-headerOffset());history.pushState(null,'',link.hash);
  if(link.classList.contains('skip-link'))target.focus({preventScroll:true});
 });
 const flows=[];
 $$('[data-scroll-flow]').forEach((track,flowIndex)=>{
  const stage=$('.product-flow-stage',track),controls=$('.product-flow-tabs',track),panels=$$('[data-flow-panel]',track),buttons=controls?$$('button',controls):[];
  if(!stage||panels.length<2||buttons.length!==panels.length)return;
  let selected=0,timeline,pinned=false,top=0,span=0;
  const images=panels.map(p=>$('img',p));
  controls.hidden=false;controls.setAttribute('role','tablist');track.classList.add('flow-enhanced');
  panels.forEach((p,i)=>{p.id||=`motion-flow-${flowIndex}-${i}`;buttons[i].id||=p.id+'-tab';buttons[i].setAttribute('role','tab');buttons[i].setAttribute('aria-controls',p.id);p.setAttribute('role','tabpanel');p.setAttribute('aria-labelledby',buttons[i].id);});
  function select(index){
   if(index!==selected&&panels[selected].contains(document.activeElement))buttons[index].focus({preventScroll:true});
   selected=index;buttons.forEach((b,i)=>{const on=i===index;b.setAttribute('aria-selected',String(on));b.tabIndex=on?0:-1;b.dataset.stepState=on?'current':i<index?'previous':'upcoming';panels[i].inert=!on;panels[i].setAttribute('aria-hidden',String(!on));});
  }
  function seek(index,focus=false){
   if(focus)buttons[index].focus({preventScroll:true});
   if(pinned){go(timeline.scrollTrigger.start+(index+.3)*span/panels.length);return;}
   const previous=selected;select(index);panels.forEach((p,i)=>p.hidden=i!==index);
   if(!reduced.matches&&previous!==index){gsap.killTweensOf(panels);gsap.fromTo(panels[index],{opacity:0,y:20},{opacity:1,y:0,duration:.55,ease:'power3.out',clearProps:'opacity,transform'});}
   ScrollTrigger.refresh();
  }
  buttons.forEach((b,i)=>{b.addEventListener('click',()=>seek(i));b.addEventListener('keydown',e=>{const next={ArrowRight:(i+1)%panels.length,ArrowLeft:(i+panels.length-1)%panels.length,Home:0,End:panels.length-1}[e.key];if(next===undefined)return;e.preventDefault();seek(next,true);});});
  function configure(){
   timeline?.scrollTrigger?.kill();timeline?.kill();timeline=null;
   gsap.killTweensOf(panels);gsap.set(panels,{clearProps:'opacity,visibility,transform,--flow-shift,--flow-copy-alpha'});
   images.filter(Boolean).forEach(im=>gsap.set(im,{clearProps:'transform'}));
   panels.forEach(p=>p.hidden=false);track.classList.remove('flow-pinned','flow-tabbed','flow-reading');
   top=headerOffset();const view=innerHeight,available=view-top-24;
   track.style.setProperty('--flow-view',view+'px');track.style.setProperty('--flow-available',Math.max(180,available)+'px');
   track.classList.add('flow-measuring');const panelHeight=Math.max(...panels.map(p=>p.offsetHeight)),height=panelHeight+controls.offsetHeight+24;track.classList.remove('flow-measuring');
   pinned=desktop.matches&&!reduced.matches&&height<=available;
   track.classList.add(pinned?'flow-pinned':'flow-tabbed');track.dataset.flowMode=pinned?'pinned':'tabbed';
   track.style.setProperty('--flow-top',top+'px');track.style.setProperty('--flow-stage-height',height+'px');
   if(!pinned){select(selected);panels.forEach((p,i)=>p.hidden=i!==selected);return;}
   span=Math.max(480,view*.88)*panels.length;track.style.setProperty('--flow-span',span+'px');
   gsap.set(panels,{autoAlpha:0,'--flow-shift':'0px'});gsap.set(panels[0],{autoAlpha:1});select(0);
   // CSS owns the stable sticky frame; ScrollTrigger owns only its child timeline.
   timeline=gsap.timeline({scrollTrigger:{trigger:track,start:()=>`top ${top}px`,end:()=>'+='+span,scrub:.6,invalidateOnRefresh:true},onUpdate(){const i=Math.min(panels.length-1,Math.floor(this.time()+.04));if(i!==selected)select(i);}});
   panels.forEach((panel,i)=>{
    if(i){timeline.to(panels[i-1],{autoAlpha:0,'--flow-shift':'-14px',duration:.22,ease:'power2.in'},i-.18);timeline.fromTo(panel,{autoAlpha:0,'--flow-shift':'24px'},{autoAlpha:1,'--flow-shift':'0px',duration:.32,ease:'power3.out'},i-.03);}
    if(images[i])timeline.fromTo(images[i],{scale:1.035},{scale:1,duration:1,ease:'none'},i);
    timeline.to(track,{'--flow-progress':(i+1)/panels.length,duration:1,ease:'none'},i);
   });
  }
  flows.push({configure,track});configure();
 });
 // Reveal leaves, never sticky ancestors. Form fields, tables and filtered cards remain immediate.
 const mm=gsap.matchMedia();
 mm.add('(prefers-reduced-motion: no-preference)',()=>{
  const reveal=(nodes,trigger,duration=.8)=>{if(!nodes.length)return;return gsap.from(nodes,{opacity:0,y:28,duration,stagger:.09,ease:'power3.out',clearProps:'opacity,transform',scrollTrigger:{trigger,start:'top 90%',once:true}});};
  const hero=$('.editorial-hero-copy,.page-head .wrap,.simple-hero .hero-copy,.solar-category-hero .category-intro');
  if(hero){gsap.from(hero.children,{opacity:0,y:30,duration:.95,stagger:.12,ease:'power3.out',clearProps:'opacity,transform'});}
  const heroImage=$('.editorial-hero-media');if(heroImage)gsap.from(heroImage,{opacity:0,y:42,scale:.965,duration:1.15,ease:'power3.out',clearProps:'opacity,transform'});
  const headings=$$('main h2').filter(n=>!n.closest('[data-scroll-flow],.solar-story,.home-families,.editorial-hero,.page-head,[hidden]'));
  headings.forEach(h=>reveal([h],h));
  $$('.company-intro,.contact-info,.home-contact,.final-cta,.support-choice,.principle,.inquiry-steps').forEach(n=>{
   const leaves=[...n.children].filter(c=>!c.matches('h2,form')&&!c.querySelector('h2,form'));reveal(leaves,n,$('#inquiry-form') ? .55 : .8);
  });
  $$('.chapter-media figure,.revision-source figure,.company-photo,.feature-media,.solar-category-hero .category-backdrop').filter(n=>!n.closest('[data-scroll-flow],[data-model-panel],.bodycam-use')).forEach(n=>{
   const image=$('img',n);if(!image)return;
   reveal([image],n,.95);
  });
  if(desktop.matches){
   $$('.company-photo,.revision-source [data-composition="panorama"]>figure,.revision-source [data-composition="editorial"]>figure').forEach(n=>{const im=$('img',n);if(!im)return;gsap.fromTo(im,{scale:1.04},{scale:1,ease:'none',scrollTrigger:{trigger:n,start:'top bottom',end:'bottom top',scrub:.65}});});
  }
  // Existing tab controllers own semantics; motion responds after their selection settles.
  const onTabs=e=>{
   const button=e.target.closest('[role=tab]');if(!button||button.closest('[data-scroll-flow]'))return;
   const panel=document.getElementById(button.getAttribute('aria-controls'));if(!panel||panel.hidden)return;
   gsap.killTweensOf(panel);gsap.fromTo(panel,{opacity:.2,y:18},{opacity:1,y:0,duration:.55,ease:'power3.out',clearProps:'opacity,transform'});ScrollTrigger.refresh();
  };
  document.addEventListener('click',onTabs);return()=>document.removeEventListener('click',onTabs);
 });
 // Enlarged text and shorter viewports fall back to normal-height tabs instead of clipped pinning.
 let resizeFrame,lastWidth=innerWidth,lastHeight=innerHeight;
 const rebuild=()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>{flows.forEach(f=>f.configure());ScrollTrigger.refresh();});};
 addEventListener('resize',()=>{if(innerWidth!==lastWidth||(!matchMedia('(pointer:coarse)').matches&&innerHeight!==lastHeight)){lastWidth=innerWidth;lastHeight=innerHeight;rebuild();}});
 reduced.addEventListener('change',rebuild);
 document.fonts?.ready.then(rebuild);addEventListener('load',rebuild);
 // Expanding disclosure panels or changing catalogue filters changes subsequent trigger positions.
 document.addEventListener('toggle',()=>ScrollTrigger.refresh(),true);
 document.addEventListener('input',e=>{if(e.target.closest('.catalog-tools'))ScrollTrigger.refresh();});
 document.addEventListener('click',e=>{if(e.target.closest('.catalog-tools'))ScrollTrigger.refresh();});
 document.documentElement.dataset.motionReady='true';
})();
