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
    
    # Obtener el evento (ya fue validado en game_loop con validar_eventos())
    $ _event_monica = obtener_event("monica_event_01")
    
    # Si el evento está visible y Mónica está en el living por la tarde, disparar el evento
    if _event_monica and _event_monica.estado == ESTADO_EVENT_VISIBLE:
        if monica_en_living_tarde():
            # Activar el evento y ejecutar su label
            $ _event_monica.activar()
            jump event_monica_01_narrativa
    
    # Verificar si hay quest lista para ejecutar
    $ _quest_activa = sistema_quests.obtener_quest_activa("monica")
    
    if _quest_activa and _quest_activa.etapa_actual == 5:
        $ exito, mensajes = _quest_activa.intentar_ejecutar()
        if exito:
            $ _npc_id_temp = "monica"
            jump ejecutar_quest_activa
    
    # Si no hay evento ni quest, mostrar menú de interacción
    # Pasar opciones extra según contexto
    $ _opciones_extra_monica = []
    
    # Si evento 1 completado y está en living por la tarde, agregar opción de repetir
    if monica_event_01_completado() and monica_en_living_tarde():
        $ _opciones_extra_monica.append({
            "texto": "¿Me das un masaje?",
            "label": "event_monica_01_check_replay",
            "condicion": True
        })
    
    call screen menu_interaccion_npc_completo(_npc_actual, opciones_extra=_opciones_extra_monica)

    if isinstance(_return, tuple) and _return[0] == "opcion_especial":
        $ _label_opcion_monica = _return[1]
        jump expression _label_opcion_monica

    return
