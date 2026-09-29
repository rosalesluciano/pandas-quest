# -*- coding: utf-8 -*-
"""Módulo 00 · Python desde cero: la base para leer y escribir cualquier código."""


def chk(expr, msg):
    return {"custom": expr, "custom_msg": msg}


EXERCISES = [
# =========================================================== Primeros pasos
dict(id="py01", sec="Primeros pasos", title="Hola, Python", level=1,
theory="""**Python** es el lenguaje número uno en ciencia de datos e inteligencia artificial. pandas, NumPy, scikit-learn, PyTorch… todo se escribe en Python. Antes de analizar datos, necesitas leer y escribir Python con soltura.

Una **variable** es un nombre que guarda un valor. Se crea con `=` (se lee "guarda en"):

```python
nombre = "Ana"        # texto (string): entre comillas
edad = 28             # número entero (int)
altura = 1.65         # número decimal (float)
print(nombre, edad)   # print muestra valores en pantalla -> Ana 28
```

Reglas para nombrar variables:
- Letras minúsculas, números y guion bajo: `precio_final`, `total_2024`.
- No pueden empezar con un número ni tener espacios.
- Python distingue mayúsculas: `edad` y `Edad` son variables distintas.

> 💡 En este curso, cada ejercicio se corrige mirando la variable `resultado`. Guarda siempre ahí tu respuesta.""",
task="Crea la variable `ciudad` con el texto `'Córdoba'` y la variable `habitantes` con el número `1_500_000` (el guion bajo solo facilita la lectura). Después guarda en `resultado` la variable `habitantes`.",
starter="# Escribe tu código aquí 👇\nciudad = \nhabitantes = \nresultado = ",
solution="ciudad = 'Córdoba'\nhabitantes = 1_500_000\nresultado = habitantes",
hint="habitantes = 1_500_000  y luego  resultado = habitantes",
check=chk("ciudad == 'Córdoba' and resultado == 1500000",
          "Revisa que `ciudad` sea 'Córdoba' y que `resultado` tenga los habitantes (1500000).")),

dict(id="py02", sec="Primeros pasos", title="Tipos de datos", level=1,
theory="""Cada valor en Python tiene un **tipo**. Los cuatro básicos son:

| Tipo | Qué guarda | Ejemplo |
|---|---|---|
| `int` | números enteros | `42`, `-7` |
| `float` | números decimales | `3.14`, `0.5` |
| `str` | texto | `"hola"`, `'Python'` |
| `bool` | verdadero o falso | `True`, `False` |

La función `type()` te dice el tipo de cualquier valor:

```python
type(42)        # <class 'int'>
type("42")      # <class 'str'>  ← ¡con comillas es texto!
type(4.0)       # <class 'float'>
```

Para quedarte solo con el nombre del tipo: `type(42).__name__` devuelve `'int'`.

> 💼 **En el trabajo:** la mitad de los errores al limpiar datos son de tipo: números que llegaron como texto (`"1200"`) o fechas que llegaron como `str`.""",
task="Guarda en `resultado` una **lista** con los nombres de los tipos de estos cuatro valores, en este orden: `7`, `7.5`, `'7'`, `True`. Usa `type(valor).__name__`.",
starter="resultado = [type(7).__name__, ]",
solution="resultado = [type(7).__name__, type(7.5).__name__, type('7').__name__, type(True).__name__]",
hint="[type(7).__name__, type(7.5).__name__, type('7').__name__, type(True).__name__]",
check=chk("resultado == ['int', 'float', 'str', 'bool']",
          "Deben ser 4 nombres de tipo en orden: int, float, str, bool.")),

dict(id="py03", sec="Primeros pasos", title="La calculadora de Python", level=1,
theory="""Python calcula como una calculadora, con algunos operadores extra muy útiles:

| Operador | Qué hace | Ejemplo | Resultado |
|---|---|---|---|
| `+ - * /` | suma, resta, multiplicación, división | `7 / 2` | `3.5` |
| `//` | división entera (sin decimales) | `7 // 2` | `3` |
| `%` | resto de la división (módulo) | `7 % 2` | `1` |
| `**` | potencia | `2 ** 3` | `8` |

Se respetan las reglas matemáticas: primero potencias, luego `* / // %`, y al final `+ -`. Usa paréntesis para cambiar el orden.

```python
minutos = 135
horas = minutos // 60      # 2
resto = minutos % 60       # 15
```

> 💡 `%` sirve para saber si un número es par: `n % 2 == 0`.""",
task="Un video dura `500` segundos. Calcula cuántos **minutos completos** tiene y cuántos **segundos sobran**. Guarda en `resultado` una lista `[minutos, segundos]`.",
starter="duracion = 500\nminutos = \nsegundos = \nresultado = [minutos, segundos]",
solution="duracion = 500\nminutos = duracion // 60\nsegundos = duracion % 60\nresultado = [minutos, segundos]",
hint="minutos = duracion // 60   y   segundos = duracion % 60",
check=chk("resultado == [8, 20]", "500 segundos son 8 minutos y 20 segundos. Usa // y %.")),

dict(id="py04", sec="Primeros pasos", title="Convertir tipos", level=2,
theory="""Muchas veces un número llega como texto (por ejemplo, desde un formulario o un archivo). Con texto no se puede calcular: `"10" + "5"` da `"105"`, porque **pega** los textos.

Para convertir entre tipos se usan funciones con el nombre del tipo:

```python
int("42")       # 42     texto -> entero
float("3.5")    # 3.5    texto -> decimal
str(100)        # "100"  número -> texto
int(9.99)       # 9      corta los decimales (no redondea)
round(9.99, 1)  # 10.0   redondea a 1 decimal
```

> ⚠️ `int("3.5")` da error: primero pásalo a `float` y después a `int`.""",
task="Los precios llegaron como texto. Conviértelos a números decimales y guarda en `resultado` la **suma** de los dos.",
starter="precio_a = '1250.50'\nprecio_b = '749.50'\nresultado = precio_a + precio_b   # ⚠️ esto pega textos",
solution="precio_a = '1250.50'\nprecio_b = '749.50'\nresultado = float(precio_a) + float(precio_b)",
hint="float(precio_a) + float(precio_b)",
check=chk("isinstance(resultado, (int, float)) and abs(resultado - 2000.0) < 1e-9",
          "El resultado debe ser el número 2000.0. ¿Convertiste los dos textos con float()?")),

# =========================================================== Texto
dict(id="py05", sec="Texto (strings)", title="f-strings: texto con variables", level=1,
theory="""Las **f-strings** son la forma moderna de meter variables dentro de un texto. Se escribe una `f` antes de las comillas y cada variable va entre llaves `{}`:

```python
nombre = "Ana"
edad = 28
f"{nombre} tiene {edad} años"          # 'Ana tiene 28 años'
f"El año que viene tendrá {edad + 1}"  # dentro de {} puede ir cualquier cálculo
```

También sirven para dar formato a los números:

```python
precio = 1234.5678
f"${precio:.2f}"     # '$1234.57'   -> 2 decimales
f"{precio:,.0f}"     # '1,235'      -> separador de miles, sin decimales
f"{0.256:.1%}"       # '25.6%'      -> como porcentaje
```

> 💼 **En el trabajo:** los reportes, los mensajes de log y los títulos de gráficos se arman con f-strings.""",
task="Con las variables dadas, guarda en `resultado` exactamente el texto: `Luciano aprobó con 8.75 puntos` (la nota con **2 decimales**).",
starter="alumno = 'Luciano'\nnota = 8.7512\nresultado = ",
solution="alumno = 'Luciano'\nnota = 8.7512\nresultado = f'{alumno} aprobó con {nota:.2f} puntos'",
hint="f'{alumno} aprobó con {nota:.2f} puntos'",
check=chk("resultado == 'Luciano aprobó con 8.75 puntos'",
          "El texto debe ser exactamente: Luciano aprobó con 8.75 puntos")),

dict(id="py06", sec="Texto (strings)", title="Limpiar texto", level=1,
theory="""Los textos tienen **métodos**: funciones que se escriben después de un punto. Los más usados para limpiar datos:

| Método | Qué hace | Ejemplo |
|---|---|---|
| `.strip()` | quita espacios al inicio y al final | `"  hola ".strip()` → `'hola'` |
| `.lower()` / `.upper()` | minúsculas / mayúsculas | `"Hola".upper()` → `'HOLA'` |
| `.title()` | primera letra de cada palabra en mayúscula | `"buenos aires".title()` → `'Buenos Aires'` |
| `.replace(a, b)` | reemplaza `a` por `b` | `"1.200".replace(".", "")` → `'1200'` |

Los métodos se pueden **encadenar**: se aplican de izquierda a derecha.

```python
"  JUAN pérez ".strip().title()   # 'Juan Pérez'
```

> ⚠️ Los strings son **inmutables**: `.upper()` no cambia la variable original, devuelve un texto nuevo. Por eso se guarda el resultado: `nombre = nombre.upper()`.""",
task="Limpia el texto `sucio`: quítale los espacios de los extremos y déjalo con formato de título. Guarda el texto limpio en `resultado`.",
starter="sucio = '   sAN miguel de TUCUMÁN  '\nresultado = sucio",
solution="sucio = '   sAN miguel de TUCUMÁN  '\nresultado = sucio.strip().title()",
hint="sucio.strip().title()",
check=chk("resultado == 'San Miguel De Tucumán'", "Debe quedar 'San Miguel De Tucumán': usa .strip() y .title().")),

dict(id="py07", sec="Texto (strings)", title="Índices y recortes", level=2,
theory="""Un texto es una **secuencia** de caracteres, y cada uno tiene una posición (índice) que **empieza en 0**:

```
 texto =  P  y  t  h  o  n
 índice:  0  1  2  3  4  5
negativo: -6 -5 -4 -3 -2 -1
```

```python
texto = "Python"
texto[0]      # 'P'    primer carácter
texto[-1]     # 'n'    último carácter
texto[0:3]    # 'Pyt'  del 0 al 3 (el 3 NO se incluye)
texto[2:]     # 'thon' desde el 2 hasta el final
texto[:2]     # 'Py'   desde el inicio hasta el 2
len(texto)    # 6      cantidad de caracteres
```

Esta notación `[inicio:fin]` se llama **slicing** y funciona igual en listas, arrays de NumPy y (con `iloc`) en pandas. Vale la pena dominarla ahora.""",
task="El código de producto `'ARG-2024-00731'` tiene el país en los **primeros 3** caracteres y el número de serie en los **últimos 5**. Guarda en `resultado` una lista `[pais, serie]`.",
starter="codigo = 'ARG-2024-00731'\npais = \nserie = \nresultado = [pais, serie]",
solution="codigo = 'ARG-2024-00731'\npais = codigo[:3]\nserie = codigo[-5:]\nresultado = [pais, serie]",
hint="codigo[:3]  y  codigo[-5:]",
check=chk("resultado == ['ARG', '00731']", "Debe quedar ['ARG', '00731']. Recuerda: [:3] y [-5:].")),

dict(id="py08", sec="Texto (strings)", title="Separar y unir", level=2,
theory="""Dos métodos que vas a usar todo el tiempo:

- `texto.split(sep)` **corta** un texto en una lista, usando `sep` como separador.
- `sep.join(lista)` hace lo contrario: **une** una lista de textos usando `sep` entre cada uno.

```python
fila = "Ana;28;Córdoba"
partes = fila.split(";")      # ['Ana', '28', 'Córdoba']

palabras = ["ciencia", "de", "datos"]
" ".join(palabras)            # 'ciencia de datos'
"-".join(palabras)            # 'ciencia-de-datos'
```

> 💼 **En el trabajo:** así se procesan líneas de un CSV a mano, se arman rutas o se generan identificadores.""",
task="Convierte el email `'luciano.rosales@datos.com'` en el usuario `'luciano_rosales'`: toma la parte **antes** de la `@` y reemplaza el punto por guion bajo usando `split` y `join`.",
starter="email = 'luciano.rosales@datos.com'\nusuario = email.split('@')[0]    # 'luciano.rosales'\nresultado = ",
solution="email = 'luciano.rosales@datos.com'\nusuario = email.split('@')[0]\nresultado = '_'.join(usuario.split('.'))",
hint="'_'.join(usuario.split('.'))",
check=chk("resultado == 'luciano_rosales'", "Debe quedar 'luciano_rosales'.")),

# =========================================================== Listas
dict(id="py09", sec="Listas y tuplas", title="Tu primera lista", level=1,
theory="""Una **lista** guarda varios valores en orden, entre corchetes `[]` y separados por comas. Puede tener cualquier tipo de dato:

```python
ventas = [120, 95, 143, 88, 170]
ventas[0]        # 120  primer elemento
ventas[-1]       # 170  último
ventas[1:3]      # [95, 143]
len(ventas)      # 5
```

Funciones útiles con listas de números:

```python
sum(ventas)      # 616
max(ventas)      # 170
min(ventas)      # 88
sum(ventas) / len(ventas)   # 123.2 -> promedio
```

> 💡 Las listas son **mutables**: se pueden cambiar después de creadas (`ventas[0] = 130`).""",
task="Con la lista `temperaturas`, guarda en `resultado` una lista con tres valores: la **máxima**, la **mínima** y el **promedio** (suma dividida por la cantidad).",
starter="temperaturas = [18.5, 22.0, 25.5, 19.0, 30.0]\nresultado = [ , , ]",
solution="temperaturas = [18.5, 22.0, 25.5, 19.0, 30.0]\nresultado = [max(temperaturas), min(temperaturas), sum(temperaturas) / len(temperaturas)]",
hint="[max(temperaturas), min(temperaturas), sum(temperaturas) / len(temperaturas)]",
check=chk("len(resultado) == 3 and resultado[0] == 30.0 and resultado[1] == 18.5 and abs(resultado[2] - 23.0) < 1e-9",
          "Deben ser 3 valores: máxima (30.0), mínima (18.5) y promedio (23.0).")),

dict(id="py10", sec="Listas y tuplas", title="Modificar listas", level=2,
theory="""Las listas tienen métodos para agregar, quitar y ordenar:

| Método | Qué hace |
|---|---|
| `lista.append(x)` | agrega `x` al final |
| `lista.insert(i, x)` | inserta `x` en la posición `i` |
| `lista.remove(x)` | quita el primer `x` que encuentra |
| `lista.pop()` | quita y devuelve el último |
| `lista.sort()` | ordena la lista (de menor a mayor) |
| `lista.sort(reverse=True)` | ordena de mayor a menor |

```python
tareas = ["limpiar", "analizar"]
tareas.append("graficar")     # ['limpiar', 'analizar', 'graficar']
tareas.insert(0, "cargar")    # ['cargar', 'limpiar', 'analizar', 'graficar']
```

> ⚠️ `lista.sort()` modifica la lista y devuelve `None`. Si escribes `x = lista.sort()`, `x` queda vacío. Para obtener una lista nueva ordenada sin tocar la original usa `sorted(lista)`.""",
task="A la lista `notas` agrégale un `9` al final, quítale el `2` (fue un error de carga) y ordénala de **mayor a menor**. Guarda la lista final en `resultado`.",
starter="notas = [7, 2, 10, 6, 8]\n\nresultado = notas",
solution="notas = [7, 2, 10, 6, 8]\nnotas.append(9)\nnotas.remove(2)\nnotas.sort(reverse=True)\nresultado = notas",
hint="notas.append(9)  notas.remove(2)  notas.sort(reverse=True)",
check=chk("resultado == [10, 9, 8, 7, 6]", "La lista final debe ser [10, 9, 8, 7, 6].")),

dict(id="py11", sec="Listas y tuplas", title="Tuplas y desempaquetado", level=2,
theory="""Una **tupla** es como una lista pero **inmutable** (no se puede modificar). Se escribe con paréntesis:

```python
coordenadas = (-31.42, -64.18)   # latitud, longitud de Córdoba
coordenadas[0]                    # -31.42
```

Se usan para datos que van juntos y no deberían cambiar. Y permiten el **desempaquetado**: repartir los valores en varias variables de una sola vez.

```python
lat, lon = coordenadas            # lat = -31.42, lon = -64.18
nombre, edad, ciudad = ("Ana", 28, "Lima")
a, b = b, a                       # truco: intercambia dos variables
```

> 💼 **En el trabajo:** lo vas a ver en todos lados. Por ejemplo, `df.shape` devuelve una tupla `(filas, columnas)` y en ML se escribe `X_train, X_test, y_train, y_test = train_test_split(...)`.""",
task="La tupla `dimensiones` tiene `(filas, columnas)` de una tabla. Desempaquétala en las variables `filas` y `columnas`, y guarda en `resultado` la **cantidad total de celdas**.",
starter="dimensiones = (1500, 12)\n\nresultado = ",
solution="dimensiones = (1500, 12)\nfilas, columnas = dimensiones\nresultado = filas * columnas",
hint="filas, columnas = dimensiones",
check=chk("filas == 1500 and columnas == 12 and resultado == 18000",
          "Desempaqueta con `filas, columnas = dimensiones` y multiplica (resultado: 18000).")),

# =========================================================== Diccionarios
dict(id="py12", sec="Diccionarios y conjuntos", title="Diccionarios", level=1,
theory="""Un **diccionario** guarda pares **clave: valor** entre llaves `{}`. En lugar de buscar por posición, buscas por **clave**:

```python
socio = {"nombre": "Ana", "edad": 28, "plan": "Premium"}
socio["nombre"]            # 'Ana'
socio["edad"] = 29         # modifica un valor
socio["email"] = "a@m.com" # agrega una clave nueva
socio.get("telefono", "sin dato")   # 'sin dato' -> get no da error si falta la clave
list(socio.keys())         # ['nombre', 'edad', 'plan', 'email']
```

> 💼 **En el trabajo:** es la estructura más importante después de la lista. Un JSON de una API es un diccionario, cada fila de una base de datos se puede ver como uno, y `pd.DataFrame(dict)` crea tablas a partir de diccionarios.""",
task="Al diccionario `producto`: cambia el `precio` a `1100`, agrega la clave `'stock'` con valor `8`, y guarda en `resultado` el diccionario completo.",
starter="producto = {'nombre': 'Monitor', 'precio': 1000}\n\nresultado = producto",
solution="producto = {'nombre': 'Monitor', 'precio': 1000}\nproducto['precio'] = 1100\nproducto['stock'] = 8\nresultado = producto",
hint="producto['precio'] = 1100   y   producto['stock'] = 8",
check=chk("resultado == {'nombre': 'Monitor', 'precio': 1100, 'stock': 8}",
          "El diccionario debe quedar {'nombre': 'Monitor', 'precio': 1100, 'stock': 8}.")),

dict(id="py13", sec="Diccionarios y conjuntos", title="Recorrer un diccionario", level=2,
theory="""Con `.items()` recorres un diccionario obteniendo **clave y valor** a la vez:

```python
stock = {"mouse": 40, "teclado": 15, "monitor": 3}
for producto, cantidad in stock.items():
    print(f"{producto}: {cantidad}")
```

Otras formas útiles:

```python
sum(stock.values())              # 58 -> suma de todos los valores
max(stock, key=stock.get)        # 'mouse' -> la clave con el valor más alto
"monitor" in stock               # True -> ¿existe esa clave?
```

> 💡 `in` sobre un diccionario busca entre las **claves**, no entre los valores.""",
task="`ventas` tiene las ventas de cada vendedor. Guarda en `resultado` una lista con el **total vendido** y el **nombre del vendedor que más vendió**.",
starter="ventas = {'Sofía': 1200, 'Tomás': 950, 'Valeria': 1430, 'Andrés': 870}\nresultado = [ , ]",
solution="ventas = {'Sofía': 1200, 'Tomás': 950, 'Valeria': 1430, 'Andrés': 870}\nresultado = [sum(ventas.values()), max(ventas, key=ventas.get)]",
hint="[sum(ventas.values()), max(ventas, key=ventas.get)]",
check=chk("resultado == [4450, 'Valeria']", "Deben ser el total (4450) y el mejor vendedor ('Valeria').")),

dict(id="py14", sec="Diccionarios y conjuntos", title="Conjuntos: valores únicos", level=2,
theory="""Un **conjunto** (`set`) guarda valores **sin repetir** y sin orden. Es la forma más rápida de eliminar duplicados o comparar grupos:

```python
ciudades = ["Lima", "Quito", "Lima", "Bogotá", "Quito"]
set(ciudades)                    # {'Lima', 'Quito', 'Bogotá'}
len(set(ciudades))               # 3 -> cuántos valores distintos hay

a = {"python", "sql", "excel"}
b = {"python", "sql", "tableau"}
a & b    # {'python', 'sql'}        intersección: están en los dos
a | b    # los 4 sin repetir        unión
a - b    # {'excel'}                están en a pero no en b
```

> 💼 **En el trabajo:** "¿qué clientes compraron en enero pero no en febrero?" se responde con una resta de conjuntos. Es la misma idea que un LEFT JOIN con `IS NULL` en SQL.""",
task="Guarda en `resultado` una lista **ordenada alfabéticamente** con los clientes que compraron en `enero` pero **no** en `febrero`.",
starter="enero = ['Ana', 'Bruno', 'Carla', 'Diego', 'Ana']\nfebrero = ['Bruno', 'Elena', 'Diego']\nresultado = ",
solution="enero = ['Ana', 'Bruno', 'Carla', 'Diego', 'Ana']\nfebrero = ['Bruno', 'Elena', 'Diego']\nresultado = sorted(set(enero) - set(febrero))",
hint="sorted(set(enero) - set(febrero))",
check=chk("resultado == ['Ana', 'Carla']", "Deben quedar ['Ana', 'Carla'], ordenados y sin repetir.")),

# =========================================================== Decisiones
dict(id="py15", sec="Decisiones con if", title="if, elif y else", level=1,
theory="""`if` ejecuta un bloque de código **solo si** se cumple una condición. `elif` ("si no, si…") agrega más condiciones y `else` cubre todo lo demás:

```python
temperatura = 31
if temperatura > 30:
    estado = "calor"
elif temperatura > 15:
    estado = "templado"
else:
    estado = "frío"
```

Dos cosas clave de Python:
- Después de la condición van **dos puntos** `:`.
- El bloque se marca con **sangría** (4 espacios). La sangría no es decoración: define qué código está dentro del `if`.

Comparaciones: `==` (igual), `!=` (distinto), `>`, `<`, `>=`, `<=`.

> ⚠️ `=` guarda un valor; `==` compara. `if x = 5:` da error.""",
task="Clasifica la `nota`: `'Promociona'` si es 8 o más, `'Aprueba'` si es 6 o más, y `'Recupera'` en otro caso. Guarda el texto en `resultado`.",
starter="nota = 7\n\nresultado = ",
solution="nota = 7\nif nota >= 8:\n    resultado = 'Promociona'\nelif nota >= 6:\n    resultado = 'Aprueba'\nelse:\n    resultado = 'Recupera'",
hint="if nota >= 8: ... elif nota >= 6: ... else: ...",
check=chk("resultado == 'Aprueba' and 'if' in _pq_code and 'elif' in _pq_code",
          "Con nota 7 debe dar 'Aprueba'. Usa if / elif / else.")),

dict(id="py16", sec="Decisiones con if", title="Condiciones combinadas", level=2,
theory="""Para combinar condiciones se usan `and`, `or` y `not`:

| Operador | Es verdadero si… |
|---|---|
| `a and b` | se cumplen **las dos** |
| `a or b` | se cumple **al menos una** |
| `not a` | `a` es falsa |

```python
edad, socio = 25, True
if edad >= 18 and socio:
    print("Puede entrar")

dia = "sáb"
es_finde = dia in ["sáb", "dom"]    # in: ¿está en la lista?
```

> 💡 En Python puedes encadenar comparaciones como en matemática: `18 <= edad <= 65`.""",
task="Un cliente recibe descuento si gastó **más de 50000** y es `premium`, **o** si es su `primera_compra`. Guarda en `resultado` el booleano (`True`/`False`) de si recibe descuento.",
starter="gasto = 62000\npremium = False\nprimera_compra = True\nresultado = ",
solution="gasto = 62000\npremium = False\nprimera_compra = True\nresultado = (gasto > 50000 and premium) or primera_compra",
hint="(gasto > 50000 and premium) or primera_compra",
check=chk("resultado is True and 'or' in _pq_code and 'and' in _pq_code",
          "Combina las condiciones con `and` y `or`. Con estos datos el resultado es True.")),

# =========================================================== Bucles
dict(id="py17", sec="Bucles", title="for y range", level=1,
theory="""Un bucle `for` **repite** un bloque para cada elemento de una secuencia:

```python
for fruta in ["manzana", "pera", "uva"]:
    print(fruta)
```

`range()` genera secuencias de números:

```python
range(5)          # 0, 1, 2, 3, 4      (el 5 no se incluye)
range(1, 6)       # 1, 2, 3, 4, 5
range(0, 10, 2)   # 0, 2, 4, 6, 8      (de 2 en 2)
```

El patrón **acumulador** es clásico: una variable empieza en 0 y el bucle le va sumando.

```python
total = 0
for n in range(1, 4):
    total = total + n     # o total += n
# total = 6
```""",
task="Usando un bucle `for` con `range`, suma los **números pares del 2 al 100** (ambos incluidos). Guarda la suma en `resultado`.",
starter="total = 0\n# tu bucle aquí 👇\n\nresultado = total",
solution="total = 0\nfor n in range(2, 101, 2):\n    total += n\nresultado = total",
hint="for n in range(2, 101, 2):\n    total += n",
check=chk("resultado == 2550 and 'for' in _pq_code", "La suma de los pares del 2 al 100 es 2550. Usa un bucle for.")),

dict(id="py18", sec="Bucles", title="Recorrer y contar", level=2,
theory="""Combinando `for` con `if` puedes **filtrar** y **contar** mientras recorres una lista:

```python
edades = [15, 32, 17, 45, 22]
mayores = []
for e in edades:
    if e >= 18:
        mayores.append(e)
# mayores = [32, 45, 22]
```

Dos palabras clave para controlar el bucle:
- `break`: sale del bucle inmediatamente.
- `continue`: salta a la siguiente vuelta.

> 💼 **En el trabajo:** en pandas casi nunca harás esto con bucles (hay formas vectorizadas mucho más rápidas), pero entender el bucle es lo que te permite entender qué hace pandas por dentro.""",
task="Recorre `pagos` y guarda en `resultado` una lista con los montos **mayores a 10000**, en el mismo orden.",
starter="pagos = [8000, 12000, 15000, 9500, 10000, 11000]\naltos = []\n# tu bucle aquí 👇\n\nresultado = altos",
solution="pagos = [8000, 12000, 15000, 9500, 10000, 11000]\naltos = []\nfor p in pagos:\n    if p > 10000:\n        altos.append(p)\nresultado = altos",
hint="for p in pagos:\n    if p > 10000:\n        altos.append(p)",
check=chk("resultado == [12000, 15000, 11000]", "Deben quedar [12000, 15000, 11000] (10000 no es mayor a 10000).")),

dict(id="py19", sec="Bucles", title="while: repetir hasta que…", level=2,
theory="""`while` repite un bloque **mientras** una condición sea verdadera. Se usa cuando no sabes de antemano cuántas vueltas vas a dar:

```python
saldo = 100
meses = 0
while saldo < 200:
    saldo = saldo * 1.10     # crece un 10% por mes
    meses += 1
# meses = 8
```

> ⚠️ Si la condición nunca se vuelve falsa, el bucle no termina nunca (**bucle infinito**). Asegúrate de que algo dentro del bucle cambie la condición.""",
task="Un ahorro de `50000` crece un **5% por mes** (multiplica por `1.05`). Con un `while`, calcula cuántos **meses** hacen falta para llegar a **100000 o más**. Guarda los meses en `resultado`.",
starter="ahorro = 50000\nmeses = 0\n# tu while aquí 👇\n\nresultado = meses",
solution="ahorro = 50000\nmeses = 0\nwhile ahorro < 100000:\n    ahorro *= 1.05\n    meses += 1\nresultado = meses",
hint="while ahorro < 100000:\n    ahorro *= 1.05\n    meses += 1",
check=chk("resultado == 15 and 'while' in _pq_code", "Con un 5% mensual hacen falta 15 meses. Usa while.")),

dict(id="py20", sec="Bucles", title="enumerate y zip", level=2,
theory="""Dos funciones que hacen los bucles mucho más limpios:

`enumerate` te da la **posición** y el **valor** a la vez:

```python
for i, nombre in enumerate(["Ana", "Luis"], start=1):
    print(i, nombre)     # 1 Ana / 2 Luis
```

`zip` recorre **varias listas en paralelo**, elemento por elemento:

```python
productos = ["mouse", "teclado"]
precios = [25, 45]
for prod, precio in zip(productos, precios):
    print(f"{prod}: ${precio}")

dict(zip(productos, precios))   # {'mouse': 25, 'teclado': 45}
```

> 💡 Viste `enumerate(zip(...))` en la Clase 4: es combinar las dos ideas.""",
task="Usa `zip` para calcular el **ingreso** de cada producto (`precio * cantidad`) y guarda en `resultado` un **diccionario** `{producto: ingreso}`.",
starter="productos = ['Laptop', 'Mouse', 'Monitor']\nprecios = [1200, 25, 300]\ncantidades = [3, 40, 5]\nresultado = {}",
solution="productos = ['Laptop', 'Mouse', 'Monitor']\nprecios = [1200, 25, 300]\ncantidades = [3, 40, 5]\nresultado = {}\nfor prod, precio, cant in zip(productos, precios, cantidades):\n    resultado[prod] = precio * cant",
hint="for prod, precio, cant in zip(productos, precios, cantidades):\n    resultado[prod] = precio * cant",
check=chk("resultado == {'Laptop': 3600, 'Mouse': 1000, 'Monitor': 1500}",
          "Debe quedar {'Laptop': 3600, 'Mouse': 1000, 'Monitor': 1500}.")),

dict(id="py21", sec="Bucles", title="List comprehensions", level=3,
theory="""Una **list comprehension** crea una lista nueva en **una sola línea**. Es uno de los rasgos más característicos de Python, y lo vas a leer en cualquier código profesional:

```python
# forma larga
cuadrados = []
for n in range(5):
    cuadrados.append(n ** 2)

# list comprehension: lo mismo en una línea
cuadrados = [n ** 2 for n in range(5)]        # [0, 1, 4, 9, 16]

# con filtro: solo los pares
pares = [n for n in range(10) if n % 2 == 0]  # [0, 2, 4, 6, 8]
```

Se lee así: "**dame** `expresión` **para cada** `elemento` **en** `secuencia` **si** `condición`".

También existen para diccionarios: `{k: v for k, v in pares}`.""",
task="Con una **list comprehension**, crea una lista con los precios **con 21% de IVA** (redondeados a 2 decimales con `round(x, 2)`) pero **solo** de los precios mayores a 50. Guárdala en `resultado`.",
starter="precios = [100, 25.5, 80, 45, 300]\nresultado = ",
solution="precios = [100, 25.5, 80, 45, 300]\nresultado = [round(p * 1.21, 2) for p in precios if p > 50]",
hint="[round(p * 1.21, 2) for p in precios if p > 50]",
check=chk("resultado == [121.0, 96.8, 363.0] and ' for ' in _pq_code and '[' in _pq_code",
          "Deben quedar [121.0, 96.8, 363.0], hecho con una list comprehension.")),

# =========================================================== Funciones
dict(id="py22", sec="Funciones", title="Tu primera función", level=1,
theory="""Una **función** es un bloque de código con nombre que puedes reutilizar. Se define con `def`, recibe **parámetros** y devuelve un valor con `return`:

```python
def area_rectangulo(base, altura):
    return base * altura

area_rectangulo(3, 4)    # 12
area_rectangulo(10, 2)   # 20
```

Buenas prácticas:
- Nombres con verbo o descriptivos: `calcular_total`, `limpiar_texto`.
- Una función hace **una sola cosa**.
- Un comentario entre triples comillas justo debajo del `def` (*docstring*) explica qué hace.

> ⚠️ `print` muestra un valor, pero **no lo devuelve**. Si tu función usa `print` en vez de `return`, el resultado no se puede guardar ni reutilizar.""",
task="Define la función `precio_final(precio, descuento)` que devuelva el precio aplicando el descuento (el descuento viene en porcentaje: `20` significa 20%). Después guarda en `resultado` el valor de `precio_final(15000, 20)`.",
starter="def precio_final(precio, descuento):\n    # tu código aquí 👇\n    pass\n\nresultado = precio_final(15000, 20)",
solution="def precio_final(precio, descuento):\n    return precio * (1 - descuento / 100)\n\nresultado = precio_final(15000, 20)",
hint="return precio * (1 - descuento / 100)",
check=chk("abs(resultado - 12000) < 1e-9 and abs(precio_final(1000, 50) - 500) < 1e-9 and abs(precio_final(200, 0) - 200) < 1e-9",
          "precio_final(15000, 20) debe devolver 12000. ¿Usaste return?")),

dict(id="py23", sec="Funciones", title="Parámetros por defecto", level=2,
theory="""Un parámetro puede tener un **valor por defecto**: si al llamar la función no lo pasas, usa ese valor.

```python
def saludar(nombre, saludo="Hola"):
    return f"{saludo}, {nombre}!"

saludar("Ana")                    # 'Hola, Ana!'
saludar("Ana", "Buenas")          # 'Buenas, Ana!'
saludar(nombre="Ana", saludo="Hey")   # argumentos por nombre (keyword)
```

Así funcionan casi todas las funciones de pandas: `df.sort_values("col", ascending=False)` usa `ascending=False` para cambiar el valor por defecto (`True`).

> 💡 Los parámetros con valor por defecto van **siempre al final**.""",
task="Define `convertir(monto, cotizacion=1000)` que devuelva el monto en pesos dividido por la cotización, **redondeado a 2 decimales**. Guarda en `resultado` una lista con `convertir(250000)` y `convertir(250000, cotizacion=1250)`.",
starter="def convertir(monto, cotizacion):\n    pass\n\nresultado = [convertir(250000), convertir(250000, cotizacion=1250)]",
solution="def convertir(monto, cotizacion=1000):\n    return round(monto / cotizacion, 2)\n\nresultado = [convertir(250000), convertir(250000, cotizacion=1250)]",
hint="def convertir(monto, cotizacion=1000):\n    return round(monto / cotizacion, 2)",
check=chk("resultado == [250.0, 200.0] and convertir(1000) == 1.0",
          "Debe dar [250.0, 200.0]. ¿Pusiste cotizacion=1000 como valor por defecto?")),

dict(id="py24", sec="Funciones", title="lambda y ordenar con key", level=3,
theory="""Una **lambda** es una función pequeña y sin nombre, escrita en una línea. Se usa para pasarle una función a otra función:

```python
doble = lambda x: x * 2        # igual que def doble(x): return x * 2
doble(5)                       # 10
```

Su uso más común es el parámetro `key` de `sorted`, `max` y `min`, que indica **por qué** ordenar:

```python
alumnos = [("Ana", 8), ("Luis", 9), ("Eva", 7)]
sorted(alumnos, key=lambda a: a[1])                 # por nota, de menor a mayor
sorted(alumnos, key=lambda a: a[1], reverse=True)   # de mayor a menor
```

> 💼 **En el trabajo:** vas a ver lambdas en pandas todo el tiempo: `df["col"].apply(lambda x: x.strip())` o `df.sort_values(key=...)`.""",
task="Ordena la lista `productos` (tuplas de `(nombre, precio)`) por **precio de mayor a menor** usando `sorted` con una `lambda`. Guarda en `resultado` solo los **nombres** en ese orden.",
starter="productos = [('Mouse', 25), ('Laptop', 1200), ('Monitor', 300), ('Teclado', 45)]\nordenados = \nresultado = [p[0] for p in ordenados]",
solution="productos = [('Mouse', 25), ('Laptop', 1200), ('Monitor', 300), ('Teclado', 45)]\nordenados = sorted(productos, key=lambda p: p[1], reverse=True)\nresultado = [p[0] for p in ordenados]",
hint="sorted(productos, key=lambda p: p[1], reverse=True)",
check=chk("resultado == ['Laptop', 'Monitor', 'Teclado', 'Mouse'] and 'lambda' in _pq_code",
          "El orden debe ser Laptop, Monitor, Teclado, Mouse. Usa sorted con key=lambda.")),

# =========================================================== Código profesional
dict(id="py25", sec="Código profesional", title="Manejar errores con try", level=2,
theory="""Cuando algo puede fallar (un dato mal cargado, un archivo que no existe), `try / except` evita que el programa se detenga:

```python
def a_numero(texto):
    try:
        return float(texto)
    except ValueError:        # solo atrapa ese tipo de error
        return None

a_numero("12.5")    # 12.5
a_numero("n/d")     # None, sin romper el programa
```

Errores que vas a ver seguido:

| Error | Cuándo aparece |
|---|---|
| `ValueError` | un valor con formato inválido (`int("abc")`) |
| `KeyError` | una clave o columna que no existe |
| `TypeError` | operar tipos incompatibles (`"5" + 3`) |
| `ZeroDivisionError` | dividir por cero |

> ⚠️ Evita `except:` a secas: atrapa **todos** los errores y esconde problemas reales. Indica siempre qué error esperas.""",
task="Recorre `edades_texto`, convierte cada valor con `int()`, y **saltea** los que no se pueden convertir (atrapa el `ValueError`). Guarda en `resultado` la lista de edades válidas.",
starter="edades_texto = ['34', '28', 'n/d', '45', '', '19']\nresultado = []\nfor e in edades_texto:\n    resultado.append(int(e))   # ⚠️ se rompe con 'n/d'",
solution="edades_texto = ['34', '28', 'n/d', '45', '', '19']\nresultado = []\nfor e in edades_texto:\n    try:\n        resultado.append(int(e))\n    except ValueError:\n        pass",
hint="try:\n    resultado.append(int(e))\nexcept ValueError:\n    pass",
check=chk("resultado == [34, 28, 45, 19] and 'except' in _pq_code",
          "Deben quedar [34, 28, 45, 19]. Usa try / except ValueError.")),

dict(id="py26", sec="Código profesional", title="Importar módulos", level=1,
theory="""Python trae una **biblioteca estándar** enorme, y además hay miles de librerías externas (pandas, NumPy…). Para usarlas se **importan**:

```python
import math                       # importa el módulo completo
math.sqrt(16)                     # 4.0

from statistics import median     # importa solo una función
median([3, 1, 2])                 # 2

import pandas as pd               # importa con un alias (apodo)
```

Módulos estándar muy útiles: `math` (matemática), `statistics` (estadística básica), `random` (azar), `datetime` (fechas), `os` y `pathlib` (archivos), `json` (datos de APIs).

> 💼 **En el trabajo:** los alias son convenciones universales. Siempre `import pandas as pd`, `import numpy as np`, `import matplotlib.pyplot as plt` y `import seaborn as sns`. Si usas otro nombre, tu código va a confundir a todos.""",
task="Importa el módulo `statistics` y guarda en `resultado` una lista con la **media** (`mean`), la **mediana** (`median`) y la **moda** (`mode`) de `sueldos`.",
starter="sueldos = [30000, 35000, 40000, 45000, 45000, 55000, 500000]\n\nresultado = [ , , ]",
solution="import statistics\nsueldos = [30000, 35000, 40000, 45000, 45000, 55000, 500000]\nresultado = [statistics.mean(sueldos), statistics.median(sueldos), statistics.mode(sueldos)]",
hint="import statistics  ->  statistics.mean(sueldos), statistics.median(sueldos), statistics.mode(sueldos)",
check=chk("len(resultado) == 3 and abs(resultado[0] - 750000 / 7) < 1e-6 and resultado[1] == 45000 and resultado[2] == 45000",
          "Deben ser media (~107142.86), mediana (45000) y moda (45000).")),

dict(id="py27", sec="Código profesional", title="Clases y objetos", level=3,
theory="""Una **clase** es un molde para crear **objetos** que juntan datos (**atributos**) y comportamiento (**métodos**). Todo en Python es un objeto: un DataFrame es un objeto de la clase `DataFrame`, y `df.head()` es uno de sus métodos.

```python
class Socio:
    def __init__(self, nombre, cuota):   # se ejecuta al crear el objeto
        self.nombre = nombre             # self = el propio objeto
        self.cuota = cuota
        self.pagos = []

    def pagar(self, monto):              # un método
        self.pagos.append(monto)

    def al_dia(self):
        return sum(self.pagos) >= self.cuota

ana = Socio("Ana", 12000)   # crear un objeto (instancia)
ana.pagar(12000)
ana.al_dia()                # True
```

> 💼 **En el trabajo:** no hace falta que escribas muchas clases para analizar datos, pero **necesitas leerlas**: scikit-learn funciona así (`modelo = LinearRegression()` y después `modelo.fit(...)`).""",
task="Completa la clase `Cuenta`: el método `depositar(monto)` suma el monto al `saldo`, y `retirar(monto)` lo resta **solo si hay saldo suficiente** (si no, no hace nada). Crea una cuenta con saldo `1000`, deposita `500`, intenta retirar `2000` y después retira `300`. Guarda el saldo final en `resultado`.",
starter="class Cuenta:\n    def __init__(self, saldo):\n        self.saldo = saldo\n\n    def depositar(self, monto):\n        pass\n\n    def retirar(self, monto):\n        pass\n\ncuenta = Cuenta(1000)\ncuenta.depositar(500)\ncuenta.retirar(2000)\ncuenta.retirar(300)\nresultado = cuenta.saldo",
solution="class Cuenta:\n    def __init__(self, saldo):\n        self.saldo = saldo\n\n    def depositar(self, monto):\n        self.saldo += monto\n\n    def retirar(self, monto):\n        if monto <= self.saldo:\n            self.saldo -= monto\n\ncuenta = Cuenta(1000)\ncuenta.depositar(500)\ncuenta.retirar(2000)\ncuenta.retirar(300)\nresultado = cuenta.saldo",
hint="def retirar(self, monto):\n    if monto <= self.saldo:\n        self.saldo -= monto",
check=chk("resultado == 1200 and Cuenta(50).saldo == 50",
          "El saldo final debe ser 1200: 1000 + 500, el retiro de 2000 no se hace, y se retiran 300.")),
]
