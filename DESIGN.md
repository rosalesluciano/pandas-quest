---
name: PandasQuest
description: Curso de ciencia de datos dibujado como una red de subte, con placas de señalética y una línea de color por módulo.
colors:
  line-00-naranja: "#e0700b"
  line-01-celeste: "#0098cc"
  line-02-rojo: "#d8231b"
  line-03-azul: "#1d5bb0"
  line-04-verde: "#00825a"
  line-05-violeta: "#7a2d8f"
  line-06-amarillo: "#f0bf00"
  line-ink-light: "#ffffff"
  line-ink-dark: "#1a1400"
  ground: "#f0efeb"
  panel: "#fbfaf8"
  panel-2: "#e6e5e0"
  ink: "#0e1a2b"
  ink-2: "#334155"
  ink-3: "#5a6576"
  rule: "#d8d7d1"
  rule-strong: "#b5b4ac"
  plaque: "#0e1a2b"
  plaque-2: "#16263c"
  plaque-ink: "#ffffff"
  plaque-mute: "#b9c4d3"
  map-bg: "#ffffff"
  rail: "#8a93a0"
  ok: "#0a7a4c"
  ok-soft: "#e2f1e8"
  err: "#b3261e"
  err-soft: "#fbe8e6"
  warn: "#7a5200"
  warn-soft: "#fbf0d6"
  focus: "#1d5bb0"
  code-bg: "#f8f9fb"
  code-gutter: "#eef1f4"
  dark-ground: "#0b1422"
  dark-panel: "#111d2e"
  dark-panel-2: "#172538"
  dark-ink: "#edf1f6"
  dark-ink-3: "#93a0b2"
  dark-rule: "#213146"
  dark-plaque: "#050b14"
  dark-plaque-2: "#0f1b2c"
  dark-map-bg: "#0e192a"
  dark-ok: "#52c792"
  dark-err: "#ff8d84"
  dark-warn: "#f5cc2a"
  dark-focus: "#6ea4ff"
typography:
  display:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "36px"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "30px"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.55
  body-lesson:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "16.5px"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: 800
    lineHeight: 1.3
    letterSpacing: "0.08em"
  code:
    fontFamily: "JetBrains Mono, ui-monospace, Consolas, monospace"
    fontSize: "14.5px"
    fontWeight: 400
    lineHeight: 1.65
rounded:
  xs: "4px"
  sm: "6px"
  md: "8px"
  lg: "10px"
  full: "50%"
spacing:
  xs: "8px"
  sm: "14px"
  md: "20px"
  lg: "22px"
  xl: "28px"
  gutter: "24px"
  gutter-mobile: "16px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.ground}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "0 18px"
    height: "42px"
  button-primary-hover:
    backgroundColor: "{colors.ink-2}"
  button-line:
    backgroundColor: "{colors.line-00-naranja}"
    textColor: "{colors.line-ink-light}"
    rounded: "{rounded.sm}"
    padding: "0 18px"
    height: "42px"
  button-secondary:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "0 18px"
    height: "42px"
  button-small:
    rounded: "{rounded.sm}"
    padding: "0 12px"
    height: "34px"
  badge-line:
    backgroundColor: "{colors.line-00-naranja}"
    textColor: "{colors.line-ink-light}"
    rounded: "{rounded.full}"
    size: "30px"
  badge-line-lg:
    rounded: "{rounded.full}"
    size: "64px"
  plaque:
    backgroundColor: "{colors.plaque}"
    textColor: "{colors.plaque-ink}"
    rounded: "{rounded.lg}"
    padding: "22px"
  map-card:
    backgroundColor: "{colors.map-bg}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "18px 18px 8px"
  panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "20px 22px"
  verdict-ok:
    backgroundColor: "{colors.ok-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "14px 16px"
  verdict-bad:
    backgroundColor: "{colors.err-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "14px 16px"
  verdict-nudge:
    backgroundColor: "{colors.warn-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "14px 16px"
  level-tag:
    backgroundColor: "{colors.panel-2}"
    textColor: "{colors.ink-2}"
    rounded: "{rounded.xs}"
    padding: "3px 8px"
  mission:
    backgroundColor: "{colors.plaque}"
    textColor: "{colors.plaque-ink}"
    rounded: "{rounded.md}"
    padding: "18px 20px"
---

# Design System: PandasQuest

## Overview

