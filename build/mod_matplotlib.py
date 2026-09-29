# -*- coding: utf-8 -*-
"""Módulo 04 · Matplotlib. Los checks inspeccionan la figura con los helpers de pq_core (_ax, _fig, _legend...)."""

P = {"plot": True}


def chk(expr, msg):
    return dict(P, custom=expr, custom_msg=msg)


EXERCISES = [
# =========================================================== Primeros gráficos
dict(id="plt01", sec="Primeros gráficos", title="Tu primer gráfico", level=1,
theory="""**Matplotlib** es la librería de gráficos más usada de Python y la base de otras como seaborn o el `.plot()` de pandas. Su módulo principal se importa así:

```python
import matplotlib.pyplot as plt
```

El gráfico más básico es el de **líneas**: `plt.plot(x, y)` une los puntos con una línea. Es ideal para ver cómo **evoluciona** algo en el tiempo.

```python
plt.plot([1, 2, 3], [10, 30, 20])
```

En este módulo tienes cargadas las listas `meses`, `ingresos` y `gastos` (en miles), además de las tablas del curso.

> 💡 En Colab/Jupyter el gráfico aparece solo al final de la celda. En un script de Python hace falta `plt.show()`.""",
task="Dibuja un gráfico de líneas con `meses` en el eje X e `ingresos` en el eje Y.",
starter="# plt ya está importado\n",
solution="plt.plot(meses, ingresos)",
hint="plt.plot(meses, ingresos)",
check=chk("len(_ax().lines) == 1 and list(_ax().lines[0].get_ydata()) == ingresos",
          "Debe haber una línea con los valores de `ingresos` en el eje Y.")),

dict(id="plt02", sec="Primeros gráficos", title="Título y etiquetas", level=1,
theory="""Un gráfico sin título ni etiquetas **no comunica**: quien lo mire no sabrá qué representa. Siempre añade:

```python
plt.title("Ventas 2024")
plt.xlabel("Mes")
plt.ylabel("Unidades vendidas")
```

> 💼 **En el trabajo:** un gráfico en una presentación debe entenderse **en 5 segundos** sin que nadie lo explique. Título claro, ejes con nombre y unidades.""",
task="Dibuja `ingresos` por mes y añade el título **\"Ingresos por mes\"**, la etiqueta X **\"Mes\"** y la etiqueta Y **\"Ingresos (miles)\"** (escríbelos exactamente así).",
starter="plt.plot(meses, ingresos)\n# añade título y etiquetas\n",
solution="plt.plot(meses, ingresos)\nplt.title('Ingresos por mes')\nplt.xlabel('Mes')\nplt.ylabel('Ingresos (miles)')",
hint="plt.title('...'), plt.xlabel('...'), plt.ylabel('...')",
check=chk("len(_ax().lines) == 1 and _ax().get_title() == 'Ingresos por mes' and _ax().get_xlabel() == 'Mes' and _ax().get_ylabel() == 'Ingresos (miles)'",
          "Revisa que el título y las etiquetas estén escritos exactamente como se pide.")),

dict(id="plt03", sec="Primeros gráficos", title="Comparar con leyenda", level=2,
theory="""Puedes dibujar **varias líneas** en el mismo gráfico llamando a `plt.plot` varias veces. Para distinguirlas, pon a cada una un `label` y llama a `plt.legend()`:

```python
plt.plot(x, ventas_2023, label="2023")
plt.plot(x, ventas_2024, label="2024")
plt.legend()
```

Matplotlib asigna un color distinto a cada línea automáticamente.""",
task="Dibuja `ingresos` y `gastos` por mes en el mismo gráfico, con las etiquetas **\"Ingresos\"** y **\"Gastos\"**, y muestra la leyenda.",
starter="",
solution="plt.plot(meses, ingresos, label='Ingresos')\nplt.plot(meses, gastos, label='Gastos')\nplt.legend()",
hint="Dos plt.plot(..., label='...') y luego plt.legend()",
check=chk("len(_ax().lines) == 2 and sorted(_legend()) == ['Gastos', 'Ingresos']",
          "Deben verse 2 líneas y una leyenda con 'Ingresos' y 'Gastos'.")),

dict(id="plt04", sec="Primeros gráficos", title="Dale estilo", level=2,
theory="""`plt.plot` acepta parámetros de estilo:

| Parámetro | Ejemplos |
|---|---|
| `color` | `"red"`, `"green"`, `"#ff5733"` |
| `marker` | `"o"` (círculo), `"s"` (cuadrado), `"^"` (triángulo) |
| `linestyle` | `"-"` (sólida), `"--"` (guiones), `":"` (puntos) |
| `linewidth` | `2`, `3`… |

```python
plt.plot(x, y, color="purple", marker="s", linestyle=":")
```

> 💡 Los marcadores ayudan cuando hay pocos puntos: así se ve dónde está cada dato real.""",
task="Dibuja `ingresos` por mes en color **\"green\"**, con marcador **\"o\"** y línea de guiones **\"--\"**.",
starter="plt.plot(meses, ingresos)",
solution="plt.plot(meses, ingresos, color='green', marker='o', linestyle='--')",
hint="color='green', marker='o', linestyle='--'",
check=chk("len(_ax().lines) == 1 and _hex(_ax().lines[0].get_color()) == '#008000' and _ax().lines[0].get_marker() == 'o' and _ax().lines[0].get_linestyle() == '--'",
          "La línea debe ser verde ('green'), con marcador 'o' y estilo '--'.")),

dict(id="plt12", sec="Primeros gráficos", title="Formato abreviado y cuadrícula", level=2,
theory="""En lugar de escribir `color=`, `marker=` y `linestyle=` por separado, `plot` acepta un **formato abreviado** como tercer argumento: un texto corto que combina **color + marcador + línea**.

| Código | Significado |
|---|---|
| `'r--'` | rojo, línea discontinua |
| `'bo'` | azul, solo círculos (sin línea) |
| `'g^-'` | verde, triángulos y línea sólida |
| `'ks:'` | negro (*k*), cuadrados y línea punteada |

Colores: `r` rojo, `g` verde, `b` azul, `k` negro, `m` magenta, `c` cian, `y` amarillo.

La **cuadrícula** ayuda a leer los valores. `alpha` la hace más suave:

```python
plt.plot(x, y, 'bo-')
plt.grid(True, alpha=0.3)
```""",
task="Dibuja `y` en función de `x` con **línea verde continua y marcadores cuadrados** usando el formato abreviado, y activa la **cuadrícula**.",
starter="x = [0, 1, 2, 3, 4]\ny = [1, 4, 6, 8, 10]\nplt.plot(x, y)",
solution="x = [0, 1, 2, 3, 4]\ny = [1, 4, 6, 8, 10]\nplt.plot(x, y, 'gs-')\nplt.grid(True)",
hint="plt.plot(x, y, 'gs-')  y  plt.grid(True)",
check=chk("len(_ax().lines) == 1 and _hex(_ax().lines[0].get_color()) == '#008000' and _ax().lines[0].get_marker() == 's' and _ax().lines[0].get_linestyle() == '-' and _ax().xaxis.get_gridlines()[0].get_visible()",
          "La línea debe ser verde ('g'), con cuadrados ('s') y sólida ('-'). Y no olvides plt.grid(True).")),

dict(id="plt13", sec="Primeros gráficos", title="Límites de los ejes", level=2,
theory="""Matplotlib elige los límites de los ejes automáticamente, pero a veces conviene fijarlos: para comparar varios gráficos con la misma escala, o para enfocar una zona.

```python
plt.xlim(0, 10)              # eje X de 0 a 10
plt.ylim(-5, 100)            # eje Y de -5 a 100
plt.axis([0, 10, -5, 100])   # lo mismo en una línea: [xmin, xmax, ymin, ymax]
```

> ⚠️ Cuidado con cortar el eje Y para exagerar diferencias: un gráfico de barras que no empieza en 0 puede engañar a quien lo lee.""",
task="Dibuja `y` en función de `x` y fija el **eje X de -1 a 6** y el **eje Y de -2 a 15**.",
starter="x = [0, 1, 2, 3, 4]\ny = [1, 4, 6, 8, 10]\nplt.plot(x, y, 'gs-')",
solution="x = [0, 1, 2, 3, 4]\ny = [1, 4, 6, 8, 10]\nplt.plot(x, y, 'gs-')\nplt.xlim(-1, 6)\nplt.ylim(-2, 15)",
hint="plt.xlim(-1, 6)  y  plt.ylim(-2, 15)",
check=chk("len(_ax().lines) == 1 and tuple(round(v, 6) for v in _ax().get_xlim()) == (-1, 6) and tuple(round(v, 6) for v in _ax().get_ylim()) == (-2, 15)",
          "El eje X debe ir de -1 a 6 y el eje Y de -2 a 15.")),

dict(id="plt14", sec="Primeros gráficos", title="Guardar tu gráfico", level=1,
theory="""`plt.savefig()` guarda el gráfico en un archivo para usarlo en un informe, una presentación o una web:

```python
plt.plot(numeros)
plt.savefig("mi_grafico.png", dpi=300, bbox_inches="tight")
```

- La **extensión** define el formato: `.png` (imagen), `.pdf` o `.svg` (vectorial: no pierde calidad al agrandarse).
- `dpi=300` → alta resolución, ideal para imprimir.
- `bbox_inches="tight"` → recorta los márgenes blancos sobrantes.

> ⚠️ Llama a `savefig` **antes** de `plt.show()`: después de mostrarse, la figura se vacía y guardarías una imagen en blanco.""",
task="Dibuja la línea de `numeros` y guárdala como **`mi_grafico.png`** con `dpi=150`.",
starter="numeros = [4, 2, 7, 6, 3]\nplt.plot(numeros)",
solution="numeros = [4, 2, 7, 6, 3]\nplt.plot(numeros)\nplt.savefig('mi_grafico.png', dpi=150)",
hint="plt.savefig('mi_grafico.png', dpi=150)",
check=chk("len(_ax().lines) == 1 and 'savefig' in _pq_code and 'mi_grafico.png' in _pq_code and __import__('os').path.exists('mi_grafico.png')",
          "Usa plt.savefig('mi_grafico.png', dpi=150) después de dibujar.")),

# =========================================================== Tipos de gráfico
dict(id="plt05", sec="Tipos de gráfico", title="Gráfico de barras", level=1,
theory="""Las **barras** sirven para **comparar cantidades entre categorías** (productos, países, vendedores…):

```python
plt.bar(categorias, valores)
```

Si los nombres son largos y se superponen, gíralos:

```python
plt.xticks(rotation=45)
```

> 💡 **¿Líneas o barras?** Líneas para tendencias en el tiempo; barras para comparar categorías.""",
task="Dibuja un gráfico de barras con el `stock` de cada `producto` de la tabla `productos`.",
starter="",
solution="plt.bar(productos['producto'], productos['stock'])\nplt.xticks(rotation=45)",
hint="plt.bar(productos['producto'], productos['stock'])",
check=chk("len(_ax().patches) == 10 and _heights() == productos['stock'].tolist()",
          "Debe haber 10 barras con el stock de cada producto, en el orden de la tabla.")),

dict(id="plt06", sec="Tipos de gráfico", title="Barras horizontales: un top 5", level=2,
theory="""`plt.barh(categorias, valores)` dibuja **barras horizontales**. Son ideales para los rankings, porque los nombres se leen cómodamente.

Lo habitual es preparar los datos primero con pandas y después graficar:

```python
top = df.nlargest(5, "ventas")
plt.barh(top["vendedor"], top["ventas"])
```

> 💼 **En el trabajo:** "Top 10 productos", "Top 5 clientes"… los gráficos de ranking están en todos los dashboards.""",
task="Obtén los **5 productos más caros** con `nlargest` y dibújalos con barras horizontales (`producto` y `precio`).",
starter="top = \n",
solution="top = productos.nlargest(5, 'precio')\nplt.barh(top['producto'], top['precio'])",
hint="top = productos.nlargest(5, 'precio'); plt.barh(top['producto'], top['precio'])",
check=chk("len(_ax().patches) == 5 and sorted(_widths()) == sorted(productos.nlargest(5, 'precio')['precio'].tolist())",
          "Debe haber 5 barras horizontales con los precios de los 5 productos más caros.")),

dict(id="plt07", sec="Tipos de gráfico", title="Histograma", level=2,
theory="""Un **histograma** muestra la **distribución** de una variable numérica: divide el rango en intervalos (*bins*) y cuenta cuántos valores caen en cada uno.

```python
plt.hist(datos, bins=20, edgecolor="black")
```

Con él respondes preguntas como: ¿los valores se concentran en el centro? ¿hay valores extremos? ¿la distribución es simétrica?

> ⚠️ El número de `bins` cambia mucho la lectura: con pocos se pierde detalle y con demasiados aparece ruido. Prueba varios.""",
task="Dibuja un histograma de la columna `ventas` de `ventas_diarias` con **12 bins**.",
starter="",
solution="plt.hist(ventas_diarias['ventas'], bins=12, edgecolor='black')",
hint="plt.hist(ventas_diarias['ventas'], bins=12)",
check=chk("len(_ax().patches) == 12 and sum(_heights()) == 90",
          "El histograma debe tener 12 barras con los 90 días de ventas.")),

dict(id="plt08", sec="Tipos de gráfico", title="Dispersión: ¿hay relación?", level=2,
theory="""El gráfico de **dispersión** (*scatter*) pone un punto por cada observación, con una variable en cada eje. Sirve para ver si dos variables están **relacionadas**:

- los puntos suben juntos: relación **positiva**;
- uno sube y el otro baja: relación **negativa**;
- nube sin forma: **no hay relación**.

```python
plt.scatter(df["publicidad"], df["ventas"], alpha=0.6)
```

`alpha` añade transparencia, que viene bien cuando hay muchos puntos superpuestos.""",
task="Dibuja un gráfico de dispersión de `ventas_diarias` con `visitas` en X y `ventas` en Y. Pon las etiquetas de eje **\"Visitas\"** y **\"Ventas\"**.",
starter="",
solution="plt.scatter(ventas_diarias['visitas'], ventas_diarias['ventas'])\nplt.xlabel('Visitas')\nplt.ylabel('Ventas')",
hint="plt.scatter(x, y) + plt.xlabel / plt.ylabel",
check=chk("len(_ax().collections) == 1 and len(_ax().collections[0].get_offsets()) == 90 and _ax().get_xlabel() == 'Visitas' and _ax().get_ylabel() == 'Ventas'",
          "Debe haber un scatter con los 90 días y las etiquetas 'Visitas' y 'Ventas'.")),

dict(id="plt09", sec="Tipos de gráfico", title="Gráfico de torta", level=2,
theory="""El gráfico de **torta** (*pie*) muestra **proporciones de un total**. `autopct` escribe el porcentaje dentro de cada porción:

```python
plt.pie(valores, labels=nombres, autopct="%1.0f%%")
```

El formato `"%1.0f%%"` significa: número sin decimales seguido del símbolo `%`.

> ⚠️ Úsalo solo con **pocas categorías** (hasta unas 5). Con más, un gráfico de barras se lee mucho mejor.""",
task="Cuenta cuántos productos hay por `categoria` (con `value_counts`) y dibuja una torta con las etiquetas de cada categoría y los porcentajes (`autopct`).",
starter="conteo = productos['categoria'].value_counts()\n",
solution="conteo = productos['categoria'].value_counts()\nplt.pie(conteo, labels=conteo.index, autopct='%1.0f%%')",
hint="plt.pie(conteo, labels=conteo.index, autopct='%1.0f%%')",
check=chk("len(_ax().patches) == 4 and len(_ax().texts) == 8",
          "La torta debe tener 4 porciones, con su etiqueta y su porcentaje cada una (usa labels y autopct).")),

dict(id="plt15", sec="Tipos de gráfico", title="Histogramas superpuestos", level=3,
theory="""Para **comparar distribuciones** se pueden dibujar varios histogramas en el mismo gráfico. El truco es que no se tapen entre sí:

- `histtype="step"` dibuja solo el **contorno** de cada histograma.
- `alpha` (de 0 a 1) da **transparencia**.
- `bins` define cuántos intervalos usar. Con más bins ves más detalle, pero también más ruido.

```python
plt.hist(grupo_a, bins=30, histtype="step", alpha=0.7, label="A")
plt.hist(grupo_b, bins=30, histtype="step", alpha=0.7, label="B")
plt.legend()
```

Otros parámetros útiles de `plt.hist`: `density=True` (el eje Y muestra densidad en vez de conteo) y `color` / `edgecolor` (relleno y contorno).""",
task="Dibuja los **tres** histogramas (`serie1`, `serie2`, `serie3`) en el mismo gráfico, cada uno con `bins=35`, `histtype='step'` y `alpha=0.6`.",
starter="rng = np.random.default_rng(42)\nserie1 = rng.normal(0, 1, 800)\nserie2 = rng.normal(2, 1, 600)\nserie3 = rng.normal(-2, 1, 200)\n",
solution="rng = np.random.default_rng(42)\nserie1 = rng.normal(0, 1, 800)\nserie2 = rng.normal(2, 1, 600)\nserie3 = rng.normal(-2, 1, 200)\nfor s in [serie1, serie2, serie3]:\n    plt.hist(s, bins=35, histtype='step', alpha=0.6)",
hint="plt.hist(serie1, bins=35, histtype='step', alpha=0.6)  (y lo mismo con serie2 y serie3)",
check=chk("len(_ax().patches) == 3 and all(abs((p.get_alpha() or 0) - 0.6) < 1e-9 for p in _ax().patches) and not any(p.get_fill() for p in _ax().patches)",
          "Deben verse 3 histogramas tipo 'step' (sin relleno) con alpha=0.6.")),

dict(id="plt16", sec="Tipos de gráfico", title="Scatter con dos grupos", level=2,
theory="""`plt.scatter` permite personalizar cada grupo de puntos:

| Parámetro | Qué controla | Ejemplo |
|---|---|---|
| `color` o `c` | color de los puntos | `"orange"` |
| `s` | tamaño | `80` |
| `marker` | forma | `"s"` cuadrado, `"D"` diamante, `"^"` triángulo |
| `label` | nombre en la leyenda | `"Grupo A"` |

```python
plt.scatter(x1, y1, color="orange", marker="s", label="Grupo A")
plt.scatter(x2, y2, color="purple", marker="D", label="Grupo B")
plt.legend()
```

> 💡 `plt.plot(x, y, 'o')` también dibuja puntos y es más rápido, pero **todos iguales**. `scatter` permite un color y un tamaño distinto **para cada punto** (útil para mostrar 4 variables a la vez).""",
task="Dibuja dos grupos de puntos: el **Conjunto A** (`x1`, `y1`) en color `'orange'` con marcador `'s'`, y el **Conjunto B** (`x2`, `y2`) en color `'purple'` con marcador `'D'`. Agrega la leyenda.",
starter="x1 = [0, 1, 2, 3, 4]\ny1 = [1, 4, 6, 8, 10]\nx2 = [0, 1, 2, 3, 4]\ny2 = [0, 1, 8, 27, 64]\n",
solution="x1 = [0, 1, 2, 3, 4]\ny1 = [1, 4, 6, 8, 10]\nx2 = [0, 1, 2, 3, 4]\ny2 = [0, 1, 8, 27, 64]\nplt.scatter(x1, y1, color='orange', marker='s', label='Conjunto A')\nplt.scatter(x2, y2, color='purple', marker='D', label='Conjunto B')\nplt.legend()",
hint="plt.scatter(x1, y1, color='orange', marker='s', label='Conjunto A')  ...  plt.legend()",
check=chk("len(_ax().collections) == 2 and sorted(_legend()) == ['Conjunto A', 'Conjunto B'] and _hex(_ax().collections[0].get_facecolor()[0]) == '#ffa500' and _hex(_ax().collections[1].get_facecolor()[0]) == '#800080'",
          "Deben verse 2 grupos (naranja y púrpura) y una leyenda con 'Conjunto A' y 'Conjunto B'.")),

dict(id="plt17", sec="Tipos de gráfico", title="Torta profesional", level=3,
theory="""`plt.pie` tiene varios parámetros para que la torta se lea mejor:

| Parámetro | Qué hace |
|---|---|
| `labels` | nombre de cada porción |
| `autopct` | formato del porcentaje: `'%1.1f%%'` (1 decimal), `'%1.2f%%'` (2 decimales) |
| `colors` | lista con un color por porción |
| `explode` | separa porciones del centro: `(0, 0, 0.1, 0)` separa la tercera |
| `shadow` | `True` agrega sombra |
| `startangle` | ángulo donde empieza la primera porción (90 = arriba) |

```python
plt.pie(valores, labels=nombres, autopct="%1.1f%%", explode=(0, 0.1, 0), startangle=90)
plt.axis("equal")   # que sea un círculo perfecto
```

> ⚠️ Úsala con **pocas categorías** (6 como máximo) y diferencias claras. Si no, un gráfico de barras se lee mejor.""",
task="Con `df`, dibuja una torta con las etiquetas de cada producto, porcentajes con **2 decimales** (`'%1.2f%%'`), los `colores` dados, **sombra**, la porción de **Teléfonos separada** (`explode`) y el título **'Inventario de productos tecnológicos'**.",
starter="df = pd.DataFrame({\n    'productos': ['Laptops', 'Tablets', 'Teléfonos', 'Accesorios'],\n    'cantidades': [35, 30, 25, 10]\n})\ncolores = ['blue', 'green', 'gold', 'lightcoral']\nplt.pie(df['cantidades'])",
solution="df = pd.DataFrame({\n    'productos': ['Laptops', 'Tablets', 'Teléfonos', 'Accesorios'],\n    'cantidades': [35, 30, 25, 10]\n})\ncolores = ['blue', 'green', 'gold', 'lightcoral']\nplt.pie(df['cantidades'], labels=df['productos'], autopct='%1.2f%%', colors=colores,\n        shadow=True, explode=(0, 0, 0.1, 0))\nplt.title('Inventario de productos tecnológicos')",
hint="plt.pie(df['cantidades'], labels=df['productos'], autopct='%1.2f%%', colors=colores, shadow=True, explode=(0, 0, 0.1, 0))",
check=chk("len([p for p in _ax().patches if type(p).__name__ == 'Wedge']) == 4 and '35.00%' in [t.get_text() for t in _ax().texts] and 'Teléfonos' in [t.get_text() for t in _ax().texts] and [_hex(p.get_facecolor()) for p in _ax().patches if type(p).__name__ == 'Wedge'] == ['#0000ff', '#008000', '#ffd700', '#f08080'] and tuple(round(v, 6) for v in [p for p in _ax().patches if type(p).__name__ == 'Wedge'][2].center) != (0, 0) and len(_ax().patches) > 4 and _ax().get_title() == 'Inventario de productos tecnológicos'",
          "Revisa: labels, autopct='%1.2f%%', colors=colores, shadow=True, explode=(0, 0, 0.1, 0) y el título exacto.")),

# =========================================================== Composición
dict(id="plt10", sec="Composición y pandas", title="Varios gráficos juntos", level=3,
theory="""Hasta ahora usaste la interfaz rápida (`plt.plot`). Para gráficos más complejos se usa la **interfaz orientada a objetos**, con una **figura** (`fig`) que contiene varios **ejes** (`ax`):

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))   # 1 fila, 2 columnas
ax1.plot(x, y)
ax1.set_title("Evolución")
ax2.bar(cats, vals)
ax2.set_title("Comparación")
```

Fíjate en que con ejes se usa `ax.set_title()` en lugar de `plt.title()`.

> 💼 **En el trabajo:** los informes suelen tener varios gráficos lado a lado. `plt.subplots` es la forma profesional de montarlos.""",
task="Crea una figura con **2 gráficos lado a lado**: a la izquierda, una línea de `ingresos` por mes; a la derecha, barras de `gastos` por mes.",
starter="fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))\n",
solution="fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))\nax1.plot(meses, ingresos)\nax2.bar(meses, gastos)",
hint="ax1.plot(meses, ingresos) y ax2.bar(meses, gastos)",
check=chk("len(_fig().axes) == 2 and len(_ax(0).lines) == 1 and len(_ax(1).patches) == 6",
          "Izquierda: una línea con ingresos. Derecha: 6 barras con gastos.")),

dict(id="plt11", sec="Composición y pandas", title="Graficar directo desde pandas", level=2,
theory="""Los DataFrames tienen el método **`.plot()`**, que usa matplotlib por debajo. Es la forma más rápida de graficar datos que ya están en una tabla:

```python
df.plot(x="fecha", y="ventas")                  # líneas
df.plot(x="producto", y="precio", kind="bar")   # barras
df["edad"].plot(kind="hist", bins=10)           # histograma
```

También acepta `title=`, `figsize=`, `color=`…

> 💼 **En el trabajo:** para explorar datos, `df.plot()` es lo más cómodo. Para un gráfico final pulido, matplotlib o seaborn.""",
task="Con `ventas_diarias.plot`, dibuja las `ventas` a lo largo de la `fecha` con el título **\"Ventas diarias\"**.",
starter="",
solution="ventas_diarias.plot(x='fecha', y='ventas', title='Ventas diarias')",
hint="ventas_diarias.plot(x='fecha', y='ventas', title='Ventas diarias')",
check=chk("len(_ax().lines) >= 1 and len(_ax().lines[0].get_ydata()) == 90 and _ax().get_title() == 'Ventas diarias'",
          "Debe verse una línea con los 90 días y el título 'Ventas diarias'.")),

dict(id="plt18", sec="Composición y pandas", title="Uno encima del otro", level=2,
theory="""`plt.subplots(filas, columnas)` crea una **figura** (el lienzo completo) con varios **ejes** (cada gráfico). La analogía: la figura es una pared y cada eje es un cuadro colgado en ella.

```python
fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(6, 6))   # 2 filas, 1 columna
arriba.plot(x, y)
abajo.scatter(x, y)
plt.tight_layout()   # ajusta los márgenes para que nada se superponga
```

Con una cuadrícula de varias filas **y** columnas, los ejes vienen en un array y se accede con `[fila, columna]`:

```python
fig, axes = plt.subplots(2, 2)
axes[0, 0].plot(...)   # arriba a la izquierda
axes[1, 1].bar(...)    # abajo a la derecha
```

> 💡 `sharex=True` hace que los gráficos compartan el eje X: ideal para comparar series en el mismo período.""",
task="Crea una figura con **2 gráficos, uno encima del otro**: arriba una **línea** y abajo un **scatter**, los dos con los datos `x` e `y`.",
starter="x = [0, 1, 2, 3]\ny = [1, 3, 9, 27]\nfig, (arriba, abajo) = plt.subplots(2, 1)\n",
solution="x = [0, 1, 2, 3]\ny = [1, 3, 9, 27]\nfig, (arriba, abajo) = plt.subplots(2, 1)\narriba.plot(x, y)\nabajo.scatter(x, y)\nplt.tight_layout()",
hint="arriba.plot(x, y)  y  abajo.scatter(x, y)",
check=chk("len(_fig().axes) == 2 and _ax(0).get_position().y0 > _ax(1).get_position().y0 and len(_ax(0).lines) == 1 and len(_ax(1).collections) == 1",
          "Arriba debe haber una línea y abajo un scatter (usa plt.subplots(2, 1)).")),

dict(id="plt19", sec="Composición y pandas", title="Cuadrícula de 3 × 2", level=2,
theory="""Cuando necesitas muchos gráficos (un **dashboard**), `plt.subplots` arma la cuadrícula completa de una vez. El segundo valor que devuelve es un **array de NumPy** con todos los ejes:

```python
figura, ejes = plt.subplots(3, 2, figsize=(10, 9))
ejes.shape          # (3, 2)
ejes[2, 1]          # el gráfico de la tercera fila, segunda columna
```

`figsize=(ancho, alto)` se mide en pulgadas. Y `figura.suptitle("...")` pone un título general arriba de todo.

> 💼 **En el trabajo:** un panel de 3 × 2 con las métricas clave (ventas, clientes, stock…) es un formato clásico de reporte mensual.""",
task="Crea una cuadrícula de **3 filas por 2 columnas** guardando la figura en `figura` y los ejes en `ejes`. Dibuja una línea con `datos` en el gráfico de **abajo a la derecha**.",
starter="datos = [3, 7, 4, 9]\n",
solution="datos = [3, 7, 4, 9]\nfigura, ejes = plt.subplots(3, 2)\nejes[2, 1].plot(datos)",
hint="figura, ejes = plt.subplots(3, 2)  y  ejes[2, 1].plot(datos)",
check=chk("ejes.shape == (3, 2) and len(_fig().axes) == 6 and len(ejes[2, 1].lines) == 1 and sum(len(a.lines) for a in ejes.flat) == 1",
          "Crea `figura, ejes = plt.subplots(3, 2)` y dibuja solo en ejes[2, 1].")),

dict(id="plt20", sec="Composición y pandas", title="Fondo, área y valores", level=3,
theory="""Tres detalles que hacen que un gráfico se vea profesional:

**1. Color de fondo de la figura**, con `facecolor`:

```python
plt.figure(figsize=(8, 4), facecolor="lightblue")
```

**2. Área bajo la curva**, con `fill_between`. Rellena entre la línea y el eje, y resalta la tendencia:

```python
plt.plot(meses, ventas, lw=2)
plt.fill_between(meses, ventas, alpha=0.15)
```

**3. Valores sobre las barras**, con `bar_label` (Matplotlib 3.4 o superior):

```python
barras = plt.bar(cats, vals)
plt.bar_label(barras)
```""",
task="Crea una figura con fondo **`'lightblue'`**, dibuja la línea de `ventas` por mes y rellena el **área bajo la curva** con `fill_between` y `alpha=0.2`.",
starter="meses = list(range(1, 13))\nventas = [120, 135, 115, 160, 175, 210, 198, 225, 190, 240, 265, 310]\nplt.plot(meses, ventas)",
solution="meses = list(range(1, 13))\nventas = [120, 135, 115, 160, 175, 210, 198, 225, 190, 240, 265, 310]\nplt.figure(facecolor='lightblue')\nplt.plot(meses, ventas)\nplt.fill_between(meses, ventas, alpha=0.2)",
hint="plt.figure(facecolor='lightblue')  ->  plt.plot(...)  ->  plt.fill_between(meses, ventas, alpha=0.2)",
check=chk("_hex(_fig().get_facecolor()) == '#add8e6' and len(_ax().lines) == 1 and any('Poly' in type(c).__name__ and abs((c.get_alpha() or 0) - 0.2) < 1e-9 for c in _ax().collections)",
          "La figura debe tener fondo 'lightblue', una línea y el área rellena con fill_between(alpha=0.2).")),
]
