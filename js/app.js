/* PandasQuest · Red de Subte - app principal */
(() => {
  "use strict";

  const D = window.PQ;
  const $ = (s, el = document) => el.querySelector(s);
  const app = $("#app");

  /* ---------- Datos derivados ---------- */
  const ALL = [];
  D.modules.forEach((m, mi) => {
    m.num = m.id.slice(1);
    m.ink = inkFor(m.color);
    m.exercises.forEach((e, ei) => ALL.push(Object.assign(e, { mod: m, mi, ei })));
  });
  const BY_ID = Object.fromEntries(ALL.map((e) => [e.id, e]));
  const MOD = Object.fromEntries(D.modules.map((m) => [m.id, m]));
  const TOTAL_XP = ALL.reduce((s, e) => s + e.xp, 0);
  const GOAL = 3;
  const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;

  function inkFor(hex) {
    const n = parseInt(hex.slice(1), 16), r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    return (0.299 * r + 0.587 * g + 0.114 * b) > 170 ? "#1a1400" : "#ffffff";
  }
  const SEP = '<span class="sep" aria-hidden="true">·</span>';
  // El color vivo sale de las variables CSS (--l0…--l6), así el tema oscuro usa sus propios tonos
  const lineVars = (m) => `--c:var(--l${+m.num});--c-ink:${m.ink}`;
  const lineColor = (m) => getComputedStyle(document.documentElement).getPropertyValue(`--l${+m.num}`).trim() || m.color;

  const LEVELS = [
    ["Aprendiz", 0], ["Primer script", 0.04], ["Pythonista", 0.1], ["Analista trainee", 0.2],
    ["Analista jr", 0.32], ["Analista de datos", 0.45], ["Científico de datos jr", 0.6],
    ["Científico de datos", 0.76], ["ML engineer", 0.92],
  ].map(([n, f], i) => ({ n, i: i + 1, xp: Math.round((f * TOTAL_XP) / 10) * 10 }));
  const levelFor = (xp) => LEVELS.reduce((a, L) => (xp >= L.xp ? L : a), LEVELS[0]);

  /* ---------- Estado (localStorage) ---------- */
  const KEY = "pq_state_v2";
  const fresh = () => ({
    xp: 0, solved: {}, attempts: {}, hints: {}, code: {}, streak: { last: null, count: 0 },
    combo: 0, bestCombo: 0, badges: {}, day: { date: null, count: 0, xp: 0 }, sound: false,
    firstTry: 0, noHint: 0, night: false,
  });
  let S = load();
  function load() {
    try { return Object.assign(fresh(), JSON.parse(localStorage.getItem(KEY)) || {}); }
    catch (e) { return fresh(); }
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* sin storage */ } }

  const ymd = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const today = () => ymd(new Date());
  const yesterday = () => { const d = new Date(); d.setDate(d.getDate() - 1); return ymd(d); };
  const streakNow = () => (S.streak.last === today() || S.streak.last === yesterday() ? S.streak.count : 0);
  const dayCount = () => (S.day.date === today() ? S.day.count : 0);
  const dayXP = () => (S.day.date === today() ? S.day.xp || 0 : 0);
  const nSolved = () => Object.keys(S.solved).filter((id) => BY_ID[id]).length;
  const modSolved = (m) => m.exercises.filter((e) => S.solved[e.id]).length;
  const modDone = (id) => { const m = MOD[id]; return m && modSolved(m) === m.exercises.length; };
  const nextIn = (m) => m.exercises.find((e) => !S.solved[e.id]);
  const nextAll = () => ALL.find((e) => !S.solved[e.id]);

  /* ---------- Logros ---------- */
  const modBadge = (id, n) => ({ id, code: MOD[id].num, mod: id, n, d: `Completa la línea ${MOD[id].title}`, ok: () => modDone(id) });
  const BADGES = [
    { id: "first", code: "1", n: "Primer viaje", d: "Resuelve tu primer ejercicio", ok: () => nSolved() >= 1 },
    { id: "ten", code: "10", n: "Pasajero frecuente", d: "Resuelve 10 ejercicios", ok: () => nSolved() >= 10 },
    { id: "combo5", code: "x5", n: "Imparable", d: "Combo x5 al primer intento", ok: () => S.bestCombo >= 5 },
    { id: "combo10", code: "x10", n: "Modo leyenda", d: "Combo x10 al primer intento", ok: () => S.bestCombo >= 10 },
    { id: "goal", code: `${GOAL}/${GOAL}`, n: "Meta cumplida", d: `${GOAL} ejercicios en un día`, ok: () => dayCount() >= GOAL },
    { id: "streak3", code: "3d", n: "En racha", d: "3 días seguidos", ok: () => streakNow() >= 3 },
    { id: "streak7", code: "7d", n: "Hábito de hierro", d: "7 días seguidos", ok: () => streakNow() >= 7 },
    { id: "nohint", code: "15", n: "Sin ayuda", d: "15 ejercicios sin pistas", ok: () => S.noHint >= 15 },
    modBadge("m00", "Base de Python"), modBadge("m01", "Pandero"), modBadge("m02", "Domador de tablas"),
    modBadge("m03", "Mente matricial"), modBadge("m04", "Pintor de datos"), modBadge("m05", "Estadista visual"),
    modBadge("m06", "Primer modelo"),
    { id: "night", code: "0h", n: "Búho", d: "Resuelve algo entre 00:00 y 05:00", ok: () => S.night },
    { id: "all", code: "7/7", n: "Red completa", d: "Termina todas las líneas", ok: () => nSolved() === ALL.length },
  ];

  /* ---------- Sonido (apagado por defecto) ---------- */
  let actx;
  function tone(freqs, dur = 0.14, type = "sine", gap = 0.07, vol = 0.09) {
    if (!S.sound) return;
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      const t0 = actx.currentTime + 0.01;
      freqs.forEach((f, i) => {
        const o = actx.createOscillator(), g = actx.createGain();
        o.type = type; o.frequency.value = f;
        const st = t0 + i * gap;
        g.gain.setValueAtTime(0.0001, st);
        g.gain.exponentialRampToValueAtTime(vol, st + 0.015);
        g.gain.exponentialRampToValueAtTime(0.0001, st + dur);
        o.connect(g).connect(actx.destination);
        o.start(st); o.stop(st + dur + 0.03);
      });
    } catch (e) { /* sin audio */ }
  }
  // "Ding-dong" de estación para acertar, grave para errar.
  const SFX = {
    ok: () => tone([784, 659], 0.32, "sine", 0.18),
    bad: () => tone([220, 196], 0.18, "triangle", 0.1, 0.06),
    level: () => tone([659, 784, 988, 1319], 0.3, "sine", 0.1),
    badge: () => tone([988, 1319], 0.22, "sine", 0.09),
  };

  /* ---------- Utilidades ---------- */
  const ico = (name, cls = "") => `<svg class="ic ${cls}" aria-hidden="true"><use href="#i-${name}"/></svg>`;
  function esc(s) { return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
  function inline(raw) {
    return raw.split("`").map((seg, i) => (i % 2
      ? `<code>${esc(seg)}</code>`
      : esc(seg).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/(^|[^*])\*([^*\s](?:[^*]*[^*\s])?)\*/g, "$1<i>$2</i>"))).join("");
  }
  function codeBlock(code, lang) {
    const pre = document.createElement("pre");
    const c = document.createElement("code");
    pre.appendChild(c);
    if (window.CodeMirror && CodeMirror.runMode) CodeMirror.runMode(code, lang === "sql" ? "text/x-sql" : "python", c);
    else c.textContent = code;
    return pre.outerHTML;
  }
  const CALLOUT = { "⚠️": ["warn", "alert"], "💼": ["work", "briefcase"], "💡": ["tip", "bulb"] };
  function callout(t) {
    const m = t.match(/^(⚠️|💼|💡)\s*/);
    const [kind, icon] = m ? CALLOUT[m[1]] : ["tip", "info"];
    let body = m ? t.slice(m[0].length) : t;
    let label = "";
    const lm = body.match(/^\*\*(.+?):\*\*\s*/);
    if (lm) { label = lm[1]; body = body.slice(lm[0].length); }
    return `<div class="callout ${kind}">${ico(icon)}<div>${label ? `<span class="c-lbl">${esc(label)}:</span>` : ""}${inline(body)}</div></div>`;
  }
  function md(src) {
    const out = [], lines = src.split("\n");
    let para = [], i = 0;
    const flush = () => { if (para.length) { out.push(`<p>${inline(para.join(" "))}</p>`); para = []; } };
    const LI = /^\s*(?:-|\d+\.)\s+(.*)$/;
    while (i < lines.length) {
      const l = lines[i];
      if (l.startsWith("```")) {
        flush();
        const lang = l.slice(3).trim() || "python", buf = [];
        i++;
        while (i < lines.length && !lines[i].startsWith("```")) buf.push(lines[i++]);
        i++;
        out.push(codeBlock(buf.join("\n"), lang));
        continue;
      }
      if (/^\s*\|/.test(l)) {
        flush();
        const rows = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) rows.push(lines[i++]);
        const cells = (r) => r.trim().replace(/^\||\|$/g, "").split(/(?<!\\)\|/).map((c) => inline(c.trim().replace(/\\\|/g, "|")));
        const body = rows.filter((r) => !/^\s*\|[\s:|-]+\|\s*$/.test(r));
        const [head, ...rest] = body;
        out.push(`<div class="md-table"><table><thead><tr>${cells(head).map((c) => `<th>${c}</th>`).join("")}</tr></thead><tbody>${rest.map((r) => `<tr>${cells(r).map((c) => `<td>${c}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);
        continue;
      }
      if (l.startsWith("> ")) {
        flush();
        const buf = [];
        while (i < lines.length && lines[i].startsWith("> ")) buf.push(lines[i++].slice(2));
        out.push(callout(buf.join(" ")));
        continue;
      }
      if (LI.test(l)) {
        flush();
        const ordered = /^\s*\d+\./.test(l), items = [];
        while (i < lines.length && LI.test(lines[i])) items.push(`<li>${inline(lines[i++].match(LI)[1])}</li>`);
        out.push(ordered ? `<ol>${items.join("")}</ol>` : `<ul>${items.join("")}</ul>`);
        continue;
      }
      if (!l.trim()) { flush(); i++; continue; }
      para.push(l); i++;
    }
    flush();
    return out.join("");
  }

  /* ---------- Toasts y diálogo ---------- */
  function toast(mark, title, sub = "", m = null) {
    const t = document.createElement("div");
    t.className = "toast";
    if (m) t.style.cssText = lineVars(m);
    t.innerHTML = `<span class="t-ic">${mark}</span><div><b>${esc(title)}</b>${sub ? `<small>${esc(sub)}</small>` : ""}</div>`;
    $("#toasts").appendChild(t);
    setTimeout(() => { t.classList.add("out"); setTimeout(() => t.remove(), 320); }, 4200);
  }
  const dlg = $("#dlg");
  function openDialog(html, onOpen) {
    $("#dlgCard").innerHTML = html;
    $("#dlgCard").querySelectorAll("[data-close]").forEach((b) => b.addEventListener("click", () => dlg.close()));
    if (!dlg.open) dlg.showModal();
    if (onOpen) onOpen($("#dlgCard"));
  }
  dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
  function floatXP(el, text) {
    if (!el) return;
    const r = el.getBoundingClientRect();
    const f = document.createElement("div");
    f.className = "float-xp"; f.textContent = text;
    f.style.left = `${r.left + r.width / 2 - 26}px`; f.style.top = `${r.top - 8}px`;
    document.body.appendChild(f);
    setTimeout(() => f.remove(), 1400);
  }

  /* ---------- Python (Web Worker + Pyodide) ---------- */
  let worker, pyReady = false, seq = 0;
  const pending = new Map(), waiters = [];
  const libsReady = new Set();
  function setPy(state, text) {
    const el = $("#pyStatus");
    el.className = "py-status " + state;
    $(".txt", el).textContent = text;
    el.title = text;
  }
  function startWorker() {
    pyReady = false;
    libsReady.clear();
    setPy("", "Cargando Python…");
    worker = new Worker("js/worker.js");
    worker.onmessage = (ev) => {
      const m = ev.data;
      if (m.type === "status") setPy("", m.text);
      else if (m.type === "ready") { pyReady = true; setPy("ready", "Python listo"); waiters.splice(0).forEach((f) => f()); }
      else if (m.type === "fatal") setPy("error", "Python no cargó");
      else if (m.type === "result") {
        const p = pending.get(m.id);
        if (p) { pending.delete(m.id); clearTimeout(p.t); p.res(m.data); }
      }
    };
    worker.onerror = () => setPy("error", "Python no cargó");
  }
  const whenReady = () => (pyReady ? Promise.resolve() : new Promise((r) => waiters.push(r)));
  async function py(msg, timeout = 30000) {
    await whenReady();
    return new Promise((res) => {
      const id = ++seq;
      const t = setTimeout(() => {
        pending.delete(id);
        worker.terminate();
        pending.forEach((p) => { clearTimeout(p.t); p.res({ error: { msg: "Python se reinició" } }); });
        pending.clear();
        startWorker();
        res({ error: { msg: "Tu código tardó demasiado. ¿Hay un bucle infinito?", line: null, tip: "Python se reinició solo. Revisa el código y vuelve a ejecutar." } });
      }, timeout);
      pending.set(id, { res, t });
      worker.postMessage(Object.assign({ id }, msg));
    });
  }
  const setupFor = (m) => D.setup + (m.setup || "");
  const libMsg = (m) => ({ packages: m.packages || [], pip: m.micropip || [] });
  async function ensureMod(m) {
    if (!((m.packages && m.packages.length) || (m.micropip && m.micropip.length)) || libsReady.has(m.id)) return {};
    const r = await py(Object.assign({ type: "load" }, libMsg(m)), 300000);
    if (!r.error) libsReady.add(m.id);
    return r;
  }

  /* ---------- Barra de instrumentos ---------- */
  function updateTop() {
    const L = levelFor(S.xp), next = LEVELS[L.i] || null;
    const pct = next ? ((S.xp - L.xp) / (next.xp - L.xp)) * 100 : 100;
    $(".lvl-num").textContent = L.i;
    $(".lvl-name").textContent = L.n;
    $(".xpbar i").style.transform = `scaleX(${Math.max(3, Math.min(100, pct)) / 100})`;
    $(".xp-num").textContent = S.xp;
    const dx = dayXP();
    $(".xp-trend").textContent = dx ? `+${dx} hoy` : "";
    $("#levelPill").setAttribute("aria-label", `Nivel ${L.i}, ${L.n}, ${S.xp} XP. ${next ? `Faltan ${next.xp - S.xp} XP para ${next.n}.` : "Nivel máximo."} Ver niveles`);
    const st = streakNow();
    $(".streak-num").textContent = st;
    const ss = $(".streak-state");
    const doneToday = S.streak.last === today();
    ss.textContent = st ? (doneToday ? "hoy listo" : "falta hoy") : "";
    ss.className = "streak-state " + (doneToday ? "done" : "pending");
    const dc = Math.min(dayCount(), GOAL);
    $(".goal-num").textContent = dayCount();
    document.querySelectorAll("#goalChip .ticks i").forEach((t, i) => t.classList.toggle("on", i < dc));
    const cc = $("#comboChip");
    cc.classList.toggle("hidden", S.combo < 2);
    $("b", cc).textContent = S.combo;
    $("#soundBtn").innerHTML = `<svg class="ic"><use href="#i-${S.sound ? "sound" : "mute"}"/></svg>`;
    $("#soundBtn").setAttribute("aria-label", S.sound ? "Silenciar sonido" : "Activar sonido");
    const dark = document.documentElement.dataset.theme === "dark";
    $("#themeBtn").innerHTML = `<svg class="ic"><use href="#i-${dark ? "sun" : "moon"}"/></svg>`;
    $("#themeBtn").setAttribute("aria-label", dark ? "Cambiar a tema claro" : "Cambiar a tema oscuro");
  }
  $("#soundBtn").addEventListener("click", () => { S.sound = !S.sound; save(); updateTop(); if (S.sound) SFX.badge(); });
  $("#themeBtn").addEventListener("click", () => {
    const t = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem("pq_theme", t); } catch (e) { /* */ }
    updateTop();
    if (!location.hash.startsWith("#/e/") && !location.hash.startsWith("#/m/")) drawMap();
  });
  $("#levelPill").addEventListener("click", () => {
    const L = levelFor(S.xp);
    openDialog(`<div class="dlg-top"><h2>Tu camino profesional</h2><button class="btn small" data-close>Cerrar</button></div>
      <p style="color:var(--ink-2);margin-bottom:14px">Ganas XP al resolver ejercicios. Tres aciertos seguidos al primer intento activan el combo (x1,5 desde 3 y x2 desde 5). Usar una pista deja el ejercicio en 50% del XP; ver la solución, en 25%.</p>
      <ol class="levels">${LEVELS.map((l) => `<li class="${S.xp >= l.xp ? "got" : ""} ${l === L ? "cur" : ""}"><span class="ln">${l.i}</span><span>${esc(l.n)}${l === L ? " · tu nivel" : ""}</span><span class="xp-tag">${l.xp} XP</span></li>`).join("")}</ol>`);
  });

  /* ---------- Router ---------- */
  let cm = null;
  function route() {
    const parts = (location.hash.slice(1) || "/").split("/").filter(Boolean);
    cm = null;
    if (dlg.open) dlg.close();
    if (parts[0] === "e" && BY_ID[parts[1]]) renderExercise(BY_ID[parts[1]]);
    else if (parts[0] === "m" && MOD[parts[1]]) renderModule(MOD[parts[1]]);
    else renderHome();
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", route);

  /* ---------- Vista: Inicio (mapa de la red) ---------- */
  function renderHome() {
    document.title = "PandasQuest · Aprende ciencia de datos desde cero";
    const next = nextAll();
    const done = nSolved();
    const unlocked = BADGES.filter((b) => S.badges[b.id]).length;
    const m = next ? next.mod : D.modules[D.modules.length - 1];
    const plaque = next
      ? `<div class="np-label"><span class="badge-line" style="${lineVars(m)}">${m.num}</span><span>Línea ${m.num}${SEP}${esc(m.title)}</span></div>
         <h2 class="np-title">${esc(next.title)}</h2>
         <div class="np-meta"><span>${esc(D.levelNames[next.level])}${SEP}estación <b>${next.ei + 1}</b> de ${m.exercises.length}</span><b>+${next.xp} XP</b></div>
         <p class="np-sec">Tu próxima estación, en la sección <b>${esc(next.sec)}</b>.</p>
         <div class="np-actions" style="${lineVars(m)}">
           <a class="btn primary" href="#/e/${next.id}">${done ? "Seguir viaje" : "Empezar el viaje"} ${ico("arrow")}</a>
           <a class="btn" href="${m.colab}" target="_blank" rel="noopener">Abrir la línea en Colab ${ico("out")}</a>
         </div>`
      : `<h2 class="np-title">Recorriste toda la red</h2>
         <p class="np-sec">Completaste los ${ALL.length} ejercicios. Repasa cualquier estación desde el mapa.</p>
         <div class="np-actions"><a class="btn primary" href="#/m/m06">Repasar Machine Learning ${ico("arrow")}</a></div>`;
    app.innerHTML = `<div class="wrap view">
      <div class="home-grid">
        <aside class="next-plaque" aria-label="Próxima estación">
          ${plaque}
          <div class="np-total">
            <div><b>${done}</b><span>de ${ALL.length} estaciones</span></div>
            <div><b>${D.modules.filter((x) => modDone(x.id)).length}</b><span>de ${D.modules.length} líneas</span></div>
            <div><b>${unlocked}</b><span>de ${BADGES.length} logros</span></div>
          </div>
        </aside>
        <section class="map-card" aria-labelledby="mapTitle">
          <div class="map-head"><h1 id="mapTitle">Red de ciencia de datos</h1><p>De tu primera variable a tu primer modelo de Machine Learning</p></div>
          <div id="mapBox"></div>
          <div class="map-legend" aria-hidden="true">
            <span><i class="lg-dot done"></i>Resuelta</span>
            <span><i class="lg-dot"></i>Pendiente</span>
            <span><i class="lg-train"></i>Estás aquí</span>
            <span><i class="lg-xfer"></i>Combinación entre líneas</span>
          </div>
        </section>
      </div>
      <div class="home-lower">
        <section class="panel how">
          <div class="sec-h"><h2>Cómo se viaja</h2></div>
          <ol>
            <li><span class="step-dot">1</span><span><b>Lee la estación</b>Cada ejercicio explica el concepto con ejemplos, usos reales y errores comunes.</span></li>
            <li><span class="step-dot">2</span><span><b>Escribe y ejecuta</b>Python real en tu navegador, sin instalar nada. <kbd class="kbd" style="background:var(--panel-2)">Ctrl+Enter</kbd> ejecuta.</span></li>
            <li><span class="step-dot">3</span><span><b>Sigue a la próxima</b>Cada línea tiene su notebook de Colab con el mismo corrector.</span></li>
          </ol>
        </section>
        <section class="panel pins-wrap">
          <div class="sec-h"><h2>Logros</h2><span>${unlocked} de ${BADGES.length}</span></div>
          ${pinsBoard()}
        </section>
      </div>
      <footer class="foot">
        <span>PandasQuest${SEP}Python, pandas, NumPy, Matplotlib, Seaborn y Machine Learning</span>
        <span><a href="https://github.com/rosalesluciano/pandas-quest" target="_blank" rel="noopener">Código en GitHub</a>${SEP}<button class="reset-link" id="resetBtn" type="button">Reiniciar progreso</button></span>
      </footer>
    </div>`;
    drawMap();
    $("#resetBtn").addEventListener("click", () => {
      if (confirm("¿Borrar todo tu progreso, XP y logros? No se puede deshacer.")) { const snd = S.sound; S = fresh(); S.sound = snd; save(); updateTop(); renderHome(); }
    });
  }

  function pin(b) {
    const mm = b.mod ? MOD[b.mod] : null;
    return `<li class="pin ${S.badges[b.id] ? "unlocked" : "locked"}" ${mm ? `style="${lineVars(mm)}"` : ""}><span class="pin-mark">${esc(b.code)}</span><span><b>${esc(b.n)}</b><small>${esc(b.d)}</small></span></li>`;
  }
  // Conseguidos arriba, los tres más cercanos después y el resto contado en un desplegable
  function pinsBoard() {
    const got = BADGES.filter((b) => S.badges[b.id]);
    const locked = BADGES.filter((b) => !S.badges[b.id]);
    const cur = nextAll();
    const order = (b) => (cur && b.mod === cur.mod.id ? 0 : b.mod ? 2 : 1);
    const soon = locked.slice().sort((x, y) => order(x) - order(y)).slice(0, 3);
    const rest = locked.filter((b) => !soon.includes(b));
    return `${got.length ? `<h3 class="pins-h">Conseguidos</h3><ul class="pins">${got.map(pin).join("")}</ul>` : `<p class="pins-empty">Resuelve tu primer ejercicio para ganar el primer logro.</p>`}
      ${soon.length ? `<h3 class="pins-h">Los próximos</h3><ul class="pins">${soon.map(pin).join("")}</ul>` : ""}
      ${rest.length ? `<details class="pins-more"><summary>Ver ${rest.length} logros más por desbloquear</summary><ul class="pins">${rest.map(pin).join("")}</ul></details>` : ""}`;
  }

  function drawMap() {
    const box = $("#mapBox");
    if (!box) return;
    const W = Math.max(300, Math.round(box.clientWidth));
    const narrow = W < 640;
    const G = narrow
      ? { pad: 30, gap: 74, top: 44, r: 3.6, rNext: 6, track: 5, bulge: 22, lbl: 12.5, badge: 9 }
      : { pad: 44, gap: 92, top: 52, r: 5.5, rNext: 8.5, track: 8, bulge: 30, lbl: 14, badge: 11 };
    const x0 = G.pad, x1 = W - G.pad;
    const H = G.top + (D.modules.length - 1) * G.gap + 34;
    const next = nextAll();
    let rails = "", tracks = "", stations = "", labels = "", train = "", rows = "";
    const ends = [];
    D.modules.forEach((m, i) => {
      const col = lineColor(m);
      const y = G.top + i * G.gap;
      const n = m.exercises.length;
      const ltr = i % 2 === 0;
      const xs = m.exercises.map((_, k) => (n === 1 ? x0 : ltr ? x0 + (k * (x1 - x0)) / (n - 1) : x1 - (k * (x1 - x0)) / (n - 1)));
      ends.push({ y, first: xs[0], last: xs[n - 1] });
      if (narrow) {
        rows += `<a href="#/m/${m.id}" aria-label="${esc(`Línea ${m.num}: ${m.title}, ${modSolved(m)} de ${n} resueltas`)}"><rect x="0" y="${y - G.gap / 2 + 6}" width="${W}" height="${G.gap - 4}" fill="none" pointer-events="all"/></a>`;
      }
      tracks += `<line x1="${xs[0]}" y1="${y}" x2="${xs[n - 1]}" y2="${y}" stroke="${col}" stroke-width="${G.track}" stroke-linecap="round"/>`;
      m.exercises.forEach((e, k) => {
        const solved = !!S.solved[e.id], cur = next === e;
        const r = cur ? G.rNext : G.r;
        const fill = solved ? m.color : "var(--station)";
        const state = solved ? "resuelta" : cur ? "próxima estación" : "pendiente";
        if (narrow) {
          stations += `<circle cx="${xs[k]}" cy="${y}" r="${r}" fill="${fill}" stroke="${col}" stroke-width="${cur ? 3 : 2}" pointer-events="none"/>`;
        } else stations += `<a href="#/e/${e.id}" aria-label="${esc(`Línea ${m.num}, estación ${k + 1}: ${e.title} (${state})`)}"><title>${esc(`${k + 1}. ${e.title}`)}</title>`
          + `<circle cx="${xs[k]}" cy="${y}" r="${narrow ? 9 : 11}" fill="transparent"/>`
          + `<circle class="st" cx="${xs[k]}" cy="${y}" r="${r}" fill="${fill}" stroke="${col}" stroke-width="${cur ? 4 : narrow ? 2 : 3}"/>`
          + (solved && !narrow ? `<circle cx="${xs[k]}" cy="${y}" r="1.6" fill="var(--station)" pointer-events="none"/>` : "") + "</a>";
        if (cur) {
          // El tren va debajo de la vía: así nunca tapa el nombre de la línea
          const tw = narrow ? 18 : 24, th = narrow ? 9 : 11, ty = y + r + 7;
          train = `<g aria-hidden="true"><path d="M${xs[k] - 4} ${ty} h8 l-4 -5z" fill="var(--ink)"/>`
            + `<rect x="${xs[k] - tw / 2}" y="${ty}" width="${tw}" height="${th}" rx="3" fill="var(--ink)"/>`
            + `<rect x="${xs[k] - tw / 2 + 4}" y="${ty + 3}" width="${tw - 8}" height="${Math.max(2, th - 7)}" rx="1" fill="var(--map-bg)" opacity=".85"/></g>`;
        }
      });
      // Etiqueta de línea, del lado donde arranca
      const done = modSolved(m);
      const ly = y - (narrow ? 18 : 24);
      const bx = ltr ? x0 + G.badge - 2 : x1 - G.badge + 2;
      const anchor = ltr ? "start" : "end";
      const tx = ltr ? bx + G.badge + 7 : bx - G.badge - 7;
      labels += `<a class="lblink" href="#/m/${m.id}" aria-label="${esc(`Ver la línea ${m.num}: ${m.title}, ${done} de ${n} resueltas`)}">`
        + `<circle cx="${bx}" cy="${ly}" r="${G.badge}" fill="${col}"/>`
        + `<text class="bnum" x="${bx}" y="${ly + 3.8}" text-anchor="middle" fill="${m.ink}" style="font-size:${G.badge}px">${m.num}</text>`
        + `<text x="${tx}" y="${ly + 4.5}" text-anchor="${anchor}" style="font-size:${G.lbl}px"><tspan class="lbl">${esc(m.title)}</tspan><tspan class="lbl-n" dx="8">${done}/${n}</tspan></text></a>`;
    });
    // Combinaciones: codos a 45° entre el final de una línea y el inicio de la siguiente
    for (let i = 0; i < ends.length - 1; i++) {
      const a = ends[i], b = ends[i + 1];
      const right = i % 2 === 0;
      const x = a.last, dir = right ? 1 : -1, c = 6, d = G.bulge - c;
      rails += `<path d="M${x} ${a.y} h${dir * c} l${dir * d} ${d} V${b.y - d} l${-dir * d} ${d} H${b.first}" fill="none" stroke="var(--rail)" stroke-width="${Math.max(3, G.track - 3)}" stroke-linejoin="round" stroke-linecap="round"/>`;
    }
    let xfers = "";
    for (let i = 0; i < ends.length - 1; i++) {
      [[ends[i].last, ends[i].y], [ends[i + 1].first, ends[i + 1].y]].forEach(([x, y]) => {
        xfers += `<circle cx="${x}" cy="${y}" r="${G.rNext + 1}" fill="var(--station)" stroke="var(--ink)" stroke-width="${narrow ? 2 : 2.5}" pointer-events="none"/>`;
      });
    }
    box.innerHTML = `<svg class="netmap" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="group" aria-label="Mapa de la red: ${D.modules.length} líneas y ${ALL.length} estaciones">${rails}${tracks}${xfers}${stations}${labels}${train}${rows}</svg>`;
  }
  let rsz;
  window.addEventListener("resize", () => { clearTimeout(rsz); rsz = setTimeout(() => { if ($("#mapBox")) drawMap(); }, 150); });

  /* ---------- Vista: Línea (módulo) ---------- */
  function renderModule(m) {
    document.title = `Línea ${m.num} · ${m.title} · PandasQuest`;
    const i = D.modules.indexOf(m), n = modSolved(m), tot = m.exercises.length;
    ensureMod(m);
    const nx = nextIn(m);
    const prevM = D.modules[i - 1], nextM = D.modules[i + 1];
    let rows = "";
    m.exercises.forEach((e, k) => {
      if (k === 0 || e.sec !== m.exercises[k - 1].sec) rows += `<li class="stop-zone ${k === 0 ? "first" : ""}"><span class="trk"></span><h2>${esc(e.sec)}</h2></li>`;
      const solved = !!S.solved[e.id], isNext = e === nx;
      const state = solved ? "Resuelta" : isNext ? "Próxima estación" : `Estación ${k + 1}`;
      rows += `<li class="stop ${solved ? "solved" : ""} ${isNext ? "next" : ""}"><span class="trk"><span class="dot"></span></span>
        <a href="#/e/${e.id}"><span class="t">${esc(e.title)}<small>${solved ? `${ico("check")} ` : ""}${state}</small></span>
        <span class="lvl lvl-${e.level}">${esc(D.levelNames[e.level])}</span><span class="xp-tag">+${e.xp} XP</span></a></li>`;
    });
    app.innerHTML = `<div class="wrap view" style="${lineVars(m)}">
      <nav class="crumbs" aria-label="Ubicación"><a href="#/">Mapa de la red</a><span aria-hidden="true">/</span><span>Línea ${m.num}</span></nav>
      <header class="line-head">
        <span class="badge-line lg">${m.num}</span>
        <div>
          <h1>${esc(m.title)}</h1>
          <p>${esc(m.desc)}</p>
          <div class="line-prog"><span class="bar"><i style="width:${(n / tot) * 100}%"></i></span><span>${n} de ${tot} estaciones resueltas</span></div>
        </div>
        <div class="actions">
          <a class="btn line" href="#/e/${(nx || m.exercises[0]).id}">${n ? (nx ? "Seguir viaje" : "Repasar") : "Empezar la línea"} ${ico("arrow")}</a>
          <a class="btn" href="${m.colab}" target="_blank" rel="noopener">Abrir en Colab ${ico("out")}</a>
        </div>
      </header>
      <div class="line-body">
        <ol class="stops">${rows}</ol>
        <aside class="line-summary" aria-label="Resumen de la línea">
          <h2>Recorrido</h2>
          <ul>${[...new Set(m.exercises.map((e) => e.sec))].map((sec) => {
            const es = m.exercises.filter((e) => e.sec === sec), d = es.filter((e) => S.solved[e.id]).length;
            return `<li class="${d === es.length ? "done" : ""}"><span>${esc(sec)}</span><b class="num">${d}/${es.length}</b></li>`;
          }).join("")}</ul>
          <p>${m.exercises.reduce((t, e) => t + e.xp, 0)} XP en esta línea. ${nextM ? `Al terminar combina con la línea ${nextM.num}${SEP}${esc(nextM.title)}.` : "Es la última línea de la red."}</p>
        </aside>
      </div>
      <nav class="line-nav" aria-label="Otras líneas">
        ${prevM ? `<a class="btn ghost" href="#/m/${prevM.id}">${ico("back")} Línea ${prevM.num}${SEP}${esc(prevM.title)}</a>` : "<span></span>"}
        ${nextM ? `<a class="btn ghost" href="#/m/${nextM.id}">Línea ${nextM.num}${SEP}${esc(nextM.title)} ${ico("arrow")}</a>` : ""}
      </nav>
    </div>`;
  }

  /* ---------- Vista: Estación (ejercicio) ---------- */
  let running = false, errLine = null;
  const tablesCache = {};
  const pct = (k, n) => (n <= 1 ? 50 : (k / (n - 1)) * 100);

  function renderExercise(ex) {
    const m = ex.mod, idx = ALL.indexOf(ex), n = m.exercises.length;
    const prev = ALL[idx - 1], next = ALL[idx + 1];
    document.title = `${ex.title} · Línea ${m.num} · PandasQuest`;
    const solved = !!S.solved[ex.id];
    trainAt = null;
    const hasTables = m.tables && m.tables.length;
    app.innerHTML = `<div class="wrap view" style="${lineVars(m)}">
      <header class="station-sign">
        <div class="ss-top">
          <span class="badge-line">${m.num}</span>
          <div class="ss-title">
            <div class="ss-line"><a href="#/">Mapa</a><span aria-hidden="true">·</span><a href="#/m/${m.id}">Línea ${m.num} ${esc(m.title)}</a><span aria-hidden="true">·</span><span>${esc(ex.sec)}</span></div>
            <h1>${esc(ex.title)}</h1>
          </div>
          <div class="ss-meta">
            <span class="xp-tag num">${ex.ei + 1}/${n}</span>
            <span class="lvl">${esc(D.levelNames[ex.level])}</span>
            <span class="xp-tag">+${ex.xp} XP</span>
            <span id="stateTag">${solved ? `<span class="state-tag">${ico("check")}Resuelta</span>` : ""}</span>
          </div>
        </div>
        <div class="strip" aria-label="Estaciones de la línea ${m.num}">
          <span class="strip-track"></span>
          ${m.exercises.map((e, k) => `<a class="strip-st ${S.solved[e.id] ? "solved" : ""} ${e === ex ? "current" : ""}" href="#/e/${e.id}" style="left:${pct(k, n)}%" aria-label="${esc(`Estación ${k + 1}: ${e.title}${S.solved[e.id] ? " (resuelta)" : ""}`)}" title="${esc(`${k + 1}. ${e.title}`)}"></a>`).join("")}
          <span class="train" id="train" aria-hidden="true" style="transform:translateX(0)"></span>
        </div>
        <div class="ss-ends">
          ${prev ? `<a href="#/e/${prev.id}">${ico("back")}<span>${esc(prev.title)}</span></a>` : "<span></span>"}
          ${next ? `<a href="#/e/${next.id}"><span>${esc(next.title)}</span>${ico("arrow")}</a>` : `<a href="#/">Mapa de la red ${ico("arrow")}</a>`}
        </div>
      </header>
      <div class="ex-grid">
        <article class="panel lesson">
          <div class="md">${md(ex.theory)}</div>
          <section class="mission" aria-labelledby="missionH"><h2 id="missionH">${ico("target")}Tu misión</h2><div class="md">${md(ex.task)}</div></section>
          <div class="tools">
            <button class="btn small" id="hintBtn" type="button">${ico("bulb")}Pista</button>
            <button class="btn small" id="solBtn" type="button">${ico("eye")}Solución</button>
            ${hasTables ? `<button class="btn small" id="tablesBtn" type="button">${ico("table")}Tablas</button>` : ""}
            <a class="btn small ghost" href="${m.colab}" target="_blank" rel="noopener">Colab ${ico("out")}</a>
          </div>
          <div id="hintArea"></div>
        </article>
        <section class="workspace" aria-label="Editor y resultado">
          <div class="panel editor-card">
            <div class="editor-head">
              <span class="file-tab"><i></i>${m.id === "m06" ? "modelo" : m.id === "m00" ? "script" : m.title.toLowerCase().replace(/\s+/g, "_")}.py</span>
              <div class="editor-actions">
                <button class="btn small ghost" id="resetCode" type="button" title="Volver al código inicial">${ico("undo")}Reiniciar</button>
                <button class="btn small line" id="runBtn" type="button">${ico("play", "fill")}Ejecutar <span class="kbd">Ctrl+Enter</span></button>
              </div>
            </div>
            <div id="editor"></div>
          </div>
          <div class="panel output">
            <div class="out-head"><span>Resultado</span><span id="outInfo"></span></div>
            <div class="run-bar" id="runBar"></div>
            <div class="out-body" id="out">
              <div class="placeholder"><span class="ph-ic">${ico("play", "fill")}</span>Escribe tu código y pulsa <b>Ejecutar</b> (o <b>Ctrl + Enter</b>).<br>Guarda tu respuesta en la variable <code>resultado</code>.</div>
            </div>
          </div>
        </section>
      </div>
    </div>`;

    placeTrain(ex, false);
    const saved = S.code[ex.id];
    cm = CodeMirror($("#editor"), {
      value: saved != null ? saved : ex.starter,
      mode: "python", lineNumbers: true, indentUnit: 4, tabSize: 4,
      matchBrackets: true, autoCloseBrackets: true, viewportMargin: Infinity,
      extraKeys: {
        "Ctrl-Enter": () => run(ex), "Cmd-Enter": () => run(ex),
        "Ctrl-/": "toggleComment", "Cmd-/": "toggleComment",
        Tab: (c) => (c.somethingSelected() ? c.indentSelection("add") : c.replaceSelection("    ")),
      },
    });
    const last = cm.lastLine();
    cm.setCursor(last, cm.getLine(last).length);
    setTimeout(() => { if (!cm) return; cm.refresh(); if (matchMedia("(min-width: 1041px)").matches) cm.focus(); }, 30);
    let tmr;
    cm.on("change", () => {
      clearErrLine();
      clearTimeout(tmr);
      tmr = setTimeout(() => { S.code[ex.id] = cm.getValue(); save(); }, 400);
    });

    $("#runBtn").addEventListener("click", () => run(ex));
    $("#resetCode").addEventListener("click", () => { cm.setValue(ex.starter); delete S.code[ex.id]; save(); cm.focus(); });
    $("#hintBtn").addEventListener("click", () => showHint(ex));
    $("#solBtn").addEventListener("click", () => showSolution(ex));
    if (hasTables) $("#tablesBtn").addEventListener("click", () => showTables(m));
    updateSolBtn(ex);
    if (S.hints[ex.id] >= 1 && !solved) showHint(ex, true);
    ensureMod(m);
  }

  // El tren se ubica sobre la estación actual; al resolver, avanza a la siguiente pendiente.
  function placeTrain(ex, animate, toIndex) {
    const tr = $("#train"), strip = $(".strip");
    if (!tr || !strip) return;
    const n = ex.mod.exercises.length;
    const k = toIndex != null ? toIndex : ex.ei;
    const x = (pct(k, n) / 100) * strip.clientWidth;
    if (!animate) { tr.style.transition = "none"; tr.style.transform = `translateX(${x}px)`; void tr.offsetWidth; tr.style.transition = ""; }
    else tr.style.transform = `translateX(${x}px)`;
  }
  window.addEventListener("resize", () => { const e = currentEx(); if (e) placeTrain(e, false, trainAt); });
  let trainAt = null;
  const currentEx = () => { const p = location.hash.split("/"); return p[1] === "e" ? BY_ID[p[2]] : null; };

  function updateSolBtn(ex) {
    const b = $("#solBtn");
    if (!b) return;
    const open = S.solved[ex.id] || (S.attempts[ex.id] || 0) >= 2;
    b.disabled = !open;
    b.title = open ? "Ver la solución" : "Se desbloquea después de 2 intentos";
  }
  function clearErrLine() {
    if (cm && errLine != null) { cm.removeLineClass(errLine, "background", "cm-err-line"); errLine = null; }
  }

  function showHint(ex, silent = false) {
    if (!S.solved[ex.id] && !S.hints[ex.id]) { S.hints[ex.id] = 1; save(); }
    const factor = S.solved[ex.id] ? "" : `<p class="fine">Con pista, este ejercicio da ${S.hints[ex.id] >= 2 ? "25" : "50"}% del XP.</p>`;
    $("#hintArea").innerHTML = `<div class="help-box"><div class="hb-h">${ico("bulb")}Pista</div><code>${esc(ex.hint)}</code>${factor}</div>`;
    if (!silent) $("#hintBtn").blur();
  }

  function showSolution(ex) {
    const go = () => {
      if (!S.solved[ex.id]) { S.hints[ex.id] = 2; save(); }
      $("#hintArea").innerHTML = `<div class="help-box"><div class="hb-h">${ico("eye")}Solución</div><pre>${esc(ex.solution)}</pre>
        <div class="row"><button class="btn small" id="useSol" type="button">${ico("copy")}Copiar al editor</button>
        ${S.solved[ex.id] ? "" : '<span class="fine" style="margin:0">Este ejercicio dará 25% del XP.</span>'}</div></div>`;
      $("#useSol").addEventListener("click", () => { cm.setValue(ex.solution); cm.focus(); });
    };
    if (S.solved[ex.id] || S.hints[ex.id] >= 2) return go();
    $("#hintArea").innerHTML = `<div class="help-box"><div class="hb-h">${ico("eye")}¿Ver la solución?</div>
      <p>Mirarla deja este ejercicio en 25% del XP. ¿Lo intentas una vez más antes?</p>
      <div class="row"><button class="btn small primary" id="tryAgain" type="button">Lo intento de nuevo</button><button class="btn small" id="seeSol" type="button">Ver solución</button></div></div>`;
    $("#tryAgain").addEventListener("click", () => { $("#hintArea").innerHTML = ""; if (cm) cm.focus(); });
    $("#seeSol").addEventListener("click", go);
  }

  async function showTables(m) {
    openDialog(`<div class="dlg-top"><h2>Datos disponibles en la línea ${m.num}</h2><button class="btn small" data-close type="button">Cerrar</button></div>
      <div class="tabs" id="tblTabs">${m.tables.map((t, i) => `<button class="tab ${i ? "" : "on"}" data-t="${t}" type="button">${t}</button>`).join("")}</div>
      <div id="tblBody"><div class="placeholder">${pyReady ? "Cargando tablas…" : "Esperando a que Python termine de cargar…"}</div></div>
      ${(m.packages || []).includes("sqlite3") ? `<p class="dtypes" style="margin:12px 0 0">${ico("db")} También tienes <code>conn</code>: una base SQLite con las tablas <code>clientes</code>, <code>productos</code> y <code>pedidos</code>.</p>` : ""}`,
    async (card) => {
      const key = m.id;
      if (!tablesCache[key]) {
        await ensureMod(m);
        tablesCache[key] = await py(Object.assign({ type: "tables", setup: setupFor(m), names: m.tables }, libMsg(m)), 120000);
      }
      const data = tablesCache[key];
      if (!card.isConnected || !$("#tblBody", card)) return;
      if (data.error) { $("#tblBody", card).innerHTML = `<p>No se pudieron cargar las tablas: ${esc(data.error.msg)}</p>`; delete tablesCache[key]; return; }
      const show = (t) => {
        const d = data[t];
        $("#tblBody", card).innerHTML = `<p class="dtypes"><b>${t}</b> · ${esc(d.info)}<br>${esc(d.dtypes)}</p>${d.html}`;
        card.querySelectorAll(".tab").forEach((b) => b.classList.toggle("on", b.dataset.t === t));
      };
      card.querySelectorAll(".tab").forEach((b) => b.addEventListener("click", () => show(b.dataset.t)));
      show(m.tables[0]);
    });
  }

  /* ---------- Ejecutar y corregir ---------- */
  const PRAISE = ["¡Eso es!", "¡Impecable!", "¡Así se hace!", "¡Perfecto!", "¡Muy bien!", "¡Excelente!", "¡Nivel profesional!"];
  const NUDGE = ["Casi", "Todavía no", "Cerca, muy cerca", "Falta un detalle"];
  const pick = (a) => a[Math.floor(Math.random() * a.length)];
  const RUN_LABEL = `${ico("play", "fill")}Ejecutar <span class="kbd">Ctrl+Enter</span>`;

  async function run(ex) {
    if (running || !cm) return;
    running = true;
    clearErrLine();
    const btn = $("#runBtn");
    btn.disabled = true;
    btn.textContent = pyReady ? "Ejecutando…" : "Cargando Python…";
    $("#runBar").className = "run-bar running";
    const code = cm.getValue();
    S.code[ex.id] = code; save();
    const m = ex.mod;
    if (((m.packages && m.packages.length) || (m.micropip && m.micropip.length)) && !libsReady.has(m.id)) {
      btn.textContent = "Cargando librerías…";
      const lr = await ensureMod(m);
      if (!$("#runBtn") || !cm) { running = false; return; }
      if (lr.error) { running = false; btn.disabled = false; btn.innerHTML = RUN_LABEL; $("#runBar").className = "run-bar"; showResult(ex, lr); return; }
      btn.textContent = "Ejecutando…";
    }
    const t0 = performance.now();
    const r = await py(Object.assign({ type: "run", setup: setupFor(m), code, solution: ex.solution, check: ex.check }, libMsg(m)), 60000);
    running = false;
    if (!$("#runBtn") || !cm) return;
    btn.disabled = false;
    btn.innerHTML = RUN_LABEL;
    $("#runBar").className = "run-bar";
    $("#outInfo").textContent = `${Math.round(performance.now() - t0)} ms`;
    showResult(ex, r);
  }

  function showResult(ex, r) {
    const out = $("#out");
    let verdict = "";
    const wasSolved = !!S.solved[ex.id];
    let g = null;
    if (r.error) {
      if (r.error.line && cm) { errLine = r.error.line - 1; cm.addLineClass(errLine, "background", "cm-err-line"); }
      verdict = `<div class="verdict bad" role="alert"><span class="v-ic">${ico("bug")}</span><div>
        <h3>${r.error.line ? `El código falló en la línea ${r.error.line}` : "El código no se pudo ejecutar"}</h3>
        <p><code>${esc(r.error.msg)}</code></p>${r.error.tip ? `<p class="tip">${esc(r.error.tip)}</p>` : ""}</div></div>`;
      onFail(ex);
    } else if (r.checked && r.passed) {
      g = onSolved(ex);
      const lineDone = g.first && modSolved(ex.mod) === ex.mod.exercises.length;
      verdict = `<div class="verdict ok" role="status"><span class="v-ic">${ico("check")}</span><div>
        <h3>${pick(PRAISE)} Estación resuelta. ${g.first ? `<span class="xp-gain">+${g.xp} XP</span>` : ""}</h3>
        <p>${g.first ? (g.combo >= 2 ? `Combo x${g.combo}${g.mult > 1 ? `: tu XP se multiplicó por ${String(g.mult).replace(".", ",")}` : ". Acierta al primer intento para multiplicar el XP"}.` : "Estación superada.") : "Ya la tenías resuelta: buen repaso."}</p>
        ${lineDone ? `<div class="line-done"><span class="badge-line" style="--s:26px">${ex.mod.num}</span><span>Completaste la <b>línea ${ex.mod.num}${SEP}${esc(ex.mod.title)}</b>.</span></div>` : ""}
        <div class="next-row">${nextBtn(ex)}</div></div></div>
        ${ex.sql ? `<details class="sql-eq" ${g.first ? "open" : ""}><summary>${ico("db")}Así se haría en SQL</summary>${codeBlock(ex.sql, "sql")}</details>` : ""}`;
    } else if (r.checked) {
      verdict = `<div class="verdict bad nudge" role="status"><span class="v-ic">${ico("x")}</span><div><h3>${pick(NUDGE)}: la estación sigue sin resolver</h3><p>${inline(r.msg || "Todavía no es correcto.")}</p></div></div>`;
      onFail(ex);
    }
    let body = verdict;
    if (r.stdout) body += `<p class="label">Salida de print</p><pre class="stdout">${esc(r.stdout)}</pre>`;
    if (r.images && r.images.length) body += `<p class="label">Tu gráfico</p>${r.images.map((b) => `<div class="plot"><img alt="Gráfico generado por tu código" src="data:image/png;base64,${b}"></div>`).join("")}`;
    if (r.display) body += `<p class="label">Tu resultado</p>${r.display}`;
    if (!body) body = '<div class="placeholder">Tu código se ejecutó sin mostrar nada.</div>';
    out.innerHTML = body;
    const nb = $("#nextBtn");
    if (nb) nb.focus({ preventScroll: true });
    if (g && g.first && !wasSolved) {
      floatXP($("#runBtn"), `+${g.xp} XP`);
      advanceTrain(ex);
      $("#stateTag").innerHTML = `<span class="state-tag">${ico("check")}Resuelta</span>`;
    }
    updateSolBtn(ex);
  }

  // Interacción insignia: la estación se llena y el tren avanza a la próxima pendiente de la línea.
  function advanceTrain(ex) {
    const sts = document.querySelectorAll(".strip-st");
    if (sts[ex.ei]) sts[ex.ei].classList.add("solved");
    const nx = nextIn(ex.mod);
    const k = nx ? nx.ei : ex.mod.exercises.length - 1;
    trainAt = k;
    setTimeout(() => placeTrain(ex, !REDUCED, k), REDUCED ? 0 : 250);
  }

  function nextBtn(ex) {
    const idx = ALL.indexOf(ex);
    const nxt = ALL.slice(idx + 1).find((e) => !S.solved[e.id]) || ALL[idx + 1];
    return nxt ? `<a class="btn line small" id="nextBtn" href="#/e/${nxt.id}" style="${lineVars(nxt.mod)}">Próxima estación ${ico("arrow")}</a>` : `<a class="btn primary small" id="nextBtn" href="#/">Ver el mapa de la red</a>`;
  }

  function onFail(ex) {
    SFX.bad();
    if (S.solved[ex.id]) return;
    S.attempts[ex.id] = (S.attempts[ex.id] || 0) + 1;
    if (S.combo >= 2) toast(ico("bolt"), "Combo perdido", `Llegaste a x${S.combo}. Empieza uno nuevo.`);
    S.combo = 0;
    save(); updateTop();
  }

  function onSolved(ex) {
    if (S.solved[ex.id]) { SFX.ok(); return { first: false }; }
    const before = levelFor(S.xp);
    const attempts = S.attempts[ex.id] || 0;
    const hint = S.hints[ex.id] || 0;
    const clean = attempts === 0 && !hint;
    S.combo = clean ? S.combo + 1 : 0;
    S.bestCombo = Math.max(S.bestCombo, S.combo);
    const mult = S.combo >= 5 ? 2 : S.combo >= 3 ? 1.5 : 1;
    const xp = Math.round(ex.xp * [1, 0.5, 0.25][hint] * mult);
    S.xp += xp;
    S.solved[ex.id] = { at: Date.now(), xp };
    if (!hint) S.noHint++;
    if (clean) S.firstTry++;
    const t = today();
    if (S.streak.last !== t) {
      S.streak.count = S.streak.last === yesterday() ? S.streak.count + 1 : 1;
      S.streak.last = t;
      if (S.streak.count > 1) setTimeout(() => toast(ico("flame"), `Racha de ${S.streak.count} días`, "Vuelve mañana para seguir sumando."), 900);
    }
    if (S.day.date !== t) S.day = { date: t, count: 0, xp: 0 };
    S.day.count++;
    S.day.xp = (S.day.xp || 0) + xp;
    if (S.day.count === GOAL) setTimeout(() => toast(ico("target"), "Meta diaria cumplida", `${GOAL} ejercicios hoy.`), 600);
    if (new Date().getHours() < 5) S.night = true;
    save();
    SFX.ok();
    updateTop();
    const cc = $("#comboChip");
    if (S.combo >= 2) { cc.classList.remove("bump"); void cc.offsetWidth; cc.classList.add("bump"); }
    const after = levelFor(S.xp);
    if (after.i > before.i) setTimeout(() => { SFX.level(); toast(String(after.i), `Subiste al nivel ${after.i}`, after.n); }, 700);
    checkBadges();
    return { first: true, xp, combo: S.combo, mult };
  }

  function checkBadges(silent = false) {
    let delay = 1500;
    BADGES.forEach((b) => {
      if (!S.badges[b.id] && b.ok()) {
        S.badges[b.id] = Date.now();
        if (!silent) {
          setTimeout(() => { SFX.badge(); toast(esc(b.code), `Logro: ${b.n}`, b.d, b.mod ? MOD[b.mod] : null); }, delay);
          delay += 900;
        }
      }
    });
    save();
  }

  /* ---------- Inicio ---------- */
  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter" && !cm && location.hash.startsWith("#/e/")) e.preventDefault();
  });
  checkBadges(true);
  updateTop();
  startWorker();
  route();

  // Exponer para pruebas automáticas
  window.__pq = { ALL, BY_ID, get state() { return S; }, get cm() { return cm; }, run: (id) => run(BY_ID[id]), LEVELS };
})();
