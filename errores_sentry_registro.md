# Registro de errores — Sentry

> Errores capturados por **Sentry** (integración en `sistema_sentry.rpy`), a partir
> de 0.1.8b. Distinto de `errores_registro.md` (que era el volcado manual de los
> reportes viejos de Discord).
>
> Cada entrada: estado, traceback, diagnóstico y fix. IDs con prefijo **S**.

---

## Resumen

| Errores procesados | Corregidos | Pendientes |
|---|---|---|
| 3 | 2 (S01, S03) | 1 (S02: mismo fix, falta que llegue a un build) |

> ⚠️ **Importante (S02):** todos los fixes de esta sesión están **sin commitear**
> (working tree). Si el build parte de un checkout limpio de git, no los incluye.
> Hay que **commitear (o buildear desde el working tree) y rebuildear** para que
> los arreglos lleguen a los jugadores.

---

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
