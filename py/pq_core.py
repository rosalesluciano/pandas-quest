"""PandasQuest - motor de corrección.

Se usa igual en el navegador (Pyodide), en los notebooks de Colab y en los tests.
Compara el `resultado` del alumno contra el de la solución oficial con tolerancia
a diferencias irrelevantes (tipos int/float, nombres de índice, dtype string, etc.).
"""
import math

import numpy as np
import pandas as pd


def _norm_s(s):
    dt = s.dtype
    if isinstance(dt, pd.CategoricalDtype) or pd.api.types.is_string_dtype(dt):
        s = s.astype(object)
    elif pd.api.types.is_extension_array_dtype(dt):
        if pd.api.types.is_numeric_dtype(dt) and not pd.api.types.is_bool_dtype(dt):
            s = s.astype("float64")
        else:
            s = s.astype(object)
    if s.dtype == object:
        s = s.where(s.notna(), None)
    return s


def _norm_index(idx):
    if isinstance(idx, pd.MultiIndex):
        return idx
    if isinstance(idx, pd.CategoricalIndex) or pd.api.types.is_string_dtype(idx.dtype):
        return pd.Index(list(idx), dtype=object)
    return idx


def _norm(o):
    if isinstance(o, pd.Series):
        o = _norm_s(o.copy())
    else:
        cols = list(o.columns)
        o = pd.DataFrame({i: _norm_s(o.iloc[:, i]) for i in range(o.shape[1])}, index=o.index)
        o.columns = _norm_index(pd.Index(cols))
    o.index = _norm_index(o.index)
    return o


def _sort(o, ignore_index):
    if ignore_index:
        o = o.reset_index(drop=True)
        try:
            if isinstance(o, pd.Series):
                o = o.sort_values(kind="mergesort")
            else:
                o = o.sort_values(by=list(o.columns), kind="mergesort")
        except TypeError:
            key = o.astype(str) if isinstance(o, pd.Series) else o.astype(str).agg("|".join, axis=1)
            o = o.iloc[np.argsort(key.to_numpy(), kind="mergesort")]
        return o.reset_index(drop=True)
    try:
        return o.sort_index()
    except TypeError:
        return o


def _tipo(x):
    nombres = {pd.DataFrame: "un DataFrame", pd.Series: "una Series"}
    return nombres.get(type(x), f"un {type(x).__name__}")


def _scalar_eq(u, e):
    if isinstance(e, (np.generic,)):
        e = e.item()
    if isinstance(u, (np.generic,)):
        u = u.item()
    if isinstance(e, float) or isinstance(u, float):
        try:
            u, e = float(u), float(e)
        except (TypeError, ValueError):
            return False
        if math.isnan(e):
            return math.isnan(u)
        return math.isclose(u, e, rel_tol=1e-6, abs_tol=1e-6)
    if isinstance(e, (list, tuple)) and isinstance(u, (list, tuple, np.ndarray, pd.Index)):
        u = list(u)
        return len(u) == len(e) and all(_scalar_eq(a, b) for a, b in zip(u, e))
    try:
        return bool(u == e)
    except Exception:
        return False


