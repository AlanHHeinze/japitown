# Versión 0.1.4

---

## 1. Sistema de Acciones de Locación (nuevo)

### Qué es

Las **acciones de locación** son actividades que el jugador puede realizar en lugares específicos de la casa (cocinar en la cocina, ver TV en el living, etc.). Aparecen como botones en un panel lateral derecho sobre el HUD. Cada acción puede tener efectos propios y puede ser interceptada por quests y eventos para disparar contenido narrativo.

---

### Archivos del sistema

| Archivo | Contenido |
|---|---|
| `game/script/core/actions/actionsystem_core.rpy` | Clases `AccionLocacion`, `ListenerAccion`, `SistemaAcciones` e instancia global `sistema_acciones` |
| `game/script/core/actions/actionsystem_screen.rpy` | Screen `acciones_locacion()` — panel de botones de acción |
| `game/script/core/actions/actions_catalog.rpy` | Definiciones de todas las acciones y sus labels genéricos |

---

### Clases principales

#### `AccionLocacion`

Define una acción disponible en una locación.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `id` | `str` | Identificador único (`"cocinar"`, `"ver_tv"`) |
| `nombre` | `str` | Texto del botón |
| `icono` | `str` | Emoji del botón |
| `locacion_id` | `str` | Locación donde aparece |
| `label_generico` | `str \| None` | Label a llamar si no hay listeners activos |
| `reseteo` | `str` | `"diario"` / `"semanal_lunes"` / `None` |
| `mensaje_reintento` | `str \| None` | Si es `str`: botón siempre clickeable, muestra piensa al reintentar. Si es `None`: botón insensible cuando ya se usó |

#### `ListenerAccion`

Registrado por una quest o evento para interceptar una acción.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `accion_id` | `str` | Qué acción intercepta |
| `label` | `str` | Label a ejecutar |
| `nombre_menu` | `str` | Texto en el menú de elección (si hay conflicto) |
| `prioridad` | `str` | `"quest"` / `"evento"` / `"generico"` |
| `condicion` | `callable \| None` | Condición extra para que el listener sea válido |
| `unico` | `bool` | Si es `True`, se auto-elimina al dispararse (default) |

---

### Flujo de ejecución (`label accion_locacion_ejecutar`)

```
Jugador clickea botón de acción
      │
      ├─ ¿Restricción activa bloquea esta acción? → piensa mensaje → return
      │
      ├─ ¿Acción ya usada hoy?
      │   ├─ Con mensaje_reintento → piensa mensaje → return
      │   └─ Sin mensaje_reintento → imposible (botón insensible)
      │
      ├─ Obtener listeners válidos (ordenados por prioridad: quest > evento > generico)
      │
      ├─ 0 listeners → llamar label_generico (o piensa "nada que hacer")
      ├─ 1 listener → ejecutar directamente → post_ejecutar (marca usada, remueve si unico)
      └─ 2+ listeners → renpy.display_menu() → jugador elige → ejecutar → post_ejecutar
```

---

### Integración en el HUD

El screen `acciones_locacion` se incluye via `use acciones_locacion` dentro del HUD principal, justo antes de `use hud_navegacion`. Los botones respetan `modo_posicionamiento` (cuando está activo, se bloquean con `NullAction()`).

---

### Reset automático

En `dormir()` se llama a:
- `sistema_acciones.resetear_diario()` — limpia `_usados_hoy` para todas las acciones con `reseteo="diario"`
- `sistema_acciones.resetear_semanal()` — si el día que comienza es lunes, limpia `_usados_semana`

---

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/core/npcs/npcsystem_interactions.rpy` | Nuevo `label accion_locacion_ejecutar` |
| `game/script/core/time/timesystem_core.rpy` | Hook de reset en `dormir()` |
| `game/script/ui/hud/hud_navigation.rpy` | `use acciones_locacion` en el HUD |

---

### API para quests y eventos

```python
# Registrar listener (desde un label de quest al activarse)
$ sistema_acciones.registrar_listener(ListenerAccion(
    accion_id="cocinar",
    label="jasmine_quest3_cocinar",
    nombre_menu="Preparar la receta de Jasmine",
    prioridad="quest",
    condicion=lambda: jasmine_quest3_activa,
    unico=True,
))

