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
| 15 | 9 (S01, S02, S03, S05, S08, S12, S13, S14, S15) | 6 (familia GL: S04/S06/S07/S09 · S10 sync · **S11 game_loop: sin localizar** — la variante precarga de S11 quedó cerrada el 2026-09-17) |

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

**Reverificado el 2026-09-16** contra un traceback real de Ren'Py web con su
bloque de metadata: `_jp_sentry_parse` devuelve `('TypeError', "'int' object is
not callable")` y el mismo error con otra fecha da el **mismo** fingerprint. El
arreglo sigue en pie; el agrupamiento por issue separado no vuelve a pasar por
esta causa. (Si un mismo error se ve todavía en dos issues, mirar el *mensaje*:
un valor variable adentro del texto de la excepción —una ruta, un id— sí parte
el grupo, y para eso está la normalización de `_jp_sentry_fingerprint`, que hoy
sólo aplana direcciones de memoria y números de 4+ dígitos.)

---

## 🔧 Nota de herramienta — jugador y controlador en los reportes (2026-09-16)

Los tres canales (Discord de errores, Discord de feedback y Sentry) mandan ahora
dos datos más:

- **Jugador** — `jp_jugador_actual()` (sistema_reporte_errores.rpy): el nombre
  que eligió el jugador, con `(tester)` cuando la partida corre en `MODO_DEV`.
  Sirve para saber de quién es cada reporte sin preguntarlo. En Sentry va como
  **tag** `jugador`, nunca en el fingerprint: identifica al que reporta sin
  partir en dos el agrupamiento de un mismo error.
- **Controlador** — `planificador_reporte()` (core/quests/planificador.rpy), vía
  `jp_controlador_actual()`: la restricción activa (dueño, reloj, acciones
  bloqueadas, locaciones permitidas, NPCs ocultos, celular), las reservas
  vigentes y, por cada quest viva, cómo la ve el controlador (`espera para
  nacer (detrás de X)` / `en narrativa` / `disponible` / `interrumpida
  (motivo)`). Es lo que hacía falta para reconstruir una traba como E10 o E11
  sin tener la partida. En Sentry va como **extra** (`controlador`), no como
  tag: es multilínea y no debe influir en el agrupamiento.

Las dos funciones son a prueba de fallos (corren dentro del handler de errores) y
tienen tope de líneas; en el reporte de Discord el bloque del controlador se
recorta a 600 caracteres y el traceback se ajusta a lo que queda libre.

## 🔧 Nota de herramienta — id de instalación: Sentry ya puede contar personas (2026-09-23)

Hasta ahora **todos los issues decían "Users Impacted: 0"**: el evento no
llevaba ningún `user`, así que Sentry contaba eventos pero no gente. En la
revisión del 2026-09-23 eso costó trabajo real — 46 eventos de tres issues
había que cruzarlos por país y navegador para descubrir que eran **un solo
jugador** insistiendo, no cuarenta y seis personas.

**`jp_instalacion_id()`** (sistema_sentry.rpy) devuelve un `uuid4` de 12
caracteres hex, generado en la máquina del jugador la primera vez y guardado en
`persistent`. Va como `user.id` en el evento de Sentry y como línea
**Instalación** en los dos reportes de Discord (error y feedback) — con el mismo
id en los tres canales, un feedback se puede cruzar con los crashes que esa
misma instalación mandó.

Qué es y qué no es: un número al azar. No sale de ningún dato de la persona, no
viaja con nada más y no sirve para reconocerla en otro lado. Borrar los datos
del navegador (web) o el persistent (escritorio) lo cambia por otro, y está
bien: identifica **una instalación**, no a alguien.

Si `persistent` no está disponible (puede pasar en web en la primera escritura)
cae a un id de sesión con prefijo `sesion_`, que avisa de un vistazo que ese no
sobrevive al reinicio.

---

## 📋 Revisión del 2026-09-23 (Sentry conectado por MCP)

25 issues sin resolver, que son tres cosas:

| Issue | Qué | Estado |
|---|---|---|
| `PYTHON-4R0` + `PYTHON-4QZ` + `PYTHON-4R1` | 46 eventos, **un jugador** (El Cairo, Chrome 152, web 0.1.9.1) con `renderer: ?`. Cascada: `Could not set video mode` → display en None → revienta el `pause` → y al entrar al menú, el `take_screenshot`. Es S04/S07/S09. | **El cartel de WebGL ya existe** (patch del `index.html` del SDK, 18/09) pero la build publicada es anterior. Se cierra al republicar. |
| `PYTHON-4QY` | 8 eventos, otro jugador (Canadá, Chrome 153, `renderer: gles2` — este sí tiene WebGL). `Possible infinite loop` en la precarga: es **S11**. | Arreglado en el working tree (el bucle en un solo bloque `python:`), sin publicar. |
| 20 issues del 28/08 con título de timestamp (`Error: Fri Aug 28 15:51:07 2026`) | El agrupamiento roto de antes del fix de fingerprint: un mismo error partido en veinte. | Ruido histórico. |

`PYTHON-4R8` (traducción duplicada de "Esperar") era de una corrida de lint en
la máquina de desarrollo: llegó con `environment: dev`, que es exactamente para
lo que se puso ese tag.

**La conclusión de la revisión:** los dos problemas que están tocando a
jugadores ya tienen el arreglo escrito. Lo que los cierra no es más
diagnóstico — es publicar una build.

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
- **Reincidencia 2026-09-18:** `Fri Sep 18 07:24:47` (0.1.9.1, Trois-Rivières,
  CA, Chrome 151 con `Norton/1`), en `pantalla_carga.rpy:153` (el `pause 2.0`
  del logo) tras tocar "Ignore" al S07 de dos segundos antes. Misma sesión que
  el S09 de las 07:26:25: S07 → S04 → S09, un dispositivo, tres firmas.
  Cubierto por el cartel sin WebGL del 18/09 (ver S09).
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
- **Veces:** 2 — `Thu Jul 30 17:17:38 2026` (0.1.8f, escritorio) ·
  `Fri Sep 18 09:59:28 2026` (0.1.9.1, **Firefox 156 en Android 15**, Omaha,
  US, jugador "Mc", **día 11, en partida** — `renderer=gles2`, o sea que el
  renderer había andado once días; murió al recompilar los shaders en un
  `on_resize`). Es el subgrupo que el cartel sin WebGL del 18/09 **no cubre**.
  Hipótesis a vigilar: en móvil el `height: 100dvh` del patch hace que cada
  aparición/desaparición de la barra del navegador redimensione el canvas, y
  cada resize recompila shaders — más oportunidades de fallo que en escritorio.
  Si aparece un tercero en móvil, medir antes de tocar el patch (el dvh arregla
  un problema real en 3 de 4 teléfonos).
- **Versión:** 0.1.8f, 0.1.9.1 · **Web (Emscripten)**
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

- **Estado:** 📋 **DOCUMENTADO — mismo incidente que S06/S04, sin fix.**
  Reincidió el 2026-09-17; decisión de ese día para toda la familia GL:
  **ignorar** (ver S09).
- **Veces:** 3 — `17:17:57` (incidente A) y `14:45:20` (incidente C, Miami),
  ambos 0.1.8f; en C fue el **primer** error de la sesión, en
  `pantalla_carga.rpy:152`. Y `Thu Sep 17 20:59:20 2026` (0.1.9.1, Santana do
  Livramento, BR, Chrome 152, jugador nuevo, `renderer=?`), otra vez en
  `pantalla_carga.rpy:152` — el `with dissolve` del logo, la primera línea que
  dibuja. Y `Fri Sep 18 07:24:45 2026` (Trois-Rivières, CA, Chrome 151 con
  `Norton/1`): **la misma sesión** que el S09 de las 07:26:25 — primero este
  al dibujar el logo, después el `screenshot` al entrar al menú tras "Ignore".
  Un dispositivo, dos firmas. Cubierto por el cartel sin WebGL del 18/09 (S09).
- **Versión:** 0.1.8f, 0.1.9.1 · **Web (Emscripten)**
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

- **Estado:** 📋 **DOCUMENTADO — misma familia que S04/S06/S07, sin fix.**
  Reincidió el 2026-09-17 y se decidió **ignorarlo** (ver abajo).
