# -*- coding: utf-8 -*-
"""Fuente única de contenido de PandasQuest.

build.py genera a partir de aquí: js/data.js (web) y notebooks/*.ipynb (Colab).
tests/test_content.py valida que cada solución pase y cada plantilla inicial falle.
"""

SETUP = '''import pandas as pd
import numpy as np

clientes = pd.DataFrame({
    "cliente_id": range(1, 13),
    "nombre": ["Ana", "Bruno", "Carla", "Diego", "Elena", "Facundo",
               "Gabriela", "Hugo", "Inés", "Julián", "Karina", "Lucas"],
    "ciudad": ["Madrid", "Buenos Aires", "CDMX", "Bogotá", "Madrid", "Lima",
               "Buenos Aires", "CDMX", "Santiago", "Bogotá", "Madrid", "Lima"],
    "pais": ["España", "Argentina", "México", "Colombia", "España", "Perú",
             "Argentina", "México", "Chile", "Colombia", "España", "Perú"],
    "edad": [34, 28, 45, 23, 51, 39, 30, 27, 42, 36, 25, 48],
    "segmento": ["Premium", "Básico", "Premium", "Básico", "Premium", "Estándar",
                 "Estándar", "Básico", "Premium", "Estándar", "Básico", "Estándar"],
    "email": ["ana@mail.com", None, "carla@mail.com", "diego@mail.com", None, "facu@mail.com",
              "gabi@mail.com", None, "ines@mail.com", "julian@mail.com", "kari@mail.com", "lucas@mail.com"],
    "fecha_registro": pd.to_datetime([
        "2023-01-15", "2023-02-03", "2023-02-20", "2023-03-11", "2023-04-02", "2023-05-19",
        "2023-06-07", "2023-07-23", "2023-08-30", "2023-09-14", "2023-10-05", "2023-11-28"]),
})

productos = pd.DataFrame({
    "producto_id": range(1, 11),
    "producto": ["Laptop", "Mouse", "Teclado", "Monitor", "Auriculares",
                 "Webcam", "Silla gamer", "Escritorio", "Tablet", "Micrófono"],
    "categoria": ["Computación", "Accesorios", "Accesorios", "Computación", "Audio",
                  "Accesorios", "Muebles", "Muebles", "Computación", "Audio"],
    "precio": [1200.0, 25.5, 45.0, 300.0, 80.0, 60.0, 250.0, 180.0, 450.0, 95.0],
    "stock": [5, 150, 80, 20, 60, 0, 12, 7, 15, 0],
})

_estados = ["entregado", "enviado", "entregado", "cancelado", "entregado", "pendiente"]
pedidos = pd.DataFrame({
    "pedido_id": range(1001, 1031),
    "cliente_id": [(i * 7) % 11 + 1 for i in range(29)] + [99],
    "producto_id": [(i * 3) % 10 + 1 for i in range(30)],
    "cantidad": [(i % 4) + 1 for i in range(30)],
    "fecha": pd.date_range("2024-01-03", periods=30, freq="5D"),
    "estado": [_estados[i % 6] for i in range(30)],
})

empleados = pd.DataFrame({
    "emp_id": range(1, 11),
    "nombre": ["Marta", "Pablo", "Sofía", "Tomás", "Valeria",
               "Andrés", "Lucía", "Martín", "Paula", "Ramiro"],
    "depto": ["Dirección", "Ventas", "Ventas", "Ventas", "IT",
              "IT", "IT", "Marketing", "Marketing", "Ventas"],
    "salario": [9000, 4200, 3900, 4000, 5200, 4800, 6100, 3700, 4100, 3500],
    "jefe_id": pd.array([None, 1, 2, 2, 1, 5, 5, 1, 8, 2], dtype="Int64"),
    "fecha_ingreso": pd.to_datetime([
        "2015-03-01", "2018-06-15", "2019-01-10", "2020-09-01", "2017-11-20",
        "2021-02-01", "2016-08-08", "2022-04-18", "2019-07-07", "2023-01-09"]),
})

_i = np.arange(90)
_f = pd.date_range("2024-01-01", periods=90, freq="D")
_v = 1000 + 8 * _i + 250 * (_f.dayofweek >= 5) + ((_i * 37) % 11) * 20
_v = np.where(np.isin(_i, [20, 55, 77]), _v + 1500, _v)
ventas_diarias = pd.DataFrame({
    "fecha": _f,
    "ventas": _v.astype(float),
    "visitas": (300 + (_i * 13) % 97 + 2 * _i).astype(int),
})

sucio = pd.DataFrame({
    "id": [1, 2, 2, 3, 4, 5, 6, 7],
    "nombre": ["  ana ", "BRUNO", "BRUNO", "carla", None, "Diego  ", "elena", "facundo"],
    "edad": ["34", "28", "28", "n/d", "23", "51", None, "39"],
    "ciudad": ["madrid", "Buenos Aires", "Buenos Aires", " santiago", "bogotá", "Madrid ", "madrid", "LIMA"],
    "monto": ["$1,200.50", "$300", "$300", "$45.00", None, "$80.5", "$99", "$1,000"],
})
del _i, _f, _v, _estados
'''

TABLES = ["clientes", "productos", "pedidos", "empleados", "ventas_diarias", "sucio"]

SQL_SETUP = '''
import sqlite3
conn = sqlite3.connect(":memory:")
clientes.to_sql("clientes", conn, index=False)
productos.to_sql("productos", conn, index=False)
pedidos.to_sql("pedidos", conn, index=False)
'''

RESHAPE_SETUP = '''
trimestral = pd.DataFrame({
    "tienda": ["Centro", "Norte", "Sur"],
    "Q1": [100, 80, 60],
    "Q2": [120, 95, 70],
    "Q3": [130, 90, 85],
})
'''

# Cada ejercicio: id, title, level (1-4), theory, task, starter, solution, hint, sql, check(opcional)
# check: {"ordered": bool, "ignore_index": bool} o {"custom": "expr", "custom_msg": "..."}

