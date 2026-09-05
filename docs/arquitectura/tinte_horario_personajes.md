# Tinte de personajes por horario — propuesta

> **Estado: NO implementado.** Es un relevamiento hecho el 2026-09-04, guardado
> para el día que se encare. Nada de lo que hay acá está en el código todavía.
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
