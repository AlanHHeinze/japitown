# Japitown — Skill de Funcionamiento

> Cómo funciona **internamente** cada sistema del juego. Leer esto para entender la
> lógica de algo antes de modificarlo. Para *crear* contenido nuevo, ver `creacion.md`.
>
> Todo el código, comentarios y variables están en **español**.

---

## 0. Arquitectura y Game Loop

```
game/script/
├── core/                 # Motor del juego
│   ├── quests/           # questsystem_core, restriccion_quest_system, questsystem_memories, quest_strings
│   ├── events/           # eventsystem_core
│   ├── npcs/             # npcsystem_core, npcsystem_interactions, npcsystem_interactions_basic
│   ├── talk/             # talksystem_core, talksystem_labels, talksystem_screens
│   ├── actions/          # actionsystem_core, actions_catalog, actionsystem_screen
│   ├── locations/        # locationsystem_core, locations_house, door_access_system, door_relation_system, movesystem_validation
│   ├── relationships/    # relationship_unlocks
│   ├── shopping/         # shopping_system, items_shopping, usar_casco_vr
│   ├── skins/            # skinsystem_core
│   ├── time/             # timesystem_core, despertar_system
│   ├── messages/         # messagesystem_core
│   ├── thoughts/         # pensamiento_system
│   └── utils/            # transforms, layers, camera
├── characters/<npc>/     # definition, chat/, interaction/, quests/, events/, screens/, visual/, talk/
├── ui/                   # hud/, menus/, base/
├── tools/                # position/, celular/
├── tutorial/             # tutorial.rpy
└── story/                # intro
```

### El game loop

```renpy
label game_loop:
    window hide
    $ validar_eventos()           # hace aparecer/activar eventos cuyas condiciones se cumplen
    if not renpy.get_screen("navegacion_locaciones_con_hud"):
        show screen navegacion_locaciones_con_hud
    pause                         # espera input del jugador
    jump game_loop
```

El HUD (`navegacion_locaciones_con_hud`) **nunca se destruye**. Se controla con
`ocultar_hud()` / `mostrar_hud()` (ocultan/muestran contenido + desactivan/activan modal).

El HUD lanza labels con `Call(...)` al clickear hotspots o sprites NPC:
- Hotspot **MOVE** → `accion_hotspot_move`
- Hotspot **ACTION** → `accion_hotspot_action`
- Sprite NPC → `interaccion_<npc_id>`
- Acción de locación → `accion_locacion_ejecutar`

**Regla de oro:** cualquier label invocado por el sistema vía `call expression` **debe terminar
en `return`** para devolver control al game loop. Los labels que terminan flujo propio hacen
`window hide` + `$ mostrar_hud()` + `jump game_loop`.

---

## 1. Sistema de Tiempo — `timesystem_core.rpy`

| Horario | Valor | | Día | Valor |
|---|---|---|---|---|
| Mañana | 0 | | Lunes…Domingo | 0…6 |
| Tarde | 1 | | | |
| Noche | 2 | Variables: `horario_actual`, `dia_semana_actual`, `dia_actual` (1-31), |
| Trasnoche | 3 | `dias_totales` (contador absoluto para quests), `estacion_actual`, `año_actual` |

Calendario: 31 días/estación, estaciones `["Primavera","Verano","Otoño","Invierno"]`.

### `avanzar_horario()` (Mañana→Tarde→Noche→Trasnoche, no avanza más allá de 3)
En orden: entrega paquete si el repartidor estaba en la mañana → `horario_actual += 1` →
actualiza background con fade → `actualizar_rutinas_npcs()` (los NPCs se reubican al instante) →
`verificar_fallos_quests()` → `actualizar_quests()` → `verificar_mensajes_en_espera()`.

