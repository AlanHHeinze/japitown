image escena_final_quest0_mc = "images/quest/mc/quest0/escena_final_quest0_mc.jpg"

################################################################################
## Quest 0 del MC — De nuevo en casa
################################################################################
## El MC recorre la casa para familiarizarse con ella recién llegado.
## Exploración: el jugador se mueve libremente y tiene que pasar por el Pasillo
## de Abajo, el Pasillo de Arriba y el Patio. No hace falta que reconozca cada
## conexión: para eso está el panel de viaje rápido.

# ── Estado de la quest ──────────────────────────────────────────────────────
default mc_q0_explorando = False
default mc_q0_locaciones_exploradas = set()
default mc_q0_entrada_mostrada = set()

# Fase mudanza
default mc_q0_cajas_en_garage = False
default mc_q0_mudanza_garage_activa = False
default mc_q0_mudanza_hmc_activa = False
default mc_q0_entrada_garage_mostrada = False

# Fase espera / stage B / sueño final
default mc_q0_esperar_horario = False
default mc_q0_final_sleep = False


# ── Constantes ───────────────────────────────────────────────────────────────

init 5 python:
    # Idle de cajas en el garage — posicionable con la herramienta (P)
    sistema_pos.registrar(
        "mc_q0_cajas_intro",
        "images/quest/mc/quest0/idle_cajas_intro.webp",
        "Cajas intro",
        "quest_elemento",
        960, 900,
        xanchor=0.5, yanchor=1.0,
    )


init python:

    # Locaciones que hay que visitar para terminar la exploración: (id, nombre, cómo llegar).
    # Los nombres deben coincidir con locaciones_pendientes de la QuestMC "mc_quest_0"
    # (quest_mc.rpy), que es de donde sale el "Visitar: ..." de la pista.
    # Las tres se alcanzan desde el Living, por eso las pistas lo toman como referencia.
    # Las pistas van cortas a proposito: el area de texto muestra 4 renglones y una
    # linea larga envuelve y se come otro. Como las tres salen del Living, eso se
    # dice una sola vez en la cabecera en lugar de repetirlo en cada linea.
    MC_Q0_OBJETIVOS = [
        ("casa_pasilloarriba", "Pasillo arriba", "por la escalera"),
        ("casa_pasilloabajo",  "Pasillo abajo",  "por la flecha de abajo a la izquierda"),
        ("casa_patio",         "Patio",          "por el ventanal del centro"),
    ]

    MC_Q0_LOCS_OBJETIVO = frozenset(_id for (_id, _n, _c) in MC_Q0_OBJETIVOS)
    MC_Q0_NOMBRES_OBJETIVO = {_id: _n for (_id, _n, _c) in MC_Q0_OBJETIVOS}

    # Durante la intro las chicas están ocultas (npcs_ocultos). Entrar a sus
    # habitaciones dispararía la interacción de puerta de una NPC que el juego
    # considera ausente, así que quedan afuera del recorrido libre.
    MC_Q0_LOCS_BLOQUEADAS = frozenset({
        "casa_hmonica", "casa_hviolet", "casa_hjasmine", "casa_baniomonica",
    })


# ── Helpers Python ────────────────────────────────────────────────────────────