# Remover listener manualmente (si unico=False)
$ sistema_acciones.remover_listener("cocinar", label="jasmine_quest3_cocinar")
```

---

### Acciones iniciales

#### Cocinar

| Parámetro | Valor |
|---|---|
| Locación | `casa_cocina` |
| Restricción de horario | Ninguna |
| Efecto | +1 stat1 (amor) a Violet, Mónica y Jasmine |
| Texto | Varía según horario: "el desayuno" / "la merienda" / "la cena" |
| Efecto especial | Si Violet tiene estado `violet_hambre` y no fue hablada (`estado_posterior_id is None`), se activa `violet_feliz` |
| Avanza tiempo | Sí (+1 horario) |
| Reseteo | Diario |
| Reintento | "Estoy cansado hoy, quizás debería intentarlo mañana." (botón siempre clickeable) |

#### Ver TV

| Parámetro | Valor |
|---|---|
| Locación | `casa_living` |
| Restricción de horario | Solo de noche (horario ≥ 2) — si se clickea de día muestra piensa: "La casa está muy activa como para ver una película, podría intentarlo por la noche." |
| Efecto | +1 stat2 (deseo) al NPC elegido al azar (Violet, Mónica, Jasmine, o nadie) |
| Texto si NPC | "Te sentaste a ver una película, a los minutos apareció [nombre] y se unió. Compartieron un lindo momento juntos." |
| Texto si solo | "Aprovechaste la noche para ver una película y relajar un poco." |
| Avanza tiempo | Sí (+1 horario) |
| Reseteo | Diario |
| Reintento | Ninguno (botón insensible cuando ya se usó) |

---

## 2. Sistema de Puerta — Opción "Pedir mangas prestados" (quest 02_a)

### Qué cambió

El trigger de la quest `violet_questprincipal_02_a` podía activarse únicamente haciendo click en el sprite de Violet dentro de su habitación. Ahora también aparece como opción en el menú de puerta, permitiendo al jugador iniciarla desde el pasillo.

### Condiciones para que aparezca

- La quest `violet_questprincipal_02_a` está activa, no completada y en etapa `ETAPA_BOTON_LISTO`.
- Se cumple una de estas dos condiciones:
  - El jugador **nunca intentó** pedir los mangas (`violet_quest02a_primer_intento_hecho == False`).
  - El jugador ya intentó antes **y** tiene stat1 (amor) de Violet ≥ 10.

### Archivo modificado

| Archivo | Cambio |
|---|---|
| `game/script/core/locations/door_access_system.rpy` | Nueva entrada en `obtener_opciones_puerta()` para `npc_id == "violet"` |

---

## 3. Línea de quests de Violet — Reestructuración de la cadena

### Qué cambió

Se eliminó la quest `violet_questprincipal_5` ("Solo en casa") de la cadena principal de Violet. Ahora la quest `violet_questprincipal_04_a` se activa directamente al completarse `violet_questprincipal_03_a`, sin paso intermedio.

### Quests afectadas

| Quest | Cambio |
|---|---|
| `violet_questprincipal_5` | Eliminada del sistema. Archivo `violet_quest_05.rpy` borrado. |
| `violet_questprincipal_04_a` | `quest_anterior` cambiado de `violet_questprincipal_5` a `violet_questprincipal_03_a` |

### Archivos eliminados

Los siguientes archivos de quests individuales fueron consolidados dentro de `quest_violet.rpy` durante versiones anteriores y sus archivos sueltos fueron borrados:

`violet_quest_01.rpy`, `violet_quest_02.rpy`, `violet_quest_04.rpy`, `violet_quest_05.rpy`, `violet_quest_06.rpy`, `violet_quest_07.rpy`, `violet_quest_08.rpy`, `violet_quest_09.rpy`

También fueron eliminados los scripts auxiliares `update_quests.py` y `update_triggers.py` del directorio de quests de Violet.

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/quests/quest_violet.rpy` | Eliminada definición de `quest_violet_5`; actualizado `quest_anterior` de `quest_violet_04_a` |
| `game/script/core/time/timesystem_core.rpy` | Eliminado bloque de auto-inicio de quest_5 en `label accion_dormir` |

---

## 4. Quests de Violet — Cambios de requisitos (04_c, 04_d, 04_e)

### Quest 04_c — De requisito de deseo a espera de 1 día

**Antes:** La quest requería un nivel de deseo de Violet para avanzar.  
**Ahora:** La quest espera automáticamente 1 día (`dias_espera=1`) desde que `violet_questprincipal_04_b` se completa. Al día siguiente, Violet envía un mensaje de chat (`violet_quest04c_chat`) con las condiciones de entrega originales (Violet en su habitación, horario noche).

| Etapa | Antes | Ahora |
|---|---|---|
| Pista (ESPERA) | — | "Quizás Violet me mande un mensaje sobre el cosplay." |
| Que hacer (ESPERA) | — | "Darle un día" |
| Mensaje despertar (ESPERA) | — | "Quizás hoy Violet me mande algo sobre el cosplay." |
| Pista (BOTON_LISTO) | — | Dinámica: varía si el grupo de chat fue completado o no |
| Que hacer (BOTON_LISTO) | — | Dinámica: "Responder mensaje de Violet" / "Ir a ver a Violet." |

### Quest 04_d — Requisito de deseo: 25 → 10

Los mensajes de pista, que_hacer y mensaje_despertar fueron actualizados para reflejar el umbral de 10 de deseo.

### Quest 04_e — Requisito de deseo: 30 → 15

Los mensajes de pista, que_hacer y mensaje_despertar fueron actualizados para reflejar el umbral de 15 de deseo.

