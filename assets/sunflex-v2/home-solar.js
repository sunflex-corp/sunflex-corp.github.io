(() => {
 'use strict';
 const stage=document.querySelector('.simple-hero'),canvas=document.querySelector('#background-sun');
 if(!stage||!canvas)return;
 const params=new URLSearchParams(location.search);
 const reduced=params.get('motion')==='reduce'?{matches:true,addEventListener(){}}:matchMedia('(prefers-reduced-motion:reduce)');
 const mobile=matchMedia('(max-width:760px)');
 let width=0,height=0,inView=true,raf=0,last=0,time=0,pulse=-20,gl,program,loc={};
 let engagement=0,flareEngagement=0,targetEngagement=0,surfacePointer={x:0,y:0},flowDrift={x:0,y:0};
 let target={x:0,y:0},pointer={x:0,y:0},tint=[1,.62,.27],targetTint=tint.slice();
 const tints=[[1,.62,.27],[1,.43,.22],[.80,.65,1]];
 const paused=()=>stage.dataset.sunPaused==='true';
 const vertex='attribute vec2 a; void main(){gl_Position=vec4(a,0.,1.);}';
 const fragment=`precision highp float;
uniform vec2 uRes;uniform vec2 uPointer;uniform vec2 uSurfacePointer;uniform float uTime;uniform float uMobile;uniform float uPulse;uniform vec3 uTint;uniform sampler2D uNoise;uniform float uEngagement;uniform float uFlare;uniform vec2 uDrift;
// Seamless 3-D value noise from a small, repeatable two-channel lattice.
float noise3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);vec2 uv=i.xy+vec2(37.,17.)*i.z+f.xy;vec2 rg=texture2D(uNoise,(uv+.5)/256.).rg;return mix(rg.x,rg.y,f.z);}
float fbm(vec3 p){float n=0.,a=.52;for(int i=0;i<5;i++){n+=a*noise3(p);p=p*2.03+vec3(7.1,3.7,11.3);a*=.48;}return n;}
float bell(vec2 v,vec2 center,vec2 scale){vec2 p=(v-center)*scale;return exp(-dot(p,p));}
float prominence(float angle,float r,float origin,float spread,float height){float x=(angle-origin)/spread;float arch=1.006+height*sin(clamp(x,0.,1.)*3.14159);return exp(-pow((r-arch)*180.,2.))*smoothstep(0.,.12,x)*(1.-smoothstep(.88,1.,x));}
void main(){
 vec2 uv=gl_FragCoord.xy/uRes;float aspect=uRes.x/uRes.y;
 vec2 p=(uv-.5)*vec2(aspect,1.);
 vec2 center=vec2(mix(.235,.14,uMobile)*aspect,mix(.015,-.10,uMobile))+uPointer*vec2(.036,.024)+vec2(sin(uTime*.23)*.004,cos(uTime*.31)*.006);
 float radius=mix(.278,.225,uMobile)*(1.+sin(uTime*.54)*.004);vec2 q=(p-center)/radius;
 float r=length(q),angle=atan(q.y,q.x),t=uTime*.15;
 vec2 cursorOnSun=(uSurfacePointer*vec2(aspect,1.)-center)/radius;
 float cursorRadius=length(cursorOnSun);
 float surfacePresence=1.-smoothstep(1.,1.18,cursorRadius);
 vec2 flareAnchor=cursorOnSun/max(1.,cursorRadius);
 float edgeBlend=smoothstep(.70,.99,cursorRadius);
 vec2 surfaceNormal=cursorOnSun/max(.001,cursorRadius);
 float mx=clamp(uPointer.x+.5,0.,1.),my=clamp(uPointer.y+.5,0.,1.);
 // Pointer direction is measured from the solar center, in aspect-correct world space.
 vec2 aim=uPointer*vec2(aspect,1.)-center;
 float idleAngle=uTime*.12+.5;
 float targetAngle=atan(aim.y,aim.x+.00001);
 float angleDelta=atan(sin(targetAngle-idleAngle),cos(targetAngle-idleAngle));
 float lightAngle=idleAngle+angleDelta*uEngagement;
 vec2 direction=vec2(cos(lightAngle),sin(lightAngle));
 vec2 radial=q/max(r,.001);
 float focus=pow(max(0.,dot(radial,direction)),18.)*uEngagement*.12;
 float focusWide=pow(max(0.,dot(radial,direction)),3.)*uEngagement;
 // Atmosphere and corona share the same center, palette, and breathing rhythm.
 vec2 lightUV=center/vec2(aspect,1.)+.5;
 vec3 gold=mix(vec3(1.,.49,.14),uTint,.10);
 float breath=.94+.06*sin(uTime*.54);
 vec3 col=vec3(.019,.023,.030);
 vec2 field=(uv-lightUV)*vec2(aspect,1.);
 float nearGlow=exp(-dot(field,field)*5.8);
 vec2 drift=field-uPointer*vec2(.17,.12);
 float haze=exp(-dot(drift,drift)*1.9);
 float eddy=noise3(vec3(field*3.+uPointer*.20,t*.14));
 vec3 copper=mix(vec3(.15,.055,.023),vec3(.11,.058,.035),my);
 vec3 dusk=mix(vec3(.023,.035,.055),vec3(.048,.026,.040),mx);
 col+=gold*nearGlow*.061*breath+copper*haze*(.35+.20*eddy)*breath;
 col+=dusk*(1.-nearGlow)*(.40+.32*my);
 // Warm light spills out from the same active limb, not a detached cursor spotlight.
 float spill=exp(-max(r-1.,0.)*1.45)*focusWide*smoothstep(.95,1.3,r);
 float flareBreath=.86+.14*sin(uTime*1.7+noise3(vec3(direction*7.,uTime*.2))*3.);
 col+=gold*spill*.13*flareBreath;
 vec2 lightOrigin=center+direction*radius*1.02;
 vec2 scattered=(p-lightOrigin)*vec2(2.0,2.5);
 col+=gold*exp(-dot(scattered,scattered))*uEngagement*.018;
 // Solar bounce light reaches the editorial side as one broad, soft atmospheric ribbon.
 // Source, tint and breathing come from the same sun; the copy remains on a dark field.
 vec2 bounceTarget=vec2(-aspect*.24+uPointer.x*.38,.045+uPointer.y*.46);
 vec2 bounceSource=center+direction*radius*.24;
 vec2 bounceDirection=normalize(bounceTarget-bounceSource);
 vec2 fromSource=p-bounceSource;
 float travel=dot(fromSource,bounceDirection);
 float side=fromSource.x*bounceDirection.y-fromSource.y*bounceDirection.x;
 float air=noise3(vec3(p*2.2+uPointer*.28,uTime*.028));
 float spread=.15+max(travel,0.)*.22;
 float ribbon=exp(-pow((side+(air-.5)*.08)/spread,2.));
 float reach=smoothstep(-.18,.10,travel)*exp(-max(travel,0.)*.55);
 float response=uFlare*(.82+.18*flareBreath);
 float leftField=1.-smoothstep(.53,.80,uv.x);
 vec3 bounceColor=mix(vec3(.68,.29,.085),vec3(.53,.24,.12),my);
 col+=bounceColor*ribbon*reach*response*.30*leftField;
 // A softer secondary reflection gives depth without a second independent spotlight.
 float reflection=exp(-pow((side+.21)/(.36+max(travel,0.)*.16),2.));
 col+=vec3(.25,.12,.07)*reflection*reach*response*.10*leftField;
 // Gentle localized protection under the headline, with no visible rectangle or hard mask.
 float copyGuard=bell(uv,vec2(.26,.54),vec2(2.6,2.0))*leftField;
 col*=1.-copyGuard*.13;
 // Slow circumsolar scattering follows the same rotation as the visible surface.
 vec2 sweep=vec2(cos(uTime*.095),sin(uTime*.095));
 float rayField=pow(max(0.,dot(normalize(field+vec2(.0001)),sweep)),8.);
 col+=gold*haze*rayField*.022;
 vec2 ringDirection=q/max(r,.001);
 float flow=noise3(vec3(ringDirection*8.,t*.45));
 float fineFlow=noise3(vec3(ringDirection*33.,t*.7+4.));
 float edge=r-1.;float outer=max(edge,0.);

 // Outward advection and curved turbulence form continuously changing fire tongues.
 float curl=noise3(vec3(ringDirection*9.,outer*6.-uTime*.31))-.5;
 float bentAngle=angle+curl*outer*.7;
 vec2 bent=vec2(cos(bentAngle),sin(bentAngle));
 float plasma=noise3(vec3(bent*25.,outer*16.-uTime*.85));
 float finePlasma=noise3(vec3(bent*61.,outer*29.-uTime*1.25));
 float height=.040+.075*flow+.11*focus;
 float tongues=exp(-outer/max(height,.01))*pow(plasma,2.)*(.32+finePlasma*.42);
 float outerGate=smoothstep(.997,1.018,r);
 float corona=exp(-outer*11.)*(.10+.14*flow)+exp(-outer*3.6)*.033;
 float rim=exp(-abs(edge)*155.)*(.40+.42*flow+.14*fineFlow+.68*focus*flareBreath);
 col+=gold*(corona+tongues*(1.+focus*1.7))*breath*outerGate;
 col+=mix(gold,vec3(1.,.86,.58),.40)*rim;
 // Small closed magnetic loops grow and fade independently along the limb.
 float arcs=prominence(angle,r,.42+sin(uTime*.23)*.08,.20,.075+.035*sin(uTime*.9))+prominence(angle,r,2.30+sin(uTime*.17)*.04,.17,.06+.023*sin(uTime*.67))+prominence(angle,r,-1.04,.15,.04+.020*sin(uTime*.8));
 col+=gold*arcs*(.32+.16*sin(uTime*.85));
 // Responsive flare bloom at the pointed-to limb; it lights the surrounding atmosphere.
 float hotspot=exp(-pow((r-1.02)*19.,2.))*pow(max(0.,dot(radial,direction)),75.)*uEngagement*.10;
 col+=vec3(1.,.72,.34)*hotspot*.62*flareBreath;
 if(r<1.006){
  float z=sqrt(max(0.,1.-r*r));vec3 sphere=vec3(q,z);
  float rot=uTime*.095;mat2 tilt=mat2(.980,-.199,.199,.980);sphere.xy=tilt*sphere.xy;mat2 turn=mat2(cos(rot),-sin(rot),sin(rot),cos(rot));sphere.xz=turn*sphere.xz;
  vec3 domain=sphere*10.8;
  vec3 warp=vec3(noise3(domain+vec3(t,0.,1.)),noise3(domain+vec3(8.,t,4.)),noise3(domain+vec3(2.,9.,t)))-.5;
  float cloud=fbm(domain+warp*1.4+vec3(0.,t*.16,0.));
  float granules=noise3(sphere*155.+warp*3.);
  float detail=noise3(sphere*63.+warp*5.);
  float flux=fbm(domain*2.1+warp*3.);
  float filaments=pow(max(0.,1.-abs(flux-.48)*6.),12.);
  float pores=noise3(sphere*245.+warp*4.);
  float active=smoothstep(.43,.70,cloud);
  float limb=.72+.28*pow(z,.4);
  // Multiscale photosphere: convection cells, thin hot filaments, then fine granular relief.
  float relief=.54+granules*.53+detail*.18+pores*.12;
  float energy=(.14+cloud*.26+active*.22+filaments*.10)*relief*limb;
  // Cursor heats the same material, preserving its local texture instead of painting a white blob.
  float surfaceHover=(1.-smoothstep(.98,1.07,length(cursorOnSun)))*uEngagement;
  vec2 cursorDelta=q-cursorOnSun;
  float core=exp(-dot(cursorDelta,cursorDelta)/.012);
  float softLight=exp(-dot(cursorDelta,cursorDelta)/.070);
  // Hover activates turbulent filaments and convection cells on the sphere itself.
  // The envelope only selects the region; emission follows moving material detail.
  float current=noise3(sphere*43.+warp*6.+vec3(0.,-uTime*.38,uTime*.19));
  float currentFine=noise3(sphere*112.+warp*8.+vec3(uTime*.24,0.,-uTime*.31));
  float hotVeins=pow(max(0.,1.-abs(current-.50)*5.5),7.);
  float hotCells=smoothstep(.40,.78,currentFine);
  float brokenEnvelope=exp(-dot(cursorDelta,cursorDelta)/(.042+current*.032));
  float reaction=brokenEnvelope*surfaceHover;
  energy*=1.+(core*.30+softLight*.16)*surfaceHover;
  energy+=reaction*(hotVeins*.48+hotCells*.16+filaments*.18);
  // Dark interstices remain visible between luminous ridges at peak response.
  energy-=reaction*(1.-hotCells)*(1.-hotVeins)*.032;
  vec3 deepGold=vec3(.24,.057,.007),solarGold=vec3(1.,.53,.115),whiteGold=vec3(1.,.86,.47);
  vec3 disk=mix(deepGold,solarGold,smoothstep(.14,.57,energy));
  disk+=whiteGold*smoothstep(.46,.95,energy)*.36;
  disk+=whiteGold*filaments*active*.065;
  disk+=vec3(1.,.94,.70)*reaction*hotVeins*(.15+.16*hotCells);
  // Gentle highlight compression retains the hot texture at the peak of cursor illumination.
  disk=disk/(1.+disk*.12);
  disk+=gold*pow(1.-z,10.)*(.13+.17*flow+.12*focus);
  col=mix(col,disk,1.-smoothstep(.992,1.005,r));
 }
 // Foreground plasma arches are anchored at the actual cursor, after the opaque disk.
 // A small tilted bundle lifts above two surface feet, with open spaces between strands.
 vec2 local=q-flareAnchor;
 float localFlare=surfacePresence*uFlare;
 if(localFlare>.001&&length(local)<.40){
  float eruptionAge=max(0.,uTime-uPulse);
  float impulse=(1.-exp(-eruptionAge*8.))*exp(-eruptionAge*1.8);
  float threads=0.,sheath=0.;
  float footprint=1./max(1.,uRes.y*radius);
  for(int i=0;i<6;i++){
   float k=float(i),group=floor(k/2.),layer=mod(k,2.);
   // Three overlapping currents steer independently; no fixed upright flare stamp.
   float bearing=group*2.32+.65*sin(uTime*(.17+group*.021)+group*1.9)+.18*sin(uTime*.43+group);
   vec2 liftAxis=vec2(cos(bearing),sin(bearing));
   liftAxis=normalize(liftAxis+uDrift*.55);
   // Near the limb, all currents bend outward and their feet inherit the spherical contour.
   liftAxis=normalize(mix(liftAxis,surfaceNormal,edgeBlend)+surfaceNormal*.001);
   vec2 acrossAxis=vec2(liftAxis.y,-liftAxis.x);
   vec2 patch=vec2(dot(local,acrossAxis),dot(local,liftAxis));
   float life=.5+.5*sin(uTime*(.61+group*.11)-group*2.094);
   float dominance=.14+.86*life*life;
   float halfSpan=.095+layer*.020+life*.022;
   float along=(patch.x+halfSpan)/(2.*halfSpan);
   float gate=smoothstep(0.,.06,along)*(1.-smoothstep(.94,1.,along));
   float warpedAlong=clamp(along+.075*sin(along*3.14159)*sin(uTime*.32+group),0.,1.);
   float arch=pow(max(0.,sin(warpedAlong*3.14159)),.72+group*.09);
   float rise=(.09+life*.15+layer*.022)*(.40+.60*uFlare)+impulse*.055;
   float crossCoordinate=dot(flareAnchor,acrossAxis)+patch.x;
   float curvedSurface=sqrt(max(0.,1.-crossCoordinate*crossCoordinate))-dot(flareAnchor,liftAxis);
   float root=mix(-.025,curvedSurface-.003,edgeBlend);
   float path=root+arch*rise+sin(along*16.-uTime*(.8+group*.14)+k)*.004*arch;
   float d=patch.y-path;
   float stream=(.35+.65*pow(.5+.5*sin(along*20.-uTime*2.3+k*1.7),3.))*dominance;
   // A pixel-aware footprint avoids subpixel sparkle on small or high-density canvases.
   float nativeWidth=.0035-layer*.0006;
   float threadWidth=sqrt(nativeWidth*nativeWidth+footprint*footprint*.65);
   float taper=.55+.45*sin(clamp(along,0.,1.)*3.14159);
   threads+=exp(-pow(d/(threadWidth*taper),2.))*gate*stream*(nativeWidth/threadWidth);
   sheath+=exp(-pow(d*105.,2.))*gate*(.18+.82*stream)*dominance;
  }
  // Copper edges and a warm-white core give the hovering threads depth over the photosphere.
  // Keep the outer corona transparent: depth shading belongs only on the opaque sphere.
  float diskCoverage=1.-smoothstep(.992,1.005,r);
  col*=1.-min(.40,sheath*.16)*localFlare*diskCoverage;
  col+=vec3(1.,.92,.65)*(1.-exp(-threads*1.6))*localFlare;
  col+=vec3(1.,.25,.025)*sheath*localFlare*.085;
  // Feather the attachment into the existing rim, with no detached hard-edged ring.
  float contact=exp(-pow((r-1.)*70.,2.))*exp(-dot(local,local)*65.);
  col+=vec3(1.,.56,.18)*contact*localFlare*edgeBlend*.22;
  // A short, soft wake connects quick cursor movement while the hot core stays exact.
  vec2 wakeLocal=local+uDrift*.065;
  float wakeLength=length(uDrift);
  col+=gold*exp(-dot(wakeLocal,wakeLocal)*58.)*localFlare*(.025+.04*wakeLength);
 }
 // Gentle film grain prevents banding without distracting moving noise.
 float grain=fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5;
 col+=grain*.003;
 col*=1.-.20*dot(uv-.5,uv-.5);
 gl_FragColor=vec4(col,1.);
}`;
 function init(){
  if(params.has('fallback')){stage.dataset.renderer='css';return;}
  gl=canvas.getContext('webgl',{alpha:false,antialias:false,depth:false,stencil:false,powerPreference:'low-power'});
  if(!gl){stage.dataset.renderer='css';return;}
  const compile=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);return s};
  const vs=compile(gl.VERTEX_SHADER,vertex),fs=compile(gl.FRAGMENT_SHADER,fragment);
  program=gl.createProgram();gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);
  if(!gl.getProgramParameter(program,gl.LINK_STATUS)){console.error('Solar shader:',gl.getProgramInfoLog(program),gl.getShaderInfoLog(fs));gl.deleteProgram(program);gl=null;return;}
  gl.deleteShader(vs);gl.deleteShader(fs);gl.useProgram(program);
  const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
  const a=gl.getAttribLocation(program,'a');gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,2,gl.FLOAT,false,0,0);
  for(const n of ['uRes','uPointer','uTime','uProgress','uMobile','uPulse','uTint','uEngagement','uSurfacePointer','uFlare','uDrift'])loc[n]=gl.getUniformLocation(program,n);
  // A deterministic 256² lattice avoids expensive per-fragment hash noise.
  let seed=42;const lattice=new Uint8Array(256*256);
  for(let i=0;i<lattice.length;i++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;lattice[i]=seed>>>24;}
  const data=new Uint8Array(256*256*4);
  for(let y=0;y<256;y++)for(let x=0;x<256;x++){const i=(y*256+x)*4;data[i]=lattice[y*256+x];data[i+1]=lattice[((y+17)%256)*256+(x+37)%256];data[i+3]=255;}
  const texture=gl.createTexture();gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,texture);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,256,256,0,gl.RGBA,gl.UNSIGNED_BYTE,data);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.REPEAT);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.REPEAT);
  gl.uniform1i(gl.getUniformLocation(program,'uNoise'),0);
  stage.classList.add('sun-webgl');stage.dataset.renderer='webgl';
 }

 function resize(){
  width=stage.clientWidth;height=stage.clientHeight;
  const budget=mobile.matches?650000:1400000;
  const scale=Math.min(devicePixelRatio||1,1.4,Math.sqrt(budget/Math.max(1,width*height)));
  canvas.width=Math.max(1,Math.floor(width*scale));canvas.height=Math.max(1,Math.floor(height*scale));
  if(gl)gl.viewport(0,0,canvas.width,canvas.height);
  wake();
 }
 function draw(now){
  raf=0;if(document.hidden||!inView)return;
  const delta=last?Math.min((now-last)/1000,.06):1/60;last=now;
  const still=paused()||reduced.matches||!gl;
  if(params.get('qa')==='xy')time=4;else if(!still)time+=delta;
  const lerp=reduced.matches?1:1-Math.exp(-delta*3.4);
  engagement+=(targetEngagement-engagement)*(reduced.matches?1:1-Math.exp(-delta*8.));
  flareEngagement+=(targetEngagement-flareEngagement)*lerp;
  const flowEase=1-Math.exp(-delta*8.);
  flowDrift.x+=((still?0:(target.x-pointer.x)*18.)-flowDrift.x)*flowEase;
  flowDrift.y+=((still?0:(target.y-pointer.y)*18.)-flowDrift.y)*flowEase;
  pointer.x+=(target.x-pointer.x)*lerp;pointer.y+=(target.y-pointer.y)*lerp;
  tint=tint.map((v,i)=>v+(targetTint[i]-v)*lerp);
  if(gl){
   gl.uniform2f(loc.uRes,canvas.width,canvas.height);gl.uniform2f(loc.uPointer,pointer.x,pointer.y);gl.uniform2f(loc.uSurfacePointer,surfacePointer.x,surfacePointer.y);
   gl.uniform1f(loc.uTime,time);gl.uniform1f(loc.uEngagement,engagement);gl.uniform1f(loc.uFlare,flareEngagement);gl.uniform2f(loc.uDrift,Math.tanh(flowDrift.x),Math.tanh(flowDrift.y));gl.uniform1f(loc.uProgress,0);gl.uniform1f(loc.uMobile,mobile.matches?1:0);
   gl.uniform1f(loc.uPulse,pulse);gl.uniform3fv(loc.uTint,tint);gl.drawArrays(gl.TRIANGLES,0,6);
   if(params.has('qa')){stage.dataset.sunTime=time.toFixed(3);stage.dataset.sunRotation=(time*.095).toFixed(3);stage.dataset.sunEngagement=engagement.toFixed(3);stage.dataset.sunFlare=flareEngagement.toFixed(3);stage.dataset.sunSurfacePointer=`${surfacePointer.x.toFixed(3)},${surfacePointer.y.toFixed(3)}`;stage.dataset.sunPointer=`${pointer.x.toFixed(3)},${pointer.y.toFixed(3)}`;stage.dataset.sunFrames=String(Number(stage.dataset.sunFrames||0)+1);}
  }
  const settling=Math.abs(flowDrift.x)+Math.abs(flowDrift.y)>.001||Math.abs(flareEngagement-targetEngagement)>.001||Math.abs(engagement-targetEngagement)>.001||tint.some((v,i)=>Math.abs(v-targetTint[i])>.001)||Math.abs(pointer.x-target.x)+Math.abs(pointer.y-target.y)>.001;
  if(gl&&!reduced.matches&&(!still||settling))raf=requestAnimationFrame(draw);
 }
 function wake(){if(!raf&&!document.hidden&&inView){last=0;raf=requestAnimationFrame(draw);}}
 stage.addEventListener('pointermove',e=>{
  if(reduced.matches||paused()||(e.pointerType!=='mouse'&&e.pointerType!=='pen'))return;
  const r=stage.getBoundingClientRect();targetEngagement=1;target={x:(e.clientX-r.left)/width-.5,y:.5-(e.clientY-r.top)/height};surfacePointer={...target};wake();
 },{passive:true});
 stage.addEventListener('pointerleave',()=>{if(!paused()){targetEngagement=0;target={x:0,y:0};wake();}});
 let touchRelease=0;
 stage.addEventListener('pointerup',e=>{
  if(e.pointerType!=='touch'||e.target.closest('a,button')||reduced.matches||paused())return;
  const r=stage.getBoundingClientRect();target={x:(e.clientX-r.left)/width-.5,y:.5-(e.clientY-r.top)/height};surfacePointer={...target};targetEngagement=1;
  clearTimeout(touchRelease);touchRelease=setTimeout(()=>{if(!paused()){targetEngagement=0;target={x:0,y:0};wake();}},1600);wake();
 });
 stage.addEventListener('click',e=>{if(e.target.closest('a,button')||reduced.matches||paused())return;pulse=time;wake();});
 new MutationObserver(()=>{
  targetTint=tints[Number(stage.dataset.current)||0];
  if(raf){cancelAnimationFrame(raf);raf=0;}wake();
 }).observe(stage,{attributes:true,attributeFilter:['data-current','data-sun-paused']});
 document.addEventListener('visibilitychange',()=>{if(raf){cancelAnimationFrame(raf);raf=0;}wake();});
 new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;if(!inView&&raf){cancelAnimationFrame(raf);raf=0;}wake();}).observe(stage);
 reduced.addEventListener('change',()=>{targetEngagement=0;target={x:0,y:0};if(raf){cancelAnimationFrame(raf);raf=0;}wake();});
 new ResizeObserver(resize).observe(stage);
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();if(raf)cancelAnimationFrame(raf);raf=0;gl=null;stage.classList.remove('sun-webgl');stage.dataset.renderer='css';});
 canvas.addEventListener('webglcontextrestored',()=>{init();resize();wake();});
 targetTint=tints[Number(stage.dataset.current)||0];init();resize();wake();
})();
