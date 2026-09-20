(() => {
  'use strict';
  const root=document.querySelector('[data-cctv-process]');
  if(!root)return;
  const controls=root.querySelector('.cctv-step-controls');
  const buttons=[...controls.querySelectorAll('button')];
  const panels=[...root.querySelectorAll('[data-cctv-stage]')];
  function select(index,focus=false){
    buttons.forEach((button,i)=>{
      button.setAttribute('aria-selected',String(i===index));button.tabIndex=i===index?0:-1;
      panels[i].hidden=i!==index;panels[i].setAttribute('role','tabpanel');panels[i].setAttribute('aria-labelledby',button.id);
    });
    if(focus)buttons[index].focus();
  }
  buttons.forEach((button,index)=>{
    button.addEventListener('click',()=>select(index));
    button.addEventListener('keydown',event=>{
      const next={ArrowRight:(index+1)%3,ArrowLeft:(index+2)%3,Home:0,End:2}[event.key];
      if(next===undefined)return;
      event.preventDefault();select(next,true);
    });
  });
  controls.hidden=false;select(0);
  // Anchors remain usable inside native disclosures.
  const reveal=()=>{
    const target=document.getElementById(location.hash.slice(1));
    if(!target)return;
    const details=target.closest('details')||target.querySelector('details');if(details)details.open=true;
  };
  window.addEventListener('hashchange',reveal);reveal();
})();
