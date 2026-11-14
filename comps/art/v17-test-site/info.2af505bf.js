/* Information sections (v16): language, countdown, calendar file, copy IBAN, and the prop hooks. Runs only when the page
   was built with the RSVP on. The sections are plain HTML: without JavaScript they show (except the countdown).
   FAKE: every guest-facing sentence in T is placeholder wording; the couple replaces it (rsvp/comps/REPLACE-ME.md). */
(function () {
  'use strict';
  var root = document.documentElement, wrap = document.getElementById('info-wrap');
  if (!wrap) return;
  var $ = function (id) { return document.getElementById(id); };

  /* FAKE: all wording below (three languages). Real and kept: the times (the user, 2026-11-12), the address, the IBAN. */
  var T = {
    'pt-PT': { whereH:'Como chegar', maps:'Abrir no mapa', cal:'Juntar ao calendário',
      countKick:'Contagem decrescente', countH:'Faltam', days:['dia','dias'], hours:['hora','horas'], minutes:['minuto','minutos'],
      dayKick:'O dia', dayH:'Programa', s1:'Chegada dos convidados', s2:'Cerimónia', s3:'Cocktail', s4:'Jantar', s5:'Corte do bolo', s6t:'Depois', s6:'Festa',
      dressKick:'O que vestir', dressH:'Traje formal', dressText:'Escolham o vosso melhor, com sapatos para dançar: a festa vai noite fora.',
      giftKick:'Se quiserem', giftH:'Prendas', giftText:'A vossa presença é o melhor presente. Se quiserem deixar-nos uma prenda, uma ajuda para começarmos a nossa vida a dois será recebida com muito carinho.',
      copy:'Copiar IBAN', copied:'IBAN copiado. Já o podem colar na app do banco.', copyFail:'Não foi possível copiar. Toquem no número para o selecionar.',
      faqKick:'Perguntas frequentes', faqH:'Antes do dia',
      q1:'Há estacionamento?', a1:'Sim, há estacionamento na quinta.',
      q2:'Podemos levar acompanhantes ou crianças?', a2:'O vosso link pessoal já diz quantos lugares guardámos para vós. Se tiverem dúvidas, falem connosco.',
      q3:'Como vai estar o tempo?', a3:'Os dias costumam ser quentes e as noites frescas. Tragam um casaco leve para depois do jantar.',
      icsTitle:'Casamento de Maya e Tomás' },
    en: { whereH:'Finding us', maps:'Open in Maps', cal:'Add to calendar',
      countKick:'Counting down', countH:'Not long now', days:['day','days'], hours:['hour','hours'], minutes:['minute','minutes'],
      dayKick:'The day', dayH:'Order of the day', s1:'Guests arrive', s2:'Ceremony', s3:'Cocktails', s4:'Dinner', s5:'Cutting the cake', s6t:'Then', s6:'Dancing',
      dressKick:'What to wear', dressH:'Formal attire', dressText:'Wear your finest, with shoes to dance in: the party runs late.',
      giftKick:'If you wish', giftH:'Gifts', giftText:'Having you with us is the best gift. If you would like to give us something, a contribution towards our life together will be received with much love.',
      copy:'Copy IBAN', copied:'IBAN copied. You can paste it in your banking app.', copyFail:'Could not copy. Tap the number to select it.',
      faqKick:'Questions', faqH:'Before the day',
      q1:'Is there parking?', a1:'Yes, there is parking at the venue.',
      q2:'Can we bring a partner or children?', a2:'Your personal link already shows how many seats we have kept for you. If in doubt, just ask us.',
      q3:'What will the weather be like?', a3:'The days are usually hot and the nights cool. Bring a light jacket for after dinner.',
      icsTitle:'Maya and Tomás’s wedding' },
    es: { whereH:'Cómo llegar', maps:'Abrir en el mapa', cal:'Añadir al calendario',
      countKick:'Cuenta atrás', countH:'Faltan', days:['día','días'], hours:['hora','horas'], minutes:['minuto','minutos'],
      dayKick:'El día', dayH:'Programa', s1:'Llegada de los invitados', s2:'Ceremonia', s3:'Cóctel', s4:'Cena', s5:'Corte de la tarta', s6t:'Después', s6:'Fiesta',
      dressKick:'Qué ponerse', dressH:'Etiqueta formal', dressText:'Vestid vuestras mejores galas, con zapatos para bailar: la fiesta acaba tarde.',
      giftKick:'Si queréis', giftH:'Regalos', giftText:'Vuestra presencia es el mejor regalo. Si queréis hacernos un regalo, una ayuda para empezar nuestra vida juntos será recibida con mucho cariño.',
      copy:'Copiar IBAN', copied:'IBAN copiado. Ya podéis pegarlo en la app del banco.', copyFail:'No se pudo copiar. Tocad el número para seleccionarlo.',
      faqKick:'Preguntas frecuentes', faqH:'Antes del día',
      q1:'¿Hay aparcamiento?', a1:'Sí, hay aparcamiento en la finca.',
      q2:'¿Podemos llevar acompañantes o niños?', a2:'Vuestro enlace personal ya indica cuántas plazas hemos guardado para vosotros. Si tenéis dudas, escribidnos.',
      q3:'¿Qué tiempo hará?', a3:'Los días suelen ser calurosos y las noches frescas. Traed una chaqueta ligera para después de la cena.',
      icsTitle:'Boda de Maya y Tomás' }
  };
  var t = T['pt-PT'];
  function setLang(code) {
    t = T[code] || T['pt-PT'];
    Array.prototype.forEach.call(wrap.querySelectorAll('[data-it]'), function (el) {
      var v = t[el.getAttribute('data-it')];
      if (typeof v === 'string') el.textContent = v;
    });
    tick(); calendar();
  }

  /* ---- countdown: whole minutes to the guests' arrival, 15:00 in Lisbon on the day (14:00 UTC, summer time) ---- */
  var START = Date.UTC(2027, 6, 10, 14, 0, 0);
  var timer = 0;
  function put(id, n, pair) { $('i-' + id).textContent = String(n); $('i-' + id + 'u').textContent = pair[n === 1 ? 0 : 1]; }
  function tick() {
    var ms = Math.max(0, START - Date.now()), m = Math.floor(ms / 60000);
    put('d', Math.floor(m / 1440), t.days); put('h', Math.floor(m / 60) % 24, t.hours); put('m', m % 60, t.minutes);
  }
  function startClock() { if (!timer) { tick(); timer = setInterval(tick, 20000); } }

  /* ---- calendar: a small .ics made here, so it works offline and needs no outside service ---- */
  function esc(s) { return s.replace(/([\\,;])/g, '\\$1'); }
  function calendar() {
    var a = $('i-cal'); if (!a) return;
    var lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//convite//PT', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH', 'BEGIN:VEVENT',
      'UID:casamento-20270710@convite', 'DTSTAMP:20261112T120000Z',
      'DTSTART:20270710T140000Z',      /* 15:00 in Lisbon: the guests arrive (the user, 2026-11-12) */
      'DTEND:20270711T020000Z',        /* FAKE: 03:00 in Lisbon; the end of the party is not known */
      'SUMMARY:' + esc(t.icsTitle),
      'LOCATION:' + esc('Quinta do Grilo, R. Vale de São Gião, 2665-382 Milharado, Portugal'),
      'URL:https://maps.app.goo.gl/7gWufo1vMswyDxfbA?g_st=ac',
      'END:VEVENT', 'END:VCALENDAR'];
    if (!window.Blob || !window.URL || !URL.createObjectURL) return;   /* the button stays hidden */
    if (a.getAttribute('data-url')) URL.revokeObjectURL(a.getAttribute('data-url'));
    var u = URL.createObjectURL(new Blob([lines.join('\r\n') + '\r\n'], { type: 'text/calendar;charset=utf-8' }));
    a.setAttribute('data-url', u); a.href = u;
    a.hidden = false;
  }

  /* ---- copy the IBAN: no spaces (banking apps take it either way), a spoken and visible confirmation ---- */
  var copy = $('i-copy'), done = $('i-copied'), num = $('i-iban'), doneT = 0;
  function say(msg) { done.textContent = msg; clearTimeout(doneT); doneT = setTimeout(function () { done.textContent = ''; }, 6000); }
  function selectNum() { var r = document.createRange(); r.selectNodeContents(num); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }
  if (copy) {
    copy.hidden = false;
    copy.addEventListener('click', function () {
      var v = num.textContent.replace(/\s+/g, '');
      var ok = function () { say(t.copied); }, bad = function () { selectNum(); say(t.copyFail); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(v).then(ok, bad);
      else bad();
    });
  }

  /* ---- props: art one screen ahead (.near), the entrance once (.seen), loops only while in view (.vis) ---- */
  function hooks() {
    var secs = Array.prototype.slice.call(document.querySelectorAll('.isec, .rsvp, .foot-flora'));
    if (!('IntersectionObserver' in window)) { secs.forEach(function (s) { s.classList.add('near', 'seen', 'vis'); }); return; }
    var near = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('near'); near.unobserve(e.target); } }); }, { rootMargin: '100% 0px 100% 0px' });
    var seen = new IntersectionObserver(function (es) { es.forEach(function (e) {
      e.target.classList.toggle('vis', e.isIntersecting);
      if (e.isIntersecting) e.target.classList.add('seen');
    }); }, { threshold: 0.15 });
    secs.forEach(function (s) { near.observe(s); seen.observe(s); });
  }

  /* ---- visibility: like the RSVP, the sections show once the invitation is opened ---- */
  var page = document.querySelector('main.page'), on = false;
  function sync() {
    var open = !page || page.classList.contains('opened');
    if (open && !on) { on = true; wrap.classList.add('info-on'); startClock(); hooks(); }
  }
  setLang(root.lang);
  new MutationObserver(function () { setLang(root.lang); }).observe(root, { attributes: true, attributeFilter: ['lang'] });
  if (page) new MutationObserver(sync).observe(page, { attributes: true, attributeFilter: ['class'] });
  sync();
})();
