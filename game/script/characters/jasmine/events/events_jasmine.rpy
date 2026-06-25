################################################################################
## Eventos de Jasmine
################################################################################
## Definición de todos los eventos de Jasmine

init 10 python:

    # ===========================================================================
    # NOTA: La PRIMERA parte del evento 1 ("Ropa Nueva") se convirtió en la quest
    # jasmine_questprincipal_0_c. La cadena de quests es: 0_a → 0_b → 0_c.
    # El evento formal de abajo es solo la REPETICIÓN ("Volver a ver"): aparece en
    # el panel de pistas tras completar la 0_c y se dispara con el botón del menú.
    # ===========================================================================

    def condicion_aparicion_event1_jasmine():
        """Aparece (VISIBLE) tras completar la quest 0_c de Jasmine."""
        q = sistema_quests.obtener_quest("jasmine_questprincipal_0_c")
        return bool(q and q.completada)

    def condicion_activacion_event1_jasmine():
        """El evento NO se auto-activa por tiempo: lo dispara el botón
        'Volver a ver el conjunto' (ver interaccion_jasmine → check_replay).
        Devolver False evita que validar_eventos() lo saque de VISIBLE."""
        return False

    def inicializar_events_jasmine():
        """Inicializa todos los eventos de Jasmine."""

        # =====================================================================
        # EVENTO 1: Volver a ver (repetición del conjunto deportivo)
        # =====================================================================
        event_jasmine_01 = Event(
            id="jasmine_event_01",
            nombre="Volver a ver",
            tipo=TIPO_EVENT_ESPORADICO,
            prioridad=10,
            condicion_aparicion=condicion_aparicion_event1_jasmine,
            condicion_activacion=condicion_activacion_event1_jasmine,
            label_efecto="event_jasmine_01_check_replay",
            descripcion="Jasmine estrenó un conjunto deportivo nuevo.",
            npc_id="jasmine",
            mensaje_pista="Podría volver a ver el conjunto de Jasmine en el gym por la tarde.",
            mensaje_que_hacer="Habla con Jasmine en el gym por la tarde.",
            condicion_cierre_texto="",
            mensaje_despertar="Podría volver a ver el conjunto nuevo de Jasmine si la encuentro en el gym por la tarde.",
            config_etapas={
                ESTADO_EVENT_VISIBLE: ConfigEtapa(
                    pista="Podría volver a ver el conjunto de Jasmine en el gym por la tarde.",
                    que_hacer="Habla con Jasmine en el gym por la tarde.",
                    mensaje_despertar="Podría volver a ver el conjunto nuevo de Jasmine si la encuentro en el gym por la tarde.",
                ),
            },
        )

        sistema_events.registrar_event(event_jasmine_01)


# Inicializar eventos de Jasmine al cargar el juego
init 11 python:
    inicializar_events_jasmine()


################################################################################
## Funciones auxiliares para eventos de Jasmine
################################################################################

init python:

    def jasmine_event_01_completado():
        """Verifica si la quest 0_c de Jasmine está completada (conversión de evento 1)."""
        q = sistema_quests.obtener_quest("jasmine_questprincipal_0_c")
        return q and q.completada

    def jasmine_en_gym_tarde():
        """Verifica si Jasmine está en el gym por la tarde."""
        dia = getattr(store, 'dia_semana_actual', 0)
        horario = getattr(store, 'horario_actual', 0)

        # Obtener locación actual correctamente
        locacion_id = ""
        if hasattr(store, 'sistema_locaciones') and store.sistema_locaciones.locacion_actual:
            locacion_id = store.sistema_locaciones.locacion_actual.id

        return dia in [0, 1, 2, 3, 4] and horario == 1 and locacion_id == "casa_gym"
