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
