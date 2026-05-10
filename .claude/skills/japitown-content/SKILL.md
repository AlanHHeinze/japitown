---
name: japitown-content
description: Guia completa para desarrollar contenido nuevo en Japitown (quests, eventos, escenas, NPCs, sprites, screens interactivos). Usar siempre que se trabaje con el juego Ren'Py Japitown.
---

# Desarrollo de Contenido — Japitown

## Arquitectura del Proyecto

```
game/script/
├── core/                    # Sistemas del motor del juego
│   ├── quests/              # questsystem_core.rpy, restriccion_quest_system.rpy
│   ├── events/              # eventsystem_core.rpy
│   ├── npcs/                # npcsystem_core.rpy, npcsystem_interactions.rpy
│   ├── locations/           # locationsystem_core.rpy, locations_house.rpy, door_access_system.rpy
│   ├── shopping/            # shopping_system.rpy, items_shopping.rpy
│   ├── skins/               # Sistema de skins
│   ├── time/                # timesystem_core.rpy, despertar_system.rpy
│   ├── messages/            # Sistema de mensajes
│   ├── thoughts/            # pensamiento_system.rpy
│   └── utils/               # Utilidades generales
├── characters/              # Datos por personaje
│   ├── violet/
│   │   ├── definition_violet.rpy     # NPC init, rutinas, Character define
│   │   ├── chat/                     # Conversaciones del celular
│   │   ├── interaction/              # Menu de interaccion NPC
│   │   ├── quests/                   # quest_violet.rpy (definiciones) + violet_quest_XX.rpy (labels)
│   │   ├── screens/                  # Screens especificos de quests
│   │   └── visual/                   # sprites_violet.rpy, skins_violet.rpy
│   ├── monica/               # (misma estructura)
│   │   └── events/           # events_monica.rpy (definiciones) + event_monica_XX.rpy (labels)
│   ├── jasmine/              # (misma estructura)
│   └── mc/                   # Protagonista
├── ui/                       # Interfaz de usuario
│   ├── hud/                  # HUD principal (hud_navigation.rpy), herramientas dev
│   ├── menus/                # Menus del juego
│   └── base/                 # Screens base
├── tools/                    # Herramientas de desarrollo
│   └── position/             # posicionamiento_elementos.rpy
└── story/                    # Narrativa principal (intro)
```

## Idioma

**IMPORTANTE:** Todo el codigo, comentarios, nombres de variables, textos de pistas, dialogos, y documentacion esta en **español**. Siempre usar español para todo contenido nuevo.

---

## 1. Game Loop y Flujo de Control

### Estructura del Game Loop

```renpy
# game/script/story/intro/intro_main.rpy
label game_loop:
    window hide
    $ validar_eventos()
    if not renpy.get_screen("navegacion_locaciones_con_hud"):
        show screen navegacion_locaciones_con_hud
    pause
    jump game_loop
```

El loop: valida eventos → muestra HUD → pausa esperando input → repite.

### Como se llaman los labels desde el game loop

El HUD (`navegacion_locaciones_con_hud`) es un screen **siempre activo** (nunca se destruye). En vez de hide/show, se controla con:
- `$ ocultar_hud()` — oculta contenido visual, desactiva modal (clicks pasan a say/otros screens)
- `$ mostrar_hud()` — muestra contenido visual, activa modal

El screen tiene hotspots y NPC sprites como botones. Al clickear:
- **Hotspot MOVE**: `Call("accion_hotspot_move")` → mueve al jugador
- **Hotspot ACTION**: `Call("accion_hotspot_action")` → ejecuta label del hotspot
- **NPC sprite**: `Call("interaccion_" + npc.id)` → interaccion con NPC

Cuando un hotspot MOVE se ejecuta, si hay restriccion activa con `labels_por_locacion`, se hace `call expression` del label registrado para esa locacion. **Ese label DEBE terminar en `return`** para devolver control al gameloop.

### Regla de oro: como devolver control

```renpy
# Devolver al gameloop con HUD visible:
$ sistema_locaciones.mover_a_locacion("casa_living")
window hide
$ mostrar_hud()
jump game_loop

# Devolver al gameloop desde un label llamado por el sistema de locaciones:
# (llamado via call expression desde npcsystem_interactions.rpy)
return  # OBLIGATORIO — vuelve al gameloop automaticamente
```

