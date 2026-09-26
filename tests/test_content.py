"""Valida todo el contenido: cada solución pasa su propio corrector y cada plantilla falla.

Uso:  python tests/test_content.py
"""
import os
import re
import sys
import warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
sys.path.insert(0, os.path.join(ROOT, "py"))

warnings.simplefilter("ignore")
import pandas as pd  # noqa: E402

from content import MODULES, SETUP  # noqa: E402
from pq_core import pq_check  # noqa: E402


def strip_comments(code):
    return "\n".join(re.sub(r"#.*$", "", line) for line in code.splitlines())


def run(setup, code):
    ns = {}
    exec(setup, ns)
    ns["_pq_code"] = strip_comments(code)
    exec(code, ns)
    return ns


def main():
    fails, total, ids = 0, 0, set()
    for m in MODULES:
        setup = SETUP + m.get("setup", "")
        for ex in m["exercises"]:
            total += 1
            assert ex["id"] not in ids, f"id repetido {ex['id']}"
            ids.add(ex["id"])
            opts = ex.get("check", {})
            exp_ns = run(setup, ex["solution"])
            ok, msg = pq_check(exp_ns, exp_ns, opts)
            if not ok:
                fails += 1
                print(f"FALLA solución {ex['id']}: {msg}")
            # la plantilla inicial no debe pasar
            try:
                st_ns = run(setup, ex["starter"])
                ok2, _ = pq_check(st_ns, exp_ns, opts)
            except Exception:
                ok2 = False
            if ok2:
                fails += 1
                print(f"FALLA plantilla {ex['id']}: la plantilla ya pasa el ejercicio")
            if "-v" in sys.argv and "resultado" in exp_ns:
                print(f"--- {ex['id']} {ex['title']}\n{exp_ns['resultado']}\n")
    print(f"{total} ejercicios, {fails} fallos")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
