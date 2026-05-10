---
name: Registro de Cambios Estructurales
description: Documentación de modificaciones estructurales importantes y nuevos sistemas añadidos al juego Japitown.
---

# Registro de Cambios Estructurales

Este documento sirve como bitácora para registrar aquellas modificaciones importantes en la estructura o en los sistemas base del juego. Su objetivo es mantener un historial claro de cómo evolucionan las mecánicas para facilitar el desarrollo de contenido futuro y evitar romper sistemas existentes.

---

## 1. Sistema Visual de Recompensas en Diálogos de NPCs (Fecha: 22/02/2026)

### Descripción
Se añadió una indicación visual (emojis) a las opciones de respuesta del jugador durante las conversaciones diarias con las chicas. El emoji indica qué estadística (relación, afinidad o personalidad) será incrementada si el jugador elige esa opción. Esta característica puede ocultarse o mostrarse a gusto del jugador a través del menú de cheats.

### Archivos Modificados
- `game/script/core/npcs/npcsystem_core.rpy`
- `game/script/ui/menus/menu_cheats.rpy`
- `game/script/characters/violet/interaction/conversacion_violet.rpy`
- `game/script/characters/jasmine/interaction/conversacion_jasmine.rpy`
- `game/script/characters/monica/interaction/conversacion_monica.rpy`

### Detalles de la Implementación
1. **Lógica Central (`npcsystem_core.rpy`)**:
   - Se introdujo la función `formatear_opcion_recompensa(texto, stat)`.
   - Evalúa si `persistent.mostrar_recompensa` es Verdadero. De ser así, añade un emoji al final del `texto` según el `stat` pasado:
     - "afinidad" -> 🔥 (Fueguito)
     - "relacion" -> 😊 (Carita feliz)
     - "personalidad" -> 😎 (Lentes de sol)

2. **Control UI (`menu_cheats.rpy`)**:
   - Se añadió una fila en la cabecera del menú de cheats "CHEATS - MODIFICAR ESTADÍSTICAS".
   - Contiene un botón que alterna la variable `persistent.mostrar_recompensa` usando `ToggleField`. Se divide en un bloque `if/else` tradicional de Screen Language de Ren'Py para evitar errores de sintaxis en la definición de la pantalla.

3. **Manejo en los Menús de los Scripts de Personajes (`conversacion_*.rpy`)**:
   - En lugar de inyectar directamente la variable del diccionario `_op0['texto']` dentro de la declaración `menu:`, los textos ahora se pre-procesan pasándolos a través de `formatear_opcion_recompensa()` guardándolos en variables temporales (ej. `_txt_op0`).
   - Las variables temporales son las que luego alimentan las opciones visualizadas por el jugador.

## 2. Refactorización del Stat de Personalidad (Fecha: 22/02/2026)

### Descripción
El stat de "personalidad" dejó de ser una estadística individual que poseía cada NPC (como la relación y la afinidad) para convertirse en una única métrica global perteneciente exclusivamente al MC (`mc_personalidad`). Todas las interacciones, opciones de diálogo o eventos que modificaban la "personalidad" del NPC ahora impactan directamente en el MC.

### Archivos Modificados
- `game/script/core/npcs/npcsystem_core.rpy`
- `game/script/characters/violet/definition_violet.rpy`
- `game/script/characters/jasmine/definition_jasmine.rpy`
- `game/script/characters/monica/definition_monica.rpy`
- `game/script/ui/menus/menu_interaction.rpy`

### Detalles de la Implementación
1. **Lógica Central (`npcsystem_core.rpy`)**:
   - Se eliminó `"personalidad"` de la inicialización de estado (`self.estado`) de la clase base `NPC`.
   - Se reescribió `modificar_personalidad()` para que no modifique ni sincronice variables locales ni `store.[npc]_personalidad`. En su lugar, todo argumento `cantidad` se suma directamente a la variable global `store.mc_personalidad`.

2. **Definición de NPCs (`definition_[nombre].rpy`)**:
   - Se eliminaron las sentencias `default [nombre]_personalidad = 0`.
   - Se eliminaron las líneas que cargaban el estado guardado para la personalidad.
   - Se removió el texto descriptivo del stat desde los atributos (`agregar_atributo("personalidad", ...)`).