---

## 2. Crear una Quest Nueva

### Archivos necesarios (2-3 archivos)

1. **Definicion**: `game/script/characters/<npc>/quests/quest_<npc>.rpy` (agregar al existente)
2. **Labels narrativos**: `game/script/characters/<npc>/quests/<npc>_quest_XX.rpy` (nuevo)
3. **Screens** (si tiene interacciones): `game/script/characters/<npc>/screens/<npc>_questXX_screens.rpy`

### Plantilla: Definicion de Quest

```renpy
# En quest_<npc>.rpy, dentro del bloque init 5 python:

quest_<npc>_X = Quest(
    id="<npc>_questprincipal_X",           # ID unico global
    npc_id="<npc>",                         # violet, monica, jasmine
    nombre="Nombre de la Quest",
    descripcion="Descripcion corta desde la perspectiva del MC",
    numero_quest=X,                         # Numero secuencial (0, 1, 2...)
    dias_espera=4,                          # Dias antes de que se active
    quest_anterior="<npc>_questprincipal_Y", # ID de quest previa requerida

    # Requisitos para avanzar de ETAPA_CONDICIONES a ETAPA_BOTON_LISTO
    requisitos=[
        Requisito("mensaje", "Descripcion", grupo_id="<grupo_chat>"),
        # Tipos: "relacion", "afinidad", "stat", "item", "dinero",
        #        "memoria", "locacion", "horario", "dia", "mensaje", "npc_presente"
    ],

    # Validaciones para el boton "Listo" (ETAPA_BOTON_LISTO -> ETAPA_DESARROLLO)
    validacion_especial=[
        Requisito("dia", "Debe ser sabado", dia_id=5),
        Requisito("horario", "Por la mañana", horario_id=0),
        Requisito("npc_presente", "NPC debe estar ahi", npc_id="<npc>", locacion_id="casa_h<npc>"),
    ],

    # Rutina del NPC durante la quest (override sobre rutina base)
    rutina_quest={
        (5, 0): RutinaQuest(  # (dia_semana, horario)
            locacion="casa_h<npc>",
            sprite="images/characters/casa/idle/idle_<npc>_..._skinbase.png",
            posicion=(800, 700)
        ),
    },

    # Rutinas de OTROS NPCs durante la quest
    rutinas_adicionales={
        "monica": {(5, 0): RutinaQuest(locacion="fuera")},
        "jasmine": {(5, 0): RutinaQuest(locacion="fuera")},
    },

    prioridad_rutina=0,
    retorno=ConfiguracionRetorno(avanzar_dia=False),

    # Configuracion por etapas — pistas, mensajes y triggers del HUD
    config_etapas={
        ETAPA_ESPERA: ConfigEtapa(
            pista="Mensaje de pista durante espera",
            que_hacer="Que debe hacer el jugador",
        ),
        ETAPA_CONDICIONES: ConfigEtapa(
            pista="Pista para completar condiciones",
            que_hacer="Accion requerida",
            trigger_mensaje=("grupo_chat_id", "npc_remitente"),
        ),
        ETAPA_BOTON_LISTO: ConfigEtapa(
            pista="Pista cuando el boton esta visible",
            que_hacer="Instruccion de que hacer",
            mensaje_despertar="Mensaje al despertar ese dia",
        ),
    },

    # Configuracion de fallo (opcional)
    config_fallo=ConfigFallo(
        condicion=lambda: getattr(store, 'dia_semana_actual', 0) == 5 and getattr(store, 'horario_actual', 0) == 1,
        trigger_mensaje=("grupo_chat_fallo", "npc"),
        cambio_relacion=("npc", -1),
        pista="Pista despues del fallo",
        que_hacer=lambda: "Que hacer despues del fallo",
    ),
)
sistema_quests.registrar_quest(quest_<npc>_X)
```

### Etapas del Sistema de Quests (flujo automatico)

```
ETAPA_INICIALIZACION (1) -> ETAPA_ESPERA (2) -> ETAPA_CONDICIONES (3)
-> ETAPA_RUTINA (4) -> ETAPA_BOTON_LISTO (5) -> ETAPA_VALIDACION (6)
-> ETAPA_DESARROLLO (7) -> ETAPA_MEMORIAS (8) -> ETAPA_FINALIZACION (9)
```

### Plantilla: Label Narrativo de Quest

