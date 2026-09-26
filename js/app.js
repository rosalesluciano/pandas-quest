/* PandasQuest - app principal */
(() => {
  "use strict";

  const D = window.PQ;
  const $ = (s, el = document) => el.querySelector(s);
  const app = $("#app");

  /* ---------- Datos derivados ---------- */
  const ALL = [];
  D.modules.forEach((m, mi) => m.exercises.forEach((e, ei) => ALL.push(Object.assign(e, { mod: m, mi, ei }))));
  const BY_ID = Object.fromEntries(ALL.map((e) => [e.id, e]));
  const TOTAL_XP = ALL.reduce((s, e) => s + e.xp, 0);
  const GOAL = 3;
  const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const LEVELS = [
    ["Panda bebé", "🐼", 0], ["Curioso de datos", "🔎", 0.04], ["Domador de Series", "🤠", 0.1],
    ["Ninja de DataFrames", "🥷", 0.2], ["Mago de NumPy", "🧙", 0.32], ["Artista de gráficos", "🎨", 0.45],
    ["Analista de datos", "📊", 0.6], ["Científico de datos jr", "🧪", 0.76], ["ML Master", "👑", 0.92],
  ].map(([n, e, f], i) => ({ n, e, i: i + 1, xp: Math.round((f * TOTAL_XP) / 10) * 10 }));
  const levelFor = (xp) => LEVELS.reduce((a, L) => (xp >= L.xp ? L : a), LEVELS[0]);

  /* ---------- Estado (localStorage) ---------- */
  const KEY = "pq_state_v2";
  const fresh = () => ({
    xp: 0, solved: {}, attempts: {}, hints: {}, code: {}, streak: { last: null, count: 0 },
    combo: 0, bestCombo: 0, badges: {}, day: { date: null, count: 0 }, sound: true,
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
  const nSolved = () => Object.keys(S.solved).filter((id) => BY_ID[id]).length;
  const modSolved = (m) => m.exercises.filter((e) => S.solved[e.id]).length;
  const modDone = (id) => { const m = D.modules.find((x) => x.id === id); return m && modSolved(m) === m.exercises.length; };

  /* ---------- Logros ---------- */
  const BADGES = [
    { id: "first", ico: "🥇", n: "Primer paso", d: "Resuelve tu primer ejercicio", ok: () => nSolved() >= 1 },
    { id: "ten", ico: "🔟", n: "Calentando motores", d: "Resuelve 10 ejercicios", ok: () => nSolved() >= 10 },
    { id: "combo5", ico: "⚡", n: "Imparable", d: "Combo x5 al primer intento", ok: () => S.bestCombo >= 5 },
    { id: "combo10", ico: "🌪️", n: "Modo leyenda", d: "Combo x10 al primer intento", ok: () => S.bestCombo >= 10 },
    { id: "goal", ico: "🎯", n: "Meta cumplida", d: `Resuelve ${GOAL} ejercicios en un día`, ok: () => dayCount() >= GOAL },
    { id: "streak3", ico: "🔥", n: "En racha", d: "3 días seguidos practicando", ok: () => streakNow() >= 3 },
    { id: "streak7", ico: "📅", n: "Hábito de hierro", d: "7 días seguidos", ok: () => streakNow() >= 7 },
    { id: "nohint", ico: "🧠", n: "Cerebrito", d: "15 ejercicios sin pistas", ok: () => S.noHint >= 15 },
    { id: "m01", ico: "🐼", n: "Pandero", d: "Completa el módulo Pandas", ok: () => modDone("m01") },
    { id: "m02", ico: "📋", n: "Domador de tablas", d: "Completa DataFrames", ok: () => modDone("m02") },
    { id: "m03", ico: "🔢", n: "Mente matricial", d: "Completa NumPy", ok: () => modDone("m03") },
    { id: "m04", ico: "📈", n: "Pintor de datos", d: "Completa Matplotlib", ok: () => modDone("m04") },
    { id: "m05", ico: "🎨", n: "Estadista visual", d: "Completa Seaborn", ok: () => modDone("m05") },
    { id: "m06", ico: "🤖", n: "Primer modelo", d: "Completa Machine Learning", ok: () => modDone("m06") },
    { id: "night", ico: "🦉", n: "Búho nocturno", d: "Resuelve algo entre 00:00 y 05:00", ok: () => S.night },
    { id: "all", ico: "👑", n: "Data Master", d: "Completa todo el curso", ok: () => nSolved() === ALL.length },
  ];

  /* ---------- Sonido ---------- */
  let actx;
  function tone(freqs, dur = 0.14, type = "triangle", gap = 0.07, vol = 0.12) {
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
  const SFX = {
    ok: (combo = 0) => { const k = 1 + Math.min(combo, 10) * 0.06; tone([523, 659, 784, 1047].map((f) => f * k), 0.2); },
    bad: () => tone([247, 196], 0.2, "sine", 0.12, 0.1),
    level: () => tone([523, 659, 784, 1047, 1319, 1568, 2093], 0.3, "triangle", 0.085, 0.13),
    badge: () => tone([988, 1319, 1760], 0.22, "sine", 0.08, 0.1),
  };

  /* ---------- Confeti ---------- */
  const COLORS = ["#ffca00", "#ff2d9b", "#8b6cff", "#22d3a0", "#38bdf8"];
  function boom(el, big = false) {
    if (REDUCED || !window.confetti) return;
    let origin = { x: 0.5, y: 0.5 };
    if (el) {
      const r = el.getBoundingClientRect();
      origin = { x: (r.left + r.width / 2) / innerWidth, y: (r.top + r.height / 2) / innerHeight };
    }
    confetti({ particleCount: big ? 160 : 70, spread: big ? 110 : 70, startVelocity: big ? 45 : 32, origin, colors: COLORS, disableForReducedMotion: true });
    if (big) setTimeout(() => confetti({ particleCount: 90, angle: 60, spread: 60, origin: { x: 0, y: 0.8 }, colors: COLORS }), 250);
    if (big) setTimeout(() => confetti({ particleCount: 90, angle: 120, spread: 60, origin: { x: 1, y: 0.8 }, colors: COLORS }), 400);
  }
  function floatXP(el, text) {
    const r = el.getBoundingClientRect();
    const f = document.createElement("div");
    f.className = "float-xp"; f.textContent = text;
    f.style.left = `${r.left + r.width / 2 - 30}px`; f.style.top = `${r.top - 10}px`;
    document.body.appendChild(f);
    setTimeout(() => f.remove(), 1400);
  }

  /* ---------- Toasts y modales ---------- */
  function toast(ico, title, sub = "") {
    const t = document.createElement("div");
    t.className = "toast";
    t.innerHTML = `<span class="ico">${ico}</span><div><b>${esc(title)}</b>${sub ? `<small>${esc(sub)}</small>` : ""}</div>`;
    $("#toasts").appendChild(t);
    setTimeout(() => { t.classList.add("out"); setTimeout(() => t.remove(), 320); }, 3800);
  }
  const modalQueue = [];
  let modalOpen = false;
  function modal(html, cls = "", onOpen) {
    modalQueue.push({ html, cls, onOpen });
    if (!modalOpen) nextModal();
  }
  function nextModal() {
    const m = modalQueue.shift();
    if (!m) { modalOpen = false; $("#modal").classList.add("hidden"); return; }
    modalOpen = true;
    const card = $("#modalCard");
    card.className = "modal-card " + m.cls;
    card.innerHTML = m.html;
    $("#modal").classList.remove("hidden");
    card.querySelectorAll("[data-close]").forEach((b) => b.addEventListener("click", nextModal));
    if (m.onOpen) m.onOpen(card);
    const focusable = card.querySelector("button");
    if (focusable) focusable.focus();
  }
  $("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") nextModal(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && modalOpen) nextModal(); });

  /* ---------- Utilidades de texto ---------- */
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
        const t = buf.join(" ");
        const kind = t.startsWith("⚠️") ? "warn" : t.startsWith("💼") ? "work" : "tip";
        out.push(`<div class="callout ${kind}">${inline(t)}</div>`);
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

  /* ---------- Python (Web Worker + Pyodide) ---------- */
  let worker, pyReady = false, seq = 0;
  const pending = new Map(), waiters = [];
  function setPy(state, text) {
    const el = $("#pyStatus");
    el.className = "py-status " + state;
    $(".txt", el).textContent = text;
  }
  function startWorker() {
    pyReady = false;
    if (typeof libsReady !== "undefined") libsReady.clear();
    setPy("", "Cargando Python…");
    worker = new Worker("js/worker.js");
    worker.onmessage = (ev) => {
      const m = ev.data;
      if (m.type === "status") setPy("", m.text);
      else if (m.type === "ready") { pyReady = true; setPy("ready", "Python listo"); waiters.splice(0).forEach((f) => f()); }
      else if (m.type === "fatal") setPy("error", "Error cargando Python");
      else if (m.type === "result") {
        const p = pending.get(m.id);
        if (p) { pending.delete(m.id); clearTimeout(p.t); p.res(m.data); }
      }
    };
    worker.onerror = () => setPy("error", "Error cargando Python");
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
        res({ error: { msg: "⏱️ Tu código tardó demasiado. ¿Hay un bucle infinito?", line: null, tip: "Python se reinició solo. Revisa el código y vuelve a ejecutar." } });
      }, timeout);
      pending.set(id, { res, t });
      worker.postMessage(Object.assign({ id }, msg));
    });
  }
  const setupFor = (m) => D.setup + (m.setup || "");
  const libsReady = new Set();
  const libMsg = (m) => ({ packages: m.packages || [], pip: m.micropip || [] });
  async function ensureMod(m) {
    if (!(m.packages || m.micropip) || libsReady.has(m.id)) return {};
    const r = await py(Object.assign({ type: "load" }, libMsg(m)), 300000);
    if (!r.error) libsReady.add(m.id);
    return r;
  }

  /* ---------- Barra superior ---------- */
  function updateTop() {
    const L = levelFor(S.xp), next = LEVELS[L.i] || null;
    const pct = next ? ((S.xp - L.xp) / (next.xp - L.xp)) * 100 : 100;
    $(".lvl-num").textContent = L.i;
    $(".lvl-name").textContent = `${L.e} ${L.n}`;
    $(".xpbar i").style.width = `${Math.max(3, Math.min(100, pct))}%`;
    $(".xp-txt b").textContent = S.xp;
    $("#levelPill").title = next ? `Nivel ${L.i} · faltan ${next.xp - S.xp} XP para "${next.n}"` : "¡Nivel máximo!";
    $("#streakChip b").textContent = streakNow();
    const cc = $("#comboChip");
    cc.classList.toggle("hidden", S.combo < 2);
    $("b", cc).textContent = S.combo;
    $("#soundBtn").textContent = S.sound ? "🔊" : "🔇";
    $("#themeBtn").textContent = document.documentElement.dataset.theme === "light" ? "🌙" : "☀️";
  }
  $("#soundBtn").addEventListener("click", () => { S.sound = !S.sound; save(); updateTop(); if (S.sound) SFX.badge(); });
  $("#themeBtn").addEventListener("click", () => {
    const t = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    document.documentElement.dataset.theme = t;
    try { localStorage.setItem("pq_theme", t); } catch (e) { /* */ }
    updateTop();
  });
  $("#levelPill").addEventListener("click", showLevels);

  function showLevels() {
    const L = levelFor(S.xp);
    const rows = LEVELS.map((l) => `<div class="ex-row ${S.xp >= l.xp ? "solved" : ""}" style="cursor:default">
      <span class="st">${S.xp >= l.xp ? "✓" : l.i}</span><span class="t">${l.e} ${l.n}</span><span class="xp-tag">${l.xp} XP</span></div>`).join("");
    modal(`<div class="modal-top"><h2>Tu camino: nivel ${L.i}</h2><button class="btn small" data-close>Cerrar</button></div>
      <p style="color:var(--muted);margin:0 0 14px">Ganas XP resolviendo ejercicios. Aciertos seguidos al primer intento activan el <b>combo</b> (x1.5 desde 3, x2 desde 5). Las pistas reducen el XP del ejercicio.</p>
      <div class="ex-list">${rows}</div>`);
  }

  /* ---------- Router ---------- */
  function route() {
    const parts = (location.hash.slice(1) || "/").split("/").filter(Boolean);
    if (cm) { cm = null; }
    if (parts[0] === "e" && BY_ID[parts[1]]) renderExercise(BY_ID[parts[1]]);
    else if (parts[0] === "m" && D.modules.find((x) => x.id === parts[1])) renderModule(D.modules.find((x) => x.id === parts[1]));
    else renderHome();
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", route);

  /* ---------- Vista: Inicio ---------- */
  function renderHome() {
    document.title = "PandasQuest · Aprende pandas con ejercicios";
    const next = ALL.find((e) => !S.solved[e.id]);
    const done = nSolved(), pctDay = Math.min(100, (dayCount() / GOAL) * 100);
    const unlocked = BADGES.filter((b) => S.badges[b.id]).length;
    const cta = next
      ? `<a class="btn primary" href="#/e/${next.id}">${done ? "▶ Continuar" : "▶ Empezar ahora"} <span class="kbd">${esc(next.title)}</span></a>`
      : `<a class="btn primary" href="#/m/m06">👑 ¡Completaste todo! Repasar</a>`;
    app.innerHTML = `<div class="page-enter">
      <section class="hero">
        <div class="hero-main">
          <span class="eyebrow">🐍 Pandas · NumPy · Matplotlib · Seaborn · ML</span>
          <h1>Aprende ciencia de datos <span class="hl">resolviendo retos reales</span></h1>
          <p class="lead">${ALL.length} ejercicios prácticos en ${D.modules.length} módulos: de tu primera Series a tu primer modelo de Machine Learning. Escribe código, ejecútalo y recibe corrección al instante. Todo en el navegador o en Google Colab.</p>
          <div class="hero-cta">${cta}
            <a class="btn colab-btn" href="${D.modules[0].colab}" target="_blank" rel="noopener">Abrir en Colab ↗</a>
          </div>
        </div>
        <div class="hero-side">
          <div class="daily">
            <div class="ring" style="--p:${pctDay}"><span>${dayCount()}/${GOAL}</span></div>
            <div><h3>${dayCount() >= GOAL ? "¡Meta diaria cumplida! 🎉" : "Meta de hoy"}</h3>
            <p>${dayCount() >= GOAL ? "Tu cerebro de datos te lo agradece. ¿Uno más?" : `Resuelve ${GOAL - dayCount()} ejercicio${GOAL - dayCount() === 1 ? "" : "s"} más para mantener la racha 🔥`}</p></div>
          </div>
          <div class="stats">
            <div class="stat"><span class="v">${done}<small style="font-size:15px;color:var(--muted)">/${ALL.length}</small></span><span class="l">Ejercicios</span></div>
            <div class="stat"><span class="v">${S.xp}</span><span class="l">XP totales</span></div>
            <div class="stat"><span class="v">🔥 ${streakNow()}</span><span class="l">Días de racha</span></div>
            <div class="stat"><span class="v">${unlocked}<small style="font-size:15px;color:var(--muted)">/${BADGES.length}</small></span><span class="l">Logros</span></div>
          </div>
        </div>
      </section>

      <div class="section-title"><h2>🗺️ Tu ruta</h2><span>De cero a tu primer modelo de ML</span></div>
      <div class="modules">${D.modules.map((m, i) => modCard(m, i)).join("")}</div>

      <div class="section-title"><h2>🏅 Logros</h2><span>${unlocked} de ${BADGES.length} desbloqueados</span></div>
      <div class="badges">${BADGES.map((b) => `<div class="badge ${S.badges[b.id] ? "unlocked" : "locked"}"><span class="ico">${b.ico}</span><b>${b.n}</b><small>${b.d}</small></div>`).join("")}</div>

      <div class="section-title"><h2>⚡ Cómo funciona</h2></div>
      <div class="steps">
        <div class="step"><div class="n">1</div><h4>Lee y entiende</h4><p>Cada reto explica el concepto con ejemplos, usos reales y errores comunes. Muchos incluyen su equivalente en SQL.</p></div>
        <div class="step"><div class="n">2</div><h4>Escribe y ejecuta</h4><p>Python y pandas reales corriendo en tu navegador. <b>Ctrl + Enter</b> para ejecutar.</p></div>
        <div class="step"><div class="n">3</div><h4>Gana XP y sube de nivel</h4><p>Combos, rachas y logros. ¿Prefieres Colab? Cada módulo tiene su notebook con corrector.</p></div>
      </div>

      <footer class="foot">
        <span>🐼 PandasQuest · Pandas, NumPy, Matplotlib, Seaborn y Machine Learning</span>
        <span><a href="https://github.com/rosalesluciano/pandas-quest" target="_blank" rel="noopener">GitHub</a> · <button class="reset-link" id="resetBtn">Reiniciar progreso</button></span>
      </footer>
    </div>`;
    $("#resetBtn").addEventListener("click", () => {
      if (confirm("¿Seguro? Se borrará todo tu progreso, XP y logros.")) { const snd = S.sound; S = fresh(); S.sound = snd; save(); updateTop(); renderHome(); }
    });
  }
  function modCard(m, i) {
    const n = modSolved(m), tot = m.exercises.length, pct = (n / tot) * 100;
    return `<a class="mod ${n === tot ? "done" : ""}" href="#/m/${m.id}" style="--c:${m.color}">
      <div class="mod-head"><div class="mod-icon">${m.icon}</div><div><div class="mod-num">Módulo ${i + 1}</div><h3>${esc(m.title)}</h3></div></div>
      <p>${esc(m.desc)}</p>
      <div class="mod-foot"><div class="bar"><i style="width:${pct}%"></i></div><span>${n}/${tot}</span></div>
    </a>`;
  }

  /* ---------- Vista: Módulo ---------- */
  function renderModule(m) {
    document.title = `${m.title} · PandasQuest`;
    const i = D.modules.indexOf(m), n = modSolved(m);
    ensureMod(m);
    const next = m.exercises.find((e) => !S.solved[e.id]) || m.exercises[0];
    app.innerHTML = `<div class="page-enter">
      <div class="crumbs"><a href="#/">🗺️ Ruta</a> / <span>Módulo ${i + 1}</span></div>
      <div class="mod-hero" style="--c:${m.color}">
        <div class="mod-icon">${m.icon}</div>
        <div class="grow"><h1>${esc(m.title)}</h1><p>${esc(m.desc)}</p></div>
        <a class="btn primary" href="#/e/${next.id}">${n ? "▶ Continuar" : "▶ Empezar"}</a>
        <a class="btn colab-btn" href="${m.colab}" target="_blank" rel="noopener">Abrir en Colab ↗</a>
      </div>
      <div class="mod-foot" style="--c:${m.color};margin-bottom:20px"><div class="bar"><i style="width:${(n / m.exercises.length) * 100}%"></i></div><span>${n}/${m.exercises.length} completados</span></div>
      <div class="ex-list">${m.exercises.map((e, k) => `${k === 0 || e.sec !== m.exercises[k - 1].sec ? `<h3 class="sec-title">${esc(e.sec)}</h3>` : ""}
        <a class="ex-row ${S.solved[e.id] ? "solved" : ""}" href="#/e/${e.id}">
          <span class="st">${S.solved[e.id] ? "✓" : k + 1}</span>
          <span class="t">${esc(e.title)}</span>
          <span class="lvl lvl-${e.level}">${D.levelNames[e.level]}</span>
          <span class="xp-tag">+${e.xp} XP</span>
        </a>`).join("")}</div>
      <div class="ex-nav" style="margin-top:24px">
        ${i > 0 ? `<a class="btn ghost" href="#/m/${D.modules[i - 1].id}">← ${esc(D.modules[i - 1].title)}</a>` : "<span></span>"}
        ${i < D.modules.length - 1 ? `<a class="btn ghost" href="#/m/${D.modules[i + 1].id}">${esc(D.modules[i + 1].title)} →</a>` : ""}
      </div>
    </div>`;
  }

  /* ---------- Vista: Ejercicio ---------- */
  let cm = null, running = false, errLine = null;
  const tablesCache = {};

  function renderExercise(ex) {
    const m = ex.mod, idx = ALL.indexOf(ex);
    const prev = ALL[idx - 1], next = ALL[idx + 1];
    document.title = `${ex.title} · PandasQuest`;
    const solved = !!S.solved[ex.id];
    app.innerHTML = `<div class="ex-page page-enter">
      <aside class="panel lesson">
        <div class="crumbs"><a href="#/">🗺️ Ruta</a> / <a href="#/m/${m.id}">${m.icon} ${esc(m.title)}</a> / <span>${esc(ex.sec)}</span></div>
        <div class="dots">${m.exercises.map((e) => `<a href="#/e/${e.id}" title="${esc(e.title)}" class="${S.solved[e.id] ? "solved" : ""} ${e === ex ? "current" : ""}"></a>`).join("")}</div>
        <h1>${esc(ex.title)}</h1>
        <div class="meta"><span class="ex-count">${ex.ei + 1}/${m.exercises.length}</span><span class="lvl lvl-${ex.level}">${D.levelNames[ex.level]}</span><span class="xp-tag">+${ex.xp} XP</span>${solved ? '<span class="lvl lvl-1">✓ Resuelto</span>' : ""}</div>
        <div class="md">${md(ex.theory)}</div>
        <div class="mission"><h3>🎯 Tu misión</h3><div class="md">${md(ex.task)}</div></div>
        <div class="tools">
          <button class="btn small" id="hintBtn">💡 Pista</button>
          <button class="btn small" id="solBtn">👀 Solución</button>
          <button class="btn small" id="tablesBtn">📋 Tablas</button>
          <a class="btn small colab-btn" href="${m.colab}" target="_blank" rel="noopener">Colab ↗</a>
        </div>
        <div id="hintArea"></div>
      </aside>
      <section class="workspace">
        <div class="panel editor-card">
          <div class="editor-head">
            <span class="file-tab"><i></i>${m.id === "m06" ? "modelo" : m.title.toLowerCase()}.py</span>
            <div class="editor-actions">
              <button class="btn small ghost" id="resetCode" title="Volver al código inicial">↺ Reiniciar</button>
              <button class="btn small run" id="runBtn">▶ Ejecutar <span class="kbd">Ctrl+Enter</span></button>
            </div>
          </div>
          <div id="editor"></div>
        </div>
        <div class="panel output">
          <div class="out-head"><span>Resultado</span><span id="outInfo"></span></div>
          <div id="runBar"></div>
          <div class="out-body" id="out">
            <div class="placeholder"><span class="big">🐼</span>Escribe tu código y pulsa <b>Ejecutar</b> (o <b>Ctrl + Enter</b>).<br>Guarda tu respuesta en la variable <code>resultado</code>.</div>
          </div>
        </div>
        <div class="ex-nav">
          ${prev ? `<a class="btn ghost small" href="#/e/${prev.id}">← Anterior</a>` : "<span></span>"}
          ${next ? `<a class="btn ghost small" href="#/e/${next.id}">Siguiente →</a>` : `<a class="btn ghost small" href="#/">🏁 Ruta</a>`}
        </div>
      </section>
    </div>`;

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
    setTimeout(() => { cm.refresh(); if (matchMedia("(min-width: 981px)").matches) cm.focus(); }, 30);
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
    $("#tablesBtn").addEventListener("click", () => showTables(m));
    updateSolBtn(ex);
    if (S.hints[ex.id] >= 1 && !solved) showHint(ex, true);
    ensureMod(m);
  }

  function updateSolBtn(ex) {
    const b = $("#solBtn");
    if (!b) return;
    const open = S.solved[ex.id] || (S.attempts[ex.id] || 0) >= 2;
    b.disabled = !open;
    b.title = open ? "Ver la solución" : "Se desbloquea tras 2 intentos";
  }

  function clearErrLine() {
    if (cm && errLine != null) { cm.removeLineClass(errLine, "background", "cm-err-line"); errLine = null; }
  }

  function showHint(ex, silent = false) {
    if (!S.solved[ex.id] && !S.hints[ex.id]) { S.hints[ex.id] = 1; save(); }
    const factor = S.solved[ex.id] ? "" : `<div style="color:var(--muted);font-size:12px;margin-top:6px">Usar pista: este ejercicio da ${S.hints[ex.id] >= 2 ? "25" : "50"}% del XP.</div>`;
    $("#hintArea").innerHTML = `<div class="hint-box">💡 <code>${esc(ex.hint)}</code>${factor}</div>`;
    if (!silent) $("#hintBtn").blur();
  }

  function showSolution(ex) {
    const go = () => {
      if (!S.solved[ex.id]) { S.hints[ex.id] = 2; save(); }
      $("#hintArea").innerHTML = `<div class="hint-box"><b>👀 Solución</b><pre>${esc(ex.solution)}</pre>
        <div style="margin-top:10px;display:flex;gap:8px;align-items:center;flex-wrap:wrap"><button class="btn small" id="useSol">Copiar al editor</button>
        ${S.solved[ex.id] ? "" : '<span style="color:var(--muted);font-size:12px">Este ejercicio dará solo 25% del XP.</span>'}</div></div>`;
      $("#useSol").addEventListener("click", () => { cm.setValue(ex.solution); cm.focus(); });
    };
    if (S.solved[ex.id] || S.hints[ex.id] >= 2) return go();
    modal(`<span class="big-emoji">🤔</span><h2>¿Ver la solución?</h2>
      <p>Aprender cuesta: mirar la solución deja el XP de este ejercicio en un 25%. ¿Probamos una vez más antes?</p>
      <div class="hero-cta" style="justify-content:center"><button class="btn primary" data-close>Lo intento otra vez 💪</button><button class="btn" id="seeSol">Ver solución</button></div>`,
    "center", (card) => $("#seeSol", card).addEventListener("click", () => { nextModal(); go(); }));
  }

  async function showTables(m) {
    modal(`<div class="modal-top"><h2>📋 Datos disponibles</h2><button class="btn small" data-close>Cerrar</button></div>
      <div class="tabs" id="tblTabs">${m.tables.map((t, i) => `<button class="tab ${i ? "" : "on"}" data-t="${t}">${t}</button>`).join("")}</div>
      <div id="tblBody"><div class="placeholder"><span class="big">⏳</span>${pyReady ? "Cargando tablas…" : "Esperando a que Python termine de cargar…"}</div></div>
      ${(m.packages || []).includes("sqlite3") ? '<p style="margin:12px 0 0;font-size:13px">En este módulo también tienes <code>conn</code>: una base SQLite con las tablas <code>clientes</code>, <code>productos</code> y <code>pedidos</code>.</p>' : ""}`,
    "", async (card) => {
      const key = m.id;
      if (!tablesCache[key]) {
        await ensureMod(m);
        tablesCache[key] = await py(Object.assign({ type: "tables", setup: setupFor(m), names: m.tables }, libMsg(m)), 120000);
      }
      const data = tablesCache[key];
      if (!card.isConnected || !$("#tblBody", card)) return;
      if (data.error) { $("#tblBody", card).innerHTML = `<p>Error: ${esc(data.error.msg)}</p>`; delete tablesCache[key]; return; }
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
  const PRAISE = ["¡Brutal!", "¡Eso es!", "¡Crack!", "¡Impecable!", "¡Así se hace!", "¡Data wizard! 🧙", "¡Nivel senior!", "¡Perfecto!", "¡Qué máquina!"];
  const NUDGE = ["Casi… 🤏", "¡Tú puedes!", "Uy, todavía no", "Cerca, muy cerca", "Un detalle más"];
  const pick = (a) => a[Math.floor(Math.random() * a.length)];

  async function run(ex) {
    if (running || !cm) return;
    running = true;
    clearErrLine();
    const btn = $("#runBtn");
    btn.disabled = true;
    btn.innerHTML = pyReady ? "⏳ Ejecutando…" : "⏳ Cargando Python…";
    $("#runBar").className = "running-bar";
    const code = cm.getValue();
    S.code[ex.id] = code; save();
    if ((ex.mod.packages || ex.mod.micropip) && !libsReady.has(ex.mod.id)) {
      btn.innerHTML = "⏳ Cargando librerías…";
      const lr = await ensureMod(ex.mod);
      if (!$("#runBtn") || !cm) { running = false; return; }
      if (lr.error) { running = false; btn.disabled = false; btn.innerHTML = '▶ Ejecutar <span class="kbd">Ctrl+Enter</span>'; $("#runBar").className = ""; showResult(ex, lr); return; }
      btn.innerHTML = "⏳ Ejecutando…";
    }
    const t0 = performance.now();
    const r = await py(Object.assign({ type: "run", setup: setupFor(ex.mod), code, solution: ex.solution, check: ex.check }, libMsg(ex.mod)), 60000);
    running = false;
    if (!$("#runBtn") || !cm) return;
    btn.disabled = false;
    btn.innerHTML = '▶ Ejecutar <span class="kbd">Ctrl+Enter</span>';
    $("#runBar").className = "";
    $("#outInfo").textContent = `${Math.round(performance.now() - t0)} ms`;
    showResult(ex, r);
  }

  function showResult(ex, r) {
    const out = $("#out");
    let verdict = "";
    const wasSolved = !!S.solved[ex.id];
    if (r.error) {
      if (r.error.line && cm) { errLine = r.error.line - 1; cm.addLineClass(errLine, "background", "cm-err-line"); }
      verdict = `<div class="verdict bad"><span class="emo">🐞</span><div class="grow"><h4>Error${r.error.line ? ` en la línea ${r.error.line}` : ""}</h4>
        <p><code>${esc(r.error.msg)}</code></p>${r.error.tip ? `<p class="tip">💡 ${esc(r.error.tip)}</p>` : ""}</div></div>`;
      onFail(ex);
    } else if (r.checked && r.passed) {
      const g = onSolved(ex);
      verdict = `<div class="verdict ok"><span class="emo">${g.first ? "🎉" : "✅"}</span><div class="grow">
        <h4>${pick(PRAISE)} ${g.first ? `<span class="xp-gain">+${g.xp} XP</span>` : ""}</h4>
        <p>${g.first ? (g.combo >= 2 ? `Combo <b>x${g.combo}</b> ⚡ ${g.mult > 1 ? `(bonus x${g.mult})` : "— ¡acierta al primer intento para multiplicar XP!"}` : "Ejercicio superado.") : "Ya lo tenías resuelto: ¡buen repaso!"}</p>
        <div class="next-row">${nextBtn(ex)}</div></div></div>
        ${ex.sql ? `<details class="sql-eq" ${g.first ? "open" : ""}><summary>🗄️ Así se haría en SQL</summary>${codeBlock(ex.sql, "sql")}</details>` : ""}`;
    } else if (r.checked) {
      verdict = `<div class="verdict bad"><span class="emo">🤔</span><div class="grow"><h4>${pick(NUDGE)}</h4><p>${inline(r.msg || "Todavía no es correcto.")}</p></div></div>`;
      onFail(ex);
    }
    let body = verdict;
    if (r.stdout) body += `<p class="label">Salida (print)</p><pre class="stdout">${esc(r.stdout)}</pre>`;
    if (r.images && r.images.length) body += `<p class="label">Tu gráfico</p>${r.images.map((b) => `<div class="plot"><img alt="Gráfico generado por tu código" src="data:image/png;base64,${b}"></div>`).join("")}`;
    if (r.display) body += `<p class="label">Tu resultado</p>${r.display}`;
    if (!body) body = '<div class="placeholder">Sin salida.</div>';
    out.innerHTML = body;
    const nb = $("#nextBtn");
    if (nb) nb.focus({ preventScroll: true });
    if (r.checked && r.passed && !wasSolved) {
      boom($("#runBtn"));
      floatXP($("#runBtn"), `+${S.solved[ex.id].xp} XP`);
    }
    updateSolBtn(ex);
    $(".dots") && refreshDots(ex);
  }

  function refreshDots(ex) {
    ex.mod.exercises.forEach((e, i) => { const a = $(".dots").children[i]; if (a) a.classList.toggle("solved", !!S.solved[e.id]); });
  }

  function nextBtn(ex) {
    const idx = ALL.indexOf(ex);
    const nxt = ALL.slice(idx + 1).find((e) => !S.solved[e.id]) || ALL[idx + 1];
    return nxt ? `<a class="btn primary small" id="nextBtn" href="#/e/${nxt.id}">Siguiente reto →</a>` : `<a class="btn primary small" id="nextBtn" href="#/">🏁 Ver mi ruta</a>`;
  }

  function onFail(ex) {
    SFX.bad();
    if (S.solved[ex.id]) return;
    S.attempts[ex.id] = (S.attempts[ex.id] || 0) + 1;
    if (S.combo > 0) toast("💔", "Combo perdido", `Llegaste a x${S.combo}. ¡A por otro!`);
    S.combo = 0;
    save(); updateTop();
  }

  function onSolved(ex) {
    if (S.solved[ex.id]) { SFX.ok(0); return { first: false }; }
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
    // racha y meta diaria
    const t = today();
    if (S.streak.last !== t) {
      S.streak.count = S.streak.last === yesterday() ? S.streak.count + 1 : 1;
      S.streak.last = t;
      if (S.streak.count > 1) setTimeout(() => toast("🔥", `¡Racha de ${S.streak.count} días!`, "Vuelve mañana para seguir sumando"), 900);
    }
    if (S.day.date !== t) S.day = { date: t, count: 0 };
    S.day.count++;
    if (S.day.count === GOAL) setTimeout(() => toast("🎯", "¡Meta diaria cumplida!", `${GOAL} ejercicios hoy. Imparable.`), 600);
    if (new Date().getHours() < 5) S.night = true;
    save();
    SFX.ok(S.combo);
    const cc = $("#comboChip");
    updateTop();
    if (S.combo >= 2) { cc.classList.remove("bump"); void cc.offsetWidth; cc.classList.add("bump"); }
    // subir de nivel
    const after = levelFor(S.xp);
    if (after.i > before.i) {
      setTimeout(() => {
        SFX.level(); boom(null, true);
        modal(`<span class="big-emoji">${after.e}</span><h2>¡Nivel ${after.i}!</h2><p>Ahora eres <b style="color:var(--text)">${after.n}</b>. Tu yo del futuro con trabajo de datos te lo agradece.</p><button class="btn primary" data-close>¡Vamos! 🚀</button>`, "center");
      }, 700);
    }
    // módulo completado
    const m = ex.mod;
    if (modSolved(m) === m.exercises.length) {
      const nm = D.modules[D.modules.indexOf(m) + 1];
      setTimeout(() => {
        boom(null, true); SFX.level();
        modal(`<span class="big-emoji">${m.icon}</span><h2>¡Módulo completado!</h2><p>Dominaste <b style="color:var(--text)">${esc(m.title)}</b>. ${nm ? `Siguiente parada: ${nm.icon} ${esc(nm.title)}.` : "¡Completaste la ruta!"}</p>
          <div class="hero-cta" style="justify-content:center">${nm ? `<a class="btn primary" href="#/m/${nm.id}" data-close>Continuar →</a>` : ""}<button class="btn" data-close>Cerrar</button></div>`, "center");
      }, 1100);
    }
    checkBadges();
    return { first: true, xp, combo: S.combo, mult };
  }

  function checkBadges(silent = false) {
    let delay = 1500;
    BADGES.forEach((b) => {
      if (!S.badges[b.id] && b.ok()) {
        S.badges[b.id] = Date.now();
        if (!silent) { setTimeout(() => { SFX.badge(); toast(b.ico, `Logro: ${b.n}`, b.d); }, delay); delay += 900; }
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