### Archivo modificado

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/quests/quest_violet.rpy` | Definiciones de `quest_violet_04_c`, `quest_violet_04_d`, `quest_violet_04_e` |

---

## 5. Sistema de Mensajes — Entrega retroactiva al dormir

### Qué es

Cuando el jugador se duerme en un horario anterior al de entrega de un mensaje (por ejemplo, duerme a la tarde y el mensaje debería llegar a la noche), el sistema ahora simula los horarios omitidos y entrega el mensaje. El jugador se despierta al día siguiente con el mensaje ya recibido.

### Problema que resuelve

Antes, si un mensaje tenía condición `momento_horario=2` (noche) y el jugador dormía a la tarde (horario 1), el mensaje nunca llegaba: al despertar `horario_actual=0`, la condición fallaba, y en los días siguientes el horario tampoco era "noche de ese día" sino del día siguiente.

### Flujo corregido en `dormir()`

```
1. Guardar _horario_antes_dormir = horario_actual   (ej: 1 = Tarde)
2. Resetear horario_actual = 0
3. Avanzar día, evaluar rutinas especiales, actualizar rutinas NPCs
4. actualizar_quests()   ← los triggers de quests disparan aquí
5. verificar_mensajes_horarios_omitidos(_horario_antes_dormir)
   ├─ Simula horarios [desde+1 .. 3]  (ej: [2, 3])
   ├─ En cada horario: actualiza posiciones de NPCs → intenta entrega
   └─ Al terminar: restaura horario=0 y posiciones de mañana
6. verificar_mensajes_en_espera()   ← mensajes con condición de mañana
```

### Método nuevo: `verificar_mensajes_horarios_omitidos(horario_desde)`

```python
# SistemaMensajes — messagesystem_core.rpy
def verificar_mensajes_horarios_omitidos(self, horario_desde):
    # horario_desde: horario en que el jugador durmió
    # Simula horarios omitidos, actualizando posición de NPCs en cada uno
    ...
```

| Parámetro | Descripción |
|---|---|
| `horario_desde` | Horario en que el jugador se fue a dormir (0–3) |

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/core/messages/messagesystem_core.rpy` | Nuevo método `verificar_mensajes_horarios_omitidos()`; corregida indentación en `OpcionRespuesta.__init__` y `GrupoMensajes.__init__` |
| `game/script/core/time/timesystem_core.rpy` | `dormir()`: guarda horario antes de dormir, llama `verificar_mensajes_horarios_omitidos` después de `actualizar_quests()` |

---

## 6. Bloqueo de dormir durante la entrega de la quest 01 de Violet

### Qué cambió

Una vez que la quest `violet_questprincipal_01` se dispara (el repartidor llega o el paquete aparece en la habitación), el jugador no puede ejecutar la acción de dormir hasta resolver la situación pendiente.

El bloqueo muestra el pensamiento: `"Tengo cosas pendientes por hacer, no puedo dormir ahora"`.

El chequeo se inserta antes del bloqueo genérico de paquete en habitación, para que el mensaje específico de la quest tome prioridad.

### Archivo modificado

| Archivo | Cambio |
|---|---|
| `game/script/core/time/timesystem_core.rpy` | Nueva verificación de `violet_quest1_entrega_pendiente` al inicio de `label accion_dormir` |

---

## 7. Fix — Mensaje de uso de ítem se cerraba instantáneamente

### Problema

Al intentar usar un ítem desde una locación inválida, el mensaje de instrucción (`instruccion_uso`) se mostraba y desaparecía de inmediato sin que el jugador pudiera leerlo.

### Causa

El botón del inventario llama a `label mostrar_mensaje_uso_item` vía `Function()` + `renpy.jump()`. El evento `mouseup` del click original propagaba al primer `pause` del `piensa`, cerrándolo sin que el jugador pudiera verlo.

### Fix

Se añadió `renpy.pause(0)` antes del `piensa` para absorber el evento de click pendiente, y se agregaron `window show` / `window hide` explícitos para garantizar que la ventana de diálogo esté visible.

```renpy
label mostrar_mensaje_uso_item:
    hide screen panel_inventario
    $ renpy.pause(0)          # absorbe el click pendiente del botón
    window show
    piensa "[msg_uso_item]"
    window hide
    jump game_loop
```

### Archivo modificado

| Archivo | Cambio |
|---|---|
| `game/script/core/shopping/shopping_system.rpy` | `label mostrar_mensaje_uso_item`: añadidos `renpy.pause(0)`, `window show` y `window hide` |

---

## 8. Evento 03 de Violet — Renombrado y corrección completa

### Qué cambió

El archivo `event_violet_limpieza.rpy` fue renombrado a `evento03_violet.rpy` para seguir la convención de los demás eventos. El evento era anteriormente una quest y al migrar al sistema de eventos quedaron varios mecanismos rotos, todos corregidos en esta versión.

### Correcciones realizadas

#### Sistema de Eventos — soporte para callback `on_aparicion`

La clase `Event` no tenía parámetro `on_aparicion`. Se añadió para permitir ejecutar una función arbitraria cuando el evento transiciona por primera vez de OCULTO a VISIBLE.

| Archivo | Cambio |
|---|---|
| `game/script/core/events/eventsystem_core.rpy` | Parámetro `on_aparicion=None` en `Event.__init__`; llamada al callback en `validar_eventos()` al transicionar OCULTO → VISIBLE |

#### Sistema de Eventos — transición VISIBLE → ACTIVO faltante

`validar_eventos()` solo manejaba la transición OCULTO → VISIBLE. Los eventos en estado VISIBLE nunca eran evaluados para activarse, por lo que el evento nunca llegaba a ACTIVO el sábado.

