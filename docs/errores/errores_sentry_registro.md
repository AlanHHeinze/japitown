# Registro de errores — Sentry

> Errores capturados por **Sentry** (integración en `sistema_sentry.rpy`), a partir
> de 0.1.8b. Distinto de `errores_registro.md` (que era el volcado manual de los
> reportes viejos de Discord).
>
> Cada entrada: estado, traceback, diagnóstico y fix. IDs con prefijo **S**.

---

## Resumen

| Errores procesados | Corregidos | En observación |
|---|---|---|
| 11 | 5 (S01, S02, S03, S05, S08) | 6 (familia GL: S04/S06/S07/S09 · S10 sync · **S11 bucle: sin localizar, prioridad alta**) |

> ⚠️ **Importante (S02):** todos los fixes de esta sesión están **sin commitear**
> (working tree). Si el build parte de un checkout limpio de git, no los incluye.
> Hay que **commitear (o buildear desde el working tree) y rebuildear** para que
> los arreglos lleguen a los jugadores.

---

## 🔧 Nota de herramienta — el fingerprint estaba roto (corregido 2026-07-30)

Hasta esta fecha, **Sentry abría un issue nuevo por cada ocurrencia** en vez de
agrupar los errores iguales. La causa estaba en nuestra integración, no en Sentry.

`_jp_sentry_parse()` tomaba la **última línea no vacía** del traceback para sacar
tipo y mensaje. Pero Ren'Py agrega DESPUÉS del traceback un bloque de metadata:

```
AttributeError: 'NoneType' object has no attribute 'update'
                                          <- (linea en blanco)
Emscripten-3.1.67-wasm32-32bit wasm32
Ren'Py 8.5.2.26010301
Japitown 0.1.8f
Thu Jul 30 22:07:51 2026                  <- ULTIMA linea no vacia
```

Resultado: el tipo era siempre `Error` y el mensaje era **el timestamp**. Como el
fingerprint se arma con esos dos valores, cada evento tenía una huella única.
Se veía en el dashboard como `Fingerprint values: Error, Thu Jul 30 22:07:51 #`.

**Arreglo:** ahora se busca hacia atrás la última línea que realmente parezca una
excepción (sin indentar, con forma de identificador). Verificado contra los
tracebacks reales de S04–S07:

| Traceback | Fingerprint viejo | Fingerprint nuevo |
|---|---|---|
| S04 (22:07:47) | `Error \| Thu Jul 30 22:07:47 #` | `AttributeError \| 'NoneType' object has no attribute 'update'` |
| S04 (22:07:51) | `Error \| Thu Jul 30 22:07:51 #` | `AttributeError \| 'NoneType' object has no attribute 'update'` |
| S06 | `Error \| Thu Jul 30 17:17:38 #` | `renpy.gl2.gl2shader.ShaderError` |
| S07 | `Error \| Thu Jul 30 17:17:57 #` | `Exception \| Could not set video mode.` |

Los dos eventos de S04 ahora **agrupan juntos**; antes eran dos issues separados.

**Consecuencia para leer el histórico:** todos los conteos anteriores a esta
fecha están inflados en cantidad de *issues* (no de eventos). Los conteos de este
documento son correctos porque se agruparon a mano.

## S01 — TypeError: not all arguments converted during string formatting (screenshot)
- **Estado:** ✅ **CORREGIDO en código (2026-07-26)** — pero el build 0.1.8b
  publicado se generó **antes** de este fix, así que sigue crasheando en la calle
  (visto en Windows 0.1.8b, jugando en inglés, al sacar captura). Se va con el
  rebuild limpio. Mismo caso de deploy que S02.
- **Versión:** 0.1.8b · Windows 11 (y recurrente)
- **Clave:** `TypeError|not all arguments converted during string formatting`
- **Traceback (cola):**
```
  File "renpy/common/00keymap.rpy", line 346, in _screenshot_callback
    renpy.notify(__("Saved screenshot as %s.") % fn)
TypeError: not all arguments converted during string formatting
```

#### 🔧 Diagnóstico y arreglo

**Qué lo producía:** al sacar una captura de pantalla, Ren'Py hace
`renpy.notify(__("Saved screenshot as %s.") % fn)`. `__()` traduce el string al
idioma actual. En **inglés**, la traducción de `"Saved screenshot as %s."` en
[tl/english/common.rpy](game/tl/english/common.rpy) tenía el **`new` vacío**
(`new ""`) — auto-generado y nunca completado. Entonces `__()` devolvía `""`, y
`"" % fn` falla: hay un argumento (`fn`) pero **ningún `%s`** en el string.
(El español `tl/None` estaba bien: `"Captura guardada como %s."`.)

**Clase de bug:** cualquier traducción con `new ""` de un string que lleva
`%s`/`%d` y se usa con `% args` crashea igual. Barrido de todo `game/tl`:
**5 casos**, todos built-in de Ren'Py en `tl/english/common.rpy` con `new ""`:
- `Saved screenshot as %s.` → **crash** (el reportado).
- `Failed to save screenshot as %s.` → crash al fallar una captura.
- `Save slot %s: [text]` / `Load slot %s: [text]` → crash latente (self-voicing/accesibilidad).
- `%b %d, %H:%M` → no crashea pero mostraba **fecha vacía** en los slots de guardado en inglés.

**El arreglo:** se rellenaron los 5 `new` vacíos con el texto inglés correcto
(mismo que el `old`, preservando los `%`). Verificación: 0 traducciones con
`%`-format + `new` vacío restantes; lint limpio.

**Nota:** solo afectaba a quienes juegan en **inglés**. El bug estaba desde antes;
recién ahora entró por Sentry porque alguien sacó una captura jugando en inglés.

## S02 — TypeError: 'str' object is not callable (`_p`, en 0.1.8b)
- **Estado:** ⚠️ **CORREGIDO EN CÓDIGO, pero el build 0.1.8b publicado NO lo tiene**
- **Veces:** 3+ (varios jugadores en 0.1.8b web; misma firma exacta). Todos los
  reportes de `_p` en 0.1.8b son este mismo — build corriendo talksystem viejo por
  caché/`.rpyc` stale. Se resuelve con el rebuild limpio + cache-busting (ver abajo).
- **Versión:** 0.1.8b · Web (Emscripten)
- **Clave:** `TypeError|'str' object is not callable`
- **Traceback (cola):**
```
  File "renpy/common/00start.rpy", line 86, in _init_language
    renpy.change_language(language, force=True)
  File "renpy/common/00gui.rpy", line 120, in _apply_rebuild
    renpy.ast.redefine([ "store.gui" ])
  File "game/script/ui/base/options.rpy", line 35, in <module>
    define gui.about = _p("""
TypeError: 'str' object is not callable
```

#### 🔧 Diagnóstico

**Es el mismo bug que E01** (`errores_registro.md`): un `for _i, _p in ...` en
`talksystem_labels.rpy` pisaba el builtin `_p` de Ren'Py al usar "Hablar"; luego,
al cambiar de idioma / reiniciar, `define gui.about = _p(...)` crasheaba.

