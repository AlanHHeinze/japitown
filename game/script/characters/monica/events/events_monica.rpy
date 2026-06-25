################################################################################
## Eventos de Mónica
################################################################################
## Definición de todos los eventos de Mónica

# Variable para rastrear dia de completación de quest 0
default monica_quest_0_dia_completada = 0

init 10 python:

    # ===========================================================================
    # Funciones de condición para eventos de Mónica (module-level para pickle)
    # ===========================================================================

    def condicion_aparicion_event1_monica():
        """El evento aparece 2 días después de completar la quest 0 de Mónica."""
        quest = sistema_quests.obtener_quest("monica_questprincipal_0")
        if not quest or not quest.completada:
            return False

        # Verificar que hayan pasado al menos 2 dias desde la completación
        dia_completada = getattr(store, 'monica_quest_0_dia_completada', 0)
        dias_totales = getattr(store, 'dias_totales', 1)
        return dias_totales - dia_completada >= 2

    def condicion_activacion_event1_monica():
        """El evento NO se auto-activa por tiempo: lo dispara la interacción con
        Mónica en el living por la tarde (ver interaccion_monica, que exige estado
        VISIBLE y llama a activar() manualmente).

        Devolver False evita que validar_eventos() lo pase a ACTIVO apenas es de
        tarde — eso lo sacaba de estado VISIBLE y rompía el disparador."""
        return False

    def inicializar_events_monica():
        """Inicializa todos los eventos de Mónica."""

        # =====================================================================
        # EVENTO 1: Monica adolorida
        # =====================================================================
        # Se dispara 2 dias despues de completar quest 0
        # Al interactuar en living por la tarde, ejecuta escena

        event_monica_01 = Event(
            id="monica_event_01",
            nombre="Monica adolorida",
            tipo=TIPO_EVENT_ESPORADICO,
            prioridad=10,
            condicion_aparicion=condicion_aparicion_event1_monica,
            condicion_activacion=condicion_activacion_event1_monica,
            label_efecto="event_monica_01_narrativa",
            descripcion="Mónica se estuvo quejando de dolor en sus hombros",
            npc_id="monica",
            mensaje_pista="Podría ver a Monica en la tarde y ofrecerle un masaje.",
            mensaje_que_hacer="Habla con Monica cuando esté en el living por la tarde.",
            condicion_cierre_texto="",
            mensaje_despertar="Mónica se quejó de dolor en sus hombros, podría hacerle un masaje en la tarde.",
            config_etapas={
                ESTADO_EVENT_VISIBLE: ConfigEtapa(
                    pista="Podría ver a Monica en la tarde y ofrecerle un masaje.",
                    que_hacer="Habla con Monica cuando esté en el living por la tarde.",
                    mensaje_despertar="Mónica se quejó de dolor en sus hombros, podría hacerle un masaje en la tarde.",
                ),
            },
        )

        sistema_events.registrar_event(event_monica_01)


# Inicializar eventos de Mónica al cargar el juego
init 11 python:
    inicializar_events_monica()


################################################################################
## Funciones auxiliares para eventos de Mónica
################################################################################

init python:
    
    def monica_event_01_completado():
        """Verifica si el evento 1 de Mónica está completado."""
        event = obtener_event("monica_event_01")
        return event and event.estado == ESTADO_EVENT_COMPLETADO
    
    def monica_en_living_tarde():
        """Verifica si Mónica está en el living por la tarde."""
        horario = getattr(store, 'horario_actual', 0)
        
        # Obtener locación actual correctamente
        locacion_id = ""
        if hasattr(store, 'sistema_locaciones') and store.sistema_locaciones.locacion_actual:
            locacion_id = store.sistema_locaciones.locacion_actual.id
        
        return horario == 1 and locacion_id == "casa_living"
