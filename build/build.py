"""Genera js/data.js y notebooks/*.ipynb a partir de content.py.

Uso:  python build/build.py
"""
import base64
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))

from content import LEVEL_NAMES, MODULES, SETUP, TABLES, XP_BY_LEVEL  # noqa: E402

REPO = "rosalesluciano/pandas-quest"
SITE = "https://rosalesluciano.github.io/pandas-quest/"


def colab_url(mid):
    return f"https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{mid}.ipynb"


def build_data():
    mods = []
    for m in MODULES:
        exs = []
        for ex in m["exercises"]:
            exs.append({
                "id": ex["id"], "title": ex["title"], "level": ex["level"],
                "xp": XP_BY_LEVEL[ex["level"]], "theory": ex["theory"], "task": ex["task"],
                "starter": ex["starter"], "solution": ex["solution"], "hint": ex["hint"],
                "sql": ex.get("sql", ""), "check": ex.get("check", {}),
            })
        mods.append({
            "id": m["id"], "title": m["title"], "icon": m["icon"], "color": m["color"],
            "desc": m["desc"], "setup": m.get("setup", ""), "sql": m.get("sql", False),
            "tables": TABLES + m.get("extra_tables", []), "colab": colab_url(m["id"]),
            "exercises": exs,
        })
    data = {"setup": SETUP, "modules": mods, "levelNames": LEVEL_NAMES}
    out = os.path.join(ROOT, "js", "data.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write("// Generado por build/build.py - no editar a mano\n")
        f.write("window.PQ = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    return out


def md_cell(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code_cell(src, form=False):
    meta = {"cellView": "form"} if form else {}
    return {"cell_type": "code", "execution_count": None, "metadata": meta, "outputs": [], "source": src}


NB_HELPERS = r'''
import base64 as _b64, json as _json, re as _re, warnings as _w
_w.simplefilter("ignore")
_SOL = _json.loads(_b64.b64decode(_SOL_B64).decode("utf-8"))

def reiniciar_datos():
    """Vuelve a cargar todas las tablas limpias (cada ejercicio empieza de cero)."""
    globals().pop("resultado", None)
    exec(_SETUP, globals())

def _codigo_celda():
    try:
        src = get_ipython().history_manager.input_hist_raw[-1]
    except Exception:
        return ""
    src = "\n".join(l for l in src.splitlines() if "comprobar(" not in l)
    return "\n".join(_re.sub(r"#.*$", "", l) for l in src.splitlines())

def comprobar(ej):
    info = _SOL[ej]
    exp_ns = {}
    exec(_SETUP, exp_ns)
    exec(info["solution"], exp_ns)
    g = globals()
    g["_pq_code"] = _codigo_celda()
    ok, msg = pq_check(g, exp_ns, info["check"])
    if ok:
        from IPython.display import HTML, display
        display(HTML('<div style="padding:12px 16px;border-radius:12px;background:#0f9d6e;color:#fff;'
                     'font:600 15px system-ui">🎉 ¡Correcto! +' + str(info["xp"]) + ' XP · Sigue así 🐼</div>'))
    else:
        from IPython.display import HTML, display
        import html as _h
        display(HTML('<div style="padding:12px 16px;border-radius:12px;background:#b4235a;color:#fff;'
                     'font:500 15px system-ui">❌ Todavía no. ' + _h.escape(msg) + '</div>'))
    if "resultado" in g:
        return g["resultado"]

def ver_solucion(ej):
    print(_SOL[ej]["solution"])

reiniciar_datos()
print("✅ Datos cargados:", ", ".join(_TABLAS))
'''


def build_notebooks():
    core = open(os.path.join(ROOT, "py", "pq_core.py"), encoding="utf-8").read()
    os.makedirs(os.path.join(ROOT, "notebooks"), exist_ok=True)
    paths = []
    for idx, m in enumerate(MODULES, 1):
        setup = SETUP + m.get("setup", "")
        sols = {ex["id"]: {"solution": ex["solution"], "check": ex.get("check", {}),
                           "xp": XP_BY_LEVEL[ex["level"]]} for ex in m["exercises"]}
        b64 = base64.b64encode(json.dumps(sols, ensure_ascii=False).encode("utf-8")).decode()
        tablas = TABLES + m.get("extra_tables", []) + (["conn (SQLite)"] if m.get("sql") else [])
        setup_cell = (
            "#@title ⚙️ 1) Ejecuta esta celda primero (carga datos y corrector) { display-mode: \"form\" }\n"
            + core + "\n\n_SETUP = " + repr(setup) + "\n_SOL_B64 = " + repr(b64)
            + "\n_TABLAS = " + repr(tablas) + "\n" + NB_HELPERS
        )
        cells = [
            md_cell(f"# {m['icon']} Módulo {idx}: {m['title']}\n\n{m['desc']}\n\n"
                    f"**PandasQuest** · versión web interactiva: [{SITE}]({SITE}#/m/{m['id']})\n\n"
                    "**Cómo funciona:**\n"
                    "1. Ejecuta la celda ⚙️ de abajo (carga las tablas y el corrector).\n"
                    "2. En cada ejercicio escribe tu código y guarda la respuesta en `resultado`.\n"
                    "3. Ejecuta la celda: `comprobar()` te dirá si está bien. 🎯\n\n"
                    "¿Atascado? `ver_solucion(\"id\")` muestra la solución (¡pero inténtalo antes! 😉)"),
            code_cell(setup_cell, form=True),
        ]
        for n, ex in enumerate(m["exercises"], 1):
            nivel = LEVEL_NAMES[ex["level"]]
            md = (f"---\n## {n}. {ex['title']}\n`{nivel}` · **+{XP_BY_LEVEL[ex['level']]} XP**\n\n"
                  f"{ex['theory']}\n\n### 🎯 Tu misión\n{ex['task']}\n\n"
                  f"<details><summary>💡 Pista</summary>\n\n`{ex['hint']}`\n</details>\n\n"
                  f"<details><summary>🗄️ Equivalente en SQL</summary>\n\n```sql\n{ex['sql']}\n```\n</details>")
            cells.append(md_cell(md))
            cells.append(code_cell(f"reiniciar_datos()  # empieza con los datos limpios\n\n{ex['starter']}\n\ncomprobar(\"{ex['id']}\")"))
        cells.append(md_cell(f"---\n# 🏁 ¡Módulo completado!\nVuelve a [PandasQuest]({SITE}) para sumar tus XP y seguir con el siguiente módulo. 🚀"))
        nb = {"cells": cells, "metadata": {
            "colab": {"provenance": [], "name": f"{m['id']}.ipynb"},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 0}
        p = os.path.join(ROOT, "notebooks", f"{m['id']}.ipynb")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        paths.append(p)
    return paths


if __name__ == "__main__":
    print(build_data())
    for p in build_notebooks():
        print(p)
