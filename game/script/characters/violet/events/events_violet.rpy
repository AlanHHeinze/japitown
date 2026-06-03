################################################################################
## Eventos de Violet
################################################################################

default violet_limpieza_completada = False

init 10 python:

    # ===========================================================================
    # Funciones de condición para eventos de Violet (module-level para pickle)
    # ===========================================================================

    def condicion_aparicion_evento01_violet():
        """El evento aparece cuando la quest 0 de Violet está completada."""
        quest = sistema_quests.obtener_quest("violet_questprincipal_0")
        return quest is not None and quest.completada

    def condicion_aparicion_evento03_violet():
        """El evento aparece cuando la quest 03_a de Violet está completada."""
        quest = sistema_quests.obtener_quest("violet_questprincipal_03_a")
        return quest is not None and quest.completada

    def condicion_activacion_evento03_violet():
        """Se activa cuando es sábado por la mañana."""
        dia = getattr(store, 'dia_semana_actual', 0)
        horario = getattr(store, 'horario_actual', 0)
        return dia == 5 and horario == 0

    def on_aparicion_evento03_violet():
        """Dispara el chat de Monica al aparecer el evento de limpieza."""
        if hasattr(store, 'sistema_mensajes'):
            store.sistema_mensajes.disparar_por_trigger("event_aparicion", "violet_quest2_chat_monica", "monica")

    def inicializar_events_violet():
        """Inicializa todos los eventos de Violet."""

        # =====================================================================
        # EVENTO 01: Casco VR
        # =====================================================================
        # Aparece al completar la quest 0 de Violet (el casco se desbloquea en tienda)
        # Se dispara manualmente al usar el casco de noche con Violet en su habitación

        evento01_violet = Event(
            id="violet_evento_01",
            nombre="Casco VR",
            tipo=TIPO_EVENT_ESPORADICO,
            prioridad=5,
            condicion_aparicion=condicion_aparicion_evento01_violet,
            npc_id="violet",
            config_etapas={
                ESTADO_EVENT_VISIBLE: ConfigEtapa(
                    pista="Podría probar el casco VR.",
                    que_hacer="Comprar el casco VR.",
                ),
            },
        )

        sistema_events.registrar_event(evento01_violet)

        # =====================================================================
        # EVENTO 03: Limpieza del Sábado
        # =====================================================================
        # Disponible luego de completar la quest 03_a
        # Se activa el sábado por la mañana
        # El jugador lo dispara desde el door access de la habitación de Violet

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
            mensaje_despertar="Hoy es sábado, tengo que despertar a Violet para que limpiemos la casa.",
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
                    mensaje_despertar="Este sábado tengo que despertar a Violet para limpiar la casa.",
                ),
                ESTADO_EVENT_ACTIVO: ConfigEtapa(
                    pista="Hoy es sábado, tengo que despertar a Violet para limpiar.",
                    que_hacer="Ir a la habitación de Violet.",
                    mensaje_despertar="Hoy es sábado, tengo que despertar a Violet para que limpiemos la casa.",
                ),
            },
        )

        sistema_events.registrar_event(evento03_violet)


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