init python:

    def mc_q0_locs_exploracion():
        """Locaciones habilitadas durante el recorrido: toda la casa menos las
        habitaciones de las chicas (ver MC_Q0_LOCS_BLOQUEADAS)."""
        return [l.id for l in sistema_locaciones.locaciones.values()
                if l.id.startswith("casa_") and l.id not in MC_Q0_LOCS_BLOQUEADAS]

    def mc_q0_registrar_exploracion(loc_id):
        """Marca una locación objetivo como visitada: estado interno + pista de la quest."""
        store.mc_q0_locaciones_exploradas = store.mc_q0_locaciones_exploradas | {loc_id}
        nombre = MC_Q0_NOMBRES_OBJETIVO.get(loc_id)
        if nombre:
            quest = store.sistema_quests_mc.quests.get("mc_quest_0")
            if quest:
                quest.marcar_locacion_visitada(nombre)

    def mc_q0_exploracion_terminada():
        """True cuando ya se visitaron las 3 locaciones objetivo."""
        return MC_Q0_LOCS_OBJETIVO.issubset(store.mc_q0_locaciones_exploradas)

    # --- Triggers de motor de la quest 0 (registros de triggers_contenido) ---

    def _gl_trigger_mc_q0_exploracion():
        # Recorrido libre terminado (visito las 3 locaciones objetivo). Vive en
        # el game_loop y no en los labels de entrada porque esos llegan por
        # call expression y deben retornar; este jump es frameless.
        if getattr(store, 'mc_q0_explorando', False) and mc_q0_exploracion_terminada():
            return "mc_q0_exploracion_completada"
        return None

    def _avanzar_trigger_mc_q0():
        # Al avanzar horario en la etapa de espera de la quest 0.
        if getattr(store, 'mc_q0_esperar_horario', False):
            store.mc_q0_esperar_horario = False
            return "mc_q0_stage_b"
        return None

    def _dormir_trigger_mc_q0_final():
        # Primer sueño al finalizar la introduccion: cierra la quest 0 y apaga
        # las ayudas visuales. Solo efectos python, el sueño sigue normal.
        if getattr(store, 'mc_q0_final_sleep', False):
            store.mc_q0_final_sleep = False
            desactivar_restriccion()
            store.sistema_quests_mc.completar_activa()
            store.config_mostrar_accion_movimiento = False
            store.visualizador_hotspot_activo = False
        return None

    # El area de texto muestra 4 lineas, por eso el aviso de entrada va partido en
    # dos mensajes: primero donde estas (1 linea) y despues que falta (cabecera +
    # hasta 3 objetivos = 4 lineas justas).

    def mc_q0_mensaje_ubicacion(loc_id):
        """Primer mensaje: 'Esto es <locación>'."""
        loc = sistema_locaciones.obtener_locacion(loc_id)
        nombre = renpy.translate_string(loc.nombre) if loc else loc_id
        return renpy.translate_string("Esto es") + u" " + colorear_locacion(nombre)

    def mc_q0_mensaje_faltantes():
        """
        Segundo mensaje: locaciones objetivo que faltan y cómo llegar a cada una.
        Devuelve "" si ya no falta ninguna (ahí no se muestra el segundo mensaje).
        """
        vistas = store.mc_q0_locaciones_exploradas
        faltantes = [(n, c) for (i, n, c) in MC_Q0_OBJETIVOS if i not in vistas]
        if not faltantes:
            return u""

        lineas = [renpy.translate_string("Locaciones faltantes a visitar, todas desde el Living:")]
        for nombre_obj, como_llegar in faltantes:
            lineas.append(u"{} ({})".format(
                colorear_locacion(renpy.translate_string(nombre_obj)),
                renpy.translate_string(como_llegar),
            ))
        return u"\n".join(lineas)

    def mc_q0_activar_rutinas_npc():
        """Pone a Monica, Jasmine y Violet en sus habitaciones para toda la quest."""
        habitaciones = {
            "monica":  "casa_hmonica",
            "jasmine": "casa_hjasmine",
            "violet":  "casa_hviolet",
        }
        for npc_id, hab in habitaciones.items():
            npc = obtener_npc(npc_id)
            if npc:
                npc.rutinas_quest.clear()
                for dia in range(7):
                    for horario in range(4):
                        npc.rutinas_quest[(dia, horario)] = RutinaQuest(locacion=hab)
        actualizar_rutinas_npcs()

    def mc_q0_limpiar_rutinas_npc():
        """Restaura rutinas normales de los NPCs."""
        for npc_id in ["monica", "jasmine", "violet"]:
            npc = obtener_npc(npc_id)
            if npc:
                npc.rutinas_quest.clear()
        actualizar_rutinas_npcs()


################################################################################
## Label principal — inicio de la quest
################################################################################

