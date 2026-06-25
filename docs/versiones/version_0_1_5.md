# Versión 0.1.5

---

## 1. Sistema de Skin Dinámico en Quests

### Descripción
Se estableció el patrón estándar para mostrar NPCs con skin variable dentro de labels de quest, evitando duplicar labels enteros por cada variante de skin.

### Problema resuelto
Ren'Py no soporta expresiones dinámicas como `show npc [var]_sufijo` ni múltiples `[var]` en el mismo `show`. El `show expression` (usado en el sistema Talk) muestra imágenes planas y no es compatible con layered images compuestas. La solución es:

1. Evaluar el skin **una sola vez al inicio del label principal** y guardarlo en un `default`.
2. Usar `if/else` con atributos hardcodeados en cada `show` que depende del skin.

### Patrón estándar

```renpy
# Al inicio del label principal — evalúa UNA VEZ, persiste en save
default vq_cuerpo = "c_rbase"
...
label quest_npc_X:
    $ vq_cuerpo = cuerpo_activo("npc_id")
    ...
    if vq_cuerpo == "c_pijama":
        show npc_parada c_pijama_base ca_pijama o_base b_none at right with dissolve
    else:
        show npc_parada c_rbase_base ca_base o_base b_none at right with dissolve
```

Para quests con más skins, escalar con `elif`:
```renpy
if vq_cuerpo == "c_pijama":
    show npc_parada c_pijama_base ca_pijama ...
elif vq_cuerpo == "c_bikini":
    show npc_parada c_bikini_base ca_bikini ...
else:
    show npc_parada c_rbase_base ca_base ...
```

### Reglas del `[var]` en show statements (Ren'Py 8.5)
- ✓ `show npc attr_estatico [var]` — atributos estáticos ANTES del `[var]`
- ✓ `show npc [var]` — `[var]` como único token
- ✗ `show npc [var] attr_estatico` — nada puede seguir al `[var]`
- ✗ `show npc [var1] [var2]` — dos `[var]` se concatenan como un único atributo inválido

### Archivos Modificados
- `game/script/characters/violet/quests/violet_quest_03_a.rpy`

---

## 2. Refactor Quest Violet 03_A — De 860 a ~380 líneas

### Descripción
Se eliminaron los labels duplicados `*_pijama` (quest, ramas, comun, final_escena) y se reemplazaron por el patrón de skin dinámico. El archivo pasó de ~860 líneas a ~380 sin perder funcionalidad.

### Variables
| Variable | Tipo | Descripción |
|---|---|---|
| `vq3a_cuerpo` | `default str` | Prefijo de cuerpo evaluado al inicio (`"c_rbase"` / `"c_pijama"`). Persiste en saves. |

### Archivos Modificados
- `game/script/characters/violet/quests/violet_quest_03_a.rpy`

---

## 3. Sistema de Notificaciones de Inventario

### Descripción
Se añadieron funciones centrales para agregar/quitar items del inventario que disparan automáticamente una notificación visual con el emoji y nombre del item.

### API

```python
agregar_al_inventario("item_id")          # agrega 1 unidad + notificación verde
agregar_al_inventario("item_id", 3)       # agrega 3 unidades
quitar_del_inventario("item_id")          # quita 1 unidad + notificación roja
```

La notificación usa el campo `"emoji"` y `"nombre"` del catálogo de items (`CATALOGO_ITEMS`). El texto en rojo indica pérdida.

### Archivos Modificados
- `game/script/ui/hud/hud_notificaciones.rpy`
- `game/script/characters/violet/quests/violet_quest_01_a.rpy`
- `game/script/characters/violet/quests/violet_quest_02_b.rpy`
- `game/script/core/shopping/shopping_system.rpy`
- `game/script/core/messages/messagesystem_core.rpy`

---

## 4. Fix — Días hábiles en sistema de compras

