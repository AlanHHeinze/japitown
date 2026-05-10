################################################################################
## Labels de Acciones del Juego
################################################################################
## Labels que crean checkpoints guardables para todas las acciones del juego

# Variable temporal para pasar datos a los labels
default _hotspot_temp = None
default _locacion_temp = None


label accion_hotspot_move:

    # Verificar si el destino es habitación de NPC (door_access system)
    if _hotspot_temp and _hotspot_temp.destino in ["casa_hmonica", "casa_hviolet", "casa_hjasmine"]:

        # PRIORIDAD 1: Verificar restriccion de movimiento — tiene precedencia sobre el door access
        $ _msg_restriccion_puerta = accion_bloqueada_movimiento(_hotspot_temp.destino)
        if _msg_restriccion_puerta:
            piensa "[_msg_restriccion_puerta]"
            return

        # EXCEPCION: Omitir puerta si hay una restriccion con label para esta habitacion
        $ _omitir_puerta = False
        if hay_restriccion_activa() and restriccion_quest_activa.obtener_label_locacion(_hotspot_temp.destino):
            $ _omitir_puerta = True

        # EXCEPCION: Desde el baño de Monica a su habitacion no pasa por door access
        if not _omitir_puerta and _hotspot_temp.destino == "casa_hmonica":
            $ _loc_actual_id = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else None
            if _loc_actual_id == "casa_baniomonica":
                $ _omitir_puerta = True

        if not _omitir_puerta:
            # Guardar destino antes de salir del flujo
            $ _destino_puerta = _hotspot_temp.destino
            jump interaccion_puerta_npc
    
    if _hotspot_temp and _hotspot_temp.destino:
        # Verificar restricción de movimiento
        $ _msg_restriccion = accion_bloqueada_movimiento(_hotspot_temp.destino)
        if _msg_restriccion:
            piensa "[_msg_restriccion]"
            return
        
        $ exito = sistema_locaciones.mover_a_locacion(_hotspot_temp.destino)
        if exito:
            $ destino = sistema_locaciones.locacion_actual

            # Verificar mensajes en espera (condiciones de entrega)
            if hasattr(store, 'sistema_mensajes'):
                $ store.sistema_mensajes.verificar_mensajes_en_espera()

            # PRIORIDAD 3: Verificar si la restricción activa tiene un label para esta locación
            if hay_restriccion_activa() and destino:
                $ _label_locacion = restriccion_quest_activa.obtener_label_locacion(destino.id)
                if _label_locacion:
                    call expression _label_locacion from _call_expression
    
    return



label accion_hotspot_action:
    
    if _hotspot_temp:
        # Si el hotspot tiene un label definido, llamarlo directamente con call de Ren'Py
        if _hotspot_temp.label:
            call expression _hotspot_temp.label from _call_expression_1
            
        # FIX: Compatibilidad para saves viejos donde el hotspot dormir no tiene label
        elif _hotspot_temp.id == "dormir":
            call accion_dormir from _call_accion_dormir
            
        # Si tiene una acción Python, ejecutarla
        elif _hotspot_temp.accion:
            $ _hotspot_temp.accion()
        else:
            pass
    
    return


label accion_avanzar_tiempo:
    
    # Verificar restricción de quest/evento
    $ _msg_restriccion = accion_bloqueada("avanzar_tiempo")
    if _msg_restriccion:
        piensa "[_msg_restriccion]"
        return
    
    # Verificar si hay bloqueo de evento
    if hasattr(store, 'sistema_events') and sistema_events.hay_bloqueo("avanzar_tiempo"):
        piensa "No puedes avanzar el tiempo ahora."
        return
    
    $ avanzar_horario()
    
    return


label accion_ir_a_locacion:
    
    if _locacion_temp:
        # Verificar restricción de quest/evento
        $ _msg_restriccion = accion_bloqueada_movimiento(_locacion_temp)
        if _msg_restriccion:
            piensa "[_msg_restriccion]"
            return
        $ exito = sistema_locaciones.mover_a_locacion(_locacion_temp)
        # Verificar mensajes en espera (condiciones de entrega)
        if exito and hasattr(store, 'sistema_mensajes'):
            $ store.sistema_mensajes.verificar_mensajes_en_espera()
        if exito and hay_restriccion_activa():
            $ _dest_loc = sistema_locaciones.locacion_actual
            if _dest_loc:
                $ _label_loc = restriccion_quest_activa.obtener_label_locacion(_dest_loc.id)
                if _label_loc:
                    call expression _label_loc from _call_expression_2
    
    return

