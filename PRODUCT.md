# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Estudiantes de ciencia de datos e inteligencia artificial de habla hispana (el caso de origen: un estudiante universitario en Córdoba, Argentina) que parten desde cero en programación. Usan el sitio para practicar lo que ven en clase (Python, pandas, NumPy, Matplotlib, Seaborn, Machine Learning, SQL) hasta poder leer y escribir código con soltura y conseguir su primer trabajo en datos. Estudian en sesiones cortas y frecuentes, en notebook o PC, a veces también en Google Colab.

## Product Purpose

Un curso práctico e interactivo que lleva de "nunca programé" a "entrenar un modelo de ML": cada concepto se explica con ejemplos y uso real, y se practica con un ejercicio que se corrige al instante. El éxito es que el estudiante complete la ruta, entienda qué hace cada línea y llegue a nivel empleable.

## Positioning

Python real corriendo en el navegador (Pyodide) con un corrector que compara el resultado del alumno contra la solución oficial y explica el error en español, sin instalar nada. Cada módulo tiene su notebook de Colab con el mismo corrector, y muchos ejercicios muestran su equivalente en SQL.

## Operating Context

- Ruta: 00 Python desde cero · 01 Pandas · 02 DataFrames (incluye SQL) · 03 NumPy · 04 Matplotlib · 05 Seaborn · 06 Introducción a Machine Learning.
- Flujo por ejercicio: leer teoría → misión → escribir código en el editor → ejecutar (Ctrl+Enter) → veredicto, salida, tabla o gráfico → siguiente reto.
- Contenido derivado de los materiales de clase del estudiante (carpeta `pandas`: Clases 1 a 4, estadística básica, parcial de base de datos).

## Capabilities and Constraints

- Sitio estático en GitHub Pages (`rosalesluciano.github.io/pandas-quest`), sin backend; progreso en `localStorage`.
- Contenido fuente en `build/*.py`; `build/build.py` genera `js/data.js` y `notebooks/*.ipynb`; `tests/test_content.py` valida que cada solución pase y cada plantilla falle.
- Python vía Pyodide en un Web Worker; librerías pesadas (matplotlib, seaborn, scikit-learn) se cargan bajo demanda.
- Gamificación: XP, niveles, combos, rachas, meta diaria y logros. Confirmado: se mantiene, con un tono más sobrio y orientado al progreso profesional.

## Brand Commitments

- Nombre: **PandasQuest** (confirmado; se mantiene aunque el temario ahora empieza en Python).
- Voz: español neutro con **tú** (confirmado). Cercana, directa, con notas "En el trabajo" que conectan cada tema con el empleo.

## Evidence on Hand

- 145 ejercicios propios con teoría, solución y corrector (7 módulos).
- No existen testimonios, cantidad de usuarios, ni avales institucionales: no inventarlos.

## Product Principles

1. Practicar antes que leer: cada concepto termina en código que se ejecuta y se corrige.
2. Entender, no memorizar: explicar el porqué, el uso real y los errores comunes.
3. Cero fricción: nada que instalar, progreso guardado, una sola acción clara por pantalla.
4. Progreso honesto: la gamificación premia intentar sin pistas, sin distraer del aprendizaje.

## Accessibility & Inclusion

Uso prolongado de lectura y código: contraste alto en claro y oscuro, navegación por teclado (Ctrl+Enter para ejecutar), respeto de `prefers-reduced-motion`, funcional en pantallas chicas.
