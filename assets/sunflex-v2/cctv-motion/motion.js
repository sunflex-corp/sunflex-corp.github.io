(() => {
 'use strict';
 const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
 const preference=matchMedia('(prefers-reduced-motion: reduce)'), desktop=matchMedia('(min-width: 761px)');
 const params=new URLSearchParams(location.search);
 let reduced=preference.matches || params.get('motion')==='off', ctx, lenis, ticker, storyTrigger, activeStep=0, activeModel=0;
 const panels=$$('.story-panel'), tabs=$$('.story-tabs button'), modelButtons=$$('[data-model]');
 function paintStoryProgress(progress){tabs.forEach((t,i)=>$('i',t).style.transform=`scaleX(${Math.max(0,Math.min(1,progress*tabs.length-i))})`);}
 function goTo(target,options={}) { if(lenis)lenis.scrollTo(target,{offset:-98,duration:1.1,...options}); else {const top=typeof target==='number'?target:target.getBoundingClientRect().top+scrollY-98;scrollTo({top,behavior:reduced?'instant':'smooth'});} }
 function syncStep(index){activeStep=index;tabs.forEach((t,i)=>{t.setAttribute('aria-selected',String(i===index));t.tabIndex=i===index?0:-1});panels.forEach((p,i)=>{p.setAttribute('aria-hidden',String(i!==index));p.inert=i!==index;});}
 function selectStep(index){
  index=Math.max(0,Math.min(2,index));
  if(storyTrigger){goTo(storyTrigger.start+(storyTrigger.end-storyTrigger.start)*((index+.5)/3),{offset:0});return;}
  const old=panels[activeStep];syncStep(index);panels.forEach((p,i)=>p.hidden=i!==index);tabs.forEach((t,i)=>$('i',t).style.transform=`scaleX(${i===index?1:0})`);
  if(!reduced&&window.gsap&&old!==panels[index])gsap.fromTo(panels[index],{opacity:0,y:18},{opacity:1,y:0,duration:.55,ease:'power3.out',clearProps:'opacity,transform'});
 }
 tabs.forEach((t,i)=>{t.addEventListener('click',()=>selectStep(i));t.addEventListener('keydown',e=>{let next=i;if(e.key==='ArrowRight')next=(i+1)%3;else if(e.key==='ArrowLeft')next=(i+2)%3;else if(e.key==='Home')next=0;else if(e.key==='End')next=2;else return;e.preventDefault();selectStep(next);tabs[next].focus({preventScroll:true});});});
 function selectModel(index){
  if(index===activeModel)return;const oldImage=$(`[data-model-image="${activeModel}"]`),newImage=$(`[data-model-image="${index}"]`);activeModel=index;
  modelButtons.forEach((b,i)=>{b.setAttribute('aria-selected',String(i===index));b.tabIndex=i===index?0:-1;$(`#model-description-${i}`).hidden=i!==index;});
  $('.model-letter').textContent=['S','M','L'][index];
  if(!reduced&&window.gsap){gsap.killTweensOf($$('.model-pictures img'));oldImage.hidden=true;newImage.hidden=false;gsap.fromTo(newImage,{autoAlpha:0,x:32,scale:.94},{autoAlpha:1,x:0,scale:1,duration:.85,ease:'power3.out',clearProps:'all'});gsap.fromTo($(`#model-description-${index}`),{opacity:0,y:10},{opacity:1,y:0,duration:.5,ease:'power2.out',clearProps:'all'});}
  else{$$('.model-pictures img').forEach((im,i)=>im.hidden=i!==index);}
 }
 modelButtons.forEach((b,i)=>{b.addEventListener('click',()=>selectModel(i));b.addEventListener('keydown',e=>{let next=i;if(['ArrowDown','ArrowRight'].includes(e.key))next=(i+1)%3;else if(['ArrowUp','ArrowLeft'].includes(e.key))next=(i+2)%3;else if(e.key==='Home')next=0;else if(e.key==='End')next=2;else return;e.preventDefault();selectModel(next);modelButtons[next].focus({preventScroll:true});});});
 $$('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{const target=$(a.getAttribute('href'));if(!target)return;e.preventDefault();goTo(target);history.replaceState(null,'',a.getAttribute('href'));if(a.classList.contains('skip')){target.tabIndex=-1;target.focus({preventScroll:true});}}));
 function build(){
  const restore=scrollY;
  const reading=$$('main>section').find(s=>{const r=s.getBoundingClientRect();return r.top<=innerHeight*.45&&r.bottom>innerHeight*.45;});
  const readingOffset=reading?reading.getBoundingClientRect().top:0;
  if(ctx)ctx.revert();if(lenis){lenis.destroy();gsap.ticker.remove(ticker);lenis=null;}storyTrigger=null;
  $('.story-stage').classList.remove('story-stepped','story-measuring');document.documentElement.classList.remove('motion-active');panels.forEach(p=>{p.hidden=false;p.removeAttribute('style')});
  if(!window.gsap||!window.ScrollTrigger){syncStep(activeStep);panels.forEach((p,i)=>p.hidden=i!==activeStep);return;}
  gsap.registerPlugin(ScrollTrigger);
  if(reduced){syncStep(activeStep);panels.forEach((p,i)=>p.hidden=i!==activeStep);tabs.forEach((t,i)=>$('i',t).style.transform=`scaleX(${i===activeStep?1:0})`);if(reading){const target=reading.id==='story'?$('.story-stage'):reading;scrollTo(0,target.getBoundingClientRect().top+scrollY-(reading.id==='story'?100:Math.max(0,readingOffset)));}return;}
  document.documentElement.classList.add('motion-active');
  if(desktop.matches&&window.Lenis){lenis=new Lenis({lerp:.11,smoothWheel:true,syncTouch:false});lenis.on('scroll',ScrollTrigger.update);ticker=t=>lenis.raf(t*1000);gsap.ticker.add(ticker);gsap.ticker.lagSmoothing(0);}
  ctx=gsap.context(()=>{
   gsap.from('.hero .eyebrow',{opacity:0,y:16,duration:.65,delay:.08});
   gsap.from('.hero h1 .line>span',{yPercent:110,duration:1.1,stagger:.12,ease:'power4.out',delay:.15});
   gsap.from('.hero-description,.hero .text-link',{opacity:0,y:22,duration:.85,stagger:.1,ease:'power3.out',delay:.55});
   gsap.from('.hero-product>img',{opacity:0,y:65,rotation:-3,scale:.93,duration:1.35,ease:'power3.out',delay:.15});
   gsap.from('.product-word',{opacity:0,x:30,duration:1.4,ease:'power3.out',delay:.3});
   gsap.to('.page-progress i',{scaleX:1,ease:'none',scrollTrigger:{start:0,end:'max',scrub:true}});
   if(desktop.matches){
    gsap.fromTo('.field-frame',{scale:.9},{scale:1,ease:'none',scrollTrigger:{trigger:'.field',start:'top 95%',end:'top 12%',scrub:.6}});
    gsap.fromTo('.field img',{yPercent:-4,scale:1.07},{yPercent:1,scale:1,ease:'none',scrollTrigger:{trigger:'.field',start:'top bottom',end:'bottom top',scrub:.7}});
   }
   gsap.from('.field-copy>*',{opacity:0,y:35,stagger:.13,duration:1,ease:'power3.out',scrollTrigger:{trigger:'.field-copy',start:'top 85%',once:true}});
   $$('.section-head').forEach(h=>gsap.from(h.children,{opacity:0,y:36,stagger:.1,duration:.9,ease:'power3.out',scrollTrigger:{trigger:h,start:'top 82%',once:true}}));
   const stage=$('.story-stage');
   stage.classList.add('story-measuring');
   const stageHeight=stage.offsetHeight,top=desktop.matches?100:80;
   stage.classList.remove('story-measuring');
   if(stageHeight<=innerHeight-top-16){
    const show=(index,animate=true)=>{
     gsap.killTweensOf(panels);syncStep(index);
     panels.forEach((p,i)=>{p.hidden=false;if(i!==index)gsap.set(p,{autoAlpha:0,y:0});else if(animate)gsap.fromTo(p,{autoAlpha:0,y:14},{autoAlpha:1,y:0,duration:.32,ease:'power3.out',lazy:false});else gsap.set(p,{autoAlpha:1,y:0});});
    };
    show(activeStep,false);stage.classList.add('story-stepped');
    storyTrigger=ScrollTrigger.create({id:'movingcam-story',trigger:stage,start:`top ${top}px`,end:()=>'+='+Math.max(480,innerHeight*.88)*3,pin:true,anticipatePin:1,
     snap:{snapTo:p=>p<.025?0:p>.975?1:(Math.min(2,Math.floor(p*3))+.5)/3,inertia:false,delay:.18,duration:{min:.18,max:.38},ease:'power2.out'},
     onUpdate:self=>{paintStoryProgress(self.progress);const index=Math.min(2,Math.floor(self.progress*3));if(index!==activeStep)show(index);},
     onRefresh:self=>paintStoryProgress(self.progress)
    });
    paintStoryProgress(storyTrigger.progress);
   }else{syncStep(activeStep);panels.forEach((p,i)=>p.hidden=i!==activeStep);tabs.forEach((t,i)=>$('i',t).style.transform=`scaleX(${i===activeStep?1:0})`);}
   gsap.from('.model-display',{opacity:0,y:50,scale:.94,duration:1.1,ease:'power3.out',scrollTrigger:{trigger:'.model-layout',start:'top 83%',once:true}});
   gsap.from('.model-choices',{opacity:0,y:35,duration:.9,ease:'power3.out',scrollTrigger:{trigger:'.model-layout',start:'top 80%',once:true}});
   gsap.from('.configure-inner>.eyebrow,.configure h2',{opacity:0,y:38,stagger:.12,duration:.9,ease:'power3.out',scrollTrigger:{trigger:'.configure',start:'top 76%',once:true}});
   gsap.from('.conditions>div',{opacity:0,y:35,duration:.8,stagger:.12,ease:'power3.out',scrollTrigger:{trigger:'.conditions',start:'top 84%',once:true}});
   gsap.from('.cta',{opacity:0,y:20,duration:.7,ease:'power3.out',scrollTrigger:{trigger:'.cta',start:'top 92%',once:true}});
  });
  ScrollTrigger.refresh();if(restore>0)scrollTo(0,Math.min(restore,document.documentElement.scrollHeight-innerHeight));
 }
 preference.addEventListener('change',e=>{reduced=e.matches;build();});
 let resizeFrame,lastWidth=innerWidth,lastHeight=innerHeight;
 addEventListener('resize',()=>{
  if(innerWidth===lastWidth&&(matchMedia('(pointer:coarse)').matches||innerHeight===lastHeight))return;
  lastWidth=innerWidth;lastHeight=innerHeight;cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(build);
 });
 document.fonts.ready.then(()=>{build();if(location.hash){const target=$(location.hash);if(target)goTo(target,{immediate:true});}});
 window.addEventListener('load',()=>{if(window.ScrollTrigger)ScrollTrigger.refresh();});
})();