```renpy
# En <npc>_quest_XX.rpy

# =============================================================================
# IMAGENES
# =============================================================================
image questX_fondo = "images/quest/<npc>/questX/nombre_imagen.png"

# =============================================================================
# VARIABLES
# =============================================================================
default questX_variable = False

################################################################################
## LABEL PRINCIPAL
################################################################################

label quest_<npc>_questprincipal_X:

    # === SIEMPRE EMPEZAR ASI ===
    $ ocultar_hud()
    window show

    # === ESCENA NARRATIVA ===
    scene questX_fondo with fade

    # Sprites con layered image
    show <npc>_parada c_<ropa>_base o_basemirando b_aburrida ca_<ropa> at right
    show mc_parado_base c_rbase_base o_basemirando b_serio at mc_izquierda

    # Dialogos
    show <npc>_parada b_hablandochica
    <npc_character> "Texto de dialogo"
    show <npc>_parada b_none

    show mc_parado_base b_hablando
    mc "Texto de dialogo del MC"
    show mc_parado_base b_none

    piensa "Texto pensamiento"

    # === ACTIVAR RESTRICCION (cuando hay gameplay interactivo) ===
    $ activar_restriccion(
        locaciones_permitidas=["casa_living", "casa_hmc"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento="Debo hacer X primero",
        mensajes_acciones={
            "avanzar_tiempo": "No puedo perder tiempo",
            "dormir": "No puedo perder tiempo",
            "entrenar": "No puedo perder tiempo",
            "trabajar": "No puedo perder tiempo",
            "usar_item": "No puedo perder tiempo",
            "comprar": "No puedo perder tiempo",
        },
        mensaje_npc_bloqueado="No tengo tiempo para eso ahora",
        celular_bloqueado=True,
        mensaje_celular="No puedo perder tiempo",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    # Registrar labels que se ejecutan al llegar a una locacion
    $ restriccion_quest_activa.registrar_label_locacion("casa_living", "label_al_entrar_living")

    # Mover jugador y devolver control al gameloop
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    window hide
    $ mostrar_hud()
    jump game_loop

    # === AL FINAL DE LA QUEST ===
    $ desactivar_restriccion()
    $ completar_quest_actual("<npc>")
    window hide
    $ mostrar_hud()
    jump game_loop
```

---

## 3. Screens Interactivos en Quests

### Patron A: Screen overlay sobre el HUD (elementos sobre la locacion)

El screen se muestra SOBRE el HUD sin ocultarlo. El jugador puede seguir navegando.
Usado para: sillones, objetos en el piso, elementos clickeables sobre el fondo de la locacion.

```renpy
# Screen overlay — no oculta HUD, se auto-oculta si el jugador sale de la locacion
screen mi_screen_quest():
    # Auto-ocultar si el jugador salio de la locacion
    if sistema_locaciones.locacion_actual and sistema_locaciones.locacion_actual.id != "casa_living":
        timer 0.01 action Hide("mi_screen_quest")
    else:
        imagebutton:
            idle Transform("imagen.png", alpha=0.0)
            hover "imagen.png"
            xpos 500
            ypos 400
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action [Hide("mi_screen_quest"), Jump("mi_label")]
```

Uso desde un label (llamado por el sistema de locaciones via `registrar_label_locacion`):
```renpy
label mi_label_al_entrar:
    show screen mi_screen_quest
    return  # OBLIGATORIO — devuelve control al gameloop
```

### Patron B: Screen de exploracion (reemplaza la interaccion normal)

El screen tiene multiples elementos clickeables. El HUD sigue visible pero el screen captura clicks.
Usado para: habitaciones con objetos explorables (habitacion de Violet en quest 4).

**Regla clave: Call vs Jump desde screens**
- **Interacciones simples** (dialogo y volver): usar `action Call("label")` — el screen NO se oculta, el label hace `return` y el screen se re-evalua
- **Interacciones que cambian escena** (ropero, cajonera): usar `action [Hide("screen"), Jump("label")]` — el screen se oculta, el label maneja todo y al terminar hace `jump label_mostrar_screen` para volver
- **Salir del screen**: usar `action [Hide("screen"), Jump("label_verificar")]` — verifica condiciones antes de permitir salir

