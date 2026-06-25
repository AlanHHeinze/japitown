################################################################################
## Interacciones de Jasmine
################################################################################

# Variable temporal para preview de skin
default _skin_preview_jasmine = None

label interaccion_jasmine:
    # Guardar NPC actual
    $ _npc_actual = obtener_npc("jasmine")
    
    if not _npc_actual:
        return
    
    # Quest 0_b: Ropa Nueva — disponible despues de completar quest 0
    $ _quest_j0b = sistema_quests.obtener_quest("jasmine_questprincipal_0_b")
    if (_quest_j0b and _quest_j0b.activa and not _quest_j0b.completada and
            _quest_j0b.etapa_actual == ETAPA_BOTON_LISTO and
            sistema_locaciones.locacion_actual and
            sistema_locaciones.locacion_actual.id == "casa_gym" and
            horario_actual == 1):
        $ _npc_id_temp = "jasmine"
        $ _quest_id_temp = "jasmine_questprincipal_0_b"
        jump ejecutar_quest_activa
    
    # Verificar si hay quest lista para ejecutar
    # Quests con validacion_especial de lugar/hora se manejan via opciones_extra
    $ _quest_activa = sistema_quests.obtener_quest_activa("jasmine")

    if _quest_activa and _quest_activa.etapa_actual == ETAPA_BOTON_LISTO:
        # Las quests 0_a/0_b/0_c se manejan via opciones_extra y triggers especiales
        # (lugar/hora), por eso NO deben auto-ejecutarse aqui.
        if _quest_activa.id not in ("jasmine_questprincipal_0_a", "jasmine_questprincipal_0_b", "jasmine_questprincipal_0_c"):
            $ exito, mensajes = _quest_activa.intentar_ejecutar()
            if exito:
                $ _npc_id_temp = "jasmine"
                jump ejecutar_quest_activa
            elif mensajes:
                $ _fallo_msg = mensajes[0]
                piensa "[_fallo_msg]"

    # Construir opciones extra
    $ _opciones_extra_jasmine = []

    # Quest 0_a: Reencuentro — solo disponible en gym por la tarde
    $ _quest_j0a = sistema_quests.obtener_quest("jasmine_questprincipal_0_a")
    if (_quest_j0a and _quest_j0a.activa and not _quest_j0a.completada and
            _quest_j0a.etapa_actual == ETAPA_BOTON_LISTO and
            sistema_locaciones.locacion_actual and
            sistema_locaciones.locacion_actual.id == "casa_gym" and
            horario_actual == 1):
        $ _opciones_extra_jasmine.append({
            "texto": "Saludar",
            "label": "quest_jasmine_questprincipal_0_a",
            "condicion": True
        })

    # Quest 0_b: Transición
    $ _quest_j0b = sistema_quests.obtener_quest("jasmine_questprincipal_0_b")
    if (_quest_j0b and _quest_j0b.activa and not _quest_j0b.completada and
            _quest_j0b.etapa_actual == ETAPA_BOTON_LISTO):
        $ _opciones_extra_jasmine.append({
            "texto": "¿Hay algo más que quieras decirme?",
            "label": "quest_jasmine_questprincipal_0_b",
            "condicion": True
        })

    # Quest 0_c: Mostrando Ropa (si está en gym por la tarde)
    $ _quest_j0c = sistema_quests.obtener_quest("jasmine_questprincipal_0_c")
    if (_quest_j0c and _quest_j0c.activa and not _quest_j0c.completada and
            _quest_j0c.etapa_actual == ETAPA_BOTON_LISTO and jasmine_en_gym_tarde()):
        $ _opciones_extra_jasmine.append({
            "texto": "¿Quería mostrarme algo?",
            "label": "quest_jasmine_questprincipal_0_c",
            "condicion": True
        })

    # Evento 1 "Volver a ver" (formal, aparece en el panel de pistas): tras
    # completar la quest 0_c, con Jasmine en el gym por la tarde aparece el botón
    # "Volver a ver el conjunto". La primera vez ejecuta event_jasmine_01_repetir
    # (que completa el evento); las siguientes, event_jasmine_01_repetir_alternativo
    # (lo decide event_jasmine_01_check_replay según el estado del evento).
    if jasmine_event_01_completado() and jasmine_en_gym_tarde():
        $ _opciones_extra_jasmine.append({
            "texto": "Volver a ver el conjunto",
            "label": "event_jasmine_01_check_replay",
            "condicion": True,
            "tipo": "evento"
        })

    # Quest 09_a: "Preguntar por Violet" mientras el MC no sabe que está enferma
    $ _quest_v09a_jas = sistema_quests.obtener_quest("violet_questprincipal_09_a")
    if (_quest_v09a_jas and _quest_v09a_jas.activa and not _quest_v09a_jas.completada and
            _quest_v09a_jas.etapa_actual == ETAPA_BOTON_LISTO and
            not getattr(store, 'mc_sabe_violet_enferma', False)):
        $ _opciones_extra_jasmine.append({
            "texto": "Preguntar por Violet",
            "label": "violet_quest09a_jasmine_preguntar",
            "condicion": True
        })

    call screen menu_interaccion_npc_completo(_npc_actual, opciones_extra=_opciones_extra_jasmine)

    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        $ _label_opcion_jasmine = _return[1]
        jump expression _label_opcion_jasmine

    return