3. **Interfaz (`menu_interaction.rpy`)**:
   - Se eliminó toda la representación visual de la barra de personalidad de los NPCs en la pantalla `estadisticas_npcs`.

## 3. Implementación Estructural del Evento 2 de Violet (Fecha: 23/02/2026)

### Descripción
Se creó la estructura base y narrativa de "placeholder" para el Evento 2 de Violet. Este evento tiene la particularidad de ejecutarse automáticamente durante la noche al ir a dormir, en la cual se revisa si la Quest 3.2 de Violet ha sido completada previamente.

### Archivos Modificados/Creados
- **[NUEVO]** `game/script/characters/violet/events/evento2_violet.rpy`
- **[MODIFICADO]** `game/script/core/time/timesystem_core.rpy`

### Detalles de la Implementación
1. **Definiciones y Variables (`evento2_violet.rpy`)**:
   - Creación de variables guardables: `violet_evento2_completado` y `violet_evento2_repetir`.
   - Implementación de labels narrativos vacíos: `evento2_violet` (disparador inicial) y `evento2_violet_repetir` (versión repetible para su futura integración con otro sistema).

2. **Integración con Sistema de Tiempo (`timesystem_core.rpy`)**:
   - Dentro del bloque `label accion_dormir:` se inyectó una validación del estado del sistema de quests.
   - Antes de procesar el salto de día, el sistema corrobora que exista la quest ID `"violet_questprincipal_3_2"` y que su atributo de completado devuelva Verdadero.
   - En caso positivo, si aún no se había completado el evento (`violet_evento2_completado` es Falso), ocurre un `jump` forzado al label `evento2_violet`.

## 4. Sistema de Pensamientos al Dormir (Fecha: 23/02/2026)

### Descripción
Se añadió un sistema de "Pensamientos" integrado con la mecánica de dormir. Al interactuar con la cama, si hay pensamientos desbloqueados, aparece un menú con las opciones "Dormir" y "Pensar". "Pensar" abre un submenú con los pensamientos disponibles (asociados a NPCs), que llevan a labels narrativos repetibles. Tras completar el pensamiento, se ejecuta automáticamente la función dormir. Si no hay pensamientos disponibles, la cama funciona igual que antes (sin menú intermedio).

### Archivos Creados/Modificados
- **[NUEVO]** `game/script/core/thoughts/pensamiento_system.rpy`
- **[MODIFICADO]** `game/script/core/time/timesystem_core.rpy`
- **[MODIFICADO]** `game/script/characters/violet/events/evento2_violet.rpy`

### Detalles de la Implementación
1. **Sistema Central (`pensamiento_system.rpy`)**:
   - Diccionario `pensamientos_registrados` como catálogo central (init 5).
   - Función `registrar_pensamiento(id, npc_id, nombre, label, condicion)` para registrar pensamientos con una condición lambda que determina su disponibilidad.
   - Función `obtener_pensamientos_disponibles()` que filtra y retorna solo los pensamientos cuya condición es True.
   - Registro del primer pensamiento de Violet (init 6): `"violet_pensamiento_1"`, condición `violet_evento2_completado`, apunta al label `evento2_violet_repetir`.
   - Screen `menu_pensamientos` con diseño modal consistente (fondo `#1a1a2e`, botones teal `#009688`), itera dinámicamente sobre el dict de pensamientos y retorna el label seleccionado o `"volver"`.

2. **Integración con Dormir (`timesystem_core.rpy`)**:
   - En `label accion_dormir`, después de los checks de restricción y paquete, se llama a `obtener_pensamientos_disponibles()`.
   - Si hay pensamientos disponibles, se muestra un `menu:` con "Dormir" y "Pensar".
   - "Dormir" continúa el flujo normal. "Pensar" muestra `menu_pensamientos`; si el jugador selecciona un pensamiento se ejecuta con `call expression`; si elige "Volver" regresa al menú con `jump .menu_cama`.
   - Ambos caminos convergen en el flujo de dormir (animación → eventos nocturnos → `dormir()` → despertar).

