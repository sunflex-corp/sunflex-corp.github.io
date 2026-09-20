/* Product motion: bounded scene transitions, reversible image depth, no scroll hijacking. */
(() => {
 'use strict';
 const clamp=n=>Math.min(1,Math.max(0,n));
 function plan(kind,direction=1){
  if(['wear','hook'].includes(kind))return {from:`translateY(28px) scale(.88) rotate(${direction*3}deg)`,duration:780};
  if(['dashboard','document','translation','timeline'].includes(kind))return {from:`translateY(36px) scale(.94)`,duration:720};
  if(['network','broadcast','signal','chart'].includes(kind))return {from:`translateX(${direction*32}px) scale(.96)`,duration:640};
  return {from:`translateX(${direction*48}px) scale(1.045)`,duration:820};
 }
 function pose(progress,mobile){const p=clamp(progress);return {scale:1.065-p*.065,y:(.5-p)*(mobile?12:36)};}
 if(typeof module!=='undefined')module.exports={plan,pose};
 if(typeof document==='undefined')return;
 const root=document.querySelector('[data-motion-profile]');
 if(!root||typeof IntersectionObserver==='undefined'||!Element.prototype.animate)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)'),mobile=matchMedia('(max-width:760px)');
 const kind=root.dataset.motionProfile,live=new Set(),running=new Set(),owned=new WeakMap();let frame=0;
 function play(node,frames,options){
  if(!node||reduced.matches||document.hidden)return;
  owned.get(node)?.cancel();
  const animation=node.animate(frames,{duration:700,easing:'cubic-bezier(.16,1,.3,1)',...options});
  owned.set(node,animation);running.add(animation);
  const release=()=>{running.delete(animation);if(owned.get(node)===animation)owned.delete(node);};
  animation.onfinish=release;animation.oncancel=release;
 }
 function enter(panel,direction=1){
  if(reduced.matches)return;
  const p=plan(kind,direction),visual=panel.querySelector('.benefit-visual,.pedestrian-scene,figure'),copy=panel.querySelector('.benefit-copy,.pedestrian-story-copy');
  play(visual,[{opacity:.35,transform:p.from},{opacity:1,transform:'none'}],{duration:p.duration});
  if(copy)[...copy.children].forEach((node,i)=>play(node,[{opacity:.25,transform:'translateY(18px)'},{opacity:1,transform:'none'}],{duration:540,delay:i*65}));
  // Small signal graphics have a finite pulse; nothing loops after the scene settles.
  if(['network','broadcast','signal','chart','opening'].includes(kind)){
   [...panel.querySelectorAll('svg > circle,svg > path')].slice(-4).forEach((node,i)=>play(node,[{opacity:.3},{opacity:1},{opacity:.55},{opacity:1}],{duration:950,delay:i*90}));
  }
 }
 root.querySelectorAll('[data-scroll-flow]').forEach(track=>{
  const panels=[...track.querySelectorAll('[data-flow-panel]')],tabs=[...track.querySelectorAll('[role=tab]')];let last=-1;
  const progress=document.createElement('div');progress.className='product-motion-progress';progress.setAttribute('aria-hidden','true');
  const fill=document.createElement('span');progress.append(fill);track.querySelector('.product-flow-tabs')?.after(progress);
  function changed(){
   const current=tabs.findIndex(tab=>tab.getAttribute('aria-selected')==='true');
   fill.style.transform=`scaleX(${(current+1)/panels.length})`;
   if(current===last||current<0)return;const direction=current<last?-1:1;last=current;
   if(!track.classList.contains('flow-pinned'))return;
   const rect=track.getBoundingClientRect();if(rect.bottom>0&&rect.top<innerHeight)enter(panels[current],direction);
  }
  new MutationObserver(changed).observe(track,{subtree:true,attributes:true,attributeFilter:['aria-selected','hidden']});changed();
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{
   if(entry.isIntersecting&&!track.classList.contains('flow-pinned')){enter(entry.target);observer.unobserve(entry.target);}
  }),{threshold:.18});panels.forEach(panel=>observer.observe(panel));
 });
 // Editorial imagery progresses with the real scroll position and rewinds naturally.
 const pictures=[...root.querySelectorAll('[data-composition] > figure, .revision-proof a')];
 function draw(){frame=0;if(reduced.matches||document.hidden)return;
  const updates=[...live].map(node=>{const r=node.getBoundingClientRect();return [node,pose((innerHeight-r.top)/(innerHeight+r.height),mobile.matches)];});
  updates.forEach(([node,p])=>{const image=node.querySelector('img');if(image)image.style.transform=`translateY(${p.y.toFixed(2)}px) scale(${p.scale.toFixed(4)})`;});
 }
 function schedule(){if(!frame&&live.size&&!reduced.matches&&!document.hidden)frame=requestAnimationFrame(draw);}
 const imageObserver=new IntersectionObserver(entries=>{entries.forEach(entry=>{
  if(entry.isIntersecting)live.add(entry.target);else{live.delete(entry.target);const image=entry.target.querySelector('img');if(image)image.style.removeProperty('transform');}
 });schedule();},{rootMargin:'80px'});pictures.forEach(node=>{node.classList.add('motion-depth');imageObserver.observe(node);});
 const reveals=new IntersectionObserver(entries=>entries.forEach(entry=>{if(!entry.isIntersecting)return;
  const node=entry.target;
  if(node.matches('.editorial-hero-media')){
   const items=[...node.querySelectorAll('.content-grid > div')];
   if(items.length>1)items.forEach((item,i)=>play(item,[{transform:`translateX(${(1-i)*46}px) scale(.91)`,opacity:.5},{transform:'none',opacity:1}],{duration:900,delay:i*90}));
   else play(node,[{transform:'translateY(35px) scale(.96)',opacity:.55},{transform:'none',opacity:1}],{duration:950});
  }else if(node.matches('[data-composition=mosaic]'))[...node.children].forEach((child,i)=>play(child,[{transform:'translateY(32px)',opacity:.45},{transform:'none',opacity:1}],{duration:680,delay:i*90}));
  else play(node,[{transform:'translateY(26px)',opacity:.35},{transform:'none',opacity:1}],{duration:650});
  reveals.unobserve(node);
 }),{threshold:.12});
 root.querySelectorAll('.editorial-hero-media,.revision-source h2,.revision-proof h2,[data-composition=mosaic]').forEach(node=>reveals.observe(node));
 window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);
 function reset(){if(frame){cancelAnimationFrame(frame);frame=0;}running.forEach(a=>a.cancel());pictures.forEach(node=>node.querySelector('img')?.style.removeProperty('transform'));if(!reduced.matches&&!document.hidden)schedule();}
 reduced.addEventListener('change',reset);document.addEventListener('visibilitychange',reset);
})();