```renpy
screen vq4_habitacion_violet():
    # Fondo que absorbe clicks
    button:
        xpos 0 ypos 0 xsize 1920 ysize 1080
        background None
        action NullAction()

    # Elemento simple (dialogo): usa Call — screen queda visible
    if vq4_compu_pendiente:
        imagebutton:
            idle Transform("compu.png", alpha=0.0)
            hover "compu.png"
            xpos 500 ypos 400
            xanchor 0.5 yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Call("violet_quest4_click_compu")

    # Elemento que cambia escena (ropero): usa Hide + Jump
    if not violet_quest4_tiene_pijama:
        imagebutton:
            idle Transform("ropero.png", alpha=0.0)
            hover "ropero.png"
            xpos 234 ypos 908
            xanchor 0.5 yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action [Hide("vq4_habitacion_violet"), Jump("violet_quest4_click_ropero")]

    # Boton Salir (con verificacion)
    button:
        xalign 0.5 ypos 20
        background "#0288D1EE"
        hover_background "#4FC3F7"
        padding (30, 10)
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action [Hide("vq4_habitacion_violet"), Jump("violet_quest4_check_salida")]
        text "Salir" size 22 color "#ffffff" bold True
```

Labels para interacciones simples (llamados con Call):
```renpy
label violet_quest4_click_compu:
    $ vq4_compu_pendiente = False
    window show
    piensa "La computadora de Violet... mejor no tocar nada."
    window hide
    return  # Vuelve al screen que sigue visible
```

Label que muestra el screen y devuelve control:
```renpy
label violet_quest4_mostrar_habitacion:
    show screen vq4_habitacion_violet
    return  # Devuelve control al gameloop
```

### Patron C: Screen con loop de interaccion (ui.interact)

Para screens que tienen su propia escena (ropero, cajonera). Se oculta el HUD, se cambia el background, y el screen usa `Return()` con un loop `while/ui.interact()`.

```renpy
screen vq4_screen_ropero():
    # Fondo clickeable
    button:
        xpos 0 ypos 0 xsize 1920 ysize 1080
        background None
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("fuera")

    # Elementos con Return
    imagebutton:
        idle Transform("pijama.png", alpha=0.0)
        hover "pijama.png"
        xpos 821 ypos 824
        xanchor 0.5 yanchor 1.0
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("pijama")

    # Boton Volver
    button:
        xalign 0.5 ypos 20
        background "#0288D1EE"
        hover_background "#4FC3F7"
        padding (30, 10)
        action Return("volver")
        text "Volver" size 22 color "#ffffff" bold True
```

Label con loop ui.interact():
```renpy
label violet_quest4_click_ropero:
    hide screen vq4_habitacion_violet
    $ ocultar_hud()
    scene vq4_ropero with fade
    show screen vq4_screen_ropero
    $ _en_ropero = True
    while _en_ropero:
        $ _resultado = ui.interact()
        if _resultado == "pijama":
            hide screen vq4_screen_ropero
            window show
            mc "Esto es lo que necesitaba."
            $ violet_quest4_tiene_pijama = True
            window hide
            $ _en_ropero = False  # Salir automaticamente al tomar item
        elif _resultado == "caja":
            hide screen vq4_screen_ropero
            window show
            mc "Le tendria que preguntar a Violet por el cosplay."
            window hide
            show screen vq4_screen_ropero  # Volver al screen
        elif _resultado == "volver":
            $ _en_ropero = False
        elif _resultado == "fuera":
            hide screen vq4_screen_ropero
            window show
            mc "Violet me pidio su pijama rosa."
            window hide
            show screen vq4_screen_ropero
    hide screen vq4_screen_ropero
    # Volver a la habitacion
    scene vq4_hviolet_tormenta with fade
    $ mostrar_hud()
    jump violet_quest4_mostrar_habitacion
```

**Patron dentro del loop ui.interact():**
1. `hide screen` antes de dialogos (para que no interfiera con clicks del say)
2. `window show` → dialogo → `window hide`
3. `show screen` para volver al loop, O `_en_loop = False` para salir
4. Al salir del loop: `hide screen`, restaurar escena, `$ mostrar_hud()`, jump al screen anterior

### Patron D: Verificacion de salida

```renpy
label violet_quest4_check_salida:
    if not violet_quest4_tiene_pijama:
        window show
        piensa "Debo buscar la ropa de Violet."
        window hide
        jump violet_quest4_mostrar_habitacion  # Volver al screen

    # Tiene el pijama — avanzar la quest
    jump violet_quest4_salir
```