label quest_mc_quest_0:

    # Asegurar ubicación correcta
    $ sistema_locaciones.mover_a_locacion("casa_living")

    # Rutinas: las tres chicas en sus habitaciones durante toda la quest
    $ mc_q0_activar_rutinas_npc()

    # Bg especial de la habitacion del MC (sin acomodar). Se aplica desde el
    # arranque porque en el recorrido libre ya se puede entrar a la habitacion;
    # mc_q0_mudanza_completada lo devuelve al bg normal.
    python:
        _loc_hmc = sistema_locaciones.locaciones.get("casa_hmc")
        if _loc_hmc:
            _loc_hmc.background_base = "images/quest/mc/quest0/bg_casa_intro_hmc.webp"

    # Estado
    $ mc_q0_explorando = True
    $ mc_q0_locaciones_exploradas = set()
    $ mc_q0_entrada_mostrada = set()

    # Activar la visualización de hotspots (la config tambien)
    $ config_mostrar_accion_movimiento = True
    $ visualizador_hotspot_activo = True

    # Recorrido libre: se puede ir a cualquier lado de la casa salvo las
    # habitaciones de las chicas. El objetivo son las 3 locaciones conectoras.
    $ activar_restriccion(
        locaciones_permitidas=mc_q0_locs_exploracion(),
        acciones_bloqueadas=[
            "avanzar_tiempo", "dormir", "entrenar",
            "trabajar", "comprar", "ver_tv", "usar_item",
        ],
        mensaje_movimiento="No voy a meterme en sus habitaciones apenas llego",
        celular_bloqueado=True,
        mensaje_celular="Mejor termino de recorrer la casa antes",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )
    # Mensaje de entrada en TODAS las locaciones habilitadas, no solo en las 3
    # objetivo: al llegar a cualquier lado el juego recuerda qué falta y cómo ir.
    python:
        for _mcq0_loc in mc_q0_locs_exploracion():
            restriccion_quest_activa.registrar_label_locacion(_mcq0_loc, "mc_q0_entrada_locacion")

    # Actualizar la quest MC en el panel de pistas
    $ sistema_quests_mc.iniciar("mc_quest_0")

    # Piensa iniciales
    $ ocultar_hud()
    window show

    piensa "Que nostalgia, han pasado años desde la última vez que estuve en esta casa "
    piensa "Podría recorrer un poco la casa antes de guardar las cosas"
    piensa "Me gustaría ver que tanto cambio"

    tutorial "Aprendamos como movernos. Todos los puntos de movimiento están remarcados en la pantalla, al hacer click en uno nos llevara a la locacion conectada"
    tutorial "A medida que durante el juego te muevas por la casa, la iras conociendo mejor y moverte sea algo simple"
    tutorial "Ahora vamos a centrarnos en 4 locaciones que son las que conectan a la mayoría.{w} El [colorear_locacion('Living')], el [colorear_locacion('Patio')], el [colorear_locacion('Pasillo de abajo')] y el [colorear_locacion('Pasillo de arriba')]"
    tutorial "Vamos a recorrerlos uno por uno"

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## Entrada a una locación durante el recorrido
## Un solo label para TODAS las locaciones: dice dónde estás y qué falta visitar.
## Llega por call expression (accion_hotspot_move), asi que termina en return:
## cuando ya se visitaron las 3, el hook del game_loop es el que dispara
## mc_q0_exploracion_completada.
################################################################################

label mc_q0_entrada_locacion:
    $ _mcq0_loc_id = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else ""

    if _mcq0_loc_id and _mcq0_loc_id not in mc_q0_entrada_mostrada:
        $ mc_q0_entrada_mostrada = mc_q0_entrada_mostrada | {_mcq0_loc_id}

        # Si es una de las 3 objetivo, registrarla ANTES de armar el mensaje
        # para que no se liste a sí misma como faltante.
        if _mcq0_loc_id in MC_Q0_LOCS_OBJETIVO:
            $ mc_q0_registrar_exploracion(_mcq0_loc_id)

        $ actualizar_bg_master()
        $ ocultar_hud()
        window show

        $ _mcq0_msg_ubi = mc_q0_mensaje_ubicacion(_mcq0_loc_id)
        tutorial "[_mcq0_msg_ubi]"

        # El segundo mensaje se omite cuando ya no falta ninguna
        $ _mcq0_msg_falt = mc_q0_mensaje_faltantes()
        if _mcq0_msg_falt:
            tutorial "[_mcq0_msg_falt]"

        window hide
        $ mostrar_hud()
    return


################################################################################
## Exploración completada → siguiente etapa de la quest
## Lo dispara el game_loop (frameless), por eso la cadena termina en jump.
################################################################################

