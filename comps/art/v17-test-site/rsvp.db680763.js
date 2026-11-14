/* RSVP section script. Runs only when the page was built with the RSVP on (rsvp/rsvp-config.json).
   The personal code comes from the part of the address after #, is removed from the address bar at once and is sent only in
   the X-Rsvp-Code header. Nothing the guest types is shown as saved until the server confirms it.
   FAKE: every guest-facing sentence in T is placeholder wording; the couple replaces it (rsvp/comps/REPLACE-ME.md). */
(function () {
  'use strict';
  var CFG = {"api": "https://rsvp-test.tominacio99.workers.dev"};
  var root = document.documentElement, wrap = document.getElementById('rsvp-wrap'), sec = document.getElementById('rsvp');
  if (!wrap || !sec) return;
  var $ = function (id) { return document.getElementById(id); };
  var reduce = matchMedia('(prefers-reduced-motion: reduce)');
  var T = {
    'pt-PT': { kicker:'Confirmação', title:'Contamos convosco?', sub:'Respondam até 30 de abril', lead:'Guardámos um lugar para cada um de vós. Digam-nos quem vem; podem mudar a resposta até lá.',
      locKicker:'Como chegar', maps:'Abrir no mapa', cal:'Juntar ao calendário', loading:'A abrir o vosso convite…',
      formFor:'Convite para', who:'Convidado', extraSeat:'Lugar extra', extra:'Acompanhante', yes:'Vou', no:'Não posso ir',
      diet:'Alergias ou restrições alimentares (opcional)', dietPh:'ex.: sem glúten, alergia a frutos secos', dietNote:'Só a cozinha vê isto; apagamos tudo depois do casamento.',
      extraName:'Nome do acompanhante', msg:'Uma mensagem para nós (opcional)', msgPh:'Escrevam-nos umas linhas…', send:'Enviar resposta', sending:'A enviar…',
      errTitle:'Falta pouco. Corrijam isto:', errChoose:'Escolham “Vou” ou “Não posso ir” para {n}.', errName:'Escrevam o nome do acompanhante.',
      netTitle:'Não foi possível enviar.', netText:'A ligação falhou. Não se perdeu nada: as vossas respostas continuam aqui.', retry:'Tentar de novo',
      confTitle:'As respostas mudaram noutro telemóvel.', confText:'Esta é a resposta guardada agora. Querem ficar com ela ou enviar a vossa?', useSaved:'Ficar com a guardada', sendMine:'Enviar a minha',
      savedTitle:'Obrigado!', savedText:'Recebemos a vossa resposta.', edit:'Alterar respostas', coming:'vem', notComing:'não vem',
      closedTitle:'As respostas já fecharam.', closedText:'Já não aceitamos respostas. Para mudar alguma coisa, falem connosco no WhatsApp.', wa:'Falar no WhatsApp',
      nolinkTitle:'Não encontrámos o vosso convite.', nolinkText:'Abram o link pessoal que vos enviámos no WhatsApp, ou escrevam o código que vem no fim dele.',
      tmTitle:'Demasiadas tentativas.', tmText:'Por segurança, esperem uma hora e tentem de novo, ou abram o link do WhatsApp.', code:'O vosso código', codeHint:'16 letras e números, sem espaços.', open:'Abrir',
      nojsTitle:'Para responder aqui, esta página precisa de JavaScript.', nojsText:'Respondam-nos pelo WhatsApp, ou abram o link noutro navegador.',
      extrasHead:'Só se precisarmos', dinner:'Prato principal', fish:'Peixe', veg:'Vegetariano', song:'Uma música que vos ponha a dançar', songPh:'ex.: Lisboa Menina e Moça',
      transport:'Precisamos de transporte desde Lisboa', stay:'Queremos ajuda com alojamento perto da quinta', phone:'Telemóvel (opcional)',
      liveSending:'A enviar a resposta.', liveSaved:'Resposta guardada.', liveError:'Há campos por corrigir.', liveNet:'Falhou o envio. As respostas continuam no formulário.', liveConf:'As respostas mudaram noutro telemóvel.' },
    en: { kicker:'Kindly reply', title:'Will you join us?', sub:'Please let us know by 30 April', lead:'We have kept a seat for each of you. Tell us who is coming; you can change your answer until then.',
      locKicker:'How to get there', maps:'Open in Maps', cal:'Add to calendar', loading:'Opening your invitation…',
      formFor:'Invitation for', who:'Guest', extraSeat:'Extra seat', extra:'Your guest', yes:'I’ll be there', no:'Can’t make it',
      diet:'Allergies or dietary needs (optional)', dietPh:'e.g. gluten-free, nut allergy', dietNote:'Only the kitchen sees this; we delete it after the wedding.',
      extraName:'Your guest’s name', msg:'A message for us (optional)', msgPh:'Write us a few lines…', send:'Send reply', sending:'Sending…',
      errTitle:'Almost there. Please fix:', errChoose:'Choose “I’ll be there” or “Can’t make it” for {n}.', errName:'Write your guest’s name.',
      netTitle:'We couldn’t send it.', netText:'The connection failed. Nothing is lost: your answers are still here.', retry:'Try again',
      confTitle:'These answers changed on another phone.', confText:'This is the answer saved now. Keep it, or send yours?', useSaved:'Keep the saved one', sendMine:'Send mine',
      savedTitle:'Thank you!', savedText:'We have your reply.', edit:'Change answers', coming:'coming', notComing:'not coming',
      closedTitle:'Replies are closed.', closedText:'We are no longer taking replies. To change anything, message us on WhatsApp.', wa:'Message us on WhatsApp',
      nolinkTitle:'We couldn’t find your invitation.', nolinkText:'Open the personal link we sent you on WhatsApp, or type the code at the end of it.',
      tmTitle:'Too many tries.', tmText:'For safety, wait an hour and try again, or open the WhatsApp link.', code:'Your code', codeHint:'16 letters and numbers, no spaces.', open:'Open',
      nojsTitle:'To reply here, this page needs JavaScript.', nojsText:'Reply to us on WhatsApp, or open the link in another browser.',
      extrasHead:'Only if we need it', dinner:'Main course', fish:'Fish', veg:'Vegetarian', song:'A song that gets you dancing', songPh:'e.g. Lisboa Menina e Moça',
      transport:'We need transport from Lisbon', stay:'We would like help with a place to stay', phone:'Mobile (optional)',
      liveSending:'Sending your reply.', liveSaved:'Reply saved.', liveError:'Some fields need fixing.', liveNet:'Sending failed. Your answers are still in the form.', liveConf:'These answers changed on another phone.' },
    es: { kicker:'Confirmación', title:'¿Nos acompañáis?', sub:'Responded antes del 30 de abril', lead:'Hemos guardado un sitio para cada uno de vosotros. Decidnos quién viene; podéis cambiar la respuesta hasta entonces.',
      locKicker:'Cómo llegar', maps:'Abrir en el mapa', cal:'Añadir al calendario', loading:'Abriendo vuestra invitación…',
      formFor:'Invitación para', who:'Invitado', extraSeat:'Plaza extra', extra:'Acompañante', yes:'Allí estaré', no:'No podré ir',
      diet:'Alergias o restricciones alimentarias (opcional)', dietPh:'p. ej.: sin gluten, alergia a frutos secos', dietNote:'Solo lo ve la cocina; lo borramos después de la boda.',
      extraName:'Nombre del acompañante', msg:'Un mensaje para nosotros (opcional)', msgPh:'Escribidnos unas líneas…', send:'Enviar respuesta', sending:'Enviando…',
      errTitle:'Casi listo. Corregid esto:', errChoose:'Elegid “Allí estaré” o “No podré ir” para {n}.', errName:'Escribid el nombre del acompañante.',
      netTitle:'No se pudo enviar.', netText:'Falló la conexión. No se ha perdido nada: vuestras respuestas siguen aquí.', retry:'Reintentar',
      confTitle:'Las respuestas cambiaron en otro teléfono.', confText:'Esta es la respuesta guardada ahora. ¿Os quedáis con ella o enviáis la vuestra?', useSaved:'Quedarme con la guardada', sendMine:'Enviar la mía',
      savedTitle:'¡Gracias!', savedText:'Hemos recibido vuestra respuesta.', edit:'Cambiar respuestas', coming:'viene', notComing:'no viene',
      closedTitle:'Las respuestas están cerradas.', closedText:'Ya no aceptamos respuestas. Para cambiar algo, escribidnos por WhatsApp.', wa:'Escribirnos por WhatsApp',
      nolinkTitle:'No encontramos vuestra invitación.', nolinkText:'Abrid el enlace personal que os enviamos por WhatsApp, o escribid el código del final.',
      tmTitle:'Demasiados intentos.', tmText:'Por seguridad, esperad una hora y volved a intentarlo, o abrid el enlace de WhatsApp.', code:'Vuestro código', codeHint:'16 letras y números, sin espacios.', open:'Abrir',
      nojsTitle:'Para responder aquí, esta página necesita JavaScript.', nojsText:'Respondednos por WhatsApp, o abrid el enlace en otro navegador.',
      extrasHead:'Solo si lo necesitamos', dinner:'Plato principal', fish:'Pescado', veg:'Vegetariano', song:'Una canción que os haga bailar', songPh:'p. ej.: Lisboa Menina e Moça',
      transport:'Necesitamos transporte desde Lisboa', stay:'Queremos ayuda con alojamiento cerca de la quinta', phone:'Móvil (opcional)',
      liveSending:'Enviando la respuesta.', liveSaved:'Respuesta guardada.', liveError:'Hay campos por corregir.', liveNet:'Falló el envío. Las respuestas siguen en el formulario.', liveConf:'Las respuestas cambiaron en otro teléfono.' }
  };

  /* FAKE wording for the two states the mock did not have */
  T['pt-PT'].loadErrText = 'Não conseguimos abrir o vosso convite agora. Tentem de novo daqui a pouco.'; T['pt-PT'].errGeneric = 'Algo não correu bem. Verifiquem as respostas e tentem de novo.';
  T.en.loadErrText = 'We could not open your invitation right now. Please try again in a moment.'; T.en.errGeneric = 'Something went wrong. Please check your answers and try again.';
  T['pt-PT'].errChanges = 'Já fizeram demasiadas alterações hoje. Tentem amanhã ou falem connosco.'; T.en.errChanges = 'You have made too many changes today. Try again tomorrow or contact us.'; T.es.errChanges = 'Habéis hecho demasiados cambios hoy. Probad mañana o hablad con nosotros.';
  T['pt-PT'].codeBad = 'Esse código não funcionou. Confirmem o link ou escrevam o código de novo.'; T.en.codeBad = 'That code did not work. Check the link or type the code again.'; T.es.codeBad = 'Ese código no funcionó. Revisad el enlace o escribid el código de nuevo.';
  T['pt-PT'].codeShort = 'O código tem 16 letras e números.'; T.en.codeShort = 'The code has 16 letters and numbers.'; T.es.codeShort = 'El código tiene 16 letras y números.';
  T['pt-PT'].savedNo = 'Obrigado por nos avisarem. Vamos sentir a vossa falta.'; T.en.savedNo = 'Thank you for letting us know. We will miss you.'; T.es.savedNo = 'Gracias por avisarnos. Os echaremos de menos.';
  T.es.loadErrText = 'No pudimos abrir vuestra invitación ahora. Probad de nuevo en un momento.'; T.es.errGeneric = 'Algo ha ido mal. Revisad las respuestas y probad de nuevo.';

  var lang = 'pt-PT', state = 'nojs', view = null, code = '', started = false, sending = false;
  var t = function (k) { return (T[lang] && T[lang][k]) || T['pt-PT'][k] || k; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var people = function () { return view ? view.people : []; };
  var DRAFT = 'rsvp-draft-', CODEKEY = 'rsvp-code', DRAFT_MS = 24 * 3600 * 1000;
  /* the draft is kept per household (a short non-secret fingerprint of the code) so one family's answers never appear in another's form */
  var fp = function (s) { var x = 2166136261; for (var i = 0; i < s.length; i++) { x ^= s.charCodeAt(i); x = Math.imul(x, 16777619); } return (x >>> 0).toString(36); };
  var store = function (fn) { try { return fn(); } catch (_) { return null; } };

  function renderPeople() {
    var keep = collect();
    $('people').innerHTML = people().map(function (p) {
      var id = 'p' + p.slot, ex = !!p.is_extra;
      return '<fieldset class="person" id="' + id + '" data-slot="' + p.slot + '">' +
        '<legend><small>' + esc(ex ? t('extraSeat') : t('who')) + '</small>' + (ex ? '<span>' + esc(t('extra')) + '</span>' : '<span translate="no">' + esc(p.name) + '</span>') + '</legend>' +
        '<div class="choices">' +
          '<label class="choice yes"><input type="radio" name="' + id + '-a" value="yes" aria-describedby="' + id + '-e"><span class="dot"></span><span class="txt">' + esc(t('yes')) + '</span></label>' +
          '<label class="choice no"><input type="radio" name="' + id + '-a" value="no" aria-describedby="' + id + '-e"><span class="dot"></span><span class="txt">' + esc(t('no')) + '</span></label>' +
        '</div>' +
        '<p class="err e-choice" id="' + id + '-e"></p>' +
        '<div class="more">' +
          (ex ? '<div class="field" id="' + id + '-nf"><label for="' + id + '-n">' + esc(t('extraName')) + '</label><input type="text" id="' + id + '-n" maxlength="80" autocomplete="off" aria-describedby="' + id + '-ne"><p class="err" id="' + id + '-ne"></p></div>' : '') +
          '<div class="field"><label for="' + id + '-d">' + esc(t('diet')) + '</label><input type="text" id="' + id + '-d" maxlength="200" autocomplete="off" placeholder="' + esc(t('dietPh')) + '" aria-describedby="' + id + '-dn"><p class="note" id="' + id + '-dn">' + esc(t('dietNote')) + '</p></div>' +
        '</div></fieldset>';
    }).join('');
    apply(keep);
  }

  function collect() {
    var out = {};
    people().forEach(function (p) {
      var id = 'p' + p.slot, r = document.querySelector('input[name="' + id + '-a"]:checked');
      if (!$(id)) return;
      out[p.slot] = { attending: r ? r.value === 'yes' : null, diet: ($(id + '-d') || {}).value || '', name: ($(id + '-n') || {}).value || '' };
    });
    return out;
  }
  function apply(a) {
    people().forEach(function (p) {
      var id = 'p' + p.slot, v = a[p.slot] || {};
      if (!$(id)) return;
      document.querySelectorAll('input[name="' + id + '-a"]').forEach(function (r) { r.checked = v.attending != null && v.attending === (r.value === 'yes'); });
      if ($(id + '-d')) $(id + '-d').value = v.diet || '';
      if ($(id + '-n')) $(id + '-n').value = v.name || '';
      $(id).classList.toggle('yes', v.attending === true);
    });
  }
  function fromView(v) {
    var o = {};
    v.people.forEach(function (p) { o[p.slot] = p.answer ? { attending: p.answer.attending, diet: p.answer.diet || '', name: p.answer.name || '' } : {}; });
    return o;
  }
  function clearErrors() {
    document.querySelectorAll('.person.bad,.field.bad').forEach(function (e) { e.classList.remove('bad'); });
    document.querySelectorAll('[aria-invalid]').forEach(function (e) { e.removeAttribute('aria-invalid'); });
    $('errlist').innerHTML = '';
  }
  function validate() {
    clearErrors();
    var a = collect(), errs = [];
    people().forEach(function (p) {
      var id = 'p' + p.slot, v = a[p.slot];
      if (!p.is_extra && v.attending == null) {
        var m = t('errChoose').replace('{n}', p.name);
        $(id).classList.add('bad'); $(id + '-e').textContent = m;
        document.querySelectorAll('input[name="' + id + '-a"]').forEach(function (r) { r.setAttribute('aria-invalid', 'true'); });
        errs.push({ to: id, m: m });
      }
      if (p.is_extra && v.attending && !v.name.trim()) {
        $(id + '-nf').classList.add('bad'); $(id + '-ne').textContent = t('errName'); $(id + '-n').setAttribute('aria-invalid', 'true');
        errs.push({ to: id + '-n', m: t('errName') });
      }
    });
    $('errlist').innerHTML = errs.map(function (e) { return '<li><a href="#' + e.to + '">' + esc(e.m) + '</a></li>'; }).join('');
    return errs;
  }
  function summary(a, list) {
    $(list).innerHTML = people().filter(function (p) { return !p.is_extra || (a[p.slot] && a[p.slot].attending); }).map(function (p) {
      var v = a[p.slot] || {}, nm = p.is_extra ? (v.name || t('extra')) : p.name;
      return '<li class="' + (v.attending ? '' : 'not') + '"><span translate="no">' + esc(nm) + (v.attending && v.diet ? '<span class="diet">' + esc(v.diet) + '</span>' : '') + '</span><span>' + esc(v.attending ? t('coming') : t('notComing')) + '</span></li>';
    }).join('');
  }
  function say(k) { var l = $('live'); l.textContent = ''; setTimeout(function () { l.textContent = t(k); }, 30); }
  function focus(el) { if (el) el.focus(); }

  function setState(s, opts) {
    opts = opts || {};
    state = s; sec.dataset.state = s;
    sec.querySelectorAll('.blk').forEach(function (b) { b.classList.remove('enter'); });
    var vis = [].find.call(sec.querySelectorAll('.blk'), function (b) { return getComputedStyle(b).display !== 'none'; });
    if (vis && !reduce.matches) { void vis.offsetWidth; vis.classList.add('enter'); }
    $('sendlbl').textContent = t(s === 'sending' ? 'sending' : 'send');
    $('form').setAttribute('aria-busy', s === 'sending' ? 'true' : 'false');
    $('send').setAttribute('aria-disabled', s === 'sending' ? 'true' : 'false');
    if (s === 'error') { if (!opts.quiet) { say('liveError'); focus($('errsum')); } } else if (s !== 'sending') clearErrors();
    if (s === 'network') { if (!opts.quiet) { say('liveNet'); focus($('netbox')); } }
    if (s === 'conflict') { summary(fromView(view), 'conflist'); if (!opts.quiet) { say('liveConf'); focus($('confbox')); } }
    if (s === 'saved') {
      var av = fromView(view), any = Object.keys(av).some(function (k) { return av[k].attending; });
      $('savedtext').dataset.i18n = any ? 'savedText' : 'savedNo'; $('savedtext').textContent = t(any ? 'savedText' : 'savedNo');
      summary(av, 'savedlist'); if (!opts.quiet) { say('liveSaved'); focus($('savedbox')); }
    }
    if (s === 'closed') summary(fromView(view), 'closedlist');
    if (s === 'sending' && !opts.quiet) say('liveSending');
  }

  function setLang(l) {
    lang = T[l] ? l : (T[(l || '').slice(0, 2)] ? (l || '').slice(0, 2) : 'pt-PT');
    sec.lang = lang;
    document.querySelectorAll('#rsvp [data-i18n]').forEach(function (e) { e.textContent = t(e.dataset.i18n); });
    document.querySelectorAll('#rsvp [data-i18n-ph]').forEach(function (e) { e.placeholder = t(e.dataset.i18nPh); });
    if (view) renderPeople();
    setState(state, { quiet: true });
  }

  /* ---- talking to the Worker ---- */
  function call(path, body) {
    /* a request that never answers must not leave the guest on "Sending..." for ever */
    var ac = typeof AbortController === 'function' ? new AbortController() : null, timer = ac ? setTimeout(function () { ac.abort(); }, 15000) : 0;
    return fetch(CFG.api + path, {
      method: 'POST', cache: 'no-store', credentials: 'omit', referrerPolicy: 'no-referrer', mode: 'cors', signal: ac ? ac.signal : undefined,
      headers: { 'Content-Type': 'application/json', 'X-Rsvp-Code': code },
      body: JSON.stringify(body || {})
    }).then(function (r) { clearTimeout(timer); return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; }); },
      function (e) { clearTimeout(timer); throw e; });
  }
  var typed = false;
  function codeProblem(k) {
    $('code').setAttribute('aria-invalid', 'true'); $('codeerr').textContent = t(k); $('code').focus(); say(k);
  }
  function lookup() {
    setState('loading', { quiet: true });
    call('/api/lookup').then(function (r) {
      if (r.status === 200) { view = r.body; show(!typed); if (typed) { typed = false; focus(document.querySelector('#people input') || $('savedbox')); } }
      else if (r.status === 404) { store(function () { sessionStorage.removeItem(CODEKEY); }); code = ''; setState('nolink', { quiet: true }); if (typed) codeProblem('codeBad'); }
      else if (r.status === 429) setState('toomany', { quiet: true });
      else setState('loaderr', { quiet: true });
    }, function () { setState('loaderr', { quiet: true }); });
  }
  function show(first) {
    $('family').textContent = view.family.label;
    renderPeople();
    $('msg').value = view.message || ''; $('msgcount').textContent = $('msg').value.length + '/600';
    if (!view.open) { setState('closed', { quiet: true }); return; }
    if (view.answered) { apply(fromView(view)); setState('saved', { quiet: first }); return; }
    var d = store(function () { return JSON.parse(localStorage.getItem(DRAFT + fp(code)) || 'null'); });
    if (d && d.rev === view.revision && d.answers && Date.now() - d.at < DRAFT_MS) { apply(d.answers); if (d.message) { $('msg').value = d.message; $('msgcount').textContent = d.message.length + '/600'; } }
    setState('form', { quiet: first });
  }
  function submit() {
    if (sending) return;
    var a = collect();
    var body = { revision: view.revision, message: $('msg').value, website: ($('hp-field') || {}).value || '',
      answers: people().map(function (p) {
        var v = a[p.slot] || {};
        return { slot: p.slot, attending: v.attending == null ? (p.is_extra ? false : undefined) : v.attending, diet: v.attending ? v.diet : '', name: v.attending ? v.name : '' };
      }) };
    sending = true; setState('sending');
    call('/api/answer', body).then(function (r) {
      sending = false;
      if (r.status === 200 && r.body && r.body.people) { view = r.body; store(function () { localStorage.removeItem(DRAFT + fp(code)); }); setState('saved'); }
      else if (r.status === 409 && r.body && r.body.people) { view = r.body; setState('conflict'); }
      else if (r.status === 403 && r.body && r.body.error === 'closed') { if (r.body.closes_at && view) view.open = false; setState('closed'); }
      else if (r.status === 429 && r.body && r.body.error === 'too_many_attempts') setState('toomany');
      else if (r.status === 429) problem('errChanges');
      else if (r.status === 400 || r.status === 413) problem('errGeneric');
      else setState('network');
    }, function () { sending = false; setState('network'); });
  }
  function problem(k) {
    $('errlist').innerHTML = '<li><a href="#p' + people()[0].slot + '">' + esc(t(k)) + '</a></li>';
    setState('error', { keep: true });
  }
  function saveDraft() {
    if (!view) return;
    store(function () { localStorage.setItem(DRAFT + fp(code), JSON.stringify({ rev: view.revision, at: Date.now(), answers: collect(), message: $('msg').value })); });
  }

  /* ---- events ---- */
  $('people').addEventListener('change', function (e) {
    var f = e.target.closest('.person'); if (!f) return;
    if (e.target.type === 'radio') {
      f.classList.toggle('yes', e.target.value === 'yes');
      if (f.classList.contains('bad')) { f.classList.remove('bad'); f.querySelectorAll('[aria-invalid]').forEach(function (x) { x.removeAttribute('aria-invalid'); }); }
    }
    saveDraft();
  });
  $('people').addEventListener('input', saveDraft);
  $('msg').addEventListener('input', function () { $('msgcount').textContent = this.value.length + '/600'; saveDraft(); });
  $('form').addEventListener('submit', function (e) {
    e.preventDefault();
    if (sending || !view) return;
    if (validate().length) { setState('error', { keep: true }); return; }
    submit();
  });
  $('errlist').addEventListener('click', function (ev) {
    var a = ev.target.closest('a'); if (!a) return; ev.preventDefault();
    var el = $(a.getAttribute('href').slice(1)); var inp = el && (el.matches('input') ? el : el.querySelector('input'));
    if (inp) { inp.focus(); el.scrollIntoView({ block: 'center', behavior: reduce.matches ? 'auto' : 'smooth' }); }
  });
  $('retry').addEventListener('click', submit);
  $('usesaved').addEventListener('click', function () { renderPeople(); $('msg').value = view.message || ''; apply(fromView(view)); setState('form'); focus(document.querySelector('#people input')); });
  $('sendmine').addEventListener('click', submit);
  $('edit').addEventListener('click', function () { setState('form'); focus(document.querySelector('#people input')); });
  $('reload').addEventListener('click', lookup);
  $('codeform').addEventListener('submit', function (e) {
    e.preventDefault();
    if (state === 'toomany') return;
    var raw = $('code').value, k = raw.indexOf('#'); if (k >= 0) raw = raw.slice(k + 1); /* a pasted whole link: the code is after the # */
    var v = raw.toUpperCase().replace(/[^0-9A-Z]/g, '');
    if (v.length !== 16) { codeProblem('codeShort'); return; }
    $('codeerr').textContent = ''; $('code').removeAttribute('aria-invalid');
    typed = true; code = v; store(function () { sessionStorage.setItem(CODEKEY, code); }); lookup();
  });

  /* ---- start: take the code out of the address, then wait until the invitation is opened ---- */
  var h = location.hash.replace(/^#/, '');
  if (h) {
    code = h.toUpperCase().replace(/[\s-]+/g, '');
    store(function () { sessionStorage.setItem(CODEKEY, code); });
    store(function () { history.replaceState(null, '', location.pathname + location.search); });
  } else code = store(function () { return sessionStorage.getItem(CODEKEY); }) || '';

  function begin() {
    if (started) return; started = true;
    if (code) lookup(); else setState('nolink', { quiet: true });
  }
  var page = document.querySelector('main.page');
  function sync() {
    var open = !page || page.classList.contains('opened');
    wrap.classList.toggle('rsvp-on', open);
    if (open) begin();
  }
  setLang(root.lang);
  new MutationObserver(function () { setLang(root.lang); }).observe(root, { attributes: true, attributeFilter: ['lang'] });
  if (page) new MutationObserver(sync).observe(page, { attributes: true, attributeFilter: ['class'] });
  setState('loading', { quiet: true });
  sync();
})();
