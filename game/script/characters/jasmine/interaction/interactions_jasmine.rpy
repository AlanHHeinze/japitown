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
    
    # Obtener el evento (ya fue validado en game_loop con validar_eventos())
    $ _event_jasmine = obtener_event("jasmine_event_01")
    
    # Si el evento está visible y Jasmine está en el gym por la tarde, disparar el evento
    if _event_jasmine and _event_jasmine.estado == ESTADO_EVENT_VISIBLE:
        if jasmine_en_gym_tarde():
            # Activar el evento y ejecutar su label
            $ _event_jasmine.activar()
            jump event_jasmine_01_mostrando_ropa
    
    # Verificar si hay quest lista para ejecutar
    $ _quest_activa = sistema_quests.obtener_quest_activa("jasmine")
    
    if _quest_activa and _quest_activa.etapa_actual == 5:
        # Quest lista, verificar validación especial
        $ exito, mensajes = _quest_activa.intentar_ejecutar()
        if exito:
            # Ejecutar quest directamente
            $ _npc_id_temp = "jasmine"
            jump ejecutar_quest_activa
    
    # Si no hay evento ni quest, mostrar menú de interacción
    # Pasar opciones extra según contexto
    $ _opciones_extra_jasmine = []
    
    # Si evento 1 completado y está en gym por la tarde, agregar opción de repetir
    if jasmine_event_01_completado() and jasmine_en_gym_tarde():
        $ _opciones_extra_jasmine.append({
            "texto": "¿Puedo ver cómo te queda otra vez?",
            "label": "event_jasmine_01_check_replay",
            "condicion": True
        })
    
    call screen menu_interaccion_npc_completo(_npc_actual, opciones_extra=_opciones_extra_jasmine)

    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        $ _label_opcion_jasmine = _return[1]
        jump expression _label_opcion_jasmine

    return