**Creative North Star: "Red de Subte"**

PandasQuest se ve y se recorre como una red de transporte. Cada módulo del curso es una línea con un color fijo y una insignia circular con su número; cada ejercicio es una estación; el alumno es un tren que avanza. La orientación (dónde estoy, qué sigue, cuánto falta) se resuelve con el lenguaje de la señalética de estación: placas esmaltadas azul noche con tinta blanca, trazos gruesos de mapa, estaciones como círculos con anillo, y una sola sans de cartelería en todas partes.

La densidad es de tablero de trabajo, no de landing: el mapa ocupa el primer viewport a todo ancho, las métricas son instrumentos tabulares y cada pantalla tiene una sola acción primaria teñida con el color de la línea en curso. El suelo es hueso de baja saturación en claro y azul noche profundo en oscuro; las superficies de contenido son planas y separadas por filetes, y la sombra se reserva para las piezas de primer nivel.

La gamificación (XP, racha, meta diaria, combos, logros) vive dentro de ese mismo lenguaje: instrumentos en la barra de placa, insignias como pines de línea, el tren como marcador de posición. No hay confeti ni ilustración decorativa; el color siempre significa una línea o un estado.

**Key Characteristics:**
- Siete colores de línea fijos, uno por módulo, usados como identidad y nunca como decoración.
- Placas azul noche con tinta blanca para todo lo que orienta: barra superior, próxima estación, cartel de estación, misión, avisos.
- Mapa SVG con trazos gruesos, estaciones circulares con anillo y combinaciones grises con codos a 45°.
- Overpass como única voz tipográfica, con JetBrains Mono solo para código y datos.
- Números tabulares en todo instrumento y métrica.
- Claro y oscuro como modos de primera clase, con el mismo sistema de roles.

## Colors

Un suelo neutro y frío-cálido de señalética, tinta azul noche, y siete colores de línea saturados que cargan toda la identidad.

### Primary
- **Colores de línea** (00 naranja, 01 celeste, 02 rojo, 03 azul, 04 verde, 05 violeta, 06 amarillo; ver `line-*` en el frontmatter): cada módulo tiene el suyo, inyectado como `--c` en su contexto. Pinta la vía del mapa, la insignia, la franja de estaciones del cartel, el botón primario de "Seguir viaje", el punto del archivo en el editor y la barra de ejecución. La tinta sobre cada color se decide por luminancia (`line-ink-light` o `line-ink-dark`): el amarillo 06 lleva tinta oscura.
- **Franja de red**: los siete colores en orden, a partes iguales, forman una banda de 4px bajo la barra superior. Es el único lugar donde conviven todos.

### Secondary
- **Azul Noche de Placa** (`plaque`): fondo de las placas de orientación. En claro coincide con la tinta (`ink`); en oscuro baja a casi negro (`dark-plaque`) para seguir leyéndose como placa sobre un suelo ya oscuro.
- **Azul Noche Segundo** (`plaque-2`): celdas y subdivisiones dentro de una placa (los totales de la placa "Próxima estación", la misión en oscuro).

### Tertiary (estados)
- **Verde Resuelto** (`ok`, `ok-soft`): veredicto correcto, XP ganado, estado "Resuelta".
- **Rojo Error** (`err`, `err-soft`): veredicto incorrecto, línea de error en el editor, nivel 4 de dificultad.
- **Ámbar Aviso** (`warn`, `warn-soft`): veredicto de "casi" (nudge), nivel 3 de dificultad, callouts de advertencia.
- **Azul Foco** (`focus`): anillo de foco de 3px en todo elemento interactivo; coincide con la línea 03 en claro.

### Neutral
- **Hueso de Andén** (`ground`): suelo de la página. Hueso de baja saturación, sin llegar al crema.
- **Papel de Panel** (`panel`) y **Panel Hundido** (`panel-2`): superficie de tarjetas y, un paso abajo, cabezales de editor, encabezados de tabla, chips de nivel y código en línea.
- **Blanco de Mapa** (`map-bg`): fondo del mapa y relleno de estación pendiente; más blanco que el panel para que las vías destaquen.
- **Tinta, Tinta 2, Tinta 3** (`ink`, `ink-2`, `ink-3`): texto principal, texto de lectura y texto secundario o metadatos.
- **Filete y Filete Fuerte** (`rule`, `rule-strong`): bordes de tarjeta y separadores; el fuerte para bordes de botón y callouts.
- **Gris de Combinación** (`rail`): los tramos que unen el final de una línea con el inicio de la siguiente en el mapa.