3. **Adaptación del Evento 2 (`evento2_violet.rpy`)**:
   - El label `evento2_violet_repetir` fue cambiado de `jump game_loop` a `return`, permitiendo que el sistema de pensamientos recupere el control y continúe con el flujo de dormir automáticamente.

## 5. Modificaciones al Sistema de Chat/Mensajes (Fecha: 24/02/2026)

### Descripción
Se realizaron 8 mejoras al sistema de mensajes: indicador "escribiendo" por cada mensaje individual (en lugar de uno solo para todos), duración dinámica basada en longitud del texto, auto-selección de grupo único, auto-envío de respuesta única, iconos de NPC en contactos/chat, validación de condiciones de quests en tiempo real, sistema de horario de respuesta por grupo, y sistema de bloqueo de chat.

### Archivos Modificados
- `game/script/core/messages/messagesystem_core.rpy`
- `game/script/ui/hud/hud_mensajes.rpy`
- `game/script/core/time/timesystem_core.rpy`

### Detalles de la Implementación

1. **Escribiendo por mensaje + duración dinámica (`hud_mensajes.rpy`)**:
   - Nueva variable `_msg_tiempo_escribiendo` (default 1.5) controla la duración del timer.
   - Nueva función `calcular_tiempo_escribiendo(texto)` retorna 0.8s (≤20 chars), 1.2s (≤50), 1.8s (≤100), 2.5s (>100).
   - `_procesar_respuesta` filtra mensajes vacíos, agrega `mensaje_siguiente` a la cola, y calcula el tiempo del primer mensaje antes de activar el indicador.
   - `_finalizar_escribiendo` ahora hace pop del primer mensaje de la cola. Si quedan más, recalcula el tiempo y re-activa el indicador. Si no, limpia el estado.
   - El timer screen usa `_msg_tiempo_escribiendo` en lugar del valor fijo 1.5.

2. **Auto-selección y auto-envío (`hud_mensajes.rpy`)**:
   - Nueva función `_abrir_selector_respuesta(npc_id)` reemplaza el `Show("selector_respuesta")` directo.
   - Si hay exactamente 1 grupo pendiente y no hay grupo activo, lo auto-selecciona.
   - Si tras seleccionar hay exactamente 1 opción visible, auto-envía sin mostrar el selector.
   - El botón "Responder" ahora usa `Function(_abrir_selector_respuesta, npc_id)`.

3. **Iconos NPC (`hud_mensajes.rpy`)**:
   - En lista de contactos (45x45) y header del chat (35x35), se intenta cargar `images/hud/pista_{npc_id}.png` con `renpy.loadable()`.
   - Si existe, se muestra la imagen con zoom apropiado (0.175 / 0.137). Si no, fallback al emoji anterior.

4. **Validación en tiempo real (`timesystem_core.rpy`)**:
   - Se agregó `actualizar_quests()` dentro de `avanzar_horario()`, después de `verificar_fallos_quests`.
   - Las condiciones de quests ahora se verifican cada vez que avanza el horario, no solo al dormir.

5. **Horario de respuesta (`messagesystem_core.rpy`)**:
   - Nuevo parámetro opcional `horario_respuesta` en `GrupoMensajes.__init__` (lista de horarios válidos o None).
   - Nuevo método `_horario_valido(grupo)` en `ChatNPC` que verifica `horario_actual in grupo.horario_respuesta`.
   - `puede_responder()` ahora verifica horario para grupo activo y grupos pendientes.
   - En el selector de respuesta, los grupos pendientes se filtran por horario válido.
   - Mensaje "responderá más tarde" cuando hay pendientes pero el horario no es válido.

6. **Bloqueo de chat (`messagesystem_core.rpy`)**:
   - Nuevo atributo `bloqueado = False` en `ChatNPC.__init__`.
   - `puede_responder()` retorna False si `bloqueado` es True (usa `getattr` para compatibilidad con saves).
   - Funciones de utilidad `bloquear_chat_npc(npc_id)` y `desbloquear_chat_npc(npc_id)`.

## 6. Refactorización de Stats NPC y Conversaciones Secuenciales (Fecha: 27/02/2026)

