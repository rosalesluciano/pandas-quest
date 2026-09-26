/* Web Worker: ejecuta Python + pandas con Pyodide sin bloquear la interfaz. */
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/";
importScripts(PYODIDE + "pyodide.js");

let py = null;
const loaded = new Set();

function post(msg) { self.postMessage(msg); }

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

const ready = boot().catch((e) => post({ type: "fatal", text: String(e) }));

const NAMES = { "scikit-learn": "scikit-learn", matplotlib: "matplotlib", micropip: "micropip", sqlite3: "sqlite3", seaborn: "seaborn" };

async function ensure(packages = [], pip = []) {
  const pk = packages.filter((p) => !loaded.has(p));
  if (pk.length) {
    post({ type: "status", text: `Cargando ${pk.map((p) => NAMES[p] || p).join(", ")}…` });
    await py.loadPackage(pk);
    pk.forEach((p) => loaded.add(p));
  }
  const pp = pip.filter((p) => !loaded.has(p));
  if (pp.length) {
    post({ type: "status", text: `Instalando ${pp.join(", ")}…` });
    const micropip = py.pyimport("micropip");
    for (const p of pp) { await micropip.install(p); loaded.add(p); }
    micropip.destroy();
  }
  if (pk.length || pp.length) post({ type: "ready" });
}

self.onmessage = async (ev) => {
  const m = ev.data;
  await ready;
  try {
    let out;
    if (m.type === "load") {
      await ensure(m.packages, m.pip);
      out = "{}";
    } else {
      await ensure(m.packages, m.pip);
      const fn = py.globals.get(m.type === "run" ? "pq_run" : "pq_tables");
      out = m.type === "run"
        ? fn(m.setup, m.code, m.solution, JSON.stringify(m.check || {}), m.doCheck !== false)
        : fn(m.setup, JSON.stringify(m.names));
      fn.destroy();
    }
    post({ type: "result", id: m.id, data: JSON.parse(out) });
  } catch (e) {
    post({ type: "result", id: m.id, data: { error: { msg: String(e), line: null, tip: "Si el error es de descarga, revisa tu conexión y recarga la página." } } });
  }
};
