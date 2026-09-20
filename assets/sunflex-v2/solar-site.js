(() => {
 'use strict';
 const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 const menu=$('.solar-menu');
 if(menu){
   document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.open){menu.open=false;$('summary',menu).focus();}});
   document.addEventListener('click',e=>{if(menu.open&&!menu.contains(e.target))menu.open=false;});
   $$('a',menu).forEach(a=>a.addEventListener('click',()=>menu.open=false));
 }
 const tools=$('.catalog-tools');
 if(tools){
   const cards=$$('[data-catalog-card]'),input=$('input[name=q]',tools),selects=$$('select',tools),tabs=$$('[data-category]',tools);
   let category='';
   const aliases={eyes:'detect',sound:'alert',guard:'respond',story:'record',air:'detect'};
   const normalize=s=>s.normalize('NFKC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
   const update=(write=false)=>{
     const query=normalize(input.value),terms=query.split(' ').filter(Boolean),values=Object.fromEntries(selects.map(s=>[s.name,s.value]));
     let count=0;
     cards.forEach(card=>{const match=(!category||card.dataset.category===category)&&terms.every(t=>normalize(card.dataset.search).includes(t))&&Object.entries(values).every(([key,value])=>!value||(card.dataset[key]||'').split(' ').includes(value));card.hidden=!match;if(match)count++;});
     $('#result-count').textContent=String(count);$('.catalog-empty').hidden=count!==0;
     tabs.forEach(t=>t.setAttribute('aria-pressed',String(t.dataset.category===category)));
     if(write){const url=new URL(location.href);['q','category',...selects.map(s=>s.name)].forEach(k=>url.searchParams.delete(k));if(input.value.trim())url.searchParams.set('q',input.value.trim());if(category)url.searchParams.set('category',category);Object.entries(values).forEach(([k,v])=>{if(v)url.searchParams.set(k,v);});history.replaceState(null,'',url.pathname+url.search+url.hash);}
   };
   const restore=()=>{const params=new URLSearchParams(location.search),raw=params.get('category')||'';category=aliases[raw]||raw;if(!tabs.some(t=>t.dataset.category===category))category='';input.value=params.get('q')||'';selects.forEach(s=>{s.value=params.get(s.name)||'';if(s.selectedIndex<0)s.value='';});if(selects.some(s=>s.value))$('.catalog-filters').open=true;update();};
   input.addEventListener('input',()=>update(true));selects.forEach(s=>s.addEventListener('change',()=>update(true)));
   tabs.forEach(t=>t.addEventListener('click',()=>{category=t.dataset.category;update(true);}));
   $$('[data-reset]').forEach(b=>b.addEventListener('click',()=>{category='';input.value='';selects.forEach(s=>s.value='');update(true);input.focus();}));
   window.addEventListener('popstate',restore);tools.hidden=false;restore();
 }
 const gallery=$('.product-gallery');
 if(gallery){const stage=$('.gallery-stage img',gallery),buttons=$$('[data-gallery-src]',gallery);buttons.forEach(button=>button.addEventListener('click',()=>{stage.src=button.dataset.gallerySrc;stage.alt=button.dataset.galleryAlt;stage.removeAttribute('srcset');buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));}));$('.gallery-thumbs',gallery).hidden=false;}
 const names=$('#product-names');
 if(names){try{const slug=new URLSearchParams(location.search).get('product'),name=JSON.parse(names.textContent)[slug],field=$('#need');if(name&&field&&!field.value)field.value=name+' 도입 문의';}catch{ /* No prefill for invalid data. */ }}
 const search=$('#support-search');
 if(search){const questions=$$('.faq details');$('.faq-search').hidden=false;search.addEventListener('input',()=>{const q=search.value.trim().toLocaleLowerCase();let n=0;questions.forEach(d=>{d.hidden=!d.textContent.toLocaleLowerCase().includes(q);if(!d.hidden)n++;});$('#support-search-status').textContent=q?`${n}개의 안내를 찾았습니다.`:'';});}
 if('IntersectionObserver' in window){
   const nav=$$('.product-index nav a');
   if(nav.length){const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){nav.forEach(a=>{const active=a.hash==='#'+entry.target.id;a.classList.toggle('is-current',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});}});},{rootMargin:'-20% 0px -60% 0px',threshold:0});$$('.detail-block').forEach(s=>observer.observe(s));}
   // Elements remain visible before JS and when animation is disabled.
   if(!reduced.matches){const reveal=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('solar-reveal');reveal.unobserve(entry.target);}}),{threshold:.08});$$('.solar-family,.solar-card,.category-topics a,.principle,.support-choice,.detail-block>header').forEach(el=>reveal.observe(el));}
 }
 const progress=document.createElement('div');progress.className='reading-progress';progress.setAttribute('aria-hidden','true');document.body.append(progress);
 const top=document.createElement('button');top.className='back-top';top.type='button';top.setAttribute('aria-label','페이지 맨 위로');top.textContent='↑';top.hidden=true;document.body.append(top);top.addEventListener('click',()=>{window.scrollTo({top:0,behavior:reduced.matches?'instant':'smooth'});$('#main-content').focus({preventScroll:true});});
 let ticking=false;const paint=()=>{const max=document.documentElement.scrollHeight-innerHeight;progress.style.transform=`scaleX(${max>0?Math.min(1,Math.max(0,scrollY/max)):0})`;top.hidden=scrollY<700;ticking=false;};window.addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(paint);ticking=true;}},{passive:true});paint();
})();
