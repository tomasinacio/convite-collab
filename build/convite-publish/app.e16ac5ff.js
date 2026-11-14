(function(){
  var T = {
    'pt-PT': {seal:'Toca para abrir', skip:'Saltar', kicker:'TODO(user) · frase de abertura', join:'e', date:'10 de julho de 2027', card:'Convite', again:'Fechar e ver de novo'},
    'en':    {seal:'Tap to open', skip:'Skip', kicker:'TODO(user) · opening line', join:'and', date:'10 July 2027', card:'Invitation', again:'Close and replay'},
    'es':    {seal:'Toca para abrir', skip:'Saltar', kicker:'TODO(user) · frase de apertura', join:'y', date:'10 de julio de 2027', card:'Invitación', again:'Cerrar y repetir'}
  };
  var code = new URLSearchParams(location.search).get('lang') || 'pt-PT';
  if (!T[code]) code = 'pt-PT';
  var t = T[code];
  document.documentElement.lang = code;
  if (new URLSearchParams(location.search).get('sharp') === '1') document.documentElement.classList.add('sharp');
  document.querySelectorAll('[data-i18n]').forEach(function(el){ el.textContent = t[el.getAttribute('data-i18n')]; });

  var $ = function(s, r){ return (r || document).querySelector(s); }, $$ = function(s, r){ return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var page = $('#page'), sheet = $('#sheet'), seal = $('#seal'), skip = $('#skip'), names = $('#names'), light = $('#light');
  names.setAttribute('aria-label', t.card);
  var liteMotion = document.documentElement.classList.contains('lite-motion');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var timers = [];
  function later(fn, ms){ timers.push(setTimeout(fn, ms)); }

  /* the names, one span per letter: MAYA / e / TOMÁS (capitals by CSS, the copy stays as written) */
  $('.pen').innerHTML = ['Maya', t.join, 'Tomás'].map(function(line, li){
    return '<span class="l ' + (li === 1 ? 'join' : 'cap') + '">' + line.split('').map(function(c){
      return c === ' ' ? ' ' : '<span class="ch">' + c + '</span>';
    }).join('') + '</span>';
  }).join('');

  /* v14: the hero printed inside the letter (see .print): a copy of the names block, hidden from assistive technology */
  (function(){
    var c = names.cloneNode(true);
    c.removeAttribute('id'); c.removeAttribute('tabindex'); c.removeAttribute('aria-label');
    c.querySelectorAll('.glint, .vh').forEach(function(n){ n.remove(); });
    c.querySelectorAll('[id]').forEach(function(n){ n.removeAttribute('id'); });
    $('#print').appendChild(c);
  })();

  /* ---- the timeline, seconds from the tap [CH] one lead at a time; full table in V10-NOTES.md ----
     0 to .10 press; 0 the seal cracks, .06 to .42 twine and label go; .16 to 1.46 top fold + sheet; 1.04 to 2.20 bottom fold;
     1.70 to 2.50 the world comes up under the sheet (margins turn to paper, the sky widens); 2.20 to 2.90 the sheet dissolves;
     2.40 panel glaze; 2.55 opening line; 2.85 to 3.85 names by glyph advance (lift between lines); 3.95/4.07/4.15 date,
     place, village (uneven gaps, no metronome); 4.30 to 5.60 olive from its corner; 4.90/5.10 two tiny swallows; 5.40 left
     grass; 5.80 right grass; 6.30 bloom; 6.80 to 8.80 mist hills and land glaze together; 8.20 to 10.30 one swallow crosses;
     Skip fades at 10.0 on the animation clock; from 10.5 ambient only (cloud drift, a glint at 11.5 s, sway from 13 s, a rare
     bird every ~52 s from 18 s), continuous by the user's choice. */
  var NAMES_AT = 2.85, NAMES_END = 3.85, LIFT = .12;
  function timeNames(){
    var lines = $$('.pen .l'), total = 0, ws = [];
    lines.forEach(function(l){ $$('.ch', l).forEach(function(c){ var w = c.getBoundingClientRect().width || 10; ws.push(w); total += w; }); });
    var span = NAMES_END - NAMES_AT - .16 - LIFT * (lines.length - 1), x = 0, i = 0;
    lines.forEach(function(l, li){
      $$('.ch', l).forEach(function(c){
        c.style.setProperty('--d', (NAMES_AT + x / total * span + li * LIFT).toFixed(3) + 's');
        x += ws[i++];
      });
    });
  }

  /* ---- before the tap: measure the names once the fonts are in, and decode the screen-1 art while the letter waits,
     so the tap frame does no layout read and no image decode (the folds keep 60 fps) [AN] animation-performance ---- */
  /* static build: decode the closed front's art on its real URLs as soon as the script runs, so the letter's first paint
     and the tap frame do no decode (the files are preloaded by index.html) */
  (function(){ var cs = getComputedStyle(document.documentElement);
    ['--img-paper', '--img-closed-top', '--img-closed-bottom', '--img-closed-emboss', '--img-closed-deco', '--img-seal', '--img-linen', '--img-seal-top', '--img-seal-bottom'].forEach(function(v){
      var m = /url\(["']?([^"')]+)["']?\)/.exec(cs.getPropertyValue(v)); if (!m) return;
      var im = new Image(); im.onerror = function(){ document.documentElement.classList.add('art-failed'); };
      im.src = new URL(m[1], document.baseURI).href; if (im.decode) im.decode().catch(function(){}); }); })();
  var timed = false;
  function timeOnce(){ if (!timed) { timed = true; timeNames(); } }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(timeOnce);
  function warm(){ document.documentElement.classList.add('warm'); }
  /* frame-time probe: if the closed letter cannot hold 50 fps for 600 ms, take the lighter motion tier */
  if (!/[?&]motion=/.test(location.search) && !document.documentElement.classList.contains('lite-motion') && window.requestAnimationFrame) {
    addEventListener('load', function(){
      var f = [], t0 = 0;
      (function tick(t){ if (!t0) t0 = t; f.push(t); if (t - t0 < 600 && !page.classList.contains('opened')) requestAnimationFrame(tick); else {
        var g = []; for (var i = 1; i < f.length; i++) g.push(f[i] - f[i - 1]); g.sort(function(a, b){ return a - b; });
        if (g.length > 5 && g[Math.floor(g.length / 2)] > 20) document.documentElement.classList.add('lite-motion');
      } })(0);
    });
  }
  addEventListener('load', function(){
    warm();   // the letter (the poster) is up: now fetch the painted art while the guest looks at it
    (window.requestIdleCallback || setTimeout)(function(){
      /* v15 (critic 4): the observers (lazy art one screen ahead, the names leaving, the dogs, the loops in view) are made now,
         while the letter waits, so their first callbacks and the near art's decode happen before the tap */
      watch(); ambObserve();
      /* the seal halves and the flaps' faces too: they first show at the tap */
      $$('.world .art:not([data-lazy]), .world .in:not([data-lazy]), .sheet .half, .sheet .face, .mid-sky, .mid-sky i').forEach(function(el){
        var m = /url\("?([^")]+)"?\)/.exec(getComputedStyle(el).backgroundImage);
        if (m) { var im = new Image(); im.src = m[1]; if (im.decode) im.decode().catch(function(){}); }
      });
    });
  });

  /* ---- closed: the idle light from 2.5 s, stopped for good by the first touch or focus (CC 6.8) ---- */
  var lightT = reduce ? 0 : setTimeout(function(){ light.classList.add('on'); }, 2500);
  function stopLight(){ clearTimeout(lightT); light.classList.remove('on'); }
  document.addEventListener('pointerdown', stopLight, {once:true});
  seal.addEventListener('pointerdown', function(){ seal.classList.add('pressed'); });
  seal.addEventListener('focus', stopLight);

  /* ---- finishing: what still runs ends within 300 ms (Skip; the names block leaving the view, CC 4.11, 4.12).
     The ambient (cloud drift, the rare bird) is left alone: it is slow by design and never part of the reveal. ---- */
  /* the ambient: never hurried, paused while out of view */
  var AMBIENT = /^(drift|cross-rare|sweep|gust|sway|sw\d|leaf|glint|settle|breath|wag|tail|bob|soar)/;
  function hurry(anims){
    anims.forEach(function(a){
      if (AMBIENT.test(a.animationName || '')) return;
      var tg = a.effect && a.effect.target;
      if (tg && tg.closest && tg.closest('.dogs')) return;   /* the dogs come in when they are seen, not on the reveal clock */
      var ct = a.effect && a.effect.getComputedTiming(), left = ct ? ct.endTime - (a.currentTime || 0) : 0;
      if (isFinite(left) && left > 300) a.updatePlaybackRate(left / 300);
    });
  }

  /* ---- lower scenes: their image is applied one screen before they come into view (first load stays small) ---- */
  var near = null, leave = null, seenDogs = null, dogs = $('#dogs');
  function watch(){
    var lazies = $$('[data-lazy]');
    if (!('IntersectionObserver' in window)) { lazies.forEach(function(el){ el.classList.add('near'); }); return; }
    near = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('near'); near.unobserve(e.target); } }); }, {rootMargin:'100% 0px 100% 0px'});
    lazies.forEach(function(el){ near.observe(el); });
    leave = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.intersectionRatio < .05) hurry(page.getAnimations({subtree:true})); }); }, {threshold:[0, .05]});
    leave.observe(names);
    /* the dogs come in when a third of the group is in view */
    seenDogs = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('seen'); seenDogs.unobserve(e.target); } }); }, {threshold:.3});
    seenDogs.observe(dogs);
  }

  /* ---- open ---- */
  function open(){
    if (sheet.classList.contains('is-open')) return;
    stopLight(); seal.classList.add('pressed'); warm();
    page.classList.add('opened'); sheet.classList.add('is-open', 'crack');
    /* v15 (critic 4): the press and the crack own the tap frame; the reveal's ~120 animations are created two frames later */
    if (reduce) page.classList.add('go');
    else requestAnimationFrame(function(){ requestAnimationFrame(function(){ page.classList.add('go'); }); });
    timeOnce();
    seal.disabled = true;
    if (reduce) { sheet.classList.add('instant'); finish(true); return; }
    later(function(){ names.focus({preventScroll:true}); }, 3200);
    later(sweep, 7200);   /* after the reveal: pause the loops of every piece that is out of view */
    /* Skip leaves on the animation clock, not a timer, so it always matches the reveal it skips (a timer let it leave
       early whenever the animation clock ran slower than the wall clock, as in slowed captures): v14: held to 6.9 s, out by 7.0 s, as the reveal ends */
    skipExit = skip.animate([{opacity:1}, {opacity:1, offset:.98}, {opacity:0}], {duration:7000, fill:'forwards'});
    skipExit.finished.then(function(){ skip.classList.add('out'); skip.hidden = true; skipExit.cancel(); skipExit = null; }, function(){});
  }
  var skipExit = null;
  function finish(now){
    if (skipExit) { skipExit.cancel(); skipExit = null; }
    if (!sheet.classList.contains('is-open')) { sheet.classList.add('instant'); open(); }
    hurry(document.getAnimations());
    if (!near) watch();
    swept = false;    names.focus({preventScroll:true});
    timers.forEach(clearTimeout); timers = [];
    skip.classList.add('out');
    setTimeout(function(){ skip.hidden = true; }, now ? 0 : 300);
    setTimeout(sweep, 400);
  }

  /* ---- ambient control: each ambient animation runs only while its element is in view (battery) ---- */
  var seen = new Map(), amb = null, AMB_SEL = '.amb, .glint, .dogs';
  /* v15 (critic 4): no checkpoints, no forced style flushes during the reveal. The loops start themselves from rest when their
     piece lands (CSS delays); the lite tier's loops all start at 7 s (CSS). One IntersectionObserver, made while the letter
     waits, records what is in view; after the reveal (7.2 s, or Skip) a single sweep pauses the loops of pieces out of view,
     and from then on only a change of view pauses or resumes a piece. */
  function apply(el){
    var out = seen.get(el) === false;
    el.getAnimations({subtree:true}).forEach(function(a){
      if (!AMBIENT.test(a.animationName || '')) return;
      if (out) { if (a.playState === 'running') a.pause(); }
      else if (a.playState === 'paused') a.play();
    });
  }
  var swept = false;
  function sweep(){ swept = true; seen.forEach(function(v, el){ if (v === false) apply(el); }); }
  function ambObserve(){
    if (reduce || amb || !('IntersectionObserver' in window)) return;
    amb = new IntersectionObserver(function(es){ es.forEach(function(e){
      var was = seen.get(e.target); seen.set(e.target, e.isIntersecting);
      if (swept && was !== e.isIntersecting) apply(e.target);
    }); });
    $$(AMB_SEL).forEach(function(el){ amb.observe(el); });
  }
  /* the falling leaf varies a little at every fall: where it starts and how wide it sways */
  var leaf = $('#leaf');
  if (leaf) leaf.addEventListener('animationiteration', function(e){
    if (e.animationName !== 'leaf-fall') return;
    leaf.style.left = 'calc(var(--u) * ' + (3.5 + Math.random() * 2).toFixed(2) + ')';
    leaf.style.setProperty('--sa', (2.2 + Math.random() * 1.4).toFixed(2));
  });
  seal.addEventListener('click', function(){ open(); });
  skip.addEventListener('click', function(){ finish(false); });

  /* prototype only: close and replay */
  $('#again').addEventListener('click', function(){
    timers.forEach(clearTimeout); timers = [];
    dogs.classList.remove('seen');
    if (seenDogs) seenDogs.observe(dogs);
    window.scrollTo(0, 0);
    sheet.classList.add('instant');
    sheet.classList.remove('is-open', 'crack'); page.classList.remove('opened', 'go');
    seal.classList.remove('pressed'); seal.disabled = false;
    skip.hidden = false; skip.classList.remove('out');
    if (skipExit) { skipExit.cancel(); skipExit = null; }
    seal.focus({preventScroll:true});
    requestAnimationFrame(function(){ requestAnimationFrame(function(){ sheet.classList.remove('instant'); }); });
  });
})();