| Archivo | Cambio |
|---|---|
| `game/script/core/events/eventsystem_core.rpy` | Nuevo bloque `elif estado == ESTADO_EVENT_VISIBLE` en `validar_eventos()` que llama `event.activar()` si `verificar_activacion()` es True |

#### Trigger del chat de Monica

El mensaje de Monica que avisa de la limpieza no llegaba. Se implementó mediante el callback `on_aparicion`:

```python
def on_aparicion_evento03_violet():
    store.sistema_mensajes.disparar_por_trigger("event_aparicion", "violet_quest2_chat_monica", "monica")
```

#### Mensajes despertar

Ambos estados (VISIBLE y ACTIVO) tenían el mismo texto en `mensaje_despertar`, lo que hacía que el set `mensajes_despertar_mostrados` bloqueara el mensaje del sábado (ya marcado como mostrado en un día anterior). Se asignaron textos distintos a cada estado.

| Estado | Mensaje |
|---|---|
| VISIBLE | "Este sábado tengo que despertar a Violet para limpiar la casa." |
| ACTIVO | "Hoy es sábado, tengo que despertar a Violet para que limpiemos la casa." |

#### Referencias al ID del evento

El `door_access_system.rpy` referenciaba el ID y label viejos. Actualizados:

| Antes | Ahora |
|---|---|
| `"violet_event_limpieza"` | `"violet_evento_03"` |
| label `"event_violet_limpieza_narrativa"` | label `"evento03_violet"` |

### Archivos modificados / renombrados

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/events/event_violet_limpieza.rpy` | **Eliminado** |
| `game/script/characters/violet/events/evento03_violet.rpy` | **Nuevo** — mismo contenido narrativo, label principal renombrado a `evento03_violet`, referencia interna al ID de evento actualizada |
| `game/script/characters/violet/events/events_violet.rpy` | ID del evento, label, callback `on_aparicion`, `config_etapas` con textos diferenciados por estado, rutinas NPC correctas |
| `game/script/core/events/eventsystem_core.rpy` | Soporte para `on_aparicion`; transición VISIBLE → ACTIVO en `validar_eventos()` |
| `game/script/core/locations/door_access_system.rpy` | Actualizado ID de evento y label en `obtener_opciones_puerta()` |

---

## 9. Fix — Exploit de rollback en recompensas de quests

### Problema

En Ren'Py el jugador puede retroceder a través del historial de decisiones usando la tecla de retroceso. Si el `modificar_stat` ocurría **dentro** de una rama del `menu:`, el jugador podía volver al menú, elegir otra opción y acumular stats infinitos.

### Solución aplicada

Se introdujo el patrón "variable de ruta + cierre compartido":

1. Cada rama del menú asigna una variable de ruta (`_ruta_X = "nombre"`) en lugar de modificar el stat directamente.
2. El stat se aplica **una sola vez** en un label de cierre compartido al que todas las ramas hacen `jump`.

Cuando el jugador retrocede dentro del menú, Ren'Py restaura la variable de ruta a su valor previo a la elección. Al elegir de nuevo, la variable se sobreescribe — nunca se acumula.

```renpy
# ANTES — explotable
"Opción A":
    npc "Respuesta A"
    $ npc.modificar_stat1(4)   # se ejecuta en la rama
"Opción B":
    npc "Respuesta B"
    $ npc.modificar_stat2(2)   # se ejecuta en la rama

# DESPUÉS — seguro
"Opción A":
    npc "Respuesta A"
    $ _ruta_x = "a"            # solo marca la elección
"Opción B":
    npc "Respuesta B"
    $ _ruta_x = "b"

# Cierre compartido:
label mi_quest_cierre:
    if _ruta_x == "a":
        $ npc.modificar_stat1(4)   # se ejecuta una sola vez
    elif _ruta_x == "b":
        $ npc.modificar_stat2(2)
    $ completar_quest_actual("npc")
```

### Archivos modificados

| Archivo | Variable de ruta | Cierre donde se aplica el stat |
|---|---|---|
| `game/script/characters/violet/quests/violet_quest_0.rpy` | `_ruta_vq0` | `quest_violet_0_puerta` |
| `game/script/characters/violet/quests/violet_quest_01_b.rpy` | `_ruta_vq01b` | `dar_paquete_violet_cierre` (label nuevo) |
| `game/script/characters/violet/quests/violet_quest_02_b.rpy` | `violet_recuerdo_mangas` (reutilizado) | `violet_quest02b_fin` |
| `game/script/characters/violet/events/evento03_violet.rpy` | `vq4_rama_elegida` (reutilizado) | `violet_quest2_cierre` |
| `game/script/characters/jasmine/quests/jasmine_quest_0.rpy` | `_ruta_jq0` | `quest_jasmine_0_regalo` |
| `game/script/characters/monica/quests/monica_quest_0.rpy` | `_ruta_mq0` | `quest_monica_0_cierre` |

---

## 10. Fix — Exploit de rollback en el sistema de conversación (Talk)

### Problema

El mismo exploit de rollback de la sección 9 afectaba al sistema de conversación diaria (`hablar`) de los tres NPCs. El `modificar_stat` ocurría dentro de cada rama del menú de preguntas, permitiendo acumular stats repitiendo la misma conversación.

### Solución aplicada

Mismo patrón, adaptado al sistema genérico de conversaciones:

```renpy
# ANTES — explotable
menu:
    "[_txt_op0]":
        violet "[_op0['resp']]"
        $ _npc_v.modificar_stat(_op0["stat"], 1)   # dentro de la rama
    "[_txt_op1]":
        ...