### Descripción
`obtener_dias_restantes()` mostraba días calendario mientras el catálogo indicaba días hábiles. Ahora itera contando solo Lunes–Viernes, igual que `calcular_fecha_entrega()`.

### Archivos Modificados
- `game/script/core/shopping/shopping_system.rpy`

---

## 5. Fix — PicklingError en condición de desbloqueo de skin

### Descripción
Las lambdas definidas dentro de funciones no son serializables por Ren'Py al guardar. La condición de desbloqueo del skin pijama de Violet usaba una lambda local.

**Solución:** función nombrada a nivel de módulo (fuera de `inicializar_violet`).

```python
def _cond_pijama_desbloqueo():
    q = store.sistema_quests.obtener_quest("violet_questprincipal_02_b")
    return bool(q and q.completada)
```

### Archivos Modificados
- `game/script/characters/violet/definition_violet.rpy`

---

## 6. Fix — Idles de Jasmine en el gym

### Descripción
Antes del desbloqueo del skin deportivo, el idle del gym mostraba el sprite `skinropadeportiva` (incorrecto). Además, el `sprite_idle` del skin deportivo tenía un typo (`rutinabae` en lugar de `rutinabase`).

**Correcciones:**
- Agregado `sprite_idle` al skin `jasmine_entrenamiento_base` apuntando al sprite de ropa casual.
- Corregido el typo en `sprite_idle` de `jasmine_entrenamiento_deportiva`.
- Actualizada la rutina visual base del gym al path correcto como fallback.

### Archivos Modificados
- `game/script/characters/jasmine/visual/skins_jasmine.rpy`
- `game/script/characters/jasmine/definition_jasmine.rpy`

---

## 7. Fix — Trigger de evento Jasmine (ESTADO_EVENT_ACTIVO)

### Descripción
`validar_eventos()` corre en cada ciclo del game loop y auto-avanza el evento `jasmine_event_01` de `VISIBLE` a `ACTIVO` si la condición de activación se cumple (tarde de semana). La interacción con Jasmine solo chequeaba `ESTADO_EVENT_VISIBLE`, fallando siempre.

**Solución:** el check en `interaccion_jasmine` ahora acepta `VISIBLE` o `ACTIVO`:

```python
if _event_jasmine and _event_jasmine.estado in [ESTADO_EVENT_VISIBLE, ESTADO_EVENT_ACTIVO]:
```

### Archivos Modificados
- `game/script/characters/jasmine/interaction/interactions_jasmine.rpy`

---

## 8. Ítem Tanga de Violet

### Descripción
Nuevo item no comprable que el jugador obtiene al finalizar la quest `violet_questprincipal_03_a`. Tiene un label de uso con contenido pendiente.

| Campo | Valor |
|---|---|
| ID | `tanga_violet` |
| Emoji | 🩲 |
| Label uso | `usar_tanga_violet` |
| Condición uso | Solo en `casa_hmc` |

### Archivos Modificados
- `game/script/core/shopping/items_shopping.rpy`
- `game/script/characters/violet/quests/violet_quest_03_a.rpy`

---

## 9. Item Mangas — Uso actualizado

### Descripción
Usar el item `mangas_violet_mc` ahora:
- Muestra al MC en su habitación con el cuerpo `c_rbase_leyendocyberpunk`.
- Bloquea el uso si el horario es trasnoche (mensaje: "Es muy tarde para ponerme a leer...").
- Avanza el horario en 1 al terminar la lectura.

### Archivos Modificados
- `game/script/characters/violet/quests/violet_item_mangas.rpy`

---

## 10. Rutina Quest Violet 0 — Tarde en habitación

### Descripción
Durante la quest `violet_questprincipal_0`, Violet ahora está en su habitación (`casa_hviolet`) todos los días de la semana por la tarde (override sobre la rutina base del sábado que la ponía en el living).

### Archivos Modificados
- `game/script/characters/violet/quests/quest_violet.rpy`

---