### Named Rules
**The Un Color, Una Línea Rule.** Un color de línea identifica a su módulo en el mapa, la insignia, el cartel, el botón primario y el editor. No se usa un color de línea para decorar algo ajeno a esa línea, y ningún color nuevo entra a la red.

**The Placa Orienta Rule.** Lo que dice dónde estás y qué sigue va sobre placa azul noche con tinta blanca. El contenido de estudio (teoría, código, salida) va sobre hueso o panel.

**The Estado Con Nombre Rule.** Un estado nunca se comunica solo con color: el veredicto lleva ícono y texto, "Resuelta" lleva check y palabra, el mapa lleva leyenda.

## Typography

**Display Font:** Overpass (con Segoe UI, system-ui, sans-serif)
**Body Font:** Overpass (con Segoe UI, system-ui, sans-serif)
**Label/Mono Font:** JetBrains Mono (con ui-monospace, Consolas, monospace)

**Character:** Overpass es una sans derivada de la señalética vial: abierta, legible a tamaños chicos y firme en 800. Toda la jerarquía sale de peso y tamaño dentro de esa única familia; la mono queda confinada al código.

### Hierarchy
- **Display** (800, 36px, 1.15, -0.02em): título de la página de línea. Baja a 26px en móvil.
- **Headline** (800, 26–30px, 1.1, -0.02em): nombre de la próxima estación en la placa (30px), título del ejercicio en el cartel (28px), título del mapa (26px). En móvil, 21–25px.
- **Title** (800, 16–20px, 1.15): encabezados de sección y de panel (19px), misión y veredicto (16px), diálogos (20px).
- **Body** (400, 16px, 1.55): interfaz general. La teoría usa 16.5px con interlineado 1.65 y un máximo de 68ch.
- **Label** (700–800, 11–13px, 0.06–0.08em, MAYÚSCULAS): nombres de instrumento ("NIVEL"), secciones dentro de una línea, grupos de logros y rótulos de la salida ("TU RESULTADO"). Siempre rotula un dato o grupo que sigue; nunca va encima de un titular.
- **Code** (400, 14.5px, 1.65, JetBrains Mono): editor. Bloques de teoría y salida a 13.5–14px; tablas de DataFrame a 13px con cifras alineadas a la derecha.

### Named Rules
**The Una Sola Voz Rule.** Overpass en todo, incluido el texto del mapa SVG. JetBrains Mono solo para código, nombre de archivo, atajos de teclado, pestañas de datasets y tablas de datos.

**The Instrumento Tabular Rule.** Toda cifra que cambia (XP, racha, meta, contadores de estación, tiempos, XP por ejercicio) usa `tabular-nums`, y en listas se alinea a la derecha.

## Layout

Contenedor centrado de 1320px con gutter de 24px (16px bajo 720px). El inicio es una grilla de dos columnas: placa "Próxima estación" de 340px, pegajosa bajo la barra, y el mapa en el resto; debajo, la misma proporción para "Cómo se viaja" y "Logros". La página de línea usa una columna de paradas y un resumen lateral pegajoso de 300px. El ejercicio pone el cartel de estación a todo ancho y debajo teoría y espacio de trabajo en proporción 1 : 1.12, con el editor y la salida pegajosos.

El ritmo se apoya en 8, 14, 20 y 28px: 8 dentro de grupos de botones, 14 entre bloques de teoría, 20 entre tarjetas, 26–28 entre bloques mayores. Las placas usan 22px de relleno.

Cortes: a 1180px el instrumento de nivel pierde nombre y barra; a 1040px todas las grillas pasan a una columna y nada queda pegajoso (el resumen de línea sube antes de las paradas); a 720px la barra superior se parte en dos filas con los instrumentos a todo ancho, y el mapa pasa a modo estrecho, donde cada fila completa es un enlace a su línea.

El mapa dibuja las siete líneas como un recorrido continuo en zigzag: una línea por fila, alternando sentido, unidas por tramos grises que bajan con codos a 45°. Las estaciones se reparten a igual distancia en la fila.

## Elevation & Depth