### `dormir()` (resetea a Mañana del día siguiente)
En orden: guarda horario previo → `horario_actual = 0` → avanza `dia_semana_actual`,
`dia_actual`, `dias_totales` → repone stock si es Lunes → resetea entrenamiento/trabajo →
`resetear_interacciones_todos_npcs()` → `evaluar_todas_rutinas_especiales_dia()` →
`actualizar_rutinas_npcs()` → `actualizar_quests()` →
`verificar_mensajes_horarios_omitidos()` (entrega mensajes que debían llegar esa noche) →
`verificar_mensajes_en_espera()` → entregas de compras → resetea acciones de locación
(`resetear_diario()`, y `resetear_semanal()` si es Lunes) → **asigna nuevos estados de talk**
(`decrementar_estados_especiales` + `asignar_estado_aleatorio` para violet/monica/jasmine).

El **label `accion_dormir`** envuelve a `dormir()` y antes/después corre hooks: bloqueo por
restricción, bloqueo por mensaje prioritario, despertar anticipado por mensaje prioritario,
entregas pendientes, menú de **Pensamientos**, animación de dormir, **eventos nocturnos**
(p.ej. `evento2_violet`), y triggers de quests al despertar (08_a, 09_a/09_b, evento 03).
Termina con `call mensajes_al_despertar`.

---

## 2. Sistema de NPCs — `npcsystem_core.rpy`

Clase `NPC(id, nombre, nombre_completo, sprite, nombre_stat1="amor", nombre_stat2="deseo")`.
**Todos los NPCs (violet, monica, jasmine) usan `amor` (stat1) y `deseo` (stat2).**
*(Los nombres antiguos complicidad/sumisión/adulación/provocación/madurez/debilidad ya NO existen.)*

### Estado del NPC (`npc.estado`)
- `amor` (stat1), `deseo` (stat2): 0-100, clamp automático.
- `progreso`: oculto, +1 al completar cada quest del NPC.
- `conocido`, `disponible`.

`relacion_total = amor + deseo + progreso` (valor visible principal al jugador).

### Sincronización con variables guardables
`modificar_stat1/stat2/progreso` actualizan `npc.estado` **y** escriben la variable default
`{npc_id}_{stat}` (ej: `violet_amor`, `monica_deseo`, `jasmine_progreso`) vía `setattr(store, ...)`.
Las funciones del NPC leen de `npc.estado`; los `default` existen para el save y se
sincronizan en `inicializar_<npc>()`.

### Helpers globales
```python
obtener_stat1(npc_id) / obtener_stat2(npc_id)       # → int
cambiar_stat1(npc_id, n) / cambiar_stat2(npc_id, n) # modifica + notifica
obtener_progreso(npc_id) / incrementar_progreso(npc_id)
obtener_relacion_total(npc_id)
interactuar_con_npc(npc_id, "hablar"|"coquetear")   # +1 stat, 1 vez/día
```

### Rutinas (qué locación ocupa el NPC)
`obtener_locacion_rutina()` resuelve por prioridad:
1. **Override de evento** (`sistema_events.obtener_override_rutina`)
2. **Rutina de quest** (`npc.rutinas_quest`, dict `{(dia,horario): locacion}`)
3. **Rutina especial del día** (`RutinaEspecial`: fuera, ducha — con probabilidad/cooldown)
4. **Rutina base** (`npc.rutinas`, seteada en `definition_<npc>.rpy`)

`RutinaEspecial(id, locacion, sprite, posicion, probabilidad, horarios, dias, condicion, nombre)`:
se evalúa al inicio de cada día. Las rutinas "fuera"/"baño" tienen cooldown de 2 días y no
pueden coexistir el mismo día; conflictos de ducha (Violet/Jasmine) se resuelven al azar.

### Sprite y posición visuales
Cada `definition_<npc>.rpy` tiene `obtener_sprite_rutina_<npc>()` y `obtener_posicion_rutina_<npc>()`
con prioridad: **0)** pasillo (door access) → **1)** skin activo de quest/evento
(`obtener_sprite_idle_rutina`) → **2)** rutina especial → **3)** rutina visual base
(`<npc>_rutinas_visuales[(dia,horario)]`, seteada con `establecer_rutina_visual_<npc>`).

---

## 3. Sistema de Skins — `skinsystem_core.rpy`

Grupos oficiales: `["base", "entrenamiento", "bikini", "pijama", "ropa_interior", "vestidos"]`.

