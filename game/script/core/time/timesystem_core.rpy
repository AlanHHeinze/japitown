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
default dia_actual = 1  # Dia del mes (1-31)
default estacion_actual = 0  # Índice de la estación (0=Primavera, 1=Verano, 2=Otoño, 3=Invierno)
default año_actual = 1  # Año actual
default dia_semana_actual = 0  # Índice del dia de la semana (0=Lunes, 6=Domingo)
default horario_actual = 0  # Índice del horario (0=Mañana, 1=Tarde, 2=Noche, 3=Trasnoche)
default dias_totales = 1  # Contador de dias totales (para quests)

################################################################################
## Funciones del sistema de tiempo
################################################################################

init python:

    # Suscriptores a "el repartidor se fue sin ser atendido". El contenido se
    # registra en init 5 (ej. violet_quest_01_a) con funciones de MODULO sin
    # argumentos; el motor solo itera la lista y no conoce ninguna quest.
    # (Refactor C3 de arquitectura_sistemas.md)
    REPARTIDOR_AL_IRSE = []

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

    def jp_nombre_guardado():
        """
        Texto que identifica la partida en los slots de Guardar/Cargar.

        Va por DOS caminos distintos, por eso es una funcion y no un string:
        - Guardados manuales: lo toman de la variable `save_name`, que Ren'Py
        pasa como extra_info (00action_file.rpy:415). Hay que mantenerla al dia.
        - Autoguardados: lo toman de config.auto_save_extra_info, que se evalua
        en el momento de guardar, asi que siempre sale fresco.

        Ambos terminan en el campo `_save_name` del save, que es lo que lee
        FileSaveName() en la pantalla de slots.
        """
        return renpy.translate_string("Día {dia}").format(
            dia=getattr(store, 'dias_totales', 1)
        )

    # Los autoguardados evaluan esto al guardar (loadsave.py:253).
    config.auto_save_extra_info = jp_nombre_guardado

    def avanzar_horario():
        """
        Avanza el horario al siguiente estado.
        Si está en Trasnoche, no avanza más.

        NOTA (refactor C2): acá había un if que congelaba el horario mientras
        la quest 0_b de Jasmine estuviera activa. Se eliminó porque era peso
        muerto: la 0_b pasa de no-iniciada a BOTON_LISTO en un solo tick del
        game_loop (dias_espera=0, sin requisitos) y su escena activa una
        restricción que ya bloquea avanzar_tiempo, dormir y cheats. El motor
        no debe conocer quests por nombre; los bloqueos van por restricción.
        """
        # Usar store directamente en lugar de global
        if store.horario_actual < 3:  # Si no es Trasnoche
            # Si era mañana y el repartidor estaba presente, se va y deja paquete
            if store.horario_actual == 0 and store.repartidor_presente:
                if hasattr(store, 'sistema_compras'):
                    store.sistema_compras.colocar_paquete_en_habitacion()
                # Avisar al contenido suscripto (entregas de quest no recibidas)
                for _rep_fn in REPARTIDOR_AL_IRSE:
                    _rep_fn()
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

    def autoguardar_partida():
        """
        Autoguardado en un punto seguro. Se usa al dormir, para que el jugador
        pueda recuperar la partida si el juego crashea durante el dia.

        IMPORTANTE — por que hace checkpoint() ANTES del autosave:
        al cargar una partida, Ren'Py no resume en el statement exacto del
        guardado: `unfreeze_core` termina llamando a `rollback_core(0)`, o sea
        hace rollback hasta el ULTIMO CHECKPOINT (loadsave/rollback.py). Los
        checkpoints normalmente solo se crean en interacciones (dialogo, menus).
        Sin este checkpoint explicito, cargar el autosave podria retroceder hasta
        antes de la llamada a dormir() y re-ejecutarla, avanzando el dia dos
        veces. renpy.checkpoint() marca ESTE punto exacto como restaurable.

        Llamar SIEMPRE como statement propio de script, nunca desde adentro de
        dormir(): si el checkpoint cayera sobre la linea que ejecuta dormir(),
        volveriamos a tener el riesgo de la doble ejecucion.

        POR QUE SE REPLICAN LAS GUARDAS DE force_autosave():
        esa funcion no devuelve nada y se cancela EN SILENCIO en 6 casos
        distintos (loadsave.py:325-350). Sin replicar los chequeos no hay forma
        de distinguir "guardo" de "no hizo nada": ni para avisarle al jugador sin
        mentirle, ni para diagnosticar por que un dia no se guardo.
        """
        renpy.checkpoint()

        _motivo = None
        if not config.has_autosave:
            _motivo = "config.has_autosave=False"
        elif not getattr(store, "_autosave", True):
            _motivo = "_autosave=False"
        elif renpy.game.after_rollback or renpy.in_rollback():
            # Ren'Py no guarda mientras hay rollback pendiente (la pila de
            # roll-forward se llena cuando el jugador rebobina con la rueda).
            _motivo = "rollback pendiente"
        elif getattr(store, "main_menu", False):
            _motivo = "menu principal"
        elif getattr(store, "_in_replay", None):
            _motivo = "replay"

        if _motivo:
            if config.developer:
                print("[Autosave] omitido al dormir: {}".format(_motivo))
            return

        # block=True (guarda en el hilo principal) a proposito. Con el modo
        # background, autosave_thread_function() envuelve todo en
        # `except Exception: pass`, asi que un fallo de guardado (ej. un
        # PicklingError por un callable no picklable) seria COMPLETAMENTE
        # invisible: ni error, ni partida guardada. Justo en el sistema que
        # existe para recuperarse de crashes, eso es inaceptable — preferimos
        # que reviente y se vea. Ademas evita la carrera del flag
        # autosave_not_running, que descarta el guardado si el hilo anterior
        # sigue corriendo. En web Ren'Py ya lo corre sincronico igual.
        #
        # Se llama a la funcion ORIGINAL, no a renpy.force_autosave: esa quedo
        # pisada por core/utils/autosave_filtrado.rpy con una version que
        # descarta todo, para que los disparadores del motor (menu principal,
        # salir, cargar) no llenen los slots. Este es el UNICO camino que
        # realmente guarda.
        _jp_force_autosave_real(block=True)

        # Aviso al jugador (notificacion no bloqueante de la cola izquierda).
        notificar_partida_guardada()

    def dormir():
        """
        Accion de dormir: avanza al dia siguiente y resetea el horario a Mañana.
        """
        # Fin del efecto de la Poción de Conquista (dura hasta dormir)
        store.pocion_conquista_activa = False

        # Guardar horario antes de dormir para simular horarios omitidos despues
        _horario_antes_dormir = store.horario_actual

        # Usar store directamente en lugar de global
        store.horario_actual = 0
        
        # Avanzar dia de la semana
        store.dia_semana_actual = (store.dia_semana_actual + 1) % 7
        
        # Reponer stock de tienda al inicio de semana (Lunes)
        if store.dia_semana_actual == 0:
            if hasattr(store, 'reponer_stock'):
                store.reponer_stock()
        
        # Avanzar dia del mes
        store.dia_actual += 1
        
        # Incrementar contador de dias totales (para quests)
        store.dias_totales += 1

        # Refrescar la etiqueta de los slots de guardado (los guardados manuales
        # leen `save_name` tal como esté en ese momento).
        store.save_name = jp_nombre_guardado()
        
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
        
        # Evaluar rutinas especiales del nuevo dia (antes de actualizar ubicaciones)
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
            if store.dia_semana_actual == 0:  # Lunes — resetear tambien semanales
                store.sistema_acciones.resetear_semanal()

        # Asignar nuevos estados de talk para el dia que empieza
        if hasattr(store, 'sistema_talk'):
            for _npc_id_talk in ["violet", "monica", "jasmine"]:
                store.sistema_talk.decrementar_estados_especiales(_npc_id_talk)
                store.sistema_talk.asignar_estado_aleatorio(_npc_id_talk)


    def obtener_fecha_completa():
        """
        Retorna la fecha completa como string.
        """
        return f"{DIAS_SEMANA[dia_semana_actual]}, Día {dia_actual} de {ESTACIONES[estacion_actual]}, Año {ano_actual}"
    
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
        Retorna el dia de la semana actual como string.
        """
        return renpy.translate_string(DIAS_SEMANA[dia_semana_actual])
    
    def es_fin_de_semana():
        """
        Retorna True si es Sábado o Domingo.
        """
        return dia_semana_actual >= 5
    
    def es_dia_especifico(dia_nombre):
        """
        Verifica si el dia actual es el especificado.
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

    # Embudo unico de bloqueos (C11): restriccion + bloqueos de events +
    # mensaje prioritario sin responder + bloqueos registrados por contenido
    # (ej. la entrega pendiente de la quest 1 de Violet). Una sola consulta.
    $ _msg_restriccion = accion_bloqueada("dormir")
    if _msg_restriccion:
        $ _blk_guardar_toque()
        piensa "[_msg_restriccion]"
        return

    # Mensaje prioritario que llega mientras el jugador duerme — despertar
    # anticipado. Es un flujo alternativo, no un bloqueo: por eso vive aca y
    # no en el embudo.
    $ _horario_despertar = obtener_horario_despertar_prioritario()
    if _horario_despertar is not None:
        call screen animacion_dormir with dissolve
        $ avanzar_horario_multiple(_horario_despertar - horario_actual)
        $ _blk_guardar_toque()
        piensa "Me despertó un mensaje"
        return

    # Verificar si hay paquete bloqueando
    if paquete_en_habitacion:
        call intentar_dormir_con_paquete from _call_intentar_dormir_con_paquete
        return

    # Verificar si hay una entrega pendiente para hoy por la mañana
    if horario_actual == 0 and len(sistema_compras.verificar_entregas_hoy()) > 0:
        $ _blk_guardar_toque()
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
            "Volver":
                return

    # Llamar al screen como modal (espera a que el timer del screen haga Return())
    call screen animacion_dormir with dissolve

    # Triggers de contenido ANTES de avanzar el dia (registro
    # TRIGGERS_DORMIR fase "antes"; ej. eventos nocturnos como el evento 2
    # de Violet). El motor no conoce quests ni eventos por nombre.
    $ _trigger_dormir = ejecutar_triggers_dormir("antes")
    if _trigger_dormir:
        jump expression _trigger_dormir

    # Ejecutar lógica de cambio de dia
    $ dormir()

    # Autoguardado del nuevo dia. Va justo despues de dormir() a proposito: los
    # bloqueos de "no podes dormir" ya retornaron antes, y TODO el contenido del
    # dia nuevo (triggers de quest al despertar, mensajes, eventos) pasa despues
    # — asi que si algo de eso crashea, el autosave es anterior al problema.
    $ autoguardar_partida()

    # Triggers de contenido DESPUES del autosave (registro TRIGGERS_DORMIR
    # fase "despues": hooks de fin de intro, escenas al despertar, gestion
    # diaria de quests, mensajes diferidos). Si un trigger devuelve label se
    # saltean los siguientes Y los mensajes al despertar — misma semantica
    # que los jumps encadenados que reemplaza este registro.
    $ _trigger_dormir = ejecutar_triggers_dormir("despues")
    if _trigger_dormir:
        jump expression _trigger_dormir

    # Mostrar mensajes al despertar (quests, eventos, pedidos nuevos)
    call mensajes_al_despertar from _call_mensajes_al_despertar

    # Verificar si hay entregas hoy
    if repartidor_presente:
        "El repartidor debería estar en la puerta con el pedido."
    
    # Forzar actualización asegurada
    $ renpy.restart_interaction()
    
    return