label mc_q0_exploracion_completada:

    $ mc_q0_explorando = False

    $ ocultar_hud()
    window show

    tutorial "Esas son las [colorear_locacion('habitaciones')] con más conexiones dentro de la casa"
    tutorial "Durante el juego te podras mover libremente y explorar cada lugar, el movimiento no tiene ningún costo así que sientete libre de hacerlo"
    tutorial "Siempre que quieras puedes [colorear_quest('activar')] y [colorear_quest('desactivar')] la ayuda de movimiento con el [colorear_quest('boton del ojo')] que tendras en la [colorear_quest('barra de acciones')] de la locacion"
    tutorial "Una vez que estes familiarizado con el movimiento, dentro del [colorear_quest('celular')] en las [colorear_quest('opciones')] podras directamente [colorear_quest('desactivarla')] si así lo prefieres"
    tutorial "Tambien tendras una forma adicional para moverte por la casa si prefieres algo mas directo. En el [colorear_quest('Menu superior')] tienes 4 botones, [colorear_quest('el que tiene el icono de la casa')] te despliega una lista con todas las locaciones a las que te puedes mover"
    tutorial "En esta lista tambien veras la locacion en la que te encuentras actualmente, y las locaciones en la que se encuentran los otros [colorear_quest('personajes')]"

    window hide
    $ mostrar_hud()

    jump mc_q0_mudanza


################################################################################
## Fase Mudanza — buscar cajas en garage y llevarlas a la habitacion
################################################################################

label mc_q0_mudanza:

    # Activar cajas y accion de mudanza en el garage
    $ mc_q0_cajas_en_garage = True
    $ mc_q0_mudanza_garage_activa = True
    $ mc_q0_mudanza_hmc_activa = True

    # Restricción: solo puede ir a hmc, pasillo arriba, living, garage
    $ activar_restriccion(
        locaciones_permitidas=[
            "casa_hmc", "casa_pasilloarriba",
            "casa_living", "casa_garage",
        ],
        acciones_bloqueadas=[
            "avanzar_tiempo", "dormir", "entrenar", "trabajar",
            "ver_tv", "usar_item", "comprar",
        ],
        mensaje_movimiento="Monica dijo que las cosas están en el garage",
        mensaje_accion_default="Debo ocuparme de las cosas de la mudanza",
        celular_bloqueado=True,
        mensaje_celular="Debo ocuparme de las cosas de la mudanza",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )
    $ restriccion_quest_activa.registrar_label_locacion("casa_garage", "mc_q0_entrada_garage")

    $ ocultar_hud()
    window show

    piensa "Bueno... Monica dijo que mis cosas están en el [colorear_locacion('Garage')]"
    piensa "Voy a buscarlas y subirlas a [colorear_locacion('Mi Habitación')]"

    window hide
    $ mostrar_hud()
    jump game_loop


label mc_q0_entrada_garage:
    if not mc_q0_entrada_garage_mostrada:
        $ mc_q0_entrada_garage_mostrada = True
        $ actualizar_bg_master()
        # Mostrar cajas junto al bg (el HUD que las renderiza se oculta a continuación)
        $ _cajas_pos = sistema_pos.obtener("mc_q0_cajas_intro")
        $ _cajas_x = _cajas_pos.x if _cajas_pos else 629
        $ _cajas_y = _cajas_pos.y if _cajas_pos else 422
        show expression "images/quest/mc/quest0/idle_cajas_intro.webp" as cajas_temp:
            xpos _cajas_x ypos _cajas_y xanchor 0.0 yanchor 0.0
        $ ocultar_hud()
        window show
        piensa "Ahí están mis cosas. Tengo que llevarlo todo a mi habitación"

        tutorial "Al entrar a una locacion tendremos un [colorear_quest('menu flotante')] con las [colorear_quest('acciones')] que podremos hacer en la misma"
        tutorial "Algunas [colorear_quest('acciones')] estaran siempre disponibles al entrar a una locacion"
        tutorial "Mientras que otras solo estaran disponibles durante una parte de una [colorear_quest('quest')] o un [colorear_quest('evento')]"
        tutorial "Ahora vamos a usar la acción de [colorear_quest('acción mudanza')] para recoger las cajas"
        window hide
        hide cajas_temp
        $ mostrar_hud()
    return


################################################################################
## Accion Mudanza — Garage
################################################################################