- `Skin(id, npc_id, nombre, grupo, descripcion, condicion_desbloqueo, sprite_idle, sprite_menu, posicion)`.
  `id` por convención `{npc}_{grupo}_{variante}` (ej: `violet_pijama_base`).
- `skins_activos` (guardable): `{npc_id: {grupo: skin_id}}` — un skin activo por grupo.
- `rutinas_skin_grupos`: `{npc_id: {(dia,horario): grupo | {"grupo","condicion"}}}` — qué grupo de
  skin usa cada rutina. Si la entrada tiene `condicion` y falla, cae a `"base"`.

### Resolución del sprite activo
`obtener_grupo_rutina_actual(npc)` da el grupo según `(dia,horario)` →
`obtener_sprite_idle_por_grupo` / `obtener_sprite_menu_por_grupo` buscan el skin activo de
ese grupo (con fallback a base). Por eso un skin "se ve" cuando: (a) está registrado, (b) está
activo en `skins_activos`, y (c) la rutina actual mapea a ese grupo.

### API clave
```python
desbloquear_skin(skin_id)        # marca el skin como activo en su grupo (llamar desde quests)
activar_skin(npc_id, skin_id)
desactivar_skin(npc_id, grupo=None)
cuerpo_activo(npc_id)            # → "c_rbase" | "c_pijama" según grupo activo (GRUPO_CUERPO_MAP)
```

`GRUPO_CUERPO_MAP` mapea grupo → prefijo de cuerpo en la layered image (solo `pijama` usa
`c_pijama`; el resto `c_rbase`). Usar `cuerpo_activo()` al inicio de una quest para mostrar el
sprite correcto sin asumir ropa.

---

## 4. Sistema de Quests — `questsystem_core.rpy`

### Etapas (avance automático)
```
1 INICIALIZACION → 2 ESPERA → 3 CONDICIONES → 4 RUTINA → 5 BOTON_LISTO
→ 6 VALIDACION → 7 DESARROLLO → 8 MEMORIAS → 9 FINALIZACION
```
- **2 ESPERA**: pasan `dias_espera` (medidos con `dias_totales`) y, opcional, `condicion_espera()`.
- **3 CONDICIONES**: se cumplen todos los `requisitos` (lista de `Requisito`).
- **4 RUTINA**: se aplica `rutina_quest` (y `rutinas_adicionales`) sobre `npc.rutinas_quest`.
- **5 BOTON_LISTO**: la quest está lista; el botón/opción para iniciarla aparece.
- **6 VALIDACION**: al intentar ejecutar, se chequea `validacion_especial`; si falla, muestra
  sus mensajes y no avanza. `intentar_ejecutar()` → `(exito, mensajes)`.
- **7 DESARROLLO**: corre el label `quest_<id>`.
- **8-9**: `completar()` restaura rutina, aplica `retorno`, marca completada, `progreso +1`,
  dispara chat (`trigger "quest"`), e inicia la siguiente quest del mismo NPC
  (la que tenga `quest_anterior == este_id`).

El avance ocurre en `actualizar()` (llamado por `actualizar_quests()` en avanzar_horario/dormir).

### `Requisito(tipo, mensaje, **params)` — tipos válidos en `verificar()`
`"amor"` (npc_id, valor) · `"deseo"` (npc_id, valor) · `"stat"` (stat_id, valor → `mc_<stat>`) ·
`"item"` (item_id, cantidad) · `"dinero"` (valor) · `"memoria"` (categoria, clave, valor) ·
`"locacion"` (locacion_id) · `"horario"` (horario_id) · `"dia"` (dia_id) ·
`"mensaje"` (grupo_id → `grupo_completado`) · `"npc_presente"` (npc_id, locacion_id).
**No existen tipos por stat antiguo (complicidad, etc.).**

### `config_etapas={ETAPA_X: ConfigEtapa(...)}`
`ConfigEtapa(pista, que_hacer, mensaje_despertar, trigger_mensaje, accion_al_entrar)`.
- Campos de texto pueden ser str o callable; se traducen con `renpy.translate_string`.
- `trigger_mensaje=(grupo_chat_id, npc_id)` dispara un chat al **entrar** a esa etapa.
- `accion_al_entrar` callable al entrar a la etapa.
Prioridad de mensajes: `config_fallo` (si hubo fallo) > `config_etapas` > genéricos.