**El código fuente YA está arreglado** (`_p`→`_t_p`). Verificación exhaustiva
(2026-07-26): **0** shadows de `_p` en todo `game/` (for/assign/unpack/as/walrus/
global/setattr/exec/globals/store._p); el `.rpyc` local está fresco; lint limpio.

**Por qué 0.1.8b igual crashea (diagnóstico corregido):** el código fuente **Y el
`.rpyc` local tienen el fix** — se descompiló `talksystem_labels.rpyc` y contiene
`_t_p` (×48), no el `for _i, _p` viejo. Barrido exhaustivo: **0** shadows de `_p` en
todo `game/`. O sea el fix está bien aplicado; un build hecho ahora sale limpio.

Como el usuario buildea **local con los archivos actuales**, el problema NO es
commitear. El 0.1.8b publicado está corriendo **código viejo de talksystem** por
una de estas causas de deploy (build **web**):
1. **Caché del navegador** (lo más probable): los builds web de Ren'Py no hashean
   los nombres de archivo, así que el navegador puede servir un bundle parcial —
   `options` nuevo (versión 0.1.8b) + `talksystem.rpyc` cacheado viejo (buggy).
2. **`.rpyc` stale al momento de ESE build:** si ese 0.1.8b se generó antes de que
   Ren'Py recompilara talksystem con el fix (el `.rpyc` local se recompiló 07-25).

**Acción requerida (no de código):**
1. **Rebuild limpio:** borrar los `.rpyc` (o `game/cache/`), reabrir el proyecto en
   Ren'Py (fuerza recompilar todo), y recién ahí generar el build web. Así ningún
   `.rpyc` viejo se cuela.
2. **Cache-busting en el deploy:** subir el build nuevo y forzar que los jugadores
   reciban archivos frescos (hard-refresh / limpiar caché, o servir el juego desde
   una carpeta/URL nueva). Si no, el navegador puede seguir sirviendo lo viejo.

**Verificación (2026-07-26):** todos los fixes de la sesión (E01–E06, S01, leak,
traducciones, espiar off, versión 0.1.8b) confirmados presentes en el source.

## S03 — Exception: A translation ... already exists (traducción duplicada)
- **Estado:** ✅ **YA RESUELTO — era un estado transitorio; el repo actual está limpio**
- **Versión:** 0.1.8b · Windows (crash de init, al cambiar de idioma a inglés)
- **Clave:** `Exception|A translation for ... already exists`
- **Traceback (cola):**
```
  File "game/tl/english/script/core/quests/quest_strings.rpy", line 460, in script
    old "Hoy es sábado, tengo que despertar a Violet para que limpiemos la casa."
Exception: A translation for "Hoy es sábado, tengo que despertar a Violet para que
limpiemos la casa." already exists at game/tl/english/quest_strings_despertar.rpy:303.
```

#### 🔧 Diagnóstico

**Qué lo producía:** la misma string estaba traducida en DOS archivos a la vez
(`quest_strings.rpy` **y** `quest_strings_despertar.rpy`). Las traducciones de string
son globales; un `old` repetido crashea a Ren'Py **al cargar / cambiar de idioma**
(afecta a todos los que juegan en inglés).

**Origen:** fue un **duplicado transitorio** durante la sesión de fix. Al agregar
las traducciones de "mensajes de despertar", un primer intento metió "Hoy es
sábado..." en `quest_strings_despertar.rpy` (creando el duplicado con `quest_strings.rpy`)
y se **revirtió** minutos después. El build 0.1.8b se generó **justo en esa ventana**,
así que capturó el estado roto.

