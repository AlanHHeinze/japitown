image escena_final_quest0_mc = "images/quest/mc/quest0/escena_final_quest0_mc.jpg"

################################################################################
## Quest 0 del MC — De nuevo en casa
################################################################################
## El MC llega a la casa, se le explica como moverse y se instala.
##
## EL RECORRIDO OBLIGATORIO YA NO EXISTE. Antes habia que pasar si o si por el
## Pasillo de Abajo, el Pasillo de Arriba y el Patio para que la quest avanzara:
## el juego bloqueaba las habitaciones de las chicas, listaba las locaciones que
## faltaban cada vez que entrabas a algun lado y recien despues seguia.
##
## Ahora el tutorial SOLO EXPLICA: dice como funciona el movimiento, cuales son
## las cuatro locaciones que conectan a la mayoria y como se apaga la ayuda, y
## pasa derecho a la mudanza. El jugador conoce la casa moviendose cuando quiere
## — que era lo que el recorrido forzado intentaba conseguir a los empujones.

# ── Estado de la quest ──────────────────────────────────────────────────────

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


# ── Helpers Python ────────────────────────────────────────────────────────────

init python:

    # --- Triggers de motor de la quest 0 (registros de triggers_contenido) ---

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
            desactivar_restriccion(duenio="mc_0_a")
            store.sistema_quests_mc.completar_activa()
            store.config_mostrar_accion_movimiento = False
            store.visualizador_hotspot_activo = False
        return None

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
    # arranque, antes de que la mudanza pueda llevar al jugador ahi;
    # mc_q0_mudanza_completada lo devuelve al bg normal.
    python:
        _loc_hmc = sistema_locaciones.locaciones.get("casa_hmc")
        if _loc_hmc:
            _loc_hmc.background_base = "images/quest/mc/quest0/bg_casa_intro_hmc.webp"

    # Activar la visualización de hotspots (la config tambien). Se prende igual
    # que antes: el tutorial explica que los puntos de movimiento estan
    # remarcados, y despues cuenta como apagarlos.
    $ config_mostrar_accion_movimiento = True
    $ visualizador_hotspot_activo = True

    # Actualizar la quest MC en el panel de pistas
    $ sistema_quests_mc.iniciar("mc_quest_0")

    # Piensa iniciales
    $ ocultar_hud()
    window show

    piensa "Qué nostalgia, han pasado años desde la última vez que estuve en esta casa"
    piensa "Podría recorrer un poco la casa antes de guardar las cosas"
    piensa "Me gustaría ver qué tanto cambió"

    tutorial "Para movernos por una locación lo podemos hacer haciendo click en puntos de movimiento (Normalmente estarán ubicados en puertas o escaleras)"
    tutorial "O mediante el panel de movimiento rápido que se encuentra en la parte superior de la pantalla y tiene el icono de una casa"

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
        duenio="mc_0_a",
        locaciones_permitidas=[
            "casa_hmc", "casa_pasilloarriba",
            "casa_living", "casa_garage",
        ],
        acciones_bloqueadas=[
            "avanzar_tiempo", "dormir", "entrenar", "trabajar",
            "ver_tv", "usar_item", "comprar",
        ],
        mensaje_movimiento="Mónica dijo que las cosas están en el Garage",
        mensaje_accion_default="Debo ocuparme de las cosas de la mudanza",
        celular_bloqueado=True,
        mensaje_celular="Debo ocuparme de las cosas de la mudanza",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )
    $ restriccion_quest_activa.registrar_label_locacion("casa_garage", "mc_q0_entrada_garage")

    $ ocultar_hud()
    window show

    piensa "Bueno... Mónica dijo que mis cosas están en el [colorear_locacion('Garage')]"
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

        tutorial "Al entrar a una locación tendremos un menú flotante con las acciones disponibles a realizar en ese lugar"
        tutorial "Esta es la forma de interactuar con los elementos de cada lugar"
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

    piensa "Momento de empezar a acomodar todo"

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

    piensa "Listo. Ya está todo acomodado"
    piensa "Mónica dijo que íbamos a salir por la [colorear_quest('noche')]. Todavía falta algo de tiempo"
    piensa "Podría relajarme un momento"

    tutorial "Para pasar el tiempo haz click en el botón central de la parte superior de la pantalla"


    window hide

    # Restricción Stage A: solo se puede avanzar el tiempo, sin salir de la habitacion
    $ activar_restriccion(
        duenio="mc_0_a",
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
        duenio="mc_0_a",
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
    $ desactivar_restriccion(duenio="mc_0_a")
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
    piensa "Mejor duermo. Mañana será un día nuevo para ponerme al día con las chicas"
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

    piensa "Estoy agotado, no sé si fue por la mudanza, por el viaje, por mi padre..."
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

    tutorial "Para pasar al día siguiente haz click sobre la cama"

    window hide
    $ mostrar_hud()

    # Restricción: solo se puede dormir
    # validar_bloqueos: reloj libre — la salida es dormir; cocinar solo mueve el horario y no importa
    $ activar_restriccion(
        duenio="mc_0_a",
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
    # El trigger de game_loop "mc_q0_exploracion" (prioridad 20) se elimino junto
    # con el recorrido obligatorio: era el que vigilaba si ya habias visitado las
    # tres locaciones. Las prioridades que quedan no cambian.
    registrar_trigger_avanzar("mc_q0_espera", _avanzar_trigger_mc_q0)
    registrar_trigger_dormir(
        "mc_q0_final", "despues", _dormir_trigger_mc_q0_final, prioridad=40)
