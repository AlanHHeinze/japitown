################################################################################
## Sistema de Tiempo
################################################################################

## Inicialización de variables del sistema de tiempo
init python:
    # Configuración del calendario
    DIAS_POR_ESTACION = 31
    ESTACIONES = ["Primavera", "Verano", "Otoño", "Invierno"]
    DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    HORARIOS = ["Mañana", "Tarde", "Noche", "Trasnoche"]

# Variables del sistema de tiempo
default dia_actual = 1  # Día del mes (1-31)
default estacion_actual = 0  # Índice de la estación (0=Primavera, 1=Verano, 2=Otoño, 3=Invierno)
default año_actual = 1  # Año actual
default dia_semana_actual = 0  # Índice del día de la semana (0=Lunes, 6=Domingo)
default horario_actual = 0  # Índice del horario (0=Mañana, 1=Tarde, 2=Noche, 3=Trasnoche)
default dias_totales = 1  # Contador de días totales (para quests)

################################################################################
## Funciones del sistema de tiempo
################################################################################

init python:

    def actualizar_bg_master(con_fade=False):
        """Limpia el master layer y muestra el background de la locacion actual.
        Siempre limpia para eliminar sprites de quests que hayan quedado."""
        if not (hasattr(store, 'sistema_locaciones') and store.sistema_locaciones.locacion_actual):
            return
        bg_path = store.sistema_locaciones.locacion_actual.background
        if not bg_path:
            return
        renpy.scene(layer="master")
        renpy.show("_hud_bg", what=renpy.displayable(bg_path), layer="master")
        if con_fade:
            renpy.transition(Dissolve(1.5), layer="master")

    def avanzar_horario():
        """
        Avanza el horario al siguiente estado.
        Si está en Trasnoche, no avanza más.
        Si la quest 0_b de Jasmine está activa, no avanza el horario.
        """
        # Verificar si la quest 0_b de Jasmine está activa (restricción de horario)
        if hasattr(store, 'sistema_quests'):
            q_j0b = store.sistema_quests.obtener_quest("jasmine_questprincipal_0_b")
            if q_j0b and q_j0b.activa and not q_j0b.completada:
                return

        # Usar store directamente en lugar de global
        if store.horario_actual < 3:  # Si no es Trasnoche
            # Si era mañana y el repartidor estaba presente, se va y deja paquete
            if store.horario_actual == 0 and store.repartidor_presente:
                if hasattr(store, 'sistema_compras'):
                    store.sistema_compras.colocar_paquete_en_habitacion()
                # Hook para entregas de quest no recibidas
                if hasattr(store, 'manejar_quest1_violet_no_recibido'):
                    store.manejar_quest1_violet_no_recibido()
                store.repartidor_presente = False
            
            store.horario_actual += 1
            actualizar_bg_master(con_fade=True)

            # Actualizar ubicaciones de NPCs (desaparecen de inmediato)
            if hasattr(store, 'actualizar_rutinas_npcs'):
                store.actualizar_rutinas_npcs()

            # Ocultar sprites NPC durante la transicion del bg (se revelan al terminar)
            store.hud_npc_delay_horario = True
            
            # Verificar fallos de quests
            if hasattr(store, 'verificar_fallos_quests'):
                store.verificar_fallos_quests()

            # Verificar condiciones de quests en tiempo real
            if hasattr(store, 'actualizar_quests'):
                store.actualizar_quests()

            # Verificar mensajes en espera (condiciones de entrega)
            if hasattr(store, 'sistema_mensajes'):
                store.sistema_mensajes.verificar_mensajes_en_espera()
        else:
            pass

    def avanzar_horario_multiple(veces):
        """Avanza el horario N veces consecutivas."""
        for _i in range(veces):
            avanzar_horario()
        renpy.restart_interaction()

    def dormir():
        """
        Acción de dormir: avanza al día siguiente y resetea el horario a Mañana.
        """
        # Guardar horario antes de dormir para simular horarios omitidos después
        _horario_antes_dormir = store.horario_actual

        # Usar store directamente en lugar de global
        store.horario_actual = 0
        
        # Avanzar día de la semana
        store.dia_semana_actual = (store.dia_semana_actual + 1) % 7
        
        # Reponer stock de tienda al inicio de semana (Lunes)
        if store.dia_semana_actual == 0:
            if hasattr(store, 'reponer_stock'):
                store.reponer_stock()
        
        # Avanzar día del mes
        store.dia_actual += 1
        
        # Incrementar contador de días totales (para quests)
        store.dias_totales += 1
        
        # Verificar si se completa la estación
        if store.dia_actual > DIAS_POR_ESTACION:
            store.dia_actual = 1
            store.estacion_actual += 1
            
            # Verificar si se completa el año
            if store.estacion_actual >= len(ESTACIONES):
                store.estacion_actual = 0
                store.año_actual += 1

        
        # Resetear estado hover del icono de horario
        store._hud_horario_hover = False

        # Resetear límites diarios de entrenamiento y trabajo
        store.entrenamiento_hoy = False
        store.trabajo_hoy = 0

        # Resetear interacciones diarias de NPCs
        if hasattr(store, 'resetear_interacciones_todos_npcs'):
            store.resetear_interacciones_todos_npcs()
        
        # Evaluar rutinas especiales del nuevo día (antes de actualizar ubicaciones)
        if hasattr(store, 'sistema_npcs'):
            store.sistema_npcs.evaluar_todas_rutinas_especiales_dia(store.dia_semana_actual)

        # Actualizar ubicaciones de NPCs
        if hasattr(store, 'actualizar_rutinas_npcs'):
            store.actualizar_rutinas_npcs()
        
        # Actualizar estado de quests (para verificar tiempos de espera)
        if hasattr(store, 'actualizar_quests'):
            store.actualizar_quests()

        # Simular horarios omitidos al dormir: entrega mensajes que debían llegar esa noche
        if hasattr(store, 'sistema_mensajes'):
            store.sistema_mensajes.verificar_mensajes_horarios_omitidos(_horario_antes_dormir)

        # Verificar mensajes en espera (condiciones de entrega)
        if hasattr(store, 'sistema_mensajes'):
            store.sistema_mensajes.verificar_mensajes_en_espera()

        # Verificar entregas del sistema de compras
        if hasattr(store, 'sistema_compras'):
            entregas = store.sistema_compras.verificar_entregas_hoy()
            if entregas:
                store.repartidor_presente = True

        # Resetear acciones de locación
        if hasattr(store, 'sistema_acciones'):
            store.sistema_acciones.resetear_diario()
            if store.dia_semana_actual == 0:  # Lunes — resetear también semanales
                store.sistema_acciones.resetear_semanal()

        # Asignar nuevos estados de talk para el día que empieza
        if hasattr(store, 'sistema_talk'):
            for _npc_id_talk in ["violet", "monica", "jasmine"]:
                store.sistema_talk.decrementar_estados_especiales(_npc_id_talk)
                store.sistema_talk.asignar_estado_aleatorio(_npc_id_talk)


    def obtener_fecha_completa():
        """
        Retorna la fecha completa como string.
        """
        return f"{DIAS_SEMANA[dia_semana_actual]}, Día {dia_actual} de {ESTACIONES[estacion_actual]}, Año {año_actual}"
    
    def obtener_horario():
        """
        Retorna el horario actual como string.
        """
        return renpy.translate_string(HORARIOS[horario_actual])
    
    def obtener_estacion():
        """
        Retorna la estación actual como string.
        """
        return renpy.translate_string(ESTACIONES[estacion_actual])
    
    def obtener_dia_semana():
        """
        Retorna el día de la semana actual como string.
        """
        return renpy.translate_string(DIAS_SEMANA[dia_semana_actual])
    
    def es_fin_de_semana():
        """
        Retorna True si es Sábado o Domingo.
        """
        return dia_semana_actual >= 5
    
    def es_dia_especifico(dia_nombre):
        """
        Verifica si el día actual es el especificado.
        Ejemplo: es_dia_especifico("Lunes")
        """
        return DIAS_SEMANA[dia_semana_actual] == dia_nombre
    
    def es_estacion_especifica(estacion_nombre):
        """
        Verifica si la estación actual es la especificada.
        Ejemplo: es_estacion_especifica("Verano")
        """
        return ESTACIONES[estacion_actual] == estacion_nombre
    
    def es_horario_especifico(horario_nombre):
        """
        Verifica si el horario actual es el especificado.
        Ejemplo: es_horario_especifico("Noche")
        """
        return HORARIOS[horario_actual] == horario_nombre

