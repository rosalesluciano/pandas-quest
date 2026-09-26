/* Web Worker: ejecuta Python + pandas con Pyodide sin bloquear la interfaz. */
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/";
importScripts(PYODIDE + "pyodide.js");

let py = null;
let sqlLoaded = false;

async function boot() {
  post({ type: "status", text: "Descargando Python…" });
  py = await loadPyodide({ indexURL: PYODIDE });
  post({ type: "status", text: "Cargando pandas…" });
  await py.loadPackage(["pandas"]);
  const [core, web] = await Promise.all([
    fetch("../py/pq_core.py").then((r) => r.text()),
    fetch("../py/pq_web.py").then((r) => r.text()),
  ]);
  py.runPython(core);
  py.runPython(web);
  post({ type: "ready" });
}

function post(msg) { self.postMessage(msg); }

const ready = boot().catch((e) => post({ type: "fatal", text: String(e) }));

self.onmessage = async (ev) => {
  const m = ev.data;
  await ready;
  try {
    if (m.sql && !sqlLoaded) {
      await py.loadPackage(["sqlite3"]);
      sqlLoaded = true;
    }
    let out;
    if (m.type === "run") {
      const fn = py.globals.get("pq_run");
      out = fn(m.setup, m.code, m.solution, JSON.stringify(m.check || {}), m.doCheck !== false);
      fn.destroy();
    } else if (m.type === "tables") {
      const fn = py.globals.get("pq_tables");
      out = fn(m.setup, JSON.stringify(m.names));
      fn.destroy();
    }
    post({ type: "result", id: m.id, data: JSON.parse(out) });
  } catch (e) {
    post({ type: "result", id: m.id, data: { error: { msg: String(e), line: null, tip: "" } } });
  }
};
