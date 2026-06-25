################################################################################
## Eventos de Violet
################################################################################

default violet_limpieza_completada = False
default violet_ev03_pendiente_desde_dia = None
default violet_ev03_mensaje_disparado = False

init 10 python:

    # ===========================================================================
    # Funciones de condición para eventos de Violet (module-level para pickle)
    # ===========================================================================

    def condicion_aparicion_evento01_violet():
        """El evento aparece cuando la quest 0 de Violet está completada."""
        quest = sistema_quests.obtener_quest("violet_questprincipal_0_b")
        return quest is not None and quest.completada

    def condicion_aparicion_evento03_violet():
        """El evento aparece cuando la quest 03_a de Violet está completada."""
        quest = sistema_quests.obtener_quest("violet_questprincipal_0_b3_a")
        return quest is not None and quest.completada

    def condicion_activacion_evento03_violet():
        """Se activa cuando es sábado por la mañana y el mensaje de Monica fue completado."""
        dia = getattr(store, 'dia_semana_actual', 0)
        horario = getattr(store, 'horario_actual', 0)
        if dia != 5 or horario != 0:
            return False
        if not getattr(store, 'violet_ev03_mensaje_disparado', False):
            return False
        # El mensaje se envía el dia siguiente a violet_ev03_pendiente_desde_dia.
        # Bloqueamos activación en ese mismo dia para evitar que evento y mensaje
        # se disparen juntos en la misma mañana (ej: quest completa viernes, jugador
        # duerme directo al sábado).
        dias_actuales = getattr(store, 'dias_totales', 0)
        dia_visible = getattr(store, 'violet_ev03_pendiente_desde_dia', None)
        if dia_visible is None or dias_actuales <= dia_visible + 1:
            return False
        if not hasattr(store, 'sistema_mensajes'):
            return False
        return store.sistema_mensajes.grupo_completado("monica_chat_violet_quest2")

    def on_aparicion_evento03_violet():
        """Guarda el día en que el evento se volvió visible para enviar el mensaje al día siguiente."""
        store.violet_ev03_pendiente_desde_dia = getattr(store, 'dias_totales', 0)

    def inicializar_events_violet():
        """Inicializa todos los eventos de Violet."""

        # =====================================================================
        # EVENTO 01: Casco VR
        # =====================================================================
        # Aparece al completar la quest 0 de Violet (el casco se desbloquea en tienda)
        # Se dispara manualmente al usar el casco de noche con Violet en su habitacion

        evento01_violet = Event(
            id="violet_evento_01",
            nombre="Casco VR",
            tipo=TIPO_EVENT_ESPORADICO,
            prioridad=5,
            condicion_aparicion=condicion_aparicion_evento01_violet,
            npc_id="violet",
            config_etapas={
                ESTADO_EVENT_VISIBLE: ConfigEtapa(
                    pista="Siempre quise un casco VR, ahora que esta disponible podria comprarlo",
                    que_hacer="Comprar el casco VR y usarlo en tu habitacion por la noche",
                ),
            },
        )

        sistema_events.registrar_event(evento01_violet)

        # =====================================================================
        # EVENTO 03: Limpieza del Sábado
        # =====================================================================
        # Disponible luego de completar la quest 03_a
        # Se activa el sábado por la mañana
        # El jugador lo dispara desde el door access de la habitacion de Violet

        evento03_violet = Event(
            id="violet_evento_03",
            nombre="Limpieza del Sábado",
            tipo=TIPO_EVENT_ESPORADICO,
            prioridad=10,
            condicion_aparicion=condicion_aparicion_evento03_violet,
            condicion_activacion=condicion_activacion_evento03_violet,
            on_aparicion=on_aparicion_evento03_violet,
            label_efecto="evento03_violet",
            descripcion="Monica pidió que limpie la casa con Violet el sábado por la mañana.",
            npc_id="violet",
            mensaje_pista="Monica me pidió que limpie la casa con Violet el sábado por la mañana.",
            mensaje_que_hacer="Ir a la habitación de Violet el sábado por la mañana.",
            modificaciones={
                "rutinas": {
                    "violet":   {(5, 0): "casa_hviolet"},
                    "monica":   {(5, 0): "fuera"},
                    "jasmine":  {(5, 0): "fuera"},
                }
            },
            config_etapas={
                ESTADO_EVENT_VISIBLE: ConfigEtapa(
                    pista="Monica me pidió que limpie la casa con Violet el sábado por la mañana.",
                    que_hacer="Esperar al sábado por la mañana.",
                ),
                ESTADO_EVENT_ACTIVO: ConfigEtapa(
                    pista="Hoy es sábado, tengo que despertar a Violet para limpiar.",
                    que_hacer="Ir a la habitación de Violet.",
                    mensaje_despertar="Hoy es sábado, tengo que despertar a Violet para que limpiemos la casa.",
                ),
            },
        )

        # DESCONECTADO TEMPORALMENTE: el evento 03 (Limpieza del Sábado) no se
        # registra por ahora, asi que no aparece en el panel de pistas ni se
        # dispara. La definición de arriba y el label evento03_violet se dejan
        # intactos para reconectarlo en el futuro (basta descomentar la línea).
        # sistema_events.registrar_event(evento03_violet)


# Inicializar eventos de Violet al cargar el juego
init 11 python:
    inicializar_events_violet()


################################################################################
## Funciones auxiliares para eventos de Violet
################################################################################

init python:

    def violet_evento03_completado():
        """Verifica si el evento de limpieza de Violet está completado."""
        return getattr(store, 'violet_limpieza_completada', False)

    # Alias para compatibilidad
    def violet_event_limpieza_completado():
        return violet_evento03_completado()