**Varios duplicados transitorios distintos** (todos de esta sesión, todos ya
revertidos), capturados por builds hechos a mitad de edición. Vistos hasta ahora:
- `"Hoy es sábado, tengo que despertar a Violet..."` (quest_strings ↔ despertar)
- `"Tengo que responderle a CoXplay con la dirección."` (faltantes ↔ despertar)
- `"Mónica se quejó de dolor en sus hombros, podría hacerle un masaje en la tarde."` (quest_strings ↔ despertar)
- (posibles más del mismo lote de 4 que se agregó y revirtió: "Podría mostrarle a
  violet los cosplays..." y "Tengo que encontrar algún momento para acercarme a Violet...")

**Estado actual:** el repo **ya no tiene ningún duplicado**. Barrido global
(2026-07-26): **0 duplicados** en las 1508 traducciones de string; lint limpio.
Un build fresco no tiene este error.

**Lección:** no generar builds a mitad de una sesión de edición (puede capturar
estados intermedios rotos). El rebuild limpio del final (con los `.rpyc` borrados y
todos los cambios finales) evita esto.

## S04 — AttributeError: 'NoneType' object has no attribute 'update' (renderer en web)

- **Estado:** ⚠️ **CAUSA IDENTIFICADA (incidente A) — sin fix, pero SUBIÓ DE PRIORIDAD**
  al aparecer un segundo incidente independiente (ver Reevaluación al final)
- **Veces:** 9 eventos, en **5 incidentes** (C y D podrían ser el mismo jugador):
  - **Incidente A** (3 eventos) — `17:18:00`, `17:18:12`, `17:18:24`. Misma
    sesión, intervalos de **exactamente 12 s**, alternando las líneas 181 y 184
    del splash (los dos `pause` del bucle de precarga). Precedido por
    **S06 → S07** en la misma sesión: cadena completa y explicada.
  - **Incidente B** (3 eventos) — `22:07:47` (splash, línea 181), `22:07:50`
    (`intro_main.rpy:224`, menú de intro) y `22:07:51`
    (`config_globals.rpy:144`, pantalla de ingreso del nombre). **~5 h después**
    del A. Igual que en A, **arranca en el bucle de precarga del splash**; los
    dos siguientes son el jugador tocando "Continuar" en la pantalla de error y
    avanzando hasta chocar otra vez. Sin S06/S07 reportados, pero el punto de
    partida es el mismo. Tags: `dias_totales=1`, `loc=?` (partida recién
    empezada). Geo: **Clichy-sous-Bois, Francia**.
  - **Incidente C** (1 evento) — `14:45:43`, el **más temprano** de los tres.
    `pantalla_carga.rpy:191`, en el `with dissolve` que cierra la pantalla de
    carga (justo al terminar la precarga). Tags: `dias_totales=1`, `loc=?`.
    Geo: **Miami, Estados Unidos**.
  - **Incidente D** (1 evento) — `14:57:00`, **11 min después del C**.
    `pantalla_carga.rpy:184` (splash otra vez). Geo: **Estados Unidos** (sin
    ciudad). Puede ser el mismo jugador del C reintentando tras recargar, o uno
    distinto — la precisión geográfica de Sentry varía y no hay ID de usuario.
    A efectos del análisis da igual: no aporta información nueva.
  - **Incidente E** (1 evento) — `22:43:05`, `pantalla_carga.rpy:181` (splash).
    Geo: **Nairobi, Kenia**.
- ⚠️ **Se repite por diseño dentro de un mismo incidente.** Una vez muerto el
  renderer no se recupera solo: cada interacción posterior vuelve a reventar
  hasta que el jugador cierra. Un solo dispositivo con WebGL roto genera
  **muchos** eventos. Al triagear, **agrupar por sesión/timestamp** antes de
  contar jugadores afectados — lo que importa no es el volumen de eventos sino
  cuántas sesiones distintas lo producen.
- **Versión:** 0.1.8f · **Web (Emscripten)**
- ⚡ **Ver S06:** 22 segundos antes, en la misma sesión, un `ShaderError`
  mató el renderer durante un `on_resize`. Este AttributeError es el síntoma
  posterior: el loop de interacción encontró `renpy.display.draw` en `None`.
  La "hipótesis 1" de abajo quedó **confirmada**.
- **Clave:** `AttributeError|'NoneType' object has no attribute 'update'`
- **Contexto:** durante el **splashscreen**, en el `pause` del busy-wait que
  espera la decodificación de cada lote de la precarga
  (`pantalla_carga.rpy:181`).
- **Traceback (cola):**
```
  File "//game/script/ui/base/pantalla_carga.rpyc", line 181, in script
  File "renpy/display/core.py", line 2808, in interact_core
AttributeError: 'NoneType' object has no attribute 'update'
```

#### 🔎 Diagnóstico

La línea que revienta es de Ren'Py, no nuestra:

```python
# renpy/display/core.py:2808
if renpy.display.draw.update(force=self.display_reset):
```

`renpy.display.draw` es el **renderer**. Estaba en `None`, o sea que el motor
entró al loop de interacción **sin renderer**. Dos formas de llegar a eso:

1. **Nunca se inicializó.** En web eso pasa cuando falla el contexto WebGL
   (navegador/dispositivo sin soporte, contexto bloqueado o perdido). Es el
   patrón que aparece en los reportes de web de Ren'Py.
2. **Se destruyó a mitad de camino.** `renpy.display.draw = None` está en el
   camino de reinicio total del motor (`renpy/__init__.py:676`), que corre al
   hacer un restart/reload.

Por el contexto (web, al arrancar, en el primer `pause` con contenido en
pantalla) la **hipótesis 1 es la más probable**: el renderer no llegó a existir.
Si es así, el juego era injugable en ese dispositivo de todos modos, y el
crash es el síntoma y no la causa.

#### 🚫 Por qué no hay fix desde el código

El fallo está dentro del loop de interacción de Ren'Py, antes de que nuestro
código pueda intervenir. No se puede parchear desde el proyecto.

**Mitigación posible (NO aplicada):** el splash hace muchísimas interacciones —
~691 imágenes / lotes de 6 = ~115 lotes, cada uno con hasta 40 × `pause 0.01`.
Eso es una ventana de exposición grande en el momento más frágil del arranque en
web. Subir ese `pause` a 0.05 mantendría la misma espera de reloj con 5× menos
ciclos de interacción. No se hizo porque: (a) es una sola ocurrencia, (b) no
arreglaría el caso de "el renderer nunca existió", y (c) hace menos fluido el
contador de %. Reconsiderar si el error se vuelve frecuente.

**Si se vuelve masivo:** pedir a los reportantes navegador + dispositivo. Si se
concentra en un navegador o en equipos viejos, confirma el fallo de WebGL y la
respuesta es de soporte (recomendar otro navegador o la versión de escritorio),
no de código.

#### 🔄 Reevaluación (2026-07-30, tras el incidente B)

**Qué cambió:** dejó de ser "un dispositivo con mala suerte". Dos sesiones
distintas, separadas por 5 horas y en contextos distintos del juego, con el
renderer muerto. Eso mueve la lectura de *anomalía aislada* a *patrón posible*.

**Qué NO cambió:** seguimos sin poder arreglarlo desde el juego. El fallo ocurre
dentro del loop de interacción de Ren'Py, con el contexto GL ya perdido. No
usamos shaders propios. Las opciones evaluadas en S06 (forzar GL1, precompilar
shaders, reducir resize) siguen teniendo el mismo daño colateral: perjudicar a
todas las partidas estables por un caso que además no arreglarían.

**Decisión: se mantiene el no-fix, pero baja el umbral para reabrir.**

**Dato que falta para decidir bien** — si es el mismo mecanismo o dos causas:
1. ¿Hubo un `ShaderError` (S06) o un `Could not set video mode` (S07) cerca de
   las **22:07**? Si sí, es la misma vía (shader → resize) y hay un patrón real.
   Si no, el renderer murió por otra razón y hay que investigar aparte.
2. ¿Son **el mismo jugador**? Sentry agrupa por evento, no por usuario. Si es la
   misma persona reintentando en el mismo dispositivo, sigue siendo 1 dispositivo
   con WebGL roto. Si son dos personas distintas, es un patrón.

**Umbral para reabrir:** 3+ sesiones distintas, o confirmación de que son
jugadores distintos. Ahí sí conviene invertir en investigar el renderer.

#### 💡 Hipótesis NUEVA: la precarga del splash como causa (no como escenario)

**El dato:** los **2 incidentes arrancan en el bucle de precarga del splash**
(`pantalla_carga.rpy:181`). Hasta ahora se leía como "el splash es donde estaba
el jugador cuando falló el GL". Con dos de dos, vale invertir la lectura: puede
que la precarga **cause** el fallo.

**El mecanismo plausible:** la precarga llena el cache de imágenes hasta
`CARGA_TOPE_CACHE = 0.75` de `config.image_cache_size_mb = 400`, o sea hasta
**~300 MB de texturas YA DECODIFICADAS** empujadas a la GPU lo más rápido
posible. En un navegador móvil o una GPU modesta, eso puede agotar los recursos
del contexto WebGL — y ahí aparecen justamente los síntomas que vemos:
`ShaderError` al compilar (S06) y `draw` muerto (S04).

**Contraargumento honesto:** hay sesgo de supervivencia. El splash es donde el
juego pasa sus primeros ~30 segundos y donde más trabajo de GPU hace, así que
*cualquier* fallo temprano de GL tendería a caer ahí igual. La correlación es
sugestiva, no concluyente.

> ### ⛔ HIPÓTESIS DEBILITADA (2026-07-30, con el S07 del incidente C)
>
> Apareció el evento que **precede** al incidente C: un `Could not set video mode`
> a las `14:45:20`, 23 s antes, en **`pantalla_carga.rpy:152`**.
>
> Esa línea es el **primer `with dissolve` del splash** — el fundido del logo de
> empresa. Ocurre **ANTES de que la precarga siquiera empiece** (arranca en la
> 159).
>
> O sea: en ese incidente **el renderer ya estaba roto antes de cargar una sola
> textura**. La precarga no pudo haberlo causado.
>
> **Lectura corregida:** el splash no es la causa, es el primer lugar donde el
> juego toca la GPU. El primerísimo `with dissolve` ya necesita inicializar
> texturas y shaders; si el WebGL del dispositivo está roto o limitado, falla
> justo ahí. Los crashes "en la precarga" son el mismo fallo apareciendo unos
> segundos después, no un fallo distinto.
>
> **Consecuencia práctica:** bajar `CARGA_TOPE_CACHE` **no habría servido**. La
> decisión de no tocar la web (tomada por razones de producto) queda además
> respaldada por la evidencia técnica.

**Mitigación posible — ESTA SÍ tiene daño colateral bajo:**

| Opción | Efecto | Daño colateral |
|---|---|---|
| Bajar `CARGA_TOPE_CACHE` **solo en web** (ej. 0.75 → 0.35) | La mitad de presión de VRAM en el arranque | **Bajo.** Algunas imágenes se decodifican al mostrarse: un parpadeo pixelado la primera vez. No afecta a escritorio |
| Bajar `config.image_cache_size_mb` en web | Techo de cache más bajo en toda la partida | **Medio.** Más recargas durante el juego |
| No tocar nada | — | Cero, pero si la hipótesis es correcta se sigue perdiendo a esos jugadores |

**Estado: NO aplicado.** Es una hipótesis, no una causa probada, y tocar la
precarga afecta a **todos** los jugadores web para atender 2 incidentes. Antes
de aplicarla conviene confirmar con los datos pedidos arriba (si son jugadores
distintos, y si hubo S06/S07 a las 22:07).

**Si se confirma:** la opción 1 es la que conviene — se limita a web, es un
número, y su costo es estético (un parpadeo) contra el beneficio de que el juego
arranque.

#### ✅ Umbral ALCANZADO (2026-07-30): son jugadores distintos

Confirmado: los incidentes A y B son de **dos jugadores diferentes**. Eso cumple
la condición que se había fijado para reabrir, y descarta la lectura de "un solo
dispositivo con mala suerte". **Es un patrón real.**

**Sobre la geografía: descartada como pista.** Se había observado que los dos
primeros incidentes eran de Francia, con la advertencia de que con n=2 podía ser
solo la tasa base del tráfico. Con los incidentes siguientes quedó confirmado:
**Francia ×2, EE.UU. ×2, Kenia ×1**. La geografía no es un factor.

**Pero el reparto SÍ dice algo del alcance:** 5 incidentes en al menos 3 países y
4 jugadores distintos, en un solo día de reportes. No es un puñado de equipos
raros — es una fracción no despreciable de quienes abren el juego en web y
**nunca llegan a jugar**. Ese es el número a tener en cuenta al priorizar el APK:
no cuántos crashes hay, sino cuántos jugadores se pierden en la puerta.

#### 🔧 Mejora aplicada: más contexto en los reportes

El problema para decidir era que Sentry reporta `Emscripten wasm32` para **todo**
lo web, sin distinguir un celular de una PC — y la hipótesis de la precarga
depende justamente de eso (agotar la GPU es plausible en un móvil, no tanto en
escritorio).

Se agregaron tags en `_jp_sentry_tags()` (sistema_sentry.rpy):

| Tag | Para qué |
|---|---|
| `dispositivo` | movil / tablet / escritorio_web / escritorio |
| `renderer` | el renderer realmente en uso (`renpy.session["renderer"]`) |
| `navegador` | user agent recortado a 120 chars (solo web) |

Con esto, el **próximo** reporte de esta familia dice solo si fue en un móvil y
con qué navegador. Si los crashes de GL caen todos en `dispositivo=movil`,
la hipótesis de la precarga queda confirmada y se aplica la mitigación 1
(bajar `CARGA_TOPE_CACHE` en web).

#### 🚫 DECISIÓN FINAL (2026-07-30): no se toca la precarga web

Se descarta aplicar la mitigación, **incluso si la hipótesis se confirma**, por
una razón de producto:

1. **Costo general por un problema parcial.** Bajar `CARGA_TOPE_CACHE` afectaría
   a **todos** los jugadores web — incluidos los de escritorio, que son la
   mayoría y no tienen el problema — para atender solo a los móviles.
2. **El APK cubre esa población, y mejor.** Está planificado un build de Android
   con ajustes propios para móvil. Los jugadores que hoy sufren esto son justo
   los que van a pasar a la app nativa, donde el juego controla memoria y
   renderer directamente en vez de pelear con el WebGL del navegador.
3. **Sería trabajo con fecha de vencimiento.** Un parche en la precarga web
   quedaría obsoleto apenas salga el APK, dejando un número mágico que nadie
   recuerda por qué está ahí.

**Lo que SÍ queda:** los tags nuevos (`dispositivo`, `renderer`, `navegador`).
Cuestan cero, no afectan a nadie, y sirven para dimensionar cuánto pesa el
móvil web en los crashes — dato útil para priorizar el APK, no para parchear
la web.

**Reabrir solo si:** el problema aparece en `dispositivo=escritorio_web`. Ahí ya
no lo resolvería el APK y habría que atacarlo de verdad.

#### 📈 Actualización con el incidente C (3 de 3 en el splash)

**El dato:** los **4 incidentes arrancan en la pantalla de carga**, en tres
puntos distintos de ella:

| Incidente | Punto exacto |
|---|---|
| A | `pantalla_carga.rpy:181` — `pause` del busy-wait de un lote |
| B | `pantalla_carga.rpy:181` — idem |
| C | `pantalla_carga.rpy:191` — el `with dissolve` que cierra la carga |
| D | `pantalla_carga.rpy:184` — `pause` del contador de % |

4 de 4 refuerza bastante la hipótesis de la precarga: no es que "el splash sea
donde el jugador pasa más tiempo", es que **el fallo aparece mientras o justo
después de empujar ~300 MB de texturas a la GPU**. El incidente C es el más
elocuente: revienta en la transición final, o sea con el cache ya lleno.

**Qué NO cambia la decisión:** sigue en pie el no-fix por producto (el APK cubre
al móvil, y parchear la web perjudicaría a los de escritorio). Lo que cambia es
que la hipótesis técnica ya está bastante sólida — si algún día hay que atacarlo,
sabemos por dónde.

**Sigue faltando el dato decisivo:** móvil o escritorio. Los tags nuevos
(`dispositivo`, `renderer`, `navegador`) todavía no están en ningún build
publicado. Con el próximo build, el primer reporte de esta familia lo resuelve:
- Si es `movil` → confirmado, y lo resuelve el APK. No se toca la web.
- Si es `escritorio_web` → el APK NO lo cubre, y ahí sí hay que bajar
  `CARGA_TOPE_CACHE` (mitigación ya evaluada, daño colateral bajo).

## S05 — TypeError: 'int' object is not callable (builtin pisado desde la consola)

- **Estado:** ✅ **NO ES BUG DEL JUEGO — mitigado con red de seguridad (2026-07-30)**
- **Veces:** 1 — `Thu Jul 30 19:34:04 2026` (llegó dos veces a Sentry; **mismo
  evento**, no dos ocurrencias: idéntico traceback, versión y timestamp)
- **Versión:** 0.1.8f · Windows 10
- **Clave:** `TypeError|'int' object is not callable`
- **Traceback (cola):**
```
  File "renpy/common/00console.rpy", line 1195, in <module>
    console.interact()
  ...
  File "game/script/ui/hud/hud_stats.rpy", line 268, in <module>
    yoffset int(120 * _pe_k)
TypeError: 'int' object is not callable
```

#### 🔎 Diagnóstico

`int` no era el builtin: era un **entero guardado como variable del store**. A
partir de ahí, todo `int(...)` del juego revienta — y como el HUD lo usa para
escalar, se cae la interfaz entera.

**No lo causó nuestro código.** Barrido completo: no hay ninguna asignación a
`int` (ni `for int`, ni desempaquetado) en todo `game/`. Y el proyecto no fuerza
`config.developer` ni `config.console` (usa los defaults de Ren'Py).

El propio traceback muestra al culpable: la **consola de desarrollador estaba
abierta** (`00console.rpy:1195 → console.interact()`). Alguien con acceso a la
consola escribió algo tipo `int = 5`.

**Lo grave no es el crash puntual:** las variables del store **se guardan**. Una
vez pisado, el save queda envenenado de forma permanente y el jugador no tiene
manera de saber por qué ni de arreglarlo.

Es exactamente la misma clase de bug que E01/S02 (`_p`), que costó semanas de
crashes — solo que aquella vez el culpable sí era código nuestro.

#### 🔨 Mitigación

Nuevo `core/utils/builtins_pisados.rpy`:

- `jp_limpiar_builtins_pisados()` recorre ~28 builtins (`int`, `str`, `len`...) y
  borra del store los que estén tapados. Compara contra el builtin real, así que
  solo borra si el valor es distinto del original — no toca nada legítimo.
- Corre **al cargar partida** (cura saves ya envenenados) y **al cambiar de
  idioma** (el momento que re-evalúa los `define`, que es donde explotó `_p`).
- Botón 🧹 "Limpiar builtins pisados" en el panel de cheats, para reparar en
  caliente sin recargar.
- **No tapa bugs nuestros en silencio:** en modo desarrollador avisa por consola
  qué nombres limpió, así si el culpable es el código del juego igual se ve.

**Ojo:** NO se protegen `_`, `__` ni `_p`. Esos SÍ son variables del store en
Ren'Py (traducción y formato de párrafos); borrarlos rompería el juego.

## S06 — ShaderError: falla al compilar un shader tras un resize (web)

- **Estado:** 📋 **DOCUMENTADO — NO se aplica fix (ver daño colateral)**
- **Veces:** 1 — `Thu Jul 30 17:17:38 2026`
- **Versión:** 0.1.8f · **Web (Emscripten)**
- **Clave:** `ShaderError|gl2shader.Program.load_shader`
- **Traceback (cola):**
```
  File "renpy/display/core.py", line 2808, in interact_core
  File "renpy/gl2/gl2draw.pyx", line 711, in GL2Draw.update
  File "renpy/gl2/gl2draw.pyx", line 637, in GL2Draw.on_resize
  File "renpy/gl2/gl2texture.pyx", line 75, in TextureLoader.init
  File "renpy/gl2/gl2shadercache.py", line 372, in get
  File "renpy/gl2/gl2shader.pyx", line 283, in Program.load
  File "renpy/gl2/gl2shader.pyx", line 267, in Program.load_shader
renpy.gl2.gl2shader.ShaderError
```

#### 🔗 Es la CAUSA RAÍZ de S04

Los dos son **el mismo incidente**, del mismo jugador y la misma sesión:

| Hora | Error | Rol |
|---|---|---|
| 17:17:38 | **S06** (este) — el shader no compila durante `on_resize` | causa |
| 17:18:00 | **S04** — `'NoneType' object has no attribute 'update'` | consecuencia |

Secuencia: el canvas se **redimensiona** → Ren'Py reinicializa el contexto GL y
recompila sus shaders → la compilación **falla** → el renderer queda muerto →
22 segundos después, la siguiente interacción encuentra `renpy.display.draw`
en `None` y revienta con el AttributeError de S04.

Esto **confirma** la hipótesis 1 que se había anotado en S04 (fallo del
renderer) y le pone el mecanismo exacto.

#### 🔎 Análisis

- **No usamos shaders propios.** Barrido del proyecto: no hay
  `renpy.register_shader`, ni `Model()`, ni `shader=`, ni `mesh=`. Los que
  fallan son los built-in de Ren'Py.
- El disparador es **`on_resize`**: el contexto GL se rehace al cambiar el
  tamaño del canvas. En web eso pasa al entrar/salir de pantalla completa,
  al rotar el dispositivo o al aparecer/desaparecer la barra del navegador —
  justo lo que itch fuerza en móvil (ver el bug de pantalla cortada).
- La compilación de un shader estándar fallando apunta a una limitación del
  **WebGL de ese dispositivo/navegador**, no a nuestro contenido.

#### ⚖️ Fix posible y daño colateral

| Opción | Efecto | Daño colateral |
|---|---|---|
| Forzar renderer GL1/software en web | Evitaría GL2 | **Inaceptable.** GL1 está deprecado en Ren'Py 8; degradaría el rendimiento **de todos** los jugadores web por un caso |
| Precompilar shaders (`game/cache/shaders.txt`) | Compila al inicio | **No sirve:** si el shader no compila en ese dispositivo, precompilar solo adelanta el fallo |
| Reducir los resize en web | Menos recompilaciones | **No lo controlamos:** el resize lo dispara itch/el navegador, no el juego |
| **No hacer nada** | — | **Cero.** El jugador afectado no podía correr el juego igual |

**Decisión: no se aplica fix.** Es un fallo de GL del dispositivo, sobre código
que no es nuestro, con 1 ocurrencia. Cualquier cambio de renderer perjudicaría a
todas las partidas estables para atender un caso aislado.

**Si se vuelve frecuente:** pedir navegador + dispositivo. Si se concentra en un
navegador, la respuesta es de soporte (recomendar otro navegador o la versión de
escritorio). Si aparece en muchos equipos, ahí sí revisar el renderer.

## S07 — Exception: Could not set video mode (web)

- **Estado:** 📋 **DOCUMENTADO — mismo incidente que S06/S04, sin fix**
- **Veces:** 2 — `17:17:57` (incidente A) y `14:45:20` (incidente C, Miami).
  En C fue el **primer** error de la sesión, en `pantalla_carga.rpy:152`.
- **Versión:** 0.1.8f · **Web (Emscripten)**
- **Clave:** `Exception|Could not set video mode`
- **Traceback (cola):**
```
  File "//game/script/ui/base/pantalla_carga.rpyc", line 153, in script
  File "renpy/display/core.py", line 932, in start
  File "renpy/display/core.py", line 1264, in set_mode
Exception: Could not set video mode.
```

#### 🔗 Eslabón del medio de la cascada S06 → S07 → S04

Los **tres** errores son el mismo incidente, del mismo jugador y la misma sesión,
en 22 segundos:

| Hora | Error | Qué pasó |
|---|---|---|
| 17:17:38 | **S06** | Un shader no compila durante `on_resize` |
| 17:17:57 | **S07** (este) | Ren'Py intenta rehacer el display y **ningún renderer inicializa** |
| 17:18:00 | **S04** | `renpy.display.draw` quedó en `None` → revienta el loop de interacción |

#### 🔎 Análisis

La excepción sale de acá (`core.py:1259-1264`):

```python
for name, draw in draws:
    if draw.init(virtual_size):
        renpy.display.draw = draw
        break
    else:
        pygame.display.destroy()
else:
    renpy.game.preferences.fullscreen = False
    raise Exception("Could not set video mode.")
```

Ren'Py recorre **todos** los renderers disponibles y solo lanza el error si
**ninguno** logra inicializar. En web hay uno solo (GL2/WebGL), y ya había
fallado en S06. O sea: el contexto GL del dispositivo quedó muerto y no se pudo
reconstruir.

Detalle: Ren'Py pone `preferences.fullscreen = False` justo antes de lanzar,
para no dejar al jugador trabado en pantalla completa. O sea que el propio motor
ya contempla que este fallo se relaciona con transiciones de pantalla completa.

#### ⚖️ Fix posible y daño colateral

**Ninguno aplicable.** Es el mismo caso que S06: contexto WebGL muerto en el
dispositivo del jugador, dentro del código de inicialización de Ren'Py. No hay
nada del juego que intervenga en ese punto.

Ver el cuadro completo de opciones evaluadas en **S06** — todas descartadas por
daño colateral sobre las partidas estables.

**Decisión: no se aplica fix.** Se documenta para poder reconocer la cascada
completa si vuelve a aparecer.

## S08 — NameError: name '_jugar_intro' is not defined

- **Estado:** ✅ **CORREGIDO (2026-07-30)** — y se arregló la clase entera, no solo el caso
- **Veces:** 2 eventos, **2 variables distintas del mismo patrón**, mismo jugador
  y misma cascada de "Continuar":
  - `14:58:11` — `NameError: name '_nc_nombre' is not defined`
    (`config_globals.rpy:151`)
  - `14:58:12` — `NameError: name '_jugar_intro' is not defined`
    (`intro_main.rpy:257`)
  Geo: Estados Unidos. El de `_nc_nombre` llegó **después** de aplicado el fix y
  **confirma la auditoría**: se había corregido preventivamente al barrer el
  patrón, sin haber visto todavía un reporte suyo.
  - `22:44:06` — `_jugar_intro` otra vez, pero **otro jugador** (Nairobi, Kenia),
    1 min después de su S04. Confirma que no era un caso aislado: **cualquiera**
    que caiga en el bug del renderer y toque "Continuar" llega acá.

**Alcance real del fix:** 3 eventos, 2 jugadores en 2 continentes, en un día. No
arregla la causa raíz, pero corta la cascada — con el fix, esos jugadores dejan
de acumular errores derivados y pueden llegar a jugar si el renderer se recupera.
- **Versión:** 0.1.8f · **Web (Emscripten)**
- **Clave:** `NameError|name '_jugar_intro' is not defined`
- **Traceback (cola):**
```
  File "game/script/characters/mc/quests/intro_main.rpy", line 257, in <module>
    if _jugar_intro:
NameError: name '_jugar_intro' is not defined
```

#### 🔎 Diagnóstico

```renpy
$ _jugar_intro = renpy.call_screen("menu_intro_choice")   # línea 224  ← crashea acá
...
if _jugar_intro:                                          # línea 257  ← NameError
```

La línea 224 reventó por la muerte del renderer (misma familia que S04 — este
jugador venía crasheando desde las 14:57). El jugador tocó **"Continuar"** en
nuestra pantalla de error, la ejecución siguió **en el statement siguiente**, y
la variable nunca llegó a existir. 33 líneas después se la usa.

**Es una fragilidad que introdujo nuestra propia opción de "Continuar":** al
reanudar después de una excepción, cualquier variable que ese statement iba a
asignar queda sin definir.

#### 🔨 Arreglo — la clase, no el caso

Se auditó el patrón `$ var = renpy.call_screen(...)` seguido de uso. Había **3
instancias**, todas con la misma fragilidad:

| Variable | Archivo | Distancia al uso | Fallback elegido |
|---|---|---|---|
| `_jugar_intro` | intro_main.rpy:224 | 33 líneas | `False` → entra al juego sin intro |
| `_resultado_menu` | evento03_violet.rpy:550 | 2 líneas | `None` → cae al `jump violet_quest2_cierre` existente |
| `_nc_nombre` | config_globals.rpy:144 | 1 línea | `""` → termina en `mc_name = "Mc"`, el fallback ya previsto ✅ **confirmado en la calle** |

Se les agregó `default` a las tres (más `_nc_previo` y `_nc_error`, que se leen
como argumentos del mismo `call_screen`). Es la convención que el proyecto ya
usa para variables con guion bajo (`_skin_preview_*`, `_ruta_jq0`, `_carga_pct`).

**Daño colateral: nulo.** Los defaults solo entran en juego cuando la asignación
no llegó a ejecutarse — que hoy significa "el juego ya crasheó". En el camino
normal la variable se asigna igual que siempre. Los tres fallbacks son rutas que
ya existían en el código, no comportamiento nuevo.

**Nota:** esto NO arregla la causa raíz (el renderer muerto, ver S04/S06). Lo que
hace es que un crash de esa familia no se convierta en un segundo crash distinto
al continuar. El jugador puede llegar a jugar aunque el arranque haya fallado.

## S09 — AttributeError: 'NoneType' object has no attribute 'screenshot'

- **Estado:** 📋 **DOCUMENTADO — misma familia que S04/S06/S07, sin fix**
- **Veces:** 1 — `Thu Jul 30 14:58:07 2026` · Geo: Estados Unidos
- **Versión:** 0.1.8f · **Web (Emscripten)**
- **Clave:** `AttributeError|'NoneType' object has no attribute 'screenshot'`
- **Traceback (cola):**
```
  File "renpy/common/00gamemenu.rpy", line 85, in _enter_menu
    renpy.take_screenshot((config.thumbnail_width, config.thumbnail_height), ...)
  File "renpy/display/core.py", line 1341, in take_screenshot
AttributeError: 'NoneType' object has no attribute 'screenshot'
```

#### 🔎 Diagnóstico

Otra firma, **misma causa raíz**: `renpy.display.draw` en `None`.

```python
# renpy/display/core.py:1341
surf = renpy.display.draw.screenshot(self.surftree)
```

Al entrar al menú, Ren'Py saca una miniatura para los slots de guardado. Con el
renderer muerto, `draw` no existe y revienta. Es el mismo fallo que S04, solo
que en otro punto del motor (S04 es `draw.update()`, este es `draw.screenshot()`).

Sentry lo agrupa aparte porque el mensaje difiere, pero **no es un problema
nuevo**.

#### 🧭 Sesión completa de este jugador (EE.UU.)

Sirve como ejemplo de cómo un solo fallo de GL se ramifica:

| Hora | Error | Dónde |
|---|---|---|
| 14:57:00 | S04 | splash — `draw.update()` |
| 14:58:07 | **S09** | entrar al menú — `draw.screenshot()` |
| 14:58:11 | S08 | `_nc_nombre` sin definir (tras "Continuar") |
| 14:58:12 | S08 | `_jugar_intro` sin definir (tras "Continuar") |

Un contexto WebGL muerto → 4 errores de 3 firmas distintas en 72 segundos.

#### ⚖️ Fix

**Ninguno.** Está dentro del código de Ren'Py, con el renderer ya perdido. Ver
el cuadro de opciones evaluadas en **S06** — todas descartadas por daño
colateral. Los `default` de S08 ya evitan los errores *derivados*; este es
directo del motor y no hay dónde intervenir.

## S10 — AttributeError: Can't get attribute '_lookup_girl' (save de OTRO juego, vía Ren'Py Sync)

- **Estado:** ⚠️ **DOCUMENTADO — sin fix, pero requiere DECISIÓN de producto**
- **Veces:** 1 — `Thu Jul 30 16:27:23 2026` · Geo: Montevideo, Uruguay
- **Versión:** 0.1.8f · **Web (Emscripten)**
- **Clave:** `AttributeError|Can't get attribute '_lookup_girl'`
- **Impacto:** el jugador **no puede cargar su partida**. No es un crash de
  gameplay: es pérdida de acceso al progreso guardado.
- **Traceback (cola):**
```
  File "renpy/common/00action_file.rpy", line 499, in __call__
    renpy.load(fn)
  File "renpy/loadsave.py", line 636, in load
  File "renpy/compat/pickle.py", line 280, in find_class
AttributeError: Can't get attribute '_lookup_girl' on <StoreModule object>
```

#### 🔎 Diagnóstico

El jugador tocó "Cargar" y el **unpickle falló**: el save guarda una referencia
a la función `_lookup_girl`, que **ya no existe en el código**.

Es la contracara de la regla anti-PicklingError del proyecto: cuando un callable
queda dentro de un objeto que se guarda, el save no almacena la función sino su
**nombre**. Si después se renombra o elimina, los saves viejos dejan de cargar.

**Investigación:**
- `_lookup_girl` **no existe hoy** en `game/`.
- **Nunca existió en el historial de git** (21 commits desde 2025-10-15).
- **No aparece** en los 292 reportes viejos (0.1.7 / 0.1.8a).

**Descartado que sea un save viejo del propio juego:** el juego se publicó por
primera vez hace ~3 meses, o sea que TODAS las versiones publicadas están dentro
del historial del repo. Un save de "antes del repo" no puede existir en la calle.

**CAUSA REAL: el save es de OTRO JUEGO, importado por Ren'Py Sync.**

`config.has_sync` viene en `True` por defecto (lo pone `00sync.rpy:41`), así que
el menú muestra los botones "Upload/Download Sync". Al bajar un sync, Ren'Py
valida que sea del mismo juego... **pero no aborta si no lo es**:

```python
# renpy/common/00sync.rpy:356-368
if not valid:
    report_error(_("The sync belongs to a different game."))
    # <-- NO hay return: la ejecucion sigue

for fn in zf.namelist():
    ...  # importa los archivos igual
```

Y `report_error()` solo hace `renpy.call_screen("sync_error", ...)`: muestra el
cartel y **vuelve normalmente**, no corta nada.

Es un descuido claro de Ren'Py: **todos** los demás chequeos de esa misma función
(`check_sync_id`, error de descarga, fallo de descifrado, nombre de archivo
inválido) hacen `report_error(...)` **seguido de `return`**. Solo a este le falta.

**Resultado:** el jugador bajó un sync ajeno, vio el cartel "The sync belongs to a
different game", lo cerró — y los saves del otro juego se importaron igual,
pisando sus slots. Al cargar uno, aparece `_lookup_girl`, que es de ESE juego.

El propio prompt de Ren'Py delata que conocen el riesgo: *"Never enter a sync ID
you didn't create yourself"*.

#### ⚖️ Opciones y daño colateral

| Opción | Efecto | Daño colateral |
|---|---|---|
| **Desactivar sync** (`config.has_sync = False`) | Elimina el vector: sin botones de sync, nadie puede importar saves ajenos | **Bajo-medio.** Los jugadores pierden pasar partidas entre dispositivos. En web es útil (el almacenamiento del navegador es frágil), pero hoy es también la única vía conocida de destrucción silenciosa de saves |
| **Stub** `def _lookup_girl(...)` | El unpickle resolvería el nombre | **Inútil y peligroso.** El save es de OTRO juego: aunque cargara, todo su contenido es ajeno. Y habría que stubbear cada símbolo del otro juego, uno por uno |
| **Mensaje claro al fallar la carga** | El jugador entiende que ese save no es cargable | **Bajo.** Es UX, no lógica |
| **No hacer nada** | El jugador pierde sus slots pisados | Cero técnico, muy malo en experiencia |

**Recomendación: desactivar el sync** mientras el juego esté en alfa. El
beneficio (mover partidas entre dispositivos) no compensa que un jugador pueda
**destruir sus propios saves** con un código equivocado, y que además el aviso de
Ren'Py no impide la importación.

**Descartado el stub:** no es un save viejo nuestro sino de otro juego. Aunque
lograra cargar, el contenido sería ajeno por completo.

#### ✅ DECISIÓN (2026-07-30): el sync queda ACTIVO

Se evaluó desactivarlo y **se decidió mantenerlo**. La utilidad de mover partidas
entre dispositivos —especialmente en web, donde el almacenamiento del navegador
es frágil— pesa más que un caso aislado de importación cruzada.

**Consecuencia asumida:** un jugador que ingrese un sync ID ajeno puede pisar sus
propios slots, y el aviso de Ren'Py no lo impide. Es un riesgo conocido y
aceptado, no un pendiente.

**Cómo reconocerlo si vuelve a aparecer:** un `AttributeError: Can't get
attribute 'X'` dentro de `renpy.load` → `pickle.find_class`, donde `X` **no
existe en nuestro código**. Eso es siempre un save ajeno, no un bug del juego.

**Qué decirle al jugador afectado:** los slots con saves ajenos no se pueden
cargar y hay que borrarlos (desde el menú de Cargar, con `save_delete` sobre el
slot). Sus partidas propias que no hayan sido pisadas siguen funcionando.

**No es reportable a Sentry como bug nuestro** — conviene ignorar esta firma al
triagear.

## S11 — Exception: Possible infinite loop (en partida real)

- **Estado:** ⚠️ **DOS PROBLEMAS DISTINTOS con la misma firma** — el de la
  precarga está **CORREGIDO**; el del `game_loop` sigue **sin localizar**
- **Veces:** 2 eventos, en **dos lugares completamente distintos**:
  - `Thu Jul 30 20:14:34` — `intro_main.rpy:590` (**game_loop**), partida real:
    `loc=casa_pasilloabajo`, día 9, de noche. Geo: Marseille, Francia.
  - `Fri Jul 31 15:05:39` — `intro_main.rpy:587` (**game_loop** otra vez),
    partida MUY avanzada: `loc=casa_hmc`, **día 36**, de mañana, lunes.
    Geo: Varaždin, Croacia.
  → Los dos del game_loop: **SIN LOCALIZAR**, ver instrumentación abajo.
  - `Fri Jul 31 00:12:03` — `pantalla_carga.rpy:179` (**precarga del splash**),
    partida nueva: `loc=?`, `dias_totales=1`. Geo: Seneca, EE.UU.
    **✅ LOCALIZADO Y CORREGIDO** (ver abajo).
- **Versión:** 0.1.8f · Web
- **Clave:** `Exception|Possible infinite loop`
- **Contexto (tags):** `loc=casa_pasilloabajo`, `dias_totales=9`,
  `horario_actual=2` (noche), `dia_semana_actual=1` (martes)
- **Traceback:**
```
  File "//game/script/characters/mc/quests/intro_main.rpyc", line 590, in script
  File "renpy/execution.py", line 62, in check_infinite_loop
Exception: Possible infinite loop.
```

#### ⚠️ Por qué este importa más que los anteriores

**No es de la familia del renderer.** Los tags muestran una partida real y
avanzada: día 9, de noche, en el pasillo de abajo. Es un bug de gameplay que le
pasó a alguien que venía jugando bien.

#### 🔎 Qué significa

`check_infinite_loop` (execution.py:45) cuenta statements: si se ejecutan
**1000 sin ninguna interacción** que resetee el temporizador, lanza la excepción.
Es una red de seguridad — sin ella el juego se habría **colgado**.

La línea 590 es donde el contador llegó a 1000, **no necesariamente donde está el
bucle**. Cae dentro de `game_loop` (línea 590 de 0.1.8f ≈ 598 actual, en los
chequeos de quests).

O sea: algo hace que el `game_loop` dé decenas de vueltas **sin llegar nunca al
`pause`**, que es lo único que cede el control al jugador.

#### ✅ Descartado (verificado)

El `game_loop` tiene **4 disparadores** que hacen `jump` antes del `pause`. Los
cuatro **limpian su propia condición**, así que ninguno cicla por sí solo:

| Disparador | Cómo corta el ciclo |
|---|---|
| `violet_quest09a_piensa_avisarle` | `$ store.violet_9a_piensa_mostrado = True` como 1er statement |
| `quest_jasmine_questprincipal_0_b` | `$ store._jasmine_0b_iniciada = True` antes del jump |
| `mc_q0_exploracion_completada` | `$ mc_q0_explorando = False` |
| `mc_q0b_trigger` | `$ mc_q0b_disparada = True` |

También descartado:
- **`renpy.jump()` desde Python**: los 4 que hay (shopping_system) van a
  `mostrar_mensaje_uso_item`, que muestra diálogo — o sea, interactúa.
- **`validar_eventos()`**: solo cambia estados y llama callbacks de Python; no
  ejecuta labels ni salta.

#### ❓ Qué falta para localizarlo

No se puede ubicar el bucle con un solo traceback: el guard reporta dónde cayó el
contador, no el ciclo. Datos que lo resolverían:

1. **¿Se repite?** Si el jugador queda trabado y vuelve a pasar, el contexto
   (locación / horario / día) acota mucho.
2. **¿Otros reportes con la misma firma?** Si todos comparten `loc` u `horario`,
   eso apunta al disparador.
3. **Feedback del jugador:** ¿qué estaba haciendo justo antes? Un bucle en el
   game_loop suele arrancar tras una acción concreta.

**Sin fix por ahora:** no se puede arreglar lo que no está localizado, y tocar el
`game_loop` a ciegas es de alto riesgo — es el corazón del juego y un cambio mal
puesto ahí afecta a todas las partidas.

**Prioridad si vuelve a aparecer: ALTA.** A diferencia de la familia de GL (que
afecta a dispositivos que no pueden correr el juego igual), este le pasa a
jugadores con partidas avanzadas y en curso.

#### ✅ El de la PRECARGA: localizado y corregido (2026-07-31)

El segundo evento cayó en `pantalla_carga.rpy:179`, dentro del bucle de precarga
— **no en el game_loop**. Ahí sí se pudo reconstruir el mecanismo exacto:

```renpy
while _carga_idx < _carga_total:          # ~115 lotes (691 imgs / 6)
    ...
    while not carga_lote_terminado() and _carga_espera < 40:
        $ _carga_espera += 1              # <- linea 179
        pause 0.01
```

**No es un bucle infinito de verdad:** `carga_encolar_lote()` siempre avanza
(`min(desde+6, len)`), así que termina. El problema es el **volumen**: ~115 lotes
× hasta 40 vueltas del busy-wait ≈ **10.000 statements**, contra un guard que
salta a los 1000.

**Por qué los `pause 0.01` no alcanzaban:** el guard exige DOS condiciones —
1000 statements acumulados **y** ~50 s desde el último frame de interacción. Y
el contador `il_statements` **no se resetea con las interacciones**, solo al
llegar a 1000 (`execution.py:45-58`). En web basta con que el jugador **cambie de
pestaña mientras carga** (el navegador congela los frames) para que se cumpla
también la condición de tiempo.

**Arreglo:** `$ renpy.not_infinite_loop(30)` al inicio de cada vuelta del bucle
externo. Es la API que Ren'Py expone exactamente para esto: declarar que un
bucle largo es intencional.

**Daño colateral: nulo.** Solo corre el temporizador del detector; no cambia la
precarga, ni el orden, ni los tiempos. Solo evita que Ren'Py confunda un trabajo
legítimo con un cuelgue.

**Auditados los demás `while` del proyecto:** el resto son de Python (dentro de
funciones, no cuentan statements de script) o cortos con diálogo en el medio
(`despertar_system.rpy:134`, que interactúa en cada vuelta). Solo la precarga
estaba en riesgo.

#### 🔬 El del GAME_LOOP: instrumentado (2026-07-31)

Con dos reportes, **ningún contexto compartido**:

| | Reporte 1 | Reporte 2 |
|---|---|---|
| Locación | `casa_pasilloabajo` | `casa_hmc` |
| Día | 9 | 36 |
| Horario | noche | mañana |
| Geo | Francia | Croacia |

Y los **4 disparadores del game_loop limpian su condición** (verificado dos
veces), así que ninguno debería ciclar. No se puede deducir de los tracebacks:
el guard reporta dónde llegó a 1000 el contador, no dónde está el ciclo.

**NO se aplicó `not_infinite_loop()` acá — a propósito.** En la precarga era
correcto porque el bucle es legítimo y acotado. En el game_loop **no hay ningún
bucle que justifique 1000 statements**, así que probablemente haya un ciclo real:
silenciar el guard convertiría "mensaje de error" en **juego colgado**, que es
peor. El guard está haciendo su trabajo.

**En vez de eso, se instrumentó:**
- `_gl_ultimo_trigger` guarda cuál de los 4 disparadores hizo el último `jump`.
- Se limpia al llegar al `pause` (vuelta completada sin ciclar).
- Viaja a Sentry como tag **`gl_trigger`**.

Así el próximo reporte dice **qué estaba ciclando**:
- Tag con valor → ese disparador es el culpable, y se ataca directo.
- Tag vacío o ausente → el ciclo NO viene de los 4 disparadores, y hay que
  buscar en labels externos que terminen en `jump game_loop`.

**Daño colateral: nulo.** Son 5 asignaciones de string; no cambian ninguna
condición ni flujo.

**Prioridad: ALTA.** Es el único error activo que le pega a jugadores con
partidas en curso (día 9 y día 36) — no a dispositivos que no pueden correr el
juego de ninguna forma.