### `config_fallo=ConfigFallo(condicion, trigger_mensaje, cambio_relacion, pista, que_hacer)`
Verificado en `verificar_fallo()` solo en etapas RUTINA/BOTON_LISTO, máx 1 vez/día.
Al fallar: marca `fallo_ocurrido`, dispara chat de fallo, aplica `cambio_relacion=(npc, n)`
sobre stat1.

### Serialización: `_qc()` / `CallableRef` (anti-PicklingError)
Las quests se **guardan en el save**. Python no puede picklear lambdas anónimas. Solución:
- Funciones con `def` (picklables) → referencia directa.
- Lambdas inline → envolver con `_qc("clave_unica", lambda: ...)`. `_qc` registra la lambda en
  `_quest_callable_registry` (reconstruido en cada arranque) y devuelve un `CallableRef` que solo
  guarda la clave. **Nunca poner una lambda cruda en Quest/ConfigEtapa/ConfigFallo.**

### Rutinas de quest
`rutina_quest={(dia,horario): RutinaQuest(locacion, sprite, posicion)}`,
`rutinas_adicionales={npc_id: {...}}`, con `prioridad_rutina` (mayor gana ante conflicto entre
quests activas). Se aplican al entrar a etapa RUTINA y se limpian al completar.

---

## 5. Sistema de Eventos — `eventsystem_core.rpy`

Más simples que las quests. Estados:
```
OCULTO → VISIBLE → ACTIVO → COMPLETADO
```
Tipos: `TIPO_EVENT_ESPORADICO` (se completa y desaparece) / `TIPO_EVENT_PERSISTENTE`
(reaparece mientras la condición se cumpla).

`Event(id, nombre, tipo, prioridad, condicion_aparicion, condicion_activacion, condicion_duracion,
label_efecto, modificaciones, descripcion, npc_id, mensaje_pista, mensaje_que_hacer,
mensaje_despertar, config_etapas, on_aparicion)`.

- `condicion_aparicion()` → cuándo pasa a VISIBLE. `None` = siempre.
- `condicion_activacion()` → cuándo pasa a ACTIVO. `None` = autoactiva al aparecer.
- `on_aparicion()` → callback que se ejecuta **una vez** al volverse visible (lo dispara
  `validar_eventos()` en el game loop). Útil para "anclar" el día (`dias_totales`) de inicio.
- `config_etapas={ESTADO_EVENT_X: ConfigEtapa(...)}` igual que quests pero por estado.

`validar_eventos()` (game loop) hace aparecer y activar eventos. `completar()` limpia
modificaciones, dispara chat (`trigger "event"`) y bloquea rollback.

### `modificaciones` (cambios temporales del mundo)
```python
modificaciones={
    "rutinas": {"violet": {(0,2): "casa_hviolet"}},   # override de ubicación NPC
    "fondos":  {"casa_living": "images/bg/special.png"},# override de background
    "bloqueos": ["avanzar_tiempo"],                     # acciones bloqueadas globalmente
}
```
El sistema resuelve por `prioridad` (mayor gana). Se aplican al aparecer y se quitan al completar.

---

## 6. Sistema de Talk — `talksystem_core.rpy` + `talksystem_labels.rpy`

Reemplaza al viejo "hablar secuencial". Cada NPC tiene un `ConfigTalkNPC` registrado en
`sistema_talk`. La conversación diaria ("Hablar", 1 vez/día) presenta **5 opciones base** fijas:
```
OPCIONES_BASE_IDS = ["complacerla", "provocarla", "escucharla", "hablarle", "adularla"]
```

### EstadoTalk — el "ánimo" del NPC
`EstadoTalk(id, nombre, intro, efectos, mensaje, es_especial, jerarquia, dias_duracion,
estados_posteriores, condicion)`.
- `efectos`: dict `opcion_id → resultado_id`. Cada estado distribuye los resultados entre las 5
  opciones (qué da cada elección con ese ánimo).
