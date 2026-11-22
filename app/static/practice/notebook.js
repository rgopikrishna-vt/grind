/* Scratchpad notebook: code and text cells sharing one Python namespace, saved to the server. */
(function () {
  "use strict";
  var NB = window.NOTEBOOK;
  var G = window.Grind;
  var $ = function (id) { return document.getElementById(id); };
  var NS = "nb-" + NB.id;

  var cellsEl = $("cells");
  var tpl = $("cell-tpl");
  var saveState = $("save-state");
  var statusEl = $("kernel-status");
  var cells = [];
  var execCounter = 0;
  var runningAll = false;

  var kernel = new G.Kernel(function (status, detail) {
    statusEl.dataset.status = status;
    statusEl.textContent = G.statusText(status, detail);
    $("stop").hidden = status !== "busy";
  });

  // ---------- markdown ----------
  function renderMarkdown(src) {
    if (window.marked && window.DOMPurify) return DOMPurify.sanitize(marked.parse(src || ""));
    var d = document.createElement("div");
    d.textContent = src;
    return "<p>" + d.innerHTML.replace(/\n/g, "<br>") + "</p>";
  }

  // ---------- saving ----------
  function snapshot() {
    return {
      title: $("nb-title").value.trim() || "Untitled",
      cells: cells.map(function (c) {
        var o = { type: c.type, source: c.editor.getValue() };
        var stdin = c.el.querySelector(".stdin").value;
        if (c.type === "code" && stdin) o.stdin = stdin;
        return o;
      }),
    };
  }
  var lastSaved = null;
  var deleting = false;

  function save() {
    if (deleting) return;
    var data = snapshot();
    var json = JSON.stringify(data);
    if (json === lastSaved) { saveState.textContent = "Saved"; return; }
    saveState.textContent = "Saving…";
    G.api(NB.saveUrl, data, json.length < 60000).then(function () {
      lastSaved = json;
      saveState.textContent = "Saved";
      saveState.classList.remove("warn");
    }).catch(function () {
      saveState.textContent = "Not saved (offline?)";
      saveState.classList.add("warn");
    });
  }
  var saveSoon = G.debounce(save, 1000);
  function changed() { saveState.textContent = "Editing…"; saveSoon(); }
  $("nb-title").addEventListener("input", changed);
  window.addEventListener("pagehide", function () { saveSoon.flush(); });
  document.addEventListener("visibilitychange", function () { if (document.hidden) saveSoon.flush(); });

  // ---------- cells ----------
  function makeEditor(cell, source) {
    var slot = cell.el.querySelector(".editor-slot");
    slot.innerHTML = "";
    var ta = document.createElement("textarea");
    ta.value = source || "";
    slot.appendChild(ta);
    var isCode = cell.type === "code";
    cell.editor = new G.Editor(ta, {
      mode: isCode ? "python" : "markdown",
      lineNumbers: isCode,
      lineWrapping: !isCode,
      onRun: function () { runCell(cell); },
      onRunAdvance: function () { runCell(cell).then(function () { focusNext(cell); }); },
      extraKeys: {
        "Esc": function () { if (cell.type === "markdown" && cell.editor.getValue().trim()) showMarkdown(cell); },
      },
    });
    cell.editor.onChange(changed);
    cell.el.dataset.type = cell.type;
    cell.el.querySelector('[data-act="type"]').textContent = isCode ? "T" : "{ }";
    cell.el.querySelector('[data-act="type"]').title = isCode ? "Turn into a text cell" : "Turn into a code cell";
    cell.el.querySelector('[data-act="stdin"]').hidden = !isCode;
    cell.el.querySelector('[data-act="run"]').title = isCode ? "Run (Shift+Enter)" : "Render (Shift+Enter)";
  }

  function showMarkdown(cell) {
    var view = cell.el.querySelector(".md-view");
    view.innerHTML = renderMarkdown(cell.editor.getValue());
    view.hidden = false;
    cell.el.querySelector(".editor-slot").hidden = true;
  }

  function editMarkdown(cell) {
    cell.el.querySelector(".md-view").hidden = true;
    cell.el.querySelector(".editor-slot").hidden = false;
    cell.editor.refresh();
    cell.editor.focus();
  }

  function createCell(data, index) {
    var frag = tpl.content.cloneNode(true);
    var el = frag.querySelector(".nb-cell");
    var cell = { type: data.type === "markdown" ? "markdown" : "code", el: el };
    cell.output = new G.Output(el.querySelector(".output"));
    var stdin = el.querySelector(".stdin");
    stdin.value = data.stdin || "";
    el.querySelector(".stdin-box").hidden = !data.stdin;
    stdin.addEventListener("input", changed);

    if (index == null || index >= cells.length) { cellsEl.appendChild(el); cells.push(cell); }
    else { cellsEl.insertBefore(el, cells[index].el); cells.splice(index, 0, cell); }
    makeEditor(cell, data.source);
    if (cell.type === "markdown" && (data.source || "").trim()) showMarkdown(cell);

    el.querySelector(".md-view").addEventListener("dblclick", function () { editMarkdown(cell); });
    el.addEventListener("focusin", function () { setActive(cell); });
    el.addEventListener("mousedown", function () { setActive(cell); });
    el.querySelector(".cell-actions").addEventListener("click", function (e) {
      var act = e.target.closest("[data-act]");
      if (act) cellAction(cell, act.dataset.act);
    });
    return cell;
  }

  function setActive(cell) {
    cells.forEach(function (c) { c.el.classList.toggle("active", c === cell); });
  }

  function cellAction(cell, act) {
    var i = cells.indexOf(cell);
    if (act === "run") runCell(cell);
    else if (act === "stdin") {
      var box = cell.el.querySelector(".stdin-box");
      box.hidden = !box.hidden;
      if (!box.hidden) box.querySelector("textarea").focus();
    } else if (act === "type") {
      var src = cell.editor.getValue();
      cell.type = cell.type === "code" ? "markdown" : "code";
      cell.output.clear();
      cell.el.querySelector(".exec-count").textContent = "";
      cell.el.querySelector(".md-view").hidden = true;
      cell.el.querySelector(".editor-slot").hidden = false;
      makeEditor(cell, src);
      cell.editor.focus();
      changed();
    } else if (act === "up" && i > 0) {
      cellsEl.insertBefore(cell.el, cells[i - 1].el);
      cells.splice(i, 1); cells.splice(i - 1, 0, cell);
      cell.editor.refresh();
      changed();
    } else if (act === "down" && i < cells.length - 1) {
      cellsEl.insertBefore(cells[i + 1].el, cell.el);
      cells.splice(i, 1); cells.splice(i + 1, 0, cell);
      cell.editor.refresh();
      changed();
    } else if (act === "add") {
      createCell({ type: "code", source: "" }, i + 1).editor.focus();
      changed();
    } else if (act === "delete") {
      cell.el.remove();
      cells.splice(i, 1);
      if (!cells.length) createCell({ type: "code", source: "" });
      changed();
    }
  }

  function focusNext(cell) {
    var i = cells.indexOf(cell);
    var next = cells[i + 1] || createCell({ type: "code", source: "" });
    if (!cells[i + 1]) changed();
    if (next.type === "markdown" && !next.el.querySelector(".md-view").hidden) {
      next.el.scrollIntoView({ block: "nearest" });
      setActive(next);
    } else {
      next.editor.focus();
    }
  }

  function runCell(cell) {
    if (cell.type === "markdown") {
      if (cell.editor.getValue().trim()) showMarkdown(cell);
      return Promise.resolve({});
    }
    cell.output.clear();
    var countEl = cell.el.querySelector(".exec-count");
    countEl.textContent = "[*]";
    cell.el.classList.add("running");
    var stdin = cell.el.querySelector(".stdin").value;
    if (stdin && !/\n$/.test(stdin)) stdin += "\n";
    return kernel.run(cell.editor.getValue(), { ns: NS, stdin: stdin, onStream: cell.output.append.bind(cell.output) }).then(function (v) {
      cell.el.classList.remove("running");
      countEl.textContent = v.interrupted ? "[ ]" : "[" + (++execCounter) + "]";
      cell.output.show(v);
      return v;
    });
  }

  $("run-all").addEventListener("click", function () {
    if (runningAll) return;
    runningAll = true;
    var i = 0;
    (function next() {
      if (i >= cells.length) { runningAll = false; return; }
      runCell(cells[i++]).then(function (v) {
        if (v.error || v.interrupted) { runningAll = false; return; }
        next();
      });
    })();
  });
  $("stop").addEventListener("click", function () { kernel.interrupt(); });
  $("restart").addEventListener("click", function () {
    kernel.restart();
    execCounter = 0;
    cells.forEach(function (c) { c.el.querySelector(".exec-count").textContent = ""; });
  });
  $("clear-outputs").addEventListener("click", function () {
    cells.forEach(function (c) { c.output.clear(); });
  });
  document.querySelectorAll("[data-add]").forEach(function (b) {
    b.addEventListener("click", function () {
      var c = createCell({ type: b.dataset.add, source: "" });
      c.editor.focus();
      changed();
    });
  });
  $("delete").addEventListener("click", function () {
    $("delete").hidden = true;
    $("delete-confirm").hidden = false;
  });
  $("delete-no").addEventListener("click", function () {
    $("delete").hidden = false;
    $("delete-confirm").hidden = true;
  });
  $("delete-form").addEventListener("submit", function () { deleting = true; });

  (NB.cells.length ? NB.cells : [{ type: "code", source: "" }]).forEach(function (c) { createCell(c); });
  lastSaved = JSON.stringify(snapshot());
})();