Sistema mayormente plano con una sola sombra de dos capas para las piezas de primer nivel: el mapa, la placa de próxima estación, el encabezado de línea y el cartel de estación. Todo lo que vive dentro de ellas o en la columna de contenido es plano y se separa por filetes (`rule`) o por el paso de `panel` a `panel-2`. Los flotantes (diálogo, avisos) llevan sombras más profundas porque están realmente por encima.

### Shadow Vocabulary
- **Tarjeta de primer nivel** (`box-shadow: 0 1px 2px rgba(14,26,43,.06), 0 8px 24px -12px rgba(14,26,43,.18)`; en oscuro `0 1px 2px rgba(0,0,0,.3), 0 10px 30px -12px rgba(0,0,0,.6)`): mapa, placas, encabezado de línea.
- **Aviso** (`box-shadow: 0 16px 40px -12px rgba(0,0,0,.45)`): toasts de logro y nivel.
- **Diálogo** (`box-shadow: 0 30px 80px -20px rgba(0,0,0,.5)`): tarjeta del diálogo modal, sobre un velo azul noche al 55%.
- **Halo de estación próxima** (`box-shadow: 0 0 0 4px` del color de línea al 25%): solo la parada "próxima" en la página de línea.
- **Anillo de insignia** (`box-shadow: 0 0 0 2px` del fondo que la rodea): despega la insignia circular de lo que tiene detrás.

### Named Rules
**The Sombra Solo Arriba Rule.** Solo las cuatro piezas de primer nivel y los flotantes proyectan sombra. Paneles, veredictos, bloques de código y paradas son planos.

## Shapes

Esquinas contenidas y círculos. Las tarjetas y placas usan 10px; botones, tabs y celdas 6px; bloques internos (código, veredicto, misión, tablas) 8px; chips y código en línea 4px. Todo lo que representa la red es circular: insignias de línea, estaciones, pines de logro, marcadores de paso y ícono de veredicto. Los extremos de vía son redondeados y los codos de combinación a 45° con unión redonda. El tren es un rectángulo de esquinas 3px con ventanilla y una flecha que apunta a la estación.

Los estados de forma también significan: estación pendiente es anillo con centro blanco, resuelta es círculo lleno del color de línea (con punto blanco al centro), próxima es anillo más grande y grueso. Un logro bloqueado es anillo discontinuo en `rule-strong`.

## Components

### Buttons
Firmes y compactos, de cartelería.
- **Shape:** esquinas suaves (6px), alto mínimo 42px, relleno horizontal 18px, peso 700 a 15px.
- **Primary:** tinta azul noche sobre texto hueso. Dentro de la placa de próxima estación y en "Ejecutar" / "Próxima estación", el primario toma el color de la línea en curso con su tinta calculada.
- **Hover / Focus:** el primario aclara a `ink-2`; el de línea sube brillo 8%; el secundario oscurece el borde a `ink-3`. Al presionar baja 1px. Foco: anillo de 3px en `focus` con separación de 2px.
- **Secondary:** fondo `panel`, borde `rule-strong`. **Ghost:** sin fondo ni borde, `panel-2` al pasar. **Small:** 34px de alto, 12px de relleno, 14px.
- **Disabled:** opacidad 45%, sin desplazamiento.

### Insignia de línea
El sello de cada módulo: círculo lleno del color de línea con el número en 800 y cifras tabulares, tamaño base 30px (44px en el cartel de estación, 64px en el encabezado de línea, 48px en móvil). Siempre con un anillo del color del fondo que la rodea.

### Placas (próxima estación, cartel de estación, misión)
- **Corner Style:** 10px (misión 8px).
- **Background:** `plaque`, texto `plaque-ink`, secundarios en `plaque-mute`, divisiones en blanco al 12–14%.
- **Shadow Strategy:** sombra de primer nivel, salvo la misión, que es plana (y en oscuro usa `plaque-2` con filete interno).
- **Internal Padding:** 22px; misión 18–20px.
- La placa de próxima estación cierra con tres totales en celdas `plaque-2` separadas por 1px.

### Cartel de estación con franja
Cabecera del ejercicio: insignia, migas de línea y sección, título, y a la derecha posición, nivel, XP y estado. Debajo, la línea entera como franja de 6px con una estación por ejercicio (resueltas llenas, actual blanca y mayor) y el tren encima. Al resolver, el tren se desliza a la siguiente estación en 0.7s con la curva de desaceleración de la casa; con movimiento reducido el cambio es instantáneo.