### Ocultar elementos segun estado

Los elementos del screen se muestran/ocultan con variables `default`:

```renpy
# Variables de estado
default vq4_compu_pendiente = True
default violet_quest4_tiene_pijama = False
default violet_quest4_ropainterior = False

# En el screen:
if vq4_compu_pendiente:           # Se oculta despues de interactuar
    imagebutton: ...

if not violet_quest4_tiene_pijama: # Se oculta cuando ya tiene el item
    imagebutton: ...

if not violet_quest4_ropainterior: # Se oculta cuando ya tomo ropa
    imagebutton: ...
```

### Posiciones editables con sistema_pos

Los elementos usan `sistema_pos` para ser editables con la herramienta de posicionamiento (tecla P en modo debug):

```renpy
# Defaults como fallback
default vq4_pos_compu = (1636, 775)

# En el screen:
$ _elem = sistema_pos.obtener("hviolet_compu_vq4")
$ _x = _elem.x if _elem else vq4_pos_compu[0]
$ _y = _elem.y if _elem else vq4_pos_compu[1]

imagebutton:
    xpos _x
    ypos _y
    xanchor 0.5
    yanchor 1.0
```

Registro en `game/script/tools/position/posicionamiento_elementos.rpy`:
```renpy
sistema_pos.registrar(
    id="hviolet_compu_vq4",
    imagen="images/quest/violet/quest4/violet_quest04_interaccion_compu.png",
    nombre="Compu - Habitacion VQ4",
    grupo="quest_elemento",
    screen="vq4_habitacion_violet",
    x=1636, y=775,
    xanchor=0.5, yanchor=1.0
)
```

### Bloqueo en modo posicionamiento

**TODOS los botones interactivos** deben verificar `modo_posicionamiento`:

```renpy
if modo_posicionamiento:
    action NullAction()
else:
    action Call("mi_label")
```

---

## 4. Sistema de Restricciones

### API Completa

```renpy
# Activar restriccion
$ activar_restriccion(
    locaciones_permitidas=["casa_hmc", "casa_hviolet"],  # None = todas permitidas
    acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
    mensaje_movimiento="No puedo ir ahi ahora",
    mensajes_acciones={
        "avanzar_tiempo": "Mensaje especifico",
        "dormir": "Mensaje especifico",
    },
    mensaje_npc_bloqueado="No hay nadie en la casa",
    npcs_ocultos=["monica", "jasmine", "violet"],  # NPCs que no se renderizan
    npcs_interactuables=["violet"],   # NPCs con los que SI se puede hablar (default: ninguno)
    celular_bloqueado=True,
    mensaje_celular="No puedo usar el celular ahora",
    elementos_escena=[                 # Imagebuttons temporales sobre la locacion
        {
            "locacion": "casa_hmc",
            "tipo": "imagebutton",
            "id": "elemento_id",
            "imagen": "images/quest/.../imagen.png",
            "pos": (500, 400),
            "anchor": (0.5, 1.0),
            "label": "label_al_click",
        }
    ],
)

# Modificaciones dinamicas durante la restriccion
$ restriccion_quest_activa.registrar_label_locacion("casa_living", "mi_label")
$ restriccion_quest_activa.agregar_locacion_permitida("casa_cocina")
$ restriccion_quest_activa.remover_locacion_permitida("casa_hmc")
$ restriccion_quest_activa.ocultar_npc("violet")
$ restriccion_quest_activa.mostrar_npc("violet")
$ restriccion_quest_activa.hacer_npc_interactuable("violet")
$ restriccion_quest_activa.remover_elemento("elemento_id")

# Desactivar
$ desactivar_restriccion()

# Helpers de lectura
hay_restriccion_activa() -> bool
accion_bloqueada("dormir") -> str | None
npc_esta_oculto("violet") -> bool
npc_interactuable("violet") -> bool
obtener_elementos_escena("casa_hmc") -> list
```

### Flujo tipico con restriccion + labels por locacion

```
1. Label principal activa restriccion
2. Registra labels_por_locacion
3. Mover jugador + mostrar_hud() + jump game_loop
4. Jugador navega libremente dentro de locaciones_permitidas
5. Al entrar a una locacion con label registrado → se ejecuta automaticamente
6. Ese label puede: mostrar screens, dialogos, cambiar restriccion, etc.
7. El label DEBE terminar en `return` (llamado via call expression)
```

