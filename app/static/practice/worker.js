/* Web Worker that hosts Pyodide (CPython compiled to WebAssembly).
   User code runs here, in the browser, never on the server. Running in a worker keeps the page
   responsive, and lets the page stop an infinite loop by terminating the worker. */
"use strict";

let pyodide = null;
let runner = null;

function post(msg) { self.postMessage(msg); }

async function init(indexURL, runnerURL) {
  importScripts(indexURL + "pyodide.js");
  pyodide = await loadPyodide({ indexURL: indexURL });
  const src = await (await fetch(runnerURL)).text();
  pyodide.FS.writeFile("/home/pyodide/grind_runner.py", src);
  pyodide.runPython("import sys; sys.path.insert(0, '/home/pyodide')");
  runner = pyodide.pyimport("grind_runner");
  const version = pyodide.runPython("import sys; sys.version.split()[0]");
  post({ type: "ready", version: version });
}

function toJs(proxy) {
  const value = proxy.toJs({ dict_converter: Object.fromEntries });
  proxy.destroy();
  return value;
}

self.onmessage = async function (e) {
  const m = e.data;
  try {
    if (m.cmd === "init") {
      await init(m.indexURL, m.runnerURL);
      return;
    }
    const emit = (kind, text) => post({ id: m.id, type: "stream", kind: kind, text: text });
    if (m.cmd === "run") {
      post({ id: m.id, type: "done", value: toJs(runner.run_cell(m.code, m.ns || "default", m.stdin || "", emit)) });
    } else if (m.cmd === "grade") {
      const groups = pyodide.toPy(m.groups);
      const res = runner.grade(m.code, groups, emit);
      groups.destroy();
      post({ id: m.id, type: "done", value: toJs(res) });
    } else if (m.cmd === "reset") {
      runner.reset(m.ns === undefined ? null : m.ns);
      post({ id: m.id, type: "done", value: null });
    }
  } catch (err) {
    post({ id: m.id, type: m.cmd === "init" ? "init_error" : "done", value: { error: String(err && err.message || err) } });
  }
};
