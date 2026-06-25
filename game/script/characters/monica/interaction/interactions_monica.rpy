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

    # Verificar si hay quest lista para ejecutar
    $ _quest_activa = sistema_quests.obtener_quest_activa("monica")

    # Quests que NO se auto-disparan al hacer click:
    #  - 0   : se inicia con el botón "Agradecerle" (a solas con Mónica).
    #  - 0_b : se dispara solo al entrar al living (auto-trigger por locación).
    if (_quest_activa and _quest_activa.etapa_actual == 5 and
            _quest_activa.id not in ("monica_questprincipal_0", "monica_questprincipal_0_b")):
        $ exito, mensajes = _quest_activa.intentar_ejecutar()
        if exito:
            $ _npc_id_temp = "monica"
            jump ejecutar_quest_activa

    # Si no hay evento ni quest, mostrar menú de interacción
    # Pasar opciones extra según contexto
    $ _opciones_extra_monica = []

    # Quest 0: botón "Agradecerle" — solo cuando la quest está lista y el MC
    # está a solas con Mónica (ningún otro NPC en la locación).
    $ _quest_m0 = sistema_quests.obtener_quest("monica_questprincipal_0")
    if (_quest_m0 and _quest_m0.activa and not _quest_m0.completada and
            _quest_m0.etapa_actual == ETAPA_BOTON_LISTO):
        $ _m0_presentes = npcs_en_locacion_actual()
        if len(_m0_presentes) == 1 and _m0_presentes[0].id == "monica":
            $ _opciones_extra_monica.append({
                "texto": "Agradecerle",
                "label": "monica_q0_agradecer",
                "condicion": True
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
    $ _quest_v09a_mon = sistema_quests.obtener_quest("violet_questprincipal_09_a")
    if (_quest_v09a_mon and _quest_v09a_mon.activa and not _quest_v09a_mon.completada and
            _quest_v09a_mon.etapa_actual == ETAPA_BOTON_LISTO):
        # "Preguntar por Violet" mientras el MC no sabe que está enferma
        if not getattr(store, 'mc_sabe_violet_enferma', False):
            $ _opciones_extra_monica.append({
                "texto": "Preguntar por Violet",
                "label": "violet_quest09a_monica_preguntar",
                "condicion": True
            })
        # "Te llama Violet" cuando Violet pidió que venga Monica y no se completó aún
        if (getattr(store, 'violet_9a_pedido_actual', None) == "Dile a Monica que venga" and
                not getattr(store, 'violet_9a_tiene_entregable', False)):
            $ _opciones_extra_monica.append({
                "texto": "Te llama Violet",
                "label": "violet_quest09a_monica_llamar",
                "condicion": True
            })

    call screen menu_interaccion_npc_completo(_npc_actual, opciones_extra=_opciones_extra_monica)

    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        $ _label_opcion_monica = _return[1]
        jump expression _label_opcion_monica

    return
