/* Pik deck: navigation, keypress builds, the animated pieces, print mode.
   Keys: Right / Space = next build step, then next slide. Left = back. Home / End. Digits jump (two digits within 0.6 s).
   N = speaker notes. Click anywhere = next step (the video plays on click instead). ?slide=N opens a slide. ?print=1 stacks every
   slide in its final state for the PDF. Everything runs from file:// with no network: fonts, d3, p5 and the land data are vendored. */
(function(){
'use strict';
const Q=new URLSearchParams(location.search);
const PRINT=Q.get('print')==='1';
const $=(s,r)=> (r||document).querySelector(s);
const $$=(s,r)=> Array.from((r||document).querySelectorAll(s));
const stage=$('#stage');
const slides=$$('.slide');
const mains=slides.filter(s=>s.classList.contains('main'));
const appx=slides.filter(s=>s.classList.contains('appx'));
const HOOKS={};           // name -> factory(el, slide) -> {step(n, instant), leave()}
const live={};            // slide id -> [hook instances]
const LIME=[214,242,90], LIME_DEEP=[191,224,48], INK=[23,23,23], BODY=[77,77,77], MUTE=[136,136,136], HAIR=[235,235,235];
const easeOut=t=>1-Math.pow(1-t,3);
const easeInOut=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
function txt(p,str,x,y,size,rgb,alpha,align,base){const c=p.drawingContext;c.save();c.font=size+'px "Geist Mono"';c.fillStyle='rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+','+alpha+')';c.textAlign=align||'left';c.textBaseline=base||'top';c.fillText(str,x,y);c.restore()}
function measure(p,str,size){const c=p.drawingContext;c.save();c.font=size+'px "Geist Mono"';const w=c.measureText(str).width;c.restore();return w}

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
function apply(s,n,instant){$$('[data-b]',s).forEach(e=>e.classList.toggle('on',+e.dataset.b<=n));(live[s.id]||[]).forEach(h=>{if(h.step)h.step(n,!!instant)})}

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

/* 02 problem: five role discs dissolve into one blob (p5) */
HOOKS.roles=function(el){
  const W=420,H=416,cx=210,cy=196;
  const roles=[['HR planner',92,74],['Engineer',330,64],['Designer',214,178],['Product manager',84,318],['Sales',338,330]];
  let t=0,target=0,inst=null,tm=0;
  const sk=new p5(p=>{
    p.setup=()=>{p.createCanvas(W,H);if(PRINT)p.pixelDensity(1);p.noiseSeed(11);if(PRINT)p.noLoop()};
    p.draw=()=>{p.clear();tm+=0.01;
      if(PRINT)t=target;else t+=(target-t)*0.045;if(Math.abs(target-t)<.002)t=target;
      const e=easeInOut(t);
      // the blob first (under the discs) so the discs sink into it
      const ba=Math.max(0,(t-.45)/.55);
      if(ba>0){p.push();p.noStroke();p.fill(LIME[0],LIME[1],LIME[2],255*ba);p.beginShape();const N=40;
        for(let i=0;i<N+3;i++){const a=(i%N)/N*p.TWO_PI;const r=(58+ba*20)*(1+.14*(p.noise(1.6*Math.cos(a)+4,1.6*Math.sin(a)+4,PRINT?.3:tm)-.5)*2);p.curveVertex(cx+r*Math.cos(a),cy+r*Math.sin(a))}
        p.endShape();p.pop();
        txt(p,'one task force, per task',cx,cy+96,20,INK,ba,'center','top')}
      roles.forEach(([name,x0,y0])=>{const x=p.lerp(x0,cx,e),y=p.lerp(y0,cy,e);const r=30*(1-.9*e);const la=1-Math.min(1,t*1.6);const da=1-Math.max(0,(t-.7)/.3);
        p.push();p.drawingContext.shadowColor='rgba(0,0,0,.08)';p.drawingContext.shadowBlur=8;p.drawingContext.shadowOffsetY=2;
        const fc=p.lerpColor(p.color(255),p.color(LIME[0],LIME[1],LIME[2]),Math.min(1,t*1.4));fc.setAlpha(255*da);p.stroke(HAIR[0],HAIR[1],HAIR[2],255*da);p.strokeWeight(1);p.fill(fc);if(da>0)p.circle(x,y,r*2);p.pop();
        if(la>0)txt(p,name,x,y+r+10,20,BODY,la,'center','top')});
    };
    inst=p;
  },el);
  return {step(n,instant){target=n>=1?1:0;if(instant||PRINT)t=target;if(PRINT&&inst)inst.redraw()}}
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

/* 06 impact: the number counts up once; the rings grow on their step (CSS) */
HOOKS.impact=function(s){
  const num=$('.num',s);const val=+num.dataset.value,dec=+num.dataset.decimals||0,suf=num.dataset.suffix||'';
  const fmt=x=>x.toFixed(dec)+suf;let done=false,raf=0;
  return {step(n,instant){
    if(n>=1){if(done)return;done=true;if(instant||PRINT){num.textContent=fmt(val);return}
      const t0=performance.now(),D=1200;cancelAnimationFrame(raf);
      const tick=now=>{const k=Math.min(1,(now-t0)/D);num.textContent=fmt(val*easeOut(k));if(k<1)raf=requestAnimationFrame(tick)};raf=requestAnimationFrame(tick)}
    else{done=false;cancelAnimationFrame(raf);num.textContent=fmt(0)}}}
};

/* 08 technical: the pipeline as SVG, drawn stage by stage */
HOOKS.arch=function(s){
  const box=$('.arch',s);const NS='http://www.w3.org/2000/svg';
  const svg=document.createElementNS(NS,'svg');svg.setAttribute('viewBox','0 0 1664 456');box.appendChild(svg);
  const defs=document.createElementNS(NS,'defs');defs.innerHTML='<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#888888"/></marker><marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#ee0000"/></marker>';svg.appendChild(defs);
  const groups={};const G=st=>{if(!groups[st]){const g=document.createElementNS(NS,'g');g.setAttribute('class','g');g.dataset.stage=st;svg.appendChild(g);groups[st]=g}return groups[st]};
  function node(st,x,y,w,h,lines,cls){const g=document.createElementNS(NS,'g');g.setAttribute('class','node '+(cls||''));
    const r=document.createElementNS(NS,'rect');r.setAttribute('x',x);r.setAttribute('y',y);r.setAttribute('width',w);r.setAttribute('height',h);r.setAttribute('rx',12);g.appendChild(r);
    const lh=[28,21,21];const total=lines.reduce((a,l,i)=>a+lh[Math.min(i,2)],0);let yy=y+h/2-total/2;
    lines.forEach((l,i)=>{const t=document.createElementNS(NS,'text');t.setAttribute('x',x+w/2);t.setAttribute('text-anchor','middle');const size=lh[Math.min(i,2)];yy+=size;t.setAttribute('y',yy-6);t.setAttribute('class',i===0?'t':'s');t.textContent=l;g.appendChild(t)});
    G(st).appendChild(g)}
  function edge(st,x1,y1,x2,y2,cls){const p=document.createElementNS(NS,'path');const mx=(x1+x2)/2;
    p.setAttribute('d',`M${x1} ${y1} C${mx} ${y1} ${mx} ${y2} ${x2} ${y2}`);p.setAttribute('class','edge '+(cls||''));p.setAttribute('marker-end',cls==='never'?'url(#ahr)':'url(#ah)');G(st).appendChild(p);
    if(cls!=='never'){const L=p.getTotalLength()||600;p.dataset.len=L;p.style.strokeDasharray=L;p.style.strokeDashoffset=L}}
  // columns: sources 0-250, gate 300-530, extractor 580-850, validator 900-1190, store 1240-1440, surfaces 1464-1664
  const SRC=['Public Slack channels','Shared documents','Will Can Must sheets','Manager notes','Opted-in AI sessions'];
  SRC.forEach((t,i)=>node(1,0,i*66,250,54,[t]));
  node(1,0,380,250,70,['DMs, private channels','never opened'],'never');
  node(2,300,96,230,136,['Policy gate','allowlist','purpose lock','opt-in'],'lime');
  node(3,580,104,270,120,['Extractor','Gemini 3.8 Flash','claim = source id + quote']);
  node(3,900,104,290,120,['Validator','quote found in the source?','else dropped and counted']);
  node(4,1240,104,200,120,['Receipt store','claims and drops','notes'],'lime');
  node(4,1240,268,200,60,['POST /api/ask'],'dark');
  const SUR=[['Meet listener','Gemini 3.8 Live'],['Slack bot'],['Notion watcher'],['The page','evaluator view','subject view']];
  SUR.forEach((l,i)=>node(5,1464,i*92,200,80,l));
  node(6,1464,380,200,70,['Audit','from a manifest'],'never');
  // edges, in the stage of the node they point to
  SRC.forEach((t,i)=>edge(2,250,i*66+27,300,164));
  edge(3,530,164,580,164);edge(3,850,164,900,164);edge(4,1190,164,1240,164);edge(4,1340,224,1340,268);
  SUR.forEach((l,i)=>edge(5,1440,298,1464,i*92+40));
  edge(6,250,415,1464,415,'never');
  const lab=document.createElementNS(NS,'text');lab.setAttribute('x',0);lab.setAttribute('y',366);lab.setAttribute('class','lab');lab.textContent='never read';G(1).appendChild(lab);
  return {step(n,instant){Object.keys(groups).forEach(st=>{const on=+st<=n;const g=groups[st];g.classList.toggle('on',on);
      $$('.edge',g).forEach(p=>{if(p.dataset.len){if(instant||PRINT)p.style.transition='none';p.style.strokeDashoffset=on?0:p.dataset.len;if(instant||PRINT){void p.getBoundingClientRect();p.style.transition=''}}})})}}
};

/* 09 roadmap: the product's own map (d3, land-110m), Japan, then the verticals, then North America */
HOOKS.map=function(s){
  const box=$('.map',s);const W=1092,H=560;
  if(typeof d3==='undefined'||!window.LAND110M){console.error('[deck] map: d3 or land data missing');return null}
  const svg=d3.select(box).append('svg').attr('viewBox',`0 0 ${W} ${H}`).attr('width',W).attr('height',H);
  const sc=W/(190*Math.PI/180);
  const proj=d3.geoEquirectangular().rotate([-175,0]).scale(sc).translate([W/2,62*Math.PI/180*sc]).clipExtent([[0,0],[W,H]]);
  const path=d3.geoPath(proj);
  svg.append('path').attr('class','land').attr('d',path(window.LAND110M));
  const g1=svg.append('g').attr('class','g'),g2=svg.append('g').attr('class','g'),g3=svg.append('g').attr('class','g');
  const jp=proj([139.69,35.69]),sf=proj([-122.42,37.77]),au=proj([-97.74,30.27]);
  // Japan
  const pj=g1.append('g').attr('transform',`translate(${jp[0]},${jp[1]})`);
  pj.append('circle').attr('class','disc').attr('r',16);
  pj.append('text').attr('class','nm').attr('x',28).attr('y',-2).text('Japan');
  pj.append('text').attr('class','rl').attr('x',28).attr('y',22).text('one HR team, one decision type');
  // the verticals, as the product's keyword pills, in the open Pacific
  const pills=[['hospitals',560,262],['airlines',700,336],['construction',600,416]];
  pills.forEach(([w,x,y])=>{g2.append('line').attr('class','leader').attr('x1',jp[0]).attr('y1',jp[1]).attr('x2',x).attr('y2',y);
    const wdt=w.length*13.2+36;const g=g2.append('g').attr('class','kw').attr('transform',`translate(${x},${y})`);
    g.append('rect').attr('x',-wdt/2).attr('y',-18).attr('width',wdt).attr('height',36).attr('rx',18);
    g.append('text').attr('text-anchor','middle').attr('dy','.35em').text(w)});
  // North America and the arc
  const inter=d3.geoInterpolate([139.69,35.69],[-122.42,37.77]);const pts=d3.range(0,1.0001,1/64).map(inter);
  const arc=g3.append('path').attr('class','arc').attr('d',path({type:'LineString',coordinates:pts}));
  const L=arc.node().getTotalLength()||1200;arc.style('stroke-dasharray',L).style('stroke-dashoffset',L);
  [sf,au].forEach(pt=>g3.append('circle').attr('class','disc').attr('cx',pt[0]).attr('cy',pt[1]).attr('r',11));
  g3.append('text').attr('class','nm').attr('x',au[0]+16).attr('y',au[1]+40).attr('text-anchor','end').text('North America');
  g3.append('text').attr('class','rl').attr('x',au[0]+16).attr('y',au[1]+64).attr('text-anchor','end').text('Indeed, Glassdoor');
  function pulse(){if(PRINT)return;const c=pj.append('circle').attr('class','pulse').attr('r',16).style('opacity',.9);c.transition().duration(900).ease(d3.easeCubicOut).attr('r',70).style('opacity',0).remove()}
  let last=0;
  return {step(n,instant){g1.classed('on',n>=1);g2.classed('on',n>=2);g3.classed('on',n>=3);
    if(instant||PRINT)arc.style('transition','none');arc.style('stroke-dashoffset',n>=3?0:L);if(instant||PRINT){void arc.node().getBoundingClientRect();arc.style('transition',null)}
    if(n===1&&last<1&&!instant)pulse();last=n}}
};

/* A10 inspiration, alt: a fanned stack read from the top, resolving into receipts laid out flat (p5) */
HOOKS.altpic=function(s){
  const box=$('.pic',s);const W=1664,H=460;
  const R=[["I can take the notes. I'll write them in English and post the same day.",'Slack #northwind-sync, 2026-05-06'],
    ["Six weeks of practice done. Ran today's Northwind sync in English myself for the first time.",'Slack #learning, 2026-07-15'],
    ['@juniors: office hours Thursday 4pm for SQL window functions, bring your queries.','Slack #growth-analytics, 2026-04-18'],
    ['Notes posted. I also drafted a comparison of our experiment registry vs theirs.','Slack #northwind-sync, 2026-05-27'],
    ['FY26 dashboard v1 is live. Thanks to the two juniors who built half of it.','Slack #growth-analytics, 2026-06-11'],
    ["Actually I'm back on the 19th, I'll take it so nobody has to reshuffle.",'Slack #pricing, 2026-08-12'],
    ['Agree with Kei that we should measure before we reorganize.','Slack #all-hands-questions, 2026-06-25'],
    ['Lead the Tokyo pricing analytics team next year and build the junior analyst program.','Will Can Must sheet, 2026-03-15'],
    ["I'm on call this weekend. Escalate anything customer-facing straight to me.",'Slack #platform, 2026-04-22']];
  const N=R.length;let t1=0,t2=0,g1=0,g2=0,inst=null;
  function wrap(p,str,maxw,size){const words=str.split(' ');const lines=[];let cur='';words.forEach(w=>{const test=cur?cur+' '+w:w;if(measure(p,test,size)>maxw&&cur){lines.push(cur);cur=w}else cur=test});if(cur)lines.push(cur);return lines}
  const sk=new p5(p=>{
    p.setup=()=>{p.createCanvas(W,H);if(PRINT)p.pixelDensity(1);if(PRINT)p.noLoop()};
    p.draw=()=>{p.clear();p.background(250,250,250);
      if(PRINT){t1=g1;t2=g2}else{t1+=(g1-t1)*.08;t2+=(g2-t2)*.06;if(Math.abs(g1-t1)<.002)t1=g1;if(Math.abs(g2-t2)<.002)t2=g2}
      const e2=easeInOut(t2);
      // headings
      txt(p,'FROM MEMORY: READ IN THE ORDER THEY COME TO MIND',32,24,22,MUTE,1);if(e2>0)txt(p,'FROM RECEIPTS: EVERY LINE WITH ITS SOURCE',860,24,22,MUTE,e2);
      // the stack, always there: the three sheets on top get read, the rest fade while reading from memory
      for(let k=0;k<N;k++){const sx=300+k*7,sy=290-k*6,sr=(k-4)*.045,w=300,h=180;const top=k>=N-3;const dim=top?0:t1;
        p.push();p.translate(sx,sy);p.rotate(sr);
        p.drawingContext.shadowColor='rgba(0,0,0,.10)';p.drawingContext.shadowBlur=10;p.drawingContext.shadowOffsetY=3;
        if(top&&t1>0)p.stroke(INK[0],INK[1],INK[2],120*t1);else p.stroke(210,210,210,255*(1-.6*dim));p.strokeWeight(1);p.fill(255,255,255,255*(1-.7*dim));p.rect(-w/2,-h/2,w,h,10);p.drawingContext.shadowBlur=0;
        p.noStroke();p.fill(225,225,225,255*(1-.7*dim));for(let j=0;j<4;j++)p.rect(-w/2+20,-h/2+26+j*26,w-40-(j*37%80),10,4);
        if(top&&t1>0){p.fill(LIME[0],LIME[1],LIME[2],255*t1);p.rect(w/2-70,-h/2+14,52,22,11);txt(p,'read',w/2-44,-h/2+25,13,INK,t1,'center','middle')}
        p.pop()}
      // the receipts: each one leaves the stack and lands flat, with its source line
      if(e2>0)for(let k=0;k<N;k++){const sx=300+k*7,sy=290-k*6;const col=k%3,row=Math.floor(k/3);const fx=890+col*262+120,fy=90+row*122+42;
        const kk=Math.max(0,Math.min(1,(e2*1.4-k*.05)));const x=p.lerp(sx,fx,easeInOut(kk)),y=p.lerp(sy,fy,easeInOut(kk)),w=248,h=112,a=Math.min(1,kk*2);
        p.push();p.translate(x,y);
        p.drawingContext.shadowColor='rgba(0,0,0,.10)';p.drawingContext.shadowBlur=10;p.drawingContext.shadowOffsetY=3;
        p.stroke(HAIR[0],HAIR[1],HAIR[2],255*a);p.strokeWeight(1);p.fill(255,255,255,255*a);p.rect(-w/2,-h/2,w,h,10);p.drawingContext.shadowBlur=0;
        p.noStroke();p.fill(LIME[0],LIME[1],LIME[2],255*a);p.rect(-w/2,-h/2,6,h,3);
        const lines=wrap(p,'“'+R[k][0]+'”',w-40,12).slice(0,4);lines.forEach((l,j)=>txt(p,l,-w/2+20,-h/2+12+j*15,12,INK,a));
        txt(p,R[k][1].replace(/^Slack /,''),-w/2+20,h/2-22,11,MUTE,a);
        p.pop()}
    };
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
window.addEventListener('load',()=>{const F=document.fonts;const loads=F&&F.load?[F.load('400 22px "Geist Mono"'),F.load('400 28px Geist'),F.load('500 44px Geist'),F.load('600 80px Geist')]:[];
  Promise.all(loads).catch(e=>console.error('[deck] font load: '+e)).then(()=>F&&F.ready).then(()=>{boot();setTimeout(()=>{window.__deckReady=true},PRINT?700:0)})});
})();
