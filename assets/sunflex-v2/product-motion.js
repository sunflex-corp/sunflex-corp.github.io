/* Product motion: bounded scene transitions, reversible image depth, no scroll hijacking. */
(() => {
 'use strict';
 const clamp=n=>Math.min(1,Math.max(0,n));
 function pose(progress,mobile){const p=clamp(progress);return {scale:1.065-p*.065,y:(.5-p)*(mobile?12:36)};}
 if(typeof module!=='undefined')module.exports={pose};
 if(typeof document==='undefined')return;
 if(document.documentElement?.dataset.motionEngine==='gsap'&&window.gsap&&window.ScrollTrigger)return;
 const root=document.querySelector('[data-motion-profile]');
 if(!root||typeof IntersectionObserver==='undefined'||!Element.prototype.animate)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)'),mobile=matchMedia('(max-width:760px)');
 const live=new Set(),running=new Set(),owned=new WeakMap();let frame=0;
 function play(node,frames,options){
  if(!node||reduced.matches||document.hidden)return;
  owned.get(node)?.cancel();
  const animation=node.animate(frames,{duration:700,easing:'cubic-bezier(.16,1,.3,1)',...options});
  owned.set(node,animation);running.add(animation);
  const release=()=>{running.delete(animation);if(owned.get(node)===animation)owned.delete(node);};
  animation.onfinish=release;animation.oncancel=release;
 }
 // Editorial imagery progresses with the real scroll position and rewinds naturally.
 const pictures=[...root.querySelectorAll('[data-composition=panorama] > figure, [data-composition=portrait] > figure, [data-composition=editorial] > figure')];
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
  play(node,[{transform:'translateY(20px)',opacity:.5},{transform:'none',opacity:1}],{duration:600});
  reveals.unobserve(node);
 }),{threshold:.12});
 root.querySelectorAll('.editorial-hero-copy,.revision-source h2,.revision-proof h2').forEach(node=>reveals.observe(node));
 window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);
 function reset(){if(frame){cancelAnimationFrame(frame);frame=0;}running.forEach(a=>a.cancel());pictures.forEach(node=>node.querySelector('img')?.style.removeProperty('transform'));if(!reduced.matches&&!document.hidden)schedule();}
 reduced.addEventListener('change',reset);document.addEventListener('visibilitychange',reset);
})();