- **Veces:** 3 — `Thu Jul 30 14:58:07 2026` (0.1.8f, Estados Unidos) ·
  `Thu Sep 17 18:55:51 2026` (0.1.9.1, Helsinki, Chrome 152, jugador nuevo sin
  nombre, `renderer=?`) · `Fri Sep 18 07:26:25 2026` (0.1.9.1, Trois-Rivières,
  CA, Chrome 151 con `Norton/1` en el user-agent, jugador nuevo, `renderer=?`).
  Con el S07 de Brasil del 17, son **tres dispositivos distintos sin WebGL en
  36 horas**, todos Chrome actual — el umbral que se había fijado para
  reabrir el chequeo de WebGL en el `index.html`. **Aplicado el 2026-09-18**
  (ver abajo).
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

#### 🔁 Reincidencia (2026-09-17) y decisión

Segundo evento, en 0.1.9.1: Helsinki, Chrome 152 (navegador actual, o sea
dispositivo o configuración — típicamente Chrome con la aceleración por hardware
apagada), jugador nuevo en su primera entrada al menú. El tag `renderer=?`
confirma que ningún renderer llegó a inicializar en esa sesión (Ren'Py lo
escribe recién cuando `draw.init()` tiene éxito, `core.py:1266`).

Se evaluaron dos cosas que no tocan el motor: un tag `familia=gl_dispositivo`
para archivar los cuatro fingerprints juntos en Sentry, y un chequeo de WebGL
en el `index.html` del SDK (dentro de `web/patch_index_movil.py`) que muestre
un cartel HTML antes de cargar el juego. La decisión del 17 fue ignorarlo; al
día siguiente, con el tercer dispositivo en 36 h, se aplicó el cartel.

#### 🔨 Cartel sin WebGL (2026-09-18) — `web/patch_index_movil.py`, patch 4

El `<script async src="renpy.js">` del template pasa a un script inline que:
(1) espera a que `document.visibilityState` no sea `hidden` (un arranque en
una pestaña restaurada en segundo plano puede no recibir contexto de GL — la
hipótesis de Alan sobre S07 de Brasil); (2) prueba `getContext('webgl2' /
'webgl' / 'experimental-webgl')` en un canvas **aparte** (probar sobre
`#canvas` le robaría el contexto al motor: un canvas admite un solo tipo de
contexto); (3) si hay, inyecta `renpy.js`; si no, esconde el presplash y
muestra un cartel HTML bilingüe (activar aceleración por hardware, desactivar
extensiones/modos de privacidad, otro navegador, versión de escritorio) con
"Reintentar" e "Intentar igual". Es lo único que puede llegarle a ese jugador:
pasa antes de que Ren'Py exista. Cubre el subgrupo "sin WebGL" (S07, S09); no
cubre "murió al redimensionar" (S04, S06), que sigue sin fix.