---

## 5. Crear un Evento Nuevo

### Archivos necesarios

1. **Definicion**: `game/script/characters/<npc>/events/events_<npc>.rpy`
2. **Labels**: `game/script/characters/<npc>/events/event_<npc>_XX.rpy`

### Plantilla

```renpy
# En events_<npc>.rpy, dentro de inicializar_events_<npc>():

event_<npc>_XX = Event(
    id="<npc>_event_XX",
    nombre="Nombre del Evento",
    tipo=TIPO_EVENT_ESPORADICO,           # ESPORADICO (una vez) o PERSISTENTE (repite)
    prioridad=10,
    condicion_aparicion=lambda: condicion,  # Cuando aparece
    condicion_activacion=lambda: condicion, # Cuando se puede activar (None = auto)
    label_efecto="event_<npc>_XX_narrativa",
    descripcion="Descripcion para el jugador",
    npc_id="<npc>",
    mensaje_pista="Pista del HUD",
    mensaje_que_hacer="Instruccion",
    mensaje_despertar="Mensaje al despertar",
    config_etapas={
        ESTADO_EVENT_VISIBLE: ConfigEtapa(
            pista="Pista mientras esta visible",
            que_hacer="Que hacer",
            mensaje_despertar="Mensaje al despertar",
        ),
    },
)
sistema_events.registrar_event(event_<npc>_XX)
```

### Estados

```
ESTADO_EVENT_OCULTO -> ESTADO_EVENT_VISIBLE -> ESTADO_EVENT_ACTIVO -> ESTADO_EVENT_COMPLETADO
```

### Modificaciones de eventos (rutinas, fondos, bloqueos)

```renpy
Event(
    modificaciones={
        "rutinas": {"violet": {(0, 2): "casa_hviolet"}},  # Override rutina NPC
        "fondos": {"casa_living": "images/bg/special.png"}, # Override background
        "bloqueos": ["avanzar_tiempo"],                      # Bloquear acciones
    },
)
```

---

## 6. NPCs — Definicion y Rutinas

### Characters definidos

```renpy
define mc = Character(...)            # Protagonista
define violet = Character(...)        # Violet
define monica = Character(...)        # Monica
define jasmine = Character(...)       # Jasmine
define piensa = Character(...)        # Pensamientos del MC (italica)
```

### Stats del NPC

```renpy
# Stat 1 (relacion/complicidad/adulacion/madurez): 0-100
$ cambiar_stat1("violet", 5)

# Stat 2 (afinidad/sumision/provocacion/debilidad): 0-100
$ cambiar_stat2("violet", 3)

# Progreso (oculto, tracking interno)
obtener_npc("violet").modificar_progreso(1)

# Interacciones diarias (se resetean al dormir)
interactuar_con_npc("violet", "hablar") -> bool
```

### Rutinas

```renpy
# Ubicacion por horario/dia
<npc>.establecer_rutina(dia_semana, horario, "locacion_id")

# Sprites visuales de rutina
establecer_rutina_visual_<npc>([0,1,2,3,4], 0, "idle_sprite.png", (500, 800))
```

---

## 7. Sistema de Tiempo

| Horario | Valor | Dia | Valor |
|---------|-------|-----|-------|
| Mañana | 0 | Lunes | 0 |
| Tarde | 1 | Martes | 1 |
| Noche | 2 | Miercoles | 2 |
| Trasnoche | 3 | Jueves | 3 |
| | | Viernes | 4 |
| | | Sabado | 5 |
| | | Domingo | 6 |

Variables: `horario_actual`, `dia_semana_actual`, `dia_actual`, `dias_totales`, `estacion_actual`, `año_actual`

`avanzar_horario()` actualiza rutinas NPCs + verifica quests + verifica fallos.
`dormir()` avanza dia, resetea interacciones, verifica entregas.

---

## 8. Sistema de Locaciones

### Locaciones de la Casa

