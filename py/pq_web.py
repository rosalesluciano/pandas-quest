"""Ejecutor para el navegador (Pyodide). Requiere pq_core ya cargado en el mismo namespace."""
import io
import json
import re
import sys
import traceback
import warnings

import pandas as pd
from pyodide.code import eval_code

warnings.simplefilter("ignore")
pd.set_option("display.max_columns", 30)


def _strip_comments(code):
    return "\n".join(re.sub(r"#.*$", "", line) for line in code.splitlines())


def _render(val):
    if isinstance(val, pd.DataFrame):
        extra = f'<div class="shape">{val.shape[0]} filas × {val.shape[1]} columnas</div>'
        return val.head(50).to_html(border=0, classes="df", na_rep="NaN") + extra
    if isinstance(val, pd.Series):
        name = "" if val.name is None else f" · nombre: {val.name}"
        extra = f'<div class="shape">Series · {len(val)} valores · dtype: {val.dtype}{name}</div>'
        return val.head(50).to_frame().to_html(border=0, classes="df", na_rep="NaN", header=val.name is not None) + extra
    import html
    return f'<pre class="val">{html.escape(repr(val))}</pre>'


def _format_error(err):
    tb = traceback.extract_tb(err.__traceback__)
    line = None
    for fr in tb:
        if fr.filename == "<exec>":
            line = fr.lineno
    if isinstance(err, SyntaxError):
        line = err.lineno
    msg = f"{type(err).__name__}: {err}"
    return {"msg": msg, "line": line, "tip": pq_error_tip(msg)}  # noqa: F821


def pq_run(setup, code, solution, opts_json, check=True):
    opts = json.loads(opts_json)
    out = io.StringIO()
    res = {"stdout": "", "display": "", "error": None, "passed": False, "msg": "", "checked": False}
    ns = {}
    exec(setup, ns)
    ns["_pq_code"] = _strip_comments(code)
    old = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = out
    val = None
    try:
        val = eval_code(code, ns)
    except BaseException as err:  # noqa: BLE001
        res["error"] = _format_error(err)
    finally:
        sys.stdout, sys.stderr = old
    res["stdout"] = out.getvalue()[-15000:]
    if res["error"]:
        return json.dumps(res)
    try:
        if val is not None:
            res["display"] = _render(val)
        elif "resultado" in ns and ns["resultado"] is not None:
            res["display"] = _render(ns["resultado"])
    except Exception as err:  # noqa: BLE001
        res["display"] = f"<pre class='val'>No se pudo mostrar: {err}</pre>"
    if check:
        exp_ns = {}
        exec(setup, exp_ns)
        exec(solution, exp_ns)
        try:
            ok, msg = pq_check(ns, exp_ns, opts)  # noqa: F821
        except Exception as err:  # noqa: BLE001
            ok, msg = False, f"No se pudo comparar tu resultado ({type(err).__name__}: {err})"
        res.update(passed=bool(ok), msg=msg, checked=True)
    return json.dumps(res)


def pq_tables(setup, names_json):
    ns = {}
    exec(setup, ns)
    out = {}
    for n in json.loads(names_json):
        df = ns[n]
        dtypes = " · ".join(f"{c}: {t}" for c, t in df.dtypes.astype(str).items())
        out[n] = {"html": df.head(12).to_html(border=0, classes="df", na_rep="NaN"),
                  "shape": list(df.shape), "dtypes": dtypes}
    return json.dumps(out)