MODULES = [
# ---------------------------------------------------------------- 1
{
"id": "m01", "title": "Primeros pasos", "icon": "🐣", "color": "#22d3a0",
"desc": "Series, DataFrames y cómo echarle un primer vistazo a los datos.",
"exercises": [
dict(id="m01e1", title="Hola, pandas 👋", level=1,
theory="""Una **Series** es una columna con etiquetas (el *índice*). Se crea con `pd.Series(valores, index=etiquetas)`.

```python
temperaturas = pd.Series([22, 25, 19], index=["lun", "mar", "mié"])
```""",
task="Crea una Series con los valores `10, 20, 30` y el índice `'a', 'b', 'c'`. Guárdala en `resultado`.",
starter="# Escribe tu código aquí 👇\nresultado = ",
solution="resultado = pd.Series([10, 20, 30], index=['a', 'b', 'c'])",
hint="pd.Series([10, 20, 30], index=[...])",
sql="-- En SQL no hay Series: sería una columna suelta\nSELECT valor FROM tabla;"),

dict(id="m01e2", title="Tu primer DataFrame", level=1,
theory="""Un **DataFrame** es una tabla: varias Series que comparten índice. La forma más común de crearlo es con un diccionario `{columna: lista_de_valores}`.

```python
df = pd.DataFrame({"fruta": ["pera", "uva"], "kilos": [3, 5]})
```""",
task="Crea un DataFrame con la columna `jugador` = `Messi, Ronaldo, Mbappé` y la columna `goles` = `30, 25, 28` (en ese orden).",
starter="resultado = pd.DataFrame({\n    # completa aquí\n})",
solution="resultado = pd.DataFrame({'jugador': ['Messi', 'Ronaldo', 'Mbappé'], 'goles': [30, 25, 28]})",
hint="Las claves del diccionario son los nombres de columna: {'jugador': [...], 'goles': [...]}",
sql="CREATE TABLE jugadores (jugador TEXT, goles INT);\nINSERT INTO jugadores VALUES ('Messi',30),('Ronaldo',25),('Mbappé',28);"),

dict(id="m01e3", title="¿Qué tan grande es?", level=1,
theory="""Ya tienes cargadas varias tablas: `clientes`, `productos`, `pedidos`, `empleados`, `ventas_diarias` y `sucio` (puedes verlas con el botón **Tablas**).

`df.shape` devuelve una tupla `(filas, columnas)`. `len(df)` devuelve solo las filas.""",
task="Guarda en `resultado` la forma (shape) de la tabla `clientes`.",
starter="resultado = ",
solution="resultado = clientes.shape",
hint="shape es un atributo, no lleva paréntesis: clientes.shape",
sql="SELECT COUNT(*) FROM clientes;  -- filas"),

dict(id="m01e4", title="Echar un vistazo", level=1,
theory="""`df.head(n)` devuelve las primeras *n* filas (5 por defecto) y `df.tail(n)` las últimas. Es lo primero que hace cualquier analista con datos nuevos. 👀""",
task="Guarda en `resultado` las **3 primeras filas** de `productos`.",
starter="resultado = ",
solution="resultado = productos.head(3)",
hint="productos.head(3)",
sql="SELECT * FROM productos LIMIT 3;"),

dict(id="m01e5", title="Inventario de columnas", level=1,
theory="""`df.columns` devuelve las columnas (un objeto `Index`). Con `list(df.columns)` lo conviertes en una lista normal de Python. También es útil `df.dtypes` para ver el tipo de cada columna.""",
task="Guarda en `resultado` una **lista** con los nombres de las columnas de `pedidos`.",
starter="resultado = ",
solution="resultado = list(pedidos.columns)",
hint="list(pedidos.columns) o pedidos.columns.tolist()",
sql="SELECT column_name FROM information_schema.columns WHERE table_name = 'pedidos';"),

dict(id="m01e6", title="Estadística exprés", level=1,
theory="""`df.describe()` calcula de una vez count, mean, std, min, cuartiles y max de las columnas numéricas. Para una sola métrica usa `df["col"].mean()`, `.max()`, `.min()`, `.sum()`…""",
task="¿Cuál es la **edad media** de los clientes? Guárdala en `resultado`.",
starter="resultado = ",
solution="resultado = clientes['edad'].mean()",
hint="clientes['edad'].mean()",
sql="SELECT AVG(edad) FROM clientes;"),
]},
# ---------------------------------------------------------------- 2
{
"id": "m02", "title": "Seleccionar datos", "icon": "🎯", "color": "#38bdf8",
"desc": "Columnas, filas, loc e iloc: el SELECT de pandas.",
"exercises": [
dict(id="m02e1", title="Una sola columna", level=1,
theory="""Con `df["columna"]` obtienes **una Series**. Es el equivalente a elegir una columna en un `SELECT`.""",
task="Guarda en `resultado` la columna `nombre` de `clientes`.",
starter="resultado = ",
solution="resultado = clientes['nombre']",
hint="clientes['nombre']",
sql="SELECT nombre FROM clientes;"),

dict(id="m02e2", title="Varias columnas", level=1,
theory="""Para quedarte con varias columnas pasa una **lista**: `df[["a", "b"]]`. Fíjate en el doble corchete: el de fuera selecciona y el de dentro es la lista. El resultado es un DataFrame.""",
task="Guarda en `resultado` las columnas `nombre` y `ciudad` de `clientes` (en ese orden).",
starter="resultado = ",
solution="resultado = clientes[['nombre', 'ciudad']]",
hint="Doble corchete: clientes[['nombre', 'ciudad']]",
sql="SELECT nombre, ciudad FROM clientes;"),

dict(id="m02e3", title="loc: por etiquetas", level=2,
theory="""`df.loc[filas, columnas]` selecciona por **etiquetas**. Ojo: con `loc` los rangos **incluyen el final**.

```python
df.loc[0:2, ["a", "b"]]   # filas 0, 1 y 2
```""",
task="Con `loc`, toma de `productos` las filas con índice **2 a 4 (incluido)** y solo las columnas `producto` y `precio`.",
starter="resultado = productos.loc[   ]",
solution="resultado = productos.loc[2:4, ['producto', 'precio']]",
hint="productos.loc[2:4, ['producto', 'precio']]",
sql="SELECT producto, precio FROM productos LIMIT 3 OFFSET 2;"),

dict(id="m02e4", title="iloc: por posición", level=2,
theory="""`df.iloc[...]` selecciona por **posición** (como las listas de Python): el final **no** se incluye y se pueden usar negativos.

```python
df.iloc[:2]    # dos primeras filas
df.iloc[-1]    # última fila
```""",
task="Guarda en `resultado` las **3 últimas filas** de `clientes` usando `iloc`.",
starter="resultado = ",
solution="resultado = clientes.iloc[-3:]",
hint="Índices negativos: clientes.iloc[-3:]",
sql="SELECT * FROM clientes ORDER BY cliente_id DESC LIMIT 3;"),

dict(id="m02e5", title="Un valor concreto", level=2,
theory="""`set_index("col")` convierte una columna en el índice. Así puedes buscar por un valor legible:

```python
df.set_index("nombre").loc["Ana", "edad"]
```
Para un único valor también existe `.at[fila, col]`, que es más rápido.""",
task="¿Cuál es el `precio` del producto **Monitor**? Guarda el número en `resultado`.",
starter="resultado = ",
solution="resultado = productos.set_index('producto').loc['Monitor', 'precio']",
hint="productos.set_index('producto').loc['Monitor', 'precio']",
sql="SELECT precio FROM productos WHERE producto = 'Monitor';"),
]},
# ---------------------------------------------------------------- 3
{
"id": "m03", "title": "Filtrar como un pro", "icon": "🔍", "color": "#a78bfa",
"desc": "Máscaras booleanas, isin, query y nulos: el WHERE de pandas.",
"exercises": [
dict(id="m03e1", title="Mayores de 40", level=1,
theory="""Una comparación sobre una columna genera una **máscara booleana** (True/False por fila). Al pasarla entre corchetes, solo se quedan las filas True.

```python
df[df["precio"] > 100]
```""",
task="Guarda en `resultado` los clientes con `edad` **mayor que 40**.",
starter="resultado = ",
solution="resultado = clientes[clientes['edad'] > 40]",
hint="clientes[clientes['edad'] > 40]",
sql="SELECT * FROM clientes WHERE edad > 40;"),

dict(id="m03e2", title="Dos condiciones", level=2,
theory="""Para combinar condiciones usa `&` (y), `|` (o) y `~` (no). **Cada condición va entre paréntesis**; es el error número uno de principiante.

```python
df[(df["a"] > 1) & (df["b"] == "x")]
```""",
task="Clientes de **España** con segmento **Premium**.",
starter="resultado = ",
solution="resultado = clientes[(clientes['pais'] == 'España') & (clientes['segmento'] == 'Premium')]",
hint="(cond1) & (cond2), cada una entre paréntesis",
sql="SELECT * FROM clientes WHERE pais = 'España' AND segmento = 'Premium';"),

dict(id="m03e3", title="Varios valores con isin", level=2,
theory="""`df["col"].isin([...])` es el `IN` de SQL: True si el valor está en la lista. Mucho más limpio que encadenar `|`.""",
task="Pedidos cuyo `estado` sea **enviado** o **pendiente**.",
starter="resultado = ",
solution="resultado = pedidos[pedidos['estado'].isin(['enviado', 'pendiente'])]",
hint="pedidos['estado'].isin(['enviado', 'pendiente'])",
sql="SELECT * FROM pedidos WHERE estado IN ('enviado', 'pendiente');"),

dict(id="m03e4", title="query(): filtros legibles", level=2,
theory="""`df.query("expresión")` permite escribir el filtro como texto, casi como SQL. Se usa `and`/`or` y los nombres de columna van sin comillas.

```python
df.query("edad >= 18 and pais == 'Chile'")
```""",
task="Usando `query`, obtén los productos con `precio` **menor que 100** y `stock` **mayor que 0**.",
starter="resultado = productos.query(\"\")",
solution="resultado = productos.query('precio < 100 and stock > 0')",
hint="productos.query('precio < 100 and stock > 0')",
sql="SELECT * FROM productos WHERE precio < 100 AND stock > 0;"),

dict(id="m03e5", title="Filtrar texto", level=2,
theory="""El accesor `.str` trae métodos de texto vectorizados: `.str.startswith()`, `.str.contains()`, `.str.lower()`, `.str.len()`…

```python
df[df["nombre"].str.contains("an", case=False)]
```""",
task="Clientes cuya `ciudad` **empieza por \"B\"**.",
starter="resultado = ",
solution="resultado = clientes[clientes['ciudad'].str.startswith('B')]",
hint="clientes['ciudad'].str.startswith('B')",
sql="SELECT * FROM clientes WHERE ciudad LIKE 'B%';"),

dict(id="m03e6", title="Cazando nulos", level=2,
theory="""Los datos faltantes aparecen como `NaN` o `None`. **Nunca** compares con `== None`: usa `.isna()` / `.notna()`.

```python
df[df["telefono"].notna()]
```""",
task="Clientes que **no tienen email**.",
starter="resultado = ",
solution="resultado = clientes[clientes['email'].isna()]",
hint="clientes['email'].isna()",
sql="SELECT * FROM clientes WHERE email IS NULL;"),
]},
# ---------------------------------------------------------------- 4
{
"id": "m04", "title": "Ordenar y transformar", "icon": "🧪", "color": "#f472b6",
"desc": "sort_values, columnas calculadas, pd.cut, rename y drop.",
"exercises": [
dict(id="m04e1", title="Del más caro al más barato", level=1,
theory="""`df.sort_values("col")` ordena de menor a mayor. Con `ascending=False` lo inviertes.""",
task="Ordena `productos` por `precio` de **mayor a menor**.",
starter="resultado = ",
solution="resultado = productos.sort_values('precio', ascending=False)",
hint="sort_values('precio', ascending=False)",
sql="SELECT * FROM productos ORDER BY precio DESC;"),

dict(id="m04e2", title="Orden con desempate", level=2,
theory="""Puedes ordenar por varias columnas pasando listas, y elegir la dirección de cada una:

```python
df.sort_values(["a", "b"], ascending=[True, False])
```""",
task="Ordena `clientes` por `pais` (A→Z) y, dentro de cada país, por `edad` de **mayor a menor**.",
starter="resultado = ",
solution="resultado = clientes.sort_values(['pais', 'edad'], ascending=[True, False])",
hint="ascending=[True, False]",
sql="SELECT * FROM clientes ORDER BY pais ASC, edad DESC;"),

dict(id="m04e3", title="Columna calculada", level=1,
theory="""Crear una columna es tan fácil como asignarla. Las operaciones entre columnas son **vectorizadas** (se aplican a todas las filas a la vez, sin bucles).

```python
df["total"] = df["precio"] * df["cantidad"]
```""",
task="Añade a `productos` la columna `valor_stock` = `precio * stock`. Guarda el DataFrame completo en `resultado`.",
starter="# crea la columna y luego:\nresultado = productos",
solution="productos['valor_stock'] = productos['precio'] * productos['stock']\nresultado = productos",
hint="productos['valor_stock'] = productos['precio'] * productos['stock']",
sql="SELECT *, precio * stock AS valor_stock FROM productos;"),

dict(id="m04e4", title="Top 3", level=2,
theory="""`df.nlargest(n, "col")` y `df.nsmallest(n, "col")` devuelven los *n* mayores o menores. Es más rápido que ordenar todo y hacer `head`.""",
task="Los **3 productos más caros**.",
starter="resultado = ",
solution="resultado = productos.nlargest(3, 'precio')",
hint="productos.nlargest(3, 'precio')",
sql="SELECT * FROM productos ORDER BY precio DESC LIMIT 3;"),

dict(id="m04e5", title="Tramos de edad", level=3,
theory="""`pd.cut` convierte números en categorías por tramos. `bins` define los bordes (el borde derecho entra en el tramo):

```python
pd.cut(df["nota"], bins=[0, 4, 7, 10], labels=["bajo", "medio", "alto"])
```""",
task="Añade a `clientes` la columna `rango_edad`: **joven** (≤29), **adulto** (30–44) y **senior** (≥45). Guarda en `resultado` solo las columnas `nombre`, `edad` y `rango_edad`.",
starter="clientes['rango_edad'] = \nresultado = ",
solution="clientes['rango_edad'] = pd.cut(clientes['edad'], bins=[0, 29, 44, 120], labels=['joven', 'adulto', 'senior'])\nresultado = clientes[['nombre', 'edad', 'rango_edad']]",
hint="bins=[0, 29, 44, 120] y labels=['joven', 'adulto', 'senior']",
sql="SELECT nombre, edad,\n  CASE WHEN edad <= 29 THEN 'joven'\n       WHEN edad <= 44 THEN 'adulto'\n       ELSE 'senior' END AS rango_edad\nFROM clientes;"),

dict(id="m04e6", title="Renombrar y descartar", level=2,
theory="""- `df.rename(columns={"viejo": "nuevo"})` cambia nombres.
- `df.drop(columns=["col"])` elimina columnas.

Ambos devuelven un DataFrame **nuevo** (no modifican el original), así que se pueden encadenar.""",
task="A partir de `pedidos`: elimina la columna `estado` y renombra `cantidad` a `unidades`.",
starter="resultado = ",
solution="resultado = pedidos.drop(columns=['estado']).rename(columns={'cantidad': 'unidades'})",
hint="pedidos.drop(columns=[...]).rename(columns={...})",
sql="SELECT pedido_id, cliente_id, producto_id, cantidad AS unidades, fecha FROM pedidos;"),
]},
# ---------------------------------------------------------------- 5
{
"id": "m05", "title": "Limpieza de datos", "icon": "🧹", "color": "#fbbf24",
"desc": "El 80% del trabajo real: duplicados, texto sucio, tipos y nulos.",
"exercises": [
dict(id="m05e1", title="Adiós, duplicados", level=1,
theory="""La tabla `sucio` tiene de todo. `df.drop_duplicates()` elimina las filas **idénticas** (conserva la primera). Con `subset=[...]` puedes mirar solo algunas columnas. `df.duplicated()` te dice cuáles son duplicadas.""",
task="Elimina las filas duplicadas de `sucio`.",
starter="resultado = ",
solution="resultado = sucio.drop_duplicates()",
hint="sucio.drop_duplicates()",
sql="SELECT DISTINCT * FROM sucio;"),

dict(id="m05e2", title="Nombres prolijos", level=2,
theory="""Con `.str` puedes encadenar limpiezas de texto:

```python
s.str.strip()   # quita espacios al inicio y al final
s.str.title()   # Primera Letra En Mayúscula
s.str.lower()   # todo en minúsculas
```""",
task="Limpia la columna `nombre` de `sucio`: quita los espacios sobrantes y ponla en formato Título (`Ana`, `Bruno`...). Guarda la **Series** resultante.",
starter="resultado = sucio['nombre']",
solution="resultado = sucio['nombre'].str.strip().str.title()",
hint="Encadena .str.strip().str.title()",
sql="SELECT INITCAP(TRIM(nombre)) FROM sucio;  -- PostgreSQL"),

dict(id="m05e3", title="Texto a número", level=2,
theory="""Cuando una columna numérica viene como texto con basura (`"n/d"`), `astype(int)` explota. `pd.to_numeric(s, errors="coerce")` convierte lo que puede y deja `NaN` en el resto.""",
task="Convierte la columna `edad` de `sucio` a número; los valores inválidos deben quedar como NaN.",
starter="resultado = ",
solution="resultado = pd.to_numeric(sucio['edad'], errors='coerce')",
hint="pd.to_numeric(..., errors='coerce')",
sql="SELECT TRY_CAST(edad AS INT) FROM sucio;  -- SQL Server"),

dict(id="m05e4", title="Dinero con formato", level=3,
theory="""`"$1,200.50"` no es un número. Quita los símbolos con `.str.replace()` y convierte con `.astype(float)`. Usa `regex=False` para reemplazar texto literal.

```python
s.str.replace("€", "", regex=False)
```""",
task="Convierte la columna `monto` de `sucio` a `float` (sin `$` ni comas). Los nulos deben seguir siendo nulos.",
starter="resultado = ",
solution="resultado = sucio['monto'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)",
hint="Dos replace (uno para '$' y otro para ',') y luego .astype(float)",
sql="SELECT CAST(REPLACE(REPLACE(monto, '$', ''), ',', '') AS DECIMAL) FROM sucio;"),

dict(id="m05e5", title="Rellenar huecos", level=1,
theory="""`s.fillna(valor)` reemplaza los nulos. En un DataFrame puedes pasar un diccionario: `df.fillna({"col1": 0, "col2": "?"})`.""",
task="Rellena los emails vacíos de `clientes` con `\"sin_email\"`. Guarda la **Series** `email` resultante.",
starter="resultado = ",
solution="resultado = clientes['email'].fillna('sin_email')",
hint="clientes['email'].fillna('sin_email')",
sql="SELECT COALESCE(email, 'sin_email') FROM clientes;"),

dict(id="m05e6", title="Descartar filas incompletas", level=2,
theory="""`df.dropna()` elimina filas con **algún** nulo. Normalmente conviene limitarlo con `subset=[...]` a las columnas que de verdad importan.""",
task="De `sucio`, elimina las filas donde `nombre` **o** `monto` sean nulos.",
starter="resultado = ",
solution="resultado = sucio.dropna(subset=['nombre', 'monto'])",
hint="dropna(subset=['nombre', 'monto'])",
sql="SELECT * FROM sucio WHERE nombre IS NOT NULL AND monto IS NOT NULL;"),

dict(id="m05e7", title="Pipeline de limpieza completo", level=3,
theory="""En un trabajo real juntas todo en un paso. `assign` crea o reemplaza columnas y permite encadenar:

```python
df.assign(col=lambda d: d["col"].str.strip())
```""",
task="""Limpia `sucio` de una vez:
1. Elimina duplicados.
2. `ciudad`: sin espacios y en formato Título (`Madrid`, `Lima`...).
3. `edad`: numérica (inválidos → NaN).

Guarda el DataFrame resultante (mismas columnas).""",
starter="resultado = (\n    sucio\n    # .drop_duplicates()\n    # .assign(...)\n)",
solution="resultado = (\n    sucio.drop_duplicates()\n    .assign(ciudad=lambda d: d['ciudad'].str.strip().str.title(),\n            edad=lambda d: pd.to_numeric(d['edad'], errors='coerce'))\n)",
hint="sucio.drop_duplicates().assign(ciudad=lambda d: ..., edad=lambda d: ...)",
sql="SELECT DISTINCT id, nombre, TRY_CAST(edad AS INT) AS edad,\n       INITCAP(TRIM(ciudad)) AS ciudad, monto\nFROM sucio;"),
]},
# ---------------------------------------------------------------- 6
{
"id": "m06", "title": "GroupBy y agregaciones", "icon": "📊", "color": "#34d399",
"desc": "Agrupar, contar, sumar y filtrar grupos: el GROUP BY de pandas.",
"exercises": [
dict(id="m06e1", title="¿Cuántos por país?", level=1,
theory="""`s.value_counts()` cuenta cuántas veces aparece cada valor, ordenado de mayor a menor. Con `normalize=True` te da proporciones.""",
task="Cuenta cuántos clientes hay por `pais`.",
starter="resultado = ",
solution="resultado = clientes['pais'].value_counts()",
hint="clientes['pais'].value_counts()",
sql="SELECT pais, COUNT(*) FROM clientes GROUP BY pais ORDER BY 2 DESC;",
check={"ordered": False}),

dict(id="m06e2", title="Media por grupo", level=2,
theory="""El patrón **split → apply → combine**: `df.groupby("grupo")["col"].agg_func()`.

```python
ventas.groupby("tienda")["importe"].sum()
```""",
task="Edad **media** de los clientes por `segmento`.",
starter="resultado = ",
solution="resultado = clientes.groupby('segmento')['edad'].mean()",
hint="clientes.groupby('segmento')['edad'].mean()",
sql="SELECT segmento, AVG(edad) FROM clientes GROUP BY segmento;"),

dict(id="m06e3", title="Varias métricas a la vez", level=3,
theory="""Con **named aggregation** calculas varias métricas y eliges el nombre de cada una:

```python
df.groupby("g").agg(
    total=("importe", "sum"),
    pedidos=("id", "count"),
)
```""",
task="Por `categoria` de `productos`, calcula: `precio_medio` (media de precio), `stock_total` (suma de stock) y `n_productos` (cuántos productos hay).",
starter="resultado = productos.groupby('categoria').agg(\n    \n)",
solution="resultado = productos.groupby('categoria').agg(\n    precio_medio=('precio', 'mean'),\n    stock_total=('stock', 'sum'),\n    n_productos=('producto_id', 'count'),\n)",
hint="agg(precio_medio=('precio', 'mean'), stock_total=('stock', 'sum'), n_productos=('producto_id', 'count'))",
sql="SELECT categoria, AVG(precio) AS precio_medio, SUM(stock) AS stock_total,\n       COUNT(*) AS n_productos\nFROM productos GROUP BY categoria;"),

dict(id="m06e4", title="Ranking de estados", level=2,
theory="""Con `as_index=False` (o `.reset_index()`) el resultado del groupby vuelve a ser una tabla plana, lista para ordenar o exportar.""",
task="Total de `cantidad` por `estado` de pedido, como DataFrame con columnas `estado` y `cantidad`, ordenado de **mayor a menor** cantidad (si hay empate, por `estado` A→Z).",
starter="resultado = ",
solution="resultado = pedidos.groupby('estado', as_index=False)['cantidad'].sum().sort_values(['cantidad', 'estado'], ascending=[False, True])",
hint="groupby(...).sum() y luego sort_values(['cantidad', 'estado'], ascending=[False, True]) para desempatar",
sql="SELECT estado, SUM(cantidad) AS cantidad FROM pedidos\nGROUP BY estado ORDER BY cantidad DESC, estado;",
check={"ignore_index": True}),

dict(id="m06e5", title="HAVING en pandas", level=3,
theory="""En SQL filtras grupos con `HAVING`. En pandas primero agregas y luego filtras el resultado como cualquier Series:

```python
conteo = df["g"].value_counts()
conteo[conteo > 10]
```""",
task="Países con **al menos 2** clientes (Series con el conteo por país).",
starter="conteo = clientes['pais'].value_counts()\nresultado = ",
solution="conteo = clientes['pais'].value_counts()\nresultado = conteo[conteo >= 2]",
hint="conteo[conteo >= 2]",
sql="SELECT pais, COUNT(*) FROM clientes GROUP BY pais HAVING COUNT(*) >= 2;",
check={"ordered": False}),

dict(id="m06e6", title="Mejor que la media de su equipo", level=4,
theory="""`transform` devuelve un valor **por fila** (no por grupo), alineado con el DataFrame original. Ideal para comparar cada fila con su grupo:

```python
df["media_grupo"] = df.groupby("g")["x"].transform("mean")
```""",
task="Empleados que cobran **más que la media de su departamento**.",
starter="media_depto = empleados.groupby('depto')['salario'].transform('mean')\nresultado = ",
solution="media_depto = empleados.groupby('depto')['salario'].transform('mean')\nresultado = empleados[empleados['salario'] > media_depto]",
hint="empleados[empleados['salario'] > media_depto]",
sql="SELECT * FROM (\n  SELECT *, AVG(salario) OVER (PARTITION BY depto) AS media_depto\n  FROM empleados) t\nWHERE salario > media_depto;"),
]},
# ---------------------------------------------------------------- 7
{
"id": "m07", "title": "Joins: unir tablas", "icon": "🔗", "color": "#60a5fa",
"desc": "merge, left/anti joins, self joins y concat. Pensar como en una base de datos.",
"exercises": [
dict(id="m07e1", title="Inner join", level=2,
theory="""`df1.merge(df2, on="clave")` une dos tablas por una columna común. Por defecto es un **inner join**: solo quedan las filas con coincidencia en ambas.""",
task="Une `pedidos` con `productos` por `producto_id`.",
starter="resultado = ",
solution="resultado = pedidos.merge(productos, on='producto_id')",
hint="pedidos.merge(productos, on='producto_id')",
sql="SELECT * FROM pedidos p\nJOIN productos pr ON p.producto_id = pr.producto_id;",
check={"ordered": False, "ignore_index": True}),

dict(id="m07e2", title="¿Cuánto facturamos?", level=2,
theory="""Tras unir, puedes calcular columnas con datos de ambas tablas y agregarlas. Recuerda filtrar lo que no cuenta como venta.""",
task="Facturación total (`cantidad * precio`) de los pedidos que **no** están `cancelado`. Guarda un número.",
starter="df = pedidos.merge(productos, on='producto_id')\nresultado = ",
solution="df = pedidos.merge(productos, on='producto_id')\ndf = df[df['estado'] != 'cancelado']\nresultado = (df['cantidad'] * df['precio']).sum()",
hint="Filtra estado != 'cancelado' y luego (cantidad * precio).sum()",
sql="SELECT SUM(p.cantidad * pr.precio)\nFROM pedidos p JOIN productos pr USING (producto_id)\nWHERE p.estado <> 'cancelado';"),

dict(id="m07e3", title="Clientes sin pedidos", level=3,
theory="""Un **anti join** busca filas de A sin pareja en B. En pandas lo más directo es `isin` negado:

```python
a[~a["id"].isin(b["id"])]
```
También puedes hacer un `merge(how="left", indicator=True)` y filtrar `_merge == "left_only"`.""",
task="Clientes que **nunca** hicieron un pedido.",
starter="resultado = ",
solution="resultado = clientes[~clientes['cliente_id'].isin(pedidos['cliente_id'])]",
hint="~clientes['cliente_id'].isin(pedidos['cliente_id'])",
sql="SELECT c.* FROM clientes c\nLEFT JOIN pedidos p ON c.cliente_id = p.cliente_id\nWHERE p.pedido_id IS NULL;"),

dict(id="m07e4", title="Pedidos huérfanos", level=3,
theory="""Problema real de calidad de datos: filas que apuntan a claves que no existen (integridad referencial rota). `indicator=True` añade la columna `_merge` con `both`, `left_only` o `right_only`.""",
task="Encuentra los pedidos cuyo `cliente_id` **no existe** en `clientes`. Devuelve solo las columnas originales de `pedidos`.",
starter="m = pedidos.merge(clientes, on='cliente_id', how='left', indicator=True)\nresultado = ",
solution="resultado = pedidos[~pedidos['cliente_id'].isin(clientes['cliente_id'])]",
hint="Filtra m['_merge'] == 'left_only' y quédate con pedidos.columns, o usa ~isin",
sql="SELECT p.* FROM pedidos p\nLEFT JOIN clientes c ON p.cliente_id = c.cliente_id\nWHERE c.cliente_id IS NULL;",
check={"ordered": False, "ignore_index": True}),

dict(id="m07e5", title="Ventas por país", level=3,
theory="""Puedes encadenar varios `merge` como encadenas JOINs. Piensa en el grano: una fila por pedido → luego agregas.""",
task="Ingresos (`cantidad * precio`) por `pais` del cliente, **sin** pedidos cancelados, como Series ordenada de mayor a menor.",
starter="df = (pedidos\n      .merge(clientes, on='cliente_id')\n      .merge(productos, on='producto_id'))\n",
solution="df = (pedidos\n      .merge(clientes, on='cliente_id')\n      .merge(productos, on='producto_id'))\ndf = df[df['estado'] != 'cancelado']\ndf['importe'] = df['cantidad'] * df['precio']\nresultado = df.groupby('pais')['importe'].sum().sort_values(ascending=False)",
hint="Filtra cancelados, crea importe, groupby('pais')['importe'].sum().sort_values(ascending=False)",
sql="SELECT c.pais, SUM(p.cantidad * pr.precio) AS ingresos\nFROM pedidos p\nJOIN clientes c USING (cliente_id)\nJOIN productos pr USING (producto_id)\nWHERE p.estado <> 'cancelado'\nGROUP BY c.pais ORDER BY ingresos DESC;"),

dict(id="m07e6", title="¿Quién es mi jefe?", level=4,
theory="""Un **self join** une una tabla consigo misma. Cuando las claves tienen nombres distintos usa `left_on` / `right_on`, y `suffixes` para distinguir columnas repetidas.""",
task="DataFrame con columnas `nombre` (empleado) y `jefe` (nombre de su jefe) para **todos** los empleados; quien no tiene jefe queda con nulo.",
starter="m = empleados.merge(empleados, left_on='jefe_id', right_on='emp_id', how='left', suffixes=('', '_jefe'))\nresultado = ",
solution="m = empleados.merge(empleados, left_on='jefe_id', right_on='emp_id', how='left', suffixes=('', '_jefe'))\nresultado = m[['nombre', 'nombre_jefe']].rename(columns={'nombre_jefe': 'jefe'})",
hint="Selecciona ['nombre', 'nombre_jefe'] y renombra a 'jefe'",
sql="SELECT e.nombre, j.nombre AS jefe\nFROM empleados e\nLEFT JOIN empleados j ON e.jefe_id = j.emp_id;",
check={"ordered": False, "ignore_index": True}),

dict(id="m07e7", title="Apilar tablas", level=2,
theory="""`pd.concat([df1, df2])` apila DataFrames uno debajo del otro (como `UNION ALL`). Con `ignore_index=True` se renumera el índice.""",
task="Apila los clientes de **España** y luego los de **Perú**, con el índice renumerado desde 0.",
starter="espana = clientes[clientes['pais'] == 'España']\nperu = clientes[clientes['pais'] == 'Perú']\nresultado = ",
solution="espana = clientes[clientes['pais'] == 'España']\nperu = clientes[clientes['pais'] == 'Perú']\nresultado = pd.concat([espana, peru], ignore_index=True)",
hint="pd.concat([espana, peru], ignore_index=True)",
sql="SELECT * FROM clientes WHERE pais = 'España'\nUNION ALL\nSELECT * FROM clientes WHERE pais = 'Perú';"),
]},
# ---------------------------------------------------------------- 8
{
"id": "m08", "title": "Reshape: pivot y melt", "icon": "🔄", "color": "#c084fc",
"desc": "Tablas dinámicas, formato largo vs ancho y tablas cruzadas.",
"setup": RESHAPE_SETUP,
"extra_tables": ["trimestral"],
"exercises": [
dict(id="m08e1", title="Tabla dinámica", level=3,
theory="""`pd.pivot_table` es la tabla dinámica de Excel: `index` (filas), `columns` (columnas), `values` y `aggfunc`. Con `fill_value=0` rellenas las combinaciones vacías.""",
task="Une `pedidos` con `productos` y crea una tabla con `estado` en filas, `categoria` en columnas y la **suma de `cantidad`**; los huecos deben ser 0.",
starter="df = pedidos.merge(productos, on='producto_id')\nresultado = pd.pivot_table(df, )",
solution="df = pedidos.merge(productos, on='producto_id')\nresultado = pd.pivot_table(df, index='estado', columns='categoria', values='cantidad', aggfunc='sum', fill_value=0)",
hint="index='estado', columns='categoria', values='cantidad', aggfunc='sum', fill_value=0",
sql="SELECT estado,\n  SUM(CASE WHEN categoria='Audio' THEN cantidad ELSE 0 END) AS Audio,\n  SUM(CASE WHEN categoria='Muebles' THEN cantidad ELSE 0 END) AS Muebles\n  -- ...una columna por categoría\nFROM pedidos JOIN productos USING (producto_id)\nGROUP BY estado;"),

dict(id="m08e2", title="De ancho a largo", level=3,
theory="""La tabla `trimestral` está en formato **ancho** (una columna por trimestre). Para analizarla o guardarla en una base de datos se prefiere el formato **largo**: `melt`.

```python
df.melt(id_vars="id", var_name="variable", value_name="valor")
```""",
task="Convierte `trimestral` a formato largo con columnas `tienda`, `trimestre` y `ventas`.",
starter="resultado = trimestral.melt()",
solution="resultado = trimestral.melt(id_vars='tienda', var_name='trimestre', value_name='ventas')",
hint="id_vars='tienda', var_name='trimestre', value_name='ventas'",
sql="SELECT tienda, 'Q1' AS trimestre, Q1 AS ventas FROM trimestral\nUNION ALL SELECT tienda, 'Q2', Q2 FROM trimestral\nUNION ALL SELECT tienda, 'Q3', Q3 FROM trimestral;",
check={"ordered": False, "ignore_index": True}),

dict(id="m08e3", title="Tabla cruzada", level=2,
theory="""`pd.crosstab(filas, columnas)` cuenta combinaciones de dos variables categóricas. Súper útil en análisis exploratorio.""",
task="Tabla cruzada de clientes: `pais` en filas y `segmento` en columnas.",
starter="resultado = ",
solution="resultado = pd.crosstab(clientes['pais'], clientes['segmento'])",
hint="pd.crosstab(clientes['pais'], clientes['segmento'])",
sql="SELECT pais,\n  SUM(segmento='Básico') AS Básico,\n  SUM(segmento='Estándar') AS Estándar,\n  SUM(segmento='Premium') AS Premium\nFROM clientes GROUP BY pais;"),

dict(id="m08e4", title="De largo a ancho", level=3,
theory="""`df.pivot(index=..., columns=..., values=...)` es la operación inversa a `melt`. A diferencia de `pivot_table`, **no agrega**: cada combinación debe ser única.""",
task="Convierte el formato largo de vuelta a ancho: `tienda` como índice, una columna por `trimestre` y los valores de `ventas`.",
starter="largo = trimestral.melt(id_vars='tienda', var_name='trimestre', value_name='ventas')\nresultado = ",
solution="largo = trimestral.melt(id_vars='tienda', var_name='trimestre', value_name='ventas')\nresultado = largo.pivot(index='tienda', columns='trimestre', values='ventas')",
hint="largo.pivot(index='tienda', columns='trimestre', values='ventas')",
sql="-- Igual que el pivot con CASE WHEN del ejercicio anterior"),
]},
# ---------------------------------------------------------------- 9
{
"id": "m09", "title": "Fechas y series temporales", "icon": "⏱️", "color": "#fb923c",
"desc": ".dt, rangos de fechas, resample, rolling y crecimiento.",
"exercises": [
dict(id="m09e1", title="Pedidos por mes", level=2,
theory="""Las columnas de fecha tienen el accesor `.dt`: `.dt.year`, `.dt.month`, `.dt.day_name()`, `.dt.to_period("M")`… Puedes agrupar directamente por ellos.""",
task="Número de pedidos por **mes** (número de mes 1–12) como Series.",
starter="resultado = ",
solution="resultado = pedidos.groupby(pedidos['fecha'].dt.month).size()",
hint="pedidos.groupby(pedidos['fecha'].dt.month).size()",
sql="SELECT EXTRACT(MONTH FROM fecha) AS mes, COUNT(*)\nFROM pedidos GROUP BY mes;"),

dict(id="m09e2", title="Solo febrero", level=2,
theory="""Puedes comparar fechas con textos en formato ISO, o usar `between` (incluye ambos extremos):

```python
df[df["fecha"].between("2024-03-01", "2024-03-31")]
```""",
task="Pedidos realizados en **febrero de 2024**.",
starter="resultado = ",
solution="resultado = pedidos[pedidos['fecha'].between('2024-02-01', '2024-02-29')]",
hint="between('2024-02-01', '2024-02-29')",
sql="SELECT * FROM pedidos WHERE fecha BETWEEN '2024-02-01' AND '2024-02-29';"),

dict(id="m09e3", title="Ventas semanales", level=3,
theory="""`resample` agrupa una serie temporal por frecuencia (`"D"`, `"W"`, `"MS"`...). Necesita que la fecha sea el **índice**:

```python
s = df.set_index("fecha")["valor"]
s.resample("MS").sum()   # por mes
```""",
task="Suma de `ventas` por **semana** (`\"W\"`) en `ventas_diarias`.",
starter="resultado = ",
solution="resultado = ventas_diarias.set_index('fecha')['ventas'].resample('W').sum()",
hint="set_index('fecha')['ventas'].resample('W').sum()",
sql="SELECT DATE_TRUNC('week', fecha) AS semana, SUM(ventas)\nFROM ventas_diarias GROUP BY semana;"),

dict(id="m09e4", title="Media móvil", level=3,
theory="""`rolling(n)` crea ventanas deslizantes de *n* filas. La media móvil suaviza el ruido del día a día: los analistas la adoran. 📈""",
task="Media móvil de **7 días** de `ventas` en `ventas_diarias` (Series; los primeros 6 valores serán NaN).",
starter="resultado = ",
solution="resultado = ventas_diarias['ventas'].rolling(7).mean()",
hint="ventas_diarias['ventas'].rolling(7).mean()",
sql="SELECT fecha, AVG(ventas) OVER (ORDER BY fecha ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)\nFROM ventas_diarias;  -- (SQL no pone NaN en los 6 primeros)"),

dict(id="m09e5", title="Crecimiento diario", level=3,
theory="""`shift(1)` desplaza la serie una fila (el valor de ayer). `pct_change()` calcula directamente `(hoy - ayer) / ayer`.""",
task="Variación **porcentual** diaria de `ventas` (multiplicada por 100).",
starter="resultado = ",
solution="resultado = ventas_diarias['ventas'].pct_change() * 100",
hint="ventas_diarias['ventas'].pct_change() * 100",
sql="SELECT fecha,\n  100.0 * (ventas - LAG(ventas) OVER (ORDER BY fecha)) / LAG(ventas) OVER (ORDER BY fecha)\nFROM ventas_diarias;"),

dict(id="m09e6", title="Antigüedad", level=2,
theory="""Restar fechas da un **Timedelta**. Con `.dt.days` obtienes los días como número.

```python
(pd.Timestamp("2024-12-31") - df["fecha"]).dt.days
```""",
task="Días de antigüedad de cada empleado al **2024-12-31** (Series de enteros).",
starter="resultado = ",
solution="resultado = (pd.Timestamp('2024-12-31') - empleados['fecha_ingreso']).dt.days",
hint="(pd.Timestamp('2024-12-31') - empleados['fecha_ingreso']).dt.days",
sql="SELECT DATEDIFF('2024-12-31', fecha_ingreso) FROM empleados;"),
]},
# ---------------------------------------------------------------- 10
{
"id": "m10", "title": "Window functions", "icon": "🪟", "color": "#f87171",
"desc": "RANK, ROW_NUMBER, acumulados y LAG... versión pandas.",
"exercises": [
dict(id="m10e1", title="Ranking por departamento", level=3,
theory="""`groupby(...)["col"].rank()` es el `RANK() OVER (PARTITION BY ...)` de SQL. `method="dense"` no deja huecos y `ascending=False` pone al mayor en 1.""",
task="Añade a `empleados` la columna `ranking`: posición del salario **dentro de su depto** (1 = el que más cobra, método `dense`). Guarda `nombre`, `depto`, `salario`, `ranking`.",
starter="empleados['ranking'] = \nresultado = empleados[['nombre', 'depto', 'salario', 'ranking']]",
solution="empleados['ranking'] = empleados.groupby('depto')['salario'].rank(method='dense', ascending=False)\nresultado = empleados[['nombre', 'depto', 'salario', 'ranking']]",
hint="groupby('depto')['salario'].rank(method='dense', ascending=False)",
sql="SELECT nombre, depto, salario,\n  DENSE_RANK() OVER (PARTITION BY depto ORDER BY salario DESC) AS ranking\nFROM empleados;"),

dict(id="m10e2", title="El mejor pagado de cada área", level=3,
theory="""Patrón **top-N por grupo**: ordena y luego `groupby(...).head(n)`. Equivale a `ROW_NUMBER() ... WHERE rn <= n`.""",
task="El empleado con **mayor salario de cada depto** (filas completas de `empleados`).",
starter="resultado = ",
solution="resultado = empleados.sort_values('salario', ascending=False).groupby('depto').head(1)",
hint="sort_values('salario', ascending=False).groupby('depto').head(1)",
sql="SELECT * FROM (\n  SELECT *, ROW_NUMBER() OVER (PARTITION BY depto ORDER BY salario DESC) AS rn\n  FROM empleados) t\nWHERE rn = 1;",
check={"ordered": False}),

dict(id="m10e3", title="Total acumulado", level=4,
theory="""`cumsum()` suma acumulada; combinada con `groupby` reinicia en cada grupo. **Ordena antes** por fecha para que el acumulado tenga sentido.""",
task="Une `pedidos` con `productos`, calcula `importe` = `cantidad * precio`, ordena por `cliente_id` y `fecha`, y crea `acumulado`: gasto acumulado de cada cliente. Guarda las columnas `cliente_id`, `fecha`, `importe`, `acumulado`.",
starter="df = pedidos.merge(productos, on='producto_id')\n",
solution="df = pedidos.merge(productos, on='producto_id')\ndf['importe'] = df['cantidad'] * df['precio']\ndf = df.sort_values(['cliente_id', 'fecha'])\ndf['acumulado'] = df.groupby('cliente_id')['importe'].cumsum()\nresultado = df[['cliente_id', 'fecha', 'importe', 'acumulado']]",
hint="df.groupby('cliente_id')['importe'].cumsum() después de ordenar",
sql="SELECT cliente_id, fecha, cantidad * precio AS importe,\n  SUM(cantidad * precio) OVER (PARTITION BY cliente_id ORDER BY fecha) AS acumulado\nFROM pedidos JOIN productos USING (producto_id);",
check={"ordered": False, "ignore_index": True}),

dict(id="m10e4", title="Días entre pedidos (LAG)", level=4,
theory="""`groupby(...)["fecha"].diff()` resta a cada fila la anterior **de su mismo grupo** (como `fecha - LAG(fecha)`). El primero de cada grupo queda NaN.""",
task="Ordena `pedidos` por `cliente_id` y `fecha` y añade `dias_desde_anterior`: días desde el pedido anterior del mismo cliente. Guarda `pedido_id`, `cliente_id`, `fecha`, `dias_desde_anterior`.",
starter="df = pedidos.sort_values(['cliente_id', 'fecha'])\n",
solution="df = pedidos.sort_values(['cliente_id', 'fecha'])\ndf['dias_desde_anterior'] = df.groupby('cliente_id')['fecha'].diff().dt.days\nresultado = df[['pedido_id', 'cliente_id', 'fecha', 'dias_desde_anterior']]",
hint="df.groupby('cliente_id')['fecha'].diff().dt.days",
sql="SELECT pedido_id, cliente_id, fecha,\n  fecha - LAG(fecha) OVER (PARTITION BY cliente_id ORDER BY fecha) AS dias\nFROM pedidos;",
check={"ordered": False, "ignore_index": True}),

dict(id="m10e5", title="Porcentaje del total", level=3,
theory="""Dividir por `transform("sum")` te da la participación de cada fila en su grupo: `SUM(x) OVER (PARTITION BY g)`.""",
task="Añade a `empleados` la columna `pct_depto`: % que representa el salario de cada uno sobre el total de su depto (0–100). Guarda `nombre`, `depto`, `pct_depto`.",
starter="empleados['pct_depto'] = \nresultado = empleados[['nombre', 'depto', 'pct_depto']]",
solution="empleados['pct_depto'] = empleados['salario'] / empleados.groupby('depto')['salario'].transform('sum') * 100\nresultado = empleados[['nombre', 'depto', 'pct_depto']]",
hint="salario / groupby('depto')['salario'].transform('sum') * 100",
sql="SELECT nombre, depto,\n  100.0 * salario / SUM(salario) OVER (PARTITION BY depto) AS pct_depto\nFROM empleados;"),
]},
# ---------------------------------------------------------------- 11
{
"id": "m11", "title": "Pandas + Bases de datos", "icon": "🗄️", "color": "#2dd4bf",
"desc": "read_sql, to_sql, parámetros seguros y procesar por lotes. El pan diario del Data Engineer.",
"setup": SQL_SETUP,
"sql": True,
"exercises": [
dict(id="m11e1", title="Tu primera consulta", level=2,
theory="""En este módulo hay una base de datos SQLite en memoria (`conn`) con las tablas `clientes`, `productos` y `pedidos`. Con `pd.read_sql(consulta, conn)` el resultado llega directo a un DataFrame.

En un trabajo real, `conn` sería un engine de SQLAlchemy apuntando a PostgreSQL, MySQL, Snowflake...

```python
pd.read_sql("SELECT * FROM productos", conn)
```""",
task="Con `read_sql`, trae `nombre` y `ciudad` de los clientes con `edad > 40`.",
starter="resultado = pd.read_sql(\"\"\"\n    SELECT ...\n\"\"\", conn)",
solution="resultado = pd.read_sql('SELECT nombre, ciudad FROM clientes WHERE edad > 40', conn)",
hint="SELECT nombre, ciudad FROM clientes WHERE edad > 40",
sql="SELECT nombre, ciudad FROM clientes WHERE edad > 40;"),

dict(id="m11e2", title="Que la base haga el trabajo", level=3,
theory="""Regla de oro del Data Engineer: **filtra y agrega en la base de datos** y trae a pandas solo lo necesario. Mover millones de filas por la red es caro.""",
task="Con **una sola consulta SQL**: unidades totales (`SUM(cantidad)`) por `categoria`, en columnas `categoria` y `unidades`, ordenado de mayor a menor (empates: por `categoria` A→Z).",
starter="query = \"\"\"\n\n\"\"\"\nresultado = pd.read_sql(query, conn)",
solution="query = '''\nSELECT pr.categoria, SUM(p.cantidad) AS unidades\nFROM pedidos p JOIN productos pr ON p.producto_id = pr.producto_id\nGROUP BY pr.categoria\nORDER BY unidades DESC, pr.categoria\n'''\nresultado = pd.read_sql(query, conn)",
hint="JOIN productos ... GROUP BY categoria ORDER BY unidades DESC, categoria",
sql="SELECT pr.categoria, SUM(p.cantidad) AS unidades\nFROM pedidos p JOIN productos pr ON p.producto_id = pr.producto_id\nGROUP BY pr.categoria ORDER BY unidades DESC, pr.categoria;"),

dict(id="m11e3", title="Parámetros seguros", level=3,
theory="""**Nunca** metas valores con f-strings en tus consultas: es la puerta a la **inyección SQL**. Usa parámetros (`?` en SQLite, `%s` o `:nombre` en otros motores):

```python
pd.read_sql("SELECT * FROM t WHERE pais = ?", conn, params=("Chile",))
```""",
task="Usando un parámetro, trae los productos con `precio` mayor que `precio_min`.",
starter="precio_min = 100\nresultado = pd.read_sql(\"SELECT * FROM productos WHERE precio > ?\", conn, )",
solution="precio_min = 100\nresultado = pd.read_sql('SELECT * FROM productos WHERE precio > ?', conn, params=(precio_min,))",
hint="params=(precio_min,)  ← ¡la coma hace que sea una tupla!",
sql="SELECT * FROM productos WHERE precio > :precio_min;"),

dict(id="m11e4", title="Guardar en la base", level=3,
theory="""`df.to_sql("tabla", conn, index=False, if_exists="replace")` escribe un DataFrame en la base. `if_exists` puede ser `"fail"`, `"replace"` o `"append"` (cargas incrementales).""",
task="Calcula con pandas el número de clientes por país (columnas `pais` y `n_clientes`), guárdalo en la tabla `resumen_pais` y léelo de vuelta con `read_sql` en `resultado`.",
starter="resumen = \nresumen.to_sql('resumen_pais', conn, index=False, if_exists='replace')\nresultado = pd.read_sql('SELECT * FROM resumen_pais', conn)",
solution="resumen = clientes.groupby('pais', as_index=False).agg(n_clientes=('cliente_id', 'count'))\nresumen.to_sql('resumen_pais', conn, index=False, if_exists='replace')\nresultado = pd.read_sql('SELECT * FROM resumen_pais', conn)",
hint="clientes.groupby('pais', as_index=False).agg(n_clientes=('cliente_id', 'count'))",
sql="CREATE TABLE resumen_pais AS\nSELECT pais, COUNT(*) AS n_clientes FROM clientes GROUP BY pais;",
check={"ordered": False, "ignore_index": True}),

dict(id="m11e5", title="Procesar por lotes", level=4,
theory="""Con tablas gigantes no cabe todo en memoria. `chunksize` hace que `read_sql` devuelva un **iterador** de DataFrames que procesas de a uno:

```python
for chunk in pd.read_sql(q, conn, chunksize=50_000):
    procesar(chunk)
```""",
task="Lee `SELECT cantidad FROM pedidos` en lotes de **10 filas** y calcula la suma total de `cantidad` acumulando lote a lote.",
starter="total = 0\nfor chunk in pd.read_sql('SELECT cantidad FROM pedidos', conn, chunksize=10):\n    pass  # acumula aquí\nresultado = total",
solution="total = 0\nfor chunk in pd.read_sql('SELECT cantidad FROM pedidos', conn, chunksize=10):\n    total += chunk['cantidad'].sum()\nresultado = total",
hint="total += chunk['cantidad'].sum()",
sql="SELECT SUM(cantidad) FROM pedidos;"),

dict(id="m11e6", title="Traduce SQL a pandas", level=4,
theory="""En entrevistas es clásico: te dan una consulta SQL y la reescribes en pandas (o al revés). Piensa en el orden lógico: **FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY**.""",
task="""Reproduce **solo con pandas** (sin `read_sql`) esta consulta:

```sql
SELECT categoria, AVG(precio) AS precio_medio
FROM productos
WHERE stock > 0
GROUP BY categoria
HAVING COUNT(*) >= 2
ORDER BY precio_medio DESC;
```
Resultado: DataFrame con columnas `categoria` y `precio_medio`.""",
starter="df = productos[productos['stock'] > 0]\n",
solution="df = productos[productos['stock'] > 0]\ng = df.groupby('categoria').agg(precio_medio=('precio', 'mean'), n=('precio', 'size'))\nresultado = g[g['n'] >= 2].reset_index()[['categoria', 'precio_medio']].sort_values('precio_medio', ascending=False)",
hint="agg(precio_medio=('precio','mean'), n=('precio','size')) → filtra n >= 2 → reset_index → ordena",
sql="SELECT categoria, AVG(precio) AS precio_medio FROM productos\nWHERE stock > 0 GROUP BY categoria HAVING COUNT(*) >= 2\nORDER BY precio_medio DESC;",
check={"ignore_index": True}),
]},
# ---------------------------------------------------------------- 12
{
"id": "m12", "title": "Nivel Pro", "icon": "🚀", "color": "#e879f9",
"desc": "Vectorización, method chaining, memoria y funciones reutilizables.",
"exercises": [
dict(id="m12e1", title="Mata el bucle", level=3,
theory="""Los bucles `for` con `iterrows()` son **lentísimos**: en pandas casi siempre hay una versión vectorizada 100x más rápida. `np.where(cond, si, no)` es un `if` vectorizado.""",
task="""El código de abajo funciona, pero es lento. Reescríbelo **sin bucles**: una Series `precio_final` con el precio de cada producto aplicando un 10% de descuento a los que cuestan **más de 200**.""",
starter="# ❌ Versión lenta\nprecios = []\nfor _, fila in productos.iterrows():\n    if fila['precio'] > 200:\n        precios.append(fila['precio'] * 0.9)\n    else:\n        precios.append(fila['precio'])\nresultado = pd.Series(precios)\n\n# ✅ Tu versión vectorizada:\n# resultado = pd.Series(np.where(...), index=productos.index)",
solution="resultado = pd.Series(np.where(productos['precio'] > 200, productos['precio'] * 0.9, productos['precio']), index=productos.index)",
hint="np.where(productos['precio'] > 200, productos['precio'] * 0.9, productos['precio'])",
sql="SELECT CASE WHEN precio > 200 THEN precio * 0.9 ELSE precio END FROM productos;",
check={"custom": "'iterrows' not in _pq_code and 'for ' not in _pq_code and isinstance(resultado, pd.Series) and np.allclose(resultado.values, np.where(productos['precio'] > 200, productos['precio'] * 0.9, productos['precio']))",
       "custom_msg": "Tiene que dar el precio correcto y NO usar bucles for ni iterrows (borra la versión lenta)."}),

dict(id="m12e2", title="Method chaining", level=4,
theory="""Los pros escriben pipelines encadenados, legibles de arriba abajo y sin variables intermedias:

```python
(df
 .query("x > 0")
 .assign(y=lambda d: d.x * 2)
 .groupby("g", as_index=False)["y"].sum()
 .sort_values("y", ascending=False))
```""",
task="En **una cadena**: pedidos `entregado` → unir con `productos` → `importe` = `cantidad * precio` → ingresos por `categoria` (columnas `categoria` e `ingresos`) → orden descendente.",
starter="resultado = (\n    pedidos\n    .query(\"estado == 'entregado'\")\n    # ...\n)",
solution="resultado = (\n    pedidos\n    .query(\"estado == 'entregado'\")\n    .merge(productos, on='producto_id')\n    .assign(importe=lambda d: d['cantidad'] * d['precio'])\n    .groupby('categoria', as_index=False)\n    .agg(ingresos=('importe', 'sum'))\n    .sort_values('ingresos', ascending=False)\n)",
hint=".merge(...).assign(importe=lambda d: ...).groupby('categoria', as_index=False).agg(ingresos=('importe','sum')).sort_values(...)",
sql="SELECT categoria, SUM(cantidad * precio) AS ingresos\nFROM pedidos JOIN productos USING (producto_id)\nWHERE estado = 'entregado'\nGROUP BY categoria ORDER BY ingresos DESC;",
check={"ignore_index": True}),

dict(id="m12e3", title="Dieta de memoria", level=3,
theory="""Columnas de texto con pocos valores distintos (países, estados, segmentos) ocupan mucho menos como `category`. Con millones de filas es la diferencia entre que el proceso funcione o se quede sin RAM.

```python
df.memory_usage(deep=True)
```""",
task="Convierte la columna `segmento` de `clientes` a tipo `category` y guarda la Series en `resultado`.",
starter="resultado = ",
solution="resultado = clientes['segmento'].astype('category')",
hint=".astype('category')",
sql="-- En SQL: un ENUM o una tabla de dimensión con FK",
check={"custom": "isinstance(resultado, pd.Series) and isinstance(resultado.dtype, pd.CategoricalDtype) and resultado.astype(str).tolist() == clientes['segmento'].astype(str).tolist()",
       "custom_msg": "resultado debe ser la columna segmento con dtype 'category'."}),

dict(id="m12e4", title="Función reutilizable", level=4,
theory="""En un pipeline de datos real el código se organiza en **funciones** pequeñas y testeables. Luego se encadenan con `.pipe()`:

```python
def solo_activos(df):
    return df[df["activo"]]

df.pipe(solo_activos)
```""",
task="Define `top_n(df, col, n)` que devuelva las `n` filas con mayor valor en `col`. (Se probará con varias tablas.)",
starter="def top_n(df, col, n):\n    pass\n",
solution="def top_n(df, col, n):\n    return df.nlargest(n, col)",
hint="return df.nlargest(n, col)",
sql="SELECT * FROM t ORDER BY col DESC LIMIT n;",
check={"custom": "top_n(productos, 'stock', 2)['stock'].tolist() == [150, 80] and top_n(empleados, 'salario', 3)['nombre'].tolist() == ['Marta', 'Lucía', 'Valeria'] and len(top_n(clientes, 'edad', 1)) == 1",
       "custom_msg": "top_n debe devolver las n filas con mayor valor en col, ordenadas de mayor a menor."}),

dict(id="m12e5", title="Validar antes de cargar", level=4,
theory="""Un Data Engineer **no confía** en los datos de entrada. Antes de cargar se validan reglas: claves únicas, sin nulos obligatorios, rangos válidos... Si falla, se para el pipeline.

```python
assert df["id"].is_unique, "IDs duplicados"
```""",
task="Escribe `validar(df)` que devuelva una **lista de textos** con los problemas de `df`: `\"ids duplicados\"` si `id` no es único y `\"nombres nulos\"` si `nombre` tiene nulos. Si todo está bien, lista vacía.",
starter="def validar(df):\n    problemas = []\n    # ...\n    return problemas\n",
solution="def validar(df):\n    problemas = []\n    if not df['id'].is_unique:\n        problemas.append('ids duplicados')\n    if df['nombre'].isna().any():\n        problemas.append('nombres nulos')\n    return problemas",
hint="df['id'].is_unique y df['nombre'].isna().any()",
sql="SELECT id FROM t GROUP BY id HAVING COUNT(*) > 1;\nSELECT COUNT(*) FROM t WHERE nombre IS NULL;",
check={"custom": "sorted(validar(sucio)) == ['ids duplicados', 'nombres nulos'] and validar(sucio.drop_duplicates().dropna(subset=['nombre'])) == [] and validar(sucio.drop_duplicates()) == ['nombres nulos']",
       "custom_msg": "Revisa: con `sucio` deben salir los 2 problemas; con datos limpios, lista vacía []."}),
]},
# ---------------------------------------------------------------- 13
{
"id": "m13", "title": "Desafíos de entrevista", "icon": "🏆", "color": "#facc15",
"desc": "Problemas tipo entrevista técnica. Si los resuelves, estás listo.",
"exercises": [
dict(id="m13e1", title="El mejor cliente", level=4,
theory="""Clásico de entrevista: *¿quién es el cliente que más gastó?* Combina joins, filtros, agregación y `idxmax()` (devuelve la etiqueta del máximo).""",
task="**Nombre** del cliente con mayor gasto total (`cantidad * precio`) excluyendo pedidos `cancelado`. Guarda un texto.",
starter="resultado = ",
solution="df = pedidos[pedidos['estado'] != 'cancelado'].merge(productos, on='producto_id').merge(clientes, on='cliente_id')\ndf['importe'] = df['cantidad'] * df['precio']\nresultado = df.groupby('nombre')['importe'].sum().idxmax()",
hint="merge x2 → importe → groupby('nombre')['importe'].sum().idxmax()",
sql="SELECT c.nombre FROM pedidos p\nJOIN productos pr USING (producto_id) JOIN clientes c USING (cliente_id)\nWHERE p.estado <> 'cancelado'\nGROUP BY c.nombre ORDER BY SUM(p.cantidad * pr.precio) DESC LIMIT 1;"),

dict(id="m13e2", title="Clientes recurrentes", level=4,
theory="""Métrica de negocio: **tasa de recompra**. Cuenta pedidos por cliente y calcula qué porcentaje de la base de clientes compró más de una vez.""",
task="Qué % de los clientes de la tabla `clientes` hizo **2 o más** pedidos. Redondea a 2 decimales.",
starter="resultado = ",
solution="n = pedidos['cliente_id'].value_counts()\nrecurrentes = clientes['cliente_id'].isin(n[n >= 2].index).sum()\nresultado = round(recurrentes / len(clientes) * 100, 2)",
hint="value_counts por cliente → cuántos de clientes tienen >= 2 → / len(clientes) * 100",
sql="SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM clientes), 2)\nFROM (SELECT cliente_id FROM pedidos\n      WHERE cliente_id IN (SELECT cliente_id FROM clientes)\n      GROUP BY cliente_id HAVING COUNT(*) >= 2) t;"),

dict(id="m13e3", title="Estrella de cada categoría", level=4,
theory="""Top-1 por grupo tras una agregación: agrega → ordena → `drop_duplicates("grupo")` (se queda con la primera fila de cada grupo).""",
task="Para cada `categoria`, el `producto` con más `unidades` vendidas (suma de `cantidad`, todos los estados). Columnas: `categoria`, `producto`, `unidades`.",
starter="resultado = ",
solution="u = pedidos.merge(productos, on='producto_id').groupby(['categoria', 'producto'], as_index=False).agg(unidades=('cantidad', 'sum'))\nresultado = u.sort_values('unidades', ascending=False).drop_duplicates('categoria')",
hint="groupby(['categoria','producto']) → sort_values → drop_duplicates('categoria')",
sql="SELECT categoria, producto, unidades FROM (\n  SELECT categoria, producto, SUM(cantidad) AS unidades,\n    ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY SUM(cantidad) DESC) rn\n  FROM pedidos JOIN productos USING (producto_id)\n  GROUP BY categoria, producto) t\nWHERE rn = 1;",
check={"ordered": False, "ignore_index": True}),

dict(id="m13e4", title="Informe mensual", level=4,
theory="""Informe que te pedirán en tu primera semana: ingresos por mes y crecimiento contra el mes anterior. `dt.to_period("M")` agrupa por mes y `astype(str)` lo deja como `"2024-01"`.""",
task="Pedidos no cancelados: DataFrame con `mes` (texto `\"2024-01\"`), `ingresos` (suma de `cantidad * precio`) y `crecimiento_pct` (variación % vs mes anterior, redondeada a 1 decimal), ordenado por mes.",
starter="resultado = ",
solution="df = pedidos[pedidos['estado'] != 'cancelado'].merge(productos, on='producto_id')\ndf['mes'] = df['fecha'].dt.to_period('M').astype(str)\ndf['importe'] = df['cantidad'] * df['precio']\nresultado = df.groupby('mes', as_index=False).agg(ingresos=('importe', 'sum')).sort_values('mes')\nresultado['crecimiento_pct'] = (resultado['ingresos'].pct_change() * 100).round(1)",
hint="to_period('M').astype(str) → groupby mes → pct_change() * 100 → round(1)",
sql="SELECT mes, ingresos,\n  ROUND(100.0 * (ingresos - LAG(ingresos) OVER (ORDER BY mes)) / LAG(ingresos) OVER (ORDER BY mes), 1)\nFROM (SELECT TO_CHAR(fecha, 'YYYY-MM') AS mes, SUM(cantidad * precio) AS ingresos\n      FROM pedidos JOIN productos USING (producto_id)\n      WHERE estado <> 'cancelado' GROUP BY mes) t;",
check={"ignore_index": True}),

dict(id="m13e5", title="Detector de anomalías", level=4,
theory="""Una regla simple y muy usada para detectar valores raros: todo lo que esté más de **2 desviaciones estándar** por encima de la media.""",
task="Filas de `ventas_diarias` cuyas `ventas` superan `media + 2 * desviación estándar`.",
starter="media = ventas_diarias['ventas'].mean()\nstd = ventas_diarias['ventas'].std()\nresultado = ",
solution="media = ventas_diarias['ventas'].mean()\nstd = ventas_diarias['ventas'].std()\nresultado = ventas_diarias[ventas_diarias['ventas'] > media + 2 * std]",
hint="ventas_diarias[ventas_diarias['ventas'] > media + 2 * std]",
sql="SELECT * FROM ventas_diarias\nWHERE ventas > (SELECT AVG(ventas) + 2 * STDDEV(ventas) FROM ventas_diarias);"),

dict(id="m13e6", title="Boss final: ETL completo", level=4,
theory="""Todo junto, como en un trabajo real: **Extract** (leer de la base) → **Transform** (limpiar, unir, agregar) → **Load** (escribir el resultado). En este ejercicio tienes `conn` disponible.""",
task="""1. **Extract**: lee `pedidos` y `productos` desde `conn` con `read_sql`.
2. **Transform**: pedidos `entregado`, `importe` = `cantidad * precio`, ingresos por `producto` (columnas `producto`, `ingresos`), ordenado de mayor a menor.
3. **Load**: guárdalo en la tabla `top_productos` y léelo de vuelta en `resultado`.""",
starter="# 1. Extract\n\n# 2. Transform\n\n# 3. Load\n\nresultado = pd.read_sql('SELECT * FROM top_productos', conn)",
solution="ped = pd.read_sql('SELECT * FROM pedidos', conn)\nprod = pd.read_sql('SELECT * FROM productos', conn)\ntop = (ped[ped['estado'] == 'entregado']\n       .merge(prod, on='producto_id')\n       .assign(importe=lambda d: d['cantidad'] * d['precio'])\n       .groupby('producto', as_index=False).agg(ingresos=('importe', 'sum'))\n       .sort_values('ingresos', ascending=False))\ntop.to_sql('top_productos', conn, index=False, if_exists='replace')\nresultado = pd.read_sql('SELECT * FROM top_productos', conn)",
hint="read_sql x2 → filtro → merge → assign → groupby/agg → sort → to_sql",
sql="CREATE TABLE top_productos AS\nSELECT producto, SUM(cantidad * precio) AS ingresos\nFROM pedidos JOIN productos USING (producto_id)\nWHERE estado = 'entregado'\nGROUP BY producto ORDER BY ingresos DESC;",
check={"ignore_index": True}),
]},
]

# el último módulo necesita la base de datos para el boss final
MODULES[-1]["setup"] = SQL_SETUP
MODULES[-1]["sql"] = True

XP_BY_LEVEL = {1: 10, 2: 20, 3: 35, 4: 50}
LEVEL_NAMES = {1: "Básico", 2: "Intermedio", 3: "Avanzado", 4: "Pro"}