- `intro`: narración antes del menú. `mensaje`: fragmento para el texto resultado.
- `condicion` (callable → bool): si está, el estado solo entra al pool cuando se cumple.

`resultado_id` → stat (`RESULTADO_A_STAT`):
```
+1_amor:(amor,1)  +2_amor:(amor,2)  +4_amor:(amor,4)
+1_deseo:(deseo,1) +2_deseo:(deseo,2)
-2_amor:(amor,-2)  -1_deseo:(deseo,-1)  nada:None
```
`RESULTADO_TEXTO` da el texto/emoji (❤️ amor, 💋 deseo).

### Tres clases de estados
1. **Generales** (`estados_generales_ids`): pool del que se elige uno al azar **al dormir**
   (`asignar_estado_aleatorio`). Filtra por `condicion` antes de elegir.
2. **Condicionales**: están en `estados_generales_ids` pero con `condicion` (ej:
   `violet_buen_humor` requiere `violet_amor >= 15`). Solo entran al pool si se cumplen.
3. **Especiales** (`es_especial=True`, con `jerarquia` y `dias_duracion`): se activan desde
   quests/eventos/items con `activar_estado_especial_npc(npc, estado_id, dias?)`. Tienen
   prioridad sobre los generales (gana la mayor `jerarquia`). Se decrementan al dormir; pueden
   marcarse "consumido" tras usarlos (`consumir_estado_especial`).

`obtener_estado_activo(npc)`: especial de mayor jerarquía > estado general del día > asigna uno.

### Opciones especiales — `OpcionEspecialTalk`
Opción extra que aparece bajo condición (ítem, estado, inteligencia, etc.):
`OpcionEspecialTalk(id, texto, condicion, mensaje_opcion, resultado_id, item_requerido,
item_consumible, estado_posterior_npc, recompensa_extra)`. Sus callables se excluyen del pickle
(`__getstate__`) y se recrean al inicio (vive en `define sistema_talk`).

### Memoria del MC e inteligencia/carisma
- `actualizar_memoria_mc` recuerda el resultado de cada `(estado, opcion)`; límite =
  `mc_inteligencia` entradas por NPC. En el menú, las opciones recordadas muestran su resultado.
- `mc_carisma >= 2`: muestra preview ("?") de una opción desconocida.
- `mc_carisma >= 5`: permite **reconsiderar** una vez si el resultado sería negativo.

### Flujo del label `talk_iniciar`
Chequea bloqueo/ya-habló → obtiene estado activo y opciones especiales → arma escena (bg +
MC izquierda + sprite NPC derecha) → muestra `intro` → menú dinámico → aplica stat →
construye texto de 4 partes (momento+lugar / mensaje opción / mensaje estado / resolución) →
muestra expresión facial según `_TALK_EXPRESION_FACIAL` y skin (`_TALK_SKIN_CUERPO`) →
guarda memoria → asigna estado posterior → `avanzar_horario()` → vuelve al HUD.

Estado del NPC para talk vive en el objeto: `talk_estado_id`, `talk_estados_especiales`,
`talk_reconsiderar_usado`, `estado_posterior_id`.

---

## 7. Sistema de Acciones de Locación — `actionsystem_core.rpy` + `actions_catalog.rpy`

Define qué puede **hacer** el jugador en cada locación (cocinar, ver TV, y acciones de
quest/evento como limpiar/buscar). El HUD lista las acciones visibles de la locación actual.

### `AccionLocacion`
`AccionLocacion(id, nombre, icono, locacion_id, label_generico, reseteo, condicion,
mensaje_reintento, color, color_hover)`.
- `reseteo`: `"diario"` (reset al dormir) | `"semanal_lunes"` | `None` (sin límite).
- `condicion` (callable → bool): visibilidad extra (ej: solo durante cierta quest). `_condicion`
  se excluye del pickle.
- `mensaje_reintento`: si `None` el botón se vuelve insensible al usarse; si es str, sigue
  clickeable y muestra ese pensamiento cuando ya se usó.

