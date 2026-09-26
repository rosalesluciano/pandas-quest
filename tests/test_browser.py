"""Prueba end-to-end en Chromium real: resuelve los 75 ejercicios desde la interfaz.

Uso:  python -m http.server 8765  (en la raíz)  y luego  python tests/test_browser.py [url] [carpeta_capturas]
"""
import os
import sys

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/"
SHOTS = sys.argv[2] if len(sys.argv) > 2 else "."


def main():
    errors, fails = [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1400, "height": 900})
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.on("console", lambda m: m.type == "error" and errors.append(f"console: {m.text}"))
        page.goto(URL)
        page.wait_for_selector(".py-status.ready", timeout=180000)
        page.screenshot(path=os.path.join(SHOTS, "home_dark.png"), full_page=True)
        ids = page.evaluate("window.__pq.ALL.map(e => e.id)")
        print("ejercicios:", len(ids))

        # 1) Plantilla inicial del primer ejercicio: debe fallar con mensaje amigable
        page.goto(URL + "#/e/df06")
        page.wait_for_selector(".CodeMirror")
        page.evaluate("window.__pq.cm.setValue(\"resultado = clientes[clientes['pais'] == 'España' and clientes['edad'] > 3]\")")
        page.click("#runBtn")
        page.wait_for_selector(".verdict", timeout=60000)
        txt = page.inner_text(".verdict")
        assert "ambiguous" in txt and "&" in txt, txt
        page.screenshot(path=os.path.join(SHOTS, "error.png"))

        # 2) Resolver todos con la solución oficial (la 1ª carga de seaborn/sklearn tarda)
        for i, ex_id in enumerate(ids):
            page.goto(URL + f"#/e/{ex_id}")
            page.wait_for_selector(".CodeMirror")
            # la plantilla no debe aprobar
            page.evaluate(f"window.__pq.cm.setValue(window.__pq.BY_ID['{ex_id}'].starter)")
            page.click("#runBtn")
            page.wait_for_selector("#runBtn:not([disabled])", timeout=300000)
            page.wait_for_selector(".verdict, .placeholder", timeout=60000)
            if page.query_selector(".verdict.ok"):
                fails.append(f"{ex_id}: la plantilla aprueba")
            # solución
            page.evaluate(f"window.__pq.cm.setValue(window.__pq.BY_ID['{ex_id}'].solution)")
            page.click("#runBtn")
            page.wait_for_selector("#runBtn:not([disabled])", timeout=300000)
            page.wait_for_selector(".verdict", timeout=60000)
            if not page.query_selector(".verdict.ok"):
                fails.append(f"{ex_id}: {page.inner_text('.verdict')[:300]}")
            if ex_id in ("df23", "plt10", "sns10", "ml10"):
                page.screenshot(path=os.path.join(SHOTS, f"ok_{ex_id}.png"), full_page=True)
            # los modales de nivel/módulo aparecen tras la celebración: esperar y cerrarlos
            page.wait_for_timeout(1300)
            while page.query_selector("#modal:not(.hidden)"):
                page.keyboard.press("Escape")
                page.wait_for_timeout(100)
            print(f"{i + 1:02d} {ex_id} ok" if not fails or not fails[-1].startswith(ex_id) else f"{i + 1:02d} {ex_id} FALLA")

        st = page.evaluate("({xp: window.__pq.state.xp, n: Object.keys(window.__pq.state.solved).length, badges: Object.keys(window.__pq.state.badges)})")
        print("estado final:", st)

        # 3) Modal de tablas
        page.goto(URL + "#/e/df27")
        page.wait_for_selector(".CodeMirror")
        page.click("#tablesBtn")
        page.wait_for_selector("#tblBody table.df", timeout=60000)
        page.click(".tab[data-t='trimestral']")
        assert "Centro" in page.inner_text("#tblBody")
        page.screenshot(path=os.path.join(SHOTS, "tables.png"))
        page.keyboard.press("Escape")

        # 4) Bucle infinito: debe cortarse y reiniciar Python
        page.goto(URL + "#/e/pd01")
        page.wait_for_selector(".CodeMirror")
        page.evaluate("window.__pq.cm.setValue('while True:\\n    pass')")
        page.click("#runBtn")
        page.wait_for_selector(".verdict.bad", timeout=90000)
        assert "tardó demasiado" in page.inner_text(".verdict")
        page.wait_for_selector(".py-status.ready", timeout=180000)
        page.evaluate("window.__pq.cm.setValue(window.__pq.BY_ID['pd01'].solution)")
        page.click("#runBtn")
        page.wait_for_selector(".verdict.ok", timeout=60000)
        print("bucle infinito: ok")

        page.goto(URL)
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(SHOTS, "home_done.png"), full_page=True)

        # 5) Tema claro y móvil (estado limpio)
        ctx = b.new_context(viewport={"width": 390, "height": 844}, color_scheme="light")
        mp = ctx.new_page()
        mp.on("pageerror", lambda e: errors.append(f"mobile pageerror: {e}"))
        mp.goto(URL)
        mp.wait_for_selector(".mod")
        mp.screenshot(path=os.path.join(SHOTS, "mobile_home.png"), full_page=True)
        overflow = mp.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        mp.goto(URL + "#/e/df19")
        mp.wait_for_selector(".CodeMirror")
        mp.screenshot(path=os.path.join(SHOTS, "mobile_ex.png"), full_page=True)
        overflow2 = mp.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        if overflow or overflow2:
            fails.append(f"scroll horizontal en móvil: home={overflow} ejercicio={overflow2}")
        lp = b.new_page(viewport={"width": 1400, "height": 900}, color_scheme="light")
        lp.goto(URL + "#/e/np10")
        lp.wait_for_selector(".CodeMirror")
        lp.screenshot(path=os.path.join(SHOTS, "exercise_light.png"))
        b.close()

    print("\nerrores de consola:", errors or "ninguno")
    print("fallos:", fails or "ninguno")
    return 1 if (fails or errors) else 0


if __name__ == "__main__":
    sys.exit(main())
