################################################################################
## Eventos de Jasmine
################################################################################
## Definición de todos los eventos de Jasmine

init 10 python:

    # ===========================================================================
    # Funciones de condición para eventos de Jasmine (module-level para pickle)
    # ===========================================================================

    def condicion_aparicion_event1_jasmine():
        """El evento aparece cuando se completa la quest 0 de Jasmine."""
        quest = sistema_quests.obtener_quest("jasmine_questprincipal_0")
        return quest and quest.completada

    def condicion_activacion_event1_jasmine():
        """Se activa al interactuar con Jasmine en gym por la tarde."""
        # Verificar que es tarde (horario 1) y días de semana (0-4)
        dia = getattr(store, 'dia_semana_actual', 0)
        horario = getattr(store, 'horario_actual', 0)
        return dia in [0, 1, 2, 3, 4] and horario == 1

    def on_aparicion_event1_jasmine():
        """Se ejecuta cuando el evento aparece (se hace visible)."""
        # Activar skin de ropa deportiva automáticamente
        activar_skin("jasmine", "jasmine_entrenamiento_deportiva")

    def inicializar_events_jasmine():
        """Inicializa todos los eventos de Jasmine."""

        # =====================================================================
        # EVENTO 1: Ropa Nueva
        # =====================================================================
        # Se dispara al completar quest 0, activa skin deportiva
        # Al interactuar en gym por la tarde, ejecuta escena

        event_jasmine_01 = Event(
            id="jasmine_event_01",
            nombre="Ropa Nueva",
            tipo=TIPO_EVENT_ESPORADICO,
            prioridad=10,
            condicion_aparicion=condicion_aparicion_event1_jasmine,
            condicion_activacion=condicion_activacion_event1_jasmine,
            label_efecto="event_jasmine_01_mostrando_ropa",
            descripcion="Jasmine quiere mostrarte su ropa deportiva nueva",
            npc_id="jasmine",
            mensaje_pista="Jasmine me dijo que hoy la vea en el gym por la tarde.",
            mensaje_que_hacer="Ve al Gym por la tarde",
            condicion_cierre_texto="",
            mensaje_despertar="Jasmine me dijo que hoy la vea en el gym por la tarde.",
            config_etapas={
                ESTADO_EVENT_VISIBLE: ConfigEtapa(
                    pista="Jasmine me dijo que hoy la vea en el gym por la tarde.",
                    que_hacer="Ve al Gym por la tarde.",
                    mensaje_despertar="Jasmine me dijo que hoy la vea en el gym por la tarde.",
                ),
            },
        )

        # Guardar callback de aparición
        event_jasmine_01.on_aparicion = on_aparicion_event1_jasmine

        sistema_events.registrar_event(event_jasmine_01)


# Inicializar eventos de Jasmine al cargar el juego
init 11 python:
    inicializar_events_jasmine()


################################################################################
## Funciones auxiliares para eventos de Jasmine
################################################################################

init python:
    
    def jasmine_event_01_completado():
        """Verifica si el evento 1 de Jasmine está completado."""
        event = obtener_event("jasmine_event_01")
        return event and event.estado == ESTADO_EVENT_COMPLETADO
    
    def jasmine_en_gym_tarde():
        """Verifica si Jasmine está en el gym por la tarde."""
        dia = getattr(store, 'dia_semana_actual', 0)
        horario = getattr(store, 'horario_actual', 0)
        
        # Obtener locación actual correctamente
        locacion_id = ""
        if hasattr(store, 'sistema_locaciones') and store.sistema_locaciones.locacion_actual:
            locacion_id = store.sistema_locaciones.locacion_actual.id
        
        return dia in [0, 1, 2, 3, 4] and horario == 1 and locacion_id == "casa_gym"
