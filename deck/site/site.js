/* Pik deck: navigation, keypress builds, the attention rule, the camera, the animated pieces, print mode.
   Keys: Right / Space = next build step, then next slide. Left = back (exactly reversed). Home / End. Digits jump (two digits within 0.6 s).
   N = speaker notes. Click anywhere = next step (the video plays on click instead). ?slide=N opens a slide. ?print=1 stacks every
   slide in its final state for the PDF. Everything runs from file:// with no network: fonts, d3, p5 and the land data are vendored.
   Attention rule: on every build the elements already shown drop to opacity .35 and the newest is full; the last one stays full.
   Camera: a slide's content sits in one .camera wrapper; a step can carry data-camera="x y scale" (canvas px, the point to centre on).
   The final build always returns to the full view. Off in print mode and under prefers-reduced-motion. */
(function(){
'use strict';
const Q=new URLSearchParams(location.search);
const PRINT=Q.get('print')==='1';
const REDUCED=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
const NOCAM=PRINT||REDUCED;
const $=(s,r)=> (r||document).querySelector(s);
const $$=(s,r)=> Array.from((r||document).querySelectorAll(s));
const stage=$('#stage');
const slides=$$('.slide');
const mains=slides.filter(s=>s.classList.contains('main'));
const appx=slides.filter(s=>s.classList.contains('appx'));
const HOOKS={};           // name -> factory(el, slide) -> {step(n, instant), leave()}
const live={};            // slide id -> [hook instances]
const CAMERA={};          // slide id -> {step: [x, y, scale]} for hook-driven steps; static ones are data-camera attributes
const LIME=[214,242,90], LIME_DEEP=[191,224,48], INK=[23,23,23], BODY=[77,77,77], MUTE=[136,136,136], HAIR=[235,235,235];
const easeOut=t=>1-Math.pow(1-t,3);
const easeInOut=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
function txt(p,str,x,y,size,rgb,alpha,align,base){const c=p.drawingContext;c.save();c.font=size+'px "Geist Mono"';c.fillStyle='rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+','+alpha+')';c.textAlign=align||'left';c.textBaseline=base||'top';c.fillText(str,x,y);c.restore()}

function pad(n){return String(n).padStart(2,'0')}
function maxStep(s){let m=+(s.dataset.steps||0);$$('[data-b]',s).forEach(e=>{m=Math.max(m,+e.dataset.b)});return m}
function label(i){const s=slides[i];
  if(s.classList.contains('main'))return pad(mains.indexOf(s)+1)+' / '+pad(mains.length);
  if(s.classList.contains('divider'))return 'Appendix';
  return 'A'+(appx.indexOf(s)+1)+' / A'+appx.length}

function init(s){if(live[s.id])return;live[s.id]=[];
  const els=[];if(s.dataset.hook)els.push(s);$$('[data-hook]',s).forEach(e=>els.push(e));
  els.forEach(el=>{const f=HOOKS[el.dataset.hook];if(!f){console.error('[deck] no hook named '+el.dataset.hook);return}
    try{const h=f(el,s);if(h)live[s.id].push(h)}catch(e){console.error('[deck] hook '+el.dataset.hook+' failed: '+(e&&e.stack||e))}})}

/* reveal, the attention rule, the hooks, the camera; all a pure function of the step, so Left reverses exactly */
function apply(s,n,instant){
  const els=$$('[data-b]',s);let newest=0;els.forEach(e=>{const b=+e.dataset.b;if(b<=n&&b>newest)newest=b});
  els.forEach(e=>{const b=+e.dataset.b;e.classList.toggle('on',b<=n);e.classList.toggle('past',b<=n&&b<newest)});
  (live[s.id]||[]).forEach(h=>{if(h.step)h.step(n,!!instant)});
  camTo(s,n,instant)}
function cameraFor(s,n){let cam=[960,540,1];const decl=CAMERA[s.id]||{};
  for(let k=0;k<=n;k++){const el=$('[data-b="'+k+'"][data-camera]',s);if(el)cam=el.dataset.camera.trim().split(/[\s,]+/).map(Number);else if(decl[k])cam=decl[k]}
  if(n>=maxStep(s))cam=[960,540,1];return cam}
function camTo(s,n,instant){const w=$('.camera',s);if(!w)return;if(NOCAM){w.style.transform='';return}
  let [x,y,k]=cameraFor(s,n);k=Math.max(1,Math.min(2.2,k||1));
  const hw=960/k,hh=540/k;x=Math.max(hw,Math.min(1920-hw,x));y=Math.max(hh,Math.min(1080-hh,y));
  const t=k===1?'':`translate(${(k*(960-x)).toFixed(1)}px,${(k*(540-y)).toFixed(1)}px) scale(${k})`;
  if(instant){w.style.transition='none';w.style.transform=t;void w.offsetWidth;w.style.transition=''}else w.style.transform=t}

let cur=-1,step=0;
function show(i,n,instant){i=Math.max(0,Math.min(slides.length-1,i));const s=slides[i];const m=maxStep(s);n=Math.max(0,Math.min(m,n));
  if(i!==cur){if(cur>=0){slides[cur].classList.remove('cur');(live[slides[cur].id]||[]).forEach(h=>{if(h.leave)h.leave()})}
    s.classList.add('cur');cur=i;init(s);instant=true}
  step=n;apply(s,n,instant);
  document.body.classList.toggle('theme-dark',s.classList.contains('dark'));
  $('#prog').textContent=label(i);renderNotes();
  try{history.replaceState(null,'','#'+(i+1))}catch(e){}}
function next(){if(step<maxStep(slides[cur]))show(cur,step+1);else if(cur<slides.length-1)show(cur+1,0)}
function prev(){if(step>0)show(cur,step-1);else if(cur>0)show(cur-1,maxStep(slides[cur-1]))}

function renderNotes(){const d=$('#drawer');const s=slides[cur];if(!s)return;
  const head='<div class="k">'+label(cur)+' · '+(s.dataset.name||'')+' · step '+step+' of '+maxStep(s)+' · N notes · ← → build steps · Home End · digits jump · click = next</div>';
  const ps=$$('.notes p',s).map(p=>'<p class="'+(+p.dataset.step===step?'cur':'')+'">'+p.innerHTML+'</p>').join('');
  d.innerHTML=head+ps}

function fit(){const k=Math.min(innerWidth/1920,innerHeight/1080);stage.style.setProperty('--s',k)}

/* ---------------- hooks ---------------- */

/* 02 problem: five role discs on the right third; they dissolve into one blob on the "why now" step */
HOOKS.roles=function(el){
  const W=520,H=556,cx=260,cy=250;
  const roles=[['HR planner',96,78],['Engineer',410,66],['Designer',258,208],['Product manager',110,380],['Sales',412,372]];
  let t=0,target=0,inst=null;
  new p5(p=>{
    p.setup=()=>{p.createCanvas(W,H);if(PRINT)p.pixelDensity(1);if(PRINT)p.noLoop()};
    p.draw=()=>{p.clear();
      if(PRINT)t=target;else t+=(target-t)*0.045;if(Math.abs(target-t)<.002)t=target;
      const e=easeInOut(t);const ga=Math.max(0,(t-.35)/.65);
      if(ga>0){p.push();p.noStroke();p.fill(LIME[0],LIME[1],LIME[2],255*ga);p.circle(cx,cy,2*(96+ga*18));p.pop()}
      roles.forEach(([name,x0,y0],i)=>{const a=-Math.PI/2+i*Math.PI*2/5;const x1=cx+62*Math.cos(a),y1=cy+62*Math.sin(a);
        const x=p.lerp(x0,x1,e),y=p.lerp(y0,y1,e);const r=40-8*e;const la=1-Math.min(1,t*1.6);
        p.push();p.drawingContext.shadowColor='rgba(0,0,0,.10)';p.drawingContext.shadowBlur=8;p.drawingContext.shadowOffsetY=2;
        p.stroke(HAIR[0],HAIR[1],HAIR[2]);p.strokeWeight(1);p.fill(255);p.circle(x,y,r*2);p.pop();
        if(la>0)txt(p,name,x,y+r+12,20,BODY,la,'center','top')})};
    inst=p;
  },el);
  const cv=()=>el.querySelector('canvas');
  return {step(n,instant){target=n>=3?1:0;if(instant||PRINT)t=target;if(PRINT&&inst)inst.redraw();
    const c=cv();if(c){c.style.transition=instant?'none':'opacity .24s ease-out';c.style.opacity=(n>3&&!PRINT)?'.35':'1'}}}
};

/* 04 solution: the demo video, muted until clicked, big play affordance */
HOOKS.video=function(el){
  const v=$('video',el);
  el.addEventListener('click',e=>{e.stopPropagation();if(PRINT)return;if(v.paused){v.muted=false;v.play().catch(err=>console.error('[deck] video play failed: '+err))}else v.pause()});
  v.addEventListener('play',()=>el.classList.add('playing'));
  v.addEventListener('pause',()=>el.classList.remove('playing'));
  v.addEventListener('ended',()=>{el.classList.remove('playing');v.currentTime=0});
  v.addEventListener('error',()=>console.error('[deck] video failed to load: ../pik_demo_90s.mp4'));
  return {step(){},leave(){if(!v.paused)v.pause()}}
};

/* 06 impact: the number counts up once (the camera sits on it); the rings grow on their step (CSS) */
HOOKS.impact=function(s){
  const num=$('.num',s);const val=+num.dataset.value,dec=+num.dataset.decimals||0,suf=num.dataset.suffix||'';
  const fmt=x=>x.toFixed(dec)+suf;let done=false,raf=0;
  CAMERA[s.id]={0:[615,320,1.3]}; // opens close on the number; build 2 carries the pull-back on its element
  return {step(n,instant){
    if(n>=1){if(done)return;done=true;if(instant||PRINT){num.textContent=fmt(val);return}
      const t0=performance.now(),D=1200;cancelAnimationFrame(raf);
      const tick=now=>{const k=Math.min(1,(now-t0)/D);num.textContent=fmt(val*easeOut(k));if(k<1)raf=requestAnimationFrame(tick)};raf=requestAnimationFrame(tick)}
    else{done=false;cancelAnimationFrame(raf);num.textContent=fmt(0)}}}
};

/* 08 technical: the pipeline as SVG, drawn stage by stage; the camera follows each stage and pulls back for the red path */
HOOKS.arch=function(s){
  const box=$('.arch',s);const NS='http://www.w3.org/2000/svg';const OX=160,OY=160+212+36; // canvas offset of the diagram's origin
  const svg=document.createElementNS(NS,'svg');svg.setAttribute('viewBox','0 0 1600 508');box.appendChild(svg);
  const defs=document.createElementNS(NS,'defs');defs.innerHTML='<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#888888"/></marker><marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#ee0000"/></marker>';svg.appendChild(defs);
  const root=document.createElementNS(NS,'g');root.setAttribute('transform','translate(0,36)');svg.appendChild(root);
  const groups={},bbox={};const G=st=>{if(!groups[st]){const g=document.createElementNS(NS,'g');g.setAttribute('class','g');g.dataset.stage=st;root.appendChild(g);groups[st]=g}return groups[st]};
  function grow(st,x,y,w,h){const b=bbox[st]||(bbox[st]=[1e9,1e9,-1e9,-1e9]);b[0]=Math.min(b[0],x);b[1]=Math.min(b[1],y);b[2]=Math.max(b[2],x+w);b[3]=Math.max(b[3],y+h)}
  function node(st,x,y,w,h,lines,cls){const g=document.createElementNS(NS,'g');g.setAttribute('class','node '+(cls||''));
    const r=document.createElementNS(NS,'rect');r.setAttribute('x',x);r.setAttribute('y',y);r.setAttribute('width',w);r.setAttribute('height',h);r.setAttribute('rx',12);g.appendChild(r);
    const lh=[30,26,26];const total=lines.reduce((a,l,i)=>a+lh[Math.min(i,2)],0);let yy=y+h/2-total/2;
    lines.forEach((l,i)=>{const t=document.createElementNS(NS,'text');t.setAttribute('x',x+w/2);t.setAttribute('text-anchor','middle');const size=lh[Math.min(i,2)];yy+=size;t.setAttribute('y',yy-7);t.setAttribute('class',i===0?'t':'s');t.textContent=l;g.appendChild(t)});
    G(st).appendChild(g);grow(st,x,y,w,h)}
  function edge(st,x1,y1,x2,y2,cls){const p=document.createElementNS(NS,'path');const mx=(x1+x2)/2;
    p.setAttribute('d',`M${x1} ${y1} C${mx} ${y1} ${mx} ${y2} ${x2} ${y2}`);p.setAttribute('class','edge '+(cls||''));p.setAttribute('marker-end',cls==='never'?'url(#ahr)':'url(#ah)');G(st).appendChild(p);
    if(cls!=='never'){const L=p.getTotalLength()||600;p.dataset.len=L;p.style.strokeDasharray=L;p.style.strokeDashoffset=L}}
  // columns: sources 0-240, gate 288-508, extractor 556-796, validator 844-1084, store 1132-1332, surfaces 1380-1600 (48 px gaps)
  const SRC=['Slack','Docs','Will Can Must','Manager notes','AI sessions'];
  SRC.forEach((t,i)=>node(1,0,i*68,240,56,[t]));
  node(2,288,108,220,112,['Gate','allowlist','purpose lock'],'lime');
  node(3,556,108,240,112,['Extractor','Gemini 3.8 Flash']);
  node(3,844,108,240,112,['Validator','quote in source']);
  node(4,1132,116,200,96,['Receipts'],'lime');
  node(4,1132,252,200,56,['POST /api/ask'],'dark');
  const SUR=['Meet','Slack','Notion','Page'];
  SUR.forEach((t,i)=>node(5,1380,i*72,220,56,[t]));
  node(6,0,372,240,64,['DMs, private','never opened'],'never');
  node(6,1380,372,220,64,['Audit'],'never');
  SRC.forEach((t,i)=>edge(2,240,i*68+28,288,164));
  edge(3,508,164,556,164);edge(3,796,164,844,164);edge(4,1084,164,1132,164);edge(4,1232,212,1232,252);
  SUR.forEach((t,i)=>edge(5,1332,280,1380,i*72+28));
  edge(6,240,404,1380,404,'never');
  // the camera per stage: the centre of that stage's boxes, at 1.7; stage 6 pulls back to the whole pipeline
  CAMERA[s.id]={};[1,2,3,4,5].forEach(st=>{const b=bbox[st];CAMERA[s.id][st]=[OX+(b[0]+b[2])/2,OY+(b[1]+b[3])/2,1.7]});CAMERA[s.id][6]=[960,540,1];
  return {step(n,instant){let newest=0;Object.keys(groups).forEach(st=>{if(+st<=n)newest=Math.max(newest,+st)});
    Object.keys(groups).forEach(st=>{const on=+st<=n;const g=groups[st];g.classList.toggle('on',on);g.classList.toggle('past',on&&+st<newest);
      $$('.edge',g).forEach(p=>{if(p.dataset.len){if(instant||PRINT)p.style.transition='none';p.style.strokeDashoffset=on?0:p.dataset.len;if(instant||PRINT){void p.getBoundingClientRect();p.style.transition=''}}})})}}
};

/* 09 roadmap: the product's own map (d3, land-110m); Japan, the verticals, North America, each with its line; the camera follows */
HOOKS.map=function(s){
  const box=$('.map',s);const W=1600,H=520;const OX=160,OY=160+204; // canvas offset of the map
  if(typeof d3==='undefined'||!window.LAND110M){console.error('[deck] map: d3 or land data missing');return null}
  const svg=d3.select(box).insert('svg',':first-child').attr('viewBox',`0 0 ${W} ${H}`).attr('width',W).attr('height',H);
  const sc=W/(190*Math.PI/180);
  const proj=d3.geoEquirectangular().rotate([-175,0]).scale(sc).translate([W/2,52*Math.PI/180*sc]).clipExtent([[0,0],[W,H]]);
  const path=d3.geoPath(proj);
  svg.append('path').attr('class','land').attr('d',path(window.LAND110M));
  const g1=svg.append('g').attr('class','g'),g2=svg.append('g').attr('class','g'),g3=svg.append('g').attr('class','g');
  const jp=proj([139.69,35.69]),sf=proj([-122.42,37.77]),au=proj([-97.74,30.27]);
  const pj=g1.append('g').attr('transform',`translate(${jp[0]},${jp[1]})`);
  pj.append('circle').attr('class','disc').attr('r',18);
  pj.append('text').attr('class','nm').attr('x',30).attr('y',9).text('Japan');
  const pills=[['hospitals',900,300],['airlines',1060,370],['construction',940,440]];
  pills.forEach(([w,x,y])=>{g2.append('line').attr('class','leader').attr('x1',jp[0]).attr('y1',jp[1]).attr('x2',x).attr('y2',y);
    const wdt=w.length*13.5+40;const g=g2.append('g').attr('class','kw').attr('transform',`translate(${x},${y})`);
    g.append('rect').attr('x',-wdt/2).attr('y',-20).attr('width',wdt).attr('height',40).attr('rx',20);
    g.append('text').attr('text-anchor','middle').attr('dy','.35em').text(w)});
  const inter=d3.geoInterpolate([139.69,35.69],[-122.42,37.77]);const pts=d3.range(0,1.0001,1/64).map(inter);
  const arc=g3.append('path').attr('class','arc').attr('d',path({type:'LineString',coordinates:pts}));
  const L=arc.node().getTotalLength()||1200;arc.style('stroke-dasharray',L).style('stroke-dashoffset',L);
  [sf,au].forEach(pt=>g3.append('circle').attr('class','disc').attr('cx',pt[0]).attr('cy',pt[1]).attr('r',12));
  // the three lines are HTML overlays in the map (data-b 1..3); place them next to their targets
  const place=(sel,x,y)=>{const e=$(sel,box);if(e){e.style.left=x+'px';e.style.top=y+'px'}};
  place('.t1',jp[0]+150,jp[1]-70);place('.t2',430,330);place('.t3',1150,Math.max(au[1],sf[1])+40);
  CAMERA[s.id]={1:[OX+jp[0]+150,OY+jp[1],1.5],2:[OX+780,OY+390,1.5],3:[OX+1330,OY+au[1]+60,1.5],4:[960,540,1]};
  function pulse(){if(PRINT)return;const c=pj.append('circle').attr('class','pulse').attr('r',18).style('opacity',.9);c.transition().duration(900).ease(d3.easeCubicOut).attr('r',80).style('opacity',0).remove()}
  let last=0;
  return {step(n,instant){const newest=Math.min(3,n);
    [g1,g2,g3].forEach((g,i)=>{const st=i+1;g.classed('on',st<=n).classed('past',st<=n&&st<newest)});
    if(instant||PRINT)arc.style('transition','none');arc.style('stroke-dashoffset',n>=3?0:L);if(instant||PRINT){void arc.node().getBoundingClientRect();arc.style('transition',null)}
    if(n===1&&last<1&&!instant)pulse();last=n}}
};

/* A10 inspiration, alt: a fanned stack read from the top, resolving into receipts laid flat, each with its source line (p5) */
HOOKS.altpic=function(s){
  const box=$('.pic',s);const W=1600,H=380;
  const R=['#northwind-sync, 2026-05-06','#learning, 2026-07-15','#growth-analytics, 2026-04-18','#northwind-sync, 2026-05-27','#growth-analytics, 2026-06-11','#pricing, 2026-08-12','#all-hands-questions, 2026-06-25','Will Can Must sheet, 2026-03-15','#platform, 2026-04-22'];
  const N=R.length;let t1=0,t2=0,g1=0,g2=0,inst=null;
  new p5(p=>{
    p.setup=()=>{p.createCanvas(W,H);if(PRINT)p.pixelDensity(1);if(PRINT)p.noLoop()};
    p.draw=()=>{p.clear();p.background(250,250,250);
      if(PRINT){t1=g1;t2=g2}else{t1+=(g1-t1)*.08;t2+=(g2-t2)*.06;if(Math.abs(g1-t1)<.002)t1=g1;if(Math.abs(g2-t2)<.002)t2=g2}
      const e2=easeInOut(t2);
      txt(p,'FROM MEMORY',40,20,20,MUTE,1);if(e2>0)txt(p,'FROM RECEIPTS',830,20,20,MUTE,e2);
      for(let k=0;k<N;k++){const sx=300+k*7,sy=215-k*5,sr=(k-4)*.045,w=300,h=180;const top=k>=N-3;const dim=top?0:t1;
        p.push();p.translate(sx,sy);p.rotate(sr);
        p.drawingContext.shadowColor='rgba(0,0,0,.10)';p.drawingContext.shadowBlur=10;p.drawingContext.shadowOffsetY=3;
        if(top&&t1>0)p.stroke(INK[0],INK[1],INK[2],120*t1);else p.stroke(210,210,210,255*(1-.6*dim));p.strokeWeight(1);p.fill(255,255,255,255*(1-.7*dim));p.rect(-w/2,-h/2,w,h,10);p.drawingContext.shadowBlur=0;
        p.noStroke();p.fill(225,225,225,255*(1-.7*dim));for(let j=0;j<4;j++)p.rect(-w/2+20,-h/2+26+j*26,w-40-(j*37%80),10,4);
        if(top&&t1>0){p.fill(LIME[0],LIME[1],LIME[2],255*t1);p.rect(w/2-70,-h/2+14,52,22,11);txt(p,'read',w/2-44,-h/2+25,13,INK,t1,'center','middle')}
        p.pop()}
      if(e2>0)for(let k=0;k<N;k++){const sx=300+k*7,sy=215-k*5;const col=k%3,row=Math.floor(k/3);const fx=830+col*256+124,fy=68+row*112+40;
        const kk=Math.max(0,Math.min(1,(e2*1.4-k*.05)));const x=p.lerp(sx,fx,easeInOut(kk)),y=p.lerp(sy,fy,easeInOut(kk)),w=248,h=96,a=Math.min(1,kk*2);
        p.push();p.translate(x,y);
        p.drawingContext.shadowColor='rgba(0,0,0,.10)';p.drawingContext.shadowBlur=10;p.drawingContext.shadowOffsetY=3;
        p.stroke(HAIR[0],HAIR[1],HAIR[2],255*a);p.strokeWeight(1);p.fill(255,255,255,255*a);p.rect(-w/2,-h/2,w,h,10);p.drawingContext.shadowBlur=0;
        p.noStroke();p.fill(LIME[0],LIME[1],LIME[2],255*a);p.rect(-w/2,-h/2,6,h,3);
        p.fill(225,225,225,255*a);p.rect(-w/2+20,-h/2+16,w-44,9,4);p.rect(-w/2+20,-h/2+34,w-90,9,4);
        txt(p,R[k],-w/2+20,h/2-28,12,MUTE,a);
        p.pop()}};
    inst=p;
  },box);
  return {step(n,instant){g1=n>=1?1:0;g2=n>=2?1:0;if(instant||PRINT){t1=g1;t2=g2}if(PRINT&&inst)inst.redraw()}}
};

/* ---------------- boot ---------------- */
function boot(){
  if(PRINT){document.body.classList.add('print');
    slides.forEach((s,i)=>{init(s);apply(s,maxStep(s),true);const d=document.createElement('div');d.className='prog';d.textContent=label(i);s.appendChild(d)});
    return}
  fit();addEventListener('resize',fit);
  let start=0;const q=Q.get('slide')||(location.hash||'').replace('#','');if(q&&/^\d+$/.test(q))start=Math.max(0,Math.min(slides.length-1,+q-1));
  show(start,0,true);
  let buf='',bufT=0;
  addEventListener('keydown',e=>{if(e.metaKey||e.ctrlKey||e.altKey)return;const k=e.key;
    if(k==='ArrowRight'||k===' '||k==='PageDown'||k==='Enter'){e.preventDefault();next()}
    else if(k==='ArrowLeft'||k==='PageUp'||k==='Backspace'){e.preventDefault();prev()}
    else if(k==='Home'){show(0,0)}else if(k==='End'){show(slides.length-1,0)}
    else if(k==='n'||k==='N'){document.body.classList.toggle('shownotes')}
    else if(/^\d$/.test(k)){buf+=k;clearTimeout(bufT);bufT=setTimeout(()=>{let n=+buf;buf='';if(n===0)n=10;show(Math.min(mains.length,n)-1,0)},600)}});
  stage.addEventListener('click',e=>{if(e.target.closest('#drawer'))return;next()});
}
window.addEventListener('load',()=>{const F=document.fonts;const loads=F&&F.load?[F.load('400 20px "Geist Mono"'),F.load('400 32px Geist'),F.load('500 48px Geist'),F.load('600 72px Geist')]:[];
  Promise.all(loads).catch(e=>console.error('[deck] font load: '+e)).then(()=>F&&F.ready).then(()=>{boot();setTimeout(()=>{window.__deckReady=true},PRINT?700:0)})});
})();