## 11. Refactor Sistema de Skins — Activación Interna

### Descripción
Los skins dejaron de ser elegidos por el jugador y de requerir stats para desbloquearse. Ahora se activan internamente desde quests y eventos mediante `desbloquear_skin(skin_id)`, que además los hace activos inmediatamente.

### Cambios
- `activar_skin()` ya no verifica `esta_desbloqueado()`.
- Nueva función `desbloquear_skin(skin_id)`: marca el skin como desbloqueado y lo activa en su grupo.
- `_cond_pijama_violet()` ahora lee `skins_activos["violet"]["pijama"]` en lugar de verificar quest + stats.
- Eliminado el menú de selección de skin del menú de interacción con NPCs.

### API
```python
desbloquear_skin("violet_pijama_base")   # desbloquea y activa
cuerpo_activo("violet")                  # retorna "c_pijama" o "c_rbase"
```

### Archivos Modificados
- `game/script/core/skins/skinsystem_core.rpy`
- `game/script/characters/violet/visual/skins_violet.rpy`
- `game/script/ui/menus/menu_interaction.rpy`

---

## 12. App de Cheats — Modo DEV Exclusivo

### Descripción
La aplicación de cheats en el celular ahora solo se muestra cuando `MODO_DEV = True`. El modo dev se activa ingresando `"alanhhdev"` como nombre del personaje al inicio.

### Archivos Modificados
- `game/script/ui/hud/hud_celular.rpy`

---

## 13. Fix — Violet Permanecía en el Pasillo Post-Quest 04_b

### Descripción
Al completar la quest `violet_questprincipal_04_b`, `_restaurar_rutina_normal()` no actualizaba `locacion_actual`. Se agregó limpieza explícita: itera los 7 días, elimina entradas `(dia, 0)` de `rutinas_quest`, y fuerza `npc.locacion_actual` al valor de rutina base.

### Archivos Modificados
- `game/script/characters/violet/quests/violet_quest_04_b.rpy`

---

## 14. Evaluador de Skin en Quests 04_c a 05_c

### Descripción
Se aplicó el patrón estándar de skin dinámico (ítem 1) a las quests de Violet 04_c, 04_d, 04_e, 05_a, 05_b y 05_c. Cada label principal evalúa `cuerpo_activo("violet")` al inicio.

### Archivos Modificados
- `game/script/characters/violet/quests/violet_quest_04_c.rpy`
- `game/script/characters/violet/quests/violet_quest_04_d.rpy`
- `game/script/characters/violet/quests/violet_quest_04_e.rpy`
- `game/script/characters/violet/quests/violet_quest_05_a.rpy`
- `game/script/characters/violet/quests/violet_quest_05_b.rpy`
- `game/script/characters/violet/quests/violet_quest_05_c.rpy`

---

## 15. Quest 05_c — Tracking de Elección y Notificación de Memoria

### Descripción
La elección del jugador en `vq5c_menu_confesion` queda guardada en `vq5c_eleccion` y se pasa al sistema de memorias al completar la quest. Además se muestra la notificación flotante "Violet recordará esto".

```renpy
$ completar_quest_actual("violet", recuerdos={"eleccion_05c": vq5c_eleccion})
$ notificar_recordara("violet")
```

### Archivos Modificados
- `game/script/characters/violet/quests/violet_quest_05_c.rpy`

---

## 16. Quest 06_a — Rediseño Completo

### Descripción
La quest "Las entradas" fue rediseñada para ejecutarse de noche en la habitación de Violet.

**Cambios:**
- `validacion_especial`: Violet en `casa_hviolet` + horario 2 (noche).
- Opción en door access y menú de interacción directa: solo aparecen cumplida la condición.
- Conversación siempre en pijama (sin evaluador de skin, por horario y locación garantizados).
- Reemplazado el menú de elección del jugador por branching automático según el stat más alto: `obtener_stat1("violet") >= obtener_stat2("violet")` → `camino_amor`, sino → `camino_deseo`.
- Labels refactorizados: `violet_quest06a_puerta`, `violet_quest06a_hablar`, `violet_quest06a_habitacion`, `violet_quest06a_camino_amor`, `violet_quest06a_camino_deseo`.

