# 🐼 PandasQuest

Aprende **ciencia de datos con Python** resolviendo ejercicios prácticos, con corrección al instante.

👉 **Web:** https://rosalesluciano.github.io/pandas-quest/

- **103 ejercicios en 6 módulos**:
  1. 🐼 **Pandas**: Series, operaciones vectorizadas, lectura y exportación de datos.
  2. 📋 **DataFrames**: seleccionar, filtrar, limpiar, agrupar, unir, reestructurar, fechas y **bases de datos SQL**.
  3. 🔢 **NumPy**: arrays, indexado, broadcasting, aleatoriedad reproducible y álgebra de matrices.
  4. 📈 **Matplotlib**: líneas, barras, histogramas, dispersión, tortas y subplots (el gráfico se corrige automáticamente).
  5. 🎨 **Seaborn**: distribuciones, relaciones, categorías y mapas de correlación.
  6. 🤖 **Introducción a Machine Learning**: scikit-learn, regresión, clasificación, métricas, pipelines y validación cruzada.
- Python, pandas, matplotlib, seaborn y scikit-learn se ejecutan **en el navegador** (Pyodide): no hace falta instalar nada.
- Cada módulo tiene un **notebook de Google Colab** con los mismos datos y un corrector `comprobar()`.
- Gamificación: XP, niveles, combos, rachas diarias, meta del día y logros.
- Cada ejercicio muestra su **equivalente en SQL**.

## Estructura

| Ruta | Qué es |
|---|---|
| `build/content.py` | Datasets y definición de los módulos |
| `build/mod_*.py` | Ejercicios de cada módulo (teoría, misión, solución y corrector) |
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
