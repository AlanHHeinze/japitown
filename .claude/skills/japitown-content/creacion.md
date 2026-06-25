# Japitown — Skill de Creación

> Recetas para **agregar contenido nuevo** siguiendo la misma lógica que lo ya creado, sin
> introducir bugs. Para entender cómo funciona cada sistema por dentro, ver `funcionamiento.md`.

---

## 0. Reglas globales (leer siempre)

1. **Idioma español** en todo: código, comentarios, variables, diálogos, pistas.
2. **Stats:** todos los NPCs usan `amor` (stat1) y `deseo` (stat2). Usar
   `cambiar_stat1/stat2(npc, n)` o `npc.modificar_stat1/stat2(n)`. No existen complicidad,
   sumisión, adulación, provocación, madurez ni debilidad.
3. **Anti-PicklingError en quests:** nunca poner lambdas crudas en `Quest`, `ConfigEtapa`,
   `ConfigFallo`. Usar función `def` (referencia directa) o `_qc("clave_unica", lambda: ...)`.
4. **Devolver control al game loop:**
   - Label que termina flujo propio: `window hide` + `$ mostrar_hud()` + `jump game_loop`.
   - Label llamado por el sistema (`call expression`): terminar en `return`.
5. **Inicio de label narrativo:** `$ ocultar_hud()` + `window show`.
6. **Modo posicionamiento:** TODO botón/imagebutton interactivo debe tener
   `if modo_posicionamiento: action NullAction()` / `else: action ...`.
7. **IDs únicos** en todo el proyecto. Convención: `{npc}_{tipo}_{numero}` /
   `{locacion}_{elemento}_{variante}`.

---

## 1. Crear una Quest

**Archivos:** definición en `characters/<npc>/quests/quest_<npc>.rpy` (agregar al existente),
labels en `characters/<npc>/quests/<npc>_quest_XX.rpy` (nuevo), screens opcionales en
`characters/<npc>/screens/<npc>_questXX_screens.rpy`.

### Definición (en `quest_<npc>.rpy`)
```renpy
init python:   # funciones nombradas ANTES del init 5 (picklables → referencia directa)
    def _pista_<npc>_qX():
        return "Mensaje de pista"
    def _quehacer_<npc>_qX():
        return "Qué debe hacer el jugador"

init 5 python:
    quest_<npc>_X = Quest(
        id="<npc>_questprincipal_X",
        npc_id="<npc>",
        nombre="Nombre",
        descripcion="Descripción desde el MC",
        numero_quest=X,
        dias_espera=4,
        quest_anterior="<npc>_questprincipal_Y",   # se inicia sola al completar la previa

        # Etapa 3 — condiciones para avanzar
        requisitos=[
            Requisito("mensaje", "Esperar el chat", grupo_id="<grupo_chat>"),
            # tipos: amor, deseo, stat, item, dinero, memoria, locacion, horario, dia, mensaje, npc_presente
        ],
        # Etapa 6 — validación al pulsar el botón/opción
        validacion_especial=[
            Requisito("dia", "Debe ser sábado", dia_id=5),
            Requisito("horario", "Por la noche", horario_id=2),
            Requisito("npc_presente", "Violet en su cuarto", npc_id="<npc>", locacion_id="casa_h<npc>"),
        ],
        # Etapa 4 — rutina del NPC durante la quest
        rutina_quest={ (5,0): RutinaQuest(locacion="casa_h<npc>",
                        sprite="images/characters/casa/idle/idle_<npc>_..._skinbase.png",
                        posicion=(800,700)) },
        rutinas_adicionales={ "monica": {(5,0): RutinaQuest(locacion="fuera")} },
        prioridad_rutina=0,
        retorno=ConfiguracionRetorno(avanzar_dia=False),

        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(pista=_pista_<npc>_qX, que_hacer=_quehacer_<npc>_qX),
            ETAPA_CONDICIONES: ConfigEtapa(
                pista="Pista estática",
                que_hacer="Acción",
                trigger_mensaje=("<grupo_chat>", "<npc>"),   # dispara chat al entrar a la etapa
            ),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_qc("<npc>_qX_bl_pista", lambda: "Pista dinámica {}".format(store.var)),
                que_hacer="Habla con <Npc>",
                mensaje_despertar="Mensaje al despertar ese día",
            ),
        },
        config_fallo=ConfigFallo(
            condicion=_qc("<npc>_qX_fallo", lambda: store.dia_semana_actual==5 and store.horario_actual==1),
            trigger_mensaje=("<grupo_fallo>", "<npc>"),
            cambio_relacion=("<npc>", -1),
            pista="Pista tras fallar",
        ),
    )
    sistema_quests.registrar_quest(quest_<npc>_X)
```