### Descripción
Los stats genéricos "relación" y "afinidad" fueron reemplazados por stats específicos para cada NPC. Además, el sistema de conversaciones diarias ("hablar") pasó de mostrar interacciones de forma aleatoria a mostrarlas en orden secuencial. Se eliminó la interacción "besar" del sistema.

### Stats por NPC
| NPC     | Stat 1 (antes "relación") | Stat 2 (antes "afinidad") |
|---------|---------------------------|---------------------------|
| Violet  | Complicidad               | Sumisión                  |
| Jasmine | Adulación                 | Provocación               |
| Monica  | Madurez                   | Debilidad                 |

### Archivos Modificados
- `game/script/core/npcs/npcsystem_core.rpy`
- `game/script/core/quests/questsystem_core.rpy`
- `game/script/characters/violet/definition_violet.rpy`
- `game/script/characters/jasmine/definition_jasmine.rpy`
- `game/script/characters/monica/definition_monica.rpy`
- `game/script/characters/violet/interaction/conversacion_violet.rpy`
- `game/script/characters/jasmine/interaction/conversacion_jasmine.rpy`
- `game/script/characters/monica/interaction/conversacion_monica.rpy`
- `game/script/characters/violet/quests/quest_violet.rpy`
- `game/script/characters/violet/quests/violet_quest_0.rpy`
- `game/script/characters/violet/quests/violet_quest_01.rpy`
- `game/script/characters/jasmine/quests/jasmine_quest_0.rpy`
- `game/script/characters/monica/quests/monica_quest_0.rpy`
- `game/script/characters/violet/chat/chat_violet.rpy`
- `game/script/characters/jasmine/chat/chat_jasmine.rpy`
- `game/script/characters/monica/chat/chat_monica.rpy`
- `game/script/ui/menus/menu_cheats.rpy`
- `game/script/ui/menus/menu_interaction.rpy`
- `game/script/ui/hud/hud_mensajes.rpy`
- `game/script/ui/hud/hud_navigation.rpy`

### Detalles de la Implementación

1. **Clase NPC (`npcsystem_core.rpy`)**:
   - Se añadieron parámetros `nombre_stat1` y `nombre_stat2` al `__init__` (por defecto `"relacion"` y `"afinidad"`).
   - `self.estado` usa los nombres configurables como claves en lugar de los hardcodeados.
   - `modificar_relacion` y `modificar_afinidad` fueron reemplazados por `modificar_stat1` y `modificar_stat2`.
   - Se eliminó `puede_besar()` y la interacción "besar" de `interactuar_con_npc`.
   - `formatear_opcion_recompensa` ahora mapea los 6 stats específicos a sus emojis (😊 para stat1, 🔥 para stat2).
   - `obtener_stat1`/`obtener_stat2` y `cambiar_stat1`/`cambiar_stat2` usan los nombres dinámicos.

2. **Sistema de Quests (`questsystem_core.rpy`)**:
   - `Requisito.verificar()` ahora acepta tanto los tipos genéricos ("relacion"/"afinidad") como los específicos ("complicidad", "sumision", "adulacion", "provocacion", "madurez", "debilidad").
   - `formatear_requisito` genera texto descriptivo usando el nombre del tipo directamente.
   - El handler de fallo usa `modificar_stat1` en lugar de `modificar_relacion`.

3. **Variables por defecto**:
   - `violet_complicidad` / `violet_sumision` (antes `violet_relacion` / `violet_afinidad`)
   - `jasmine_adulacion` / `jasmine_provocacion` (antes `jasmine_relacion` / `jasmine_afinidad`)
   - `monica_madurez` / `monica_debilidad` (antes `monica_relacion` / `monica_afinidad`)

4. **Conversaciones secuenciales**:
   - Cada NPC tiene un índice `store.[npc]_hablar_indice` (default 0).
   - En lugar de `renpy.random.choice`, se usa el índice para seleccionar la pregunta: `preguntas[store.[npc]_hablar_indice % len(preguntas)]`.
   - El índice se incrementa después de cada interacción y cicla automáticamente.