### `ListenerAccion` (interceptores de quests/eventos)
`ListenerAccion(accion_id, label, nombre_menu, prioridad, condicion, unico)`. Una quest/evento
registra un listener para "secuestrar" una acción y ejecutar **su** label en vez del genérico.
`prioridad`: `"quest"` > `"evento"` > `"generico"`.

### Flujo `accion_locacion_ejecutar` (`npcsystem_interactions.rpy`)
1. Restricción activa bloquea → pensamiento.
2. Si ya usada hoy y tiene `mensaje_reintento` → pensamiento.
3. Listeners válidos (`preparar_ejecucion`, ordenados por prioridad).
4. Sin listeners → `label_generico`. 5. Un listener → ejecuta su label. 6. Varios → menú de
   elección. `post_ejecutar` marca usada y remueve el listener si `unico`.

Dos patrones de "acción de quest":
- **Vía `condicion`** (lo más usado actualmente): la `AccionLocacion` aparece solo cuando una
  variable de quest es True (ej: `vq2_limpiar_accion_activa`) y su `label_generico` hace todo.
- **Vía `ListenerAccion`**: para interceptar acciones genéricas existentes (cocinar, etc.).

---

## 8. Sistema de Puertas / Door Access — `door_access_system.rpy` + `door_relation_system.rpy`

Controla entrar a habitaciones de NPC (`casa_hmonica/hviolet/hjasmine`).

### Niveles de acceso (`verificar_nivel_acceso_habitacion(npc)`)
Devuelve el más alto que se cumpla según horario y stats:
| Nivel | Condición | Resultado |
|---|---|---|
| `ingreso_noche` | horario 3 (trasnoche) + stat2 ≥ umbral + NPC presente | entra directo |
| `ingreso_diurno` | horario 0-2 + stat1 ≥ umbral | entra directo (**NPC no necesita estar**) |
| `dejar_pasar` | stat1 ≥ umbral + NPC presente | "Adelante" → entra |
| `sale_pasillo` | stat1 ≥ umbral + NPC presente | "Ahí salgo" → NPC va al pasillo |
| `None` | ninguno | "Estoy ocupada" |

### Umbrales actuales — `TABLA_ACCESO_HABITACION`
| NPC | ingreso_noche (deseo) | ingreso_diurno (amor) | dejar_pasar (amor) | sale_pasillo (amor) |
|---|---|---|---|---|
| Violet | 50 | 50 | 30 | 10 |
| Jasmine | 50 | 40 | 15 | 0 |
| Monica | 50 | 40 | 15 | 0 |

`stat1 = amor`, `stat2 = deseo`. Mensajes en `MENSAJES_NPC_PUERTA`. El **baño**
(`verificar_nivel_acceso_banio`) siempre devuelve `None` (contenido en desarrollo).

### Flujo `interaccion_puerta_npc`
Se entra con `_destino_puerta` seteado. Hooks especiales de quest (ej 09_a). Trasnoche:
solo entra si `ingreso_noche` y NPC presente. `ingreso_diurno`: entra siempre. Niveles
inferiores requieren NPC presente; si no, mensaje de ausencia. Si presente → menú
`menu_puerta_npc` con: "Golpear la puerta" + **opciones especiales** + "Volver".

### Opciones especiales de puerta — `obtener_opciones_puerta(npc)`
Devuelve dicts `{"texto", "label", "ocultar_golpear"?, "tipo"?}`. Cada quest/evento que quiera
una opción en la puerta añade su entrada condicionada (típicamente
`quest.activa and not completada and etapa == ETAPA_BOTON_LISTO` + horario/ítem). El screen
añade el tag `" (Evento)"` si `tipo=="evento"`, si no `" (Quest)"`. Al elegir, hace
`jump expression label`.

---

## 9. Desbloqueos por Relación — `relationship_unlocks.rpy`

