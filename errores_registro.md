# Registro de errores reportados

> Volcado de errores viejos (mayormente **0.1.7**) para triage.
> **Etapa actual: SOLO registrar.** Nada de análisis ni fixes todavía.
>
> Cada entrada es una **clase única de error**, identificada por
> `tipo de excepción + mensaje normalizado` (misma lógica de fingerprint que
> usa la integración de Sentry: se ignoran direcciones de memoria y números
> largos para que la misma clase caiga en una sola entrada).
>
> - **Veces:** cuántos reportes iguales llegaron.
> - **Contextos:** se van acumulando los distintos `loc/día/horario` observados.

---

## Resumen

| Reportes de bug (reales) | Clases únicas |
|---|---|
| ~84 | 6 (E01–E06) |

> **Reconciliación (2026-07-25):** fuentes procesadas: pastes manuales +
> `errores.txt` (60) + `errores2.txt` (86). Se solapan (todos del 25-07), así
> que **los conteos son aproximados** (no sumables). Se toma `errores2.txt`
> como dump más completo. Clases nuevas encontradas en errores2: **E05, E06**.
>
> **Aparte (no son bugs):** 2 reportes de `Exception: Error de prueba forzado
> desde el panel de cheats` — mis pruebas de Sentry (botón 💥). Excluidos.

---

## Errores

<!-- Formato de cada entrada:

### E## — <TipoExcepcion>: <mensaje corto>
- **Veces:** N
- **Clave:** `tipo|mensaje_normalizado`
- **Versión(es):** 0.1.7
- **Contexto(s):** loc=... dias_totales=... horario=...
- **Traceback:**
```
<traceback representativo>
```
-->

### E01 — TypeError: 'str' object is not callable
- **Estado:** ✅ **CORREGIDO en el código (verificado 2026-07-25)** — fix en
  `talksystem_labels.rpy` (loop `_p`→`_t_p`). Verificación: 0 vías de pisado de
  `_p` (directas/indirectas) y de `_` a nivel store en todo `game/`; lint limpio.
  **PENDIENTE:** que salga en un build publicado (el 0.1.8a en la calle aún NO lo tiene).
- **Veces:** ~73 (según errores2.txt: 67 en 0.1.7 + 6 en 0.1.8a)
- **Clave:** `TypeError|'str' object is not callable`
- **Versión(es):** 0.1.7 **y 0.1.8a** ⚠️ — el build 0.1.8a distribuido **sigue crasheando**, o sea NO incluye el fix de `_p`.
- **Contexto(s):** ubicuo — se dispara en cualquier locación/día (al cambiar de idioma tras usar "Hablar"). Locaciones vistas: casa_cocina, casa_pasilloarriba, casa_hmc, casa_living, casa_hviolet, casa_pasilloabajo, casa_gym. Rango de días: 2 a 116. Es de lejos el error más frecuente; muchos reportes son el mismo crash disparado varias veces seguidas.
- **Traceback:**
```
While running game code:
  ... (frames de script call acumulados) ...
  File "renpy/common/00start.rpy", line 119, in _execute_python_hide
    _init_language()
  File "renpy/common/00start.rpy", line 86, in _init_language
    renpy.change_language(language, force=True)
  File "renpy/translation/__init__.py", line 837, in change_language
  File "renpy/common/00gui.rpy", line 120, in _apply_rebuild
    renpy.ast.redefine([ "store.gui" ])
  File "game/script/ui/base/options.rpy", line 35, in <module>
    define gui.about = _p("""
    """)
TypeError: 'str' object is not callable
```

#### 🔧 Diagnóstico y arreglo (E01)

**Qué producía el error:**
En `talksystem_labels.rpy`, el bloque que limpia el texto de resultado del talk
tenía un `for` que usaba `_p` como variable de loop:

```python
for _i, _p in enumerate(_t_partes):
    _p = _p.rstrip(".,")
    ...
```

