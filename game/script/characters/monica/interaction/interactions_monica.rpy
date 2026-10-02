################################################################################
## Interacciones de Mónica
################################################################################

# Variable temporal para preview de skin
default _skin_preview_monica = None

label interaccion_monica:
    # Guardar NPC actual
    $ _npc_actual = obtener_npc("monica")
    
    if not _npc_actual:
        return
    
    # Obtener el evento (ya fue validado en game_loop con validar_eventos()).
    # El masaje ya NO se auto-dispara al clickear a Mónica: se inicia con el botón
    # "(Evento)" del menú (más abajo, en las opciones extra).
    $ _event_monica = obtener_event("monica_event_01")

    # NOTA DE ARQUITECTURA (2026-07-31): acá había un gate que auto-ejecutaba la
    # quest activa y saltaba SIN abrir el menú. Se eliminó.
    #
    # El problema: el botón "Hablar" del sistema de talk vive DENTRO del menú, y
    # el menú era la última línea de este label — así que cualquier quest que
    # secuestrara el click hacía desaparecer Talk, aunque no tuviera nada que ver
    # (ver E09: la quest 0_c dejaba a Mónica sin Hablar para siempre).
    # Se mantenía con una lista negra de exclusiones cuyo default era inseguro:
    # olvidarse de agregar una quest = secuestra el click.
    #
    # Ahora el menú SIEMPRE se abre, y las quests se inician con su propio botón
    # (arriba de todo, antes de los eventos y de Hablar). Un disparador por quest,
    # explícito y visible.

    # Opciones extra del menú, en orden: quest → evento → (Hablar lo agrega el screen)
    $ _opciones_extra_monica = []

    # Quest 0: botón "Agradecerle" — solo cuando la quest está lista y el MC
    # está a solas con Mónica (ningun otro NPC en la locación).
    if quest_lista_para_boton("monica_questprincipal_0"):
        $ _m0_presentes = npcs_en_locacion_actual()
        if len(_m0_presentes) == 1 and _m0_presentes[0].id == "monica":
            $ _opciones_extra_monica.append({
                "texto": "Agradecerle",
                "label": "monica_q0_agradecer",
                "condicion": True,
                "quest_id": "monica_questprincipal_0"
            })
    
    # Evento 1 (masaje) — primera vez: botón "(Evento)" que inicia el masaje
    # cuando el evento está visible y Mónica está en el living por la tarde.
    if _event_monica and _event_monica.estado == ESTADO_EVENT_VISIBLE and monica_en_living_tarde():
        $ _opciones_extra_monica.append({
            "texto": "Ofrecerle un masaje",
            "label": "event_monica_01_narrativa",
            "condicion": True,
            "tipo": "evento"
        })

    # Si evento 1 completado y está en living por la tarde, agregar opción de repetir
    if monica_event_01_completado() and monica_en_living_tarde():
        $ _opciones_extra_monica.append({
            "texto": "¿Me das un masaje?",
            "label": "event_monica_01_check_replay",
            "condicion": True,
            "tipo": "evento"
        })

    # Quest 09_a: opciones relacionadas con la enfermedad de Violet
    if quest_lista_para_boton("violet_questprincipal_09_a"):
        # "Preguntar por Violet" mientras el MC no sabe que está enferma
        if not getattr(store, 'mc_sabe_violet_enferma', False):
            $ _opciones_extra_monica.append({
                "texto": "Preguntar por Violet",
                "label": "violet_quest09a_monica_preguntar",
                "condicion": True,
                "quest_id": "violet_questprincipal_09_a"
            })
        # "Te llama Violet" cuando Violet pidió que venga Monica y no se completó aún
        if (getattr(store, 'violet_9a_pedido_actual', None) == "Dile a Monica que venga" and
                not getattr(store, 'violet_9a_tiene_entregable', False)):
            $ _opciones_extra_monica.append({
                "texto": "Te llama Violet",
                "label": "violet_quest09a_monica_llamar",
                "condicion": True,
                "quest_id": "violet_questprincipal_09_a"
            })

    call screen menu_interaccion_npc_completo(_npc_actual, opciones_extra=_opciones_extra_monica)

    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        $ _label_opcion_monica = despachar_opcion_quest(_return, origen="menu:monica")
        jump expression _label_opcion_monica

    return
