(() => {
  'use strict';
  const header = document.querySelector('.home-simple .site-header');
  if (!header) return;
  let previous = Math.max(0, window.scrollY), scheduled = false;
  const update = () => {
    const current = Math.max(0, window.scrollY);
    const delta = current - previous;
    header.classList.toggle('is-scrolled', current > 24);
    if (current < 120) header.classList.remove('is-away');
    else if (Math.abs(delta) > 5) header.classList.toggle('is-away', delta > 0);
    // Keyboard users and an open mobile menu always keep navigation in view.
    if (header.contains(document.activeElement) || header.querySelector('[aria-expanded="true"]')) header.classList.remove('is-away');
    previous = current;
    scheduled = false;
  };
  window.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
  }, { passive: true });
  header.addEventListener('focusin', () => header.classList.remove('is-away'));
  window.addEventListener('pageshow', update);
  update();
  const visual=document.querySelector('.home-simple .map-visual');
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  if(visual && 'IntersectionObserver' in window && !reduced.matches){
    visual.classList.add('brand-reveal-ready');
    const reveal=new IntersectionObserver(entries=>{
      if(entries.some(entry=>entry.isIntersecting)){
        visual.classList.add('brand-revealed');reveal.disconnect();
      }
    },{threshold:.4});
    reveal.observe(visual);
    const finish=()=>{visual.classList.add('brand-revealed');reveal.disconnect();};
    document.querySelectorAll('[data-map-choice]').forEach(button=>button.addEventListener('click',finish));
    reduced.addEventListener('change',event=>{if(event.matches)finish();});
  }
})();
