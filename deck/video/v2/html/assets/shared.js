/* Pik V2 beats: tiny deterministic-animation helpers. Every beat defines window.seek(ms) with these.
   No timers, no CSS transitions: seek(ms) computes the whole scene from ms. */
window.PIK = (function () {
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const easeOut = t => 1 - Math.pow(1 - t, 3);              // entrances
  const easeInOut = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;  // moves
  const easeIn = t => t * t * t;                             // exits
  const linear = t => t;
  // progress 0..1 of a segment starting at `start` lasting `dur`
  const seg = (ms, start, dur, ease = easeOut) => ease(clamp((ms - start) / dur));
  const lerp = (a, b, t) => a + (b - a) * t;
  // typewriter: characters of `text` visible at ms, given start and chars-per-second
  const typed = (text, ms, start, cps = 28) => text.slice(0, Math.max(0, Math.floor((ms - start) / 1000 * cps)));
  // apply a typewriter to an element with an optional caret
  const type = (el, text, ms, start, cps = 28, caretEl = null) => {
    const shown = typed(text, ms, start, cps);
    if (el.textContent !== shown) el.textContent = shown;
    if (caretEl) {
      const done = shown.length >= text.length;
      const on = ms >= start && (!done || ((ms - start) % 1000) < 500);
      caretEl.classList.toggle('on', on);
    }
    return shown.length >= text.length;
  };
  // inline the mascot: the screen's mark (index.html #pikmark) in the video's 200x260 box. opts.disc draws the lime disc
  // behind it (the screen's avatar). Returns the <svg> element inserted into host. Antenna root stays at (96,84).
  const pikbot = (host, size = 200, opts = {}) => {
    const w = size, h = size * 1.3;
    const disc = opts.disc ? `<circle class="pk-disc" cx="100" cy="150" r="118" fill="#D6F25A"/>` : '';
    host.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 260" width="${w}" height="${h}" style="display:block;overflow:visible">
  ${disc}<g class="pk-root" style="transform-origin:100px 244px">
    <path class="pk-antenna" d="M96 84 C 96 46, 134 46, 134 72" fill="none" stroke="#171717" stroke-width="14" stroke-linecap="round" style="transform-origin:96px 84px"/>
    <ellipse class="pk-body" cx="100" cy="166" rx="70" ry="78" fill="#171717"/>
    <g class="pk-eyes" fill="#D6F25A" style="transform-origin:100px 160px">
      <rect x="74" y="140" width="17" height="39" rx="8.5"/>
      <rect x="109" y="140" width="17" height="39" rx="8.5"/>
    </g>
  </g></svg>`;
    return host.firstElementChild;
  };
  // blink: eyes scaleY 1 -> 0.08 -> 1 over ~180 ms starting at `at`
  const blink = (svg, ms, at, dur = 180) => {
    const t = clamp((ms - at) / dur);
    const s = t <= 0 || t >= 1 ? 1 : 0.08 + 0.92 * Math.abs(t * 2 - 1);
    svg.querySelector('.pk-eyes').style.transform = `scaleY(${s})`;
  };
  // antenna spring: a damped wobble starting at `at` for `dur`
  const spring = (svg, ms, at, dur = 900, amp = 22) => {
    const t = clamp((ms - at) / dur);
    const a = t <= 0 || t >= 1 ? 0 : amp * Math.sin(t * Math.PI * 5) * (1 - t) * (1 - t);
    svg.querySelector('.pk-antenna').style.transform = `rotate(${a}deg)`;
  };
  // hop: a single jump (y offset in px, squash on landing) starting at `at`
  const hop = (svg, ms, at, dur = 520, height = 70) => {
    const t = clamp((ms - at) / dur);
    const y = t <= 0 || t >= 1 ? 0 : -height * Math.sin(t * Math.PI);
    let sy = 1, sx = 1;
    if (t > 0 && t < .12) { sy = 1 - .12 * (1 - t / .12); sx = 1 + .08 * (1 - t / .12); }
    if (t > .88 && t < 1) { const u = (t - .88) / .12; sy = 1 - .12 * Math.sin(u * Math.PI); sx = 1 + .08 * Math.sin(u * Math.PI); }
    svg.querySelector('.pk-root').style.transform = `translateY(${y}px) scale(${sx},${sy})`;
  };
  // wire ?t= and expose
  const init = (seek, duration) => {
    window.seek = seek; window.DURATION_MS = duration;
    document.fonts && document.fonts.ready.then(() => {
      const t = new URLSearchParams(location.search).get('t');
      seek(t ? +t : 0);
      window.__ready = true;
    });
    // synchronous first paint too, so a screenshot before fonts.ready still shows the right frame
    const t = new URLSearchParams(location.search).get('t'); seek(t ? +t : 0);
  };
  return { clamp, easeOut, easeInOut, easeIn, linear, seg, lerp, typed, type, pikbot, blink, spring, hop, init };
})();
