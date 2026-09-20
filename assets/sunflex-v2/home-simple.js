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
  const paint = p => {
    const reveal = ramp(p,.68,.84);
    story.style.setProperty('--word-scale', Math.exp(Math.log(24)*ramp(p,.12,.69)).toFixed(5));
    story.style.setProperty('--white-opacity', (1-ramp(p,.09,.24)).toFixed(5));
    story.style.setProperty('--mask-opacity', (1-ramp(p,.51,.69)).toFixed(5));
    story.style.setProperty('--photo-scale', (1.09-.09*ramp(p,.15,.78)).toFixed(5));
    story.style.setProperty('--copy-opacity', reveal.toFixed(5));
    story.style.setProperty('--hint-opacity', (1-ramp(p,.05,.18)).toFixed(5));
    // Invisible links must not receive focus; visible copy remains semantic.
    copy.inert = reveal < .05;
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
    if(reduced.matches){copy.inert=false;return;}
    current=progress();paint(current);
  };
  window.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('resize',reset);
  window.addEventListener('pageshow',reset);
  document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0;last=0;}else reset();});
  reduced.addEventListener('change',reset);
  reset();
})();
