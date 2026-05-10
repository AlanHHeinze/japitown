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
        """
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
        
        # Actualizar ubicaciones de NPCs
        if hasattr(store, 'actualizar_rutinas_npcs'):
            store.actualizar_rutinas_npcs()
        
        # Actualizar estado de quests (para verificar tiempos de espera)
        if hasattr(store, 'actualizar_quests'):
            store.actualizar_quests()

        # Verificar mensajes en espera (condiciones de entrega)
        if hasattr(store, 'sistema_mensajes'):
            store.sistema_mensajes.verificar_mensajes_en_espera()

        # Verificar entregas del sistema de compras
        if hasattr(store, 'sistema_compras'):
            entregas = store.sistema_compras.verificar_entregas_hoy()
            if entregas:
                store.repartidor_presente = True

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
    
    # Evento 2 de Violet: Se dispara al dormir después de completar Quest 7
    if store.sistema_quests.obtener_quest("violet_questprincipal_7") and store.sistema_quests.obtener_quest("violet_questprincipal_7").completada:
        if not violet_evento2_completado:
            jump evento2_violet



    # Ejecutar lógica de cambio de día
    $ dormir()

    # Mostrar mensajes al despertar (quests, eventos, pedidos nuevos)
    call mensajes_al_despertar from _call_mensajes_al_despertar

    # Quest 5 de Violet: auto-inicio al despertar
    if getattr(store, 'violet_quest5_inicio_pendiente', False):
        $ store.violet_quest5_inicio_pendiente = False
        $ quest_vq5 = sistema_quests.obtener_quest("violet_questprincipal_5")
        if quest_vq5 and quest_vq5.etapa_actual == ETAPA_BOTON_LISTO:
            $ quest_vq5.etapa_actual = ETAPA_DESARROLLO
            jump quest_violet_questprincipal_5

    # Verificar si hay entregas hoy
    if repartidor_presente:
        "El repartidor debería estar en la puerta con el pedido."
    
    # Forzar actualización asegurada
    $ renpy.restart_interaction()
    
    return