Cada `definition_<npc>.rpy` registra desbloqueos con
`npc.agregar_desbloqueo(stat, umbral, icono, nombre, desc, condicion_extra=None, nombre_pendiente=None)`.
El screen de Relaciones llama `obtener_desbloqueos_stat(npc, stat)` → `(desbloqueados, bloqueados)`
ordenados por umbral. `condicion_extra` (callable) debe ser True además del umbral; mientras
falla, se muestra `nombre_pendiente`. **Es solo cosmético/informativo** (lista de hitos): el
acceso real lo decide `TABLA_ACCESO_HABITACION`, no esta lista.

Desbloqueos actuales: Violet (amor 15 Buen Humor, amor 15 Muy Buen Humor, amor 30 Ingreso
Habitación, deseo 30 Caliente, deseo 60 Ingreso Nocturno); Jasmine/Monica (amor 30 Ingreso
Habitación, deseo 60 Ingreso Nocturno).

---

## 10. Sistema de Restricciones — `restriccion_quest_system.rpy`

Variable global `restriccion_quest_activa` (una a la vez). Controla qué puede hacer el jugador
durante una quest/evento. Cuando está activa, **la interacción con NPCs queda bloqueada por
defecto** (whitelist con `npcs_interactuables`).

`RestriccionQuest(locaciones_permitidas, acciones_bloqueadas, mensaje_movimiento,
mensajes_acciones, npcs_ocultos, npcs_interactuables, mensaje_npc_bloqueado, celular_bloqueado,
mensaje_celular, elementos_escena, mensajes_bloqueados)`.

- `labels_por_locacion` (`registrar_label_locacion`): label que se ejecuta automáticamente al
  **entrar** a esa locación (vía `call expression`, debe terminar en `return`).
- `elementos_escena`: imagebuttons temporales por locación.

Helpers de lectura: `hay_restriccion_activa()`, `accion_bloqueada(id)`,
`accion_bloqueada_movimiento(dest)`, `npc_esta_oculto(id)`, `npc_interactuable(id)`,
`celular_esta_bloqueado()`, `obtener_elementos_escena(loc)`, `mensajes_estan_bloqueados()`.
Modificación dinámica: `agregar/remover_locacion_permitida`, `ocultar/mostrar_npc`,
`hacer_npc_interactuable`, `remover_elemento`, etc.

---

## 11. Sistema de Mensajes / Chat — `messagesystem_core.rpy`

`sistema_mensajes` gestiona un `ChatNPC` por contacto. Estructura de una conversación:

`GrupoMensajes(id, npc_id, mensaje_inicial, pasos, trigger_id, foto_inicial, tabla_recompensas,
horario_respuesta, momento_locacion, momento_horario, condicion_entrega, accion_al_completar,
prioritario)`.
- `pasos`: lista de `PasoConversacion(opciones_jugador, mensaje_npc)`.
- `OpcionRespuesta(texto, respuesta_npc, puntos, foto_respuesta, condicion, saltar_a_paso)`.
  `respuesta_npc` puede ser str, lista (ráfaga) o callable. `saltar_a_paso`: None=siguiente,
  índice, o -1=fin.
- `tabla_recompensas` (`TablaRecompensas` con `RangoRecompensa` por categoría): al finalizar,
  evalúa puntos acumulados y aplica recompensas (`amor`, `deseo`, `stat`, `item`, `dinero`, `foto`).

### Disparo y entrega
`disparar_por_trigger(tipo, trigger_id, npc_id)` busca el grupo registrado con ese `trigger_id`.
Si el grupo tiene condiciones de entrega (`momento_locacion`, `momento_horario`,
`condicion_entrega`) entra en **espera** y se entrega cuando se cumplan (chequeado en
avanzar_horario, cambio de locación y dormir). Sin condiciones, entrega inmediata. Un NPC real
**no** entrega el mensaje si el jugador está en la misma locación (lo dice en persona).

`grupo_completado(grupo_id)` (alias `mensaje_completado`) → para `Requisito("mensaje", grupo_id=...)`.
`horario_respuesta` limita en qué horarios se puede responder. `prioritario=True` bloquea
avanzar tiempo/dormir hasta responder (puede provocar "despertar anticipado").
`bloquear_chat_npc` / `desbloquear_chat_npc` cortan respuestas de un NPC.