5. **UI actualizada**:
   - `menu_interaction.rpy`: Usa `npc.nombre_stat1` y `npc.nombre_stat2` dinámicamente.
   - `menu_cheats.rpy`: Muestra los nombres de stats específicos por NPC.
   - `hud_mensajes.rpy`: Reconoce los 6 nuevos tipos de recompensa.
   - `hud_navigation.rpy`: Debug HUD muestra las nuevas variables.

## 7. Nuevos Stats: Progreso y Relación (Fecha: 27/02/2026)

### Descripción
Se añadieron dos stats nuevos al sistema de NPCs:
- **Progreso**: Se incrementa automáticamente en +1 al completar cada quest. No es visible para el jugador.
- **Relación**: Es la suma de stat1 + stat2 + progreso. Es el valor visible principal para el jugador.

### Archivos Modificados
- `game/script/core/npcs/npcsystem_core.rpy`
- `game/script/core/quests/questsystem_core.rpy`
- `game/script/characters/violet/definition_violet.rpy`
- `game/script/characters/jasmine/definition_jasmine.rpy`
- `game/script/characters/monica/definition_monica.rpy`
- `game/script/ui/menus/menu_interaction.rpy`
- `game/script/ui/menus/menu_cheats.rpy`
- `game/script/ui/hud/hud_navigation.rpy`

### Detalles de la Implementación

1. **Clase NPC (`npcsystem_core.rpy`)**:
   - Se añadió `"progreso": 0` a `self.estado`.
   - Nuevo método `modificar_progreso(cantidad)` con sincronización a `store.{npc_id}_progreso`.
   - Nuevo método `obtener_relacion_total()` que retorna `stat1 + stat2 + progreso`.
   - Funciones helper globales: `obtener_progreso(npc_id)`, `obtener_relacion_total(npc_id)`, `incrementar_progreso(npc_id)`.

2. **Auto-incremento en Quests (`questsystem_core.rpy`)**:
   - En `Quest.completar()`, tras marcar la quest como completada, se llama `npc.modificar_progreso(1)`.
   - Esto cubre automáticamente todas las rutas de completar quests sin necesidad de modificar cada quest individual.

3. **Variables por defecto**: `violet_progreso`, `jasmine_progreso`, `monica_progreso` (default 0).

4. **UI - Menú de Interacción (`menu_interaction.rpy`)**:
   - Muestra "Relación: X" como stat principal visible (la suma total).
   - Debajo muestra los stats individuales con emojis únicos por NPC:
     - Violet: 🤝 Complicidad / 🔒 Sumisión
     - Jasmine: 💐 Adulación / 🔥 Provocación
     - Monica: 🌟 Madurez / 💧 Debilidad

5. **Cheats (`menu_cheats.rpy`)**: Controles de +1/-1/Reset para progreso de cada NPC.

6. **Debug HUD (`hud_navigation.rpy`)**: Muestra valores de progreso en el panel de debug.

## 8. UI Compartida del Celular, Herramienta de Ajuste y Fix de Layout del Chat (Fecha: 02/03/2026)

### Descripción
Se creó un sistema de componentes UI reutilizables para todas las pantallas del celular, una herramienta de desarrollo para ajustar posición/tamaño de los menús del celular en tiempo real, y se corrigió un bug crítico de layout en `pantalla_chat` donde la barra de respuesta era invisible.

### Archivos Creados/Modificados
- **[NUEVO]** `game/script/ui/hud/celular_ui_comun.rpy`
- **[NUEVO]** `game/script/tools/celular/ajuste_celular.rpy`
- **[NUEVO]** `game/script/tools/celular/panel_ajuste_celular.rpy`
- **[MODIFICADO]** `game/script/ui/hud/hud_mensajes.rpy`
- **[MODIFICADO]** `game/script/ui/hud/hud_celular.rpy`

### Detalles de la Implementación