### Archivos Modificados
- `game/script/characters/violet/quests/violet_quest_06_a.rpy`
- `game/script/characters/violet/quests/quest_violet.rpy`
- `game/script/core/locations/door_access_system.rpy`
- `game/script/characters/violet/interaction/interactions_violet.rpy`

---

## 17. Botones de Quest/Evento en Door Access

### Descripción
Los botones del menú de puerta ahora muestran un tag según su tipo:
- Quests → `(Quest)`
- Eventos → `(Evento)`

Se añadió el campo `"tipo": "evento"` a las opciones de eventos en `obtener_opciones_puerta()`. El screen `menu_puerta_npc` lo usa para elegir qué tag mostrar.

Las opciones del menú de interacción directa con NPC (`menu_interaccion_npc_completo`) ya no muestran ningún tag.

### Archivos Modificados
- `game/script/core/locations/door_access_system.rpy`
- `game/script/ui/menus/menu_interaction.rpy`

---

## 18. Renaming de Stats — Amor / Deseo

### Descripción
Los stats específicos de cada NPC (Complicidad/Sumisión para Violet, Adulación/Provocación para Jasmine, Madurez/Debilidad para Monica) fueron unificados bajo los nombres `amor` (stat1) y `deseo` (stat2) para todos los NPCs. Las variables guardables pasan a ser `{npc}_amor` y `{npc}_deseo`.

### Archivos Modificados
- `game/script/characters/violet/definition_violet.rpy`
- `game/script/characters/jasmine/definition_jasmine.rpy`
- `game/script/characters/monica/definition_monica.rpy`
- `game/script/characters/jasmine/quests/jasmine_quest_0.rpy`
- `game/script/characters/monica/quests/monica_quest_0.rpy`
- `game/script/characters/violet/quests/violet_quest_06_a.rpy`
- `game/script/core/locations/door_relation_system.rpy`

---

## 19. Fix — Interacción Jasmine Crasheaba en Locaciones Incorrectas

### Descripción
La quest `jasmine_questprincipal_0` arranca en `ETAPA_BOTON_LISTO` sin requisitos y tiene `validacion_especial` que requiere estar en el gym por la tarde. El auto-execute en `interaccion_jasmine` llamaba `intentar_ejecutar()` en cualquier locación, lo que causaba el mensaje de error y un estado inconsistente.

**Solución:** se excluyó `jasmine_questprincipal_0` del auto-execute. Se agrega como `opciones_extra` con el texto "Saludar", visible solo en `casa_gym` + horario 1.

### Archivos Modificados
- `game/script/characters/jasmine/interaction/interactions_jasmine.rpy`

---

## 20. Evento 03 — Refactorización del Flujo

### Descripción
Múltiples correcciones y mejoras al evento de limpieza del sábado:

**Flujo de activación:**
- El mensaje de Monica se envía la mañana SIGUIENTE a que se complete la quest 03_a (no inmediato).
- La condición de activación requiere: sábado mañana + `grupo_completado("monica_chat_violet_quest2")` + al menos 2 días desde que el evento se hizo visible.
- `mensaje_despertar` eliminado del constructor del `Event` (causaba disparo diario); solo existe en `ESTADO_EVENT_ACTIVO`.

**Gameplay interactivo:**
- Living, cocina y pasillo arriba reemplazados por `AccionLocacion` en lugar de screens modales.
- `ev03_limpiar_living`: ejecuta todas las escenas en secuencia (chimenea → escalera → sillón) con un solo click.
- `ev03_buscar_cocina`: da el ítem "Elementos de Limpieza" al hacer click.
- `ev03_limpiar_pasillo`: dispara la transición "Una limpieza más tarde…" y continúa el flujo.