# DESPUÉS — seguro
menu:
    "[_txt_op0]":
        violet "[_op0['resp']]"
        $ _hablar_stat_elegido = _op0["stat"]       # solo guarda cuál
    "[_txt_op1]":
        ...

$ _npc_v.modificar_stat(_hablar_stat_elegido, 1)    # se aplica una vez, fuera del menú
```

La variable `_hablar_stat_elegido` siempre queda establecida al salir del menú, y el rollback dentro del menú la restaura al valor previo a la elección.

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/interaction/conversacion_violet.rpy` | `modificar_stat` movido fuera del menú, usando `_hablar_stat_elegido` |
| `game/script/characters/jasmine/interaction/conversacion_jasmine.rpy` | Ídem |
| `game/script/characters/monica/interaction/conversacion_monica.rpy` | Ídem |

---

## 11. Sistema de Relación de Puertas (Fecha: 27/05/2026)

### Qué es

Se implementó un sistema centralizado que determina el nivel de acceso del jugador a las habitaciones de los NPCs (y al baño) basado en los stats de relación. Reemplaza la función eliminada `puede_hablar_puerta()`.

---

### Archivos del sistema

| Archivo | Contenido |
|---|---|
| `game/script/core/locations/door_relation_system.rpy` | **[NUEVO]** Tablas de acceso, mensajes y funciones de verificación |
| `game/script/core/locations/door_access_system.rpy` | **[MODIFICADO]** Refactorizado para consumir el nuevo sistema |

---

### Jerarquía de acceso a habitaciones (5 niveles)

El sistema evalúa de mayor a menor el nivel alcanzado por el jugador:

| Nivel | Condición | Resultado |
|---|---|---|
| `ingreso_noche` | `horario==3` + `stat2 >= umbral` + NPC presente | Entra directamente (trasnoche) |
| `ingreso_diurno` | `horario!=3` + `stat1 >= umbral` | Entra directamente — **NPC no necesita estar en casa** |
| `dejar_pasar` | `stat1 >= umbral` + NPC presente | NPC dice "Adelante" → entra |
| `sale_pasillo` | `stat1 >= umbral` + NPC presente | NPC dice "Ahí salgo" → NPC va al pasillo |
| `None` | — | NPC dice "Estoy ocupada" |

**Regla clave:** `ingreso_diurno` funciona como una **invitación permanente**: el jugador puede entrar aunque el NPC haya salido. Los demás niveles (salvo `ingreso_noche`) requieren que el NPC esté físicamente en su habitación.

---

### Umbrales por NPC (`TABLA_ACCESO_HABITACION`)

| NPC | `ingreso_noche` | `ingreso_diurno` | `dejar_pasar` | `sale_pasillo` |
|---|---|---|---|---|
| Violet | stat2 ≥ 60 | stat1 ≥ 80 | stat1 ≥ 30 | stat1 ≥ 15 |
| Jasmine | stat2 ≥ 60 | stat1 ≥ 80 | stat1 ≥ 0 (siempre) | stat1 ≥ 0 (siempre) |
| Monica | stat2 ≥ 60 | stat1 ≥ 80 | stat1 ≥ 0 (siempre) | stat1 ≥ 0 (siempre) |

---

### Funciones de verificación

```python
verificar_nivel_acceso_habitacion(npc_id) -> str | None
# Retorna: "ingreso_noche" | "ingreso_diurno" | "dejar_pasar" | "sale_pasillo" | None

verificar_nivel_acceso_banio(npc_id) -> None
# Siempre retorna None (contenido de baño no disponible aún)
```

---

### Cambios en `door_access_system.rpy`

- **Eliminado**: `puede_hablar_puerta()` — ya no existe en ningún archivo.
- **Nuevo label** `interaccion_golpear_dejar_pasar`: NPC dice "Adelante" y el jugador entra a la habitación.
- **Nuevo label** `interaccion_golpear_sale_pasillo`: NPC dice "Ahí salgo" y se mueve al pasillo de arriba; el jugador también se mueve al pasillo.
- **Nueva screen** `menu_banio_npc(npc_id, bg_path=None)`: menú de baño con "Golpear la puerta" activo y dos opciones desactivadas como placeholder ("Espiar" / "Entrar").
- **Refactorizado** `interaccion_banio_ocupado`: usa `menu_banio_npc` en lugar del menú de puerta genérico.

---

### Mensajes configurables (`MENSAJES_NPC_PUERTA`)

Editar en `door_relation_system.rpy` para personalizar la voz de cada NPC:

```python
MENSAJES_NPC_PUERTA = {
    "violet":  {"ocupada": "Estoy ocupada.", "ahi_salgo": "Ahí salgo.", "adelante": "Adelante."},
    "jasmine": {"ocupada": "Estoy ocupada.", "ahi_salgo": "Ahí salgo.", "adelante": "Adelante."},
    "monica":  {"ocupada": "Estoy ocupada.", "ahi_salgo": "Ahí salgo.", "adelante": "Adelante."},
}
```