1. **Componentes UI Comunes (`celular_ui_comun.rpy`)**:
   - Constantes del área del celular: `CEL_XPOS=630`, `CEL_YPOS=0`, `CEL_WIDTH=660`, `CEL_HEIGHT=1080`.
   - Screen `_celular_barra_status()`: barra superior (32px) con horario del juego e iconos decorativos.
   - Screen `_celular_app_header(titulo, icono, accion_volver)`: header de app (55px) con botón volver, icono y título.
   - Todas las pantallas del celular (`menu_celular`, `lista_contactos_mensajes`, `pantalla_chat`, `resumen_recompensas`) usan estos componentes compartidos.

2. **Herramienta de Ajuste Celular (`ajuste_celular.rpy`)**:
   - Modelo de datos: clases `ContainerCelular`, `ElementoInterno`, `SistemaAjusteCelular`.
   - `SistemaAjusteCelular` (instancia: `sistema_ajuste_cel`): registro central con métodos `registrar_container()`, `registrar_elemento()`, `obtener_container()`, `obtener_elementos_de()`.
   - Containers registrados (init 1): `menu_celular`, `lista_contactos_mensajes`, `pantalla_chat`, `selector_respuesta`, `resumen_recompensas`, `panel_galeria`, `panel_stats_mc`, `panel_tienda`, `panel_inventario`, `panel_pistas`, `estadisticas_npcs`, `menu_cheats`.
   - Sistema de undo con `obtener_estado()` / `restaurar_estado()` (máx 20 estados).
   - Área de trabajo configurable (`ajuste_cel_area_x/y/w/h`), por defecto 630x0x660x1080.
   - Exportación a archivos `.txt` (sesión + historial acumulativo) en raíz del proyecto.
   - Funciones de control: `activar_ajuste_celular()`, `desactivar_ajuste_celular()`, `toggle_ajuste_celular()`, `ajuste_cel_cambiar_screen()`, `ajuste_cel_modificar()`.
   - Input numérico directo con `ajuste_cel_abrir_input()` / `ajuste_cel_aplicar_input()`.

3. **Panel UI de Ajuste (`panel_ajuste_celular.rpy`)**:
   - Screen `panel_ajuste_celular`: panel lateral derecho (380px, zorder 300, modal).
   - Pestañas: Container / Elementos / Área de trabajo.
   - Selector de pantalla activa con lista desplegable.
   - Controles +/- y input directo para todos los atributos.
   - Botones: Exportar, Deshacer, Limpiar, Cerrar.

4. **Integración con pantallas del celular**:
   - Todas las pantallas del celular usan variables del área de trabajo (`ajuste_cel_area_x/y/w/h`) en lugar de constantes hardcodeadas para posición y tamaño.
   - Cada screen obtiene su container con `sistema_ajuste_cel.obtener_container(screen_name) if modo_ajuste_celular else None`.
   - En modo ajuste, los botones de acción se bloquean con `NullAction()`.

5. **Fix de layout en `pantalla_chat` (`hud_mensajes.rpy`)**:
   - **Bug**: el viewport de mensajes tenía `yfill True` dentro de un vbox. En Ren'Py, `yfill True` consume todo el alto disponible del padre sin dejar espacio para elementos hermanos posteriores, empujando la barra de respuesta fuera del área visible.
   - **Fix**: se reemplazó `yfill True` por un `ysize` calculado explícitamente: `ajuste_cel_area_h - 32 (status) - 55 (header) - 50 (footer) - 50 (margen inferior)`.
   - Se fijó `ysize 50` en el frame del footer para consistencia con el cálculo.
   - **Importante para futuras pantallas**: nunca usar `yfill True` en un viewport que tenga elementos hermanos después en un vbox. Siempre calcular el ysize explícitamente restando las alturas fijas de los demás elementos.

### Patrón de Layout del Celular (referencia)
Todas las pantallas del celular siguen esta estructura:
```
frame:
    xpos ajuste_cel_area_x
    ypos ajuste_cel_area_y
    xsize ajuste_cel_area_w
    ysize ajuste_cel_area_h
    background None
    padding (0, 0)

    vbox:
        xfill True
        use _celular_barra_status()         # 32px fijo
        use _celular_app_header(...)        # 55px fijo
        viewport:                           # ysize calculado (NO yfill True)
            ...contenido scrollable...
        frame:                              # footer fijo (si aplica)
            ysize 50
            ...
```
