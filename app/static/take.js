(function () {
  var cfg = window.EXAM;
  var csrf = document.querySelector('meta[name="csrf-token"]').content;
  var questions = Array.prototype.slice.call(document.querySelectorAll('.question'));
  var navButtons = Array.prototype.slice.call(document.querySelectorAll('.nav-q'));
  var current = 0;
  var submitting = false;
  var pending = {};      // question_id -> choice not yet confirmed by the server
  var inflight = 0;
  var saveState = document.getElementById('save-state');
  var flagKey = 'grind-flags-' + cfg.attemptId;

  // ---------- flags (per-browser convenience only) ----------
  var flags = {};
  try { flags = JSON.parse(localStorage.getItem(flagKey) || '{}'); } catch (e) { flags = {}; }
  function saveFlags() { try { localStorage.setItem(flagKey, JSON.stringify(flags)); } catch (e) {} }

  // ---------- navigation ----------
  function show(i) {
    if (i < 0 || i >= questions.length) return;
    questions[current].hidden = true;
    current = i;
    questions[current].hidden = false;
    navButtons.forEach(function (b, j) { b.classList.toggle('current', j === i); });
    navButtons[i].scrollIntoView({block: 'nearest'});
    window.scrollTo({top: 0});
  }
  navButtons.forEach(function (b, i) {
    b.dataset.index = i;
    b.classList.toggle('flagged', !!flags[b.dataset.qid]);
    b.addEventListener('click', function () { show(i); });
  });

  function refreshNav(q) {
    var idx = questions.indexOf(q);
    var answered = !!q.querySelector('input:checked');
    navButtons[idx].classList.toggle('answered', answered);
    document.getElementById('answered-count').textContent = document.querySelectorAll('.nav-q.answered').length;
  }

  // ---------- saving ----------
  function setState(text, cls) { saveState.textContent = text; saveState.className = 'save-state small ' + (cls || 'muted'); }

  function save(qid, choice) {
    pending[qid] = choice;
    inflight++;
    setState('Saving…');
    return fetch(cfg.saveUrl, {
      method: 'POST',
      headers: {'Content-Type': 'application/json', 'X-CSRF-Token': csrf},
      body: JSON.stringify({question_id: Number(qid), choice: choice}),
      credentials: 'same-origin'
    }).then(function (r) {
      if (r.status === 409) { finish('timeout'); return; }
      if (!r.ok) throw new Error('HTTP ' + r.status);
      if (pending[qid] === choice) delete pending[qid];
    }).catch(function () {
      setState('Not saved, retrying…', 'warn');
      setTimeout(function () { if (qid in pending) save(qid, pending[qid]); }, 2000);
    }).finally(function () {
      inflight--;
      if (!inflight && !Object.keys(pending).length) setState('All answers saved');
    });
  }

  questions.forEach(function (q) {
    var qid = q.dataset.qid;
    q.querySelectorAll('input[type=radio]').forEach(function (input) {
      input.addEventListener('change', function () { refreshNav(q); save(qid, input.value); });
    });
    q.querySelector('[data-act=prev]').addEventListener('click', function () { show(current - 1); });
    q.querySelector('[data-act=next]').addEventListener('click', function () { show(current + 1); });
    q.querySelector('[data-act=clear]').addEventListener('click', function () {
      var c = q.querySelector('input:checked');
      if (c) { c.checked = false; refreshNav(q); save(qid, null); }
    });
    var flagBtn = q.querySelector('[data-act=flag]');
    function paintFlag() { flagBtn.textContent = flags[qid] ? 'Unflag' : 'Flag'; navButtons[questions.indexOf(q)].classList.toggle('flagged', !!flags[qid]); }
    flagBtn.addEventListener('click', function () { if (flags[qid]) delete flags[qid]; else flags[qid] = 1; saveFlags(); paintFlag(); });
    paintFlag();
  });

  document.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' && e.target.type !== 'radio') return;
    if (document.getElementById('submit-dialog').open || e.ctrlKey || e.metaKey || e.altKey) return;
    var q = questions[current];
    var k = e.key.toUpperCase();
    if (k === 'ARROWRIGHT') { show(current + 1); e.preventDefault(); }
    else if (k === 'ARROWLEFT') { show(current - 1); e.preventDefault(); }
    else if (k === 'F') { q.querySelector('[data-act=flag]').click(); }
    else if (/^[A-H]$/.test(k)) {
      var input = q.querySelector('input[value="' + k + '"]');
      if (input && !input.checked) { input.checked = true; input.dispatchEvent(new Event('change')); }
    }
  });

  // ---------- timer ----------
  var timerEl = document.getElementById('timer');
  var endAt = performance.now() + Number(timerEl.dataset.remaining) * 1000;
  function tick() {
    var left = Math.max(0, Math.round((endAt - performance.now()) / 1000));
    var h = Math.floor(left / 3600), m = Math.floor(left % 3600 / 60), s = left % 60;
    timerEl.textContent = (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(s).padStart(2, '0');
    timerEl.classList.toggle('low', left <= 300);
    timerEl.classList.toggle('critical', left <= 60);
    if (left === 0) { finish('timeout'); return; }
    setTimeout(tick, 250);
  }
  tick();

  // ---------- submit ----------
  var dialog = document.getElementById('submit-dialog');
  var form = document.getElementById('submit-form');
  document.getElementById('open-submit').addEventListener('click', function () {
    var answered = document.querySelectorAll('.nav-q.answered').length;
    var left = cfg.total - answered;
    var flagged = Object.keys(flags).length;
    document.getElementById('submit-summary').textContent =
      'You have answered ' + answered + ' of ' + cfg.total + ' questions.' +
      (left ? ' ' + left + ' unanswered will count as wrong.' : '') +
      (flagged ? ' ' + flagged + ' flagged for review.' : '');
    dialog.showModal();
  });
  document.getElementById('cancel-submit').addEventListener('click', function () { dialog.close(); });
  form.addEventListener('submit', function (e) { e.preventDefault(); finish('manual'); });

  function finish(reason) {
    if (submitting) return;
    submitting = true;
    document.getElementById('submit-reason').value = reason;
    if (reason === 'timeout') setState("Time's up! Submitting…", 'warn');
    document.querySelectorAll('input[type=radio]').forEach(function (i) { i.disabled = true; });
    // Give in-flight saves a moment to land, then submit.
    var waited = 0;
    (function wait() {
      if ((inflight || Object.keys(pending).length) && waited < 3000) { waited += 100; return setTimeout(wait, 100); }
      try { localStorage.removeItem(flagKey); } catch (e) {}
      HTMLFormElement.prototype.submit.call(form);
    })();
  }

  show(0);
})();
