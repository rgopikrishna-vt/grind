/* Exercise page: run code, grade it against example + hidden tests, hints, solution, autosave. */
(function () {
  "use strict";
  var EX = window.EXERCISE;
  var G = window.Grind;
  var $ = function (id) { return document.getElementById(id); };
  var NS = "ex-" + EX.id;

  var statusEl = $("kernel-status");
  var runBtn = $("run"), submitBtn = $("submit"), stopBtn = $("stop"), runScratchBtn = $("run-scratch");
  var saveState = $("save-state");
  var hintsUsed = 0;

  var kernel = new G.Kernel(function (status, detail) {
    statusEl.dataset.status = status;
    statusEl.textContent = G.statusText(status, detail);
    var busy = status === "busy";
    stopBtn.hidden = !busy;
    [runBtn, submitBtn, runScratchBtn].forEach(function (b) { b.disabled = busy || status === "error"; });
  });

  var editor = new G.Editor($("code"), { onRun: run, onRunAdvance: run });
  var scratch = new G.Editor($("scratch"), { onRun: runScratch, onRunAdvance: runScratch });
  var output = new G.Output($("output"));
  var scratchOut = new G.Output($("scratch-output"));
  var resultsEl = $("results");

  // ---------- autosave ----------
  var lastSaved = editor.getValue();
  function save() {
    var code = editor.getValue();
    if (code === lastSaved) return Promise.resolve();
    saveState.textContent = "Saving…";
    return G.api(EX.saveUrl, { code: code, hints_used: hintsUsed }, code.length < 60000).then(function () {
      lastSaved = code;
      saveState.textContent = "Saved";
      saveState.classList.remove("warn");
    }).catch(function () {
      saveState.textContent = "Not saved (offline?)";
      saveState.classList.add("warn");
    });
  }
  var saveSoon = G.debounce(save, 800);
  editor.onChange(function () { saveState.textContent = "Editing…"; saveSoon(); });
  window.addEventListener("pagehide", function () { saveSoon.flush(); });
  document.addEventListener("visibilitychange", function () { if (document.hidden) saveSoon.flush(); });

  // ---------- run ----------
  function run() {
    output.clear();
    resultsEl.hidden = true;
    kernel.run(editor.getValue(), { ns: NS, onStream: output.append.bind(output) }).then(function (v) {
      output.show(v);
      if (!v.error && !v.interrupted && !output.size) output.note("Ran without output. Call your function in the Try it cell, or press Submit.");
    });
  }

  function runScratch() {
    scratchOut.clear();
    kernel.run(scratch.getValue(), { ns: NS, onStream: scratchOut.append.bind(scratchOut) }).then(function (v) {
      scratchOut.show(v);
      if (!v.error && !v.interrupted && !scratchOut.size) scratchOut.note("Ran without output.");
    });
  }

  runBtn.addEventListener("click", run);
  runScratchBtn.addEventListener("click", runScratch);
  stopBtn.addEventListener("click", function () { kernel.interrupt(); });

  // ---------- submit ----------
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function renderResults(res) {
    resultsEl.innerHTML = "";
    resultsEl.hidden = false;
    if (res.interrupted) {
      resultsEl.appendChild(el("div", "result-summary bad", res.interrupted === "timeout"
        ? "Stopped after 10 seconds. Is there an infinite loop?" : "Stopped."));
      return false;
    }
    if (res.error) {
      resultsEl.appendChild(el("div", "result-summary bad", "Your code raised an error before the tests could run."));
      resultsEl.appendChild(el("pre", "output out-error-block", res.error));
      return false;
    }
    var allOk = res.total > 0 && res.passed === res.total;
    var summary = el("div", "result-summary " + (allOk ? "good" : "bad"),
      (allOk ? "All " + res.total + " tests passed." : res.passed + " of " + res.total + " tests passed."));
    resultsEl.appendChild(summary);
    var list = el("ul", "test-list");
    res.results.forEach(function (r) {
      var li = el("li", r.ok ? "ok" : "fail");
      li.appendChild(el("span", "test-icon", r.ok ? "✓" : "✗"));
      var body = el("div", "test-body");
      if (r.kind === "example") body.appendChild(el("code", null, r.src));
      else body.appendChild(el("span", null, "Hidden test " + r.n));
      if (!r.ok) {
        if (r.got != null) {
          var d = el("div", "test-detail small");
          d.appendChild(el("span", "muted", "got "));
          d.appendChild(el("code", null, r.got));
          d.appendChild(el("span", "muted", "  expected "));
          d.appendChild(el("code", null, r.expected));
          body.appendChild(d);
        }
        if (r.message) body.appendChild(el("pre", "test-msg small", r.message));
      }
      li.appendChild(body);
      list.appendChild(li);
    });
    resultsEl.appendChild(list);
    return allOk;
  }

  function submit() {
    var code = editor.getValue();
    output.clear();
    resultsEl.hidden = true;
    submitBtn.disabled = true;
    var groups = [["example", EX.examples], ["hidden", EX.tests]];
    kernel.grade(code, groups, { onStream: output.append.bind(output), timeoutMs: 10000 }).then(function (res) {
      var passed = renderResults(res);
      if (output.size) { output.last = null; output.note("(printed while testing)"); }
      return G.api(EX.submitUrl, { code: code, passed: passed }).then(function (r) {
        lastSaved = code;
        if (passed) celebrate(r.first_solve);
      }).catch(function () {
        saveState.textContent = "Result not saved (offline?)";
        saveState.classList.add("warn");
      });
    });
  }
  submitBtn.addEventListener("click", submit);

  function celebrate(first) {
    $("solved-badge").hidden = false;
    var box = el("div", "solved-box");
    box.appendChild(el("strong", null, first ? "Solved! " : "Solved again. "));
    if (EX.solutionViewed) box.appendChild(el("span", "muted small", "(after viewing the solution) "));
    if (EX.nextUrl) {
      var a = el("a", "btn primary", "Next exercise →");
      a.href = EX.nextUrl;
      box.appendChild(a);
    }
    resultsEl.appendChild(box);
  }

  $("reset").addEventListener("click", function () {
    if (editor.getValue() === EX.starter) return;
    var btn = $("reset");
    if (btn.dataset.armed) {
      editor.setValue(EX.starter);
      delete btn.dataset.armed;
      btn.textContent = "Reset to starter";
      return;
    }
    btn.dataset.armed = "1";
    btn.textContent = "Click again to erase your code";
    setTimeout(function () { delete btn.dataset.armed; btn.textContent = "Reset to starter"; }, 4000);
  });

  // ---------- hints ----------
  var hintBtn = $("hint-btn");
  if (hintBtn) {
    var total = +hintBtn.dataset.total;
    hintsUsed = +hintBtn.dataset.used;
    var items = document.querySelectorAll("#hints li");
    var label = function () {
      hintBtn.textContent = hintsUsed >= total ? "No more hints" : "Show hint " + (hintsUsed + 1) + " of " + total;
      hintBtn.disabled = hintsUsed >= total;
    };
    label();
    hintBtn.addEventListener("click", function () {
      if (hintsUsed >= total) return;
      items[hintsUsed].hidden = false;
      hintsUsed++;
      label();
      lastSaved = null; // force a save so the hint count is stored
      save();
    });
  }

  // ---------- solution ----------
  var solutionEditor = null;
  function showSolution() {
    $("solution-confirm").hidden = true;
    $("solution-btn").hidden = true;
    G.api(EX.solutionUrl, {}).then(function (r) {
      EX.solutionViewed = 1;
      $("solution").hidden = false;
      $("solution-code").value = r.solution;
      solutionEditor = new G.Editor($("solution-code"), { readOnly: true });
      if (r.explanation_html) {
        $("solution-explanation").innerHTML = r.explanation_html; // server-rendered from our own Markdown
        $("solution-explanation").hidden = false;
      }
    });
  }
  $("solution-btn").addEventListener("click", function () {
    if (EX.solutionViewed || (hintBtn && hintsUsed >= +hintBtn.dataset.total) || !hintBtn) { showSolution(); return; }
    $("solution-confirm").hidden = false;
  });
  $("solution-yes").addEventListener("click", showSolution);
  $("use-solution").addEventListener("click", function () {
    if (solutionEditor) editor.setValue(solutionEditor.getValue());
    editor.focus();
  });
})();