| ID | Nombre |
|----|--------|
| `casa_hmc` | Habitacion MC |
| `casa_hviolet` | Habitacion Violet |
| `casa_hmonica` | Habitacion Monica |
| `casa_hjasmine` | Habitacion Jasmine |
| `casa_pasilloarriba` | Pasillo de arriba |
| `casa_pasilloabajo` | Pasillo de abajo |
| `casa_living` | Living |
| `casa_cocina` | Cocina |
| `casa_comedor` | Comedor |
| `casa_patio` | Patio |
| `casa_banioarriba` | Baño de arriba |
| `casa_banioabajo` | Baño de abajo |
| `casa_baniomonica` | Baño de Monica |
| `casa_gym` | Gimnasio |
| `casa_garage` | Garage |
| `casa_sotano` | Sotano |
| `casa_altillo` | Altillo |
| `casa_frente` | Frente de la casa |
| `fuera` | Fuera de la casa |

### Mover al Jugador

```renpy
$ sistema_locaciones.mover_a_locacion("casa_living")
```

### Hotspots

Tipos: `"MOVE"` (navega a otra locacion), `"ACTION"` (ejecuta label/funcion).
Se definen en `locations_house.rpy` dentro de `inicializar_locaciones_casa()`.

---

## 9. Sprites — Layered Images

### Estructura de Layered Image (grupos)

| Grupo | Prefijo | Ejemplo | Descripcion |
|-------|---------|---------|-------------|
| `area` | `a_` | `a_base`, `a_none` | Area/sombra base |
| `cabeza` | `ca_` | `ca_base`, `ca_pijama` | Cabeza/pelo |
| `boca` | `b_` | `b_hablando`, `b_hablandochica` | Expresion de boca |
| `ojos` | `o_` | `o_base`, `o_enojados` | Expresion de ojos |
| `cuerpo` | `c_` | `c_rbase_base`, `c_pijama_agotada` | Cuerpo/pose/ropa |
| `otros` | `ot_` | `ot_none`, `ot_avergonzada` | Efectos adicionales |

### Notacion de Comentarios de Sprites

Cada comando `show` que cambia un sprite parametrico (layeredimage) lleva UN comentario encima con el formato:

```
# (Personaje grupo_nombre grupo_nombre ...)
```

**Reglas:**
- Solo se listan los **elementos presentes en ese show especifico** (no todos los grupos)
- Los nombres son semanticos: se elimina el prefijo del atributo (`c_rbase_pensando` → `cuerpo pensando`)
- Las posiciones `at`, las transiciones `with`, y `xzoom` NO se incluyen en el comentario
- El nombre del personaje es `Mc` o `Violet` (mayuscula inicial)

**Ejemplos:**

```renpy
# (Mc cuerpo base ojos base boca neutral)
show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

# (Violet cuerpo fuck you)
show violet_parada c_rbase_fuckyou with sprite_normal

# (Mc boca hablando)
show mc_parado_base b_hablando
mc "Texto del MC"
# (Mc boca neutral)
show mc_parado_base b_none

# (Violet boca hablando)
show violet_parada b_hablando
violet "Texto de Violet"
# (Violet boca aburrida)
show violet_parada b_aburrida

# (Mc espalda brazos cruzados)
show mc_espalda_base brazoscruzados at mc_cerca:
    xzoom -1.0

# (Mc boca hablando cuerpo pensando)
show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
```

**Mapeos especiales:**
- `b_none` / `c_none` / `o_none` → `neutral` (sin esa parte del cuerpo)
- `ot_avergonzada` → `sonrojo`
- Atributos `nm` (sin mirar a camara): `o_abajonm` → `ojos abajo`, `o_arribanm` → `ojos arriba`
- `c_rbase_` → `cuerpo ` + resto; `c_pijama_` → `cuerpo pijama ` + resto

Referencia completa: [expresiones_referencia.md](.claude/skills/japitown-content/expresiones_referencia.md)

### Patron de Dialogo con Sprites

```renpy
# VIOLET HABLA: cambiar boca -> dialogo -> resetear boca
# (Violet boca hablando)
show violet_parada b_hablando
violet "Texto"
# (Violet boca neutral)
show violet_parada b_none

# MC HABLA
# (Mc boca hablando cuerpo brazos cruzados)
show mc_parado_base b_hablando c_rbase_brazoscruzados
mc "Texto"
# (Mc boca neutral)
show mc_parado_base b_none

# CAMBIO DE POSE COMPLETO (ojos + boca + cuerpo)
# (Mc cuerpo base ojos base boca neutral)
show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
```