### Label narrativo (en `<npc>_quest_XX.rpy`)
```renpy
image questX_fondo = "images/quest/<npc>/questX/fondo.png"
default questX_var = False

label quest_<npc>_questprincipal_X:
    $ ocultar_hud()
    window show
    scene questX_fondo with fade
    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Diálogo"
    # ... gameplay con restricción si hace falta ...
    # AL FINAL:
    $ desactivar_restriccion()          # solo si activaste una
    $ completar_quest_actual("<npc>")
    window hide
    $ mostrar_hud()
    jump game_loop
```

> **Exposición de la quest al jugador (cómo se inicia):** en `ETAPA_BOTON_LISTO`, según el diseño:
> - **Por interacción directa con el NPC** → se maneja en `interaccion_<npc>` (sección 4) o
>   auto-ejecuta si no tiene validación de lugar/hora.
> - **Por opción en la puerta** (NPC en su cuarto) → agregar a `obtener_opciones_puerta` (sección 5).
> - **Al despertar / al dormir** → hook en `accion_dormir` (`timesystem_core.rpy`).

Para screens interactivos dentro de la quest (objetos clickeables, exploración de habitación,
ropero con `ui.interact`), ver `creacion_screens.md` patrones A–D.

---

## 2. Crear un Evento

**Archivos:** definición en `characters/<npc>/events/events_<npc>.rpy`, labels en
`characters/<npc>/events/event_<npc>_XX.rpy`.

```renpy
init python:
    def condicion_aparicion_eventoXX_<npc>():
        q = store.sistema_quests.obtener_quest("<npc>_questprincipal_Y")
        return bool(q and q.completada)

    def on_aparicion_eventoXX_<npc>():
        # se ejecuta UNA vez al volverse visible — útil para anclar el día
        store.<npc>_evXX_pendiente_desde_dia = getattr(store, 'dias_totales', 0)

    def condicion_activacion_eventoXX_<npc>():
        return store.dia_semana_actual == 5 and store.horario_actual == 0

init 5 python:
    event_<npc>_XX = Event(
        id="<npc>_evento_XX",
        nombre="Nombre del evento",
        tipo=TIPO_EVENT_ESPORADICO,             # o TIPO_EVENT_PERSISTENTE
        prioridad=10,
        condicion_aparicion=condicion_aparicion_eventoXX_<npc>,
        condicion_activacion=condicion_activacion_eventoXX_<npc>,   # None = autoactiva al aparecer
        on_aparicion=on_aparicion_eventoXX_<npc>,
        label_efecto="evento_<npc>_XX",          # opcional
        npc_id="<npc>",
        descripcion="Descripción",
        config_etapas={
            ESTADO_EVENT_VISIBLE: ConfigEtapa(pista="...", que_hacer="..."),
            ESTADO_EVENT_ACTIVO:  ConfigEtapa(pista="...", que_hacer="...",
                                              mensaje_despertar="Hoy es sábado..."),
        },
        modificaciones={ "rutinas": {"<npc>": {(5,0): "casa_h<npc>"}} },  # opcional
    )
    sistema_events.registrar_event(event_<npc>_XX)
```

Label del evento → al terminar: `$ event.completar()` o `$ obtener_event("<id>").completar()`,
luego `window hide` + `$ mostrar_hud()` + `jump game_loop`.

> El `mensaje_despertar` va **solo** en `config_etapas[ESTADO_EVENT_ACTIVO]`, NUNCA como parámetro
> suelto del constructor (si no, se dispara cada mañana sin importar el estado).

---

## 3. Crear una Rutina

En `definition_<npc>.rpy` dentro de `inicializar_<npc>()`:

```renpy
# Ubicación base por (dia, horario)
<npc>.establecer_rutina(dia_semana, horario, "locacion_id")   # dia 0-6, horario 0-3

# Sprite + posición visual de esa rutina (acepta lista de días)
establecer_rutina_visual_<npc>([0,1,2,3,4], 0,
    "images/characters/casa/idle/idle_<npc>_casa_cocina_mañana_rutinabase_grupobase_skinbase.png",
    (765, 1060))   # (x,y) ancla centro-inferior

# Rutina especial opcional (probabilística: salir, ducharse)
<npc>.agregar_rutina_especial(RutinaEspecial(
    id="<npc>_salida", locacion="fuera", sprite=None, posicion=None,
    probabilidad=0.20, horarios=[1,2], nombre="<Npc> salió de la casa"))
```

La posición exacta del sprite se ajusta con la herramienta de posicionamiento (tecla P en debug);
copiar el `(x, y)` que reporta.

---

## 4. Crear una Interacción / opción en el menú del NPC

En `characters/<npc>/interaction/interactions_<npc>.rpy`, dentro de `label interaccion_<npc>`,
agregar a `_opciones_extra_<npc>`:

```renpy
$ _quest_x = sistema_quests.obtener_quest("<npc>_questprincipal_X")
if (_quest_x and _quest_x.activa and not _quest_x.completada and
        _quest_x.etapa_actual == ETAPA_BOTON_LISTO and
        sistema_locaciones.locacion_actual and
        sistema_locaciones.locacion_actual.id == "casa_gym" and horario_actual == 1):
    $ _opciones_extra_<npc>.append({
        "texto": "Saludar",
        "label": "quest_<npc>_questprincipal_X",
        "condicion": True,
    })
```

El screen ya muestra "Hablar" (talk diario) + estas opciones. Al elegir una, retorna
`("opcion_especial", label)` y el label final hace `jump expression`.

El dict acepta `"tipo"`: por defecto la opción muestra el tag `" (Quest)"`; si la opción dispara
un **evento** (no una quest), agregar `"tipo": "evento"` para que muestre `" (Evento)"`.

> **Importante:** las quests con `validacion_especial` de lugar/hora deben exponerse como opción
> extra (no auto-ejecutarse), para no crashear cuando el jugador interactúa en el contexto
> equivocado. Excluirlas del bloque de auto-ejecución (`if _quest_activa.id not in (...)`).

---

## 5. Agregar una opción al Door Access (puerta de habitación)

En `door_access_system.rpy`, dentro de `obtener_opciones_puerta(npc_id)`, en el bloque del NPC:

```renpy
quest_vXY = store.sistema_quests.obtener_quest("violet_questprincipal_XY")
if (quest_vXY and quest_vXY.activa and not quest_vXY.completada and
        quest_vXY.etapa_actual == ETAPA_BOTON_LISTO and store.horario_actual == 2):
    opciones.append({"texto": "Tengo las entradas", "label": "violet_questXY_puerta",
                     "ocultar_golpear": True})
```
- `"ocultar_golpear": True` esconde el botón "Golpear la puerta" mientras la opción está activa.
- Para un **evento** en vez de quest, añadir `"tipo": "evento"` (cambia el tag a `(Evento)`).

El label destino abre con el NPC ya en escena; al terminar, devolver al game loop normalmente.

---

## 6. Crear un Skin

En `characters/<npc>/visual/skins_<npc>.rpy` dentro de `inicializar_skins_<npc>()`:

```renpy
skin_pijama = Skin(
    id="<npc>_pijama_base",          # convención {npc}_{grupo}_{variante}
    npc_id="<npc>",
    nombre="Pijama",
    grupo="pijama",                  # base, entrenamiento, bikini, pijama, ropa_interior, vestidos
    descripcion="...",
    condicion_desbloqueo=None,       # None = siempre; o callable → bool
    sprite_menu="images/characters/casa/menu/<npc>_menu_pijama_base.png",
    sprite_idle="...png",            # opcional, usado en rutinas de ese grupo
)
sistema_skins.registrar_skin(skin_pijama)

# Asignar el grupo a las rutinas que deben mostrarlo (con condición opcional)
def _cond_pijama_<npc>():
    return store.skins_activos.get("<npc>", {}).get("pijama") is not None
establecer_grupo_rutina("<npc>", [0,1,2,3,4,5], 2, "pijama", condicion=_cond_pijama_<npc>)
```