label mudanza_garage_generico:
    $ ocultar_hud()
    window show

    piensa "Voy a agarrar todo esto y subirlo"

    window hide
    $ mostrar_hud()

    # Quitar el idle de cajas
    $ mc_q0_cajas_en_garage = False
    # Desactivar la accion del garage
    $ mc_q0_mudanza_garage_activa = False
    # Dar el item al inventario
    $ agregar_al_inventario("mis_cosas")

    # Cambiar el mensaje de bloqueo de movimiento
    $ restriccion_quest_activa.mensaje_movimiento = "Debo llevar todas las cajas a mi habitación"

    $ ocultar_hud()
    window show

    piensa "Son bastantes cosas"
    piensa "Es momento de llevar todo a [colorear_locacion('Mi Habitación')]"

    window hide
    $ mostrar_hud()
    return


################################################################################
## Accion Mudanza — Habitacion del MC
################################################################################

label mudanza_hmc_generico:
    if "mis_cosas" not in inventario or inventario.get("mis_cosas", 0) <= 0:
        piensa "Primero tengo que buscar mis cosas en el garage"
        return

    $ ocultar_hud()
    window show

    piensa "Momento de empeza a acomodar todo"

    window hide
    $ mostrar_hud()

    $ quitar_del_inventario("mis_cosas")
    $ mc_q0_mudanza_hmc_activa = False

    jump mc_q0_mudanza_completada


################################################################################
## Mudanza completada — pantalla negra + Stage A (esperar horario)
################################################################################