### Convenciones de Imagenes

```
Idle sprites:  images/characters/casa/idle/idle_<npc>_casa_<locacion>_<horario>_<rutina>_<grupo>_<skin>.png
Quest images:  images/quest/<npc>/questX/<nombre_descriptivo>.png
Backgrounds:   images/bg/casa/bg_casa_<horario>_<locacion>.png
```

### Transiciones

```renpy
with fade           # Cambio de escena completo
with sprite_fast    # Cambio rapido de sprite
with sprite_normal  # Cambio normal de sprite
with dissolve       # Transicion suave
```

---

## 10. Chat / Mensajes

Archivo: `game/script/characters/<npc>/chat/chat_<npc>.rpy`

Activacion con `trigger_mensaje` en `ConfigEtapa`:
```renpy
trigger_mensaje=("grupo_chat_id", "npc_remitente")
```

Respuestas multiples (rafaga):
```renpy
OpcionRespuesta(
    texto="No entiendo",
    respuesta_npc=["Mensaje 1", "Mensaje 2", "Mensaje 3"],
)
```

---

## 11. Sistema de Pensamientos (Eventos de Cama)

```renpy
init 6 python:
    sistema_pensamientos.registrar_pensamiento(
        id="<npc>_pensamiento_X",
        npc_id="<npc>",
        nombre="Nombre del evento repetible",
        label="label_del_pensamiento",
        condicion=lambda: store.eventoX_completado == True
    )
```

El label asignado debe terminar en `return` (el sistema continua con dormir).

---

## 12. Checklist para Nuevo Contenido

### Nueva Quest
- [ ] Definicion en `quest_<npc>.rpy` con `Quest()` y `sistema_quests.registrar_quest()`
- [ ] Labels narrativos en `<npc>_quest_XX.rpy`
- [ ] Imagenes definidas como `image` al inicio del archivo de labels
- [ ] Variables `default` para estado de la quest
- [ ] Screens interactivos si son necesarios en `<npc>_questXX_screens.rpy`
- [ ] Mensajes de chat si los hay en `chat_<npc>.rpy`
- [ ] `$ ocultar_hud()` + `window show` al inicio de cada label narrativo
- [ ] `window hide` + `$ mostrar_hud()` + `jump game_loop` al devolver control
- [ ] `$ desactivar_restriccion()` + `$ completar_quest_actual("<npc>")` al finalizar
- [ ] Todos los botones verifican `modo_posicionamiento` con `NullAction()`
- [ ] Elementos posicionables registrados en `posicionamiento_elementos.rpy`

### Nuevo Evento
- [ ] Definicion en `events_<npc>.rpy` con `Event()` y `sistema_events.registrar_event()`
- [ ] Labels narrativos en `event_<npc>_XX.rpy`
- [ ] Funciones de condicion de aparicion y activacion
- [ ] `event.completar()` al finalizar la narrativa

### Nuevos Sprites
- [ ] Agregar atributos al `layeredimage` en `visual/sprites_<npc>.rpy`
- [ ] Seguir convencion de nombres: `<npc>_parada_<grupo>_<atributo>.png`
- [ ] Imagenes en `images/characters/casa/<npc>/`

---

## Recursos adicionales

- Sistema de quests: [questsystem_core.rpy](game/script/core/quests/questsystem_core.rpy)
- Sistema de restricciones: [restriccion_quest_system.rpy](game/script/core/quests/restriccion_quest_system.rpy)
- Sistema de eventos: [eventsystem_core.rpy](game/script/core/events/eventsystem_core.rpy)
- Sistema de NPCs: [npcsystem_core.rpy](game/script/core/npcs/npcsystem_core.rpy)
- Interacciones del gameloop: [npcsystem_interactions.rpy](game/script/core/npcs/npcsystem_interactions.rpy)
- Pensamientos nocturnos: [pensamiento_system.rpy](game/script/core/thoughts/pensamiento_system.rpy)
- Ejemplo quest con screens: [violet_quest_04.rpy](game/script/characters/violet/quests/violet_quest_04.rpy)
- Ejemplo screens interactivos: [violet_quest04_screens.rpy](game/script/characters/violet/screens/violet_quest04_screens.rpy)
- Ejemplo evento: [events_monica.rpy](game/script/characters/monica/events/events_monica.rpy)
