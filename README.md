# 🐼 PandasQuest

Aprende **Python pandas** de cero a nivel profesional resolviendo ejercicios prácticos, con corrección al instante.

👉 **Web:** https://rosalesluciano.github.io/pandas-quest/

- **75 ejercicios en 13 módulos**: primeros pasos, selección, filtros, limpieza, GroupBy, joins, pivot/melt, fechas, window functions, **pandas + bases de datos (SQL)**, nivel pro y desafíos de entrevista.
- Python y pandas se ejecutan **en el navegador** (Pyodide): no hace falta instalar nada.
- Cada módulo tiene un **notebook de Google Colab** con los mismos datos y un corrector `comprobar()`.
- Gamificación: XP, niveles, combos, rachas diarias, meta del día y logros.
- Cada ejercicio muestra su **equivalente en SQL**.

## Estructura

| Ruta | Qué es |
|---|---|
| `build/content.py` | Fuente única del contenido (datos, ejercicios y soluciones) |
| `build/build.py` | Genera `js/data.js` y `notebooks/*.ipynb` |
| `py/pq_core.py` | Motor de corrección (web, Colab y tests) |
| `py/pq_web.py`, `js/worker.js` | Ejecución de Python en el navegador |
| `tests/` | Tests de contenido y end-to-end en navegador |

## Desarrollo

```bash
python build/build.py                 # regenerar datos y notebooks
python tests/test_content.py          # validar soluciones (requiere pandas)
python -m http.server 8765            # servir la web en local
python tests/test_browser.py          # prueba E2E (requiere playwright)
```
