---
name: japitown-content
description: Guia para desarrollar y entender el juego Ren'Py Japitown. Usar siempre que se trabaje con quests, eventos, interacciones, door access, skins, rutinas, estados de talk, acciones de locacion, items, mensajes/chat o cualquier sistema del juego.
---

# Japitown — Desarrollo y Funcionamiento

Juego Ren'Py (visual novel). **Todo el contenido nuevo va en español** (código, comentarios,
variables, diálogos, pistas). Este skill está dividido en dos documentos según la necesidad:

## Qué leer

| Necesidad | Archivo |
|---|---|
| **Crear algo nuevo** (quest, evento, interacción, opción de puerta, skin, rutina, estado de talk, acción de locación, item, chat, pensamiento, desbloqueo) | **`creacion.md`** |
| **Entender cómo funciona** un sistema antes de tocarlo | **`funcionamiento.md`** |
| Screens interactivos dentro de quests (objetos clickeables, exploración, `ui.interact`, `sistema_pos`) y notación de sprites | **`creacion_screens.md`** |
| Mapeo de expresiones faciales / atributos de layered image | **`expresiones_referencia.md`** |

Leer solo el archivo relevante para ahorrar contexto; no hace falta cargarlos todos.

## Hechos que NO debés olvidar (errores comunes)

1. **Stats:** los tres NPCs (violet, monica, jasmine) usan `amor` (stat1) y `deseo` (stat2).
   Ya NO existen complicidad, sumisión, adulación, provocación, madurez ni debilidad.
   `Requisito` solo acepta `"amor"`/`"deseo"` (más item, dinero, locacion, horario, dia, mensaje,
   npc_presente, memoria, stat).
2. **Anti-PicklingError:** en `Quest`/`ConfigEtapa`/`ConfigFallo`, nunca lambdas crudas — usar
   función `def` (referencia directa) o `_qc("clave_unica", lambda: ...)`.
3. **Final de un label — `return` vs `jump game_loop`** (el error más caro del proyecto:
   `return` de más cierra el juego al menú principal). Preguntá: *después de este label,
   ¿el caller tiene algo más que hacer?*
   - **No** → es **contenido** (cierre de quest/evento/escena, devuelve al juego libre):
     `window hide` + `$ mostrar_hud()` + **`jump game_loop`**.
   - **Sí** → es **subrutina** (el caller sigue con su lógica: executor de acciones,
     `pensar_mensaje`, label de entrada de locación): **`return`**.

   Ser invocado por `call expression` **no** implica `return` — muchos cierres de quest
   entran así y van con `jump game_loop`. El `game_loop` drena el call stack al inicio
   (`while renpy.call_stack_depth() > 0: renpy.pop_call()`), así que el `jump` nunca
   acumula frames. Detalle completo y casuística en `funcionamiento.md` §0.1.
4. **Modo posicionamiento:** todo botón interactivo con
   `if modo_posicionamiento: action NullAction()`.
5. **Door access** lo decide `TABLA_ACCESO_HABITACION` (umbrales actuales: Violet 50/50/30/10,
   Jasmine y Monica 50/40/15/0 para noche/diurno/dejar_pasar/sale_pasillo). El panel de
   desbloqueos es solo informativo.

## Arquitectura rápida

```
game/script/core/      # motor: quests, events, npcs, talk, actions, locations, skins, time,
                       #        messages, shopping, thoughts, relationships, utils
game/script/characters/<npc>/   # definition, chat/, interaction/, quests/, events/, screens/,
                                #               visual/, talk/
game/script/ui/        # hud/, menus/, base/
game/script/tools/     # position/, celular/
game/script/story/     # intro
```

Sistemas centrales y sus archivos en `funcionamiento.md` §0. Game loop:
`validar_eventos()` → muestra HUD → `pause` → repite; el HUD nunca se destruye, se controla con
`ocultar_hud()` / `mostrar_hud()`.