---

## 12. Fix de Serialización de Lambdas en Quests — PicklingError (Fecha: 27/05/2026)

### Problema

El juego crasheaba al guardar con quests activas. Causa raíz: `sistema_quests` es un objeto `define` mutable almacenado en `store`. Los objetos `Quest` dentro de él contienen lambdas en campos como `pista`, `que_hacer`, `mensaje_despertar`, `condicion_espera` y `accion_al_entrar`. Python no puede serializar lambdas anónimas → **PicklingError al guardar**.

---

### Solución: `CallableRef` + `_qc()`

Se agregaron tres elementos al inicio del bloque `init python:` en `questsystem_core.rpy`:

```python
_quest_callable_registry = {}   # Registro global, reconstruido en cada inicio de juego

class CallableRef:
    """Envoltorio picklable que referencia un callable por clave string."""
    def __init__(self, key):
        self.key = key
    def __call__(self, *args, **kwargs):
        fn = _quest_callable_registry.get(self.key)
        if fn is None: return None
        try: return fn(*args, **kwargs)
        except Exception: return None

def _qc(key, fn):
    """Registra fn en el registry y retorna un CallableRef picklable."""
    _quest_callable_registry[key] = fn
    return CallableRef(key)
```

**Cómo funciona:** El registro se reconstruye en cada arranque del juego (antes de cargar cualquier save). El `CallableRef` solo almacena una clave string (serializable). La función real se busca al momento de invocarse.

---

### Regla de uso: NUNCA lambdas directas en campos de Quest

```python
# INCORRECTO — crashea al guardar
pista=lambda: "Ir a ver a Violet",
que_hacer=lambda: "Ayuda a Violet ({}/3)".format(violet_atencion),

# CORRECTO opción A — función nombrada (picklable por module+qualname)
# Definir en init python: ANTES del bloque init 5 python:
def _pista_mi_quest():
    return "Ir a ver a Violet"
pista=_pista_mi_quest,   # referencia directa, sin ()

# CORRECTO opción B — _qc() para lambdas inline
que_hacer=_qc("mi_quest_quehacer", lambda: "Ayuda a Violet ({}/3)".format(store.violet_atencion)),
```

**Convención de claves `_qc`:** deben ser únicas en todo el proyecto. Usar `"<npc>_q<numero>_<campo>"`, ej: `"vq01a_espera_quehacer"`, `"vq09a_botonlisto_pista"`.

---

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/core/quests/questsystem_core.rpy` | Agregados `_quest_callable_registry`, clase `CallableRef` y función `_qc()` al inicio de `init python:` |
| `game/script/characters/violet/quests/quest_violet.rpy` | Los 21 lambdas reemplazados: ~10 por referencias a funciones nombradas, ~11 por `_qc()` |

---

## 13. Fix de Lambdas en Talk, Chat y Sistemas Auxiliares (Fecha: 27/05/2026)

### Problema

Varios archivos del juego tenían lambdas anónimas almacenadas en objetos `define` (`sistema_talk`, `sistema_mensajes`) o en dicts en `store` (`pensamientos_registrados`). Estos objetos se serializan al guardar, causando **PicklingError**. Además, las funciones de recompensa en los tres archivos de talk usaban `modificar_stat("deseo", 1)` — un nombre de stat que ya no existe tras la refactorización de stats (sección 6 del skill de cambios), por lo que la recompensa nunca se aplicaba silenciosamente.

---

### Archivos afectados y fixes aplicados

#### Talk de NPCs (`violet_talk.rpy`, `jasmine_talk.rpy`, `monica_talk.rpy`)

Cada archivo tenía dos `OpcionEspecialTalk` con 4 lambdas (`condicion` y `recompensa_extra` de cada opción). Las lambdas vivían dentro de `inicializar_talk_violet/jasmine/monica()` y luego se almacenaban en `sistema_talk` (`define`).

**Fix:** Se agregaron 4 funciones nombradas a nivel de módulo (fuera de la función inicializadora) en cada archivo, y se reemplazaron las lambdas por referencias a esas funciones.

| NPC | Funciones agregadas |
|---|---|
| Violet | `_violet_cond_golosinas`, `_violet_recompensa_golosinas`, `_violet_cond_videojuegos`, `_violet_recompensa_videojuegos` |
| Jasmine | `_jasmine_cond_bebida`, `_jasmine_recompensa_bebida`, `_jasmine_cond_entrenar`, `_jasmine_recompensa_entrenar` |
| Monica | `_monica_cond_locion`, `_monica_recompensa_locion`, `_monica_cond_tareas`, `_monica_recompensa_tareas` |

**Bug de stat silencioso corregido:** Las tres funciones `_*_recompensa_*` llamaban `modificar_stat("deseo", 1)`. El nombre `"deseo"` no coincide con ningún stat actual. Corregido a `npc.modificar_stat2(1)` en los tres archivos (stat2 = Sumisión / Provocación / Debilidad según el NPC).

```python
# ANTES — recompensa nunca se aplicaba
recompensa_extra=lambda: obtener_npc("violet").modificar_stat("deseo", 1) if obtener_npc("violet") else None

