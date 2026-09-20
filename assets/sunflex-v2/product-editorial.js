(() => {
  'use strict';
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  function tabs(root,controlsSelector,panelSelector,onSelect=()=>{}){
    const controls=root.querySelector(controlsSelector),panels=[...root.querySelectorAll(panelSelector)];
    if(!controls||!panels.length)return null;
    const buttons=[...controls.querySelectorAll('[role="tab"]')];
    if(buttons.length!==panels.length)return null;
    let selected=0;
    const select=(index,focus=false)=>{
      selected=index;
      buttons.forEach((button,i)=>{button.setAttribute('aria-selected',String(i===index));button.tabIndex=i===index?0:-1;panels[i].hidden=i!==index;panels[i].setAttribute('role','tabpanel');panels[i].setAttribute('aria-labelledby',button.id);});
      onSelect();if(focus)buttons[index].focus();
    };
    buttons.forEach((button,index)=>{
      button.addEventListener('click',()=>select(index));
      button.addEventListener('keydown',event=>{
        let next=index;
        if(event.key==='ArrowRight')next=(index+1)%buttons.length;
        else if(event.key==='ArrowLeft')next=(index+buttons.length-1)%buttons.length;
        else if(event.key==='Home')next=0;else if(event.key==='End')next=buttons.length-1;else return;
        event.preventDefault();select(next,true);
      });
    });
    controls.hidden=false;select(0);
    return{select,panels,get selected(){return selected;}};
  }
  const model=document.querySelector('[data-model-selector]');
  if(model){
    const compare=model.querySelector('.compare-models');
    const controller=tabs(model,'.model-tabs','[data-model-panel]',()=>{model.classList.remove('models-comparing');compare.setAttribute('aria-pressed','false');compare.textContent='세 모델 비교하기';});
    if(controller){
      model.classList.add('models-enhanced');model.querySelector('.model-controls').hidden=false;
      compare.addEventListener('click',()=>{
        if(model.classList.contains('models-comparing'))controller.select(controller.selected);
        else{model.classList.add('models-comparing');controller.panels.forEach(p=>{p.hidden=false;p.removeAttribute('role');});compare.setAttribute('aria-pressed','true');compare.textContent='선택한 모델만 보기';}
      });
    }
  }
  const use=document.querySelector('.bodycam-use');if(use)tabs(use,'.use-controls','[data-use-panel]');
  document.querySelectorAll('.editorial-overview').forEach(root=>{
    const rail=root.querySelector('.overview-rail'),controls=root.querySelector('.overview-controls');
    const prev=controls.querySelector('[data-rail-prev]'),next=controls.querySelector('[data-rail-next]');
    const update=()=>{controls.hidden=rail.scrollWidth<=rail.clientWidth+2;prev.disabled=rail.scrollLeft<2;next.disabled=rail.scrollLeft+rail.clientWidth>=rail.scrollWidth-2;};
    const move=direction=>rail.scrollBy({left:direction*(rail.firstElementChild.getBoundingClientRect().width+20),behavior:reduced.matches?'auto':'smooth'});
    prev.addEventListener('click',()=>move(-1));next.addEventListener('click',()=>move(1));rail.addEventListener('scroll',update,{passive:true});
    window.addEventListener('resize',update);update();
  });
  if('IntersectionObserver' in window&&!reduced.matches){
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-entering');observer.unobserve(entry.target);}}),{threshold:.08});
    document.querySelectorAll('.editorial-chapter').forEach(section=>observer.observe(section));
  }
  const motionSections=[...document.querySelectorAll('[data-product-motion]')];
  const sceneSections=[...document.querySelectorAll('[data-archetype="wearable"] .chapter-focus.chapter-media')];
  const flows=[...document.querySelectorAll('.editorial-flow')];
  const clamp=value=>Math.min(1,Math.max(0,value));
  const ease=value=>{const t=clamp(value);return t*t*(3-2*t);};
  const compact=window.matchMedia('(max-height: 650px)');
  let raf=0,lastTime=0;
  const positions=new Map();
  const draw=time=>{
    raf=0;let unsettled=false;
    const amount=1-Math.exp(-Math.min(64,lastTime?time-lastTime:16.67)/75);lastTime=time;
    motionSections.forEach(section=>{
      const stage=section.querySelector('.editorial-hero');
      const target=clamp((66-section.getBoundingClientRect().top)/Math.max(1,section.offsetHeight-stage.offsetHeight));
      let value=positions.get(section)??target;value+=(target-value)*amount;
      if(Math.abs(value-target)<.0001)value=target;else unsettled=true;
      positions.set(section,value);const progress=ease((value-.05)/.65);
      section.style.setProperty('--fan-shift',`${95*(1-progress)}%`);
      section.style.setProperty('--fan-tilt',`${7*(1-progress)}deg`);
      section.style.setProperty('--fan-scale',String(.85+.15*progress));
      section.style.setProperty('--fan-labels',String(ease((value-.45)/.25)));
      section.style.setProperty('--wearable-scale',String(1.12-.12*progress));
      section.style.setProperty('--wearable-shift',`${6*(1-progress)}%`);
      section.style.setProperty('--screen-scale',String(.82+.18*progress));
      section.style.setProperty('--screen-tilt',`${8*(1-progress)}deg`);
    });
    sceneSections.forEach(section=>{const p=ease((window.innerHeight-section.getBoundingClientRect().top)/(window.innerHeight*.9));section.style.setProperty('--scene-inset',`${12*(1-p)}%`);});
    flows.forEach(flow=>{const steps=[...flow.children],rect=flow.getBoundingClientRect();const p=clamp((window.innerHeight*.65-rect.top)/Math.max(rect.height,1));const active=Math.min(steps.length-1,Math.floor(p*steps.length));steps.forEach((step,i)=>step.classList.toggle('is-current-step',i===active));});
    if(unsettled)raf=requestAnimationFrame(draw);else lastTime=0;
  };
  const schedule=()=>{if(!raf&&!reduced.matches&&!compact.matches&&!document.hidden)raf=requestAnimationFrame(draw);};
  const configure=()=>{
    cancelAnimationFrame(raf);raf=0;lastTime=0;positions.clear();
    const enabled=!reduced.matches&&!compact.matches;
    motionSections.forEach(section=>{
      section.classList.toggle('motion-enabled',enabled);
      const stage=section.querySelector('.editorial-hero');
      // A long Korean product name or enlarged text must never be clipped by pinning.
      if(enabled&&stage.scrollHeight>stage.clientHeight+2)section.classList.remove('motion-enabled');
    });
    sceneSections.forEach(section=>section.classList.toggle('scene-reveal',enabled));
    if(enabled)schedule();
  };
  window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',configure);window.addEventListener('pageshow',configure);window.addEventListener('load',configure);
  document.fonts?.ready.then(configure);
  reduced.addEventListener('change',configure);compact.addEventListener('change',configure);
  document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0;lastTime=0;}else configure();});
  configure();
  // Fragment links into hidden model panels also work on direct arrival and back/forward.
  const revealHash=()=>{let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}const target=document.getElementById(id);if(!target)return;const panel=target.closest('[data-model-panel],[data-use-panel]');if(panel?.hidden){const button=document.querySelector(`[aria-controls="${panel.id}"]`);button?.click();target.scrollIntoView({block:'start'});}};
  window.addEventListener('hashchange',revealHash);revealHash();
})();