Desde una quest, para otorgar/activar el skin:
```renpy
$ desbloquear_skin("<npc>_pijama_base")     # lo marca activo en su grupo
```
Si un grupo nuevo tiene cuerpo propio en la layered image, actualizar `GRUPO_CUERPO_MAP` en
`skinsystem_core.rpy`. Para mostrar el cuerpo correcto al inicio de una escena usar
`cuerpo_activo("<npc>")` → `"c_rbase"` o `"c_pijama"`.

---

## 7. Crear un estado de Talk

En `characters/<npc>/talk/<npc>_talk.rpy` dentro de `inicializar_talk_<npc>()`.

### Estado general (entra al pool aleatorio del día)
```renpy
EstadoTalk(
    id="<npc>_molesta",
    nombre="Molesta",
    intro="<Npc> parece estar molesta.",
    efectos={ "complacerla":"-2_amor", "provocarla":"nada", "escucharla":"+1_deseo",
              "hablarle":"+2_amor", "adularla":"nada" },
    mensaje="ella estaba molesta.",
    estados_posteriores={ "+2_amor":"posterior_feliz", "+1_deseo":"posterior_hot", ... },
)
```
`resultado_id` válidos: `+1_amor`, `+2_amor`, `+4_amor`, `+1_deseo`, `+2_deseo`, `-2_amor`,
`-1_deseo`, `nada`. Luego agregar el `id` a `estados_generales_ids`.

### Estado condicional (solo en pool si se cumple)
Igual que general + `condicion=lambda: store.<npc>_amor >= 15`. También va en
`estados_generales_ids` (el filtro lo excluye cuando la condición no se cumple).

### Estado especial (lo activan quests/eventos/items)
Agregar `es_especial=True, jerarquia=5, dias_duracion=2`. Activarlo con:
```renpy
$ activar_estado_especial_npc("<npc>", "<npc>_feliz", dias_duracion=2)
```

### Opción especial de talk
```renpy
OpcionEspecialTalk(
    id="<npc>_golosinas", texto="Darle golosinas",
    condicion=_<npc>_cond_golosinas, mensaje_opcion="Le ofreciste golosinas.",
    resultado_id="+2_amor", item_requerido="golosinas", item_consumible=True,
    estado_posterior_npc="posterior_feliz", recompensa_extra=_<npc>_recompensa_golosinas,
)
```
Agregarla a `opciones_especiales_<npc>` y, si tiene texto final propio, a `resoluciones_especiales`.

Si agregás un `resultado_id` nuevo, registrarlo en `RESULTADO_A_STAT`, `RESULTADO_TEXTO`
(`talksystem_core.rpy`) y en `resoluciones` del NPC.

---

## 8. Crear una Acción de Locación

En `actions_catalog.rpy` (init 5):
```renpy
sistema_acciones.registrar_accion(AccionLocacion(
    id="ev03_limpiar_living",
    nombre="Limpiar", icono=u"🧹",
    locacion_id="casa_living",
    label_generico="ev03_accion_limpiar_living",
    reseteo=None,                  # "diario" | "semanal_lunes" | None
    condicion=lambda: getattr(store, 'vq2_limpiar_accion_activa', False),
))
```
El `label_generico` ejecuta la acción y termina en `return`. Patrón de quest: activar la acción
poniendo su variable de condición en True; al terminar, ponerla en False.

Para **interceptar** una acción genérica existente (cocinar, ver TV) desde una quest/evento:
```renpy
$ sistema_acciones.registrar_listener(ListenerAccion(
    accion_id="cocinar", label="mi_quest_cocinar", nombre_menu="Cocinar para Violet",
    prioridad="quest", condicion=lambda: ..., unico=True))
```

---

## 9. Crear un Item

En `items_shopping.rpy`, agregar al dict `CATALOGO_ITEMS`:
```renpy
"mi_item": {
    "nombre": "Mi Item", "emoji": "🎁", "precio": 50, "dias_entrega": 2,
    "descripcion": "...", "usable": True, "vendible": True, "consumible": False,
    "condicion_uso": lambda: store.sistema_locaciones.locacion_actual.id == "casa_hmc",
    "instruccion_uso": "Debería usarlo en mi habitación",
    "label_uso": "usar_mi_item",      # opcional
    "stock": 5, "reposicion": 3,      # reposicion = stock que vuelve cada Lunes
},
```
Ítem de quest (no comprable): `precio 0`, `vendible False`, `stock 0`, `reposicion 0`.
Dar el ítem desde código: `$ inventario["mi_item"] = inventario.get("mi_item", 0) + 1`.