# DESPUÉS — función nombrada, stat correcto
def _violet_recompensa_golosinas():
    npc = obtener_npc("violet")
    if npc:
        npc.modificar_stat2(1)
```

---

#### Chat de la tienda CoXplay (`chat_coxplay.rpy`)

8 lambdas en objetos `GrupoMensajes` y `OpcionRespuesta` almacenados en `sistema_mensajes` (`define`).

**Fix:** Se agregaron 7 funciones nombradas al bloque `init 6 python:` del mismo archivo:

| Función | Propósito |
|---|---|
| `_coxplay_disparar_g2()` | Dispara el grupo 2 al completar el grupo 1 |
| `_coxplay_disparar_g3()` | Dispara el grupo 3 al completar el grupo 2 |
| `_coxplay_disparar_g4()` | Dispara el grupo 4 al completar el grupo 3 |
| `_coxplay_texto_contacto()` | Texto del jugador (con saludo dinámico según horario) |
| `_coxplay_cond_manana()` | Condición: horario mañana (`horario_actual == 0`) |
| `_coxplay_cond_no_manana()` | Condición: horario no mañana (`horario_actual != 0`) |
| `_coxplay_msg_recordar()` | Mensaje de la tienda con nombre del MC y saludo dinámico |

---

#### Sistema de Pensamientos (`pensamiento_system.rpy`)

`pensamientos_registrados` es un dict almacenado en `store`. El pensamiento de Violet tenía `condicion=lambda: store.violet_evento2_completado` — lambda no picklable.

**Fix:** Se agregó la función `_cond_pensamiento_violet_1()` en el mismo bloque `init 5 python:` y se reemplazó la lambda.

---

#### Sistema de Validación de Movimiento (`movesystem_validation.rpy`)

La función `bloquear_movimiento()` creaba un `ValidadorEstado(condicion_func=lambda: False, ...)`. Aunque la función no es llamada en el código actual, si se llegara a usar crearía un validador con lambda no picklable.

**Fix preventivo:** Se agregó `_bloqueo_siempre_falso()` como función nombrada y se reemplazó la lambda.

---

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/talk/violet_talk.rpy` | 4 funciones nombradas + 4 lambdas reemplazadas + fix stat "deseo" |
| `game/script/characters/jasmine/talk/jasmine_talk.rpy` | 4 funciones nombradas + 4 lambdas reemplazadas + fix stat "deseo" |
| `game/script/characters/monica/talk/monica_talk.rpy` | 4 funciones nombradas + 4 lambdas reemplazadas + fix stat "deseo" |
| `game/script/characters/violet/chat/chat_coxplay.rpy` | 7 funciones nombradas + 8 lambdas reemplazadas |
| `game/script/core/thoughts/pensamiento_system.rpy` | Función `_cond_pensamiento_violet_1()` + lambda reemplazada |
| `game/script/core/locations/movesystem_validation.rpy` | Función `_bloqueo_siempre_falso()` + lambda reemplazada (preventivo) |

---

## 14. Fix — Quest 11 de Violet bloqueada por referencia incorrecta (Fecha: 27/05/2026)

### Problema

La quest `violet_questprincipal_11` ("Los ruidos nocturnos") tenía `quest_anterior="violet_questprincipal_10"`. La quest con ese ID **nunca existió** en el proyecto — por lo tanto, la condición `quest_anterior completada` nunca se cumplía y las quests 11 y 12 nunca podían activarse.

### Fix

Se corrigió la referencia a la quest predecesora correcta:

```python
# ANTES — ID inexistente
quest_anterior="violet_questprincipal_10",

# DESPUÉS — ID correcto
quest_anterior="violet_questprincipal_09_a",
```

### Efecto

La cadena `quest_11 → quest_12` queda desbloqueada. Al completar `violet_questprincipal_09_a`, el sistema espera `dias_espera=3` y activa "Los ruidos nocturnos" normalmente.

### Archivo modificado

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/quests/quest_violet.rpy` | `quest_anterior` de `violet_questprincipal_11` corregido de `"violet_questprincipal_10"` a `"violet_questprincipal_09_a"` |

---

## 15. App de Relaciones — Desbloqueos por NPC (Fecha: 01/06/2026)

### Qué es

Nueva pantalla del celular que muestra el estado de relación con cada NPC: barras de amor y deseo con su valor numérico, y listas desplegables de desbloqueos organizadas en tres columnas (icono | nombre | requisito numérico). Los ítems desbloqueados se muestran en blanco y los bloqueados en gris con candado.

### Archivos nuevos

| Archivo | Contenido |
|---|---|
| `game/script/ui/hud/hud_relaciones.rpy` | Screen `panel_relaciones` y sub-screens `_rel_bloque_npc`, `_rel_stat`, `_rel_desplegable`, `_rel_item` |
| `game/script/core/relationships/relationship_unlocks.rpy` | Función `obtener_desbloqueos_stat(npc_id, stat)` que retorna `(desbloqueados, bloqueados)` |

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/core/npcs/npcsystem_core.rpy` | `self.desbloqueos = []` en `__init__`; nuevo método `agregar_desbloqueo(stat, umbral, icono, nombre, desc)` |
| `game/script/characters/violet/definition_violet.rpy` | 3 desbloqueos de amor + 3 de deseo; stats clampeados a `min(100, max(0, ...))` |
| `game/script/characters/jasmine/definition_jasmine.rpy` | 2 desbloqueos de amor + 3 de deseo; ídem clamp |
| `game/script/characters/monica/definition_monica.rpy` | 2 desbloqueos de amor + 3 de deseo; ídem clamp |
| `game/script/ui/hud/hud_celular.rpy` | Botón relaciones apunta a `Show("panel_relaciones")` en lugar de `Show("estadisticas_npcs")` |

