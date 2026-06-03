################################################################################
## Labels de Acciones del Juego
################################################################################
## Labels que crean checkpoints guardables para todas las acciones del juego

# Variable temporal para pasar datos a los labels
default _hotspot_temp = None
default _locacion_temp = None
# (accion_locacion_temp_id se define en actionsystem_core.rpy)


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

    # Verificar si el destino es un baño ocupado por un NPC
    if _hotspot_temp and _hotspot_temp.destino in ["casa_banioarriba", "casa_baniomonica"]:
        $ _npc_banio_temp = obtener_npc_en_banio(_hotspot_temp.destino)
        if _npc_banio_temp:
            $ _msg_restriccion_banio = accion_bloqueada_movimiento(_hotspot_temp.destino)
            if _msg_restriccion_banio:
                piensa "[_msg_restriccion_banio]"
                return
            $ _destino_banio_npc = _hotspot_temp.destino
            jump interaccion_banio_ocupado

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

    # Verificar mensaje prioritario pendiente de respuesta
    $ _npc_prioritario = obtener_bloqueo_mensaje_prioritario()
    if _npc_prioritario:
        piensa "Debo responder el mensaje de [_npc_prioritario] antes de continuar"
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


################################################################################
## Label: Ejecutar acción de locación
################################################################################

label accion_locacion_ejecutar:

    # 1. Verificar restricción activa del sistema de quests/eventos
    $ _ale_msg = accion_bloqueada(_accion_locacion_temp_id)
    if _ale_msg:
        piensa "[_ale_msg]"
        return

    # 2. Si ya fue usada hoy y tiene mensaje de reintento — mostrar mensaje
    if not sistema_acciones.esta_disponible(_accion_locacion_temp_id):
        $ _ale_accion_ch = sistema_acciones.acciones.get(_accion_locacion_temp_id)
        if _ale_accion_ch and _ale_accion_ch.mensaje_reintento:
            $ _ale_msg_ch = renpy.translate_string(_ale_accion_ch.mensaje_reintento)
            piensa "[_ale_msg_ch]"
        return

    # 3. Listeners válidos registrados por quests/eventos
    $ _ale_listeners = sistema_acciones.preparar_ejecucion(_accion_locacion_temp_id)

    # 4. Sin listeners → ejecutar label genérico
    if not _ale_listeners:
        $ _ale_accion = sistema_acciones.acciones.get(_accion_locacion_temp_id)
        if _ale_accion and _ale_accion.label_generico:
            call expression _ale_accion.label_generico from _call_ale_generico
        else:
            piensa "No hay nada especial que hacer aquí ahora."
        return

    # 5. Un solo listener → ejecutar directamente
    if len(_ale_listeners) == 1:
        $ sistema_acciones.post_ejecutar(_accion_locacion_temp_id, _ale_listeners[0])
        call expression _ale_listeners[0].label from _call_ale_listener_unico
        return

    # 6. Múltiples listeners → menú de elección del jugador
    $ _ale_opciones = [(_ale_l.nombre_menu, _ale_l) for _ale_l in _ale_listeners]
    $ _ale_elegido = renpy.display_menu(_ale_opciones)
    $ sistema_acciones.post_ejecutar(_accion_locacion_temp_id, _ale_elegido)
    call expression _ale_elegido.label from _call_ale_listener_menu

    return

