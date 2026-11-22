/* Shared pieces for the practice pages: the Python kernel (a Pyodide worker), the code editor,
   cell output areas and a small JSON helper. Exposed as window.Grind. */
(function () {
  "use strict";

  var CFG = window.GRIND_PRACTICE || {};
  var CSRF = (document.querySelector('meta[name="csrf-token"]') || {}).content;

  // ---------- server calls ----------
  function api(url, body, keepalive) {
    return fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": CSRF },
      body: JSON.stringify(body || {}),
      credentials: "same-origin",
      keepalive: !!keepalive,
    }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    });
  }

  // ---------- kernel ----------
  function Kernel(onStatus) {
    this.onStatus = onStatus || function () {};
    this.pending = {};
    this.nextId = 1;
    this.status = "idle";
    this.start();
  }

  Kernel.prototype.setStatus = function (status, detail) {
    this.status = status;
    this.onStatus(status, detail);
  };

  Kernel.prototype.start = function () {
    var self = this;
    this.setStatus("loading");
    this.worker = new Worker(CFG.workerURL);
    this.ready = new Promise(function (resolve, reject) {
      self.worker.onmessage = function (e) {
        var m = e.data;
        if (m.type === "ready") { self.version = m.version; self.setStatus("ready", m.version); resolve(); return; }
        if (m.type === "init_error") { self.setStatus("error", m.value.error); reject(new Error(m.value.error)); return; }
        var p = self.pending[m.id];
        if (!p) return;
        if (m.type === "stream") { if (p.onStream) p.onStream(m.kind, m.text); return; }
        if (m.type === "done") {
          delete self.pending[m.id];
          clearTimeout(p.timer);
          if (!Object.keys(self.pending).length) self.setStatus("ready", self.version);
          p.resolve(m.value || {});
        }
      };
      self.worker.onerror = function (e) {
        self.setStatus("error", e.message || "Python failed to start");
        reject(new Error(e.message));
      };
    });
    this.ready.catch(function () {});
    this.worker.postMessage({ cmd: "init", indexURL: CFG.pyodideURL, runnerURL: CFG.runnerURL });
  };

  Kernel.prototype.send = function (msg, opts) {
    var self = this;
    opts = opts || {};
    return this.ready.then(function () {
      return new Promise(function (resolve, reject) {
        var id = self.nextId++;
        var p = { resolve: resolve, reject: reject, onStream: opts.onStream };
        if (opts.timeoutMs) {
          p.timer = setTimeout(function () { self.interrupt("timeout"); }, opts.timeoutMs);
        }
        self.pending[id] = p;
        self.setStatus("busy");
        msg.id = id;
        self.worker.postMessage(msg);
      });
    });
  };

  Kernel.prototype.run = function (code, opts) {
    opts = opts || {};
    return this.send({ cmd: "run", code: code, ns: opts.ns, stdin: opts.stdin }, opts);
  };

  Kernel.prototype.grade = function (code, groups, opts) {
    return this.send({ cmd: "grade", code: code, groups: groups }, opts);
  };

  Kernel.prototype.reset = function (ns) {
    return this.send({ cmd: "reset", ns: ns });
  };

  /* Stop whatever is running. A busy WebAssembly thread can't be interrupted politely, so the
     worker is terminated and a fresh one started; every variable is lost. */
  Kernel.prototype.interrupt = function (reason) {
    var pending = this.pending;
    this.pending = {};
    this.worker.terminate();
    Object.keys(pending).forEach(function (id) {
      clearTimeout(pending[id].timer);
      pending[id].resolve({ interrupted: reason || "stopped" });
    });
    this.start();
  };

  Kernel.prototype.restart = function () { this.interrupt("restart"); };

  // ---------- output area ----------
  var MAX_OUTPUT = 100000;

  function Output(el) {
    this.el = el;
    this.clear();
  }
  Output.prototype.clear = function () {
    this.el.innerHTML = "";
    this.el.hidden = true;
    this.size = 0;
    this.truncated = false;
    this.last = null;
  };
  Output.prototype.append = function (kind, text) {
    if (this.truncated) return;
    if (this.size + text.length > MAX_OUTPUT) {
      text = text.slice(0, Math.max(0, MAX_OUTPUT - this.size));
      this.truncated = true;
    }
    this.size += text.length;
    this.el.hidden = false;
    if (!this.last || this.last.dataset.kind !== kind) {
      this.last = document.createElement("span");
      this.last.className = "out-" + kind;
      this.last.dataset.kind = kind;
      this.el.appendChild(this.last);
    }
    this.last.textContent += text;
    if (this.truncated) this.note("Output truncated at " + MAX_OUTPUT.toLocaleString() + " characters.");
  };
  Output.prototype.result = function (value) {
    if (this.size && !/\n$/.test(this.el.textContent)) this.append("stdout", "\n");
    this.last = null;
    this.append("result", value);
  };
  Output.prototype.error = function (text) {
    if (this.size && !/\n$/.test(this.el.textContent)) this.append("stdout", "\n");
    this.last = null;
    this.append("error", text);
  };
  Output.prototype.note = function (text) {
    this.el.hidden = false;
    var n = document.createElement("div");
    n.className = "out-note";
    n.textContent = text;
    this.el.appendChild(n);
    this.last = null;
  };
  Output.prototype.show = function (value) {
    if (value.interrupted === "timeout") this.note("Stopped: it ran too long (infinite loop?). Python was restarted.");
    else if (value.interrupted) this.note("Stopped. Python was restarted, so earlier variables are gone.");
    if (value.error) this.error(value.error);
    if (value.result != null) this.result(value.result);
  };

  // ---------- editor ----------
  function Editor(textarea, opts) {
    opts = opts || {};
    this.listeners = [];
    var self = this;
    var keys = {};
    function bind(names, fn) { names.forEach(function (k) { keys[k] = fn; }); }
    if (window.CodeMirror) {
      bind(["Ctrl-Enter", "Cmd-Enter"], function () { opts.onRun && opts.onRun(); });
      bind(["Shift-Enter"], function () { (opts.onRunAdvance || opts.onRun || function () {})(); });
      bind(["Ctrl-/", "Cmd-/"], "toggleComment");
      keys.Tab = function (cm) {
        if (cm.somethingSelected()) cm.indentSelection("add");
        else cm.replaceSelection("    ", "end");
      };
      keys["Shift-Tab"] = function (cm) { cm.indentSelection("subtract"); };
      if (opts.extraKeys) Object.keys(opts.extraKeys).forEach(function (k) { keys[k] = opts.extraKeys[k]; });
      this.cm = CodeMirror.fromTextArea(textarea, {
        mode: opts.mode || "python",
        lineNumbers: opts.lineNumbers !== false,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        matchBrackets: true,
        autoCloseBrackets: true,
        lineWrapping: !!opts.lineWrapping,
        viewportMargin: Infinity,
        readOnly: !!opts.readOnly,
        extraKeys: keys,
      });
      this.cm.on("change", function () { self.emit(); });
      this.cm.on("focus", function () { opts.onFocus && opts.onFocus(); });
    } else {
      // CDN unavailable: plain textarea that still handles Tab and the run shortcuts.
      this.ta = textarea;
      textarea.classList.add("plain-editor");
      textarea.spellcheck = false;
      textarea.readOnly = !!opts.readOnly;
      textarea.addEventListener("input", function () { self.emit(); });
      textarea.addEventListener("focus", function () { opts.onFocus && opts.onFocus(); });
      textarea.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); opts.onRun && opts.onRun(); }
        else if (e.key === "Enter" && e.shiftKey) { e.preventDefault(); (opts.onRunAdvance || opts.onRun || function () {})(); }
        else if (e.key === "Tab" && !e.shiftKey) {
          e.preventDefault();
          var s = textarea.selectionStart;
          textarea.setRangeText("    ", s, textarea.selectionEnd, "end");
          self.emit();
        }
      });
    }
  }
  Editor.prototype.emit = function () { var v = this.getValue(); this.listeners.forEach(function (f) { f(v); }); };
  Editor.prototype.onChange = function (fn) { this.listeners.push(fn); };
  Editor.prototype.getValue = function () { return this.cm ? this.cm.getValue() : this.ta.value; };
  Editor.prototype.setValue = function (v) { if (this.cm) this.cm.setValue(v); else { this.ta.value = v; this.emit(); } };
  Editor.prototype.focus = function () { if (this.cm) this.cm.focus(); else this.ta.focus(); };
  Editor.prototype.refresh = function () { if (this.cm) this.cm.refresh(); };
  Editor.prototype.wrapper = function () { return this.cm ? this.cm.getWrapperElement() : this.ta; };

  // ---------- kernel status pill ----------
  function statusText(status, detail) {
    return {
      loading: "Starting Python…",
      ready: "Python " + (detail || "") + " ready",
      busy: "Running…",
      error: "Python failed to load: " + (detail || "check your connection"),
    }[status] || status;
  }

  function debounce(fn, ms) {
    var t;
    var wrapped = function () {
      var args = arguments;
      clearTimeout(t);
      t = setTimeout(function () { t = null; fn.apply(null, args); }, ms);
    };
    wrapped.flush = function () { if (t) { clearTimeout(t); t = null; fn(); } };
    return wrapped;
  }

  window.Grind = { api: api, Kernel: Kernel, Output: Output, Editor: Editor, statusText: statusText, debounce: debounce };
})();