Triggers que disparan grupos automáticamente: completar quest (`"quest"`), entrar a etapa
(`config_etapas.trigger_mensaje`), fallo de quest (`config_fallo.trigger_mensaje`), completar
evento (`"event"`). Contactos especiales no-NPC: `CONTACTOS_ESPECIALES`
(`libre_mercado`, `tienda_coxplay`).

---

## 12. Compras e Items — `items_shopping.rpy` + `shopping_system.rpy`

`CATALOGO_ITEMS[id]` define cada ítem:
```python
"golosinas": {
    "nombre", "emoji", "precio", "dias_entrega",   # dias_entrega cuenta días hábiles
    "descripcion", "usable", "vendible", "consumible",
    "condicion_uso": lambda: ...,     # cuándo puede usarse (False = nunca por sí solo)
    "instruccion_uso": "...",          # pista si no se cumple condicion_uso
    "label_uso": "usar_xxx",           # label al usarlo (opcional)
    "stock", "reposicion",             # stock de tienda; reposicion = stock que vuelve cada Lunes
}
```
`inventario` (dict `{item_id: cantidad}`) guarda lo que tiene el MC. Ítems de quest tienen
`precio 0`, `vendible False`, `stock 0`. La entrega física la maneja `sistema_compras`
(repartidor por la mañana / paquete en habitación). Helpers: `obtener_item_info`,
`obtener_precio_item`, `obtener_dias_entrega_item`.

---

## 13. Pensamientos (eventos de cama) — `pensamiento_system.rpy`

Al dormir, si hay pensamientos disponibles, la cama muestra menú "Dormir" / "Pensar".
`registrar_pensamiento(id, npc_id, nombre, label, condicion)`;
`obtener_pensamientos_disponibles()` filtra por `condicion`. El label del pensamiento es
repetible y **debe terminar en `return`** (el sistema retoma el flujo de dormir).

---

## 14. Interacción con NPC — `interactions_<npc>.rpy` + `menu_interaction.rpy`

`label interaccion_<npc>` (lanzado por el HUD al clickear el sprite):
1. Hooks de evento (activar evento si corresponde a la locación/horario).
2. Quest lista: si `obtener_quest_activa(npc).etapa == ETAPA_BOTON_LISTO` y **no** tiene
   `validacion_especial` de lugar/hora particular, `intentar_ejecutar()` → si éxito,
   `jump ejecutar_quest_activa`. Las quests con requisito de lugar/hora se exponen como
   **opciones extra** (no auto-ejecutan, para no crashear fuera de contexto).
3. Arma `_opciones_extra` (lista de `{"texto","label","condicion"}`) según quests/eventos
   disponibles en este contexto.
4. `call screen menu_interaccion_npc_completo(npc, opciones_extra=...)` → muestra "Hablar"
   (talk diario) + opciones extra + Cerrar. Las opciones extra retornan
   `("opcion_especial", label)` → `jump expression label`.

Cada opción extra es un dict `{"texto", "label", "condicion", "tipo"?}`. El screen agrega el
sufijo `" (Evento)"` si `tipo=="evento"`, si no `" (Quest)"` (igual que el menú de puertas). Por
eso las opciones que disparan quests llevan `(Quest)` y las de eventos repetibles llevan
`(Evento)`.

---

## Apéndice — Variables globales frecuentes

| Variable | Significado |
|---|---|
| `horario_actual`, `dia_semana_actual`, `dia_actual`, `dias_totales` | tiempo |
| `<npc>_amor`, `<npc>_deseo`, `<npc>_progreso` | stats guardables sincronizados |
| `inventario` | `{item_id: cantidad}` del MC |
| `dinero` | dinero del MC |
| `skins_activos` | `{npc: {grupo: skin_id}}` |
| `mc_inteligencia`, `mc_carisma`, `mc_personalidad` | stats del MC |
| `restriccion_quest_activa` | restricción de quest/evento activa o None |
| `talk_memoria` | memoria de talk del MC |
| `modo_posicionamiento` | True cuando la herramienta de posicionamiento está activa |
| `quest_actual` | contador global de quests completadas |