**Menú de opciones:**
- Las 3 opciones del menú del baño están siempre disponibles (sin requisitos de stats).
- Recompensas: A = +2 amor + 1 deseo, B = +4 amor, C = +2 deseo.
- Eliminada la variable `vq4_rama_elegida`.

**Nuevo ítem:**

| Campo | Valor |
|---|---|
| ID | `elementos_limpieza` |
| Emoji | 🧹 |
| Vendible | No |

### Archivos Modificados
- `game/script/characters/violet/events/events_violet.rpy`
- `game/script/characters/violet/events/evento03_violet.rpy`
- `game/script/core/time/timesystem_core.rpy`
- `game/script/core/actions/actions_catalog.rpy`
- `game/script/core/shopping/items_shopping.rpy`
- `game/script/core/locations/door_access_system.rpy`
- `game/script/characters/monica/chat/chat_monica.rpy`
- `game/script/characters/violet/screens/violet_quest02_screens.rpy`
- `game/script/characters/violet/definition_violet.rpy`

---

## 21. Nuevos Estados de Conversación Condicionales — Violet

### Descripción
Se añadieron 3 estados al pool diario de Violet que solo aparecen cuando se cumplen condiciones de stats. El sistema de asignación ahora filtra el pool por `condicion()` antes de elegir al azar.

| Estado | ID | Condición | Efectos destacados |
|---|---|---|---|
| Buen Humor | `violet_buen_humor` | amor ≥ 15 | Complacerla/Adularla +2 amor, resto +1 amor |
| Muy Buen Humor | `violet_muy_buen_humor` | amor ≥ 15 | Escucharla/Hablarle +4 amor, resto +2 amor |
| Caliente | `violet_caliente` | deseo ≥ 30 | Provocarla/Adularla +2 deseo, resto +1 deseo |

**Nuevos códigos de resultado:** `+1_amor`, `+4_amor`, `+2_deseo`.

**API de condición:**
```python
EstadoTalk(
    id="violet_buen_humor",
    condicion=lambda: store.violet_amor >= 15,
    ...
)
```

### Archivos Modificados
- `game/script/core/talk/talksystem_core.rpy`
- `game/script/characters/violet/talk/violet_talk.rpy`
- `game/script/characters/violet/definition_violet.rpy`

---

## 22. Limpieza de Menú de Desbloqueos

### Descripción
Se reorganizaron los desbloqueos visibles en el menú de relaciones:

**Violet** — eliminados: "Conversación Diaria" (amor 10), "Ver TV Juntos" (amor 60), "Skin Pijama" (deseo 10), "???" (deseo 40). Agregados: "Conversacion Especial Buen Humor" (amor 15), "Conversacion Especial Muy Buen Humor" (amor 15), "Conversacion Especial Caliente" (deseo 30).

**Jasmine y Monica** — conservados solo los dos desbloqueos de door access: "Ingreso Habitación" (amor 30) e "Ingreso Nocturno" (deseo 60). Todos los demás eliminados.

### Archivos Modificados
- `game/script/characters/violet/definition_violet.rpy`
- `game/script/characters/jasmine/definition_jasmine.rpy`
- `game/script/characters/monica/definition_monica.rpy`

---

## 23. Fix — Posición Idle Jasmine en Living de Noche

### Descripción
La posición del idle de Jasmine en el living durante la noche (lunes a viernes) fue corregida de `(126, 958)` a `(1219, 903)`.

### Archivos Modificados
- `game/script/characters/jasmine/definition_jasmine.rpy`

---

## 24. Carpeta Tutorial

### Descripción
Se creó la carpeta `game/script/tutorial/` con el archivo base `tutorial.rpy` para alojar el tutorial interactivo del juego.

### Archivos Creados
- `game/script/tutorial/tutorial.rpy`