Aplicado al template del SDK (idempotente, se reaplica con el mismo comando al
actualizar Ren'Py). **Hace falta rebuildear web** para que salga. Si el
chequeo se equivocara, lo peor es el cartel a alguien que sí tenía WebGL, y
para eso está "Intentar igual".

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
  precarga está **CORREGIDO (de verdad) el 2026-09-17**, ver abajo; el del
  `game_loop` sigue **sin localizar**. Desde el 2026-09-17 el fingerprint de
  esta excepción lleva el archivo del juego, así que en Sentry ya salen como
  dos issues (`pantalla_carga` / `intro_main`).
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

#### 🔁 Reincidencia de la variante precarga (2026-09-17) y arreglo definitivo

`Thu Sep 17 07:16:07 2026`, 0.1.9.1 web, España, `dias_totales=1`,
`jugador=(sin nombre)`: un jugador nuevo en su primera carga,
`pantalla_carga.rpyc:192` (la `pause 0.01` del busy-wait). **Con el
`not_infinite_loop(30)` de julio puesto.** Y otra vez `Sun Sep 20 19:30:11`
(Opera 135, Lima, PE), mismo archivo, misma línea, mismo perfil: jugador nuevo,
primera carga. **Tres eventos en total de esta variante** (0.1.8f, y dos en
0.1.9.1) — no es una rareza de un dispositivo, le pasa a cualquiera que deje la
pestaña quieta mientras carga.

Por qué no alcanzó: cada `pause` del bucle vuelve a fijar el plazo del watchdog
en 50 s — `il_time = time.time() + delay` es una asignación, no un máximo — así
que el plazo real era siempre "50 s desde el último frame". Y la ventana que
quedaba: el navegador **congela** la pestaña (segundo plano largo, minimizar, la
máquina que se duerme); al volver, la `pause` en curso termina con el plazo ya
vencido, y los **tres statements** que van hasta la siguiente `pause` corren sin
refresco. Si el contador cruza el 1000 justo ahí, salta. Lotería de ~0,3 % por
congelamiento: dos eventos en dos meses.

**Arreglo:** el bucle entero pasó a **un solo bloque `python:`** con
`renpy.pause(0.01)` adentro. El watchdog cuenta statements de Ren'Py; un bloque
Python es UN statement, dé las vueltas que dé, así que el contador no se mueve y
no hay 1000 que cruzar. Misma precarga, mismo orden, mismo contador en pantalla.
Regla: **un bucle largo de script va en Python, no en statements de Ren'Py** —
`not_infinite_loop` es un parche que cualquier interacción pisa.

#### ❓ Qué falta para localizarlo (la variante del game_loop)

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

---

## S12 — AttributeError: Can't get attribute 'condicion_aparicion_evento01_violet' (no abre un save viejo)

- **Estado:** ✅ **CORREGIDO (2026-09-16)**
- **Veces:** 1 — `Tue Sep 15 18:51:54 2026`, jugador real (Rawalpindi, PK), Windows 11
- **Release:** 0.1.9.1 · **loc:** casa_cocina · día 2, mañana · `quest_activada`: violet_questprincipal_0_a
- **Fingerprint:** `AttributeError | Can't get attribute 'condicion_aparicion_evento01_violet' on <StoreModule object at 0xADDR>` (agrupó bien, con la dirección normalizada)

```
File "renpy/loadsave.py", line 636, in load
    roots, log = loads(log_data)
File "renpy/compat/pickle.py", line 280, in find_class
    return super().find_class(module, name)
AttributeError: Can't get attribute 'condicion_aparicion_evento01_violet' on <StoreModule object>
```

#### 🔎 Diagnóstico

El jugador estaba **jugando** (el frame de arriba es el `pause` del game_loop),
abrió Cargar y tocó un slot: `FileLoad.__call__` → `renpy.load` → el unpickle
del save falló.

Un save guarda por **referencia** las funciones de módulo que quedan dentro de
objetos guardados: `Event.condicion_aparicion/activacion`, los textos callables
de `ConfigEtapa`, `ConfigFallo.condicion`, `EstadoTalk.condicion`,
`Skin.condicion_desbloqueo`, `GrupoMensajes.condicion/accion_al_completar`. El
pickle no guarda el código: guarda `store` + el **nombre**. Al cargar, el
unpickler hace `getattr(store, nombre)`.

`condicion_aparicion_evento01_violet` era la condición del evento del casco de
realidad virtual, **borrado en 0.1.8.6** (commit 309f03b, 2026-08-20). Cualquier
save que tenga ese evento en `sistema_events` —o en su log de rollback— pide ese
nombre al abrirse, no lo encuentra y revienta.

**Por qué el control de generaciones no lo frenó:** `compatibilidad_saves.rpy`
decide si una partida se puede *seguir jugando*, y corre en `after_load`, o sea
**después** de cargarla. El unpickle pasa antes que cualquier código nuestro, así
que un nombre faltante se lleva puesto el juego incluso cuando esa partida se iba
a rechazar igual.

#### 🔨 Arreglo

`game/script/core/utils/compat_nombres_muertos.rpy` (nuevo): una lista de los
nombres borrados o renombrados desde la 0.1.8f, declarados en `init -100` como
un stub inerte que devuelve `""` (sirve de condición —falsy, el contenido muerto
no aparece— y de texto —no dibuja nada—). Solo se declara lo que hoy no existe,
así que un nombre que volvió al código sigue mandando.

Con eso el save **abre siempre**: si es de una generación vieja, el rechazo sale
prolijo por `after_load` → `jp_save_incompatible`; si es de la generación actual
(0.1.9 / 0.1.9a, que sí referencian varias funciones borradas después), se sigue
jugando normal.

La lista salió de comparar los `def` de cada release publicada contra los de hoy:

```
git ls-tree -r --name-only <rev> game/script/   → defs de esa rev
menos las defs de hoy                            → candidatas a stub
```

54 nombres, entre ellos los del sistema de espiar, los helpers de las líneas de
amor/deseo previas al rediseño, el tutorial de exploración del MC y las piezas
del motor que retiró el controlador de quests.

#### 💡 Regla

**Al borrar o renombrar una función de módulo que pueda haber quedado guardada,
su nombre viejo va a `JP_NOMBRES_MUERTOS`.** Es la contracara de la regla
anti-PicklingError: esa dice que los callables guardados deben ser funciones de
módulo; ésta dice que esas funciones no se pueden borrar sin dejar el nombre
atendido.

---

## S13 — Exception: TransitionAnimation.render() must return a Render (ducha de la 08_a)

- **Estado:** ✅ **CORREGIDO (2026-09-17)** — causa raíz encontrada el 18/09
  con el segundo evento (ver abajo); el fix la cubre.
- **Veces:** 3, **tres jugadores distintos en 40 horas** — `Thu Sep 17 15:26:16`
  (web, Chrome 109, Kharkiv UA, "Oleg", día 95) · `Fri Sep 18 09:48:17` (web
  **móvil**, Android 10 + Chrome 153, Leechburg US, "Mc", día 82) ·
  `Sat Sep 19 01:36:51` (web, Opera 135, US, "Mc", día 92). Los tres en
  `loc=casa_pasilloarriba`, `quest_activada=violet_questprincipal_08_a`, y los
  tres en las **dos primeras líneas** de `violet_quest08a_entrar_baño` (fuente
  396 y 397): los primeros `piensa` después de los `show` de las capas de agua
  — o sea, **los primeros frames** de la animación. Navegadores y dispositivos
  todos distintos: no es de dispositivo, es del código.
- **Controlador (extra):** restricción de la 08_a (solo baño y pasillo, NPCs
  ocultos, celular bloqueado), reserva de Violet día 95 h0, 08_a en narrativa.
  → **La escena de la ducha de la noche de la tormenta.**
- **Fingerprint:** `Exception | <renpy.display.anim.TransitionAnimation object at 0xADDR>.render() must return a Render.`

```
File "//game/tl/english/script/characters/violet/quests/violet_quest_08_a.rpyc", line 397, in script
  ... display_say → render_screen → layout → transform → image → transform →
File "renpy/display/render.pyx", line 274, in renpy.display.render.render
Exception: <renpy.display.anim.TransitionAnimation object at 0x3e24620>.render() must return a Render.
```

#### 🔎 Diagnóstico

La línea 397 es del archivo de **traducción**: `piensa "I don't know if coming
in like this was the best option"`, el primer pensamiento de
`violet_quest08a_entrar_baño`, justo después de `show` de las cuatro capas de
agua. El árbol de render (`ImageReference → Transform → TransitionAnimation`)
es exactamente la definición de esas capas en `core/events/generics.rpy`:
`image ducha_agua_* = Transform(Animation(9 frames × 0.05), alpha=0.3)`.

`Animation()` es la API legacy de Ren'Py: por debajo construye un
`TransitionAnimation`, cuyo `render()` hace `t = at % sum(delays)` y después
recorre los frames restando el tiempo de cada uno; si ninguno "atrapa" a `t`,
**se cae del bucle y devuelve None**.

**Causa raíz (encontrada con el segundo evento, 2026-09-18).** El primer
diagnóstico decía que solo un tiempo NaN/infinito podía provocarlo — era
incompleto. Los dos eventos cayeron en **el primer frame** de la animación, y
eso apuntaba a un valor determinístico, no a un reloj roto. Es este:

```
at = -1e-17                      # animación recién mostrada: un epsilon NEGATIVO
t  = at % 0.44999999999999996    # Python redondea: t == sum(delays) EXACTO
t - 9 × 0.05 = 1.4e-17  →  ningún frame lo atrapa  →  return None
```

Un `at` negativo minúsculo en el primer render (el tiempo de animación sale de
`frame_time - show_time`, y en web el reloj puede leerse un instante antes de
la marca del `show`) hace que el módulo devuelva `sum(delays)` mismo, y el
bucle no está preparado para `t == sum`. Verificado con una traza: `-1e-17`
cae; `-1e-16`, `-0.0` y `-1e-12` no. Por eso pasa solo en algunos navegadores
y solo al mostrar: depende de que el reloj dé justo ese valor.

ATL no tiene el problema: con `st` negativo (o NaN) su `pause` simplemente no
se cumple y dibuja el primer frame.

#### 🔨 Arreglo

Las **ocho** animaciones hechas con `Animation()` / `anim.TransitionAnimation`
pasaron a **ATL**: las cuatro capas de agua (generics.rpy), las tres lluvias y
la Violet enjabonándose del minijuego de espiar (espiar_system.rpy). ATL siempre
dibuja el frame actual. Mismos frames, mismos tiempos, misma opacidad y
desfase; en la de Violet, el mismo ciclo de 26 frames con `Dissolve(0.5)` entre
cada uno y de vuelta al primero (verificado por script contra la lista vieja).
De paso se fue el `loop=True` que se le pasaba a `Animation()` como si fuera
una propiedad: no lo era, se ignoraba en silencio.

#### 💡 Regla

**Animaciones por frames, en ATL.** `Animation()` y `anim.TransitionAnimation`
no se usan más: tienen un camino de render que devuelve None y no hay forma de
defenderlo desde afuera.

---

## S14 — Exception: A translation for "Desbloqueos" already exists (instalación encima de una vieja)

- **Estado:** ✅ **CORREGIDO (2026-09-18)** — para este y para toda la clase
- **Veces:** 2, **dos jugadores distintos** — `Thu Sep 17 18:31:53 2026`
  (Windows 11, Saratoga, US) · `Sat Sep 19 21:28:46 2026` (Windows 11,
  Illkirch-Graffenstaden, FR). Los dos en 0.1.9.1, escritorio, mismo archivo
  viejo. Falla en init: **el juego no arranca**. Confirma que no es un caso
  aislado sino la forma normal en que la gente actualiza: descomprimir encima.
- **Fingerprint:** `Exception | A translation for "Desbloqueos" already exists at game/tl/english/relaciones_strings.rpy:<int>.`

```
File "game/tl/english/script/ui/hud/hud_relaciones.rpy", line 6, in script
    old "Desbloqueos"
File "renpy/translation/__init__.py", line 539, in add
Exception: A translation for "Desbloqueos" already exists at game/tl/english/relaciones_strings.rpy:39.
```

#### 🔎 Diagnóstico

`game/tl/english/script/ui/hud/hud_relaciones.rpy` **no existe en la 0.1.9.1**:
se borró en agosto (`d64faec`, 2026-08-13) cuando el panel de Relaciones pasó a
Hitos y sus strings se mudaron a `relaciones_strings.rpy`. Que el jugador lo
tenga en disco significa una sola cosa: **descomprimió la 0.1.9.1 encima de
una instalación de 0.1.8.x**. Los archivos nuevos pisan a los que siguen
existiendo; los que ya no vienen en el zip quedan ahí, y Ren'Py los carga como
parte del juego. Dos `translate strings` con el mismo `old` → excepción durante
init → pantalla de error antes del menú.

Es una **clase**, no un caso: cada versión que borra un archivo deja este
agujero para todo jugador de escritorio que instale encima. Hay 42 `.rpy`
borrados en la historia del repo; cualquiera de ellos en disco puede dar esto
(si traduce strings) o algo peor y silencioso (un `.rpy` viejo suelto registra
labels, screens, quests o triggers que ya no existen).

#### 🔨 Arreglo

`game/script/core/utils/limpieza_instalacion.rpy` (nuevo), en `init -999` —
antes de cualquier init del juego, y los `translate strings` corren en 0:
recorre la lista `JP_ARCHIVOS_VERSIONES_VIEJAS` (los 42, sacados de
`git log --diff-filter=D`), borra los que encuentre en disco (con su `.rpyc`) y,
si borró alguno, hace `renpy.utter_restart()`: bootstrap.py atrapa la
excepción y recarga Ren'Py entero, ya sin el archivo. El jugador ve un
parpadeo en el arranque. Solo se reinicia si se borró algo, así que no puede
quedar en bucle; si un borrado falla por permisos, se saltea y el juego sigue
como pudo.

Solo en escritorio Windows/Linux y **nunca con `config.developer`** (jamás
borrar del working tree). Web, mac, android e iOS reemplazan el paquete
entero y no aplican. Verificado headless con un archivo viejo simulado: en
developer no borra; sin developer borra `.rpy` y `.rpyc`.

#### 💡 Regla

**Al borrar un `.rpy` del proyecto, su ruta va a `JP_ARCHIVOS_VERSIONES_VIEJAS`.**
Y en las notas de itch, la línea de siempre: *borrá la carpeta anterior antes de
descomprimir* — el arreglo cubre lo que ya despachamos, la nota evita el resto.

---

## S15 — KeyError: 'size=+8' (el aviso de "Partida incompatible" nunca se pudo mostrar)

- **Estado:** ✅ **CORREGIDO (2026-09-20)**
- **Veces:** 1 — `Sat Sep 19 02:35:23 2026`, web (Edge 153), Curitiba, BR,
  jugador "Stark", día 19, `loc=casa_hmc`. Con su derivado (`NameError:
  _jp_aviso`, 02:35:35, fingerprint aparte) son 2 eventos de la misma sesión.
- **Fingerprint:** `KeyError | 'size=+<int>'`

```
File "//game/script/core/time/despertar_system.rpyc", line 112, in script call
File "//game/script/core/utils/compatibilidad_saves.rpyc", line 219, in script
File "game/script/core/utils/compatibilidad_saves.rpy", line 226, in <module>
    ).format(version=config.version)
KeyError: 'size=+8'
```

#### 🔎 Diagnóstico

El jugador cargó una partida de otra generación de guardado, el control de
compatibilidad hizo lo suyo (`after_load` → `jump jp_save_incompatible`) y…
**el aviso reventó al armarse**. El texto empieza con el tag de Ren'Py
`{size=+8}`, y `str.format()` lee `{size=+8}` como un campo: `KeyError`.

O sea: **ese mensaje nunca se mostró, en ningún idioma, desde que existe**
(0.1.8.5). Todo jugador que cargó una partida incompatible vio la pantalla roja
de error en vez de "Partida incompatible · volvé a instalar la versión con la
que la creaste". La ironía es que el control funcionaba perfecto; lo que
fallaba era el cartel que lo explica.

El frame de `despertar_system` es la pila de llamadas restaurada del save (la
partida se había guardado dentro del flujo de despertar), no la causa.

#### 🔨 Arreglo

`.format(version=...)` → `.replace(u"{version}", ...)`. Escapar las llaves
(`{{size=+8}}`) habría obligado a tocar el `old` de la traducción; `replace` no
le pide nada al texto y no puede confundirse con un tag.

#### 🔁 Detector

Chequeo 7 nuevo en `tools/validar_traducciones.py`: recorre las 51 llamadas
`translate_string(...).format(...)` del proyecto y, para **cada una en los dos
idiomas**, parsea el texto con `string.Formatter` y avisa si algún campo tiene
`=` o empieza con `/` — o sea, si es un tag de Ren'Py. El doble idioma importa:
una traducción puede traer un tag que el original no tenía, y ahí el crash
saldría **solo en inglés**. Corrido sobre el proyecto: era el único caso, en
los dos idiomas.

#### 🔁 El error derivado (mismo jugador, 12 segundos después)

`Sat Sep 19 02:35:35` — `NameError: name '_jp_aviso' is not defined`
(fingerprint propio, evento `6147d11c`). El jugador tocó "Ignore" al KeyError,
la ejecución siguió en la línea de abajo (`centered "[_jp_aviso]"`) y la
variable nunca se había asignado. Es el mismo patrón que S08 (`_nc_nombre` /
`_jugar_intro` tras "Ignore"), y la respuesta es la misma: **`default
_jp_aviso`** con un texto plano de respaldo — sin tags y sin placeholder, o sea
que no puede fallar al mostrarse. Así, si algún día el bloque que arma el aviso
completo vuelve a romperse, el jugador ve el mensaje corto en vez de un segundo
error. Traducido al inglés.

#### 💡 Regla

Es la hermana de la del `%` (ver `japitown-warnings` D2): **texto con tags de
Ren'Py no pasa por `.format()` ni por `%`**. Si hay que interpolar, `replace`.
Y, como en S08: **toda variable que un `python:` asigna y la línea siguiente
muestra lleva `default`** — "Ignore" hace que la ejecución siga, y sin el
`default` el error se duplica.