label mc_q0_mudanza_completada:

    $ ocultar_hud()

    # Restaurar bg normal de la habitacion antes de avanzar horario
    python:
        _loc_hmc = sistema_locaciones.locaciones.get("casa_hmc")
        if _loc_hmc:
            _loc_hmc.background_base = "images/bg/casa/bg_casa_{horario}_hmc.jpg"

    # Pantalla negra con texto.
    # `show text "..."` con literal NO se traduce (no es un say ni texto de screen):
    # hay que envolverlo en Text(renpy.translate_string(...)), igual que la intro.
    scene black with fade
    show text Text(renpy.translate_string("Algunas horas después..."), size=50, color="#FFFFFF",
        outlines=[(2, "#000000", 0, 0)]) at truecenter with dissolve
    pause 2.5
    hide text with dissolve

    # Avanzar horario (actualiza el bg de la hmc al nuevo horario con fade)
    $ avanzar_horario()

    window show

    piensa "Listo. Ya esta todo acomodado"
    piensa "Monica dijo que ibamos a salir por la [colorear_quest('noche')], todavía falta algo de tiempo"
    piensa "Podría relajarme un momento"

    tutorial "Hacer algunas acciones o quest avanzaran el tiempo automaticamente"
    tutorial "También puedes avanzarlo de forma manual haciendo [colorear_quest('haciendo click en el indicador de horario')] que se encuentra al centro de la parte superior"
    tutorial "Prueba avanzar el tiempo hasta la noche"

    window hide

    # Restricción Stage A: solo se puede avanzar el tiempo, sin salir de la habitacion
    $ activar_restriccion(
        locaciones_permitidas=["casa_hmc"],
        acciones_bloqueadas=[
            "dormir", "entrenar", "trabajar",
            "ver_tv", "usar_item", "comprar",
        ],
        mensaje_movimiento="Tengo que hacer tiempo hasta la noche",
        mensaje_accion_default="Tengo que hacer tiempo hasta la noche",
        celular_bloqueado=True,
        mensaje_celular="Tengo que hacer tiempo hasta la noche",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    $ mc_q0_esperar_horario = True
    $ mostrar_hud()
    jump game_loop


################################################################################
## Stage B — ir al frente
################################################################################

label mc_q0_stage_b:

    $ ocultar_hud()
    window show

    piensa "Ese descanso me vino bien"
    piensa "Las chicas ya deben estar listas para salir"
    piensa "Voy al [colorear_locacion('Frente')] de la casa para encontrarlas"

    window hide

    # Restricción Stage B: solo puede moverse a pasillo arriba, living y frente
    $ activar_restriccion(
        locaciones_permitidas=[
            "casa_pasilloarriba", "casa_living", "casa_frente",
        ],
        acciones_bloqueadas=[
            "avanzar_tiempo", "dormir", "entrenar", "trabajar",
            "ver_tv", "usar_item", "comprar",
        ],
        mensaje_movimiento="Debo ir al frente",
        mensaje_accion_default="No puedo, las chicas me están esperando",
        celular_bloqueado=True,
        mensaje_celular="No puedo, las chicas me están esperando",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )
    $ restriccion_quest_activa.registrar_label_locacion("casa_frente", "mc_q0_entrada_frente")

    $ mostrar_hud()
    jump game_loop


label mc_q0_entrada_frente:
    $ desactivar_restriccion()
    $ mc_q0_limpiar_rutinas_npc()
    jump mc_q0_siguiente_etapa


################################################################################
## Inicio directo (Omitir intro) — arranca en martes mañana con quest 0 completa
################################################################################

label mc_q0_inicio_directo:
    # Lunes por la noche en la habitacion del MC
    $ dia_semana_actual = 0   # Lunes
    $ horario_actual = 3      # Trasnoche
    $ dia_actual = 1
    $ dias_totales = 1
    $ actualizar_rutinas_npcs()
    $ sistema_locaciones.mover_a_locacion("casa_hmc")
    $ actualizar_bg_master()

    # Visualizador de hotspots apagado (nunca se activó en este path)
    $ config_mostrar_accion_movimiento = False
    $ visualizador_hotspot_activo = False

    # Activar el hook de cleanup que dispara al dormir
    $ mc_q0_final_sleep = True

    $ ocultar_hud()
    window show
    piensa "Hice muchas cosas el día de hoy y estoy completamente agotado"
    piensa "Mejor duermo, mañana sera un día nuevo para ponerme al día con las chicas"
    window hide
    $ mostrar_hud()

    # Ejecutar dormir automáticamente — avanza al martes mañana
    # El hook mc_q0_final_sleep completa la quest y apaga la config
    call accion_dormir from _call_mc_q0_inicio_directo_dormir

    jump game_loop


################################################################################
## Escena final de la intro — contemplación + primer sueño
################################################################################

label mc_q0_siguiente_etapa:

    $ ocultar_hud()
    window show

    scene escena_final_quest0_mc with fade

    piensa "Estoy agotado, no se si fue por la mudanza, por el viaje, por mi padre..."
    piensa "Quizás sea un poco de todo"
    piensa "Pero este momento me hace sentir que estoy en el lugar correcto y con las personas correctas"
    piensa "Es el momento de disfrutar"

    # Llevar al jugador a su habitacion en la trasnoche
    $ sistema_locaciones.mover_a_locacion("casa_hmc")
    $ horario_actual = 3
    $ actualizar_bg_master()

    piensa "No quería que el día termine, tenía tantas cosas por hablar con ellas"
    piensa "Pero tengo muchos días por delante para hacerlo, estando aquí el tiempo ya no es un problema"
    piensa "Ahora a dormir"
    tutorial "Para pasar al día siguiente haz [colorear_quest('click sobre la cama')]"

    window hide
    $ mostrar_hud()

    # Restricción: solo se puede dormir
    $ activar_restriccion(
        locaciones_permitidas=None,
        acciones_bloqueadas=[
            "avanzar_tiempo", "entrenar", "trabajar",
            "ver_tv", "usar_item", "comprar",
        ],
        mensaje_accion_default="Es tarde, debo dormir",
        celular_bloqueado=True,
        mensaje_celular="Es tarde, debo dormir",
    )

    $ mc_q0_final_sleep = True
    jump game_loop


################################################################################
## Registro de triggers de motor (triggers_contenido.rpy)
################################################################################

init 5 python:
    # Prioridades: replican el orden de los ifs que estos registros reemplazan
    # (game_loop: violet_09a=40, jasmine_0b=30, exploracion=20, mc_q0b=10;
    # dormir "despues": mc_q0_final=40 corre primero).
    registrar_trigger_game_loop(
        "mc_q0_exploracion", _gl_trigger_mc_q0_exploracion, prioridad=20)
    registrar_trigger_avanzar("mc_q0_espera", _avanzar_trigger_mc_q0)
    registrar_trigger_dormir(
        "mc_q0_final", "despues", _dormir_trigger_mc_q0_final, prioridad=40)