### Cards / Containers
- **Corner Style:** 10px.
- **Background:** `panel` (mapa en `map-bg`).
- **Border:** 1px `rule`.
- **Internal Padding:** 18–22px.

### Veredicto
Bloque de 8px de radio con fondo suave del estado (`ok-soft`, `err-soft`, `warn-soft`), ícono circular lleno de 36px con check o cruz, titular de 16px en 800, explicación en `ink-2` y fila de acciones. El XP ganado va en `ok` con cifras tabulares.

### Inputs / Fields
El único campo es el editor de código: cabezal en `panel-2` con el nombre del archivo en mono y un punto del color de línea, cuerpo en `code-bg` con canaleta `code-gutter`, altura mínima 220px. La línea con error se tiñe de `err-soft`. Sintaxis coloreada con tokens `tk-*` propios para claro y oscuro.

### Chips
- **Nivel de dificultad:** 12px 700, fondo `panel-2`, radio 4px; nivel 3 en ámbar suave, nivel 4 en rojo suave.
- **Estado "Resuelta":** check más palabra, verde sobre verde translúcido, dentro del cartel.
- **Tabs de dataset:** mono 13px, borde `rule`; la activa invierte a tinta.

### Navigation
Barra superior pegajosa sobre placa azul noche, 60px de alto, con logotipo (insignia amarilla con P), instrumentos separados por filetes verticales (nivel con barra de XP en amarillo, racha con llama naranja, meta diaria con tres marcas que se encienden en verde, combo cuando existe), estado de Python con lámpara, y botones de sonido y tema de 38px. Debajo, la franja de red. Las migas usan `ink-3` con enlaces en `ink-2` 600. En móvil los instrumentos bajan a una segunda fila a todo ancho.

### Mapa de la red
Componente firma. SVG que se redibuja al ancho del contenedor: vías de 8px (5px en estrecho) con extremos redondeados, estaciones de radio 5.5px (próxima 8.5px), combinaciones como estaciones algo mayores con anillo `ink` en los extremos de cada línea, tramos grises con codos a 45°, y rótulo de línea con insignia, nombre en 700 y contador `resueltas/total` tabular. El tren va debajo de la vía para no tapar rótulos. Leyenda al pie separada por filete.

### Parada (página de línea)
Lista vertical con la vía como barra de 8px del color de línea a la izquierda y la estación centrada en ella (20px, próxima 26px con halo). Cada fila enlaza al ejercicio con título 600, estado debajo, chip de nivel y XP alineado a la derecha. Las secciones del módulo aparecen como rótulos de 13px en mayúsculas sobre la misma vía.

## Do's and Don'ts

### Do:
- **Do** inyectar el color del módulo como `--c` (y su tinta como `--c-ink`) en el contenedor y dejar que insignia, vía, franja y botón primario lo tomen de ahí.
- **Do** poner todo lo que orienta (dónde estás, qué sigue, progreso) en placa azul noche con tinta blanca, y el contenido de estudio sobre hueso o panel.
- **Do** dibujar la red con círculos y vías gruesas: estación pendiente como anillo, resuelta llena, próxima mayor; combinaciones grises con codos a 45°.
- **Do** usar `tabular-nums` en toda cifra de progreso, XP y tiempo.
- **Do** acompañar cada estado con ícono y palabra además de color.
- **Do** mantener un solo botón primario por pantalla, teñido con la línea en curso cuando la acción avanza por esa línea.
- **Do** usar la curva `cubic-bezier(.22, 1, .36, 1)` para entradas y desplazamientos, y colapsar todo movimiento con `prefers-reduced-motion`.

### Don't:
- **Don't** agregar un octavo color ni reutilizar un color de línea fuera de su módulo; la franja de red es el único lugar donde aparecen los siete juntos.
- **Don't** volver a la grilla de tarjetas de curso con barras de progreso como forma principal de mostrar el temario; el temario es el mapa.
- **Don't** usar una segunda familia de display ni poner mono fuera de código y datos.
- **Don't** dar sombra a paneles internos, veredictos o bloques de código; la sombra es solo de las piezas de primer nivel y los flotantes.
- **Don't** poner un rótulo en mayúsculas encima de un titular como antetítulo; el rótulo en mayúsculas solo nombra un dato o un grupo.
- **Don't** usar el suelo crema: el hueso de andén es de baja saturación.