################################################################################
## Labels útiles
################################################################################

label avanzar_tiempo:
    
    $ avanzar_horario()
    return

label accion_dormir:
    
    # Verificar restricción de quest/evento
    $ _msg_restriccion = accion_bloqueada("dormir")
    if _msg_restriccion:
        piensa "[_msg_restriccion]"
        return

    # Verificar mensaje prioritario ya entregado — bloquea dormir hasta responder
    $ _npc_prioritario = obtener_bloqueo_mensaje_prioritario()
    if _npc_prioritario:
        piensa "Debo responder el mensaje de [_npc_prioritario] antes de dormir"
        return

    # Verificar mensaje prioritario que llega mientras el jugador duerme — despertar anticipado
    $ _horario_despertar = obtener_horario_despertar_prioritario()
    if _horario_despertar is not None:
        call screen animacion_dormir with dissolve
        $ avanzar_horario_multiple(_horario_despertar - horario_actual)
        piensa "Me despertó un mensaje"
        return

    # Verificar si hay entrega de quest pendiente de Violet (repartidor o paquete en cama)
    if getattr(store, 'violet_quest1_entrega_pendiente', False):
        piensa "Tengo cosas pendientes por hacer, no puedo dormir ahora"
        return

    # Verificar si hay paquete bloqueando
    if paquete_en_habitacion:
        call intentar_dormir_con_paquete from _call_intentar_dormir_con_paquete
        return

    # Verificar si hay una entrega pendiente para hoy por la mañana
    if horario_actual == 0 and len(sistema_compras.verificar_entregas_hoy()) > 0:
        piensa "Tengo una entrega pendiente para hoy"
        return

    # Verificar si hay pensamientos disponibles
    $ _pensamientos_disponibles = obtener_pensamientos_disponibles()

    if _pensamientos_disponibles:
        label .menu_cama:
        menu:
            "Dormir":
                pass
            "Pensar":
                call screen menu_pensamientos(_pensamientos_disponibles)
                if _return == "volver" or not _return:
                    jump .menu_cama
                # Ejecutar el label del pensamiento seleccionado
                call expression _return from _call_expression_4
                # Al retornar, continúa al flujo de dormir

    # Llamar al screen como modal (espera a que el timer del screen haga Return())
    call screen animacion_dormir with dissolve
    
    # --- EVENTOS NOCTURNOS ---

    # Evento 2 de Violet: Se dispara al dormir 1 día después de completar Quest 04_e
    $ _quest_v04e = store.sistema_quests.obtener_quest("violet_questprincipal_04_e")
    $ _quest_v05a = store.sistema_quests.obtener_quest("violet_questprincipal_05_a")
    if (not violet_evento2_completado and
            _quest_v04e and _quest_v04e.completada and
            _quest_v05a and _quest_v05a.dia_inicio is not None and
            getattr(store, 'dias_totales', 1) > _quest_v05a.dia_inicio):
        jump evento2_violet



    # Ejecutar lógica de cambio de día
    $ dormir()

    # Hook Quest 0 del MC — primer sueño al finalizar la introducción
    if getattr(store, 'mc_q0_final_sleep', False):
        $ mc_q0_final_sleep = False
        $ desactivar_restriccion()
        $ sistema_quests_mc.completar_activa()
        $ config_mostrar_accion_movimiento = False
        $ visualizador_hotspot_activo = False

    # Quest 08_a de Violet: auto-trigger al despertar cuando está en ETAPA_BOTON_LISTO
    $ _quest_v08a = store.sistema_quests.obtener_quest("violet_questprincipal_08_a")
    if _quest_v08a and _quest_v08a.activa and not _quest_v08a.completada and _quest_v08a.etapa_actual == ETAPA_BOTON_LISTO:
        jump violet_quest08a_despertar

    # Quest 09_a de Violet: gestión diaria de la enfermedad
    $ _quest_v09a = store.sistema_quests.obtener_quest("violet_questprincipal_09_a")
    if _quest_v09a and _quest_v09a.activa and not _quest_v09a.completada and _quest_v09a.etapa_actual == ETAPA_BOTON_LISTO:
        # Penalizar si Violet pidió algo pero no se entregó antes de dormir
        if getattr(store, 'violet_9a_pedido_actual', None) and not getattr(store, 'violet_9a_entrega_completada', False):
            $ store.violet_enferma_atencion -= 1
        # Resetear estado diario
        $ store.violet_9a_pedido_actual = None
        $ store.violet_9a_tiene_entregable = False
        $ store.violet_9a_entrega_completada = False
        # Avanzar contador de días de enfermedad
        $ store.violet_9a_enfermedad_dia = getattr(store, 'violet_9a_enfermedad_dia', 0) + 1
        if store.violet_9a_enfermedad_dia >= 3:
            if getattr(store, 'violet_enferma_atencion', 0) >= 3:
                # Buen cuidado: disparar quest 09_b en lugar de dormir normalmente
                jump violet_quest09b_despertar
            else:
                # Cuidado insuficiente: completar 09_a y continuar el sueño normal
                $ completar_quest_actual("violet")

    # Evento 03 de Violet: enviar mensaje de Monica al día siguiente de completar quest 03_a
    $ _ev03_dia_pendiente = getattr(store, 'violet_ev03_pendiente_desde_dia', None)
    if (_ev03_dia_pendiente is not None and
            not getattr(store, 'violet_ev03_mensaje_disparado', False) and
            getattr(store, 'dias_totales', 0) > _ev03_dia_pendiente):
        $ store.sistema_mensajes.disparar_por_trigger("event_aparicion", "violet_quest2_chat_monica", "monica")
        $ store.violet_ev03_mensaje_disparado = True

    # Mostrar mensajes al despertar (quests, eventos, pedidos nuevos)
    call mensajes_al_despertar from _call_mensajes_al_despertar

    # Verificar si hay entregas hoy
    if repartidor_presente:
        "El repartidor debería estar en la puerta con el pedido."
    
    # Forzar actualización asegurada
    $ renpy.restart_interaction()
    
    return
