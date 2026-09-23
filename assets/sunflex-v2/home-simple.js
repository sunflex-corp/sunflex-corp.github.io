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
  const story = document.querySelector('.solar-story');
  if (!story) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const copy = story.querySelector('.solar-story-copy');
  const stage = story.querySelector('.solar-stage');
  const clamp = n => Math.min(1, Math.max(0, n));
  const ramp = (p, a, b) => { const t = clamp((p-a)/(b-a)); return t*t*(3-2*t); };
  let frame = 0, current = 0, last = 0;
  const progress = () => clamp(-story.getBoundingClientRect().top / Math.max(1, story.offsetHeight-stage.offsetHeight));
  const aperture = story.querySelector('.solar-aperture');
  const cutout = story.querySelector('.solar-cutout');
  const white = story.querySelector('.solar-white');
  const photo = story.querySelector('.solar-backdrop');
  const shade = story.querySelector('.solar-shade');
  const hint = story.querySelector('.solar-story-hint');
  // Write only changed leaf properties, avoiding inherited variable invalidation.
  const set = (node, key, value) => {
    if (node.style[key] !== value) node.style[key] = value;
  };
  const paint = p => {
    const reveal = ramp(p,.68,.84);
    const scale = Math.exp(Math.log(24)*ramp(p,.12,.69)).toFixed(5);
    const transform = `scale(${scale})`;
    set(cutout, 'transform', transform);
    set(white, 'transform', transform);
    set(white, 'opacity', (1-ramp(p,.09,.24)).toFixed(5));
    set(aperture, 'opacity', (1-ramp(p,.51,.69)).toFixed(5));
    set(photo, 'transform', `scale(${(1.09-.09*ramp(p,.15,.78)).toFixed(5)})`);
    set(copy, 'opacity', reveal.toFixed(5));
    set(copy, 'transform', `translate3d(0,${((1-reveal)*35).toFixed(5)}px,0)`);
    set(shade, 'opacity', reveal.toFixed(5));
    set(hint, 'opacity', (1-ramp(p,.05,.18)).toFixed(5));
    if (copy.inert !== (reveal < .05)) copy.inert = reveal < .05;
  };
  const tick = time => {
    frame = 0;
    const target = progress();
    const dt = Math.min(64, last ? time-last : 16.67); last = time;
    current += (target-current)*(1-Math.exp(-dt/85));
    if (Math.abs(target-current)<.0001) current=target;
    paint(current);
    if (current!==target) frame=requestAnimationFrame(tick);
    else last=0;
  };
  const schedule = () => {
    if (!reduced.matches && !document.hidden && !frame) frame=requestAnimationFrame(tick);
  };
  const reset = () => {
    cancelAnimationFrame(frame);frame=0;last=0;
    story.classList.toggle('is-scrubbing',!reduced.matches);
    if(reduced.matches){
      [cutout,white,aperture,photo,copy,shade,hint].forEach(node=>{node.style.transform='';node.style.opacity='';});
      stage.classList.remove('is-motion-active');copy.inert=false;return;
    }
    current=progress();paint(current);
  };
  if(document.documentElement.dataset.motionEngine==='gsap'&&window.gsap&&window.ScrollTrigger){
    gsap.registerPlugin(ScrollTrigger);
    const media=gsap.matchMedia();
    media.add({animated:'(prefers-reduced-motion: no-preference)',reduced:'(prefers-reduced-motion: reduce)'},context=>{
      if(context.conditions.reduced){reset();return;}
      story.classList.add('is-scrubbing');const state={p:progress()};paint(state.p);
      gsap.fromTo(state,{p:0},{p:1,ease:'none',onUpdate:()=>paint(state.p),scrollTrigger:{trigger:story,start:'top top',end:()=>'+='+Math.max(1,story.offsetHeight-stage.offsetHeight),scrub:.65,onToggle:self=>stage.classList.toggle('is-motion-active',self.isActive)}});
      return()=>{copy.inert=false;stage.classList.remove('is-motion-active');};
    });
    return;
  }
  window.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('resize',reset);
  window.addEventListener('pageshow',reset);
  document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0;last=0;}else reset();});
  reduced.addEventListener('change',reset);
  // Promote only while this section is near the viewport; release GPU memory away from it.
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      stage.classList.toggle('is-motion-active', entries[0].isIntersecting && !reduced.matches);
    }, {rootMargin:'100% 0px'});
    observer.observe(story);
    reduced.addEventListener('change',()=>{observer.unobserve(story);observer.observe(story);});
  }
  reset();
})();