def pq_compare(u, e, ordered=True, ignore_index=False):
    """Devuelve (ok, mensaje)."""
    if isinstance(e, (pd.DataFrame, pd.Series)):
        if not isinstance(u, type(e)):
            extra = ""
            if isinstance(e, pd.Series) and isinstance(u, pd.DataFrame):
                extra = " Pista: con una sola columna usa df['col'] (corchetes simples)."
            if isinstance(e, pd.DataFrame) and isinstance(u, pd.Series):
                extra = " Pista: usa doble corchete df[['col']] o .reset_index() / .to_frame()."
            return False, f"Tu resultado es {_tipo(u)}, pero se esperaba {_tipo(e)}.{extra}"
        if isinstance(e, pd.DataFrame):
            uc, ec = [str(c) for c in u.columns], [str(c) for c in e.columns]
            if uc != ec:
                if sorted(uc) == sorted(ec):
                    return False, f"Tienes las columnas correctas pero en otro orden. Se esperaba: {ec}"
                faltan = [c for c in ec if c not in uc]
                sobran = [c for c in uc if c not in ec]
                msg = "Las columnas no coinciden."
                if faltan:
                    msg += f" Faltan: {faltan}."
                if sobran:
                    msg += f" Sobran: {sobran}."
                return False, msg
        if u.shape != e.shape:
            return False, f"Forma distinta: tu resultado tiene {u.shape} y se esperaba {e.shape} (filas, columnas)."
        u2, e2 = _norm(u), _norm(e)
        if not ordered:
            u2, e2 = _sort(u2, ignore_index), _sort(e2, ignore_index)
        elif ignore_index:
            u2, e2 = u2.reset_index(drop=True), e2.reset_index(drop=True)
        kw = dict(check_dtype=False, check_names=False, check_index_type=False,
                  check_exact=False, rtol=1e-6, atol=1e-6)
        try:
            if isinstance(e2, pd.DataFrame):
                pd.testing.assert_frame_equal(u2, e2, check_column_type=False, check_freq=False, **kw)
            else:
                pd.testing.assert_series_equal(u2, e2, check_freq=False, **kw)
        except AssertionError as err:
            txt = str(err)
            if "index" in txt.lower() and "values are different" in txt.lower() and "iloc" not in txt:
                return False, "Los valores parecen correctos pero el índice no coincide. ¿Hace falta ordenar o usar reset_index()?"
            if ordered and not ignore_index:
                try:
                    pd.testing.assert_frame_equal(
                        u2.to_frame() if isinstance(u2, pd.Series) else u2,
                        e2.to_frame() if isinstance(e2, pd.Series) else e2,
                        check_like=True, **kw)
                except AssertionError:
                    pass
                else:
                    return False, "Mismos datos, pero en otro orden. Revisa cómo ordenas las filas."
            return False, "Los valores no coinciden con lo esperado. Revisa la lógica y vuelve a intentarlo."
        return True, ""
    if isinstance(u, (pd.DataFrame, pd.Series)):
        return False, f"Tu resultado es {_tipo(u)}, pero se esperaba un valor simple ({type(e).__name__}). ¿Te falta .iloc[0], .sum() o similar?"
    if _scalar_eq(u, e):
        return True, ""
    return False, f"Tu resultado es {u!r}, pero no es el valor esperado."


def pq_check(ns, exp_ns, opts):
    """Evalúa el ejercicio. ns = namespace del alumno, exp_ns = namespace de la solución."""
    custom = opts.get("custom")
    if custom:
        try:
            ok = bool(eval(custom, ns))
        except Exception as err:
            return False, f"Aún no funciona: {type(err).__name__}: {err}"
        return ok, "" if ok else opts.get("custom_msg", "Todavía no es correcto. ¡Sigue intentándolo!")
    if "resultado" not in ns:
        return False, "Guarda tu respuesta en la variable `resultado`."
    return pq_compare(ns["resultado"], exp_ns["resultado"],
                      ordered=opts.get("ordered", True),
                      ignore_index=opts.get("ignore_index", False))


_ERR_TIPS = [
    ("truth value of a Series is ambiguous", "Para combinar condiciones usa & (y), | (o) y pon cada condición entre paréntesis."),
    ("KeyError", "Revisa que el nombre de la columna esté bien escrito (mayúsculas, tildes, espacios)."),
    ("NameError", "Estás usando una variable que no existe. ¿Un error de tipeo?"),
    ("SyntaxError", "Hay un error de sintaxis: revisa paréntesis, comillas y que la línea `resultado = ...` esté completa."),
    ("AttributeError", "Ese método o atributo no existe para este objeto. Revisa el nombre."),
    ("TypeError", "Algún tipo de dato no encaja (¿texto mezclado con números?)."),
    ("IndentationError", "Revisa la sangría (espacios al inicio de la línea)."),
    ("MergeError", "Revisa las columnas que usas para unir (on / left_on / right_on)."),
]


def pq_error_tip(msg):
    for key, tip in _ERR_TIPS:
        if key in msg:
            return tip
    return ""