### Layout de ítems

Cada ítem usa 3 segmentos de ancho fijo calculado (`_avail = ajuste_cel_area_w - 69`):
- **Seg 1** (26px): emoji del desbloqueo
- **Seg 2** (`_avail - 26 - _seg3`): nombre
- **Seg 3** (34px desbloqueado / 56px bloqueado): número de requisito [+ 🔒]

---

## 16. Fix — NPCs retornan a su habitación al salir del pasillo (Fecha: 01/06/2026)

### Qué es

Cuando el jugador sale de un pasillo, los NPCs que habían salido a ese pasillo (via `sale_pasillo`) vuelven automáticamente a su habitación de rutina.

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/core/locations/door_access_system.rpy` | Nueva función `retornar_npcs_pasillo_al_salir(locacion_salida_id)` |
| `game/script/core/locations/locationsystem_core.rpy` | `mover_a_locacion()` llama a `retornar_npcs_pasillo_al_salir()` después de `on_exit()` |

---

## 17. Sprites — Nuevos atributos y layered image `violet_espalda` (Fecha: 01/06/2026)

### Violet — `violet_parada` (nuevos atributos en grupo `cuerpo`)

| Atributo | Imagen |
|---|---|
| `c_pijama_mangas` | `violet_parada_cuerpo_pijama_mangas.png` |
| `c_rbase_cajacosplay` | `violet_parada_cuerpo_rbase_cajacoxplay.png` |

### Violet — nueva `layeredimage violet_espalda`

Vista de espalda de Violet con dos grupos independientes:

| Grupo | Atributos |
|---|---|
| `skinbase` | `sb_none` (Null — placeholder para imágenes futuras) |
| `pijama` | `p_none`, `p_base`, `p_cyberpunk`, `p_fantasia`, `p_novela`, `p_pensando`, `p_rascando1`, `p_rascando2` |

### MC — `mc_parado_base` (nuevos atributos en grupo `cuerpo`)

| Atributo | Imagen |
|---|---|
| `c_rbase_cajacosplay` | `mc_base_cuerpo_rbase_cajacoxplay.png` |
| `c_rbase_mangas` | `mc_base_cuerpo_rbase_mangas.png` |

### Archivo modificado

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/visual/sprites_violet.rpy` | Nuevos atributos en `violet_parada`; nuevo `layeredimage violet_espalda` |
| `game/script/characters/mc/sprites_mc.rpy` | Nuevos atributos en `mc_parado_base` |

---

## 18. Transforms — Movimientos de espalda (Fecha: 01/06/2026)

Cuatro transforms nuevos para `violet_espalda` (680px de ancho), agregados en `transforms_common.rpy`:

| Transform | Descripción |
|---|---|
| `salir_poquito` | Desde `right` (x=1920) hacia x=2147 — 1/3 del lado derecho fuera de pantalla. `ease 0.6` |
| `entrar_poquito` | Desde x=2147 de vuelta a `right` (x=1920). `ease 0.6` |
| `salir_todo` | Desde `right` (x=1920) hasta x=2600 — sprite completamente fuera. `ease 1.2` |
| `entrar_derecha_aright` | Desde x=2600 (fuera) hasta `right` (x=1920). `ease 1.2` |

### Archivo modificado

| Archivo | Cambio |
|---|---|
| `game/script/core/utils/transforms_common.rpy` | 4 transforms nuevos al final del archivo |

---

## 19. Quest 02_b de Violet — Correcciones (Fecha: 01/06/2026)

### Cambios

- **Escena en `violet_quest02b_fin`**: se agrega `scene expression "images/bg/casa/bg_casa_trasnoche_pasilloarriba.png" with fade` al inicio del label de fin.
- **Avance de tiempo**: se llama `$ avanzar_horario()` antes de `completar_quest_actual()`.
- **Atributos de `violet_espalda` corregidos**: todos los `c_pijama_*` reemplazados por `p_*` (ej: `c_pijama_base` → `p_base`).

### Archivo modificado

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/quests/violet_quest_02_b.rpy` | Scene de trasnoche, avance de tiempo, corrección de 7 atributos de `violet_espalda` |

---

## 20. Quest 0 de Violet — Imagen de cena (Fecha: 01/06/2026)

### Cambio

Se declaró `quest0_violet_cenando` y se reemplazó `scene black with fade` en línea 667 por `scene quest0_violet_cenando with fade`.

### Archivo modificado

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/quests/violet_quest_0.rpy` | Nueva imagen `quest0_violet_cenando.jpg` declarada y usada en escena de cena |
