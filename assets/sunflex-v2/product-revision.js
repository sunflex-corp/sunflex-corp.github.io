(() => {
 'use strict';
 function reveal(hash, scroll=false) {
  if(!hash||hash==='#')return;
  let target;try{target=document.getElementById(decodeURIComponent(hash.slice(1)));}catch{return;}
  if(!target)return;
  let parent=target.parentElement;
  while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}
  if(scroll)requestAnimationFrame(()=>target.scrollIntoView({block:'start',behavior:'instant'}));
 }
 document.addEventListener('click',event=>{
  const link=event.target.closest('a[href^="#"]');if(!link)return;
  reveal(link.hash,true);
 });
 window.addEventListener('hashchange',()=>reveal(location.hash,true));
 reveal(location.hash,true);
})();