---

## 10. Crear mensajes de Chat

En `characters/<npc>/chat/chat_<npc>.rpy`:
```renpy
init 5 python:
    grupo = GrupoMensajes(
        id="<grupo_id>",
        npc_id="<npc>",
        mensaje_inicial="Hola, ¿estás?",
        trigger_id="<trigger>",                 # = quest_id, event_id o id manual
        horario_respuesta=[1,2],                 # opcional
        momento_locacion=None, momento_horario=None, condicion_entrega=None,  # entrega condicional
        prioritario=False,
        pasos=[
            PasoConversacion(opciones_jugador=[
                OpcionRespuesta(texto="Sí", respuesta_npc=["Genial", "Te espero"],
                                puntos={"amor": 2}),
                OpcionRespuesta(texto="No", respuesta_npc="Bueno...", puntos={"amor": -1}),
            ]),
        ],
        tabla_recompensas=TablaRecompensas({
            "amor": [RangoRecompensa(2, 99, {"tipo":"amor","valor":3})],
        }),
        accion_al_completar=None,
    )
    sistema_mensajes.registrar_grupo("<npc>", grupo)
```
Se dispara con `trigger_mensaje=("<trigger>", "<npc>")` en una `ConfigEtapa`, al completar la
quest (`trigger_id == quest_id`), o con `disparar_mensaje("<trigger>", "<npc>")`.
Para usar como requisito de quest: `Requisito("mensaje", "...", grupo_id="<grupo_id>")`.

---

## 11. Crear un Pensamiento (evento de cama)

```renpy
init 6 python:
    sistema_pensamientos.registrar_pensamiento(
        id="<npc>_pensamiento_X", npc_id="<npc>", nombre="Nombre repetible",
        label="label_del_pensamiento",
        condicion=lambda: store.eventoX_completado == True,
    )
```
El label debe ser repetible y terminar en `return` (el sistema retoma el flujo de dormir).

---

## 12. Crear un Desbloqueo de Relación (lista de hitos)

En `definition_<npc>.rpy` dentro de `inicializar_<npc>()`:
```renpy
<npc>.agregar_desbloqueo("amor", 30, "🚪", "Ingreso Habitación",
    "<Npc> te deja entrar a su cuarto durante el día.")
<npc>.agregar_desbloqueo("deseo", 60, "🌙", "Ingreso Nocturno",
    "Podés entrar de noche.", condicion_extra=None, nombre_pendiente=None)
```
Es informativo (lo muestra el panel de Relaciones). El acceso real a la habitación lo controla
`TABLA_ACCESO_HABITACION` en `door_relation_system.rpy` (ajustar ahí los umbrales).

---

## Checklists

### Nueva Quest
- [ ] `Quest(...)` + `sistema_quests.registrar_quest()` en `quest_<npc>.rpy`
- [ ] Labels en `<npc>_quest_XX.rpy`; `image` e `default` al inicio
- [ ] Requisitos solo con tipos válidos (amor/deseo/…); CERO stats antiguos
- [ ] Todos los callables con `def` o `_qc("clave_unica", ...)` — CERO lambdas crudas
- [ ] `ocultar_hud()`+`window show` al iniciar; `mostrar_hud()`+`jump game_loop` al devolver
- [ ] `desactivar_restriccion()` + `completar_quest_actual("<npc>")` al finalizar
- [ ] Forma de iniciarla expuesta (interacción / puerta / despertar)
- [ ] Botones con `modo_posicionamiento → NullAction()`

### Nuevo Evento
- [ ] `Event(...)` + `sistema_events.registrar_event()`; condiciones como funciones nombradas
- [ ] `mensaje_despertar` solo en `config_etapas[ESTADO_EVENT_ACTIVO]`
- [ ] `event.completar()` al terminar la narrativa

### Nuevo Skin / Estado Talk / Acción / Item / Mensaje
- [ ] Registrado en su sistema (`registrar_skin` / `estados_generales_ids` /
      `registrar_accion` / `CATALOGO_ITEMS` / `registrar_grupo`)
- [ ] `resultado_id` nuevos también en `RESULTADO_A_STAT` y `RESULTADO_TEXTO`
- [ ] IDs únicos en todo el proyecto
