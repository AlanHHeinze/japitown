# Tinte de personajes por horario — propuesta

> **Estado: implementado (2026-09-12)** en `game/script/core/utils/tinte_horario.rpy`.
> Lo de abajo es el relevamiento original (2026-09-04); al final está lo que
> se construyó y en qué difiere.
>
> Todo lo que se afirma del motor está verificado contra el SDK instalado
> (`C:/Renpy/renpy-8.4.1-sdk`, Ren'Py 8.5.2) y se cita el archivo y la línea.

## Qué se quiere

Que los personajes tomen levemente el tono de la luz del ambiente según el
horario — de tarde un poco cálidos, de noche un poco fríos— **sin que el fondo
reciba el mismo tinte**, porque el fondo ya viene pintado con la luz de esa hora
y volver a teñirlo lo satura.

## Por qué una capa con transparencia NO sirve

Fue la primera idea y no puede funcionar. Un plano solo puede estar en dos
lugares:

- **entre el fondo y los personajes** → pinta el fondo, no los personajes;
- **arriba de los personajes** → pinta todo, fondo incluido.

No existe una posición donde afecte a los sprites y no al fondo, porque el
efecto de un plano es siempre "sobre lo que tiene debajo". El tinte tiene que
aplicarse **a los sprites mismos**.

## La herramienta correcta: `matrixcolor`

Es una propiedad de transform que transforma los colores del displayable al que
se aplica. `TintMatrix` **no toca el canal alfa**
(`renpy/common/00matrixcolor.rpy:188`), así que pinta solo los píxeles visibles
del sprite. El fondo nunca pasa por esa transformación, así que no se entera.

---

## HAY DOS SUPERFICIES, no una

Este es el hallazgo importante del relevamiento, y el que define el tamaño real
del trabajo. Los sprites de los personajes se dibujan de **dos maneras
distintas**, en capas distintas, y cada una necesita su solución:

| Superficie | Cómo se dibuja | Capa | Cuándo la ve el jugador |
|---|---|---|---|
| **Narrativa** | `show violet_parada ...` | `master` | Escenas de quest, eventos, talk |
| **Exploración (HUD)** | `imagebutton: idle sprite_actual` dentro de la screen `navegacion_locaciones_con_hud` | `screens` | Caminando por la casa — o sea, **la mayor parte del tiempo** |

Una solución de capa resuelve la primera y **no toca la segunda**. Si se hace
solo eso, el personaje cambia de tono al entrar a una escena y vuelve al tono
plano al salir, que se ve peor que no hacer nada.

---

## Superficie 1 — sprites narrativos (capa `master`)

Tres piezas, ninguna de las cuales obliga a tocar los cientos de `show` que hay
en el proyecto:

### 1. Una capa propia para los personajes

El default es `["master", "transient", "screens", "overlay"]`
(`renpy/config.py:152`). Se inserta una capa `personajes` justo después de
`master`.

### 2. Rutear los sprites a esa capa por TAG

`config.tag_layer` (`renpy/config.py:705`) mapea *tag de imagen → capa*, y lo
consulta `default_layer()` en
`renpy/exports/displayexports.py:137`. Registrando ahí los tags de los
personajes, `show violet_parada` se va solo a la capa nueva: **no hay que
cambiar ni un `show`**.

Los tags ya están enumerados: los saca `tools/validar_sprites.py`, que hoy
recorre los 35 layeredimages del proyecto.

### 3. Teñir la capa entera cuando cambia el horario

`renpy.show_layer_at(transform, layer="personajes")`
(`renpy/exports/displayexports.py:800`) aplica un transform a toda la capa de
una sola vez. Se llama al avanzar el horario y al dormir — un transform por
horario, cero por sprite.

---

## Superficie 2 — sprites del HUD (capa `screens`)

Acá no sirve la capa, porque el sprite se dibuja adentro de la screen. **Tampoco
se puede teñir la screen entera**: la misma screen dibuja los hotspots, el vapor
del baño y los elementos de quest.

La buena noticia es que el punto de dibujo está concentrado. El sprite se
resuelve en un `$ sprite_actual = ...` y se dibuja en **un solo `imagebutton`**
(`game/script/ui/hud/hud_navigation.rpy`, bloque "Modo normal: sprites
estáticos", cerca de la línea 1037):

```renpy
imagebutton:
    idle sprite_actual
    hover sprite_actual
```

Agregarle `at <transform del horario>` cubre a los tres NPCs de una. Hay que
revisar aparte los `imagebutton` de elementos de quest del mismo bloque, y
decidir si también van teñidos (probablemente sí los que son personajes, no los
que son objetos).

---

## Los tres puntos que hay que resolver sí o sí

### 1. `scene` deja de limpiar los sprites — es el riesgo serio

`scene` limpia **solo** la capa que se le pasa, y por defecto es `master`
(`renpy/exports/displayexports.py:559`). Con los sprites narrativos en otra
capa, `scene expression _bg` deja de borrarlos, y cualquier escena que hoy
confíe en eso se llevaría sprites colgados de la escena anterior.

**Solución**: `config.scene` es un hook — Ren'Py lo invoca en
`renpy/ast.py:1477`. Se lo reemplaza por una versión que limpie las dos capas y
`scene` vuelve a comportarse exactamente igual que hoy.

Es lo primero que hay que implementar y lo primero que hay que testear.

### 2. `show expression` se saltea `tag_layer`

`default_layer()` devuelve `default_tag_layer` sin mirar el mapa cuando la
imagen se muestra por expresión (`displayexports.py:130`). En el proyecto hay
**6 sitios** que muestran sprites de personaje así, y necesitan `onlayer
personajes` explícito:

| Archivo | Qué muestra |
|---|---|
| `core/talk/talksystem_labels.rpy:53` | el sprite del NPC en la charla |
| `characters/violet/quests/violet_quest_09_b.rpy:334, 381` | Violet en la cama |
| `characters/violet/ventajas/juegosnuevos/jn_pocketboy.rpy:274, 458` | Violet en el altillo |
| `characters/mc/quests/mc_quest_0_a.rpy:188` | las cajas de la intro (objeto, NO va teñido) |

`sticky_tags` gana sobre `tag_layer` (`displayexports.py:137`), así que un tag
que ya quedó pegado a una capa se queda ahí — otro motivo para poner el mapa en
`init` y no tocarlo en runtime.

### 3. La fuerza del tinte queda abierta

`TintMatrix` es **a full**: vuelca el sprite entero al color, que no es el efecto
sutil que se busca. Para mezclarlo con la identidad la vía documentada es
**subclasear `ColorMatrix`** (`renpy/common/00matrixcolor.rpy:106`; la doc del
SDK lo propone explícitamente para efectos propios) con algo tipo
`TinteAmbiente(color, fuerza)`.

Es lo único de esta propuesta que no está resuelto sobre el papel: la expresión
exacta de la mezcla hay que ajustarla probando, no deducirla.

**Nota de diseño**: el tinte puro tiende a leerse como "filtro pegado encima".
Suele quedar mejor combinar un tinte muy leve con una baja mínima de saturación
y de brillo (`SaturationMatrix`, `BrightnessMatrix`, mismo archivo) que subir la
fuerza del tinte solo.

---

## Orden sugerido de implementación

1. **`config.scene`** y la capa nueva, con los sprites todavía sin teñir.
   Recorrer el juego y confirmar que nada quedó colgado en pantalla. Este paso
   no cambia ni un píxel si está bien hecho: es la red de seguridad.
2. **Un solo horario, una sola locación**, con el tinte a ojo, para juzgar el
   efecto antes de invertir en el resto.
3. Los **6 sitios de `show expression`**.
4. La **superficie 2** (el `imagebutton` del HUD).
5. Los cuatro horarios y la clase `TinteAmbiente` definitiva.

## Qué verificar al terminar

- `tools/validar_sprites.py` sin hallazgos y lint completo sin errores.
- Recorrido por la casa en los **cuatro horarios**: que el tono del personaje sea
  el mismo caminando (HUD) que dentro de una escena (narrativa). Es el síntoma
  de que las dos superficies quedaron alineadas.
- Una escena con `scene` de por medio (cualquier quest que cambie de locación):
  que no queden sprites de la escena anterior.
- La charla (`talksystem`), la 09_b y el Pocket Boy: son los `show expression`.
- Guardar y cargar: los transforms de capa no se guardan, así que hay que
  confirmar que el tinte se re-aplica al cargar y no queda la capa sin teñir.

---

## Lo que se construyó (2026-09-12)

`game/script/core/utils/tinte_horario.rpy`, siguiendo el orden sugerido:

| Pieza | Cómo quedó |
|---|---|
| Capa `personajes` | `config.layers.insert(index("master")+1, "personajes")` en `init -20`. |
| `scene` limpia las dos capas | **`config.scene_callbacks`** (no hizo falta reemplazar `config.scene`): un callback que, cuando se limpia `master`, limpia `personajes` **y reaplica el tinte** — limpiar una capa le borra el at-list (`config.scene_clears_layer_at_list`, `scenelists.py:617`), y sin eso cada `scene` de una escena dejaba la capa sin teñir (bug encontrado en la primera prueba). `actualizar_bg_master` pasa por ahí. |
| Ruteo por tag | `init 999`: todo tag con prefijo de personaje (`violet_`, `monica_`, `jasmine_`, `mc_`, `repartidor_`, `padre_`, `beso_`) que sea un **layeredimage** o una `image` **webp/png** (con alfa). Los CG jpg con prefijo (`violet_quest08_livingnublado`) quedan en master: teñirlos es lo que no se quiere. `monica_evento_01` se excluye a mano (trae un jpg de fondo adentro). 532 tags ruteados, 27 layeredimages. |
| `show expression` | `onlayer personajes` en los 5 sitios de personaje (talk, 09_b x2, Pocket Boy x2). Las cajas de la intro quedan en master. |
| Tinte de la capa | `aplicar_tinte_personajes()` → `renpy.show_layer_at([Transform(matrixcolor=…)], layer="personajes")`. Se llama en `actualizar_bg_master` (cada cambio de horario o locación), al final de `dormir()` y en el after_load. `show_layer_at` vive en las scene lists (se guarda y rollbackea), la reaplicación es por seguridad. |
| HUD | **Sin tinte, por decisión (2026-09-12)**: los idles de la casa son ilustraciones ya pintadas con la luz de esa hora, teñirlas se veía mal. El tinte es solo para los sprites de las secuencias de diálogo (layeredimages en la capa). `tinte_transform_actual()` queda para cualquier sprite de personaje que se dibuje en una screen y sí lo pida. |
| La fuerza | `TinteAmbiente(color, fuerza, modo)` (subclase de `ColorMatrix`). Modo **multiplicar** (el que quedó, `TINTE_MODO`): `out = pixel · ((1-f) + f·color)` — matriz diagonal, como la capa Multiply de Photoshop con opacidad `f`: oscurece y colorea según lo que hay debajo. Modo "normal" (`out = (1-f)·pixel + f·color`, corrimiento en la 4ta columna): fue el primero y aplastaba a color plano. Un PNG exportado desde Photoshop no sirve: el PNG no guarda modos de fusión, Ren'Py lo compondría en normal. |

Colores: mañana ninguno · tarde `#df7f4e` · noche `#b78a73` · trasnoche `#303b4b`
(`TINTE_HORARIO_COLORES`). Fuerza **0.25** (opacidad de la capa multiplicar) (`TINTE_HORARIO_FUERZA`): es
el único botón para ajustar a ojo; con 1.0 el sprite entero pasa al color.

Regla para contenido nuevo: un sprite de personaje se muestra con `show <tag>`
y un tag con prefijo de personaje (va solo a la capa); si se muestra con
`show expression`, lleva `onlayer personajes`. Los idles del HUD no se tiñen.

