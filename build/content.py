# -*- coding: utf-8 -*-
"""Fuente única de contenido de PandasQuest.

Temario: 00 Python desde cero · 01 Pandas · 02 DataFrames · 03 NumPy · 04 Matplotlib · 05 Seaborn · 06 Introducción a Machine Learning

build.py genera a partir de aquí: js/data.js (web) y notebooks/*.ipynb (Colab).
tests/test_content.py valida que cada solución pase y cada plantilla inicial falle.

Cada ejercicio: id, sec (sección), title, level (1-4), theory, task, starter, solution, hint, sql (opcional),
check (opcional): {"ordered": bool, "ignore_index": bool} o {"custom": "expr", "custom_msg": "...", "plot": bool}
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

DF_SETUP = '''
import sqlite3
conn = sqlite3.connect(":memory:")
clientes.to_sql("clientes", conn, index=False)
productos.to_sql("productos", conn, index=False)
pedidos.to_sql("pedidos", conn, index=False)

trimestral = pd.DataFrame({
    "tienda": ["Centro", "Norte", "Sur"],
    "Q1": [100, 80, 60],
    "Q2": [120, 95, 70],
    "Q3": [130, 90, 85],
})
'''

NUMPY_SETUP = '''
temperaturas = np.array([21.5, 23.0, 19.8, 25.1, 27.3, 22.4, 18.9])   # una semana, en °C
notas = np.array([[7, 8, 6],
                  [9, 5, 8],
                  [6, 7, 9],
                  [8, 9, 10],
                  [5, 6, 7]])                                          # 5 alumnos x 3 exámenes
precios = productos["precio"].to_numpy()
'''

PLT_SETUP = '''
import matplotlib.pyplot as plt

meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
ingresos = [12.5, 14.1, 13.8, 16.2, 18.9, 21.3]   # miles
gastos = [10.2, 11.0, 11.5, 12.1, 13.0, 13.4]     # miles
'''

SNS_SETUP = '''
import matplotlib.pyplot as plt
import seaborn as sns

_rng = np.random.default_rng(7)
_n = 120
propinas = pd.DataFrame({
    "cuenta": np.round(_rng.gamma(4, 5, _n) + 5, 2),
    "dia": _rng.choice(["Jue", "Vie", "Sáb", "Dom"], _n, p=[0.2, 0.2, 0.35, 0.25]),
    "momento": _rng.choice(["Almuerzo", "Cena"], _n, p=[0.35, 0.65]),
    "fumador": _rng.choice(["Sí", "No"], _n, p=[0.4, 0.6]),
    "personas": _rng.integers(1, 7, _n),
})
propinas["propina"] = np.round(propinas["cuenta"] * _rng.uniform(0.08, 0.22, _n) + 0.5, 2)
del _rng, _n
'''

ML_SETUP = '''
_rng = np.random.default_rng(42)
_n = 200
_m2 = _rng.integers(35, 220, _n)
_hab = np.clip(_m2 // 35 + _rng.integers(-1, 2, _n), 1, 6)
_ant = _rng.integers(0, 60, _n)
_barrio = _rng.choice(["Centro", "Norte", "Sur"], _n)
_extra = np.select([_barrio == "Centro", _barrio == "Norte"], [40000, 15000], 0)
casas = pd.DataFrame({
    "m2": _m2, "habitaciones": _hab, "antiguedad": _ant, "barrio": _barrio,
    "precio": np.round(30000 + _m2 * 1800 + _hab * 5000 - _ant * 900 + _extra
                       + _rng.normal(0, 15000, _n), -2),
})
_n = 300
churn = pd.DataFrame({
    "meses_cliente": _rng.integers(1, 72, _n),
    "cargo_mensual": np.round(_rng.uniform(15, 120, _n), 2),
    "reclamos": _rng.poisson(1.2, _n),
    "contrato": _rng.choice(["Mensual", "Anual"], _n, p=[0.6, 0.4]),
})
_logit = (-1.0 - 0.05 * churn["meses_cliente"] + 0.03 * churn["cargo_mensual"]
          + 0.6 * churn["reclamos"] + np.where(churn["contrato"] == "Mensual", 1.2, -0.8))
churn["abandona"] = (_rng.uniform(0, 1, _n) < 1 / (1 + np.exp(-_logit))).astype(int)
del _rng, _n, _m2, _hab, _ant, _barrio, _extra, _logit
'''

from mod_python import EXERCISES as EX_PY  # noqa: E402
from mod_pandas import EXERCISES as EX_PANDAS  # noqa: E402
from mod_dataframes import EXERCISES as EX_DF  # noqa: E402
from mod_numpy import EXERCISES as EX_NUMPY  # noqa: E402
from mod_matplotlib import EXERCISES as EX_PLT  # noqa: E402
from mod_seaborn import EXERCISES as EX_SNS  # noqa: E402
from mod_ml import EXERCISES as EX_ML  # noqa: E402

MODULES = [
    {"id": "m00", "title": "Python desde cero", "icon": "🐍", "color": "#e0700b",
     "desc": "Variables, texto, listas, diccionarios, decisiones, bucles, funciones, errores y clases: la base para leer y escribir cualquier código.",
     "tables": [], "exercises": EX_PY},
    {"id": "m01", "title": "Pandas", "icon": "🐼", "color": "#0098cc",
     "desc": "Qué es pandas, Series, operaciones vectorizadas y tu primer contacto con tablas reales.",
     "tables": TABLES, "exercises": EX_PANDAS},
    {"id": "m02", "title": "DataFrames", "icon": "📋", "color": "#d8231b",
     "desc": "Seleccionar, filtrar, limpiar, agrupar, unir y reestructurar tablas. Y conectarlas con bases de datos SQL.",
     "setup": DF_SETUP, "packages": ["sqlite3"], "tables": TABLES + ["trimestral"], "exercises": EX_DF},
    {"id": "m03", "title": "NumPy", "icon": "🔢", "color": "#1d5bb0",
     "desc": "Arrays, indexado, cálculo vectorizado y broadcasting: el motor numérico debajo de pandas.",
     "setup": NUMPY_SETUP, "tables": ["temperaturas", "notas", "precios"], "exercises": EX_NUMPY},
    {"id": "m04", "title": "Matplotlib", "icon": "📈", "color": "#00825a",
     "desc": "Líneas, barras, histogramas, dispersión y subplots. Convierte datos en gráficos claros.",
     "setup": PLT_SETUP, "packages": ["matplotlib"], "tables": ["meses", "ingresos", "gastos", "productos", "ventas_diarias"],
     "exercises": EX_PLT},
    {"id": "m05", "title": "Seaborn", "icon": "🎨", "color": "#7a2d8f",
     "desc": "Gráficos estadísticos bonitos en una línea: distribuciones, categorías, relaciones y correlaciones.",
     "setup": SNS_SETUP, "packages": ["matplotlib", "micropip"], "micropip": ["seaborn"],
     "tables": ["propinas", "ventas_diarias"], "exercises": EX_SNS},
    {"id": "m06", "title": "Introducción a Machine Learning", "icon": "🤖", "color": "#f0bf00",
     "desc": "Tu primer modelo con scikit-learn: preparar datos, entrenar, predecir y evaluar. Regresión y clasificación.",
     "setup": ML_SETUP, "packages": ["scikit-learn"], "tables": ["casas", "churn"], "exercises": EX_ML},
]

XP_BY_LEVEL = {1: 10, 2: 20, 3: 35, 4: 50}
LEVEL_NAMES = {1: "Básico", 2: "Intermedio", 3: "Avanzado", 4: "Pro"}
