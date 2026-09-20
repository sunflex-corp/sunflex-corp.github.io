(() => {
  'use strict';
  const root=document.querySelector('[data-cctv-process]');
  if(!root)return;
  const controls=root.querySelector('.cctv-step-controls');
  const buttons=[...controls.querySelectorAll('button')];
  const panels=[...root.querySelectorAll('[data-cctv-stage]')];
  let selected=-1;
  let seek=null;
  function select(index,focus=false){
    if(selected===index){if(focus)buttons[index].focus();return;}
    selected=index;
    buttons.forEach((button,i)=>{
      button.setAttribute('data-step-state',i===index?'current':i<index?'previous':'upcoming');button.setAttribute('aria-selected',String(i===index));button.tabIndex=i===index?0:-1;
      panels[i].hidden=i!==index;panels[i].setAttribute('role','tabpanel');panels[i].setAttribute('aria-labelledby',button.id);
    });
    if(focus)buttons[index].focus();
  }
  buttons.forEach((button,index)=>{
    button.addEventListener('click',()=>{select(index);if(seek)seek(index);});
    button.addEventListener('keydown',event=>{
      const next={ArrowRight:(index+1)%3,ArrowLeft:(index+2)%3,Home:0,End:2}[event.key];
      if(next===undefined)return;
      event.preventDefault();select(next,true);if(seek)seek(next);
    });
  });
  controls.hidden=false;select(0);
  const track=root.querySelector('.cctv-scroll-track');
  if(track){
    const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
    let enabled=false,raf=0,top=80,span=0;
    const draw=()=>{
      raf=0;if(!enabled)return;
      const distance=top-track.getBoundingClientRect().top;
      // Three equal reading intervals, with reversal using the same thresholds.
      const index=Math.max(0,Math.min(2,Math.floor(distance/(span/3))));
      if(distance>=0&&distance<=span)select(index);
      else if(distance<0)select(0);else select(2);
    };
    const schedule=()=>{if(enabled&&!raf)raf=requestAnimationFrame(draw);};
    const configure=()=>{
      const nav=document.querySelector('.product-local-nav');
      top=(nav?nav.getBoundingClientRect().height:64)+12;
      enabled=!reduced.matches&&window.innerHeight>=680;
      span=window.innerHeight*2.4;
      track.style.setProperty('--process-top',top+'px');
      track.style.setProperty('--process-span',span+'px');
      track.style.setProperty('--process-view',window.innerHeight+'px');
      track.classList.toggle('is-scroll-driven',enabled);
      schedule();
    };
    seek=index=>{
      if(!enabled)return;
      const start=window.scrollY+track.getBoundingClientRect().top-top;
      // Native scroll position stays in sync with manual selection without crossing other tabs.
      window.scrollTo({top:start+(index+.2)*span/3,behavior:'instant'});
    };
    window.addEventListener('scroll',schedule,{passive:true});
    window.addEventListener('resize',configure);
    reduced.addEventListener('change',configure);
    configure();
  }
  // Anchors remain usable inside native disclosures.
  const reveal=()=>{
    const target=document.getElementById(location.hash.slice(1));
    if(!target)return;
    const details=target.closest('details')||target.querySelector('details');if(details)details.open=true;
  };
  window.addEventListener('hashchange',reveal);reveal();
})();