Ese código corre dentro de un `python:` de **label**, y ahí las variables **van
al store** (no son locales). Pero `_p` es una **función interna de Ren'Py** (arma
párrafos de texto multilínea) que el juego usa en `define gui.about = _p("""...""")`
([options.rpy:35](game/script/ui/base/options.rpy#L35)).

Al usar **"Hablar"** con cualquier NPC, ese loop **pisaba `_p`** dejándolo como un
string, **para toda la sesión** (las variables `_` no se guardan, pero sí persisten
en memoria hasta cerrar el juego). Después, cualquier cosa que dispara
`gui.rebuild()` — sobre todo **cambiar de idioma / arrancar una partida**
(`_init_language` → `change_language`) — re-evalúa el `define gui.about = _p(...)`,
y como `_p` ya era un string → `TypeError: 'str' object is not callable`.

Por eso era tan frecuente y "ubicuo": bastaba con hablar una vez (acción de las más
usadas) y después volver al menú / empezar partida.

**El arreglo:**
Se renombraron las variables del loop a `_t_i` / `_t_p` (la convención `_t_` que ya
usa ese archivo), para no tocar el builtin `_p`. Cambio de pocas líneas, sin efecto
en la lógica. Se dejó un comentario en el código advirtiendo la trampa.

**Verificación (2026-07-25):**
- Barrido de TODO `game/` (script + tl): **0** vías de pisado de `_p` (directas:
  asignación/for/as/tupla/walrus/global; indirectas: `store._p=`, `setattr`,
  `default/define _p`).
- El hermano `_` (gettext, usado en `define config.name`): **0** pisado a nivel
  store (sus 2 usos están dentro de `def`, o sea locales y seguros).
- Lint limpio.
- Test de runtime sugerido: usar "Hablar" → `type(_p)` sigue siendo función →
  `renpy.change_language("english")` no crashea.

**Estado:** corregido y verificado **en el código**. Falta que salga en un build
publicado (el 0.1.8a distribuido todavía no lo incluye).

### E02 — Exception: Style 'namebox' does not exist.
- **Estado:** ✅ **RESUELTO (2026-07-25)** — causa raíz eliminada por el fix de E01
  (no es un bug propio de `namebox`), **más** una red de seguridad aplicada por si
  cualquier otro crash futuro interrumpe un rebuild. Ver diagnóstico abajo.
- **Veces:** 1
- **Clave:** `Exception|Style 'namebox' does not exist.`
- **Versión(es):** 0.1.7
- **Nota:** apareció solo en un paste manual; **no está en errores.txt** (del 25-07).
- **Contexto(s):**
  - loc=casa_living dias_totales=40 dia_semana_actual=4 horario_actual=1
- **Traceback:**
```
While running game code:
  ... (frames de script call: intro_main, hud_stats) ...
  File "renpy/character.py", line 902, in display_say
  File "renpy/ui.py", line 306, in interact
  ... (visit_all / style build) ...
  File "renpy/style.pyx", line 83, in renpy.style.get_style
Exception: Style 'namebox' does not exist.
```

#### 🔧 Diagnóstico (E02) — efecto secundario de E01

**Qué lo producía:** NO es un defecto de `namebox` (está bien definido en
[screens.rpy:135](game/script/ui/base/screens.rpy#L135)/:148, lint limpio, nada lo
condiciona). Es colateral de **E01**:

1. El jugador cambia idioma (o arranca partida) → Ren'Py corre `change_language`.
2. Esa función hace, en orden: `renpy.style.rebuild()` → `run_blocks()` →
   `_apply_rebuild()` → re-evalúa `define gui.about = _p(...)` → **crashea E01**.
3. Los pasos siguientes (`renpy.style.restore()` + `renpy.style.rebuild()` final)
   **no se ejecutan** → el registro de estilos queda a medias, sin `namebox`.
4. El jugador toca "Continuar" en la pantalla de error → el juego reanuda.
5. El próximo diálogo con nombre busca el estilo `namebox` → no está → **E02**.

**Evidencia:** ningún código del juego llama a `change_language`/`style.rebuild`
(único disparador = cambio de idioma interno = ruta de E01); E02 salió 1 vez vs
~73 de E01; y el traceback de E02 está en `tl/english` (hubo cambio de idioma).

**El arreglo (2 capas):**
1. **Causa raíz:** con E01 corregido, `change_language` completa entero y los
   estilos se reconstruyen bien → E02 ya no tiene de dónde salir. No se tocó `namebox`.
2. **Red de seguridad (aplicada):** en `sistema_reporte_errores.rpy`, el label
   `_jp_error_context` ahora, si el jugador toca "Continuar" (`_return == "ignore"`),
   llama a `renpy.style.rebuild()` antes de reanudar. Así, si **cualquier** crash
   futuro (no solo `_p`) interrumpe un rebuild y deja los estilos a medias, al
   continuar se reconstruyen y no se arrastra el estado roto. `renpy.style.rebuild()`
   es la misma API que usa Ren'Py al cambiar idioma; va envuelta en try/except para
   no romper nunca el flujo de error. Lint limpio.

### E03 — LabelNotFound: quest_violet_questprincipal_01_a
- **Estado:** ✅ **CORREGIDO y verificado (2026-07-25)** — fix en 2 capas + tupla
  (ver diagnóstico abajo). La clase queda imposible por diseño, sin depender de la
  tupla mantenida a mano.
- **Veces:** ~8 (según errores2.txt)
- **Clave:** `renpy.script.LabelNotFound|could not find label 'quest_violet_questprincipal_01_a'`
- **Versión(es):** 0.1.7
- **Contexto(s):**
  - loc=casa_cocina dias_totales=10 dia_semana_actual=2 horario_actual=0 (×2)
  - loc=casa_hviolet dias_totales=26 dia_semana_actual=4 horario_actual=1
  - loc=casa_pasilloarriba dias_totales=12 dia_semana_actual=4 horario_actual=2
- **Traceback:**
```
While running game code:
  ... (frames de script call: intro_main, interactions_jasmine, interactions_violet, door_access) ...
  File "game/script/core/quests/questsystem_core.rpyc", line 1495, in script
  File "renpy/script.py", line 1201, in lookup
renpy.script.LabelNotFound: could not find label 'quest_violet_questprincipal_01_a'.
Did you mean: 'quest_violet_questprincipal_01_b'?
```

#### 🔧 Diagnóstico y arreglo (E03)

**Qué lo producía:** al hacer click en un NPC, `interaccion_<npc>` tiene un
**auto-trigger**: si hay una quest en `ETAPA_BOTON_LISTO`, llama a
`intentar_ejecutar()` y salta a `ejecutar_quest_activa`, que construye el label
`"quest_" + quest.id` y hace `jump expression`. Ese auto-trigger se saltea con una
**tupla de exclusión mantenida a mano** para las quests que usan triggers custom.

La quest **01_a** de Violet se dispara por el repartidor / la cama (labels
`paqueterepartidor_quest01_violet` / `paquetecama_quest01_violet`), **no tiene**
label `quest_violet_questprincipal_01_a`, y **se olvidó de la tupla**. Entonces, si
el jugador hacía click en Violet con 01_a en BOTON_LISTO → se construía
`quest_violet_questprincipal_01_a` (inexistente) → `LabelNotFound`.
Agravante: `intentar_ejecutar()` **avanza la etapa** a `ETAPA_DESARROLLO` *antes*
del jump, así que además dejaba la quest adelantada.

**El arreglo (2 capas + tupla), self-maintaining:**
1. **Red universal** en `ejecutar_quest_activa` ([questsystem_core.rpy:1513](game/script/core/quests/questsystem_core.rpy#L1513)):
   el `jump expression label_quest` ahora va dentro de `if renpy.has_label(label_quest)`.
   Ninguna quest sin label puede volver a crashear, venga de donde venga.
2. **Gate en los 3 auto-triggers** (interactions_violet/monica/jasmine): se agregó
   `renpy.has_label("quest_" + _quest_activa.id)` a la condición, para no llamar a
   `intentar_ejecutar()` (evitando el avance de etapa) en quests sin label.
3. Se dejó 01_a en la tupla de exclusión (fix previo), por intención explícita.

Con esto la clase queda cerrada **sin depender de acordarse de la tupla** — que fue
justo lo que falló.

**Verificación:** `quest_violet_questprincipal_01_a` no existe (correcto);
`ejecutar_quest_activa` (línea 1513) es el único `jump expression` que arma un label
de quest y está guardado; los 4 `jump ejecutar_quest_activa` pasan por ese guard;
lint limpio.

**Escenario 01_a ahora:** click en Violet con 01_a lista → `has_label(...)` False →
auto-trigger salteado → sin avance de etapa, sin crash → aparece el menú normal.

### E04 — OSError: Download error (asset web no descargado)
- **Estado:** ✅ **MITIGADO en 2 frentes (2026-07-25)** — **no es un bug de código**,
  es red/hosting. (1) UX: pantalla de conexión + Reintentar en vez de crash.
  (2) Infra: assets archivados en `.rpa`. Ver abajo.
- **Veces:** 1
- **Clave:** `OSError|Download error: network error` (se ignora el nombre de archivo puntual)
- **Versión(es):** 0.1.7
- **Contexto(s):**
  - loc=casa_sotano dias_totales=2 dia_semana_actual=1 horario_actual=1 — archivo: `bg_casa_mañana_living.jpg`
- **Nota:** ya se había visto otra ocurrencia antes de crear este registro (`bg_casa_tarde_hmc.jpg`). Es fallo de **descarga del build web** (red/hosting), no bug de código.
- **Traceback:**
```
While running game code:
  ... (frames de script call) ...
  File "renpy/common/000statements.rpy", line 485, in execute_pause
    renpy.pause()
  File "renpy/webloader.py", line 226, in process_downloaded_resources
OSError: Download error: network error ('images/bg/casa/bg_casa_mañana_living.jpg')
```

#### 🔧 Diagnóstico y mitigación (E04)

**Qué lo produce:** en el build web, Ren'Py baja los assets **on-demand**
(descarga progresiva). Cuando el juego necesita un recurso (ej. un fondo) y la
petición HTTP falla (corte de red, hipo del hosting/CDN, throttling), `webloader`
lanza `OSError: Download error`. **No hay defecto de código** — el asset existe; la
descarga falló.

**Por qué molestaba:** caía en el manejador genérico → mostraba la pantalla de
"Ocurrió un error" con "Reportar", así que un simple corte de red **parecía un
crash** y los jugadores lo reportaban como bug (parte de la inundación de reportes).

**Mitigación aplicada (código):** en `sistema_reporte_errores.rpy`, el handler ahora
detecta el download error (`"Download error" in traceback` → `_jp_es_descarga`) y la
pantalla muestra una vista de **"Problema de conexión"** con botón **🔄 Reintentar**
(recarga el juego y re-descarga) + "Continuar igual", **sin** el flujo de reporte de
bug. Lint limpio.

**Mitigación de infra (APLICADA):** en [options.rpy:217](game/script/ui/base/options.rpy#L217)
se archivan los assets en `.rpa` (`build.classify('game/**.png'/'.jpg'/'.webp', 'archive')`)
— **783 imágenes** dejan de ser requests HTTP sueltos on-demand. Detalle importante:
en Ren'Py **la última regla `classify` que matchea gana**, así que se re-excluye
`game/images/test/**` DESPUÉS del archive (si no, el `game/**` re-incluiría los
sprites de prueba en la distribución). Trade-off conocido: la carga inicial puede
cambiar; el efecto real se ve al generar el build.

### E05 — NameError: name '_ruta_vq0' is not defined
- **Estado:** ✅ **CORREGIDO (2026-07-25)** — `_ruta_vq0` → `default vq0b_ruta`
  (guardable). Se corrigió también el mismo patrón latente en 01_b. Ver abajo.
- **Veces:** 1 (errores2.txt)
- **Clave:** `NameError|name '_ruta_vq0' is not defined`
- **Versión(es):** 0.1.7
- **Contexto(s):**
  - loc=casa_hviolet dias_totales=3 dia_semana_actual=2 horario_actual=1
- **Traceback:**
```
While running game code:
  ... (script call) ...
  File "game/script/characters/violet/quests/violet_quest_0_b.rpy", line 698, in <module>
    if _ruta_vq0 == "respeto":
NameError: name '_ruta_vq0' is not defined
```

#### 🔧 Diagnóstico y arreglo (E05)

**Qué lo producía:** en la quest 0_b de Violet, la rama elegida (respeto/confrontar)
se guardaba en una variable **temporal** `_ruta_vq0`. En Ren'Py, **las variables que
empiezan con `_` no se guardan** (son "scratch", exentas de save/rollback). La rama
se decide temprano y se **lee mucho después**, en el cierre (tras cocinar) — y entre
medio el juego **devuelve el control al jugador** (tiene que ir a cocinar), que es un
punto natural para guardar. Si el jugador guardaba ahí y recargaba, `_ruta_vq0` no
existía → `NameError` al llegar al cierre.

**El arreglo:** `_ruta_vq0` → **`default vq0b_ruta = ""`** (guardable, sin `_`). Ahora
la variable siempre existe (el `default` evita el NameError) **y** su valor sobrevive
a save/reload (se guarda de verdad). Se renombraron las 4 referencias.

**Bonus — mismo patrón latente en 01_b:** la quest 01_b usaba `_ruta_vq01b` con
`default _ruta_vq01b = ""`. El `default` evitaba el crash, pero como la variable
sigue teniendo `_`, **su valor no se guarda** → tras un reload volvía a `""` y tomaba
la rama equivocada (bug silencioso, más raro porque su cutscene es continuo). Se
renombró a `default vq01b_ruta = ""` (7 referencias) por consistencia y correctitud.

**Verificación:** 0 referencias a `_ruta_vq0`/`_ruta_vq01b` en el proyecto; los dos
`default` nuevos presentes; lint limpio. Para saves viejos en pleno vuelo, la rama
cae a `""` (ninguna rama del if/elif) — no crashea, solo se saltea el bonus de stats.

### E06 — KeyError: 'mangas_violet'
- **Estado:** ✅ **CORREGIDO (2026-07-25)** — `del` → `pop(..., None)` (borrado
  idempotente). Se auditó y arregló toda la clase de mutaciones de inventario. Ver abajo.
- **Veces:** 1 (errores2.txt)
- **Clave:** `KeyError|'mangas_violet'`
- **Versión(es):** 0.1.7
- **Contexto(s):**
  - loc=casa_cocina dias_totales=8 dia_semana_actual=0 horario_actual=0
- **Traceback:**
```
While running game code:
  ... (script call: intro_main, hud_celular) ...
  File "game/script/characters/violet/quests/violet_quest_01_b.rpy", line 231, in <module>
    $ del store.inventario["mangas_violet"]
  File "renpy/revertable.py", line 81, in do_mutation
KeyError: 'mangas_violet'
```

#### 🔧 Diagnóstico y arreglo (E06)

**Qué lo producía:** al dar el paquete a Violet (quest 01_b), cada rama hacía
`del store.inventario["mangas_violet"]`. `del dict[key]` **crashea con KeyError si la
key no está**. Las dos opciones "Dar paquete" (sprite y puerta) están guardadas por
presencia del item, y el item es `consumible: False` (no se auto-borra), así que en
el flujo normal la key existe. Pero el `del` puede llegar con el item ausente por
**re-entrada / rollback / menú stale** (el stack venía inflado por el leak de frames),
y ahí revienta.

**El arreglo:** `del store.inventario["mangas_violet"]` → **`store.inventario.pop("mangas_violet", None)`**
en los 3 sitios (rutas a / b1 / b2). Borrado idempotente: idéntico cuando el item
está, no-op si falta. El "dar el paquete" es único igual, así que no cambia la lógica.

**Auditoría de toda la clase** (mutaciones de inventario sin guardar):
- 3× `del mangas_violet` (01_b) → `pop`. ✅
- **quest_11** `conjunto_cosplays`: hacía `-= 1` **y** `del` sin guardar (peor: el
  `-=` también crashea si falta). Se envolvió en `if get(...) > 0`. ✅ (proactivo)
- `shopping_system` (`del`/`-=`) y `event_monica_01` (`locion_masajes -=`): ya estaban
  guardados (`if item_id in inventario` / `if _tiene_locion`). Sin cambios.

**Verificación:** no quedan mutaciones de inventario sin guardar (salvo las que ya lo
estaban); lint limpio.

---

### E07 — Visual: sprite de quest en la locación equivocada

- **Estado:** ✅ **CORREGIDO (2026-07-27)**
- **Tipo:** bug visual (no crashea) — reporte manual
- **Versión:** 0.1.8c · PC
- **Contexto:** Lunes (día 22) — Mañana · Cocina (`casa_cocina`) ·
  quest activa "Violet y el Cosplay" (`violet_questprincipal_04_b`) en **etapa 2**

**Síntoma:** en la cocina, Violet aparece con el sprite del **door access** (el de
"ya salgo", `idle_violet_casa_pasillo_fuera_*`), apoyada contra el mueble y en una
posición que no corresponde a la cocina.

#### 🔧 Diagnóstico

Desincronización entre **dónde está el NPC** y **con qué sprite se lo dibuja**:

- La quest 04_b define `rutina_quest` con `locacion="casa_pasilloarriba"` +
  el sprite del pasillo, para `(dia, 0)` de **todos** los días.
- Esa rutina recién se le **aplica** al NPC en `ETAPA_RUTINA` (etapa 4), dentro de
  `_aplicar_rutina_quest()` (questsystem_core, transición etapa 3 → 4).
- Pero `obtener_sprite_quest()` / `obtener_posicion_quest()` devolvían el sprite y
  la posición **desde la etapa 1**, sin mirar la etapa ni la locación.

Resultado: en etapas 1–3 Violet sigue en su rutina normal (cocina los lunes a la
mañana), pero el HUD la dibuja con el visual de la quest — sprite del pasillo en la
posición del pasillo (663, 804) en vez de la de cocina (765, 1060).

El HUD consulta el sprite de quest como **Prioridad 1**, antes que la rutina visual,
así que el visual incorrecto le gana al correcto.

#### 🔨 El arreglo

Nuevo helper `Quest._rutina_quest_vigente()`: devuelve la `RutinaQuest` del momento
**solo si el NPC está realmente parado en la locación que ella define**.
`obtener_sprite_quest()` y `obtener_posicion_quest()` pasan a usarlo.

Se eligió contrastar contra `locacion_actual` en vez de contra la etapa porque
mantiene sprite y posición coherentes **sin importar quién movió al NPC** (rutina,
door access, evento) — no solo en el caso puntual de esta quest.

**Alcance:** afecta a las 4 quests con `rutina_quest`. Los NPCs de
`rutinas_adicionales` no tenían el mismo agujero: `obtener_quest_activa(npc_id)`
solo matchea `quest.npc_id`, así que nunca tomaban sprite de quest por ese camino.

**Verificación:** lint limpio.

#### 🔁 Ampliación (2026-07-27) — mismo bug en NPCs prestados

Al llevar el fix "a los demás personajes" se encontró que **ya estaba cubierto**
para las quests de Mónica y Jasmine (el arreglo vive en la clase `Quest`, no en el
código de Violet). Pero apareció una **segunda variante del mismo bug, ya viva**:

`_aplicar_rutina_a_npc()` guardaba **solo la locación** de la rutina y descartaba el
sprite:

```python
npc.rutinas_quest[(dia, horario)] = rutina.locacion   # el sprite se perdía
```

Y `obtener_sprite_quest_npc()` solo miraba `obtener_quest_activa(npc_id)`, que
matchea únicamente por `quest.npc_id`. Resultado: cuando una quest mueve a un NPC
**de otro personaje** vía `rutinas_adicionales`, ese NPC **cambiaba de locación pero
seguía dibujándose con el sprite de su rutina normal**, correspondiente a otra
habitación. Ya pasaba en la quest 09_a de Violet, que mueve a Mónica con sprites
propios por horario.

**Arreglo:** `_rutina_quest_vigente(npc_id)` ahora resuelve tanto `rutina_quest`
(NPC principal) como `rutinas_adicionales` (NPC prestado), con el mismo chequeo de
locación. Nuevo `_buscar_rutina_quest_vigente(npc_id)` busca en los dos lugares y lo
usan `obtener_sprite_quest_npc()` y `obtener_posicion_quest_npc()`.

No hace falta desempatar por prioridad: como solo se devuelven rutinas *vigentes*
(NPC parado donde la rutina dice) y un NPC está en una sola locación, a lo sumo una
puede coincidir.

**Verificación:** lint limpio; firmas retrocompatibles (`npc_id` es opcional).
